# Verification — Verbal 1.3.1

Prepared 2026-11-01. Target deployment: verbal.basecentral.link; **not published there by this delivery**. Package intended for the existing local Git checkout on the user's Mac.

## Passed automated checks

- `node scripts/test-core.cjs`: all bank lengths/uniqueness, daily answer determinism, normalization, repeated-letter scoring, victory, Lisbon summer/winter date boundary, versioned JSON backup round trip and malformed/duplicate/post-victory rejection without source mutation, translation-key parity and asset presence.
- `node scripts/test-sw.cjs`: mocked service-worker install verifies SHA-256 for a complete release; a mixed asset is rejected before any cache writes. This is a unit simulation, not a browser offline test.
- `python3 scripts/test-deploy.py`: disposable local Git remote/checkouts. Valid clean deployment, public allowlist, unrelated files and .htaccess preserved, staging cleaned, dirty/untracked/ahead/detached repositories refused, overlapping directories and symlink destinations refused. No external host or credentials used.
- Node syntax checks for app.js, core.js, i18n.js and sw.js.
- `python3 scripts/prepare-release.py`: release manifest generated from all public runtime assets; version agreement enforced.

## Observed in current desktop Chrome via UI

- App starts, with Settings followed by a local flag language selector.
- Switching to 8 letters changes the grid; PALAVRAS is accepted and repeated occurrences receive separate clues.
- Switching from English to Portuguese, followed by reload, preserves the game and selected size/language.
- Four-letter daily victory is recognized and result sharing becomes reachable.
- Settings exposes backup controls, manual installation guidance, updates, help/privacy, version and selectable diagnostics.

The internal preview runs over `http://terminal.local` rather than a secure origin, so that browser correctly reports offline support unavailable. Service worker installation/activation and true offline reload were not verified in that initial preview; the 1.0.1 localhost regressions below cover them. The install prompt remains unverified. They must be checked on localhost or the final HTTPS deployment. This limitation is displayed by the app rather than promising offline readiness.

## Remaining manual checks

- Physical iPhone 6 / iOS 12.5.x / Safari 12, Safari on modern iPhone and installed Home Screen modes. Source avoids known unsupported startup APIs and includes a custom dialog and FileReader, but this does not establish device compatibility.
- 320px, short landscape, enlarged text, screen readers and touch interaction. The mobile keyboard uses six columns to retain 44px targets without horizontal page scrolling; desktop uses QWERTY rows.
- Actual browser export/download → file selection → restore, with Restore preferences checked and unchecked, plus quota and simultaneous-write scenarios. Pure format validation/round trip is covered, UI restore with preference inclusion/exclusion is now covered below; actual export/download/file-picker on devices remains manual.
- Explicit app update while another tab has unsaved work; interrupted real network release delivery. Service-worker integrity is covered by simulation.
- Dictionary editorial expansion and review. Current answer counts: 4 letters 284; 5 letters 416; 6 letters 328; 7 letters 335; 8 letters 369. Five-letter accepted guesses use the inherited larger initial list. No claim of a complete dictionary or English puzzle support.

## Shared baseline adoption

Local-first/privacy, bilingual UI, Settings/language order, state preservation, JSON backup with preferences, explicit updates and local assets are implemented. Device/browser evidence remains partial as above. The exact shared condensed font asset is still unspecified by the collection; helper text uses Arial Narrow with an offline Arial fallback. Cross-app typography conformance is not claimed. Old release caches are retained while old clients may exist; there is no automatic cleanup and disk use can grow over successive versions. Export recency/change status is session-only and explicitly labelled. The shared controls and engine are now locally vendored and checked against the central kit; game keyboard/tiles remain app-specific.

## 1.0.1 correction evidence — 2026-11-01

