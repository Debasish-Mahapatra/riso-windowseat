# Held

A paper kite flies only while something holds it. Its line frays and parts at a hillside
stake; loose, the kite cannot fly, only tumble, and it falls across a harbour town. A church
weathervane snags the trailing line for a moment of false flight and lets it go. Over the water
the line drapes across a sloop's forestay, slides to the masthead, goes taut, and the kite
climbs again, now held by the boat sailing out into dusk.

The ending belongs to the subject: lift needs tension. The rhythm follows the line's state:
taut (dancing), fraying (strain), slack (tumble), briefly taut (vane), slack, taut for good
(climb and hold). The last shot pulls back from the kite to reveal what holds it; the kite,
higher, keeps the sun after the sea has gone to dusk, and the masthead lamp lights.

Delivery: the MP4 is attached to [the v1.0 release](https://github.com/sevenevesai/riso-windowseat/releases/tag/v1.0).
It is a Firefox render (`render.mjs`) of `index.html`, which is authoritative.

## Form

- 70 s, 1080², 30 fps, Firefox primary. One continuous afternoon → dusk.
- Live plates for the whole film (window-seat compositor: `compose`/`put`/`add`/`knock`):
  yellow, pink, blue, indigo. Grass = blue over yellow; roofs and sunset = pink over yellow;
  darks = indigo over blue. No black. Camera moves (knot push-in, traverse, ending pull-back)
  are vector reprojections before screening, so the screen stays pinned to the page.
- Kite: pink diamond sail, yellow upper panel, indigo spine and bowed spar crossing 28% down.
  Tail with alternating pink/yellow bows. Tails and loose lines are Verlet chains (see Motion).

## Subject references (from knowledge; no images inspected this session)

- Eddy/diamond kite construction: spar at 20–30% of the spine, bowed for dihedral, tow point on
  the spine; tail several spine lengths.
- A kite without tension loses angle of attack: noses over, spins, falls in swoops. Tension
  restores lift at once: it snaps nose-up and climbs to the edge of the wind window.
- Three-ply line parts ply by ply; parted ends unlay and curl.
- Bermuda sloop: mast ≈1.3× hull length, forestay to the bow, backstay, main on a boom, jib.

## Shots (authoritative: `SHOTS` and the event constants in index.html)

| t | shot | action | eye at the cut |
|---|---|---|---|
| 0–11 | hill, low wide | kite dances figure-eights on a sagging line to a stake; big gust at 10.3 | down the line to the stake |
| 11–18.4 | knot, close, slow push-in | round turn and hitches on a post; plies part at 13.0 (`K_PLY`) and 15.4; line snaps 17.8 (`K_SNAP`), far end whips out, stub drops | up-right, the whipping end |
| 18.4–34 | loose, side-on tracking | kite leaps, noses over, tumbles over the town; line snags the vane at 26.4 (`L_SNAG`), kite flies 1.8 s, line runs off the vane's tail at 28.2 (`L_SLIP`); falls toward the harbour | kite falling right/down |
| 34–48 | catch, medium | kite drops almost vertically at the end of its fall; tail touches water 36.9 (`C_TOUCH`); gust lifts it straight up; the boat sails into the taut line, which catches at the bow 40.6 (`C_CONTACT`), slides up the forestay to the masthead, taut 41.4 (`C_TAUT`); kite pitches nose-up, climbs and slows into the hold; camera pans with the boat | up with the kite |
| 48–70 | out, pull-back | opens close on the kite at sunset, pulls back (48.5–60) to the small sloop; sun sets, boat goes dark while the kite keeps the light; lamp at 63.2 (`E_LAMP`); stars; hold | the kite and the lamp |

## Motion (v2: tail glitch and choppy catch)

- **Chains.** `simChain` is a Verlet rope integrated once at load on a fixed 1/240 s step,
  recorded at 60 Hz and sampled by interpolation, so `seek(t)` stays pure. The head node
  rides the attachment point exactly. It has segment and minimum-bend constraints, gravity,
  drag toward `breeze()` (a steady wind plus eddies carried downwind, which make the
  flutter), and an optional water plane with friction. Each sim starts about 1 s before its
  shot so it arrives settled. Tails: hill, loose, catch and out, 41 nodes each. Lines: loose
  (900 px, 61 nodes) and catch (1500 px, 91 nodes). `trail()` and its drawn-on `wave` are
  gone. Bows are oriented from nodes ±2. Firefox page load, two runs each: v1 1204/441 ms,
  v2 1255/1244 ms, so up to ~0.8 s is added at load. Render cost is unchanged (~83 ms/frame).
- **Grips.** `gripAt` pulls the rope point at arc length s onto a moving point, so line can
  run through a snag. The vane takes the line where it is nearest the pivot at `L_SNAG`; the
  kite draws line through the snag as it rises, and it is let go over 0.12 s at `L_SLIP`.
  The `L_KEYS` 25.6/26.4 keys moved left (1920→1800, 2200→2004) so the hanging line
  itself sweeps into the vane at 26.4 (0.1 px). Key times are unchanged, so the score's
  spin runs are too.
- **Catch path.** `C_KEYS` are Hermite keys with explicit velocities (`hk`). From `C_TAUT`
  the kite is keyed relative to the masthead (`C_HAND`), starting from its world position
  and velocity: it loads and pitches nose-up by 41.9, climbs and eases to rest at R 300
  by 44.8, and the hold wobble fades in with zero slope. At `C_CONTACT` the grip starts at
  the line's nearest point on the stay (`C_GRIP`, 11 px away; they truly cross 1.5 frames
  later) and blends in over 0.1 s. It slides to the masthead by `C_TAUT` while the kite
  side is drawn in to straight (1.004 × distance). After that the kite pulls line out
  over the masthead as it climbs. The whole line stays behind the sloop, so its draw
  order never switches.
