"""Rebuild the embedded CC0 instrument bank for One Tulip a Day.

    python3 films/one-tulip-a-day/build-sample-bank.py --source /path/to/audio --embed

sample-bank.tsv lists every note: which recording, where to cut it, and its
measured root pitch. sample-sources.json pins each recording (URL and SHA-256).
With --source the recordings are read from a local copy laid out as in the
first cut's assets/audio/; without it they are downloaded from the pinned URLs
into out/one-tulip-sample-source/. Every file is checked against its SHA-256
before it is used.

Each note is trimmed at its measured onset, faded in over 4 ms and out over
fade_s, peak-levelled to -3 dBFS, resampled to 48 kHz and encoded as Ogg
Vorbis. --embed replaces the <script id="sample-bank"> block in index.html;
the manifest (sample-bank-manifest.json) records source and encoded hashes.
Needs python3 and an ffmpeg with libvorbis (imageio-ffmpeg's, $FFMPEG or PATH).
"""
import argparse
import base64
import glob
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import urllib.request

FILM = Path(__file__).resolve().parent
CACHE = FILM.parents[1] / 'out' / 'one-tulip-sample-source'
RATE = 48000
QUALITY = '4'                       # libvorbis -q:a; ~64-80 kbit/s mono


def sha(data):
    return hashlib.sha256(data).hexdigest()


def ffmpeg_exe():
    for c in [os.environ.get('FFMPEG'), shutil.which('ffmpeg'),
              *sorted(glob.glob(str(FILM.parents[2] / '.deps/imageio_ffmpeg/binaries/ffmpeg-*')))]:
        if c and os.path.exists(c):
            return c
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        raise SystemExit('ffmpeg with libvorbis not found; set $FFMPEG')


def recording(rel, prov, source_dir):
    want = prov['sha256']
    path = (Path(source_dir) / rel) if source_dir else (CACHE / rel)
    if not path.exists():
        if source_dir:
            raise SystemExit(f'missing {path}')
        path.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(prov['url'], headers={'User-Agent': 'riso-one-tulip'})
        with urllib.request.urlopen(req, timeout=90) as r:
            path.write_bytes(r.read())
    got = sha(path.read_bytes())
    if got != want:
        raise SystemExit(f'SHA-256 mismatch for {rel}: {got} != {want}')
    return path


def peak_db(ff, path, start, dur, filt):
    out = subprocess.run([ff, '-hide_banner', '-nostats', '-ss', start, '-t', dur, '-i', str(path),
                          '-af', filt + ',volumedetect', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.search(r'max_volume:\s*(-?[\d.]+) dB', out).group(1))


def build(source_dir):
    ff = ffmpeg_exe()
    prov = json.loads((FILM / 'sample-sources.json').read_text())
    rows = [l.rstrip('\n').split('\t') for l in (FILM / 'sample-bank.tsv').read_text().splitlines()
            if l.strip() and not l.startswith('#')]
    bank = dict(format='audio/ogg; codecs=vorbis', sampleRate=RATE,
                credit='CC0-1.0 recordings: Versilian Studios (VSCO 2 CE, VCSL), Karoryfer Samples, '
                       'Joseph Sardin / BigSoundBank. See AUDIO-SOURCES.md.', samples=[])
    manifest = []
    tmp = Path(tempfile.mkdtemp(prefix='tulip-bank-'))
    try:
        for key, rel, start, dur, fade, ch, root, source in rows:
            p = prov['files'][rel]
            path = recording(rel, p, source_dir)
            fst = float(dur) - float(fade)
            filt = f'afade=t=in:d=0.004,afade=t=out:st={fst:.3f}:d={fade}'
            gain = -3 - peak_db(ff, path, start, dur, filt)
            ogg = tmp / f'{len(manifest)}.ogg'
            subprocess.run([ff, '-hide_banner', '-loglevel', 'error', '-y', '-ss', start, '-t', dur, '-i', str(path),
                            '-af', f'{filt},volume={gain:.2f}dB', '-ac', ch, '-ar', str(RATE), '-map_metadata', '-1',
                            '-c:a', 'libvorbis', '-q:a', QUALITY, str(ogg)], check=True)
            enc = ogg.read_bytes()
            inst = key.rsplit('_', 1)[0] if root != '-' else key
            entry = dict(key=key, inst=inst, root=None if root == '-' else float(root), channels=int(ch),
                         seconds=float(dur), source=source, file=rel, sourceSha256=p['sha256'],
                         startSeconds=float(start), gainDb=round(gain, 2), encodedSha256=sha(enc))
            manifest.append(entry)
            bank['samples'].append(dict(key=key, inst=inst, root=entry['root'], audio=base64.b64encode(enc).decode()))
            print(f'{key:10s} {rel:55s} {len(enc) // 1024:4d} KiB', flush=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    (FILM / 'sample-bank-manifest.json').write_text(json.dumps(
        {k: v for k, v in bank.items() if k != 'samples'} | {'samples': manifest}, indent=1) + '\n')
    return json.dumps(bank, separators=(',', ':'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--source', help='local copy of the recordings (the first cut\'s assets/audio)')
    ap.add_argument('--embed', action='store_true', help='write the bank into index.html')
    a = ap.parse_args()
    payload = build(a.source)
    if a.embed:
        html = FILM / 'index.html'
        text = html.read_text(encoding='utf-8')
        block = '<script id="sample-bank" type="application/json">\n' + payload + '\n</script>'
        pattern = r'<script id="sample-bank" type="application/json">[\s\S]*?</script>'
        text = re.sub(pattern, lambda _: block, text) if re.search(pattern, text) else text.replace('</html>', block + '\n</html>')
        html.write_text(text, encoding='utf-8')
    print(f'PASS: {payload.count(chr(34) + "key" + chr(34))} notes from pinned CC0 recordings; bank {len(payload) / 1048576:.2f} MiB')
