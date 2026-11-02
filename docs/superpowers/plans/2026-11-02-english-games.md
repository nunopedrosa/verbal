# English Games Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans or superpowers:subagent-driven-development task by task.

**Goal:** English vocabulary in every game and print workflow while preserving Portuguese identities.
**Architecture:** Add English content and language-aware factories. Keep Portuguese games in original collections; store English games/variants in optional english collection. Paper combines immutable catalogues but selects by vocabulary.
**Tech Stack:** Static Safari12 JavaScript, Python generators, Node and Chromium tests.
**Spec:** docs/superpowers/specs/2026-11-02-english-games-design.md

## Global Constraints
Offline; no runtime dependencies; Safari12; schema1 additive; preserve all Portuguese content/ids; no publication.

## Review Focus
Old backups and links remain Portuguese; English tokens must bind language; language changes preserve drafts; English print exhaustion ignores Portuguese capacity; failed import cannot lose either language.

### Task1: English content
- [x] Pin licensed English dictionary and reproducible generation in vendor/english and scripts/build-english.py; curated public/english.js exports banks, guesses, six themes and verified ladders.
- [x] Verify vocabulary, theme coverage, route validity and deterministic output.

### Task2: English paper
- [x] Generate public/paper-en-data.js with200 unique essential puzzles,40 per length, canonical immutable ids.
- [x] Extend public/paper.js language-aware choose/pack; all-catalogue get/history; English codes and language-correct export headings; test every record and real PDFs.

### Task3: Gameplay/storage and links
- [x] Extend variants create with options.language and English challenge token version; preserve Portuguese key/token behavior. Validate each collection against its content.
- [x] Add optional english {games,variants} and prefs.wordLanguage; validate using core and variants with English banks; isolate collections in app selection.
- [x] Add independent native Words selector, settings, bilingual text, language-aware stats, friend preview and print selectors/history.
- [x] Test all modes, isolation, backup corruption, old fixtures and friend round trips before accepting implementation.

### Task4: Integration/release
- [x] Add assets to HTML, worker, offline verification and deploy allowlist; synchronize release1.4.0 and hashes.
- [x] Run all Node/Python checks and browser suites, inspect print output, document exact evidence and limitations; fresh scoped review.

## Implementation record
Separate English collections retain original PT identities; English nextFree is stored inside its collection. English friends use prefs.englishChallenge, with legacy prefs.challenge strictly PT-bound. Independent content/paper/integration reviews completed; fixes and actual verification documented in docs/VERIFICATION.md. No publication or commit requested.
