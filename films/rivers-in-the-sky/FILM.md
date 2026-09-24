# Rivers in the Sky

A 70-second watercolour film. One drop of water crosses South America several times without
reaching the sea, because the forest keeps breathing it back up as rain. Then the forest is cut:
the drop runs off to the sea, and the farm it used to water goes dry. Years later the girl from
that farm helps replant the forest, and the rain comes back.

- Source: `index.html` (single self-contained file: no `<script src>`, fonts, images or network)
- Render: `node render.mjs ../films/rivers-in-the-sky/index.html --fps 24 --size 1080 --engine firefox` from `tools/` makes the MP4 with its score (1920×1080, 24 fps, 70.0 s, 1680 frames). Renders and review sheets land in the git-ignored `out/`.
- Score: the `/* ── score ── */` section, one closure that reads `CUES`; see **Score** below

## Shots

`SHOTS` and `CUES` in the source are the one authoritative timeline; `window.__riso.shots` and
`window.__riso.marks` are derived from them.

| # | id | time (s) | action | handoff |
|---|---|---|---|---|
| 1 | sea | 0–6 | Atlantic at sunrise, sun low in the east (right); the drop glints on a crest, lifts as vapour; the camera tilts up with it; the title is brushed in stroke by stroke | one continuous pan, through haze |
| 2 | trades | 6–10 | 3 km over the Brazilian coast (beach, restinga, mangroves, a silty estuary) travelling west; trade-wind wisps; cumulus build over the land, not the sea | dissolve through white cloud (paper) |
| 3 | rain | 10–14 | under a cumulus base over the forest; it darkens, rain veils; the drop falls onto a big drip-tip leaf, splashes, runs down the midrib, swells at the tip, drips | match on the drop into the soil |
| 4 | roots | 14–18.5 | soil cutaway: the drop soaks in, a root drinks it, it shoots up a cut-open channel in the trunk, out along a branch to the leaves | dissolve, following it up |
| 5 | leaf | 18.5–22 | a leaf's backlit underside, reticulate veins, stomata as little mouths; one opens and breathes the drop out as vapour | vapour rises out of frame, cut |
| 6 | flying | 22–29 | the pitch frame's world alive: clouds build, the flying river flows; the sparkle joins it, two hops (a shower each), westward; the camera pans west | the pan continues |
| 7 | andes | 29–33 | the snowy range: the flow meets the wall, clouds bank against the slopes, it turns south (left); the camera follows along the range | cut as clouds arrive |
| 8 | farm | 33–38 | a farm far to the south: maize, whitewashed house, a girl (8) on the porch; clouds arrive, rain, the drop lands on a maize leaf; she runs out laughing, arms wide, face up | hard cut |
| 9 | burn | 38–44.5 | the same aerial, deforested: a road with fishbone side roads, pasture with white cattle, red clearings, burn scars, smoke drifting west, a big tree falls; the drop falls from a thin cloud onto bare red earth and runs off in a rivulet | dissolve along the rivulet |
| 10 | runoff | 44.5–48 | a muddy river carries the drop to the Atlantic; a brown plume spreads along the coast; the flying river overhead is a few weak streaks | cut to the empty sky |
| 11 | dry | 48–52.5 | the same farm a year later: empty sky, wilted maize, cracked soil, a dust devil; the girl (9) looks up and lets a handful of dust fall | a wet wash bleeds across (years pass) |
| 12 | plant | 52.5–60 | years later, cleared land: people planting saplings; the woman (25, same yellow) plants one and pats the soil; time-lapse to a young forest; macaws return | dissolve, pushing into a leaf |
| 13 | breath | 60–64 | a leaf breathes the drop out again; clouds build over the regrown forest; the flying river flows full | through white cloud |
| 14 | home | 64–70 | the farm: rain arrives, the drop falls on her upturned face; the woman stands in the field in the rain, face up, smiling (a mirror of shot 8); the last line is brushed in; fade to paper | fade to paper |

## CUES (seconds)

