// Tail/line jitter for films/held: the largest frame-to-frame displacement of any
// chain point relative to the mean of its neighbours' displacements, at 1/30 s
// across 18.4-48 (cut frames skipped). Reads window.__riso.chains(t).
// usage (from tools/): node ../films/held/jitter.mjs ../films/held/index.html [engine]
import { launch, openFilm } from '../../tools/lib/browser.mjs';
const [film, engine = 'firefox'] = process.argv.slice(2).filter(a => !a.startsWith('--'));
const browser = await launch(engine);
const { page } = await openFilm(browser, film);
const res = await page.evaluate(() => {
  const chains = window.__riso.chains;
  const h = 1 / 30, cuts = [L_END];
  const worst = { tail: { e: 0 }, line: { e: 0 } }, per = {};
  for (let f = Math.round(18.4 * 30); f < 48 * 30; f++) {
    const t0 = f * h, t1 = (f + 1) * h;
    if (cuts.some(c => t0 < c && t1 >= c)) continue;
    const A = chains(t0), B = chains(t1);
    for (const key of ['tail', 'line']) {
      const a = A[key], b = B[key]; if (!a || !b || a.length !== b.length) continue;
      const d = a.map((p, i) => [b[i][0] - p[0], b[i][1] - p[1]]);
      let e = 0, at = 0;
      for (let i = 1; i < d.length - 1; i++) {
        const v = Math.hypot(d[i][0] - (d[i - 1][0] + d[i + 1][0]) / 2, d[i][1] - (d[i - 1][1] + d[i + 1][1]) / 2);
        if (v > e) { e = v; at = i; }
      }
      const shot = t0 < L_END ? 'loose' : 'catch', k = shot + '.' + key;
      (per[k] ||= []).push([e, t0, at]);
      if (e > worst[key].e) worst[key] = { e, t: t0, i: at, n: a.length };
    }
  }
  const summary = {};
  for (const k in per) {
    const es = per[k].map(x => x[0]).sort((x, y) => x - y);
    const top = per[k].slice().sort((x, y) => y[0] - x[0]).slice(0, 6).map(x => `${x[0].toFixed(1)}@${x[1].toFixed(3)}[${x[2]}]`);
    summary[k] = { max: es.at(-1).toFixed(1), p95: es[Math.floor(es.length * .95)].toFixed(1), median: es[es.length >> 1].toFixed(2), top };
  }
  return { worst, summary };
});
console.log(JSON.stringify(res, null, 1));
await browser.close();
