# Roost

70 seconds, 1080 × 1080, 30 fps, with a chamber string score. Authoritative source: `index.html`.
Delivery: a Firefox render (`render.mjs`) to `out/roost.mp4`; score `out/roost.wav` (48 kHz stereo).
The scored Firefox export decodes to 2100 frames, 70.00 s, 1080² H.264 High, with AAC stereo
at 192 kb/s. Sample credits are retained in MP4 and WAV metadata.

## Premise

A starling murmuration over a marsh from sunset to nightfall, in one fixed view. Birds are
the halftone: each starling is a solid 2–3 px indigo dot, and where the flock's thin sheet
turns edge-on the birds pile into dark printed ribbons. The film follows one evening's
murmuration from arrival to roost. Why it ends this way: a murmuration ends when the flock
pours into the reeds for the night, so the last action is the sky emptying into the reedbed,
followed by stars.

## Passages (one continuous take)

| t | Passage | Action |
|---|---|---|
| 0–6.5 | marsh | Empty golden sky, low sun, reeds sway. Breath before the arrival. |
| 6.5–21 | gathering | Small groups fly in from both sides and fuse centre-out into one sheet over the sun. |
| 21–34 | murmuration | The sheet folds; the twist makes dark bands run along it; the sun touches the far shore. |
| 34–45 | falcon | A falcon circles top right (33–37), stoops (37.2–38.3), and punches a hollow that trails it. A dark agitation wave runs outward and the flock splits and rejoins. |
| 45–57 | overhead | The flock swings toward the camera; the camera tilts up (horizon 770→1020); individual flapping starlings pass out the top of frame; brief empty dusk while they are behind us; they re-emerge from the top, receding. |
| 57–66 | roost | The flock compresses and drains, starting from its roost-side end, in a spiral funnel into the far reedbed, doubled by its reflection. |
| 66–70 | night | Fourteen stragglers hurry in from the right and drop; stars; hold. |

`__riso.shots` in the source is authoritative for these times.

## Design decisions

- Inks: yellow, pink, blue, indigo. Sky is a live vertical ramp keyed through five states
  (golden, sunset, afterglow, dusk, night). Birds use indigo alone, solid, so they print as
  crisp overprint darks on any sky. Close birds and the falcon use indigo plus pink, with
  pink's registration miss acting as the fringe.
- Flock model: every bird owns (u, v, w) on a thin 3-D sheet. The cross-section twists
  along u (`th0 + tw·u + tw2·u²`), and there is also spine bend, yaw and lobed thickness,
  all sums of slow sines. Perspective projection with focal 1000 px. Everything is analytic
  in t, so there is no simulation. Arrival blends each band from a small round travelling
  group into its sheet slot. The falcon pushes birds from its current and two lagged
  positions, and the strike adds a travelling twist pulse plus a split gap.
- Camera: fixed, except the tilt during the overhead pass, which is modelled as a
  horizon shift. All layers hang off `horizon(t)`.
- Water mirrors the plates above the horizon in 2 px slices with ripple offsets, so the
  sun, clouds, shore and flock all reflect. Glitter fades as the sun meets the shore.
- Sun path on the water: a steady column of ripple strips fixed to the page, with widths
  that breathe slowly, plus glints that grow and shrink over about 2 s at full ink. Earlier
  glints switched on and off at 5.3 rad/s and flashed (user report). Fading 1 px dashes by
  coverage instead makes them vanish below the screen. Birds are also drawn to `BK`, which
  is mirrored with the same ripple into `BR`. `BR` is cut out of the glitter mask, so glints
  never print over reflected birds. Measured change between adjacent frames in the glitter
  area: 5.4% → 0.1% of pixels at 4 s, 3.8% → 0.1% at 16 s.
- Foreground: 210 seeded Phragmites stems with ribbon leaves and drooping plumes; plumes
  are a separate lighter plate mask. Sway comes from per-stem sines plus a shared gust.
- Live-plate compositor copied from `films/window-seat` (`compose`, `put`, `putM`).

## Subject references

From general knowledge, **not inspected images this session (unverified)**: starlings
gather at dusk over reedbeds; murmurations are thin 3-D sheets whose density bands appear
where the sheet folds; predator attacks send dark agitation waves through the flock; flocks
end by pouring into the roost; the starling silhouette has triangular pointed wings and a
short square tail; Phragmites has drooping feathery panicles.

## Verification

- `verify.mjs`: seek is pure in t in Chromium and Firefox across 26 times including shot
  boundaries.
- Inspected sheets: review sheet, arrival (5–11 s), overhead strip (49.6–51.6 s at
  0.25 s), pour (58–67 s at 0.75 s), 1:1 frames at 20, 24, 38.5 and 50.8 s.

## Remaining work / known weaknesses

