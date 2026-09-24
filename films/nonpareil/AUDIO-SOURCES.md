# Nonpareil audio sources

The notes and arrangement are original to this film. Every recording is CC0 and embedded as
Ogg Vorbis in the page's `#sample-bank` JSON script (2.24 MiB including base64). No runtime
network access.

## Handpan (lead)

[HandPan 1st model](https://freesound.org/people/GAMEDRIX974/packs/33041/) by GAMEDRIX974 on
Freesound, [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). The 18 takes are
unnamed (`1.wav` … `18.wav`, sound ids 587401–587418). The bank uses Freesound's public HQ
previews (128 kb/s MP3), not the original WAVs, because original downloads need an account.

The notes were identified from each take's partials (a handpan tone field is tuned f, 2f, 3f)
and checked against an FFT of the first second: D2, C3, D3, E3, F3, G3, A3, C4, D4, E4, F4,
G4, A4, C5, A5. That is a D Celtic-minor handpan (D E F G A C, no sixth) with an extended
bottom. `7.wav` duplicates `11.wav` and is not used. Where two takes share a note (D3, A4),
the longer-ringing one is kept. Sympathetic ringing of neighbouring fields fakes a lower
harmonic series in some takes, so the builder pins each handpan root and only measures its
tuning. Corrections range from −6.7 to +7.4 cents.

## Bass (background)

[VSCO 2 Community Edition](https://versilian-studios.com/vsco-community/) by Versilian Studios,
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/), pinned to
`sgossner/VSCO-2-CE` commit `440300901dfe9275fd84e0b7763af1f8443ae62e`. Recordings: Sam
Gossner and Simon Dalzell; sample cutting Elan Hickler / Soundemote. License text:
`VSCO-LICENSE.txt`.

| Instrument | Recordings | Role |
|---|---|---|
| Cello section, sustained vibrato, `v1` | C2 E2 G2 B2 D3 F3 A3 | the slow lament line and its few counter-lines |
| Solo contrabass, sustained, no vibrato | E1 G1 B♭1 C2 D2 | roots an octave under the cellos |

The older VSCO string files name pitches an octave low; the builder measures the sounding root
(odd-harmonic test) and records it, matching the roots Roost verified for the same files.

## Preparation

`build-sample-bank.py` downloads everything once into `out/nonpareil-samples/` (reusing Roost's
copies of the same pinned VSCO files), removes DC, trims leading silence, keeps handpan tones
until they fall 50 dB under their peak (at most 7.5 s) and strings for 6.4 s, then fades both
ends and resamples to 48 kHz. Handpan is mixed to mono and panned by the drop's position in
the score; cello stereo width is reduced to 30 % side and contrabass to 15 %. Handpan gains
match the first 300 ms of body; string gains match sustained body RMS. The encoded Oggs use
Vorbis quality 5. `sample-bank-manifest.json` keeps every source URL, source and encoded
SHA-256, trim, gain, measured root and tuning correction without the payload.

Rebuild from the project root:

```
python films/nonpareil/build-sample-bank.py --embed
```

Requires Python with `numpy`, `scipy`, `soundfile` and `imageio-ffmpeg`. Re-run the audio
gates after rebuilding: a different Vorbis encoder changes the decoded samples.

## Edge gestures and room

The skim, the sheet unrolling on and the sheet rolling off are handpan recordings from the bank
above, played backwards into the edge's mid-frame crossing and forwards out of it
(`edgeGesture` in `index.html`); v1 used the kit's procedural paper slides there. Room tone is
the kit's `air`. Nothing else is synthesised.