- `scripts/test-browser.cjs` initially reproduced the 320px board overflow, missing square fallback and custom language-button mismatch, then passed after the fixes. Chromium 156.0.8078.4 on macOS, viewport 320×640: all 4–8-letter boards fit the page, visible buttons retain 44px targets, Settings is bounded to the viewport with inset/aspect-ratio declarations removed, and the feature-detected fallback sizes tiles square. This simulation does not establish physical Safari 12 compatibility.
- Native flag selects in the header and Settings change EN/PT immediately without changing the saved answer/draft. UI backup restoration starts with Restore preferences checked; checked restores the imported preferences, unchecked retains the current preferences. A real service-worker-controlled offline reload preserves the restored language and previous draft.
- The core and word-bank files are unchanged. Storage key, schema, daily algorithm, save guard and explicit worker activation/cache retention remain unchanged. Version is now 1.0.1 in app and worker; all 15 release assets plus the navigation alias are SHA-256 verified in the offline cache.
- The actual shared Bash deploy/profile is tested against disposable local repositories: normal fetch/fast-forward pull, dry-run without fetching/writing, verify invocation without external requests, stale release hash rejection, allowlist, permissions, unrelated host-file preservation, stage/lock cleanup, dirty/ahead/detached refusal and overlap/symlink rejection. `scripts/deploy.py` was removed. The host no longer needs Python. Optional hosting headers remain manually installed and existing `.htaccess` is preserved.
- Added Verbal to the central folder list and regenerated the catalogue; retained the three excluded apps as comments. No production deployment is part of this local verification.

- Browser upgrade regression serves the original 1.0.0 assets from Git commit `8b340b2`, then 1.0.1. The old version remains active until Update app is chosen; the complete saved collection is unchanged after activation, both version caches remain present, and the new app reloads offline with its draft. This uses isolated browser storage only. A fresh independent reviewer reported no actionable findings after reading the runtime/deploy diff and passing the core, worker and deployment tests; its sandbox prevented browser startup, so browser evidence comes from the primary run.

## 1.0.2 play-screen and vocabulary update — 2026-11-02

- User requested a compact play screen with an unbroken three-row QWERTY keyboard, explicit plurals and wider accepted-guess coverage. The board/keyboard viewport test reproduced the old overflow at 320×480 before the layout change.
- Replaced the six-column mobile keyboard with three QWERTY rows. Letter keys explicitly use the user-requested narrow-width exception while retaining 44px height. Ordinary controls keep 44×44px targets. The length select and mode buttons share one row; decorative title/eyebrow are hidden. Board cells have 2px gaps and zero padding. Cell dimensions are calculated for the available viewport, so Safari 12 does not require aspect-ratio. Secondary controls may require scrolling on the shortest views; the attempts and keyboard remain together for play.
- `scripts/test-vocabulary.cjs` verifies normalized length/uniqueness, all original answers and guesses retained, expanded counts over five times the answer banks at each length, valid plural/conjugation examples, and rejected nonsense. Source dictionary is pinned under vendor/dictionary; generation uses only local Hunspell/unmunch plus Node/Python development tools. No runtime dictionary request or dependency is introduced.
- Accepted guesses: 4 letters 1,807; 5 letters 6,429; 6 letters 14,015; 7 letters 26,311; 8 letters 41,339. Generated payload 728,508 bytes, bounded below 1 MB. Answer banks and core/date/scoring/storage/backup logic are unchanged.
- Release version is 1.0.2. Both new runtime assets (guesses.js and dictionary-license.txt) are included in the public allowlist, worker integrity manifest, offline readiness check and private deployment hashes. Source dictionaries and development scripts stay outside the public root.
- Physical iPhone 6/iOS 12.5.x, installed Home Screen, enlarged text, landscape and screen-reader checks remain manual. Modern Chromium tests and CSS fallbacks do not establish physical-device compatibility.

Final 1.0.2 evidence: Chromium 156.0.8078.4 on macOS passed the EN/PT viewport matrix (320×480, 320×568, 375×559, 390×664, 768×900) at all lengths, verifying every keyboard row and board/keyboard visibility without horizontal overflow. The browser submitted MAES, CASAS, PAPEIS, ANIMAIS and CORACOES while offline. Native language/restore-preferences tests and explicit 1.0.0 → 1.0.2 upgrade preserved the full saved collection and old cache. Rebuilding vocabulary from the pinned sources reproduced identical bytes. Core, vocabulary, SW integrity and disposable deployment tests passed; an independent read-only review found no actionable issues, while explicitly leaving physical Safari/landscape verification open. Plural acceptance is stated beside the puzzle as well as in Help.

## 1.1.0 seven approved variations — 2026-11-02