- **Boat.** It starts at world x 175 (was 277). The keyframed kite tows the line taut
  across the water, so the bow meets it wherever it lies. From x 175 the first crossing is
  40.65; from 185 on, the bow grazes it from ~39.1. C_V and the pan are unchanged. The
  held boat sits ~100 px further left than v1.
- **Derived events.** `C_RING` is no longer a constant: it is where the simulated tail
  first touches the water, x 719.7 at 36.921 (0.6 frame after `C_TOUCH`). The water drop's
  pan follows it. No event constant moved.
- **Measured** (`films/held/jitter.mjs`, Firefox). Largest frame-to-frame displacement of a
  chain point relative to its neighbours, 1/30 s, 18.4–48:

  | | v1 | v2 |
  |---|---|---|
  | loose tail | 31.0 px (median 24.9) | 4.6 px (median 0.27) |
  | loose line | 3.6 | 8.5 (vane grab 26.9; slip 28.2) |
  | catch tail | 25.8 (median 18.2) | 6.6 (the dive bottom 37.8) |
  | catch line | 6.2 | 10.9 (grip sliding up the stay 41.0) |

  Cause of v1's tail number: `wave` took each normal from the previous point after it had
  been displaced, so the tip crumpled into a zig-zag every frame in every shot. Without
  wave, the spin loops still gave 7.9 px at 21.4. The v2 line maxima are the physical
  events (catch, release, sliding contact), not frame jumps.
  Catch kite, 34–48: peak acceleration 7412 → 2226 px/s² and peak spin acceleration
  117 → 11.5 rad/s². v1's peaks were both the kink at 41.4; v2's are the swoop at the dive
  bottom.

## Score

Found instruments, all CC0 1.0 by Versilian Studios (Sam Gossner), embedded as 16-bit mono
32 kHz FLAC (`SAMPLES`, written by `build-samples.py`; exact files in `AUDIO-SOURCES.md`):

- VCSL (github.com/sgossner/VCSL): Kenyan mbira "Kalimba, Kenya" (B2 F#3 G#3 B3 C#4 D#4 F#4
  A4 B4), Glockenspiel (G5, C6), Hand Chimes (F#4, C5), Concert Harp (B1 E3 G3 B3 D4 F4 A4 C5
  E5 G5 B5).
