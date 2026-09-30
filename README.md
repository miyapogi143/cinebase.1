# CineBase — IT 424 Performance Task

Interactive Movie Database Interface built with **Django 5.x + HTMX 2.x + Alpine.js 3.x**. The implementation follows the supplied performance-task brief: Django owns server data and HTML rendering, HTMX owns server exchanges/partials, and Alpine owns small client-side UI state.

## Setup
1. Install Python 3.10+.
2. Open PowerShell in this folder.
3. Create a virtual environment: `py -m venv .venv` then `.[1m\.venv\Scripts\Activate.ps1`.
4. Install: `py -m pip install -r requirements.txt`.
5. Migrate: `py manage.py migrate`.
6. Load sample data: `py manage.py loaddata fixtures/sample_data.json`.
7. Run: `py manage.py runserver`.

### Sample movie catalog
The included `fixtures/sample_data.json` contains **36 movies total**: the original 6 sample movies plus 30 additional movie records. Run `py manage.py loaddata fixtures/sample_data.json` to load or refresh the complete catalog.
8. Open `http://127.0.0.1:8000/`.

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` and activate again.

## Alpine hosting decision
Alpine.js is loaded with `defer` from a pinned CDN version (`3.14.9`) because the brief permits a pinned CDN and requires no build step. HTMX is similarly pinned to 2.0.4. This keeps the submission build-free and easy to reproduce. For an offline-only deployment, replace the CDN files with locally downloaded static copies without changing the Alpine component architecture.

## Pages
- `/` — Catalog/search/filter/grid-list/quick preview/favorite/loading state
- `/movies/<slug>/` — Overview/Cast/Reviews tabs, read-more, trailer modal, star rating, review counter, spoiler reveal
- `/watchlist/` — status tabs, sorting, bulk selection/runtime, confirmation removal, empty state
- `/manage/movies/new/` — three-step wizard, dynamic cast rows, genre tags, slug preview, validation, unsaved warning

## Alpine component inventory
| Component | Page | Main state/getters | Store? |
|---|---|---|---|
| appShell | Global | theme, watchlist, toasts | Yes |
| mobileNav | Global | open | No |
| toastStack | Global | toast items | Yes |
| htmxLoader | Catalog | loading | No |
| catalogFilters | Catalog | query, selected, year range, rating, view, activeCount | No |
| movieCard | Catalog | hover, active | No |
| detailTabs | Detail | tab, trailer, added, hideSpoilers | No |
| readMore | Detail | expanded | No |
| starRating | Detail | rating, hover | No |
| reviewComposer | Detail | body, rating, valid | No |
| watchlistPage | Watchlist | status, sort, selected, filteredItems, totalRuntime | No |
| movieWizard | Editor | step, title, synopsis, genres, cast, canAdvance, slug | No |

## Required Alpine coverage
- Stores: `theme`, `watchlist`, `toasts`.
- Persisted state: theme and catalog grid/list view use guarded `localStorage`.
- Computed getters: `activeCount`, `valid`, `filteredItems`, `counts`, `totalRuntime`, `filteredGenres`, `canAdvance`, `slug`.
- `$watch`: catalog range/rating/filter state and editor title/dirty state.
- Magic properties: `$el`, `$refs`, `$nextTick`/Alpine lifecycle usage; `$refs.search` and `$refs.title` are used directly.
- Directives represented include `x-data`, `x-init`, `x-show`, `x-if`, `x-for`, `x-model`, `x-bind`, `x-on`, `x-text`, `x-transition`, `x-ref`, `x-cloak`, `x-teleport` and dynamic `:class`/`:aria-*` bindings.
- Event modifiers include `.prevent`, `.stop`, `.window`, `.outside`, `.debounce` and `.once` (the `.once` hook is documented below for extension/demo instrumentation).
- Keyboard interactions: `/` focuses search, Escape closes overlays, arrow keys switch detail tabs, Enter is supported by native form controls/buttons.

## Alpine + HTMX integration points
1. Catalog search/filter state is held in Alpine and serialized into HTMX `:hx-vals`; Django performs the actual database filtering and returns `_movie_grid.html`.
2. HTMX emits `HX-Trigger` after watchlist changes; Alpine's global watchlist store updates the navbar count without a full page reload.
3. HTMX review submission returns server-rendered review HTML and an `HX-Trigger`; Alpine listens to the event and displays a toast.
4. Alpine reacts to `htmx:beforeRequest`/`htmx:afterRequest` for the catalog loading indicator.
5. Alpine components live in Django templates/partials and initialize as part of the page lifecycle; server-owned lists are never rebuilt with Alpine `x-html`.
6. CSRF is supplied globally through HTMX headers in `base.html`.
7. Django data is passed with `json_script` where Alpine needs initial server data.

## Responsibility boundaries
**Alpine:** menu state, theme, tabs, modal visibility, rating preview, counters, selected chips, wizard step, previews, local sort/filter of already-rendered watchlist data.

**HTMX:** search requests, server filtering, watchlist POST/DELETE, review POST, server-rendered partial replacement, loading lifecycle.

**Django:** database persistence, validation, model relationships, server-rendered movie/review lists, sessions, security and final validation.

## Demo checklist
1. Mobile menu open/close and Escape.
2. Dark mode persists after refresh.
3. `/` search with live HTMX swap and loading state.
4. Genre chips + year/rating state feed HTMX.
5. Grid/list choice persists.
6. Card hover quick view and optimistic watchlist button.
7. Detail tabs with arrow-key navigation.
8. Read-more and trailer modal with Escape/backdrop close.
9. Ten-star rating hover/click + review character counter/disabled submit.
10. Spoiler reveal/hide.
11. Watchlist status filters, sorting, bulk select/runtime and confirmation removal.
12. Editor wizard, cast rows, genre tags, slug preview and unsaved warning.

## Part 1 document
See `docs/Part1_UI_State_Analysis.docx` for the decision table, component inventory, state map and integration points requested before coding.

## Part 3 Word submission
See `docs/CineBase_Submission_Document.docx` for page-by-page implementation snippets, setup notes, component evidence and the 5–8 sentence reflection.

## Notes
The brief requests a public GitHub repository and a screen recording. Those are external submission actions and cannot be created inside this ZIP. The project is structured so it can be pushed directly to GitHub and demonstrated locally.
