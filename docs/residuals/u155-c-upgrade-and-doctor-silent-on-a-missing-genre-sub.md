---
title: crate taxonomy upgrade and doctor read a copy without the shipped genre sub as complete once its schema version is raised
found: at the review of #336, U155, 2026-11-01.
issue: no
---

**The mechanism.** `core/taxonomy_upgrade.py` compares a library's copy with
the shipped template by whole `[[sub_class]]` and `[[bucket]]` entries, and by
design never changes an entry the copy holds. The shipped Minimal / Deep Tech
bucket gained the `Rominimal` alias and genre sub in U155, at schema version 5.
A version 4 copy is read as behind only by its version: `crate taxonomy
upgrade` raises it to 5, and doctor's `taxonomy.schema` then reads OK, "the
copy declares every class and bucket it ships", with no word about the alias
or the genre sub the copy still lacks.

**Measured cost.** Driven by the review: after the planner's text is written,
`load_taxonomy(after).bucket("minimal_deep_tech").genre_subs == ()`. Nothing is
false in either sentence, and the hand edit is named in `docs/GUIDE.md` and on
the attended card, but a DJ who trusts doctor is not told.

**Closes when:** the planner names a shipped genre sub absent from a bucket of
the copy, as a hand edit it will not make, in its gap and remedy sentences.
Ledger only.
