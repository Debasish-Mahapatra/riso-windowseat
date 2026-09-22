// Visual review aid, not an aesthetic score. Reads optional shot metadata from the film.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {args,launch,openFilm} from './lib/browser.mjs';
const a=args(process.argv.slice(2)),film=a._[0];
if(!film){console.error('usage: node review.mjs <film.html> [--out directory] [--engine firefox]');process.exit(1);}
const out=path.resolve(a.out||`../out/${path.basename(path.dirname(path.resolve(film)))}-review`);
const browser=await launch(a.engine||'firefox');
let duration,shots,notes=[],times;
try {
  const opened=await openFilm(browser,film);duration=opened.duration;
  shots=await opened.page.evaluate(()=>window.__riso.shots||[]);
  if(opened.errors.length)throw Error(opened.errors.join('\n'));
  if(!(duration>0&&Number.isFinite(duration)))throw Error('Invalid duration');
  if(!shots.length){notes.push('No shot metadata: evenly spaced samples cannot establish pacing or action quality.');times=Array.from({length:12},(_,i)=>i*Math.max(0,duration-1/30)/11);}
  else {
    times=[];
    for(let i=0;i<shots.length;i++) {
      const s=shots[i];
      if(!s.id||![s.start,s.end].every(Number.isFinite)||s.start<0||s.end>duration||s.end<=s.start)
        throw Error(`Invalid shot ${i}: id, start and end required within the film duration`);
      const readAt=s.readAt??(s.start+s.end)/2;
      if(!Number.isFinite(readAt)||readAt<s.start||readAt>=s.end)throw Error(`Invalid readAt: ${s.id}`);
      times.push(s.start,readAt,Math.max(s.start,s.end-1/30));
      s.seconds=Number((s.end-s.start).toFixed(3));
      if(!s.action)notes.push(`${s.id}: name what changes within the shot, or why it holds.`);
      if(i>=2&&shots[i-2].start>0&&s.transition&&!['cut','none'].includes(s.transition)
        &&s.transition===shots[i-1].transition&&s.transition===shots[i-2].transition)
        notes.push(`${s.id}: third consecutive '${s.transition}' handoff; inspect whether repetition is intentional.`);
    }
  }
} finally {await browser.close();}
times=[...new Set(times.map(t=>Number(t.toFixed(3))))].sort((x,y)=>x-y);
fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,'review.json'),JSON.stringify({duration,shots,notes,times,judgment:'Human/model visual review required; metadata and deterministic pixels do not certify art.'},null,2));
if(shots.length)console.table(shots.map(({id,seconds,action,transition})=>({id,seconds,action,transition})));
notes.forEach(n=>console.log(`Review: ${n}`));
const shoot=fileURLToPath(new URL('./shoot.mjs',import.meta.url));
const r=spawnSync(process.execPath,[shoot,path.resolve(film),'--times',times.join(','),'--engine',a.engine||'firefox','--out',out,'--sheet','--cols','3','--cell','340'],{stdio:'inherit'});
if(r.error)throw r.error;
process.exit(r.status??1);
