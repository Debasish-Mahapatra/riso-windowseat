# Window Seat

78 seconds, 1080 × 1080, 30 fps, scored. Authoritative source: `index.html`.
Delivery: the MP4 is attached to [the v1.0 release](https://github.com/sevenevesai/riso-windowseat/releases/tag/v1.0).
It is a Firefox render; decoded, it has 2340 frames, runs 78.00 s at 1080² and is h264.

## Premise

A night's journey through one fixed train window, with the same glass of water on the sill.
The opening passage (golden departure, fields, bridge, forest, tunnel) was first built as a
standalone 30 s silent film. Here the tunnel leads into a night city instead of the coast. Each
later passage adds a visual type the project did not have, and each changes something in the
window or the glass.

| Time (s) | Passage | New technique | Switch device |
|---|---|---|---|
| 0–19 | Dusk: platform, fields, bridge, forest, tunnel | — | tunnel (A→B at 17.5) |
| 19–30 | Night city: towers with lit windows, canal reflection, slow past a level crossing (blinking lamps, boom, headlights) | `reflectPlates`, seeded window lights | — |
| 30–38.4 | Another train overtakes: lit windows, passengers read, sleep, stand, a child waves | relative motion; left→right wipe | its carriages (B→C at 34) |
| 38.4–45 | Fireworks over a far town, reflected in the lake | analytic ballistic sparks with drag | — |
| 45–51 | Sleeper hours: town lights go out, star trails lengthen, mirror strengthens | long exposure pure in t | — |
| 51–57 | Pre-dawn fog fills everything, then thins | `veil` to uniform colour | fog (C→D at 54.2) |
| 57–64.6 | Dawn from a viaduct: five ridges in haze, pooled mist, crepuscular rays, river glint | layered atmospheric ridges and rays | — |
| 64.6–70 | Clouds close, rain slants with speed, drops land and stream back along the glass | refracting drops | rain haze (D→E at 68.3) |
| 70–78 | Lakeside halt as the rain clears: snowy peaks, lake, rainbow; the train stops, drops slide straight down, the glass rings down | rainbow bands, still-state drops | hold |

Why the ending belongs here: the drops only run straight down once we have stopped, and the
water in the glass settles last. The rainbow is the reward for the rain the window collected.

## Design decisions

- Speed profile `VK` has piecewise smoothstep keys. Distance `S(t)` and acceleration are
  analytic. The train slows through the city (760 px/s) and runs fastest at night (1350).
- The sky is keyed through `SKYK` palettes (city → night → deep → predawn → dawn → morning →
  rain → clear). The only discontinuous jump happens under the overtaking train.
- Every content switch happens while the window is fully covered: by the tunnel, by the other
  train's carriages, by the fog veil at D = 1, or by the rain haze at D = 1.
- Drops: each has a seeded birth, place, radius and stick time; 45% never run. A running
  drop's horizontal travel is `blow × (S(t) − S(t_run))`, so it streams back at speed and falls
  straight down once stopped. Inside, the plates snapshot is drawn inverted and minified, like
  a tiny lens. Drops under ~8 px radius were indistinguishable from halftone dots, so radii
  are 5–22 px.
- The lake reflection uses `squash: 1.9` so high bursts land in the shallow band of lake. This
  is a stylisation, not optics. The rainbow is drawn after the lake reflection because a
  reflected arc read as an eye shape.

## Verification

- `verify.mjs`: seek is pure in t in Chromium and Firefox, including the shot boundaries.
- Strips inspected: level crossing (25.6–27.2 s), train exit wipe (36.6–38.6 s), fireworks
  (39–41.2 s), fog switch (51.5–57.5 s), rain/haze switch (64–71 s) and arrival (72.6–78 s).
  1:1 crops were checked for drops, the train, the crossing and the rainbow.
- Render cost is about 125 ms/frame; the full render took 296 s.

## Score

### Composition and instruments

"A Light Left in the Window": an original 32-bar piano miniature in D major, with relative
minor development and a borrowed G minor sixth before the final D6/9. The subject A–B–F#–E
forms longer melodic sentences, returns in different harmonic settings, and broadens at dawn.
`HARMONY`, `MELODY` and the answering line in `scoreForeground()` hold the written music.

The metre is 6/8, about 50–53 dotted-quarter beats/minute in the main passages. Phrase rubato
ranges from 43.4 at the final ritardando to 55.5 around the fireworks. `SCORE_BARS` derives its
anchors from `SHOTS`, `SKYK`, tunnel geometry and `VK`, so most cuts ride through a continuing
bar. The rail rhythm stays distance-driven; the music has its own phrasing.

The instrument is a real grand piano: Salamander Grand Piano V3 by Alexander Holm, with soft
and medium touch layers, matched key-body levels, narrowed microphone width, and natural
attacks and string decay. Bass, answering line and upper colours all use the same piano. An
earlier additive/modal piano model passed the audio meters but was heard as MIDI-like; meters
alone do not establish an acoustic timbre.

The 34 recordings are embedded in `index.html`; playback is self-contained at 48 kHz and makes
no network requests. [AUDIO-SOURCES.md](AUDIO-SOURCES.md) records the source, transformations
and CC BY 3.0 attribution. The rest of the sound is procedural.

The room has distinct early reflections and a dark diffuse tail. Its impulse is normalised
by discrete sample energy. The kit's `sqrt(energy / sampleRate)` normalisation introduced an
extra `sqrt(48000)` gain before the wet controls and masked the instrument attacks. Keep this
film's correction when changing its sound-kit copy; do not restore the old normaliser.

### Spotting and continuity

| Picture event | Musical decision |
|---|---|
| Platform, 0–5.2 s | A 0.48 s opening breath, then broken piano harmony and the first subject. |
| Fields 5.2, bridge 9.8, forest 12.8 | Continue the opening sentence; quiet truss sounds follow distance. |
| Tunnel 16.0; full dark 16.7; covered switch 17.5 | The dominant bar lands at full dark; pedal tails carry the switch. |
| City 19.1 s | Relative-minor development; the subject moves to lower keys with a light upper doubling. |
| Crossing near 26.4 s | A distant, softened two-note signal follows `X_LC` and the lamp alternation. |
| Overtake 30; carriage wipe 34 | Continue the phrase and pan the other train from `trainX`; no musical reset. |
| Fireworks 38.4 s | Gmaj9 opens the register with a soft upper-key accent. Booms follow `BURSTS` by 0.75 s. |
| Sleeper 45; fog 51; covered fog switch 54.2 | Finish the previous sentence, then thin to a slower night variation at 47.4. Sustain through fog. |
| Dawn picture 57; dawn turn 57.5 | An ascending inner line prepares the full subject's return, bass foundation and counterline. |
| Rain 64.6; covered rain switch 68.3 | Carry the reprise across both; soft, muffled taps follow rain intensity and `DROPS`. |
| Arrival 70; clear sky 74.5 | Gm6 colours the descent, resolving to D6/9 at 73.237; reduce the accompaniment. |
| Stop 76; ending 78 | A quiet tonic voicing lands with the halt and rings into the last hold. |

The night passage is a deliberate reduction, with three accompaniment notes per bar and longer
melodic gaps, not digital silence. The last 1.15 s fades the remaining piano and room tail.
Rail joints use four restrained contacts per 1400 world pixels. Carriage noise uses full-length
seeded buffers so a loop seam cannot click. Effects stay behind the musical foreground.

`windowRain()` uses aperiodic, short noise contacts, softened by a 1350 Hz low-pass and kept
out of the music reverb, instead of an outdoor wash with ringing droplets. In an isolated
65–73 s comparison before mastering, it is 4.7 dB RMS quieter than the outdoor version.
Energy below 1.5 kHz rises from 2.35% to 90.31%; energy above 4 kHz falls from 46.93% to
0.069%. This models small taps heard through a train window, not rain at an outdoor microphone.

### Measured review

Firefox WAV: I −16.7 LUFS, LRA 7.4 LU, TP −1.40 dBTP, clipped 0; two cold renders byte-identical
(`08b554b71e7932ad`). Exactly 78.000 s, stereo, 48 kHz. No detected discontinuities. Opening and
ending samples are zero. The peak ceiling retains the piano's natural dynamics 0.7 LU below
the nominal target. Stereo correlation is 0.527 after narrowing the recorded AB microphones.
Chromium's render also passes at I −16.7 LUFS, TP −1.40 dBTP, with no clipping.
The final Firefox WAV is muxed to AAC 192 kb/s: MP4 I −16.7 LUFS, LRA 7.4 LU, peak −1.4 dBFS.
The exported video stream is byte-identical to the checked Firefox reel: 2340 frames, 78.00 s,
1080 × 1080. Sample attribution is present in both WAV and MP4 metadata.

The night variation has two 200 ms valleys at 49.85 and 55 s, 12.5 and 13.3 dB below their
surroundings. These are decaying notes in the sparse phrase, away from picture cuts, and are
kept as musical breaths. `verify.mjs` passed consecutive, reordered and cold seeks at 44
picture times in both browsers.

| True sync mark | Onset / local energy peak | Loudness before → after the mark |
|---|---|---|
| Tunnel, 16.7 s | +5 / +40 ms | −16.0 → −17.1 LUFS |
| Fireworks reveal, 38.4 s | +10 / +55 ms | −17.5 → −14.6 LUFS |
| Dawn, 57.5 s | +5 / +45 ms | −20.1 → −13.9 LUFS |
| Stop, 76 s | +5 / +25 ms | −28.7 → −24.8 LUFS |

The audio sheet and picture sheet were inspected. These are measured checks, not a claim of
perceptual approval.

## Remaining weaknesses

- Nobody has watched it at speed; pacing is judged from strips.
- The forest slope before the rain (64.6–67) is flat dark green and reads as filler.
- The level crossing flashes by in about a second; its road and car are small and dark.
- Passenger silhouettes are simple heads and torsos.
- Fireworks sometimes open as a dense disc in their first frames.
