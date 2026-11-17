#!/usr/bin/env python3
"""Bake Fast Recruit art-board edits into the app (same art board as Fast Pitch).

usage: python3 src/bake.py <repo_dir> <docs_dir> <artifact_out_html>
  docs_dir: JSON files of the artifact's `layout` collection (one per document,
            as saved by ArtifactData list with out_dir). Each is either the
            document body or {"id":..,"data":{..},"version":..}.
Merges every edit into the <script id="lyBakedData"> block of src/index.src.html
(the page applies that block on every load, GitHub and claude.ai alike), runs
src/rebuild_index.py (writes index.html, bumps sw.js so installed phones update),
and copies the page to <artifact_out_html> for publishing to the artifact.
Prints the ids it baked, one per line, prefixed with "BAKED ".
"""
import json, os, re, sys, glob, subprocess, shutil

repo, docs_dir, out = sys.argv[1], sys.argv[2], sys.argv[3]
idx = os.path.join(repo, 'src', 'index.src.html')
html = open(idx, encoding='utf-8').read()
m = re.search(r'(<script id="lyBakedData" type="application/json">)(.*?)(</script>)', html, re.S)
if not m: sys.exit('lyBakedData block not found in src/index.src.html')
baked = json.loads(m.group(2).replace('<\\/', '</') or '{}')

NEUTRAL = ('sel', 'at', 'orig', 'horig', 'im', 'zp', 'lk')

def effective(d):
    for k, v in d.items():
        if k in NEUTRAL: continue
        if k in ('dx', 'dy', 'r'):
            if (v or 0) != 0: return True
        elif k == 's':
            if (v or 1) != 1: return True
        elif k == 'op':
            if v not in (None, '', 100): return True
        elif k in ('txt', 'html'):
            if isinstance(v, str): return True
        elif v not in (None, '', False, 0) or (k in ('rad', 'bw') and v == 0):
            return True
    return False

n = 0
for f in sorted(glob.glob(os.path.join(docs_dir, '**', '*.json'), recursive=True)):
    o = json.load(open(f, encoding='utf-8'))
    d = o.get('data') if isinstance(o.get('data'), dict) else o
    i = o.get('id') if isinstance(o.get('data'), dict) else None
    i = i or os.path.splitext(os.path.basename(f))[0]
    if not isinstance(d, dict) or not d.get('sel'): continue
    d = {k: v for k, v in d.items() if k not in ('at',)}
    if effective(d): baked[i] = d
    else: baked.pop(i, None)
    print('BAKED', i); n += 1

blob = json.dumps(baked, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
html = html[:m.start(2)] + blob + html[m.end(2):]
open(idx, 'w', encoding='utf-8').write(html)

os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
shutil.copy(idx, out)
subprocess.run([sys.executable, 'src/rebuild_index.py'], cwd=repo, check=True)
print('total baked', n, 'entries now', len(baked))