Implemented Classic-preserving Strict, Two words, Themes, Progressive, Word ladder, Friend challenge and One clue. Added a pure rules/validation module and bounded curated challenge data. Existing answer banks and the 89,901 accepted-guess entries are byte-identical. The classic daily algorithm is unchanged; the only core change is an explicit optional validator for additive schema 1 fields. No storage-key change, destructive migration or production publication.

### Passed

- `node scripts/test-variants.cjs`: all seven rule sets, deterministic seeds, theme coverage, every curated ladder route (valid words/single-letter steps), strict repeated-letter constraints, dual terminal state, all five progression steps, four-guess clue insertion, friend-token round trip/malformed rejection, mode limits/losses, old backups, all-mode backup round trip, canonical answer/key/clue validation and invalid/skipped-stage rejection.
- `node scripts/test-variant-regressions.cjs`: ladder cannot revisit its start, including imported histories; friend preference tokens must also contain accepted vocabulary even when variants are absent. Both reproduced as failures before corrections.
- `scripts/test-variations-browser.cjs`, Chromium 156.0.8078.4/macOS: new picker and drafts, dual solve and board switch, one-clue solve, all five progressive stages, a complete ladder, themed solve while genuinely offline, explicit friend-link creation/preview/resume, invalid-link storage preservation, Classic draft preservation, 8-letter variants at widths 320/375 and heights 568/667 in EN/PT, checked/unchecked backup preferences, complete variant restoration, invalid-backup refusal, true offline reload, simulated quota failure preserving the session draft, and a second-window write blocking stale unsaved changes.
- A checked restore from Double board two to a completed Classic game initially reproduced missing keyboard colours. The fix retains single-board keyboard scoring independent of the dual-board view; the full browser regression passed after correction.
- Existing `scripts/test-browser.cjs`: Classic portrait viewport matrix and QWERTY/touch rules, offline expanded plural guesses, legacy-CSS overlay/square fallback, native language controls and restore preferences, and real explicit 1.0.0 → 1.1.0 upgrade preserving all classic games and old caches. Optional new defaults are added to old preferences without dropping their values.
- Core, vocabulary, SW install integrity, actual temporary-Git deployment tests and central actual-profile publication tests passed. The worker verifies 19 assets plus the navigation alias; deploy publishes exactly 21 reviewed files, including the new challenges.js/variants.js, with refreshed private hashes. No host credentials or live deployment were used in these tests.
- Visual inspection of two-word and clue screenshots confirmed readable eight-letter cells, compact controls and three QWERTY rows. Large-screen boards are side by side; compact phones switch full boards with labelled keyboard context.

### Independent review

A fresh reviewer read the spec and full diff and identified three P2 edge cases: start-word ladder loops, invalid vocabulary in a preference-only friend token, and restored single-board keyboard colours after viewing board two. All three were reproduced with failing regressions, fixed, and confirmed addressed in a scoped re-review. No new breakage was identified in the corrections.

### Remaining limits

Physical iPhone 6/iOS 12.5.x/Safari 12, installed Home Screen, screen readers and real platform share/download dialogs remain manual. Very short landscape/enlarged-text views may scroll to retain readable cells and accessible controls. Friend links encode their answer and deliberately offer no anti-cheat security. Old version caches are retained for existing clients. Released challenge tables must remain immutable or receive versioned definitions/migration before expansion.

## 1.2.0 Deduction and paper integration — 2026-11-02

