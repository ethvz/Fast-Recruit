# Crash reports handled

| Gmail message id | Received | Page | Device | Orientation | Outcome |
|---|---|---|---|---|---|
| u_T0T_OuyOUTOXwAbLM_zbNg/vcbdh4iabbeke7lm0620 | 2026-11-09 | Why Vivint › Package Costs | iPad 1032×1376 (Claude app viewer) | Portrait | fixed: upright iPads now load the smaller photo copies phones use (-26% decoded image area there); idle animation pause from 11-09c also applies |
| u_T0T_OuyOUTOXwAbLM_zbNg/a9if2o3k0l2ctcywob3n | 2026-11-09 | Opportunity › Averages (safe mode) | iPad 1032×1376 (Claude app viewer) | Portrait | needs Ethan: section measured very light in safe mode (0.9 MP images, 12 layers, no errors); no app cause found |
| u_T0T_OuyOUTOXwAbLM_zbNg/1zc07l5grj9eb5zpr9er | 2026-11-09 | Home (right after opening) | iPad 1032×1376 (Claude app viewer) | Portrait | needs Ethan: Home is light (1.5 MP, 10 layers, no errors); app was alive 5s later sending reports, so it died later while on Home; no app cause found |
| 1a1c6ea0830d6ab0 | 2026-11-10 | Why Vivint › History (4s after opening, offline download running) | iPad 1032×1376 (Home Screen app) | Landscape | fixed: the 3400px History wheel no longer gets its own full-size Safari layer while it turns (peek on arrival and swipes); it now turns through a custom property on phones/tablets. Wheel layer gone during the peek, peak layer area -20% |
| u_T0T_OuyOUTOXwAbLM_zbNg/c8n0nhcu06ucc8v93sbt | 2026-11-10 | Lifestyle (while changing page from Experience) | iPad 1032×1376 (Claude app viewer) | Portrait | needs Ethan: transition measured normal (35 MP layers, 2.5 MP images, no errors); 4th unexplained crash from this iPad in the Claude app viewer |
| 1a1c7428fe051639 | 2026-11-10 | Unknown (no state saved) | iPhone 12/13/14 "iOS 15.0" Safari 390×844 | Portrait | needs Ethan: matches Playwright's "iPhone 13" test profile exactly; most likely a test run closing the page without a normal exit, not a real crash |
| 1a1c742f978b77f1 | 2026-11-10 | Unknown (no state saved) | iPhone 12/13/14 "iOS 15.0" Safari 390×844 | Landscape | needs Ethan: same test-profile false alarm as the row above (30s later) |
