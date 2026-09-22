# Emergence

Title: `emergence`. Byline: `many small things learning to listen`.

A question is asked of a page: one indigo dot, calling with blue ripples. What answers is the
history of how machines learned to listen — a timeline of AI research drawn as nine worlds, from
a single neuron to the frontier — then a second voice, orange, answers from outside the frame.
Where the two voices' ripples meet they interfere; at contact a thought branches out of the
meeting point as an explosive arbor, and the arbor turns out to be one cell in a network of
many. The title writes itself and the two voices remain as a two-dot mark.

Resonance form, a deliberate sibling to `films/lumen`: the same 28 s on a 120 BPM grid, the same
ripple, dot, iris and sweep machinery, and the same six-passage rhythm. Everything drawn and
the palette are new; the archive absorbs instead of scattering, the answer is built on
interference rather than a ribbon, and the release is an arbor and network, not a flower and
garden. Only Lumen's engine code was reused, never its frames.

## Design

The subject is a *timeline*, so time runs forward through the montage and backward through the
recollection: the lens folds through 2020 → 2017 → 1986 → 1958 and closes on the neuron that
started it. Every world places the dot as something that matters in that world's science: a
nucleus, a minimum, a query knot, a vanishing point, an impact, a fork's node, a refraction
point, a sun, a hub. Each carries a small year in drawn digits, sunken into or carved out of its
ground plate.

Palette: blue and violet carry structure and depth; indigo is the deep overprint; orange is the
signal — attention, activation, the second voice; yellow is light inside it. Green appears only
where terrain earns it (the loss landscape). Fluorescent pink is not used, so the film cannot be
mistaken for Lumen by colour alone. Voices: indigo dot with a blue registration fringe; orange
dot with a yellow fringe. Call ripples are blue, answer ripples orange.

Values: paper, a screened mid, and one overprint dark in every world. Shot sizes vary from
macro to full-bleed dense to sparse. Each world has one live element, drawn from what its
subject does (see the table).

## Worlds

| World | Year | Centre dot | Values / shot / live |
|---|---|---|---|
| neuron | 1958 | nucleolus of a soma | paper / violet dendrites / indigo core; macro; pulse down the axon, tip glints |
| valley | 1986 | the loss minimum | paper sky / green U-shaped basin with contour lines, blue peaks / indigo foreground; wide; a ball rolls in and settles |
| loom | 2017 | the query knot | paper / blue warp and weft / violet and indigo knots; full bleed dense; orange shuttle row on twos |
| hall | 2020 | vanishing point of a data hall | paper glow / blue racks / indigo+blue near racks; deep perspective; LEDs blink |
| drop | 2021 | the point of impact | paper water / violet cap and tendrils with spray / indigo core; mid; filaments drift, bubbles rise, surface rings |
| forks | 2022 | node of a tuning fork | paper / blue steel / violet+indigo resonance box; two scales; prongs vibrate, the small fork answers in sympathy |
| prism | 2023 | the refraction point | indigo+violet night / violet prism / paper-yellow-orange-violet-indigo fan; monumental; features ride the bands |
| orrery | 2024 | the sun | paper / blue rings / violet planets and plinth; mid, cropped base; planets orbit, one moon |
| web | 2025 | hub of a web | paper / blue strands / indigo leaves; sparse; a pluck travels outward every 1.25 s |

Neuron's dendrites and the release arbor share one branch generator (`arbor`); the ending is the
first world grown large.

## Timeline

| Seconds | Passage |
|---|---|
| 0–1.5 | I · question. Dot on paper; two blue ripples with rim ticks |
| 1.5–5.7 | Three windows: neuron, valley, loom; the loom dives to full bleed |
| 5.15–6.66 | Hall irises open at full bleed |
| 6–14 | II · timeline. drop 6, forks 7.25, prism 8.5, orrery 9.75, web 11 (held breath), hall 12.5 in the `dusk` colourway |
| 14–16 | Recollection: hall, loom (`ember`), valley (`dusk`), neuron fold backward through one closing lens |
| 16–18 | III · memory. Feature glyphs spiral out in three inks, drain to blue, and are drawn *into* the dot by 17.74 |
| 18–22 | IV · answer. Orange voice arrives from the upper right; alternating ripples; nodal hyperbolas form between the voices and tighten as they approach; sparks at contact |
| 22–24 | V · emergence. An arbor branches out with staggered settles under a yellow glow; orange buds; two activation pulses run root to tip on the beat at 23 and 23.5 |
| 24–26 | Indigo night: the arbor shrinks to one node among many; paper-knocked edges connect them; pulses travel the network |
| 26–28 | VI · title. `emergence` written as connected script, byline, two-dot mark, dissolve |

## Motion contracts

Each outgoing world remains until the next reveal covers it: `out.end = next.start + next.open`.
`memoryRadius(t)` owns one closing lens across all four recollections; the lens rings fade
over the last 0.22 s rather than vanishing at 16. Live elements take local seconds since cue
start. Looping elements are periodic (orbits, vibration), recycled outside the visible clip
(prism features, axon pulse) or faded on `life()` with zero slope at the wrap (web pluck,
bubbles, network dashes). Interference nodes are drawn analytically from the two voices'
positions and a wavelength of a third of their distance, so they are pure in `t`.

## Screens

