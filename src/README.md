# Fast Recruit source (runtime)

- `index.src.html` is the editable app page (the same file published to the Claude artifact).
- After editing it, run `python3 src/rebuild_index.py` from the repo root. That writes the live `index.html` and bumps `sw.js` so installed phones update.
- Page content (boards_*.json) is built from design files that are not in this repo; crash fixes should stay in `index.src.html`.
- `crash-log.md` lists every crash report that has been handled, so none is worked twice.
