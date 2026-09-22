# Worked examples: where to look

Every shipped work is one `index.html` with the whole engine inline. These tables point at
named functions and constants; search for the name (`grep -n "function compose"`,
`grep -n "const VK"`) rather than trusting line numbers. Each film's `FILM.md` explains why
the design went the way it did; read it before borrowing from that film.

The common engine is in every file under the same names: `rngFor`, `buildScreen`/`screenOf`
(halftone screens), `bakePaper`, `bakeScene`, `print`/`plane`/`shade`/`carve`/`hatch`/`spray`
(plate marks), `nib` (tapered stroke), `makeWob`/`wobbler` (seamless wobble).

## films/window-seat — fixed-frame journey, 78 s

One window, a world that travels past it, and every content switch hidden under full cover.
Its own plate compositor lets live elements be drawn per frame without baked scenes.

| Technique | Where | Why copy it |
|---|---|---|
| Analytic speed profile | `VK`, `VSEG`, `S`, `accel`, `speed`, `invS` | Distance is a closed-form integral of smoothstep speed keys, so every position is pure in `t` and parallax, vibration and sound can all read `S(t)`. |
| Shot list for tools | `SHOTS`, `shot`, `window.__riso.shots` | Named shots with `readAt` and transition give the harness and score one timing source. |
| Live-plate compositor | `compose`, `resetPlates`, `put`, `add`, `knock`, `putM`, `smear`, `mixCov` | Per-plate coverage canvases screened by threshold at compose time; `put` occludes exactly, `knock` returns plates to paper, `smear` blurs along travel. |
| Parallax layers | `fields`, `bridge`, `forest`, `towers`, `mountains`, `ridgePath` | Each layer is placed by `S(t)` times its depth factor. |
| Reflections | `reflectPlates` (option `squash`), `canal`, `lakeside`, `mirrorAt` | Mirrors the plate stack below a waterline in rippled slices; `mirrorAt` turns the glass into a mirror in the dark. |
| Covered switches | `veil`, `fogD`, `hazeD`, `tunnel`, `passingTrain` | A content switch happens only while the view is a uniform field (D = 1) or fully occluded. |
| Sky keying | `SKYK`, `skyAt` | Palette keys over time; the one hard jump sits under a covered moment. |
| Seeded drops | `DROPS`, `dropPos`, `drops` | Seeded birth, stick time and radius; horizontal run follows `S(t)`, so drops stream at speed and fall straight once stopped. |
| Ballistic sparks | `BURSTS`, `ballistic`, `fwPos`, `fireworks` | Closed-form trajectories with drag; each burst is pure in its age. |
| Long exposure | `stars`, `STARS`, `POLE` | Trail arc length is a function of `t − T0`, not accumulated across frames. |
| Rainbow over reflection | `rainbow`, `lakeside` | Draw order fix: the arc drawn after the reflection so it does not mirror into an eye shape. |
| Sloshing glass | `SLOSH`, `slosh`, `glass` | A damped oscillator driven by `accel(t)` is integrated once at load into a table; `slosh(t)` interpolates it, so physics stays pure in `t`. |
| Level crossing | `crossing`, `X_LC` | A world event placed at a distance (`S(26.4)`), not a time. |

## films/lumen — resonance form, 28 s

A centre dot opens eight worlds through irises and sweeps, recollects them through one
closing lens, then releases a flower. The template for cue-driven abstract shorts.

| Technique | Where | Why copy it |
|---|---|---|
| Cue list and dispatch | `CUES`, `DRAW`, `render` | Each cue is `{start, dur, kind}`; `render` runs every active cue's `DRAW[kind]`. |
| Overlapping reveals | `FLOW`, `drawWindow` | Each outgoing world stays until the next reveal (`reveal: 'iris'` or `'sweep'`) covers it; no empty beats. |
| One closing lens | `memoryRadius`, `drawRecollection`, `drawMemoryLens` | One continuous radius across four recollections; per-shot radii jumped. |
| Colourway swaps | `SWAPS`, `bakeScene(id, size, swap)` | Remaps plates for the recollection without redrawing scenes. |
| Scene registry | `scene('tide', {...})` with `live(ctx,u)` | Baked plates per world plus one live element. |
| Loop-safe live element | tide's `live` | Envelope value and slope reach zero before a filament wraps; recycling a visible carrier teleports a curve. |
| Release | `BLOOM`, `flowerGeometry`, `petal`, `drawRelease`, `drawNightGarden` | Staggered petal timings in one const that the score also reads. |
| Answer and attraction | `ANSWER_PULSES`, `drawAnswerRipples`, `drawAttraction` | Two voices approach; pulse times shared with the score. |
| Signature | `SCRIPT`, `letterStrokes`, `writeLetters`, `drawSignature` | Handwritten title drawn stroke by stroke with a progress parameter. |

