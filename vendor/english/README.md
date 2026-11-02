# English content provenance

The four Hunspell source files and original README notices are unchanged copies from LibreOffice/dictionaries revision `4f1df64b2e8e14751aa7c2205d170ca016071315`, directory `en/`.
REVISION includes source SHA256 values. The American source derives from SCOWL (see its full permissive source notices); the British source is LGPL (see its original README and the complete COPYING.LESSER and COPYING texts). The upstream `license.txt` is also retained verbatim.

`editorial.json` is Verbal's separately selected answer, theme and route data. British spelling is the editorial default; accepted guesses combine both dictionaries. These are finite selections, not an exhaustive dictionary. Proper nouns and abbreviation entries are excluded by retaining only originally lowercase ASCII dictionary entries before affix expansion. The generated forms are checked against Hunspell.

Run `python3 scripts/build-english.py` from the repository root. It requires development-only `unmunch` and `hunspell` executables; generation is offline. The deployed `public/english.js` has no external or runtime dependencies. Run `node scripts/test-english-content.cjs` to validate generated content, source hashes and byte-identical regeneration.

The first release freezes editorial answer order and all theme and route definitions. Future expansions must preserve those identities or version their definitions.
