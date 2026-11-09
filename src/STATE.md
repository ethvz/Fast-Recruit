# Fast Recruit: state machines

Every moving part of the app is a state machine. The six that span the whole app are **explicit**: they change only through `FR.set()` in `src/index.src.html`. The rest are small and local, so they stay inside their own code. They're listed below so nobody has to rediscover them.

## How to read the state

| Where | What you get |
|---|---|
| Browser console | `FR.snapshot()` returns every machine plus page, section, flow step, zoom and device mode. `FR.history()` / `FR.trail(10)` return the last changes. |
| CSS / tests | Each machine is mirrored on `<html data-fr-<machine>="<state>">`, for example `html[data-fr-ui="sheet"]`. |
| Tests / agents | `await FR.whenIdle()` resolves once the app has booted and no page change is running. Use it instead of fixed waits. |
| Events | `addEventListener('fr:state', e => e.detail)` gives `{machine, from, to, why}`. |
| Crash and feedback emails | Every report includes **App state** (snapshot). Crash reports also include **Last steps** (the last 8 changes before the crash). |

An unknown state logs `[FR] unknown state` in the console. It never throws, so a mistake can't take the app down.

## Explicit machines (`FR.machines`)

| Machine | States | Changes when | Notes |
|---|---|---|---|
| `boot` | loading → ready | First page shown. An auto-refresh after an error goes back to loading. | `hardReload()` allows at most 3 refreshes a minute. |
| `safety` | normal / safe | Set at start. Safe = 2+ crashes within 10 minutes (`fr_safe` in sessionStorage). | Safe mode drops background photos, animations and glows. |
| `nav` | idle → transitioning → idle; transitioning → queued → transitioning | `go()` / `openOverlay()`. A tap during a transition is queued and runs after `NAV_GAP`. | Only one page change runs at a time. Same-page section jumps don't transition. |
| `ui` | none / overlay / menu / quickmenu / sheet / popup | Menu, long-press section menu, sheets (edit flow, add sections, feedback, crash report, What's New), add-to-home-screen popup, video overlay. | Priority: popup > sheet > quickmenu > menu > overlay. Only one sheet or menu at a time. Anything except none/overlay blocks swipes, trackpad and arrow-key page changes. Escape closes the top one, and only goes back a page when nothing is open. |
| `flow` | off / on | `startFlow()` / `endFlow()`. Restored from `fr_flow` and `fr_seg` (sessionStorage). | Favorites live in localStorage `fr_favs` with a cookie and IndexedDB backup. |
| `offline` | unavailable / idle / downloading / ready | Service worker messages (`dlp`). Unavailable = no service worker (the Claude preview). | The download keeps going in the service worker if the menu closes. |

## Local machines (kept inside their own code)

| Machine | States | Where (search for) | Storage |
|---|---|---|---|
| Crash detection | alive → closed normally / crashed | `fr_alive`, `crashLoop`, `CRASH` | sessionStorage `fr_alive`, `fr_pos` (where, plus App state), `fr_reloads` |
| Swipe between pages | none → tracking → (page change / snap back) | `let sw =`, `swipeTo`, `snapBack` | — |
| Trackpad paging | idle → accumulating → cooldown | `wAcc`, `wCool` | — |
| Pinch and double-tap zoom | 1x → pinching → zoomed | `zoom`, `pinch`, `zpan`, `zoomTo` | — |
| Section snapping | free → touching → springing | `setupSnap`, `springing`, `touching` | — |
| Section loading (phones) | parked ⇄ loaded per section | `setupVirtual`, `park`, `load` | — |
| Image retry | ok → failed → retrying (up to 9) | `retryImg`, `failed` | — |
| Header idle hide | shown → hidden after idle → shown on scroll | `hdrHide`, `hdrKick` (in each board) | — |
| Mail queue | empty → queued → sent (14-day expiry) | `FB`, `fr_mailq` | localStorage `fr_mailq` |
| Add-to-home-screen popup | shows on visits 1–3, then never (or until dismissed forever) | `fr_a2hs` | localStorage and cookie `fr_a2hs`, sessionStorage `fr_a2hs_s` |
| What's New dot | unseen → seen | `fr_wn` | localStorage `fr_wn` |

## Rules for changes

1. A new app-wide mode goes in `FR.machines` and changes only through `FR.set(machine, state, why)`.
2. Anything new that opens on top of the page calls `uiSync()` (or `FR.ui()` from outside the main script) when it opens and closes. Give closing elements a `closing` class so they stop counting while they fade out.
3. Never add a new global boolean for "is X open/running". Read the machine instead: `FR.get('ui') === 'none'`.