- Audio monitoring is unavailable in the scoring session; timbre, phrasing and perceived sync
  still need a listening review of the muxed film.
- Arriving groups are soft ovals and could be more ragged.
- Thin cloud streaks read as lines at sheet scale.
- The funnel reads as a wedge more than a spiral; its swirl radius is small at 330 m.
- Frame-rate strips at every handoff were not all inspected; there are no hard cuts, but the
  re-emergence at 55–57 s was inspected at 0.5 s spacing during scoring.

## Score

Direction: calm, deep strings with a soft solo violin. Soft recorded cello section and a
restrained, centred bowed bass support one four-note violin idea, D–E–A–F♯. D major with
sixths, added ninths and a brief B-minor colour gives the falcon passage movement without a
dramatic impact. The approach lifts the violin's register; the return reverses the idea and
the cello answers down into the reeds. Sources, preparation and reconstruction are in
[AUDIO-SOURCES.md](AUDIO-SOURCES.md).

The compound pulse has two dotted quarters per implied 6/8 bar. It moves continuously between
48 and 62 dotted quarters per minute according to visible flock density and world-space speed.
Long opening phrases float across it; the approach follows it more closely. Individual
wingbeats do not trigger notes. Bass stays centred; the violin gently follows the visible
flock's horizontal position. No percussion or literal bird calls.

`FLIGHT_SCORE` samples `birdPos`, `flockState` and `flockC` on a fixed 30 Hz timeline. It derives
arrival, the close pass, exit and return from projected birds. `TS` supplies the strike;
`TR` supplies the first pour; `SHOTS` supplies the passage boundaries. These are shared
picture data, not a separate copied cue clock. Retiming the picture retimes the score.

| Cue | Music |
|---|---|
| 0–5.1 s, empty marsh | Cello D and a quiet low D; a slow opening bow |
| 5.1 s, first substantial arrival | Violin introduces D–E–A–F♯ as the groups become visible |
| 21 s, gathered flock | The motif returns over moving inner voices |
| 38.3 s, falcon strike | Soft violin bow and minor colour; no hard transient |
| 49.9 s, close pass | Higher violin and the score's main swell |
| 51.33–56 s, flock behind camera | Foreground recedes; low strings and a held fifth continue |
| 56 s, return | Violin re-enters, then descends A–F♯–E–D |
| 59.4 s, pour begins | Cello descends toward D while the violin settles |
| 66–70 s, night | Final open D, soft tail; near-silence from 69.5 s |

The five published marks are 5.1, 38.3, 49.9, 56 and 59.4 s. These are bowed musical cues,
not impact effects. Harmony pre-laps the return by 0.45 s; no cut fades through digital silence.
The quiet interval behind the camera is deliberate thinning, not a dropout.

### Measured review

Firefox WAV: I −16.0 LUFS, LRA 5.1 LU, TP −2.85 dBTP, clipped 0, two cold renders
byte-identical (`97dcd25eb0d992d9`). Exactly 70.000 s, 48 kHz stereo. FFmpeg independently
reports I −16.0 LUFS and LRA 5.2 LU. No detected discontinuities or unintended valleys.
The final AAC MP4 measures I −16.0 LUFS, LRA 5.1 LU and TP −2.9 dBTP after encoding.
Chromium also passes at I -16.0 LUFS and TP -2.88 dBTP; its two cold renders differ by at
most two 16-bit steps, the expected browser summation jitter. Stereo correlation 0.690. The dark balance is deliberate: approximately 51% below 250 Hz,
43% at 250 Hz–1 kHz, 5.4% at 1–2 kHz; the recorded bow noise remains quiet above that.

| Mark | Local energy peak relative to mark | Before → after |
|---|---|---|
| Arrival, 5.1 s | +190 ms | −21.0 → −20.6 LUFS |
| Falcon, 38.3 s | −200 ms | −16.7 → −17.7 LUFS |
| Close pass, 49.9 s | +25 ms | −15.7 → −12.7 LUFS |
| Return, 56 s | +300 ms | −20.8 → −17.1 LUFS |
| Pour, 59.4 s | −280 ms | −14.8 → −17.2 LUFS |

The detector sees no distinct transient onset at four marks; at the return it sees the
intentional pre-lap at −120 ms. Broad bow cues must be judged with the picture, not treated
as a passed 40 ms impact-sync test. The approach's local swell peaks +25 ms from its mark.

The waveform/spectral sheet and overhead/return strip were inspected. Audio was not heard.
`verify.mjs` passes consecutive, reordered and cold seeks at 26 times in Chromium and Firefox;
the original drawing/motion source remains unchanged. Player checks cover muted startup,
cached audio, pause, seek, resume and a recording with an audio track. No runtime network
requests or page errors occurred. The page's Record control includes the score even while
the local monitor is muted; the frame-by-frame MP4 is the full-quality delivery.
