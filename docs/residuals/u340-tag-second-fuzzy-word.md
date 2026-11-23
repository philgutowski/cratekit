---
title: tag second takes a word by any tier the resolver has and its gate never names the folder it means
found: at the review of #989, U340, 2026-11-23.
issue: no
---

**The mechanism.** `assert_genre_files` and `routing.files_by_genre` accept a
word any tier but the fallback resolves, the fuzzy tier included, and the
`tag.second.confirm` gate lists the word as typed, not the folder it files.

**Measured cost.** Driven at round one: `crate tag second "Soulful House"`
filed the tracks into NonElectronic / Rock, and `crate tag second disco` into
Nu Disco / Indie Dance / Med (fuzzy), where `Disco` resolves exactly to
another bucket. The adopt apply gate lists the bucket before any database
write, so the slip is visible before a membership is written; the file keeps
the word as typed.

**Closes when:** the gate shows each row's folder beside the word, or the verb
refuses a word reached by the fuzzy tier. Ledger only.
