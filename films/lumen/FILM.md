# Lumen

Title: `lumen`. Byline: `a small impossibility`.

A seed contains a sun. Its first pulse opens impossible habitats; their energy folds back into
the seed, meets another pulse, and unfolds as a vast living flower. End with two small seeds
and enough paper to hear the last note.

## Design

Make the transformation feel inevitable, then surprising. Long asymmetric contours carry the
images: a folded husk, wind-bent sails, a moth's reaching wings, a curling petal. Use scale and
negative space for wonder; reserve the most saturated colour and fastest expansion for release.

Paper, a screened middle, and a small overprinted dark anchor every scene. Indigo and blue carry
depth; fluorescent pink and orange carry living matter. Yellow belongs to the light inside it.
Keep moving screens fixed to the page. Shape points move; screened bitmaps do not scale.

Use the project's written craft references and engine code. Other films' videos and extracted
images are excluded as creative references. Inspect Lumen's own renders to refine its motion.

## Scenes

| World | Centre seed | Values / shot / movement |
|---|---|---|
| Husk | crack in a suspended seed | paper / orange shell / dark seam; intimate; shell breathes |
| Sail | knot of a wind-drawn ribbon | paper / pink folds / indigo crease; cropped; long cloth lag |
| Moth | thorax of a sun moth | pale sky / blue wings / dark wing roots; immense; wings flex |
| Tide | aperture in an impossible wave | paper foam / blue sea / dark trough; full bleed; flowing filaments |
| Garden | hovering pollen above a tiny stem | paper / pink petals / dark soil; distant; pollen lifts |
| Furnace | opening between incandescent petals | yellow light / orange walls / indigo rim; macro; heat rises |
| Canopy | star caught in a fern | pale mist / blue leaves / dark fronds; cropped; bending tips |
| Eclipse | seed in a torn solar corona | paper centre / pink corona / indigo night; monumental; corona turns |

## Timeline

| Seconds | Passage |
|---|---|
| 0–1.5 | A dot on paper; two pulses; a tiny anticipation |
| 1.5–6 | Three windows open, then a dive through the seed |
| 6–14 | Connected worlds: overlapping reveals, directional sweeps, and a held small garden |
| 14–16 | Four nested memories fold inward through one continuously closing lens |
| 16–18 | A constellation of seed memories gathers, disperses, then rests |
| 18–22 | Two pulses approach; a drawn ribbon connects them; tension gathers |
| 22–24 | Explosive, staggered petal release; a living sun fills the print |
| 24–26 | The bloom becomes a night garden of smaller lights |
| 26–28 | Hand-drawn signature; the light returns to two seeds |

Departures from the [resonance form](../../docs/forms/resonance.md): eight new worlds instead of its subject list; a continuous
botanical release instead of the four-cut reprise; seed memories instead of a literal circular
scene archive. Six dramatic passages, centre discipline through 18 s, 28 s duration, plate
mechanics, deterministic seeking, and the self-contained delivery contract remain.

## Motion and score contracts

Each outgoing world remains until the next reveal covers it; cue end is next start plus next
opening duration. Do not reintroduce empty beats at 6, 8, or 10 s. `FLOW` owns these transitions,
including the small garden's readable hold and the fern's upward sweep. `memoryRadius(t)` owns
one continuous closing lens across all four recollections; per-shot radii caused visible jumps.

Tide's cycling filaments and spray fade to zero in opacity and stroke width before their
position wraps, with zero envelope slope at each endpoint. Recycling a visible carrier caused
a full-curve jump near 6.735 s and in the later recollection.

Keep the continuous reed and air bed through 16–18 s. Foreground tones follow `CUES`, `FLOW`,
and `ANSWER_PULSES`; sweep accents account for their initial travel outside the frame. `BLOOM`
owns petal timings, and the score derives its two accents from peak expansion at approximately
22.14 and 22.31 s. Preserve the flower's silhouette and the rounded, low-register swell.

## Delivery contract

`index.html`, 1080 square at 30 fps, with a deterministic offline score. The HTML is
authoritative and needs no build step. Run the seek contract in Firefox and Chromium.

Live path bands screen directly into one scratch plate; small solid marks composite as vectors.
The night transition shares one foreground flower, preventing duplicate work and a scale jump.

## Verification

Export: H.264 High, 1080×1080, 30 fps, 28.00 s, 840 decoded frames; stereo AAC at 48 kHz. Full
decode passed, and the encoded loop strip was inspected at 30 fps. Browser seek gates pass
around the loop wraps and recollection in Firefox and Chromium. After the filament fix, the
exact wrap comparison dropped from 3,142 to zero pixels with summed RGB change above 60.
Playback controls and mobile layout pass.

Independent cold renders of the offline score match. Peak is 0.79 with no clipped samples.
The 17–18 s RMS is −21.18 dBFS (previously −55.31); bloom lift over the
preceding music is 3.63 dB (previously 8.84). These are measured levels, not a perceptual
listening test.