- Added the paper-only deduction rules as a persistent playable mode: pre-scored clues, candidate cross-outs, selection and answer checking. An incorrect candidate is rejected without consuming guesses or adding clues. Notes/drafts and solved states survive switching, reload and JSON backup/restore. Existing game banks and all previous variations are preserved.
- Initial immutable paper-v1 catalogue: 60 puzzles, 12 at each length 4–8, about18kB. `scripts/test-paper.cjs` checks all candidate/answer lengths and vocabulary, exactly one solution, every clue necessary, every score against core.js, deterministic bounded pack selection, invalid ids/options, rejected wrong answers without mutation, exclusion/draft validation and round-trip backups.
- Offline vector PDF and SVG/HTML print generation has no runtime dependency. 4/12 puzzle packs, fixed/mixed sizes, EN/PT instructions and optional separate last-page solutions. Preparing a pack does not write localStorage. Unsupported print dialogs have an explicit save/open-PDF path for iPhone. Previous standalone PDFs and generator were kept.
- `scripts/test-paper-browser.cjs` passed in Chromium156.0.8078.4/macOS at320×568: deduction, cross-out persistence, failed candidate safety, actual PDF download in both languages while offline, print preparation without game writes, optional-key omission, explicit print invocation, revoked blob after close, full backup restore and offline reload.
- Actual downloaded PDFs and Chromium HTML-print PDFs were independently parsed with pypdf strict=True: four A4 pages, correct language, key on its own last page. Solution-free unit exports have three pages. PDFs were rendered with Poppler and inspected; the print HTML and direct PDF align without clipped cells/text. Fontconfig for QA used only a temporary local config; no app font/runtime dependency was added.
- Core, vocabulary, all seven existing modes, review regressions, original classic browser suite, real SW update1.0.0→1.2.0, worker integrity, temporary-Git deployment and central actual Verbal deployment-profile checks passed. Shared controls and engine copies still match canonical files. Runtime assets/release/deploy checksums include paper-data.js, paper.js and paper.css: 24 public files;22 verified release assets plus navigation alias.
- An independent read-only review found no actionable issues in rule validation, compatibility, bounded selection, PDF encoding/byte offsets, print isolation or blob cleanup.

Remaining manual evidence: physical iPhone6/Safari12/Home Screen PDF save/open/Share→Print and real printer margins/dialogs; screen readers/enlarged text. Safari12-compatible syntax/APIs are retained, but desktop emulation is not physical-device verification. No production publication, push or commit performed.

## 1.2.1 print catalogue expansion — 2026-11-02

Expanded the printable catalogue from60 to400 records,80 at every length4–8. Original60 objects, ids and ordering are frozen in scripts/fixtures/paper-v1.json;340 print-only records use new paper-print-v2 ids. Runtime remains bounded, offline and without dictionary search. Dataset is117,787 bytes uncompressed. Screen-game choose() explicitly keeps the original v1 pool, so appending print records cannot change existing answers/keys or invalidate backups. Printing pack() uses all400.

The updated test-paper.cjs first failed on60!=400, then passed:400 unique ids and answers; all clues/core scores; unique solutions; every clue essential;80 records per length; original60 unchanged;20 prior daily/free selections and backup validations preserved; deterministic valid 4/12 selections; new ids selected; and vector exports exercise all400 records in100 four-puzzle packs. Existing variant/core/review regressions, SW integrity and temporary deployment tests passed. test-paper-browser passed offline game/restore, actual bilingual PDF download/print and URL cleanup with the larger dataset. The print dialogue shows its actual catalogue count.

Independent scoped review found no actionable issues in catalogue compatibility, append-only preservation or reproducibility. Real-time generation on the player device was not added: it would need bounded/background generation plus uniqueness/quality checks for older Safari devices. Physical-device printing remains unverified. This expansion is local and unpublished.

## 1.3.0 catalogue1000 and print/PDF request history — 2026-11-02