## films/emergence — resonance form, sibling of lumen

Same machinery as lumen with new worlds; adds interference, a branch generator and screen
supercells.

| Technique | Where | Why copy it |
|---|---|---|
| Iris and sweep transitions | `FLOW`, `drawWindow` (`reveal`, `angle`) | Same contract as lumen; the sweep angle is per cue. |
| Branch generator | `arbor`, `arborPaths`, `drawArbor`, `ARBOR`, `NEURON_ARBOR` | One seeded generator grows both dendrites and the release; branches carry spawn times so any age replays purely. |
| Interference | `interference`, `drawAnswer` | Nodal lines drawn analytically from the two voices' positions. |
| Loop-safe fades | `life`, `smooth01`, `fract` | `life(v, edge)` is zero with zero slope at both ends of a wrap (web pluck, bubbles, network dashes). |
| Memory absorption | `MEMORY_ABSORB`, `drawMemory` | One const drives both picture and score. |
| Network ending | `NET`, `NET_EDGES`, `drawNetwork` | The arbor shrinks to one node; pulses travel edges. |
| Screen supercells | `SCREEN` (header comment), `buildScreen` | Non-reduced tangents (3/3, 2/0) keep the angle but add sub-pixel phases, so slow ramps stop banding into plateaus. Compare lumen's reduced `SCREEN`. |
| Knockouts | `carve`, `print`, `shade` with `cut` | A knockout at full coverage clears the screen gaps; highlights return to bare paper. |
| Drawn year digits | `YEAR`, `yearPath` | Small numerals as paths, sunk into or carved from the ground plate. |

## prints/workings — print-kit still

A series of stills where every mark is on a baked plate, so `shade` coverage ramps are used
everywhere a film would settle for a flat pass.

| Technique | Where | Why copy it |
|---|---|---|
| Native bake size | `OUT`, `K`, `PITCH` | Pitch scales with the bake size so a larger print re-rasterises instead of resizing a screen. |
| Stills driven like a film | `PRINTS`, `window.__riso` (`seek: render`) | Each integer time is one print; the tools shoot it unchanged. |
| Baked coverage ramps | `shade` | Gradient stops screened at bake time. |
| Structure helpers | `towerPath`, `hangPoints`, `span` | Seeded architecture and sagging cables. |

## studies/

| File | Demonstrates | Look at |
|---|---|---|
| `studies/index.html` | Drawing-craft A/B pairs: silhouette, stroke, ramp, form, texture, depth, exemplars, motion weight and launch, live flame | `STUDIES` (ids and captions), `flame`, `FAMILY` |
| `studies/composition.html` | Frame budget, edge hierarchy, one event at several distances | `STUDIES`, `word` |
| `studies/scene-space.html` | 3D camera, path travel, cuts that preserve action time | `camera`, `pathByLength`, `travel`, `hermite`, `ballistic`, `staticObjects`, `motionObjects`, `SHOTS`; notes in `docs/scene-space.md` |
| `studies/sound.html` | The sound kit; see `riso-score/examples.md` | `Score`, `STUDIES` |

## How to borrow

- Copy routines, not scenes. A scene is tuned to its film's palette, timing and framing;
  the function underneath (`reflectPlates`, `arbor`, `life`) is what transfers.
- Check for collisions before pasting: every file defines `render`, `SCENES`, `INK`,
  `SCREEN`. Rename the borrowed routine or its constants when a name exists.
- Keep seeds keyed: take randomness from `rngFor('<film>:<thing>:<index>')`, never
  `Math.random()`, so the borrowed routine stays pure in `t`.
- Bring the timing contract with the routine: if it reads `S(t)`, `FLOW` or `CUES`, supply
  an equivalent in the new film rather than hard-coding times.
- Rerun `verify.mjs` after the paste; seek purity breaks quietly.
