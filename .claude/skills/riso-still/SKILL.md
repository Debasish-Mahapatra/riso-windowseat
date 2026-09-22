---
name: riso-still
description: Create or improve procedural risograph still art, illustrations, posters and images in this repo. Develops reference-led composition, perspective, pose and ink plates; delivers a native-resolution PNG and self-contained Canvas 2D source. Use for standalone still requests; use riso-film for moving work.
---

# Riso still

Deliver `prints/<name>/index.html` and a native PNG in `out/`. Same medium as the films: Canvas
2D only, no libraries, fonts, images or network calls. External references are observation
sources, never embedded assets. If the user explicitly wants generated raster imagery, that is a
different workflow; do not quietly substitute it. Commands run in `tools/`.

## Develop the picture

Read `.claude/rules/riso-plates.md`, `docs/visual-development.md` and `docs/drawing.md`; add
`docs/scene-space.md` when perspective or attached details matter. Skip film timelines,
transitions and sound. `prints/workings/index.html` is a finished print series to learn from.

Extract subject, feeling, format and exclusions. If the user wants ideas, offer different scenes
or viewpoints; if they want art, choose and draw. Default to 1080 square only when no format was
given; record other sizes before composing.

- For an unfamiliar subject, look at real references and note proportions, gesture, construction
  and material. A mood adjective or an unopened image link is not enough.
- For ambitious work, compare small compositions with different viewpoints and value groupings,
  then develop the strongest. A local edit needs less setup.
- Solve support, perspective, occlusion and identity before detail. Draw figure landmarks and
  contact points before clothing or texture: the hand reaches the tool, the tool meets the work.
  Build details on shared surfaces so ellipses, slats and legs agree on orientation and scale.
- Marks should explain form, material or the moment. Concentrate detail at the focus and leave
  quiet areas. Random hatching and misregistration do not rescue weak drawing.

## Build and inspect

```
node new-riso.mjs --kind still --out ../prints/<name>/index.html
node verify.mjs ../prints/<name>/index.html --times 0
node still.mjs ../prints/<name>/index.html --at 0 --out ../out/<name>.png
```

The starter is blank paper with the print and craft kits and no animation loop. Draw in its art
block. A single picture uses `duration: 1` and a `seek(t)` that draws the same picture; a series
may use integer print indices as `prints/workings` does. No MP4, score or artificial motion.

For another native size, change canvas, paper, plate dimensions, projection and screen pitch
before baking, and audit square assumptions like `W,W`. Larger prints must rerasterize geometry
and screens at that size; CSS/DPR enlargement and PNG upscaling do not make a higher-resolution
original. Press-ready separations need a separate print-production brief.

Inspect the whole picture at viewing size, a value/silhouette view, and 1:1 crops of difficult
anatomy, attachments and screen. Fix perspective, tangencies, missing support or an unclear
subject before polishing grain; `docs/quality-bar.md` lists the review cases. `still.mjs` exports
the canvas backing store and checks repeatability; it does not judge the art. Confirm dimensions
and open the PNG.

Keep a short `PRINT.md` beside substantial work: request, references, viewpoint, geometry and
light decisions, native size, inspected output and remaining weaknesses. Keep the previous
version when revising.
