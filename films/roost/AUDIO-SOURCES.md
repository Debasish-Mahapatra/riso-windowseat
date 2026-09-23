# Roost audio sources

The notes and arrangement are original to Roost. The instruments use recordings from
[VSCO 2 Community Edition](https://versilian-studios.com/vsco-community/) by Versilian Studios,
released under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
The publisher explicitly supplies the original WAVs for reuse and describes the vanilla library
as suitable for ambient and calm orchestral music.

Recordings: Sam Gossner and Simon Dalzell. Sample cutting: Elan Hickler / Soundemote, as credited
in the [upstream README](https://github.com/sgossner/VSCO-2-CE/blob/440300901dfe9275fd84e0b7763af1f8443ae62e/README.md).
The pinned source is `sgossner/VSCO-2-CE`, commit
`440300901dfe9275fd84e0b7763af1f8443ae62e`. Its license is retained in `VSCO-LICENSE.txt`.

## Selected instruments

| Instrument | Recordings | Role |
|---|---|---|
| Cello section, sustained vibrato, soft layer `v1` | 8 | Warm lower harmony and descending answers |
| Solo contrabass, sustained without vibrato, soft layer `v1` | 5 | Quiet, centred low foundation |
| Solo violin, arco vibrato, piano layer `p` | 8 | Four-note flight phrase and the soft return |

These are recorded bows with their natural body, pitch movement and bow noise. No external
sampler is required. Their source provenance and measurable preparation were checked; their
perceptual quality in this mix has not been auditioned in this session.

## Embedded bank

`index.html` holds 21 stereo Ogg Vorbis recordings in its final `string-bank` JSON script,
about 3.73 MiB including base64. It decodes locally without runtime network access.
`string-bank-manifest.json` keeps filenames, source and encoded SHA-256 hashes, roots, trim
offsets, gains and tuning corrections without duplicating the encoded payload.

Preparation removes DC, trims leading silence with 25 ms of safety, retains up to 7.2 seconds,
and adds 15 ms / 180 ms endpoint fades. Stereo side is 55% for cello and violin, 15% for bass.
Body RMS is matched to 0.085 with a 0.82 peak cap; the bank is resampled from 44.1 to 48 kHz
and encoded at Vorbis quality 6. A median harmonic estimate centres each recording's tuning;
it preserves the changing recorded vibrato. The largest correction is −21.1 cents on violin C4.

Cello and bass filenames use an octave convention one lower than scientific pitch; their MIDI
roots were checked against the recorded partials. Violin arco filenames use scientific pitch.
The score transposes selected recordings by at most two semitones. Long phrases change bows
with overlapping recordings; no short sustain loops or artificial vibrato are used.

Rebuild from the project root:

```
python films/roost/build-string-bank.py --embed
```

Requires Python with `numpy`, `scipy`, `soundfile` and `imageio-ffmpeg`. The script downloads
the pinned files to `out/roost-string-source/`, checks existing manifest source hashes, and
replaces only the HTML's bank. Re-run the audio checks after rebuilding with different encoders.

Credits are visible below the player and embedded in WAV comments and the delivered MP4.
CC0 does not require attribution; credits are retained for provenance. The very quiet air
and shared room are procedural, seeded parts of the project's sound kit.
