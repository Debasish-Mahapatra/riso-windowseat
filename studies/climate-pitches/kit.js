'use strict';
/* Shared kit for the climate pitch frames. Canvas 2D only: no libraries, fonts,
   images or network. Everything random is seeded, so a frame is identical on
   every render. Never call Math.random() in a render path. */

const TAU = Math.PI * 2;
const clamp = (v, a = 0, b = 1) => v < a ? a : v > b ? b : v;
const lerp = (a, b, u) => a + (b - a) * u;
const smooth = (a, b, v) => { const u = clamp((v - a) / (b - a)); return u * u * (3 - 2 * u); };
const mod = (a, n) => ((a % n) + n) % n;

/* ── deterministic randomness ─────────────────────────────────────────────── */
function mulberry32(a) {
  return function () {
    a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
function hash(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}
/** A seeded generator for a stable key: rngFor('snow:flakes')() → [0, 1). */
const rngFor = (key) => mulberry32(hash(String(key)));
/** Standard normal from a seeded generator. */
function gauss(r) {
  let u = 0, v = 0;
  while (u === 0) u = r();
  v = r();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(TAU * v);
}
const range = (r, a, b) => a + (b - a) * r();

/* ── noise ────────────────────────────────────────────────────────────────── */
/** Seeded 2D Perlin noise, returns roughly -1..1. */
function makeNoise(key) {
  const r = rngFor('noise:' + key), perm = new Uint8Array(512), p = [];
  for (let i = 0; i < 256; i++) p[i] = i;
  for (let i = 255; i > 0; i--) { const j = Math.floor(r() * (i + 1)); const t = p[i]; p[i] = p[j]; p[j] = t; }
  for (let i = 0; i < 512; i++) perm[i] = p[i & 255];
  const GX = [1, -1, 1, -1, 1.4142, -1.4142, 0, 0], GY = [1, 1, -1, -1, 0, 0, 1.4142, -1.4142];
  const fade = t => t * t * t * (t * (t * 6 - 15) + 10);
  return function (x, y) {
    const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
    const X = xi & 255, Y = yi & 255;
    const g = (h, dx, dy) => { const k = h & 7; return GX[k] * dx + GY[k] * dy; };
    const aa = perm[perm[X] + Y], ab = perm[perm[X] + Y + 1], ba = perm[perm[X + 1] + Y], bb = perm[perm[X + 1] + Y + 1];
    const u = fade(xf), v = fade(yf);
    const x1 = lerp(g(aa, xf, yf), g(ba, xf - 1, yf), u);
    const x2 = lerp(g(ab, xf, yf - 1), g(bb, xf - 1, yf - 1), u);
    return lerp(x1, x2, v) * 0.9;
  };
}
/** Fractal sum of a noise function. */
function fbm(n, x, y, oct = 4, lac = 2, gain = 0.5) {
  let s = 0, a = 1, f = 1, norm = 0;
  for (let i = 0; i < oct; i++) { s += a * n(x * f, y * f); norm += a; a *= gain; f *= lac; }
  return s / norm;
}

/* ── canvases and paths ───────────────────────────────────────────────────── */
function cv(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
function ctxOf(c) { return c.getContext('2d', { willReadFrequently: true }); }
/** Trace points into the current path of g. */
function trace(g, pts, closed = true) {
  g.moveTo(pts[0][0], pts[0][1]);
  for (let i = 1; i < pts.length; i++) g.lineTo(pts[i][0], pts[i][1]);
  if (closed) g.closePath();
}
function fillPts(g, pts, style) { g.beginPath(); trace(g, pts, true); if (style) g.fillStyle = style; g.fill(); }
function strokePts(g, pts, style, w, closed = false) {
  g.beginPath(); trace(g, pts, closed);
  if (style) g.strokeStyle = style;
  if (w) g.lineWidth = w;
  g.stroke();
}

/** Catmull-Rom through points; per = samples per segment. */
function curve(pts, closed, per) {
  per = per || 12;
  const n = pts.length, out = [];
  const at = (i) => pts[closed ? (i + n * 2) % n : clamp(i, 0, n - 1)];
  const last = closed ? n : n - 1;
  for (let i = 0; i < last; i++) {
    const p0 = at(i - 1), p1 = at(i), p2 = at(i + 1), p3 = at(i + 2);
    for (let k = 0; k < per; k++) {
      const u = k / per, u2 = u * u, u3 = u2 * u;
      out.push([
        0.5 * (2 * p1[0] + (p2[0] - p0[0]) * u + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * u2
               + (3 * p1[0] - p0[0] - 3 * p2[0] + p3[0]) * u3),
        0.5 * (2 * p1[1] + (p2[1] - p0[1]) * u + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * u2
               + (3 * p1[1] - p0[1] - 3 * p2[1] + p3[1]) * u3),
      ]);
    }
  }
  if (!closed) out.push(pts[n - 1].slice());
  return out;
}
function bezier(p0, p1, p2, p3, n = 24) {
  const out = [];
  for (let i = 0; i <= n; i++) {
    const t = i / n, q = 1 - t;
    out.push([q * q * q * p0[0] + 3 * q * q * t * p1[0] + 3 * q * t * t * p2[0] + t * t * t * p3[0],
      q * q * q * p0[1] + 3 * q * q * t * p1[1] + 3 * q * t * t * p2[1] + t * t * t * p3[1]]);
  }
  return out;
}
/** Points around an ellipse. */
function ellipsePts(x, y, rx, ry, n = 48, rot = 0) {
  const out = [], c = Math.cos(rot), s = Math.sin(rot);
  for (let i = 0; i < n; i++) {
    const th = i / n * TAU, px = Math.cos(th) * rx, py = Math.sin(th) * ry;
    out.push([x + px * c - py * s, y + px * s + py * c]);
  }
  return out;
}
/** Resample a polyline to roughly even spacing. */
function resample(pts, step, closed = false) {
  const src = closed ? [...pts, pts[0]] : pts, out = [src[0].slice()];
  let carry = 0;
  for (let i = 1; i < src.length; i++) {
    const [ax, ay] = src[i - 1], [bx, by] = src[i], d = Math.hypot(bx - ax, by - ay);
    let t = step - carry;
    while (t <= d) { out.push([ax + (bx - ax) * t / d, ay + (by - ay) * t / d]); t += step; }
    carry = d - (t - step);
  }
  if (!closed) out.push(src[src.length - 1].slice());
  return out;
}
/** Displace points with low-frequency noise: a hand-cut, hand-painted edge. */
function wobble(pts, amp, key, freq = 0.02) {
  const n = makeNoise('wob:' + key);
  return pts.map(([x, y]) => [x + amp * n(x * freq, y * freq + 17.3), y + amp * n(x * freq + 31.7, y * freq)]);
}
/** A tapered stroke along a polyline as a closed polygon.
 *  w(s) gives the half-width at arc fraction s in [0, 1]. */
function taper(pts, w) {
  const n = pts.length; if (n < 2) return [];
  const len = [0];
  for (let i = 1; i < n; i++) len[i] = len[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
  const L = len[n - 1] || 1, left = [], right = [];
  for (let i = 0; i < n; i++) {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)];
    let dx = b[0] - a[0], dy = b[1] - a[1]; const d = Math.hypot(dx, dy) || 1; dx /= d; dy /= d;
    const h = w(len[i] / L);
    left.push([pts[i][0] - dy * h, pts[i][1] + dx * h]);
    right.push([pts[i][0] + dy * h, pts[i][1] - dx * h]);
  }
  return left.concat(right.reverse());
}

/* ── colour ───────────────────────────────────────────────────────────────── */
function rgb(hex) { const v = parseInt(hex.slice(1), 16); return [v >> 16 & 255, v >> 8 & 255, v & 255]; }
const css = (c, a = 1) => `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a})`;
const mixc = (a, b, u) => [lerp(a[0], b[0], u), lerp(a[1], b[1], u), lerp(a[2], b[2], u)];

/* ── lettering ────────────────────────────────────────────────────────────────
   No fonts. Every letter is a few strokes on a 6 × 10 grid; a stroke starting
   with 'c' is smoothed, 'o' is a smoothed closed loop. lettering() returns
   polylines so each style can draw them its own way (carved, painted, stitched). */
const GLYPH = {
  A: [6, [[0, 10], [3, 0], [6, 10]], [[1.2, 6.6], [4.8, 6.6]]],
  B: [5.8, [[0, 10], [0, 0], [3.6, 0]], ['c', [3.6, 0], [5.2, .9], [5.4, 2.6], [4.4, 4.4], [3, 5], [0, 5]], ['c', [3, 5], [5.1, 5.7], [5.8, 7.5], [5, 9.3], [3.4, 10], [0, 10]]],
  C: [5.8, ['c', [5.8, 1.8], [4.5, .3], [3, 0], [1.3, .6], [.2, 2.6], [0, 5], [.2, 7.4], [1.3, 9.4], [3, 10], [4.5, 9.7], [5.8, 8.2]]],
  D: [6, [[0, 0], [0, 10], [2.6, 10]], ['c', [2.6, 10], [4.7, 9.3], [5.8, 7.3], [6, 5], [5.8, 2.7], [4.7, .7], [2.6, 0]], [[2.6, 0], [0, 0]]],
  E: [5.2, [[5.2, 0], [0, 0], [0, 10], [5.2, 10]], [[0, 5], [4, 5]]],
  F: [5.2, [[5.2, 0], [0, 0], [0, 10]], [[0, 5], [4, 5]]],
  G: [6, ['c', [5.8, 1.8], [4.5, .3], [3, 0], [1.3, .6], [.2, 2.6], [0, 5], [.2, 7.4], [1.3, 9.4], [3, 10], [4.7, 9.6], [5.9, 8.2], [6, 5.7]], [[6, 5.7], [3.4, 5.7]]],
  H: [6, [[0, 0], [0, 10]], [[6, 0], [6, 10]], [[0, 5], [6, 5]]],
  I: [0, [[0, 0], [0, 10]]],
  J: [4.6, ['c', [4.6, 0], [4.6, 7.2], [4.1, 9.2], [2.5, 10], [.9, 9.5], [0, 8]]],
  K: [5.8, [[0, 0], [0, 10]], [[5.8, 0], [0, 6.4]], [[2.1, 4.3], [5.8, 10]]],
  L: [5, [[0, 0], [0, 10], [5, 10]]],
  M: [7, [[0, 10], [0, 0], [3.5, 6.6], [7, 0], [7, 10]]],
  N: [6, [[0, 10], [0, 0], [6, 10], [6, 0]]],
  O: [6.4, ['o', [3.2, 0], [5.5, 1], [6.4, 5], [5.5, 9], [3.2, 10], [.9, 9], [0, 5], [.9, 1]]],
  P: [5.6, [[0, 10], [0, 0], [3.4, 0]], ['c', [3.4, 0], [5.2, .8], [5.6, 2.6], [5, 4.4], [3.4, 5.3], [0, 5.3]]],
  Q: [6.4, ['o', [3.2, 0], [5.5, 1], [6.4, 5], [5.5, 9], [3.2, 10], [.9, 9], [0, 5], [.9, 1]], [[3.8, 7.2], [6.4, 10.6]]],
  R: [5.8, [[0, 10], [0, 0], [3.4, 0]], ['c', [3.4, 0], [5.2, .8], [5.6, 2.6], [5, 4.4], [3.4, 5.3], [0, 5.3]], [[3, 5.3], [5.8, 10]]],
  S: [5.8, ['c', [5.6, 1.6], [4.3, .2], [2.7, 0], [1, .6], [.3, 2.2], [.9, 3.8], [2.6, 4.7], [4.3, 5.4], [5.7, 6.7], [5.8, 8.4], [4.7, 9.7], [2.9, 10], [1.2, 9.6], [0, 8.2]]],
  T: [6, [[0, 0], [6, 0]], [[3, 0], [3, 10]]],
  U: [6, ['c', [0, 0], [0, 7], [.7, 9.1], [3, 10], [5.3, 9.1], [6, 7], [6, 0]]],
  V: [6, [[0, 0], [3, 10], [6, 0]]],
  W: [8, [[0, 0], [2, 10], [4, 3.4], [6, 10], [8, 0]]],
  X: [6, [[0, 0], [6, 10]], [[6, 0], [0, 10]]],
  Y: [6, [[0, 0], [3, 5.2], [6, 0]], [[3, 5.2], [3, 10]]],
  Z: [5.8, [[0, 0], [5.8, 0], [0, 10], [5.8, 10]]],
  0: [5.8, ['o', [2.9, 0], [5, 1], [5.8, 5], [5, 9], [2.9, 10], [.8, 9], [0, 5], [.8, 1]]],
  1: [3.2, [[0, 2.2], [3.2, 0], [3.2, 10]]],
  2: [5.8, ['c', [.3, 2.3], [1.3, .5], [3, 0], [4.7, .5], [5.6, 2], [5.4, 3.8], [4.2, 5.4], [0, 10]], [[0, 10], [5.8, 10]]],
  3: [5.8, ['c', [.3, 1.1], [2, 0], [4, .1], [5.3, 1.2], [5.4, 2.9], [4.3, 4.3], [2.5, 4.9]], ['c', [2.5, 4.9], [4.7, 5.6], [5.8, 7.4], [5.3, 9.2], [3.5, 10], [1.5, 9.9], [0, 8.8]]],
  4: [6, [[4.4, 10], [4.4, 0], [0, 7.1], [6, 7.1]]],
  5: [5.8, [[5.4, 0], [.9, 0], [.4, 4.6]], ['c', [.4, 4.6], [2.4, 3.9], [4.3, 4.2], [5.6, 5.6], [5.8, 7.4], [5.1, 9.2], [3.4, 10], [1.4, 9.9], [0, 8.8]]],
  6: [5.8, ['c', [5.1, .7], [3.4, 0], [1.7, .6], [.5, 2.4], [0, 5.2], [.3, 8], [1.5, 9.6], [3.1, 10], [4.8, 9.4], [5.8, 7.8], [5.6, 6], [4.4, 4.9], [2.8, 4.7], [1.2, 5.3], [.2, 6.5]]],
  7: [5.8, [[0, 0], [5.8, 0], [2, 10]]],
  8: [5.8, ['o', [2.9, 4.8], [1, 3.9], [.6, 2.2], [1.4, .6], [2.9, 0], [4.4, .6], [5.2, 2.2], [4.8, 3.9], [2.9, 4.8], [.7, 5.8], [0, 7.6], [.8, 9.4], [2.9, 10], [5, 9.4], [5.8, 7.6], [5.1, 5.8]]],
  9: [5.8, ['c', [.7, 9.3], [2.4, 10], [4.1, 9.4], [5.3, 7.6], [5.8, 4.8], [5.5, 2], [4.3, .4], [2.7, 0], [1, .6], [0, 2.2], [.2, 4], [1.4, 5.1], [3, 5.3], [4.6, 4.7], [5.6, 3.5]]],
  '.': [.2, [[0, 9.8], [.2, 9.8]]],
  ',': [1, [[.9, 9.2], [.2, 11.2]]],
  '!': [.2, [[.1, 0], [.1, 6.6]], [[0, 9.8], [.2, 9.8]]],
  '?': [5.4, ['c', [.2, 2], [1.2, .4], [2.9, 0], [4.6, .5], [5.4, 2.1], [5, 3.7], [2.9, 5.3], [2.9, 6.9]], [[2.8, 9.8], [3, 9.8]]],
  '·': [.2, [[0, 5.2], [.2, 5.2]]],
  ':': [.2, [[0, 3.4], [.2, 3.4]], [[0, 9.8], [.2, 9.8]]],
  '-': [3.6, [[0, 5.6], [3.6, 5.6]]],
  '—': [7, [[0, 5.6], [7, 5.6]]],
  "'": [.6, [[.6, 0], [.3, 2.8]]],
  ' ': [3.2],
};
/** Strokes of a string as polylines in px. (x, y) anchors the cap-height
 *  centre; size is the cap height. Returns {strokes, width, lw}. */
function lettering(txt, x, y, size, o = {}) {
  const weight = o.weight ?? 1.4, track = o.track ?? 2.2, u = size / 10;
  const glyphs = [...txt.toUpperCase()].map(ch => GLYPH[ch] || GLYPH[' ']);
  let width = 0;
  glyphs.forEach((gl, i) => { width += gl[0] + (i < glyphs.length - 1 ? track + weight : 0); });
  const align = o.align || 'center', x0 = x - (align === 'center' ? width / 2 : align === 'right' ? width : 0) * u;
  const r = rngFor('letters:' + (o.key || txt)), wob = (o.wob ?? .22) * u;
  const strokes = [];
  let cx = 0;
  for (const gl of glyphs) {
    const [adv, ...sts] = gl;
    for (const st of sts) {
      let pts = st;
      if (st[0] === 'c') pts = curve(st.slice(1), false, 6);
      else if (st[0] === 'o') { pts = curve(st.slice(1), true, 6); pts.push(pts[0]); }
      const jx = (r() - .5) * 2 * wob, jy = (r() - .5) * 2 * wob, sk = (r() - .5) * .05;
      strokes.push(pts.map(([px, py]) => [x0 + (cx + px + (py - 5) * sk) * u + jx, y + (py - 5) * u + jy]));
    }
    cx += adv + track + weight;
  }
  return { strokes, width: width * u, lw: weight * u };
}

/* ── still-frame contract ─────────────────────────────────────────────────────
   Each pitch frame is a one-second "film" that always shows the same picture,
   so the riso-windowseat tools (still.mjs, shoot.mjs) can capture it. */
function stillFrame(W, H, draw) {
  const c = document.getElementById('c');
  c.width = W; c.height = H;
  const g = c.getContext('2d');
  const t0 = performance.now();
  draw(g, W, H);
  window.__riso = { duration: 1, ready: true, seek() {}, drawMs: Math.round(performance.now() - t0) };
}
