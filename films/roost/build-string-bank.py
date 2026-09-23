"""Rebuild the embedded CC0 strings. Requires numpy, scipy, soundfile, imageio-ffmpeg.

Run from any directory: python films/roost/build-string-bank.py --embed
Downloads are pinned; source WAVs and prepared Oggs go in out/roost-string-source/.
The manifest keeps source and encoded hashes. --embed changes only the JSON bank.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.parse
import urllib.request

import imageio_ffmpeg
import numpy as np
from scipy.signal import resample_poly
import soundfile as sf

FILM = Path(__file__).resolve().parent
CACHE = FILM.parents[1] / 'out' / 'roost-string-source'
REPO = 'sgossner/VSCO-2-CE'
COMMIT = '440300901dfe9275fd84e0b7763af1f8443ae62e'
RAW = f'https://raw.githubusercontent.com/{REPO}/{COMMIT}/'
RATE = 48000

# The older cello/bass files use C3 for middle C; the arco violin uses C4.
# Roots below are scientific MIDI pitches, checked against the recorded partials.
SOURCES = []
for pitch, root in [('C1',36),('E1',40),('G1',43),('B1',47),('D2',50),
                    ('F2',53),('A2',57),('C3',60)]:
    SOURCES.append(('cello', root, f'Strings/Cello Section/susvib/susvib_{pitch}_v1_1.wav'))
for pitch, root in [('E0',28),('G0',31),('A#0',34),('C1',36),('D1',38)]:
    SOURCES.append(('bass', root, f'Strings/Solo Contrabass/SusNV/BKCtbss_SusNV_{pitch}_v1_rr1.wav'))
for pitch, root in [('G3',55),('A3',57),('C4',60),('E4',64),('G4',67),
                    ('A4',69),('C5',72),('E5',76)]:
    SOURCES.append(('violin', root, f'Strings/Solo Violin/Arco Vib/LLVln_ArcoVib_{pitch}_p.wav'))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fetch(path):
    dst = CACHE / Path(path).name
    if not dst.exists():
        req = urllib.request.Request(RAW + urllib.parse.quote(path), headers={'User-Agent':'riso-roost'})
        with urllib.request.urlopen(req, timeout=90) as response:
            dst.write_bytes(response.read())
    return dst


def tuning_cents(y, rate, root):
    # Median harmonic estimate across the sustained body. A small correction
    # centres the recorded vibrato without flattening its changing pitch.
    fundamental = 440 * 2 ** ((root - 69) / 12)
    estimates = []
    for start in [0.8, 1.5, 2.2, 2.9, 3.6]:
        segment = y[int(start*rate):int((start+.7)*rate)].mean(axis=1)
        if len(segment) < .65*rate:
            continue
        n = 262144
        spectrum = abs(np.fft.rfft(segment*np.hanning(len(segment)), n))
        f = np.fft.rfftfreq(n, 1/rate)
        for harmonic in [1,2,3]:
            center = fundamental * harmonic
            candidates = np.flatnonzero((f > center*2**(-.48/12)) & (f < center*2**(.48/12)))
            i = candidates[np.argmax(spectrum[candidates])]
            # Parabolic interpolation in log magnitude for sub-bin precision.
            a,b,c = np.log(spectrum[i-1:i+2] + 1e-12)
            delta = .5*(a-c)/(a-2*b+c)
            estimates.append(1200*np.log2(((i+delta)*rate/n)/center))
    return float(np.median(estimates))


def build():
    CACHE.mkdir(parents=True, exist_ok=True)
    previous_path = FILM / 'string-bank-manifest.json'
    previous = json.loads(previous_path.read_text()) if previous_path.exists() else {}
    expected = {s['source']:s['sourceSha256'] for s in previous.get('samples',[])}
    license_file = fetch('LICENSE')
    (FILM / 'VSCO-LICENSE.txt').write_bytes(license_file.read_bytes())
    fetch('README.md')
    bank = dict(library='VSCO 2 Community Edition', author='Versilian Studios',
                recordings='Sam Gossner and Simon Dalzell; sample cutting Elan Hickler / Soundemote',
                license='CC0-1.0', source=f'https://github.com/{REPO}', commit=COMMIT,
                sampleRate=RATE, format='audio/ogg; codecs=vorbis', samples=[])
    for instrument, root, source in SOURCES:
        path = fetch(source)
        digest = sha(path.read_bytes())
        if source in expected and expected[source] != digest:
            raise ValueError(f'Source hash changed: {source}')
        y, sr = sf.read(path, always_2d=True)
        y -= y.mean(axis=0)
        step = max(1,int(.01*sr))
        energy = np.array([np.sqrt(np.mean(y[i:i+step]**2)) for i in range(0,len(y)-step,step)])
        audible = np.flatnonzero(energy > max(energy)*.035)
        trim = max(0,int(audible[0]*step-.025*sr))
        y = y[trim:trim+int(7.2*sr)]
        cents = tuning_cents(y,sr,root)
        mid = y.mean(axis=1)
        side = (y[:,0]-y[:,1])*.5 * (.15 if instrument=='bass' else .55)
        y = np.column_stack((mid+side, mid-side))
        body = y[int(.5*sr):int(min(4.5,len(y)/sr-.3)*sr)]
        body_rms = float(np.sqrt(np.mean(body**2)))
        gain = min(.085/body_rms, .82/max(abs(y).max(),1e-9))
        y *= gain
        y[:int(.015*sr)] *= np.linspace(0,1,int(.015*sr))[:,None]
        y[-int(.18*sr):] *= np.linspace(1,0,int(.18*sr))[:,None]
        y = resample_poly(y,160,147) if sr==44100 else y
        if sr not in [44100,RATE]:
            raise ValueError(f'Unexpected sample rate {sr}')
        stem = f'{instrument}-{root}'
        wav, ogg = CACHE/(stem+'.wav'), CACHE/(stem+'.ogg')
        sf.write(wav,y,RATE,subtype='PCM_24')
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str(wav),
                        '-map_metadata','-1','-c:a','libvorbis','-q:a','6',str(ogg)],check=True)
        encoded = ogg.read_bytes()
        sample = dict(instrument=instrument,root=root,source=source,sourceSha256=digest,
                      encodedSha256=sha(encoded),sourceRate=sr,trimSeconds=trim/sr,
                      gain=gain,stereoSide=.15 if instrument=='bass' else .55,
                      tuneCents=round(-cents,3),seconds=len(y)/RATE,
                      audio=base64.b64encode(encoded).decode())
        bank['samples'].append(sample)
        print(f'{stem}: {len(y)/RATE:.2f}s, tuning {-cents:+.1f} cents, {len(encoded)//1024} KiB',flush=True)
    manifest = {**bank,'samples':[{k:v for k,v in s.items() if k!='audio'} for s in bank['samples']]}
    previous_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    payload = json.dumps(bank,separators=(',',':'))
    (CACHE/'string-bank.json').write_text(payload,encoding='utf-8')
    return payload


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--embed',action='store_true')
    args = parser.parse_args()
    payload = build()
    if args.embed:
        html = FILM/'index.html'
        text = html.read_text(encoding='utf-8')
        block = '<script id="string-bank" type="application/json">\n'+payload+'\n</script>'
        pattern = r'<script id="string-bank" type="application/json">[\s\S]*?</script>'
        if re.search(pattern,text):
            text = re.sub(pattern,lambda _:block,text)
        else:
            text = text.replace('</html>',block+'\n</html>')
        html.write_text(text,encoding='utf-8')
    print(f'PASS: {len(SOURCES)} pinned CC0 recordings; bank {len(payload)/1048576:.2f} MiB')
