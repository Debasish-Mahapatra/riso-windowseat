"""Rebuild the piano bank embedded in index.html from the pinned, attributed Salamander samples.

Requires: pip install numpy soundfile imageio-ffmpeg. Downloads 34 FLAC files (~66 MB) into
out/piano-source/ and writes out/piano-source/bank.json, the same shape as the
`<script id="piano-bank" type="application/json">` block at the end of index.html. Replacing that
block with bank.json installs the bank. Vorbis bytes can differ between ffmpeg builds, so a rebuild
is equivalent in sound, not guaranteed byte-identical to the shipped bank.
"""
from pathlib import Path
import base64
import concurrent.futures
import hashlib
import io
import json
import subprocess
import urllib.parse
import urllib.request
import numpy as np
import soundfile as sf
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / 'out' / 'piano-source'
CACHE.mkdir(parents=True, exist_ok=True)
# AUDIO-SOURCES.md and the shipped bank record this commit; keep them in step.
commit = '3382bf9496bba2486f5ab0de55a264d1dfc38404'

def read(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'riso-windowseat-piano-build'}), timeout=120).read()

base = 'https://raw.githubusercontent.com/sfzinstruments/SalamanderGrandPiano/' + commit + '/'
license_text = read(base + 'LICENSE').decode('utf-8')
(CACHE / 'LICENSE').write_text(license_text, encoding='utf-8')
roots = list(range(33, 82, 3))
names = {0:'C',3:'D#',6:'F#',9:'A'}
tasks = [(m, v) for m in roots for v in (4, 8)]
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

def build(task):
    midi, layer = task
    name = f'{names[midi%12]}{midi//12-1}v{layer}.flac'
    source = CACHE / name
    url = base + 'Samples/' + urllib.parse.quote(name)
    if not source.exists():
        source.write_bytes(read(url))
    data, rate = sf.read(source, dtype='float32', always_2d=True)
    # Locate the recorded attack at a relative threshold, retaining 2 ms of its
    # pre-contact sound. A key's leading tape silence must not delay the cue.
    w = max(1, int(rate*.002))
    envelope = np.max(np.abs(data[:rate]), axis=1)
    power = np.convolve(envelope**2, np.ones(w)/w, mode='same')
    threshold = max(np.max(power)*.0025, 1e-9)
    onset = int(np.flatnonzero(power > threshold)[0])
    start = max(0, onset-int(.002*rate))
    seconds = 7.0 if midi < 60 else 5.5
    data = data[start:start+int(seconds*rate)].copy()
    data -= np.mean(data, axis=0)
    # Narrow the close AB microphones while retaining the recorded spatial body.
    mid = (data[:,0] + data[:,1])*.5
    side = (data[:,0] - data[:,1])*.275
    data[:,0] = mid + side
    data[:,1] = mid - side
    # Match key body levels, preserving each recording's attack and spectrum.
    rms = np.sqrt(np.mean(data[int(.06*rate):int(.70*rate)]**2))
    gain = .105 / max(rms, 1e-5)
    gain = min(gain, .86 / np.max(np.abs(data)))
    data *= gain
    fade_in = max(2, int(.0007*rate)); fade_out = int(.12*rate)
    data[:fade_in] *= np.linspace(0,1,fade_in)[:,None]
    data[-fade_out:] *= np.linspace(1,0,fade_out)[:,None]
    wav = io.BytesIO()
    sf.write(wav, data, rate, format='WAV', subtype='PCM_16')
    result = subprocess.run([ffmpeg,'-v','error','-i','pipe:0','-c:a','libvorbis','-q:a','6','-f','ogg','pipe:1'],
                            input=wav.getvalue(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    encoded = result.stdout
    (CACHE / name.replace('.flac','.ogg')).write_bytes(encoded)
    return {'root':midi, 'layer':layer, 'audio':base64.b64encode(encoded).decode('ascii'),
            'source':name, 'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'trimSeconds':start/rate, 'bodyGain':float(gain), 'seconds':len(data)/rate}

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    samples = list(executor.map(build,tasks))

bank = {'credit':'Salamander Grand Piano V3 by Alexander Holm',
        'license':'https://creativecommons.org/licenses/by/3.0/',
        'source':'https://github.com/sfzinstruments/SalamanderGrandPiano',
        'commit':commit,
        'changes':'Selected velocity layers 4 and 8; leading silence and tails trimmed; DC removed; stereo side reduced to 55%; key body levels matched; 48 kHz stereo Ogg Vorbis conversion.',
        'samples':samples}
(CACHE / 'bank.json').write_text(json.dumps(bank,separators=(',',':')),encoding='utf-8')
manifest = {**bank, 'samples':[{k:v for k,v in x.items() if k != 'audio'} for x in samples]}
(CACHE / 'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'samples':len(samples),'bytes':(CACHE/'bank.json').stat().st_size,
                  'commit':commit,'trimRange': [min(s['trimSeconds'] for s in samples),max(s['trimSeconds'] for s in samples)]},indent=2))
