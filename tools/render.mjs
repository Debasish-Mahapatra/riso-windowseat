/**
 * Render a film to MP4 by seeking every frame -- no realtime capture, so no
 * dropped or duplicated frames and the output is bit-identical between runs.
 *
 *   node render.mjs <film.html> --fps 30 --size 1080 --out ../out/film.mp4
 *   node render.mjs <film.html> --no-audio
 *
 * Audio is optional: if the film exposes window.__riso.renderAudio() returning
 * a base64 WAV (built offline with OfflineAudioContext), it is muxed in.
 */
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { launch, openFilm, args } from './lib/browser.mjs';
import { pipeFrames, run, FFMPEG } from './lib/ffmpeg.mjs';
import { parseWav } from './lib/audio.mjs';

const a = args(process.argv.slice(2));
const film = a._[0];
if (!film) { console.error('usage: node render.mjs <film.html> [--fps 30] [--size 1080] [--out x.mp4]'); process.exit(1); }

const fps = Number(a.fps || 30);
const size = Number(a.size || 1080);
const engine = a.engine || 'chromium';
const filmName = path.basename(path.dirname(path.resolve(film)));
const out = path.resolve(a.out || path.join('..', 'out', `${filmName}.mp4`));
fs.mkdirSync(path.dirname(out), { recursive: true });

const browser = await launch(engine);
const { page, duration, errors } = await openFilm(browser, film, { size, css: Number(a.css || 720) });
const from = Number(a.from || 0);
const to = Math.min(Number(a.to || duration), duration);
const total = Math.round((to - from) * fps);
console.log(`${filmName}: ${from}-${to}s @ ${fps}fps = ${total} frames, ${size}x${size} (${engine})`);

let wav = null;
if (!a['no-audio'] && from === 0 && to === duration) {
  wav = await page.evaluate(async () => {
    if (!window.__riso.renderAudio) return null;
    return window.__riso.renderAudio();
  }).catch(e => { console.error(`  audio render failed: ${e.message}`); return null; });
  if (wav) {
    const p = path.join(path.dirname(out), `${filmName}.wav`);
    const bytes = Buffer.from(wav, 'base64');
    fs.writeFileSync(p, bytes);
    wav = p;
    console.log(`  audio -> ${p}`);
    // -shortest below cuts a longer score and leaves a shorter one silent at the end.
    const parsed = parseWav(bytes), delta = parsed.duration - duration;
    if (Math.abs(delta) > 1 / fps) console.error(`  !! audio is ${delta > 0 ? 'longer' : 'shorter'} than the film by ${Math.abs(delta).toFixed(3)}s`);
    if (parsed.rate !== 48000) console.error(`  !! audio is ${parsed.rate} Hz; the AAC mux resamples anything but 48000`);
  } else {
    console.log('  no window.__riso.renderAudio(); rendering silent');
  }
}

const video = wav ? out.replace(/\.mp4$/, '.silent.mp4') : out;
const ff = pipeFrames([
  '-f', 'image2pipe', '-framerate', String(fps), '-i', 'pipe:0',
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'slow',
  '-movflags', '+faststart', '-y', video,
]);

const t0 = Date.now();
for (let f = 0; f < total; f++) {
  const t = from + f / fps;
  await page.evaluate(time => window.__riso.seek(time), t);
  await ff.write(await page.screenshot({ type: 'png' }));
  if (f % 60 === 0 || f === total - 1) {
    const pct = ((f + 1) / total * 100).toFixed(0);
    const eta = ((Date.now() - t0) / (f + 1) * (total - f - 1) / 1000).toFixed(0);
    process.stdout.write(`  frame ${f + 1}/${total} (${pct}%) eta ${eta}s\n`);
  }
}
await ff.end();

if (wav) {
  await run(['-i', video, '-i', wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
    '-shortest', '-movflags', '+faststart', '-y', out]);
  fs.unlinkSync(video);
  // AAC can raise the true peak, so read the muxed file, not the WAV.
  const r = spawnSync(FFMPEG, ['-hide_banner', '-nostats', '-i', out, '-af', 'ebur128=peak=true', '-f', 'null', '-'], { encoding: 'utf8' });
  const summary = (r.stderr || '').split(/\r?\n/).filter(l => !l.includes('TARGET') && /^\s+(I|LRA|Peak):/.test(l)).map(l => l.trim().replace(/\s+/g, ' ')).join('  ');
  if (summary) console.log(`  muxed audio: ${summary}`);
}

if (errors.length) console.error(`\n!! ${errors.length} page error(s):\n - ${errors.slice(0, 10).join('\n - ')}`);
console.log(`done in ${((Date.now() - t0) / 1000).toFixed(0)}s -> ${out}`);
await browser.close();
