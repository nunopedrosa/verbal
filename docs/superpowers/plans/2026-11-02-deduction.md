# Deduction and printable packs implementation plan

User approved adding the paper-only deduction game to Verbal. Implement inline, with final independent review.

Goal: Games → Deduction provides pre-scored clues, a finite candidate bank, persistent eliminations and a final answer. Games → Print puzzles prepares 4/12 puzzles, optional size filter, solutions on a separate page, direct offline PDF/save/open and HTML print. No service/account/runtime dependency. Preserve classic/variation definitions, verbal:data:v1/schema1, guarded writes, backups and EN/pt-PT/Safari12. Existing uncommitted paper artifacts are prior user work to keep.

Architecture: a versioned immutable prevalidated catalogue generated with the existing developer-only paper builder; a pure JS paper/PDF module; additive deduction records in variants. Pack preparation is independent of game data. Bound catalogue selection (no search in runtime), max12 puzzles per pack, one live blob URL released on context change. Standard-font vector PDF, black-and-white symbols, separate optional answer key. HTML print with PDF fallback for iOS installed mode.

- [x] Tests first: unique/essential clues, deterministic selection, valid/invalid deduction submissions and exclusions/restore, PDF page/xref/text integrity.
- [x] Generate immutable catalogue, pure selectors and offline vector PDF/print HTML.
- [x] Add deduction rules, UI candidate elimination and answer checking, print dialogue and URL cleanup in both languages.
- [x] Browser-check offline mode, preservation/restoration, PDF download actual contents, print HTML pagination and narrow layouts; refresh 1.2.0 release inventory/hashes.
- [x] Independent review, fix findings, document evidence. No commit/push/publication.

Review focus: duplicate-letter scores; forged exclusions/identity; mode/size changes preserve progress; print preparation never writes games; solution omission; print cancellation/blob lifetime; PDF encoding and print dimensions. Very short views and deduction's word list may scroll naturally; do not shrink ordinary controls below44px.

Evidence: test-paper and actual browser download/print tests passed, PDF parsed/rendered, old suites passed, final independent review returned no actionable findings. Prior uncommitted standalone paper pack preserved. Work is local and uncommitted.