- Expanded append-only to1000 unique puzzles/answers,200 per length4–8. Original400 objects/order remain identical to scripts/fixtures/paper-print-400.json;600 new print-v3 ids append. Original60 gameplay choices stay unchanged. Dataset294,856 bytes uncompressed.
- Added stable short codes A/B/C plus word length and index to puzzle and answer-key pages. Optional schema1 paperHistory stores canonical puzzle-id request timestamps for PDF and print, with strict validation and the existing atomic raw-value guard. It records requests, including cancelled dialogs, not confirmed saving/printing/solving. Preparing/regenerating alone remains read-only.
- Default pack exclusion uses the history. Mixed sizes can use other available lengths; insufficient unused puzzles produces a visible error without silent repeats. Explicit repeat override remains available. A searchable25-row paginated history avoids rendering1000 rows at once. Backups include it; legacy backups with no field retain current history, explicit new history replaces it. Null storage-clear events do not resurrect records.
- test-paper.cjs first reproduced400!=1000; now verifies all1000 unique solutions, essential clues/core scores, unique codes, preserved400/legacy60, old seeded gameplay identities/backups, and renders every record in250 in-memory PDF packs. test-paper-history.cjs first reproduced missing record functionality; now proves250 consecutive four-puzzle selections cover1000 with no repeats, exhaustion/repeat override, pure nonmutating history merges, invalid id/field/date refusal and schema1 round trips.
- Actual Chromium paper suite: new request actions initially failed PDF-request-not-recorded; now passes real bilingual PDF downloads, browser print requests, request persistence/reload/backup, no game mutations, duplicate-free later selections, code search, disabled-pagination focus trap,1000-entry pagination, exhaustion, repeat override and quota failure warning while PDF still downloads. Requests remain only in session memory after a quota error, with a truthful warning.
- Independent review found a P2 cross-window overlap: another tab could request a prepared puzzle without invalidating the first tab's pack. Browser regression reproduced the timeout, then passed after comparing incoming vs prior history and invalidating newly overlapping avoid-enabled packs. Same-tab PDF+print remains allowed. A second failing regression exposed legacy-backup history loss; the restore/storage paths preserve history only for an absent field. Scoped re-review confirmed the finding addressed and no new breakage in the corrections.
- Existing core/vocabulary/variant/review-regression, Classic browser and explicit old-release update, SW integrity, temporary deployment and actual central Verbal profile checks passed. No new external runtime dependency, storage key/schema bump or production operation. Shared kit/engine copies match.

Physical iPhone6/Safari12/Home Screen printing, real printer output and browser context-menu download variants remain manual. The history begins with new requests; earlier paper/PDF activity cannot be inferred automatically. Clearing origin data removes the local history, so portable preservation uses full JSON backup.

## 1.3.1 catalogue1700 — 2026-11-02

User requested2000 or at least1700. Expanded to1700 with distinct answers, within the1732 existing editorial words; no bank padding, changed vocabulary or repeated answer was required. Distribution:4 letters284,5 letters416,6 letters328,7 letters335,8 letters337. The initial1000 are unchanged in content/order via scripts/fixtures/paper-print-1000.json;700 appended records use print-v4 ids and D-codes. Screen-game v1 seed selection remains unchanged. Runtime data504,981 bytes uncompressed.

Updated test-paper initially reproduced1000!=1700, then passed all1700 unique/essential solutions against core scoring, preserved1000/400/60 fixtures and legacy gameplay identities, valid short codes and425 PDF-export batches covering every record. History regression now exhausts all1700 in425 disjoint four-puzzle selections, then verifies explicit exhaustion and repeat override. Uneven length capacities correctly fall back to available lengths. Core, variant/review-regression, worker integrity, temporary deployment and actual profile checks passed. Browser paper workflow passed actual bilingual downloads/print, backup/history restoration, pagination, exhaustion, quota warnings and cross-window duplicate invalidation with1700. Independent scoped review found no actionable regression.

All histories/codes/backups preserved; optional fields and storage schema unchanged. Version1.3.1 is local and unpublished. Physical-device printing remains outside the desktop verification evidence.

## 1.3.2 game UI — 2026-11-02

Rules titles identify the current localized game and selected word theme. Game/theme picker buttons are centered. Statistics uses one semantic table with row/column headings, played/wins counts and Classic best attempts. Animals, Plants and Places add five reviewed accepted words per length without modifying the three released theme tables or ladder routes. Both double boards remain visible:4–5 letters side by side,6–8 stacked; outlined source board and Word1/Word2 still select keyboard clues. Stacked boards scroll naturally on phones.

Passed: core, variants, variant regressions, vocabulary, all1700 paper puzzles, paper history, SW integrity and deployment tests; syntax checks; diff whitespace check. Chromium headless1248 on macOS: new bilingual UI suite validates rules titles, table, six themes and both boards at every length at320/375/768 widths. Existing variations and classic browser suites passed, including offline play/backup and actual1.0.0→1.3.2 update retaining prior caches and games. Screenshot inspected for stacked eight-letter boards. Physical iPhone6/Safari12/Home Screen remains manual. Release metadata and private deployment hashes regenerated; old caches retained; no production publication.

## 1.4.0 English word language — 2026-11-02