```
glint 2.0      lift 2.6       title 3.8      titleDone 5.6
coast 7.0      cloudForm 8.5
rainStart 11.0 splash 12.8    drip 13.5
soak 14.4      drink 15.2     rise 15.5      riseEnd 17.5   leafArrive 18.0
stomaOpen 19.5 exhale 19.8
join 23.0      hop1 24.2      hop2 26.0
wall 30.0      turnSouth 30.6
farmRain 35.0  girlRuns 35.5
smoke 38.5     treeFall 40.0  bareSplash 42.5 runoffStart 43.2
sea2 47.0
dryLook 49.5   dustDrop 51.0
plantOne 54.0  growStart 56.0 growEnd 59.0   macaws 59.2
exhale2 61.0   riverFlows 63.0
homeRain 65.0  endText 66.0   endTextDone 68.5 fade 69.0
marks = [2.6, 12.8, 19.8, 30.6, 35.0, 40.0, 42.5, 54.0, 61.0, 65.0]
```

## How it is painted

- **Every surface is a Tyler-Hobbs wash.** A base polygon is deformed recursively (gaussian
  midpoint displacement, with a spatially coherent variance per vertex, so some edges bleed and
  others stay crisp), then 8–60 further deformations are stacked at low alpha. The stack becomes
  pigment density.
- **The density is treated like paint.** It gets a wet blur (wet-in-wet), a crisp cut
  (wet-on-dry), and edge darkening (density minus its blur, so pigment collects at the drying
  edge). It also gets granulation against a cold-press paper heightmap (pigment settles in the
  valleys; strongest for ultramarine, sienna, umber and cerulean) and dry brush (only the peaks
  take paint: glitter, grass, dust).
- **Glazes mix subtractively.** Each wash is converted to a Beer–Lambert glaze (transmittance
  exp(−K·d) from a real pigment palette) and multiplied onto the paper.
- **Whites are reserved or lifted.** The sky is painted around clouds, snow and vapour. Mist,
  glints, sunlit flecks, the sap channel and the water's lights are lifted back toward paper.
- **The paper is periodic.** Heightmap and texture fields are 2048/1024/512 px tiles, so any size
  of painting has cold-press tooth without seams.
- **Baking and compositing.** All static paintings are baked once at load (58.8 s in Firefox).
  Each frame then composites baked plates through a camera rectangle, plus moving painted
  elements: swell bands, growing cloud sprites, flow streaks, rain and glints, figures, smoke,
  fire, the plume, saplings, the drop and the text.
- **Timing.** Painted elements change drawing on twos (a new drawing every 1/12 s); moving
  washes alternate between two seeded "boil" drawings. The camera moves on ones.
- **Cameras.** Cameras are monotone Hermite tracks (no overshoot). A `{m:1}` key carries velocity
  across a cut or dissolve, so the sea→trades pan and the flying→andes pan continue unbroken.
- **The forest is loose, as the brief asked.** The canopy is an underwash, long wet-in-wet
  strokes in four greens, tree-line bands with bumpy tops glazed one over another for the middle
  distance, and cloud shadows. Only the nearest crowns are individual trees. They are painted
  near → far, each around the crowns in front of it, with a light body, a wet-dropped shade to
  the lower left, crevices, and lifted sunlit flecks.

### People

- **A small 3D rig.** Each figure is built by forward kinematics in body space, so elbows only
  flex forward and knees only backward. It is projected with a yaw and painted as back-to-front
  washes: far limbs, trousers, dress or shirt, near limbs, neck, near sleeve, head, hair, ribbon.
  Each layer is masked by the layers in front of it. Faces (eyes, brows, a nose, cheeks, a mouth
  that opens to laugh) are painted only when turned toward us.
- **Consistent designs.**
  - The girl: dark curly hair with a yellow ribbon, a yellow dress, brown skin, bare feet.
  - The woman: the same person, in a yellow shirt with her curls in a bun (the ribbon at the bun).
  - Five planters: varied shirts and hats.
