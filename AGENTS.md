# Verbal

Before modifying this app, read `docs/SHARED_PWA_RULES.md` (reviewed copy of the shared PWA rules, revision 2026-10-27, decision set 6), then README.md and docs/VERIFICATION.md. The original shared document's central-toolbox-only rules do not change Verbal's own file layout. No missing sibling-path dependency is required.

- Repository on the user's Mac: `/Users/nfp/github/pwa/verbal`. Production destination: `https://verbal.basecentral.link`. Do not publish production unless explicitly instructed.
- Static HTML/CSS/JavaScript in `public/`. No build step, npm, PHP, account, telemetry or remote runtime dependency.
- Support iPhone 6 / iOS 12.5.x / Safari 12. Keep startup code parseable; feature-detect optional APIs. Do not use dialog.showModal, replaceChildren, optional chaining, nullish coalescing or File.text.
- UI languages: pt-PT and English, immediate switch without altering the Portuguese puzzle. Game vocabulary language and UI language are separate concerns. English word banks are not part of v1.0.0.
- Word lengths 4–8, six guesses for each. Correct occurrence counts for repeated letters. A separate daily answer for each length, midnight Europe/Lisbon. Do not reorder a released answer bank without versioning the daily algorithm and preserving saved games.
- Persist games, drafts and preferences in one app-scoped localStorage value. Lossless backup JSON `format: verbal`, `schema: 1`. Restore replaces, validates first and offers Restore preferences checked by default. Preserve storage after failed imports; guard stale writes across windows.
- The word banks are manually selected starting lists, not a full dictionary. All entries must be complete words with the declared normalized length. Do not pad banks with truncated words or unverified fragments. Expand reviewed lists and keep answers a subset of accepted guesses.
- Settings gear followed by local flag language selector in top right. 44px target minimum, page fits 320px, localized labels/errors, managed focus, non-color score cues. Use 2px control and 4px panel corners.
- Cache the complete release atomically at install; never auto-activate updates. Preserve old version caches while old tabs may use them. Bump app.js and sw.js VERSION together, run `python3 scripts/prepare-release.py`, and document cache retention. Verify each release asset hash before populating the offline cache.
- Public webroot receives only scripts/deploy.py FILES. Hosting configuration is optional and installed manually, never exposed under its source name. Pull-only host deploy; refuse dirty/ahead/detached sources and overlapping webroots, no reset/clean/stash/push/delete of unrelated files.
- Run `node scripts/test-core.cjs`, `python3 scripts/test-deploy.py`, JS syntax checks and relevant browser QA. Document actual evidence; physical iPhone 6 validation is still required.
