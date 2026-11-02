# Verbal variations

User approved all seven variations proposed in chat. Preserve the current classic daily/free games, Portuguese word banks/daily selection, local storage key verbal:data:v1, schema 1 backups, explicit updates, shared controls, EN/pt-PT, Safari 12 and compact QWERTY layout. No publishing or remote dependencies.

## Modes and defaults

- Two words: two distinct answers of the selected length, eight shared guesses. Each answer stops changing once solved. Keyboard colours refer to the selected board. Compact phones show one full board with a clearly labelled board switch; larger screens may show both. Never shrink eight-letter boards to unreadable half-width cells.
- Strict: six guesses; each must satisfy all previous score information, including duplicate counts. Separate progress from classic, with the same daily answer. Switching modes preserves both.
- Word ladder: curated start/target pairs with a verified route at every 4–8-letter length; change exactly one letter into an accepted word each step, no repeated words, at most twelve moves. Endpoints shown openly; score is move count. Show recent path on the compact board and provide complete path in Help/history. No exhaustive graph search at runtime.
- Theme: nature, food, objects, each with curated Portuguese answers at lengths 4–8. Six guesses; all ordinary accepted guesses remain valid. Theme selection does not mutate existing puzzles.
- Progressive: one series of five stages, lengths 4–8, six guesses at each. A stage victory explicitly unlocks Next length; a loss ends the series. Preserve and restore every stage. Daily and free series.
- Friend challenge: choose any valid 4–8-letter word, create/share a versioned validated fragment link, six guesses for the recipient. No account/server. The link is an encoding, not anti-cheat security. Reject malformed/oversized links without changing existing games. Cancel keeps current game; opening the same link resumes progress. Creating/sharing is explicit.
- One clue: one fixed, visibly revealed letter in all four rows; typing skips its position. Four guesses; daily/free. The revealed letter is immutable and supplied automatically in submitted words.

## Navigation and data

A Games control opens a compact mode picker; preserve Settings then Language at top right. Existing daily/free and size toolbar remains. Disable size for progressive (shows active size) and friend (shows link size). Theme and friend creation are reachable in the picker. Switching away and back restores drafts. Help explains current rules, strict feedback and keyboard board context. Stats/share identify each mode separately.

Keep legacy games untouched. Add optional validated `variants` and optional preference fields (`variant`, `theme`, `challenge`) to schema 1 in the same single atomic storage value. Older backups default to classic; newer backups preserve every variant and preference. Validate combined games <=10,000, input bytes <=5 MiB; reject invalid variant states before replacement. Keep the existing raw-value stale-window write guard and dirty-save handling. Unknown future variants are rejected, not discarded.

## Verification

Pure engine tests: all mode wins/losses/limits, strict duplicates, valid/invalid ladder paths, clue insertion, progressive transitions, theme coverage, deterministic seeds, fragment failures, additive backups including invalid/cancelled restore, no mutation on rejected guesses. Browser: mode navigation/draft persistence, EN/PT, offline submissions, two-board controls, friend-link creation/opening, progressive/clue, classic regression, storage conflict, backup restore preferences. Refresh all release/deployment hashes and verify staged publication using temporary Git repos. Physical iPhone 6 remains unverified; very short landscape may scroll. Independent final review required.

## Builder-check clarifications

Fragment links are previewed, including hashchange after startup; only explicit Play persists/selects a friend challenge. Full versioned token is its stable identity. Invalid links leave storage intact. Restore without preferences retains valid theme/variant/token preferences and recreates a missing selected puzzle using its deterministic seed or validated friend payload. If no friend payload exists, fall back to Classic without dropping imported records. Recompute outcomes from replayed guesses; validate canonical identity/answers, immutable clue position and sequential progressive stages. New schema 1 optional fields require the extension validator; unknown variants fail closed.
