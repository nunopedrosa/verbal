# Verification — Verbal 1.0.1

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
