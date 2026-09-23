# tools

Inspection, verification and export harness. Every tool drives a work through `window.__riso`
and seeks exact frames, so a still is the frame the renderer produces at `t`, not a realtime
sample that may have drifted.

## Setup

```
npm install        # playwright-core, ffmpeg-static
npm run setup      # downloads the Chromium and Firefox builds this playwright-core expects
npm test           # visual-kit, workflow and scene-space self-tests
```

Set `FFMPEG=<path>` to use your own ffmpeg; it needs libx264. Playwright's bundled ffmpeg is
webm-only and cannot write MP4.

## The contract

`tools/fixture/index.html` is a minimal working implementation.

```js
window.__riso = {
  duration,          // seconds
  ready,             // false until pre-rendering finishes, then true
  seek(t),           // render exactly the frame at t, synchronously
  renderAudio(),     // optional: Promise<base64 WAV>, 48 kHz stereo, exactly `duration` long
  marks,             // optional: visible event times for audio.mjs to check sync against
  shots,             // optional: [{id,start,end,readAt,action,transition}] for review.mjs
};
```

`seek(t)` must be pure in `t`: the same `t` twice gives identical pixels, and a cold jump to `t`
matches arriving there by playback. That is what makes a film inspectable and the MP4 exact.

## Tools

| Command | Does | Success signal |
|---|---|---|
| `new-riso.mjs --kind film\|still --out <path>` | Blank paper with print, craft and motion kits, player and contract; no inherited art. The player buffers to a frame cache when a frame draws slower than 1/30 s. | Refuses to overwrite existing files. |
| `verify.mjs <html> [--times a,b]` | Repeated seeks and cold jumps give identical pixels in both engines, across the real duration and shot boundaries. | Exit 0. Time-seeded noise can still pass; inspect adjacent frames. |
| `review.mjs <html>` | Shot sheet and JSON timing report from `__riso.shots`, else twelve samples. | Repeated-transition notes call for judgement, not errors. |
| `shoot.mjs <html> --times\|--range\|--around t --window w [--sheet]` | Numbered stills and a labelled contact sheet. | Read the sheet around every transition. |
| `still.mjs <html> --at t --out x.png` | Native canvas PNG, checked for repeatability. | Prints native dimensions. `--size` on screenshot tools scales capture, not art. |
| `render.mjs <html> [--from a --to b] --fps 30 --size 1080 --engine firefox` | Seeks every frame into ffmpeg (no dropped or duplicated frames); muxes `renderAudio()` on full renders. | Prints muxed loudness and true peak. |
| `audio.mjs <html> [--twice] [--marks a,b] [--around t --window w] [--ffmpeg]` | Renders the score alone in seconds: WAV, JSON report and sheet (waveform, log spectrogram, BS.1770 loudness, per-mark sync). | No `FAIL` lines; `--twice` proves determinism. |

Add `--engine firefox` to check the primary browser. Outputs land in `out/` at the repo root.
Run `npm test` after changing anything in `tools/lib/`. No tool certifies artistic quality.
