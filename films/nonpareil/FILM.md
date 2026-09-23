# Nonpareil

70 seconds, 1080 × 1080, 30 fps, scored for handpan over a slow bass. Working title after the
fine-combed marbling pattern; *nonpareil* also means "without equal", which is what a marbled
sheet is: a monotype, printed once from a bath that the printing empties.
Authoritative source: `index.html`.
Delivery: the MP4 is attached to [the v1.0 release](https://github.com/sevenevesai/riso-windowseat/releases/tag/v1.0).
Paths under `out/` below are the maker's local, git-ignored evidence; the first delivery is kept
there for comparison as `out/nonpareil-v1.mp4` / `.wav` (with `nonpareil-v1-index.html`).

## Premise

Paper marbling seen straight down into the bath. A newsprint strip skims the size clean; drops
of colour land and push every earlier colour outward; brush taps sprinkle stones; a rake drags
them back and forth into chevrons; a fine comb pulls those into arches; the comb returns swaying.
A flower is dropped into the middle (a bullseye pulled up into a bud, two green drops pulled
into leaves, a line of drops drawn into a stem). The camera draws back to the whole tray. A
sheet glides in as a loose roll and unrolls across the size, wetting through; lifted by its far
edge, it rolls back over toward the lens like a page being turned, and the print comes face up,
mirrored, while the size keeps only a ghost. It lands on the slate beside the tray, is rinsed,
and the camera closes on the printed flower.

Why it ends there: the print is what marbling is for, and it cannot exist without emptying
the bath. The mirror (the leaves swap sides) is the subject's own fingerprint of that transfer,
and the page-turn shows it happening instead of cutting to it.

## Passages (one camera, no cut)

Beats are the 96 BPM grid, beat b at 2.9 + 0.625·b s (`BEAT`, `G0`, `beat()`).

| t | Passage | Action |
|---|---|---|
| 0–2.9 | skim | a newsprint strip is dragged down the size, taking the dust with it |
| 2.9–12.9 | ground | plum, rose and cobalt drops land on the grid; each pushes the others outward |
| 12.9–17.9 | stones | brush taps: bursts of 14–21 small drops (ochre, white, rose, cobalt) pack into stones with veins |
| 17.9–22.9 | rake | seven pins across and back, offset half a gap: gel-git chevrons |
| 22.9–28.5 | comb | the camera closes to 1.55× while a 34-pin comb crosses; arches form behind the bar |
| 28.5–32.3 | wave | the comb returns up, swaying: waved nonpareil |
| 32.3–45.4 | flower | bullseye (white, pink, yellow, pink) pulled into a bud; leaves; stem; the camera settles in to 1.18×, then from 44.6 draws back to 0.8× to show the tin tray on its slate table |
| 45.4–49.8 | lay | the sheet glides in as a loose roll (b68), touches down on the left (46.65, b70) and unrolls to the right, crossing the flower on b72 and laying its right edge on b74; the pattern wets through behind the contact |
| 49.8–56.0 | peel | lifted by the right edge on b75, it rolls back right to left toward the lens: the print face up and mirrored on the turning flap, the ghost on the size behind; the flower turns face up on b81 (53.525); the camera follows it off the tray; it lands on the slate on b85 (56.025) |
| 56.0–70 | print | a rim of water spreads from under it; a rinse runs down it b86–b90 (front at mid-sheet on b88), lifting a veil and leaving the window reflected in the wet print; rivulets start on b90–b96 and drip off; the camera closes on the flower b88–b103; about 2.7 s rest |

`TL` and `SHOTS` in the source are authoritative for these times; `OPS` holds every drop and pass.

## Design decisions

- Mathematical marbling, not simulation. Each drop is a closed polygon in bath
  coordinates. Operations are the closed-form maps of Jaffer & Lu (2012): a drop of radius r
  at c sends p to c + (p−c)·√(1 + r²/|p−c|²); a pin moving along M displaces by z·e^(−d/λ)
  behind its tip; the swaying comb shifts sideways by A·sin(k·a). All are bijections, so
  boundaries stay simple closed curves and painting drops oldest-first is exact. Edges that
  stretch past 1.8 px are refined through the map (up to 12 levels); crowded points decimate.
  The final state is about 150k vertices.
- Pure in t. A frame applies the complete ops prefix (cached every 16 ops, recomputed
  identically from the nearest checkpoint) and then any in-progress ops at their progress.
  Drop area follows easeOutCubic; tools use ease-in-out travel. `wtip ≥ 1.65 z` keeps each
  pin's drag monotonic along its stroke, which is what keeps the map a bijection.
- Plates. Two opaque coverage canvases hold indigo, pink and yellow in r, g, b and blue
  in r. An opaque fill replaces coverage (a drop owns its value), antialiased edges blend
  linearly, `lighter` overprints shadows and `multiply` knocks ink back toward paper (window
  sheen, impact ripples, water). `compose()` screens each channel against page-pinned threshold
  tables with mottling and starvation (copied from `films/window-seat`). Registration offsets
  make the misregistered fringes at every colour boundary.
- Palette. Four inks: indigo, fluorescent pink, yellow, blue. Paint colours are
  overprint recipes: plum (indigo + pink), rose (pink + some yellow), ochre, cobalt
  (blue + a little indigo), green (blue + yellow), fluorescent pink and yellow for the flower,
  and white paint as bare paper. The bare size is a pale blue-grey screen; on the print it is
  paper. The tray is pale tin, the table slate with fixed cleft streaks.
- Physical cues. A falling bead and its shadow converge on each landing (light from the
  top left); up to three ripple rings run out from each impact; a four-pane window reflection
  sits in the size, and returns in the wet print during the rinse. Tools cast soft shadows.
- The sheet (`sheetAt`, `drawSheet`). One curve across the fold, sampled every 2 units of its
  width s (the bath x it lies on); the same along the fold (bath y). The lay is a loose curl
  (`CURL`, 1.35π over the free length) whose contact runs left to right; the peel is a loop
  (`LOOP`, angle 0 → π on a smoothstep of length λ) rolling without slipping, so the flap lies at
  x = 2a + λ − s: mirrored by construction, and at a = −80, λ = 0 exactly at `PX − s` on the
  table. Heights project by `HCAM/(HCAM − Z)` (HCAM 1600), so the curl and flap grow toward the
  lens. The finished pattern is baked once as coverage (`PAT`, 1.5 px per unit) and drawn in
  runs of samples that one affine map can carry; the print face shows where the projected order
  of s reverses. The face is blank paper until the sheet has been printed. Screening stays in
  `compose()`, so no screened bitmap is ever resized. Each run is shaded by Lambert against the
  top-left light; the raised sheet casts its shadow on the size or table before any of the
  sheet is drawn, and only the overhanging flap shades the sheet still lying down.
- Camera. Fixed overhead, orthographic scale z on the size. It eases to 1.55× over the comb's
  pass and 1.18× over the flower. `camTail` takes over at 44.6 s (continuous: z 1.18, y 520),
  draws back to 0.8×, follows the sheet's mean x (averaged over the last 0.6 s) while it is
  carried to the table, then pushes to 1.1× on the printed flower.
- Performance. v1 measured 13–100 ms per sequential frame (up to ~370 ms on a cold seek); this
  session measured 99 and 122 ms at 30 and 44 s and 28–221 ms across the tail in Firefox (the
  roll's many runs are the heaviest). The in-page player buffers frames before playing.

## Revision 2: why the last 20 s were redone

The user approved the film but found that around 50 s it "gets very off track": a different pace
and quality. Diagnosis on v1 (`out/np2-diag/`: 20–44 s and 44–70 s every 0.5 s in Firefox, 1:1
crops in `crops.png`), all four hypotheses confirmed:

- Pace. Mean frame change per 0.5 s step: 0.056 over 20–44 s, where the longest static run was one
  step; v1's tail had 13 of 52 static steps (52.0–52.5, 55.0–56.5, 58.0–59.5, 69–70). In 0–44 s
  small local actions (stylus pulls) still change the frame every step.
- Quality. Mean saturation 0.57–0.62 in the bath fell to 0.07 on the plain sheet (47.5 s), 0.30
  on the 24–34 % wet-through (51.0 s), 0.24 on the 7.5 % ghost (55.0 s). The v1 print itself was
  as saturated as the bath (0.60–0.62); the flat slate board and the hard shadow band on the
  sliding edge (53.5 s crop) were the other flat areas.
- Physicality. The sheet translated as a flat rectangle; the print arrived by a hard cut at 56.8 s.
- Score. Between 50.0 and 56.8 s v1 had one handpan note (A5 at 54.75); valleys at 47.6 s
  (−13.4 dB) and 56.7 s (−10.2 dB).

After the redesign (`out/np2-final-tail/`): saturation min 0.42, mean 0.54 over 44–70 s (v1 0.07
and 0.46; 20–44 s 0.56 and 0.59); 5 of 52 static steps, all in the final 2.5 s hold; mean
change per step 0.085.

## Subject references (inspected)

In `out/nonpareil-ref/` (Wikimedia Commons):

- `ebru.jpg` (Ebru water marbling): stone pattern, where later drops pack into polygons and the
  first colour survives as thin veins; a stylus is a needle on a turned handle.
- `video_frame.jpg` (from "How to paint on Water for Paper Marbling and Ebru Art"): a metal tray,
  full-coverage dark stones, white spots, and combed feathers.
- `combed1826.jpg`, `hudibras.jpg`, `board.jpg`, `combed1740.jpg`: nonpareil, bouquet and curl
  patterns.
- `out/nonpareil-ref2/baku_11.jpg` ("Making marbled paper in Baku", Commons): a shallow
  galvanised tray with a rolled rim on a table, finished sheets lying face up beside it. The
  other ten photos of that series were rate-limited and not seen.

Not inspected: how a sheet is laid and lifted in practice. The loose roll, the page-turn peel and
the rinse are from general knowledge and stylised; the roll in particular is a legibility choice
(it covers a third of the bath instead of all of it), not an observed technique.

## Motion checks

- Drop landing strip (2.70–3.30 s at 1/30 s): bead and shadow converge; the disc opens fast and
  creeps to rest.
- Comb close-up strip (24.6–25.2 s at 1/30 s): arches form behind the bar without pops.
- The 44.6 s hand-over from `cam` to `camTail`: mean frame change 0.004, 0.016, 0.051, then 0.19
  and 0.71 as the draw-back eases in; no step.
- Tail strips at 1/30 s (`out/np2-strip-*`): the roll's glide and touchdown (45.9–46.7), the lift
  (49.6–50.4), the landing (55.6–56.4), the rinse start (56.45–57.05), the push start (57.7–58.3):
  continuous. The roll's glide peaks near 2000 px/s before it settles.

## Score

Handpan over a slow bass, at the user's direction ("just a nice handpan, with whatever bass
in the background to draw out slow tunes"). Sources, preparation and licences:
[AUDIO-SOURCES.md](AUDIO-SOURCES.md).

- Handpan (D Celtic minor: D E F G A C, D2–A5) carries every melodic and rhythmic idea.
  The drops are the notes: each ground drop sounds on its landing, panned by its x. The first
  four plum drops state the motif, A–D–E–F. Brush taps are rolls with ghost taps; the rake
  arpeggiates as its pins cross; the comb runs down the scale, one tone per band; the swaying
  return climbs and wavers. The bullseye restates the motif; the bud, leaves and stem each sound.
- The tail, on the same grid. The roll glides in on A4 (b68) and touches down on the ding and its
  fifth (b70); it unrolls with a run up the pan, one tone per band the contact crosses (A3 → A5).
  Lifted (A4, b75), it rolls back with a run down (D5 C5 A4 G4), and as the flower turns face up
  on b81 the motif sounds mirrored, F–E–D–A; G3 and E3 step down to the landing on low D and the
  ding (b85). The rinse front crosses with E5 D5 C5 A4. Each rivulet is a note of the motif,
  A D E F on b90–b93, falling home E D on b95–b96; low D, the ding and A4 ring out from b100.
- Bass (cello section and contrabass) changes on picture events: D · C · B♭ · A (ground to
  stones), G · A (rake), D (comb), B♭ · C (sway), D · F · G · A (flower), then D (the sheet comes
  in), F (it wets through across the flower), B♭ (lifted: the bath empties), C (the flower turns
  face up), D (the print lands). B♭ is the one pitch the handpan lacks. Cello tunes: A–G–F under
  the comb, A–C as the bud draws up, F–E–D (b88, b93, b97) under the print.
- The edge gesture (`edgeGesture`, `edges()`), replacing v1's paper slides on the skim, the sheet
  laid and the peel. Each tone is a handpan recording played backwards into the moment the edge
  crosses mid-frame (its decay becomes the swell, the decay undone up to +24 dB so the rise starts
  with the edge), then forwards out of it with the strike softened, gone as the edge leaves;
  panned with the edge. Skim D4 + A4; lay A3 + E4; peel C4 + A4 (recordings that ring 7.5 s,
  long enough for its 3.75 s rise).
- Alternative built and measured, not chosen: `GESTURE = 'resonance'`, pink noise through
  band-passes (Q 60) on the same pitches, the open band stepping up the set with the edge. It
  follows the edge's entry exactly but peaks 105–290 ms late, and it is still a filtered noise,
  the family the user objected to. Switch the one constant to hear it.
- Sync marks (`SCORE_MARKS`): 2.9 s (first drop), 12.9 s (first brush tap), 32.275 s (bullseye),
  46.65 s (the sheet touches down), 56.025 s (the print lands).

### Measured review

Firefox WAV: I −16.0 LUFS, LRA 6.3 LU, TP −2.3 dBTP, clipped 0; two cold renders
byte-identical (`4e4af44850df5f4a`). Exactly 70.000 s, 48 kHz stereo; ffmpeg ebur128 agrees
(I −16.0, LRA 6.3). Stereo correlation 0.46. Bands: 35 % below 250 Hz, 63 % at 250 Hz–1 kHz,
1.2 % at 1–2 kHz, nothing measurable above: v1's 0.45 % above 2 kHz was the paper grains.
Discontinuities: none in the whole file (v1: 19, of them 18 in the skim and one at 46.27 s).
Valleys: only 20.45 s and 22.9 s, the unchanged breaths between tool passes; the tail's
short-term loudness holds at about −17 to −18 LUFS like the rest.

| Mark | Onset | Before → after (short-term LUFS) |
|---|---|---|
| 2.9 first drop | 0 ms | −27.6 → −19.6 |
| 12.9 first tap | 5 ms | −14.7 → −12.8 |
| 32.275 bullseye | 0 ms | −15.0 → −16.2 |
| 46.65 touchdown | 0 ms | −21.3 → −16.7 |
| 56.025 print lands | 5 ms | −20.0 → −16.2 |

Edge gestures, measured alone at the mix's gain (`out/np2-gesture.mjs`, Firefox; `--around`
sheets for both variants in `out/np2-gestures/`):

| Edge | Edge in → mid → out (s) | Swell onset → peak (s) | Peak vs mix (dBFS) | Spectral peaks |
|---|---|---|---|---|
| skim | 0.69 → 1.444 → 2.12 | 0.69 → 1.459 | −25.6 vs −28.7 (alone with the bass) | D5, D4, A4 |
| lay | 46.65 → 47.90 → 49.15 | 46.66 → 47.85 | −23.3 vs −18.8 | E4, A3 |
| peel | 49.78 → 53.525 → 55.83 | 50.65 → 53.465 | −26.1 vs −20.6 | C4, A4 |

Onset is where the gesture rises within 40 dB of its peak. The dry sound is shaped to end at the
edge's exit (the peel's measured end is 55.57 s); reverb carries the skim and lay 0.4–1 s further
at under −40 dB of their peaks. The resonance variant
measured onsets 0.75 / 46.75 / 49.80 s, peaks 1.549 / 47.91 / 53.395 s, and after a −7.5 dB
calibration peaks of −27.0, −24.9 and −22.4 dBFS.

