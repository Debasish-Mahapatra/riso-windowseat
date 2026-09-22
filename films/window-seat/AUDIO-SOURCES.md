# Window Seat audio sources

The composition, notes and conductor are original to this film. The piano sound uses
**Salamander Grand Piano V3**, recorded by **Alexander Holm**, under
[Creative Commons Attribution 3.0 Unported](https://creativecommons.org/licenses/by/3.0/).

Source: [sfzinstruments/SalamanderGrandPiano](https://github.com/sfzinstruments/SalamanderGrandPiano),
commit `3382bf9496bba2486f5ab0de55a264d1dfc38404`. The source repository identifies a Yamaha C5,
recorded at 48 kHz / 24 bit with two AKG C414 microphones. Its
[license](https://github.com/sfzinstruments/SalamanderGrandPiano/blob/3382bf9496bba2486f5ab0de55a264d1dfc38404/LICENSE)
applies to the sample recordings; it does not imply endorsement of this film.

## Embedded bank

`index.html` contains 34 stereo recordings in the `piano-bank` JSON script: MIDI roots 33–81
in minor thirds, velocity layers 4 and 8. Other notes transpose at most one semitone. The
bank retains source filenames, source SHA-256 hashes, trim offsets, gains and source commit.
The player decodes these bytes locally; no sampler library or runtime download is required.
For code review, read the first script block; the final JSON block is encoded audio data.

Modifications: leading silence trimmed while retaining 2 ms before the detected attack;
5.5 or 7 second tails with a 120 ms fade; DC removed; stereo side reduced to 55%; per-key
body RMS matched; encoded as 48 kHz stereo Ogg Vorbis at quality 6. The recorded attack,
inharmonic string decay and soundboard body are what an additive piano model could not supply.

Credits are visible below the player, included in exported WAV `LIST/INFO/ICMT` metadata,
and included in MP4 metadata. Keep this attribution when redistributing the piano bank or
exports. `build-piano-bank.py` in this folder rebuilds the bank from the source recordings.

## Rain

`windowRain()` is procedural and seeded. It uses short filtered noise contacts at irregular
arrival times plus contacts from visible `DROPS`, with a final 1350 Hz low-pass and no reverb.
It contains no pitched oscillators, droplet chirps, outdoor wash or sampled field recording.