- **Scale.** The farm uses a camera 2 m up at 150 px/m on the house front: the door is 2.05 m,
  the maize 2.1–2.5 m, the girl 1.25 m (1.31 m at 9), the woman 1.65 m. The planting shot is on
  its own ground plane at the same scale.

## Science, as painted

- **Atlantic moisture and the trade winds.** Sunrise over the Atlantic; the drop evaporates and
  rides the trade-wind stream west. Cumulus build over the land, not the sea (the land heats in
  the morning).
- **Recycling through transpiration.**
  - Rain, interception on a drip-tip leaf, infiltration, root uptake, xylem ascent, then
    transpiration through a stoma. The drop leaves as vapour: evaporation inside the leaf, out
    through the pore.
  - Over the forest the drop hops twice: rain and re-evaporation, recycled further west each time.
- **The flying river.** The low-level flow sits at roughly 1–2 km. At the Andes it banks clouds
  against the slopes (orographic lift) and turns south along the range, as the South American
  low-level jet does toward the La Plata basin. The farm is there, far to the south.
- **Deforestation and fire.**
  - A fishbone road pattern (Rondônia-style), pasture, fresh clearings and burn scars.
  - Smoke drifts west with the trade wind.
  - The flying river above is drawn thin (weaker evapotranspiration upstream).
  - On bare, crusted ground the drop runs off instead of soaking in, and the river carries silt
    to the sea as a brown plume.
- **Drought and regrowth.** The next year the farm is dry. Replanting restores the forest over
  years; clouds and the flying river return in shot 13.

## Transitions

- sea→trades: one continuous pan with a light haze.
- trades→rain and breath→home: through white paper.
- roots→leaf, burn→runoff, plant→breath: short dissolves on the moving subject.
- flying→andes and andes→farm: the pan carries across; a cut as clouds arrive.
- farm→burn: hard cut.
- dry→plant: a blotted wet wash bleeds across in lobes (13 soft masks baked at load, scaled up;
  no canvas filter in the render path).
- End: fade to paper from 69.0 s.

## Evidence

- **Bake and frame timings (Firefox).** Bake 58.8 s (paper 0.6, sea 2.0, trades 4.2, rain 2.7,
  roots 4.6, leaf 0.8, flying 5.9, andes 4.8, farm 9.3, burn 5.9, runoff 1.3, dry 8.5, plant 7.1,
  home 1.1). Per frame, over 280 samples: average 8.2 ms, max 35 ms (the planting time-lapse).
  Chromium bakes more slowly (≈ 119 s before the figure optimisation).
- **`verify.mjs` passes in both engines.** It printed "seek is pure in t; contract holds",
  across 46 inspection times including every shot boundary. Cross-engine pixels differ
  (antialiasing), as expected.
- **Visual review.** The animatic sheet, the final 42-frame review sheet, and per-shot sheets at
  1:1. Also a strip of ±1 and ±3 frames around every transition (13 transitions, 65 frames) and
  a sheet at every cue (49 frames). Figures were checked in a pose test sheet (standing, three run
  phases, arms-out, turned stance) and zoomed in the frame.
- **Decode check.** `out/rivers-silent.mp4` decodes clean with ffmpeg: duration 00:01:10.00,
  1680 frames, 1920×1080, h264 High, yuv420p, 24 fps, 72 MB. Rendered in 286 s with
  `render.mjs --fps 24 --size 1080 --engine firefox --no-audio`. `out/mp4-contact-2fps.png` is
  the whole film at 2 fps from the MP4 itself.

## Honest weak spots

- **Figures are simple.** The rig guarantees natural joints and consistent scale, but the figures
  are flat, cut-paper-like watercolour shapes rather than a painter's figure drawing.
  - Faces are tiny dot-and-line features.
  - The "face up" in shots 8 and 14 reads from the tilted head, closed eyes and smile, not from
    real foreshortening.
  - The run cycle has only a few distinct drawings per stride.
- **The Andes are telephoto and busy.** The range is raymarched terrain painted as washes. It
  reads as a snowy wall, but its shadow shapes are busier than a painter's would be.
