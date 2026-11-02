# English vocabulary across Verbal

## Requested outcome
Add English as a selectable puzzle language for all nine modes: Classic, Strict, Two words, Themes, Progressive, Word ladder, Friend challenge, One clue and Deduction. Include English-word printed puzzle packs and PDF downloads. Keep Portuguese available and preserve existing progress, shared links, print history and backups.

## Proposed behavior
A native Words selector offers Português and English in the game controls, separate from the existing interface-language flag selector. Word language also appears in Settings. Existing installations and old backups default to Portuguese vocabulary. Switching vocabulary resumes the selected language's saved game and draft; it never translates or overwrites an existing puzzle. Daily editions retain the Lisbon midnight boundary, with independent answers for each language and length4–8. Display the vocabulary explicitly in the play screen and rules. Statistics groups rows by word language.

Every existing mode retains its rules and limits in both languages. English Themes includes all six current theme categories, with curated English answers for each supported length. English ladders use offline preverified routes of accepted one-letter changes, with no repeated words. Deduction uses a separate immutable English catalogue generated and checked for one solution and necessary clues.

Friend links encode vocabulary language in a new versioned token. Existing v1 links remain Portuguese with identical identities. Preview identifies word language before explicit Play; Play resumes that token's exact game, regardless of the current language preference. Invalid/unknown-language tokens leave saved data untouched.

Print preparation offers separate Word language and Instructions language controls. Default word language follows the current game and instruction language follows the interface. A pack contains one vocabulary language; headings and filenames identify both. English-word packs support4/12 puzzles, fixed4–8 or mixed lengths, optional separate solutions, PDF download and isolated HTML printing. History records distinguish both catalogues, including searching language and stable unique codes. Avoid-requested behavior stays language-specific and never silently repeats on exhaustion.

## Data and compatibility
Preserve every released Portuguese answer list, theme, ladder and paper record in content/order and preserve all old deterministic identities. Extend schema1 additively with explicit vocabulary metadata and separate language-aware identities/collections, validated against the corresponding canonical banks. The builder chooses the exact additive representation after mapping validators; no old fields may acquire a different meaning. Absent vocabulary means Portuguese. Export/restore includes both languages, preferences, drafts, friend identities and print history. Restore-preferences unchecked retains vocabulary selection too. Reject malformed imports atomically, including cross-language answers/puzzle ids and unknown languages. Retain stale-window guards and bounded collection limits.

## Content and implementation choices (proposed defaults)
Use British English as the editorial spelling default, accepting common American variants in guesses when present in the pinned source. Obtain an appropriately licensed, pinned English dictionary with source revision, attribution and reproducible generation. Keep editorial answer lists separate from accepted guesses; exclude obvious proper names, abbreviations and unsuitable answer content. Do not describe a finite dictionary as exhaustive. No external runtime services or dependencies; all languages work offline after installation.

Target a substantial reviewed initial English print catalogue (at least200 puzzles, with at least40 per length), rather than claiming parity with the1700 Portuguese records. All must have distinct answers, a unique solution, no redundant clues, valid full words and layout-safe bank/clue counts. Preserve immutable English ids from first release; expansion is append-only. The builder may exceed this floor if quality checks support it.

Keep Safari12/iPhone6 compatibility, localized EN/pt-PT labels and errors,44px ordinary controls and320px layout. Existing simultaneous Two words board behavior remains. Update explicit cache assets, hashes, deploy allowlist and synchronized release version. Retain old caches for existing tabs. No publication or push is authorized by this request.

## Verification
Add regression tests before language-dependent logic: unchanged Portuguese identities/fixtures and old backups/links; English deterministic play and limits in every mode; six theme categories and verified ladder routes at every length; draft isolation; strict repeated letters; language-bound friend tokens; all-language backups and invalid imports; print-history separation/exhaustion. Browser tests cover interface/vocabulary independence, switching/resuming, all modes, English offline reload, share preview and bilingual print controls at320/375px.

Validate every English deduction record against core scoring, uniqueness and clue necessity. Inspect real downloaded English-word PDFs with both instruction languages, correct text and solutions, page counts and print boundaries; render representative PDFs for visual QA. Run core, variants, paper, history, vocabulary, SW, deploy, syntax and relevant browser suites. Document actual evidence and physical-device limitations.
