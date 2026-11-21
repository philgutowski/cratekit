---
title: The Discogs version miss names the maker's folded words, "(tale of)" or "(order)", not the maker as the file writes them
found: at the review of #882, U318, round two, 2026-11-21.
issue: no
---

**The mechanism.** `searchers._another_version` writes the named
versions' words, which `titles._naming_words` has folded: descriptions off
both ends, "and", "the" and a possessive dropped, accents off. "(Tale Of Us
Remix)" reads "(tale of)", "(New Order Remix)" "(order)", "(DJ Koze Remix)"
"(koze)".

**Measured cost.** Round two: 191 of 377 maker names read differently from
the file. Garbled, never false: the release named is the one refused.

**Closes when:** the note quotes the file's own version text beside the
words compared. Ledger only, a wording fix.
