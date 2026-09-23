"""Rebuild the embedded CC0 instrument bank. Requires numpy, scipy, soundfile, imageio-ffmpeg.

Run from any directory: python films/nonpareil/build-sample-bank.py --embed
Handpan: Freesound pack 33041 "HandPan 1st model" by GAMEDRIX974 (CC0), taken from
its public HQ previews. Bass: cello section and solo contrabass from VSCO 2 Community
Edition (CC0), pinned to one commit. Downloads and prepared Oggs go in
out/nonpareil-samples/. The manifest keeps source and encoded hashes, the measured
root of every recording and its tuning correction. --embed changes only the JSON bank.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import urllib.parse
import urllib.request

import imageio_ffmpeg
import numpy as np
from scipy.signal import resample_poly
import soundfile as sf

FILM = Path(__file__).resolve().parent
ROOT = FILM.parents[1]
CACHE = ROOT / 'out' / 'nonpareil-samples'
REUSE = ROOT / 'out' / 'roost-string-source'      # same pinned VSCO files, already downloaded
VSCO = 'https://raw.githubusercontent.com/sgossner/VSCO-2-CE/440300901dfe9275fd84e0b7763af1f8443ae62e/'
FREESOUND = 'https://cdn.freesound.org/previews/587/{id}_2214720-hq.mp3'
RATE = 48000
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# (instrument, nominal midi from inspection, source, seconds kept, mono)
# Handpan takes were identified by their f, 2f, 3f partials; where a note has two
# takes the longer-ringing one is kept. 7.wav duplicates 11.wav and is left out.
HANDPAN = [(38, 587404, '1.wav'), (48, 587412, '2.wav'), (50, 587418, '5.wav'), (52, 587413, '8.wav'),
           (53, 587414, '4.wav'), (55, 587415, '9.wav'), (57, 587411, '3.wav'), (60, 587402, '11.wav'),
           (62, 587407, '14.wav'), (64, 587410, '17.wav'), (65, 587408, '13.wav'), (67, 587409, '18.wav'),
           (69, 587416, '6.wav'), (72, 587405, '16.wav'), (81, 587406, '15.wav')]
SOURCES = [('handpan', m, dict(freesound=i, name=n), 7.5, True) for m, i, n in HANDPAN]
for m, p in [(36, 'C1'), (40, 'E1'), (43, 'G1'), (47, 'B1'), (50, 'D2'), (53, 'F2'), (57, 'A2')]:
    SOURCES.append(('cello', m, dict(vsco=f'Strings/Cello Section/susvib/susvib_{p}_v1_1.wav'), 6.4, False))
for m, p in [(28, 'E0'), (31, 'G0'), (34, 'A#0'), (36, 'C1'), (38, 'D1')]:
    SOURCES.append(('bass', m, dict(vsco=f'Strings/Solo Contrabass/SusNV/BKCtbss_SusNV_{p}_v1_rr1.wav'), 6.4, False))
SUSTAINED = {'cello', 'bass'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def get(url, dst):
    if not dst.exists():
        req = urllib.request.Request(url, headers={'User-Agent': 'riso-nonpareil'})
        with urllib.request.urlopen(req, timeout=90) as response:
            dst.write_bytes(response.read())
    return dst


def fetch(src):
    """Local path of a source recording (WAV), downloading once."""
    if 'vsco' in src:
        dst = CACHE / Path(src['vsco']).name
        old = REUSE / dst.name
        if not dst.exists() and old.exists():
            shutil.copyfile(old, dst)
        return get(VSCO + urllib.parse.quote(src['vsco']), dst), VSCO + src['vsco']
    url = FREESOUND.format(id=src['freesound'])
    mp3 = get(url, CACHE / f"handpan-{src['freesound']}.mp3")
    wav = mp3.with_suffix('.wav')
    if not wav.exists():
        subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', str(mp3), str(wav)], check=True)
    return mp3, url


def peak_near(spectrum, f, center, cents=45):
    lo, hi = center * 2 ** (-cents / 1200), center * 2 ** (cents / 1200)
    idx = np.flatnonzero((f > lo) & (f < hi))
    if len(idx) < 3:
        return 0.0, center
    i = idx[np.argmax(spectrum[idx])]
    a, b, c = np.log(spectrum[i - 1:i + 2] + 1e-12)
    delta = .5 * (a - c) / (a - 2 * b + c)
    return float(spectrum[i]), float((i + delta) * (f[1] - f[0]))


def measure_root(y, sr, nominal, sustained, octaves=range(-2, 4)):
    """The sounding fundamental of the nominal pitch class, octaves -2..+3. A
    candidate is scored by its odd harmonics (f, 3f, 5f): an octave too low
    finds none of them, and the lowest candidate that finds them is the note.
    VSCO's older string files name pitches an octave low; handpan tones are
    tuned f, 2f, 3f with the octave often stronger than the fundamental."""
    mono = y.mean(axis=1)
    start = int((0.6 if sustained else 0.12) * sr)
    seg = mono[start:start + int(1.2 * sr)]
    n = 1 << 19
    spectrum = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n))
    f = np.fft.rfftfreq(n, 1 / sr)
    cands = []
    for k in octaves:
        m = nominal + 12 * k
        hz = 440 * 2 ** ((m - 69) / 12)
        if hz < 25 or hz > 9000:
            continue
        mag, at = peak_near(spectrum, f, hz)
        score = sum(peak_near(spectrum, f, hz * h, 30)[0] for h in (1, 3, 5) if hz * h < 12000)
        cands.append((m, score, at))
    top = max(c[1] for c in cands)
    for m, score, at in cands:
        if score > 0.3 * top:
            hz = 440 * 2 ** ((m - 69) / 12)
            return m, 1200 * np.log2(at / hz)
    raise ValueError('no fundamental')


def build():
    CACHE.mkdir(parents=True, exist_ok=True)
    previous_path = FILM / 'sample-bank-manifest.json'
    previous = json.loads(previous_path.read_text()) if previous_path.exists() else {}
    expected = {s['source']: s['sourceSha256'] for s in previous.get('samples', [])}
    (FILM / 'VSCO-LICENSE.txt').write_bytes(get(VSCO + 'LICENSE', CACHE / 'VSCO-LICENSE').read_bytes())
    bank = dict(format='audio/ogg; codecs=vorbis', sampleRate=RATE, license='CC0-1.0', libraries=[
        dict(name='HandPan 1st model', author='GAMEDRIX974', license='CC0-1.0',
             source='https://freesound.org/people/GAMEDRIX974/packs/33041/',
             note='Freesound HQ previews (128 kb/s MP3) of the CC0 originals'),
        dict(name='VSCO 2 Community Edition', author='Versilian Studios', license='CC0-1.0',
             source='https://github.com/sgossner/VSCO-2-CE',
             recordings='Sam Gossner and Simon Dalzell; sample cutting Elan Hickler / Soundemote')], samples=[])
    for instrument, nominal, src, keep, mono in SOURCES:
        path, url = fetch(src)
        digest = sha(path.read_bytes())
        if url in expected and expected[url] != digest:
            raise ValueError(f'Source hash changed: {url}')
        y, sr = sf.read(path.with_suffix('.wav') if path.suffix == '.mp3' else path, always_2d=True)
        if sr not in [44100, RATE]:
            raise ValueError(f'Unexpected sample rate {sr}')
        y = y - y.mean(axis=0)
        sustained = instrument in SUSTAINED
        step = max(1, int(.005 * sr))
        energy = np.array([np.sqrt(np.mean(y[i:i + step] ** 2)) for i in range(0, len(y) - step, step)])
        audible = np.flatnonzero(energy > energy.max() * (.035 if sustained else .02))
        trim = max(0, int(audible[0] * step - (.025 if sustained else .004) * sr))
        y = y[trim:]
        # handpan roots were read from each take's f, 2f, 3f partials by hand; sympathetic
        # ringing of neighbouring tone fields can fake a lower series, so only tuning is measured
        root, cents = measure_root(y, sr, nominal, sustained, [0] if instrument == 'handpan' else range(-2, 4))
        if not sustained:
            # keep until the ring falls 50 dB under its peak, at most `keep` seconds
            env = np.array([np.sqrt(np.mean(y[i:i + step] ** 2)) for i in range(0, len(y) - step, step)])
            quiet = np.flatnonzero(env > env.max() * 10 ** (-50 / 20))
            keep = min(keep, (quiet[-1] + 1) * step / sr + .05)
        y = y[:int(keep * sr)]
        if mono:
            y = y.mean(axis=1, keepdims=True)
        else:
            mid, side = y.mean(axis=1), (y[:, 0] - y[:, 1]) * .5 * (.15 if instrument == 'bass' else .3)
            y = np.column_stack((mid + side, mid - side))
        if sustained:
            body = y[int(.5 * sr):int(min(4.5, len(y) / sr - .3) * sr)]
            gain = min(.085 / float(np.sqrt(np.mean(body ** 2))), .82 / max(abs(y).max(), 1e-9))
        else:
            # struck: match the first 300 ms of body rather than the transient
            body = y[:int(.3 * sr)]
            gain = min(.16 / float(np.sqrt(np.mean(body ** 2))), .85 / max(abs(y).max(), 1e-9))
        y = y * gain
        fade_in = int((.012 if sustained else .0015) * sr)
        y[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
        fade_out = int(min(.25, len(y) / sr * .2) * sr)
        y[-fade_out:] *= (np.linspace(1, 0, fade_out) ** 2)[:, None]
        if sr == 44100:
            y = resample_poly(y, 160, 147, axis=0)
        stem = f'{instrument}-{root}'
        wav, ogg = CACHE / (stem + '.prep.wav'), CACHE / (stem + '.ogg')
        sf.write(wav, y, RATE, subtype='PCM_24')
        subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', str(wav), '-map_metadata', '-1',
                        '-c:a', 'libvorbis', '-q:a', '5', str(ogg)], check=True)
        encoded = ogg.read_bytes()
        sample = dict(instrument=instrument, root=root, source=url, sourceSha256=digest,
                      encodedSha256=sha(encoded), sourceRate=sr, trimSeconds=round(trim / sr, 4),
                      gain=round(gain, 4), channels=y.shape[1], tuneCents=round(-cents, 2),
                      seconds=round(len(y) / RATE, 3), audio=base64.b64encode(encoded).decode())
        if 'name' in src:
            sample['freesoundName'] = src['name']
        bank['samples'].append(sample)
        print(f'{stem:12s} {len(y) / RATE:5.2f}s  tuning {-cents:+6.1f} c  {y.shape[1]}ch  '
              f'{len(encoded) // 1024} KiB  {src.get("name", "")}', flush=True)
    manifest = {**bank, 'samples': [{k: v for k, v in s.items() if k != 'audio'} for s in bank['samples']]}
    previous_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    payload = json.dumps(bank, separators=(',', ':'))
    (CACHE / 'sample-bank.json').write_text(payload, encoding='utf-8')
    return payload


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--embed', action='store_true')
    args = parser.parse_args()
    payload = build()
    if args.embed:
        html = FILM / 'index.html'
        text = html.read_text(encoding='utf-8')
        block = '<script id="sample-bank" type="application/json">\n' + payload + '\n</script>'
        pattern = r'<script id="sample-bank" type="application/json">[\s\S]*?</script>'
        if re.search(pattern, text):
            text = re.sub(pattern, lambda _: block, text)
        else:
            text = text.replace('</html>', block + '\n</html>')
        html.write_text(text, encoding='utf-8')
    print(f'PASS: {len(SOURCES)} CC0 recordings; bank {len(payload) / 1048576:.2f} MiB')
