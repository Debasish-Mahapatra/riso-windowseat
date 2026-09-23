# One Tulip a Day: audio sources

The score, a waltz in F with its themes and arrangement, is original to this film. It is played on
recordings released under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). CC0
needs no attribution, but credit is kept for provenance. The credit appears:
- in the film's end card;
- in the WAV's `LIST/INFO` comment (`AUDIO_CREDIT`);
- in the delivered MP4.

| Source | Pinned at | Credit | Used for |
|---|---|---|---|
| [VS Chamber Orchestra 2: Community Edition](https://github.com/sgossner/VSCO-2-CE), Versilian Studios | commit `440300901dfe9275fd84e0b7763af1f8443ae62e` | Recorded by Sam Gossner and Simon Dalzell; sample cutting by Elan Hickler / Soundemote | Section strings, arco and pizzicato; contrabass pizzicato; clarinet, sustained and staccato; harp; timpani roll |
| [Versilian Community Sample Library](https://github.com/sgossner/VCSL), Versilian Studios | commit `c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e` | Versilian Studios LLC | Kawai grand piano; glockenspiel; soft-mallet vibraphone; timpani hits; bass drum; snare; shaker; triangle; suspended cymbal; sleigh bells |
| [BigSoundBank.com](https://bigsoundbank.com), Joseph Sardin | Not version-pinnable; SHA-256 below | Joseph Sardin | Bicycle bells #1102 and #1042; steam locomotive whistle #3011 (Martel, France) |

The licence texts are in `licenses/`. VSCO 2 CE's 2016 `Readme.txt` also *asks*, as a request
and not a licence condition, that the samples not be sold directly and that Versilian Studios be
credited.

## Embedded bank

`index.html` ends with a `<script id="sample-bank" type="application/json">` holding 106 Ogg
Vorbis notes, about 3.5 MiB including base64. It decodes locally, with no network access.

| Instrument | Notes | Measured range (MIDI) |
|---|---|---|
| Piano | 14 | 36–84 |
| Glockenspiel | 5 | 79–103 (C and G only) |
| Vibraphone | 6 | 71–88 |
| Contrabass pizzicato | 7 | 31–45 |
| Cellos, sustained and pizzicato | 9 + 5 | 36–64 |
| Violins, sustained and pizzicato | 12 + 8 | 57–93 |
| Clarinet, sustained and staccato | 7 + 3 | 62–86 (D, F, A♯ only) |
| Harp | 12 | 45–93 |
| Timpani | 4 hits + 1 roll | 42–50 |
| Percussion and effects | 13 | unpitched |

`sample-bank.tsv` lists every note: its recording, cut point, length, fade and measured root.
`sample-sources.json` pins each recording to its URL and SHA-256.

`build-sample-bank.py` builds the bank:
- It checks every recording against its SHA-256.
- It trims each note at its measured onset.
- It fades each note in over 4 ms and out over the listed fade.
- It peak-levels each note to −3 dBFS.
- It resamples to 48 kHz and encodes Vorbis at quality 4.

`sample-bank-manifest.json` records each note's source hash, encoded hash, cut and gain.

Roots are **measured** pitches (C4 = 60), not file-name labels. This matters in two ways:
- The Versilian piano, mallets, section strings, contrabass and clarinet name middle C "C3".
- Using the measured root also corrects tuning, such as the glockenspiel's 8–24 cents sharp and
  the clarinet staccato's 21–40 cents flat.

The score picks the nearest root and transposes by playback ratio with Hermite interpolation. That
is at most ±2 semitones for most instruments and ±3.5 on the glockenspiel.

Rebuild from the project root with a local copy of the recordings, laid out as in the first cut's
`assets/audio/`. Without `--source`, the script downloads them from the pinned URLs into
`out/one-tulip-sample-source/`:

```
python3 films/one-tulip-a-day/build-sample-bank.py --source /path/to/assets/audio --embed
```

This needs Python 3 and an ffmpeg with libvorbis (imageio-ffmpeg's, `$FFMPEG`, or on `PATH`).
Re-run `tools/audio.mjs --twice` after rebuilding.

## Procedural, not recorded

No clean CC0 recording was found for some sounds. These are seeded parts of the sound kit, or
built on it, in `index.html`:
- the conductor's pea whistle;
- the locomotive's chuffs and rail joints;
- the brake's air dump, wheel squeal and sparks;
- the steam hiss;
- pigeons' wings, the tram passing, and paper and card;
- the room tone, wind and autumn rain.
