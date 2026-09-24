"""Embed the film's CC0 instrument samples into index.html.

Sources (both CC0 1.0, by Versilian Studios / Sam Gossner):
  VCSL      https://github.com/sgossner/VCSL
  VSCO-2-CE https://github.com/sgossner/VSCO-2-CE
Raw downloads live in out/_held-samples/raw (see AUDIO-SOURCES.md for the exact files).
Requires numpy and imageio-ffmpeg.

Each sample is decoded to mono 32 kHz, trimmed to its onset, capped in length
with a cosine tail, peak-normalised, encoded as 16-bit FLAC (lossless, so both
browsers decode identical samples) and written between the SAMPLES markers.
Run: python films/held/build-samples.py
"""
import base64, os, subprocess, sys
import imageio_ffmpeg
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, '..', '..', 'out', '_held-samples', 'raw')
FF = imageio_ffmpeg.get_ffmpeg_exe()
SR = 32000
CAP = {'mbira': 2.4, 'glock': 2.2, 'chime': 3.6, 'harp': 2.8, 'cello': 5.5, 'celloTrem': 4.5,
       'pizz': 0.9, 'flute': 4.5, 'violin': 4.5}

def decode(path):
    out = subprocess.run([FF, '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32).copy()

def encode(x):
    return subprocess.run([FF, '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-',
                           '-sample_fmt', 's16', '-c:a', 'flac', '-compression_level', '12', '-f', 'flac', '-'],
                          input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout

entries, total = [], 0
for name in sorted(os.listdir(RAW)):
    if not name.endswith('.wav'):
        continue
    key = name[:-4]
    kind = key.split('_')[0]
    x = decode(os.path.join(RAW, name))
    peak = np.abs(x).max()
    on = int(np.argmax(np.abs(x) > 0.02 * peak))
    x = x[max(0, on - 64):]
    n = min(len(x), int(CAP[kind] * SR))
    x = x[:n]
    tail = min(n // 3, int(0.35 * SR))
    x[n - tail:] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, tail))
    x *= 0.9 / np.abs(x).max()
    b = encode(x)
    total += len(b)
    entries.append(f"  '{key}': '{base64.b64encode(b).decode()}',")
    print(f'{key:14s} {n / SR:5.2f}s {len(b) / 1024:6.1f} KB')
print(f'total {total / 1024 / 1024:.2f} MB flac')

html = os.path.join(ROOT, 'index.html')
s = open(html, encoding='utf-8').read()
a, b = '/* SAMPLES BEGIN */', '/* SAMPLES END */'
if a not in s:
    sys.exit('index.html has no SAMPLES markers')
block = a + '\nconst SAMPLE_SR = %d, SAMPLES = {\n%s\n};\n' % (SR, '\n'.join(entries)) + b
s = s[:s.index(a)] + block + s[s.index(b) + len(b):]
open(html, 'w', encoding='utf-8', newline='\n').write(s)
print('embedded', len(entries), 'samples')