Green and indigo share the 45° angle. The reduced 1/1 tile holds two dots in 49 pixels and
quantised a slow coverage ramp into three plateaus (measured 177 → 165 → 134 across the valley's
lit slope). Both now tile a 3/3 supercell at the same angle, and yellow a 2/0 one: the same
lattice, more sub-pixel phases, so the same ramp steps through about ten levels. Pitch stays
4.6–4.7 px.

## Score

`index.html` ships two score candidates. The default is `warm` (A · Gravity), set by
`DEFAULT_SCORE`; open the page with `?score=pulse` (or use the player's selector) for B · Orbit.
The choice selects the cached buffer used by both playback and `renderAudio()`. Both aim for a
low, smooth, spacious organ score that stays continuous across 15–16 s.

| Candidate | Direction and musical material |
|---|---|
| A · Gravity (`warm`) | 60 BPM half-time over the picture's 120 BPM grid. Soft additive organ, deep bass and slowly opening chords. D major; cell D3–A3–E4–F#3. D(add9) → Bm7 → G(add9) → Asus → D6/9. |
| B · Orbit (`pulse`) | 120 BPM grid with a half-time low pulse. Rounded organ ostinato, D dorian; cell D3–A3–E4–F3. The repeating line runs across montage edits and thins gradually through memory. |

The lead sits low. Harmonic partials replace a bright mallet/clock treatment; attacks take
55–75 ms and tails last about 2–3 s. A dark room adds space while dry low notes keep the centre.
Both mixes deliberately spend little energy above 2 kHz; listen for excess darkness on small
speakers, since measurement alone cannot settle it.

Continuity at 15–18 s: overlapping chords, an A2 organ pedal and filtered wind cross the memory
cut. A quiet low pulse continues every second through 18 s while its level falls. Gravity's
reversed motif continues to 16.4 s; Orbit's ostinato loses level gradually until 17.5 s and its
last tail crosses the incoming answer. There is no digital silence or abrupt whole-mix fade.

`scoreEvents()` reads `CUES`, `FLOW`, `ANSWER_PULSES`, `RELEASE` and `MEMORY_ABSORB`.
`MEMORY_ABSORB` also drives the picture's absorption, so retiming it moves the inspection mark.
The player animation callback is `advancePlayback`; calling it `tick` shadowed the kit's clock.

| Event | Score response |
|---|---|
| 6 s, montage | Low motif over a chord pre-lap; intermediate scene cuts ride through. |
| 14–18.1 s, recollection and memory | Sustained pedal and air; pulse dissolves without stopping at 16 s. The 17.74 s mark checks continuity, not a new impact. |
| 18.1 s, answer | Complementary low organ line; successive notes pan with the two dots and approach the centre. |
| 22 s, contact | Prepared breath, low chord opening in staggered tones derived from the arbor timing; soft arrival, not a sharp stinger. |
| 23 / 23.5 s, activation | Restrained A3 / B3 tones; no high bell layer. |
| 24 / 26 s, network and title | Pulse sheds away; held harmony and the opening cell continue into a tail. The master also releases the room before 28 s. |

Measured at 48 kHz stereo, exactly 28.000 s; clipped 0, no detected discontinuities or valleys
10 dB below their surroundings. Firefox cold renders are byte-identical; Chromium differs by
at most two 16-bit steps. Both candidates deliver −16.0 LUFS; ffmpeg agrees.

| Candidate | WAV LRA | WAV TP | Stereo correlation | Loudness at 16 s, before → after |
|---|---|---|---|---|
| Gravity | 3.1 LU | −3.10 dBTP | 0.887 | −16.3 → −16.2 LUFS |
| Orbit | 4.3 LU | −3.46 dBTP | 0.946 | −15.5 → −15.1 LUFS |

Encoded AAC: Gravity I −16.0 LUFS, LRA 3.2 LU, TP −3.1 dBTP; Orbit I −16.0 LUFS,
LRA 4.4 LU, TP −1.8 dBTP. Both MP4s decode all 840 frames without error, with identical
video streams.

Marks: the answer's measured onset is +10 ms for Gravity; Orbit's contact is +15 ms. Slow
attacks and chord rolls put energy peaks later: +130 ms at the answer, +265 ms at Gravity's
contact and +70 ms at Orbit's. Some onset detections select the preceding organ pulse or find
none against a held bed. These are soft gestures, not verified percussive hits.

## Delivery contract

The HTML is authoritative and self-contained; no build step. Exports are 1080 square at 30 fps
with stereo AAC. The tools render the default (`warm`) score. To export Orbit, render a copy
whose only change is `const DEFAULT_SCORE='pulse';`.

## Verification

Picture: `verify.mjs` passes in Chromium and Firefox (seek pure in `t`). Strips at 1/10 s were
read across the 6 s iris, the 12.5 s sweep, the 16 s memory close, the 17.6–18.4 handoff, the
21.8–22.6 contact, the 23.8–24.7 night and the 25.5–26.3 title; at 1/30 s across the web pluck
wrap at 12.25. The release section was rendered to MP4 and its encoded frames tiled. All nine
worlds were inspected at 1:1.

Export: H.264 High, 1080×1080, 30 fps, 28.00 s, 840 frames decoded without error; AAC stereo
at 48 kHz. One encoded frame per second was tiled and read. Player checks cover score
selection, muting, playback, seeking and `?score=pulse` in Chromium and Firefox.

Not reviewed: the full export was not watched or listened to in real time, and no perceptual
audio review has been done. Choosing between the two scores still needs a listening pass.