All nine games support independent Portuguese/English vocabulary through the native Words selector and Settings. Interface language remains separate. Old Portuguese collections, answer banks, released theme/ladder tables, print catalogues and v1 friend identities are unchanged. English uses additive schema1 english games/variants/nextFree and vocabulary-bound challenge preferences/tokens; restores and exports include both languages. English free counters/drafts are independent. Print controls independently select word and instruction languages, with1900 total puzzles (1700 PT,200 EN). English codes/history/exclusions/exhaustion are distinct.

Content:1671 English editorial answers and59891 accepted guesses, six categories at every length, preverified ladders. Pinned British/American Hunspell sources, hashes, source notices and full license texts in vendor/english; public attribution cached offline. Reproducible builders have no network dependency. Before the initial English release, review removed two month proper names and regenerated the unpublished English catalogue so neither clues nor banks retain them. All Portuguese fixtures stay unchanged.

Passed final Node checks: core, variants, variant-regressions, vocabulary, all1700 Portuguese paper records/history, English-content (source hashes/lowercase editorial dictionary checks/reproducible bytes), English-variants (every mode at every length), English-storage (old backups, both-language roundtrip, corrupted and mismatched-language records/tokens), English-paper (all200 unique essential puzzles, every record exported, PDF offsets/page counts, both instruction languages, history and exhaustion), worker integrity (27 hashed assets plus navigation alias). Python deployment tests passed; public allowlist28 files with fresh release/private hashes. All public JavaScript syntax checks and diff whitespace checks passed.

Chromium headless1248/macOS final browser suites passed: Classic (phone viewport matrix, touch controls, language/restore, actual1.0.0→1.4.0 explicit upgrade retaining old cache/progress), existing variations, existing paper/history suite, and new English suite. New suite solves every mode in English, exercises Portuguese/English drafts, interface independence, language-bound friend creation/preview/resume, preview without game mutation, cross-tab composer language, independent Free counters/drafts, actual English-word PDF downloads in both instruction languages, invalid-backup preservation, checked/unchecked preference restoration and offline reload. Bilingual UI regression covers named rules,26 statistics rows, six themes and simultaneous boards at320/375/768 widths.

Two integration review findings were reproduced/addressed: rejecting English tokens in the legacy PT challenge preference before restoring, and preserving the displayed word language when another tab changes vocabulary during friend composition. Settings refreshes after external sync. Scoped content and paper reviews found no remaining issues after correction; final integration re-review recorded separately below.

Actual browser-downloaded PDFs inspected with pypdf strict=True: four A4 pages, correct word/instruction labels, stable E codes and solutions on their own last page. Rendered with pypdfium2 and visually inspected puzzle/solution pages in both instruction languages: eight-letter rows/banks and page margins remain clear. A first QA assertion incorrectly treated the ordinary footer text “Solutions on the last page” as a solutions-page title; corrected to exact title-line matching. No PDF product defect. Phone screenshot inspected. Early offline browser retries occurred while content/license bytes were still being finalized; after final prepare-release.py all suites passed.

No publication, push or commit. Caches for older tabs are retained. Physical iPhone6/iOS12.5.x/Safari12, installed Home Screen, real platform print/share dialogs and screen readers remain manual; desktop Chromium is not physical-device evidence.

Final independent integration re-review: clear; prior findings resolved. Reviewer independently reran English-paper, English-storage, service-worker and deployment suites; all passed, including all27 offline assets.

## 1.4.1 English print catalogue expansion — 2026-11-02

Expanded English printing from200 to1671 unique-answer puzzles, adding1471 print-only records from the existing reviewed editorial banks. Length counts:4=482,5=266,6=291,7=297,8=335. Original200 definitions/order fixed by scripts/fixtures/paper-en-200.json; English screen choose is explicitly frozen to paper-en-v1, preserving saved daily/free deduction identities. New paper-en-print-v2 ids use F codes; E codes and all PT definitions unchanged. Printing uses the full English catalogue, with combined history/backup validation. No vocabulary change or migration.

Passed: English paper tests cover all1671 scoring/unique/essential puzzles, unique codes, original200 fixture, frozen seeded gameplay identity, every record exported in both instruction languages, PDF offsets/pages and language-separated history. Exhaustion test selects1668 disjoint puzzles, refuses a further four when only three remain, and allows explicit repeat. Print-only selection excludes the original200 and validates history. English variants/storage and original PT paper/history suites passed. Core, SW27 hashed assets, JavaScript syntax and deployment tests passed. Generator rerun produced the same1671 records without changing definitions.

