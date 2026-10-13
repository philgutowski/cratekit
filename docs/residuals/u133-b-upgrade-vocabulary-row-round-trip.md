---
title: taxonomy upgrade asks a person to take a vocabulary row out and maybe write it back
found: at the review of #308, U133, 2026-10-12.
issue: no
---

**The mechanism.** A copy made before U133 files the word Jazz in
NonElectronic, and its `[vocabulary.deezer]` row `{ word = "Jazz", tag =
"Jazz" }` writes that word. `crate taxonomy upgrade` holds the Jazz bucket
until NonElectronic stops filing it, and a copy with the word out and the row
left does not load, so the verb refuses it before it can add the bucket.
U133's hold names the row and says to take it out with the word and write it
back after the upgrade if the new bucket's own words do not answer for it.
That is a hand round trip the verb leaves to the person, because the
upgrade only adds (U132) and cannot take words out and add a bucket in one
step.

**Measured cost.** For Jazz none: measured on the shipped template, the
catalogue's Jazz tags as Jazz with the row and without it, by the Jazz
bucket's own tagging word. For a future bucket whose own words do not cover
a row's word, forgetting the write back changes what that catalogue word
tags as. Not driven, since no shipped bucket has that shape.

**Closes when:** the upgrade plans a hand edit and an addition together, or
checks vocabulary rows against the copy with the candidate in place. Ledger
only: maintainer and attended facing, nothing lost.
