"""Rebuild the live app page from src/index.src.html (the editable copy) and bump the offline helper so phones pick it up.
Run from the repo root:  python3 src/rebuild_index.py"""
import re, hashlib, os
t = open('src/index.src.html', encoding='utf-8').read()
pat = re.compile(r'(?<![\w/.-])(a|img|vid|boards)/([\w.-]+\.(?:webp|png|jpg|jpeg|otf|mp4|json|bin|svg|gif))')
t = pat.sub(lambda m: m.group(1) + '_' + m.group(2), t).replace("'boards/' + fn", "'boards_' + fn").replace("el.src = 'vid/' + INAPP", "el.src = 'vid_' + INAPP").replace("DIR = 'social/'", "DIR = 'social_'")
t = t.replace('<link rel="apple-touch-icon" href="apple-touch-icon.png">', '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n<link rel="manifest" href="manifest.webmanifest">', 1)
t = t.replace('</body>', "<script>if ('serviceWorker' in navigator) addEventListener('load', () => { const had = !!navigator.serviceWorker.controller; let done = false; navigator.serviceWorker.register('sw.js', { updateViaCache: 'none' }).then(r => { r.update(); document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') r.update(); }); }); navigator.serviceWorker.addEventListener('controllerchange', () => { if (had && !done) { done = true; location.reload(); } }); });</script>\n</body>", 1)
open('index.html', 'w', encoding='utf-8').write(t)
sw = open('sw.js').read(); h = hashlib.sha1(t.encode()).hexdigest()[:12]
sw = re.sub(r"const V = 'fast-recruit-[^']*'", "const V = 'fast-recruit-%s'" % h, sw, count=1); open('sw.js', 'w').write(sw)
print('index.html rebuilt, offline helper version', h)
