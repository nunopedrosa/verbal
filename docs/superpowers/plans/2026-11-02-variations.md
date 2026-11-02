# Verbal Variations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task in this chat.

**Goal:** Implement all seven approved variations while preserving current classic games and backups.
**Architecture:** Add a pure variant engine and curated data. Keep classic games in their original collection; add optional validated variant records in the same atomic schema 1 value. Adapt the current UI renderer, keyboard, picker, backups, statistics and sharing to the active mode.
**Tech Stack:** Static Safari-12-compatible JS/HTML/CSS, Node tests, existing Bash deploy.
**Spec:** docs/superpowers/specs/2026-11-02-variations-design.md

## Global Constraints

- Preserve verbal:data:v1, schema 1, current classic answer banks and daily algorithm.
- Keep EN/pt-PT, Safari 12, local-only runtime, atomic guarded saves and explicit worker activation.
- All seven modes must be reachable, persistent, portable and usable offline.
- Shared controls and three unwrapped QWERTY rows; narrow letter-key width exception retained.
- No production deployment, push or unrequested data cleanup.

## Review Focus

- Malformed fragment/backup inputs preserve the active collection.
- Duplicate letter constraints and solved dual boards remain truthful.
- Progressive advancement cannot bypass a lost/unfinished stage.
- Language/mode/size changes and restore preferences preserve drafts correctly.
- New scripts and assets are included in complete offline releases/deployment inventories.

## Task 1: Pure rules and curated data

Files: public/variants.js, public/challenges.js, scripts/test-variants.cjs.
- [x] Write failing tests for all seven modes, link validation, terminal states and curated paths.
- [x] Implement deterministic rules, bounded vocabulary validation and curated theme/ladder data.
- [x] Run tests; reject guesses without mutation; leave classic core selection unchanged.

## Task 2: Additive persistence

Files: public/core.js, public/app.js, scripts/test-variants.cjs.
- [x] Test old backups, full new backups, corrupt variant states, combined limits and preferences.
- [x] Validate optional schema 1 additions through an explicit extension validator.
- [x] Retain a single atomic write and raw conflict guard; default older preferences to classic.

## Task 3: Mode navigation and play UI

Files: public/app.js, public/index.html, public/style.css, public/i18n.js, scripts/test-variations-browser.cjs.
- [x] Add failing browser checks for mode picker, game persistence and special actions.
- [x] Build mode selection, dual boards, clue input, ladders, progression, themes and explicit friend sharing.
- [x] Extend Help, stats, result sharing and accessible labels in both languages.
- [x] Verify compact layouts, offline play, source-conflict refusal and legacy regressions.

## Task 4: Release and review

Files: version markers, release/deploy manifests, README.md, AGENTS.md, docs/VERIFICATION.md.
- [x] Refresh the release to 1.1.0 and all inventories/hashes.
- [x] Run core/vocabulary/variants/worker/deploy/browser checks and inspect representative screenshots.
- [x] Independent review, fix actionable findings, record evidence and remaining device limits.

Local work remains reviewable and uncommitted; no automatic publication.

## Execution record

Tasks 1–3 implemented inline. Pure rules, vocabulary and worker tests passed. Browser exercised all seven modes, draft switching, five-stage progression, offline submissions, friend preview/resume, EN/PT, backup restore and offline reload. Final review returned three P2 edge cases: ladder start repeat, invalid friend preference payload and keyboard colours after checked restore from second board. Regressions added; correction wave complete. All three fixes passed their RED→GREEN regressions and scoped independent re-review. Classic/variation browser suites, quota/stale/import safety checks and actual deployment-profile tests passed. Work remains local and uncommitted.