- **The flying river is subtle in places.** In shot 7 and in the trades wisps it is a subtle
  violet-and-light band; it reads best in shots 6 and 13.
- **The rain shot's first half** (under the cloud base) is a simple graded ceiling; the leaf half
  is stronger.
- **The runoff shot** reads as a diagram-like patchwork of fields; it is the least painterly
  landscape in the film.
- **The planting time-lapse** grows saplings by swapping four painted stages with scaling. The
  young forest is loose but its crowns overlap flatly.
- **The drop in shot 2** rides a stream of soft streaks; at thumbnail size the stream reads more
  as haze than as wind.
- **Not heard**: nobody has listened to the score yet, and I can't listen. The meters pass, but
  the pan flute, the choir pad and the sound of the burn are unjudged.

## Score

**Every sound is synthesised in the page; there are no recordings.**

- **Instruments.**
  - **The tune: a pan flute.** A breathy sine with a chiff at each note, a scoop into long notes
    and a late vibrato, rendered a phrase at a time.
  - **The drop: marimba and glass.** A marimba (1 : 3.93 : 9.2 partials with a mallet thump) and
    glass. Rising open fifths (D–A–E) sound whenever the drop becomes vapour; the same notes fall
    when it runs off to the sea.
  - **The sky: a choir-like "aah" pad.** Detuned saws through vowel formants at 720, 1180 and
    2650 Hz.
  - **The farm:**
    - a cavaquinho strum (a high, bright Karplus-Strong string);
    - a surdo;
    - a shaker.
  - **Weather and world:**
    - rain, sea, wind and thunder;
    - forest birds and scarlet macaws (FM squawks);
    - fire crackle;
    - distant chainsaws;
    - a falling tree (a groan, then the crash and debris);
    - a river, water drops and falling dust.
- **The theme.** It is in D and rises like vapour (A–D–E–F♯), then settles like rain.
  - Phrase A plays under the title.
  - Phrase B plays over the flying river, and again for the last rain on the farm. Its high A
    lands as the rain arrives (65.0), and it closes on D as the words finish.
- **Shot by shot.**

| Shot | Sound |
|---|---|
| Sea | A glass glint at 2.0; the rising fifths at the lift (2.6) |
| Rain | Rain marimba plinks that thicken until the splash (12.8), which is a drop, a chord and glass |
| Roots | A muffled low pad; a gulp and a slurp as the root drinks (15.2); a marimba arpeggio up the trunk; a chime at the leaf |
| Leaf | A tiny pop at the stoma; a breath and the fifths in glass at the exhale (19.8) |
| Flying | The theme whole over marimba eighths and the choir; a cascade and a small shower on each hop (24.2, 26.0) |
| Andes | The flute climbs to D6 as the river hits the wall (30.0, with a low boom); the harmony turns (Bm–G–A) as it goes south |
| Farm | Wind and thunder, a surdo pickup; then rain and the samba strum on the downbeat (35.0); a flute flourish as she runs (35.5) |
| Burn | Hard cut to no music: a low bowed drone, fire, three distant chainsaws; the tree groans and crashes (40.0); a dull thud on bare earth (42.5), then a trickle |
| Runoff | A muddy river; the fifths falling (E–A–D); the sea again (47.0) |
| Dry | Dry wind; a lonely flute; a high thin tone as she looks up; dust from her hand (51.0) |
| Plant | A marimba sweep for the years passing; a warm D add9 chord for the first sapling (54.0); growth as a crescendo (56.0–59.0) with the theme; macaws and a bright chord (59.2) |
| Breath and home | The fifths in glass at the exhale (61.0); the choir; the theme on the flute; rain, shaker and surdo on the farm; a final D add9 |

- **Measured in Firefox (`audio.mjs --twice`).** I −16.0 LUFS, LRA 9.3 LU, TP −2.9 dBTP, clipped
  0. Two cold renders are byte-identical (`006663b850e18901`).
- **Level shape:**
  - the farm rain and the end are the loudest (about −14);
  - the burn is stark but present (about −23);
  - there is a designed hush on the farm just before the rain (33.9).