Nothing was heard: no audio monitoring was available in this session, so the gesture's timbre,
whether it reads as smooth and in tune, the balance, and perceived sync are unreviewed by ear.

## Verification

- What stayed as delivered: `verify.mjs` frame hashes at all 22 times the two versions share
  from 0 to 42 s are identical to v1 in both engines, and the 44.5–44.6 s hand-over is continuous.
  Audio from 6 to 44.5 s is v1 scaled by −0.33 dB (the mix is re-normalised to −16 LUFS once),
  with a residual 80 dB down; 3–6 s differs only by the skim gesture's reverb tail (−47 dB). The
  bass's move to D stays at v1's 45.7 s so the held A before it is re-cut identically.
- `verify.mjs`: seek is pure in t in Chromium and Firefox at 35 times, including every shot
  boundary and the frames either side of them.
- `review.mjs` (Firefox): one note, "third consecutive continuous handoff" at the rake; the film
  is one camera by design.

## Delivery

`out/nonpareil.mp4`, a Firefox render (236 s). Decoded: 2100 frames, 70.00 s, 1080²,
H.264 at 30 fps, with AAC stereo at 48 kHz; the muxed audio measures I −16.0 LUFS, LRA 6.3 LU,
peak −2.3 dBFS. The file is 251 MB (v1: 182 MB); page-pinned halftone at 1080 is high-entropy.
Score WAV: `out/nonpareil.wav`. Encoded frames at 46.3, 48.0, 52.9, 53.525, 55.0, 56.1,
58.0 and 66.0 s (`out/np2-enc/`) match the source renders; a 1:1 crop at the fold (53.525 s)
keeps its halftone dots.

## Remaining weaknesses

- The score has not been heard, including the new edge gesture and the tail's phrases.
- The roll glides in fast (about 2000 px/s at its peak) and covers the left third of the bath for
  about a second at touchdown; it is plain cream paper while it does.
- The rinse reads as a light front with flow streaks and rivulets; there is no refraction or
  colour shift under the water.
- Handpan sources are Freesound's 128 kb/s MP3 previews; the CC0 WAV originals need a
  logged-in download and would be a straight swap in `build-sample-bank.py`.
- The stem's top drop pulls into a small heart; the stylus reads as a thin line; tool
  bars are flat strips with nail heads.
- In-page playback buffers every frame before it plays; the MP4 is the way to judge pace.
