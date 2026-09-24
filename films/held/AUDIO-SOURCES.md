# Held audio sources

The notes and arrangement are original to Held. The instruments are recordings by Versilian
Studios (Sam Gossner), released under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). CC0 does not require attribution;
credits are kept for provenance. Wind, air, breath, paper, contact and the water drop are
procedural, seeded parts of the project's sound kit.

| Library | Pinned commit | Base path |
|---|---|---|
| [VCSL](https://github.com/sgossner/VCSL) | `c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e` | `https://raw.githubusercontent.com/sgossner/VCSL/<commit>/` |
| [VSCO-2-CE](https://github.com/sgossner/VSCO-2-CE) | `440300901dfe9275fd84e0b7763af1f8443ae62e` | `https://raw.githubusercontent.com/sgossner/VSCO-2-CE/<commit>/` |

The files were fetched from each repository's `master`, which was at these commits when they
were downloaded.

## Files

`<n>` is the pitch in the right-hand column; the embedded key is `<name>_<n>`.

| Name | Upstream file | Pitches |
|---|---|---|
| `mbira` | VCSL `Idiophones/Plucked Idiophones/Kalimba, Kenya/Mbira6_Normal_MainSpirit_<n>_vl3_rr2.wav` | `A4_k1 B3_k3 B4_k15 C#4_k2 D#4_k13 F#4_k14 F#3_k5 G#3_k4 B2_k8` |
| `glock` | VCSL `Idiophones/Struck Idiophones/Glockenspiel/glock_medium_<n>_01.wav` | G5 C6 |
| `chime` | VCSL `Idiophones/Struck Idiophones/Hand Chimes/sus_<n>_r01_main.wav` | F#4 C5 |
| `harp` | VCSL `Chordophones/Composite Chordophones/Concert Harp/KSHarp_<n>_mf1.wav` | B1 E3 G3 B3 D4 F4 A4 C5 E5 G5 B5 |
| `cello` | VSCO-2-CE `Strings/Cello Section/susvib/susvib_<n>_v1_1.wav` | B1 F2 E3 |
| `celloTrem` | VSCO-2-CE `Strings/Cello Section/trem/trem_<n>_v2_1.wav` | B2 G3 |
| `pizz` | VSCO-2-CE `Strings/Violin Section/Pizz/VlnEns_Pizz_<n>_v2_rr1.wav` | B4 E4 F#3 D5 A3 |
| `flute` | VSCO-2-CE `Woodwinds/Flute/expvib/LDFlute_expvib_<n>_v1_1.wav` | A4 C5 E5 |
| `violin` | VSCO-2-CE `Strings/Violin Section/susVib/VlnEns_susVib_<n>_v1.wav` | B4 D5 |

Mbira keys drop the `_k` suffix (`mbira_A4`). Roots are taken from the filenames. VSCO 2's
cello files name middle C C3 ([Roost](../roost/AUDIO-SOURCES.md) checked this against the
partials), so `cello` and `celloTrem` may sound an octave above their written pitch. This has not
been measured for Held.

## Rebuild

Download the files above into `out/_held-samples/raw/` as `<name>_<pitch>.wav`, then run from the
repo root:

```
python films/held/build-samples.py
```

Requires Python with `numpy` and `imageio-ffmpeg`. Each sample is decoded to mono 32 kHz,
trimmed to its onset, capped per family, peak-normalised and embedded as 16-bit FLAC between the
`SAMPLES` markers in `index.html` (4.4 MiB of the 4.6 MiB file, as base64). FLAC is lossless, so both
browsers decode the same samples. Re-run `audio.mjs --twice` after rebuilding.