Chromium headless1248/macOS English browser and existing paper/history suites passed: actual bilingual English-word PDF downloads, print preparation, backup, retained preferences, history, quota/cross-tab handling and offline reload. Actual downloaded PDFs parsed with pypdf strict=True: four pages, correct vocabulary/instruction labels, new F codes, solutions separately; rendered and visually checked. Independent scoped reviewer found no actionable issues and independently confirmed fixture preservation, gameplay selection, counts, codes, clues, history and exhaustion.

Release/private hashes regenerated for1.4.1; old caches retained. No production publication, push or commit. Physical iPhone6/Safari12/Home Screen and real print dialogs remain manual.

## 1.4.2 rules correction — 2026-11-02

Removed the six-guess claim from shared EN/pt-PT rules; each game's existing specific instructions supply its correct attempt/move limit. Shared text also works in Settings without implying a mode. UI regression reproduced the old contradiction as a failing assertion, then passed for Classic, Two words, One clue, Word ladder and Deduction in both languages, explicitly checking8/4/12 wording. Core, service-worker integrity, deployment tests and i18n syntax passed. Release metadata/private hashes refreshed; old caches retained. No publication.

## 1.4.3 word-language flags — 2026-11-02

Game word selector and its Settings copy now show Portugal/UK flags, matching the interface selector's native flag format. Accessible name and tooltip identify Words plus the full current vocabulary language, preserving the distinction from Interface language. Controls remain74px wide with44px minimum height. Core, worker integrity, deployment and app syntax checks passed; English gameplay/backup/offline and Classic phone-layout/upgrade browser suites passed. Release metadata refreshed; old caches retained. No publication; physical iPhone/Safari remains manual.

## 1.4.4 daily countdown — 2026-11-02

Solved daily games display localized time remaining until Lisbon midnight (hours/minutes, rounded up to the minute). Friend and Free games excluded; progressive intermediate stages do not claim the whole series is solved. Refreshes every30 seconds while visible, with existing day rollover preserved. Core countdown tests cover winter, summer, minute rounding and23/25-hour DST days. English browser suite verifies solved daily messages in EN/PT across all ordinary modes including Deduction. Core, worker integrity, deployment checks passed; release hashes refreshed and old caches retained. No publication.

## 1.5.0 attempt editing — 2026-11-02

Physical Enter submits from ordinary play controls, including a focused length/vocabulary selector; modal input behavior and deduction native form handling stay intact. Current editable cells can be selected for replacement using physical/virtual letters; cursor advances, fixed clue cells and frozen solved double boards remain protected. Sparse drafts use internal spaces, accepted by Classic/variant backup validators but rejected as incomplete on submission. Selected cell is outlined. Unused keyboard background is lighter; absent score grey is also lighter with dark text for contrast.

Passed new browser check: out-of-order letters, sparse draft persistence across reload, replacing positions with virtual letters, Enter submission while selector focused and immutable clue cell. Existing English all-mode/offline/backup browser suite passed. Core, variants, English storage, variant regressions, SW integrity, deployment and syntax passed. Release hashes regenerated for1.5.0; caches retained. No publication. Physical iPhone/Safari remains manual.

## 1.5.1 Classic random unused words — 2026-11-02

Confirmed FELIZ was the deterministic PT five-letter daily answer for2026-11-02. User explicitly requested random new daily games after completion. Classic Daily and Free now choose uniformly from remaining unused editorial answers, with saved Classic game records providing persistent per-vocabulary usage history. Existing unfinished games resume. Another word appears after Daily Classic wins/losses; its finished game is archived without overwriting occupied free keys, then a new daily record is created. Classic midnight countdown removed; other daily variants unchanged. Pool exhaustion refuses repeats with EN/PT guidance. Backup schema and word banks unchanged.

Passed unused-selection unit test (random choice, prior history exclusion, exhaustion), PT/EN browser sequence of eight daily completions with no repeats, reload and backup validation. Existing English all-mode/offline/backup browser suite passed. Core, SW, variants, English-storage, deployment and syntax passed. Release1.5.1 hashes regenerated; caches retained; no publication. Physical iPhone/Safari remains manual.