- VSCO-2-CE (github.com/sgossner/VSCO-2-CE): Cello Section sustain (B1 F2 E3) and tremolo
  (B2 G3), Violin Section pizzicato (F#3 A3 E4 B4 D5) and sustain (B4 D5), Flute (A4 C5 E5).

`samp()` repitches the nearest sample; `bowed()` chains crossfaded retriggers past the bow
attack for notes longer than a sample. Kit synthesis is used only for weather and contact:
`wind`, `air`, `breath`, `paperSfx` (renamed from the kit's `paper`, which the engine uses),
`contact`, `drop`.

Key B pentatonic. One motif: B–F#–G#, completed to B only when the line is held (41.4).
- Hill: mbira ostinato (96 bpm eighths), glockenspiel asks the motif, cello B1 pedal.
- Knot: cello tremolo B2, then G3 after the first ply, violin B4 swelling to the snap; each ply
  is a paper tear + pizzicato + card contact; the snap is tear + wood + pizz + damped harp B1,
  then wind alone (the valley at 19.1 s is this hush, deliberate).
- Loose: each keyframed spin is a falling pizzicato run; the vane is a hand chime F#4 (26.4)
  and an unfinished motif on mbira; the slip is a chime C5 (a semitone off) and a long fall.
  The valley at 25.35 s is the hold before the chime.
- Catch: water touch is a synth drop + glockenspiel; forestay contact wood + damped harp; the
  taut line is harp B1 + pizz, a 14-note harp glissando, the completed motif on mbira, violin
  swell and cello pedal; the ostinato returns. The valley at 40.5 s is the breath before contact.
- Out: flute states the motif over harp rolls; one bass change (B→E at 55.6, back at 60.2);
  the lamp answers the vane with the same chime F#4; mbira motif and a harp chord as the tail.

Room: the kit's synthesised reverb is hot (convolution gain ≈ 77× at the kit's IR norm), and
at wet .3 it took stereo correlation to 0.02. The samples carry their own rooms, so wet is .035
and sample sends are scaled by .4; correlation is now 0.72.

Measured (firefox, `audio.mjs --twice --marks 13,15.4,17.8,26.4,28.2,36.9,41.4,63.2`):
I −16.0 LUFS, LRA 7.7 LU, TP −1.39 dBTP, clipped 0, byte-identical across two cold renders.
Mark onsets 5–115 ms after their marks (15.4 is the loosest at 115 ms). Bands: lowmid 58%,
mid 22%, high 0.55%, air 0.08%: dark, as the 32 kHz samples and the palette are.

## Verification

- `verify.mjs`: seek pure in t in Chromium and Firefox at 20 times across the film, including
  both sides of every cut.
- Strips inspected: snag 26.2–26.9 at 1/15 s, catch 40.4–41.9 at 0.1 s.
- v2 strips at 1/30 s (Firefox): tail 20.8–22.2 and 28.8–31.2, snag 26.2–28.6, catch
  36.4–37.6 and 40.2–42.6. They are continuous with no frame pops. The silent range
  render `out/held-catch-range.mp4` (33–45) has not been watched at speed by this session.
- v2 audio (Firefox, same marks): byte-identical across two cold renders, I −16.0 LUFS,
  LRA 7.7, TP −1.39 dBTP, and mark onsets the same as v1. Only the drop's pan changed,
  following `C_RING`.
- `out/held-v1.mp4` is the previous delivery, kept for comparison.
- v2 final `out/held.mp4` (Firefox, 190 s render): decoded 2100 frames, 70.00 s, 1080×1080
  h264 30 fps, AAC 48 kHz stereo; muxed I −16.0 LUFS, LRA 7.7 LU, peak −1.4 dBFS. The encoded
  frame at 41.4 was inspected: the line is taut from the masthead.
- v1 MP4 (Firefox, 185 s render): same format and loudness. Encoded snap 17.6–17.9 inspected
  frame by frame: the far end whips out, the stub drops. Not re-inspected in v2.

## Remaining weaknesses

- Subject references were drawn from knowledge, not inspected images.
- Houses are a naive side elevation; the traverse's town reads as illustration more than place.
- The sheet cannot establish playback pacing; the knot shot (7.4 s) and the ending hold
  (60–70) are the likeliest to feel long.
- Nothing has been heard: the score is measured, not listened to, by this session.
- `index.html` is 4.6 MB because of the embedded samples.

## User constraints

Free range, ~70 s. Score must use found free instrument samples (done: CC0 VCSL/VSCO-2-CE).
