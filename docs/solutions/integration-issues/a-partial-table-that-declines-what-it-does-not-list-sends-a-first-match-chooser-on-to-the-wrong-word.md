---
title: "A partial table that declines what it does not list sends a first-match chooser on to the wrong word"
date: 2026-10-02
category: integration-issues
module: "core/routing.py suggest_tag, core/taxonomy.py vocabularies and named_folder, tagging/published.py choose"
problem_type: integration_issue
component: core_logic
root_cause: incorrect_assumption
resolution_type: code_fix
severity: high
applies_when:
  - "A lookup gains a second table for one source's vocabulary, and the first table goes on serving everyone else"
  - "The caller walks a list and takes the first entry the lookup accepts"
  - "The new table lists only the entries that were measured"
symptoms:
  - "A stricter rule reads as the conservative one, because a decline writes nothing"
  - "An album listing a specific word and then a broad one is written as the broad one"
  - "Every test of the new table passes, because each hands the chooser one word"
tags: [taxonomy, vocabulary, published-genre, choose, suggest-tag, decline, fall-through, r-799, r-796]
---

# A partial table that declines what it does not list sends a first-match chooser on to the wrong word

## Problem

R-799 gave the general catalogue a table of its own in the taxonomy, because
the buckets' aliases were written for the record shops and filed its Pop as a
dance genre. The table lists the catalogue's eleven measured top level words.

The first build made a declared table the whole answer: a word with no row
was declined. That read as the conservative call. A decline writes nothing,
leaves the file askable and names the word in the summary, where the aliases
could file an unmeasured word wrong for good.

The built in review drove it in one line. `published.choose` takes the FIRST
of an album's genres that maps. An album the catalogue lists as Electro,
Disco, Pop was written as `House / Funky House / Disco` before, through the
aliases. With Disco declined for having no row, the chooser went on to Pop,
which has a row, and wrote a disco track as a pop record.

## Cause

A decline is only harmless when it ends the question. Inside a first match
walk it does not end anything: it hands the decision to the next entry. So
"decline what the table does not list" was not "write nothing", it was
"prefer any listed word over any unlisted one", and the listed words are the
broad ones by construction, since those are what was measured.

Every test passed because each handed the chooser a single word.

## Fix

The table is asked first and a word with no row goes on to the aliases, as it
did before the table existed. The one fault the aliases have for this
catalogue, answering with the bare name of a bucket that files by source
genre, is closed by a rule of its own: on a copy that declares the table, an
alias's answer is written only when it names a folder,
`Taxonomy.named_folder`, the same function the loader holds a row's tag to.

## Next time

- Before making a new table exclusive, find every caller that walks a list
  through it, and drive a list whose first entry the table does not know.
- A test of a chooser hands it at least two words, in both orders.
- "Declines, so it is safe" is true of the last question asked and of no
  other.

## Related

`unmapped-genre-only-means-a-deliberate-decline-so-a-tag-alias-cannot-answer-it.md`
is the same resolver read and not driven.
`a-checker-that-reimplements-what-it-checks-drifts-and-stays-green.md` is why
`named_folder` is held to routing's own answer by a test over every string
the template declares.
`a-resolved-path-compared-with-equals-is-not-a-same-directory-test.md` was
already filed and was met again on this unit: the correction verb compared a
recorded path with the library root by name, and the second review drove a
folder typed in another case reading as outside the library. Grep
`docs/solutions/` for `resolve` before writing any path containment check.
