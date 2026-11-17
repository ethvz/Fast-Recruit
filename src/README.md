# Fast Recruit source (runtime)

- `index.src.html` is the editable app page (the same file published to the Claude artifact).
- After editing it, run `python3 src/rebuild_index.py` from the repo root. That writes the live `index.html` and bumps `sw.js` so installed phones update.
- Page content (boards_*.json) is built from design files that are not in this repo; crash fixes should stay in `index.src.html`.
- `crash-log.md` lists every crash report that has been handled, so none is worked twice.
- `STATE.md` maps every state machine in the app. In the console, `FR.snapshot()` / `FR.history()` / `await FR.whenIdle()` show and wait on them.
- Art board: in claude.ai, editors get an **Edit layout** button (same editor as Fast Pitch). Edits save live to the artifact db `layout`; `python3 src/bake.py <repo> <docs_dir> <artifact_out_html>` bakes them into `lyBakedData` in `index.src.html`.
