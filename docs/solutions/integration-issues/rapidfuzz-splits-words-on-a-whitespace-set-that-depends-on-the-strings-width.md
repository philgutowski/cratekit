---
title: rapidfuzz splits words on a whitespace set that depends on the string's width, so a sort done once must split the same way
date: 2026-11-12
category: integration-issues
module: src/cratekit/acquire/match.py
problem_type: integration_issue
component: tooling
severity: medium
root_cause: wrong_api
resolution_type: code_fix
tags: [match, approximate, rapidfuzz, token_sort_ratio, whitespace, nbsp, nel, u265]
applies_when:
  - "Precomputing what a rapidfuzz token scorer (token_sort_ratio, token_set_ratio) does to a string, to score it once instead of per pair"
  - "Any code that claims a Python split and a rapidfuzz split agree"
---

# rapidfuzz splits words on a whitespace set that depends on the string's width, so a sort done once must split the same way

## Problem

U265 made the approximate pass sort each library name's words once and score
the sorted forms with `fuzz.ratio`, which is what `fuzz.token_sort_ratio`
computes after its own sort. The first helper used `str.split()`, then a split
on Python whitespace minus U+0085 and U+00A0, after a scan of every code point
in plain ASCII strings showed rapidfuzz does not split on those two. The whole
matrix proof over odd spellings then found 18,219 pairs whose float differed,
every one a raw string holding U+0085 or U+00A0 beside a character above
U+00FF.

## What rapidfuzz does

rapidfuzz reads a Python string at its stored width (one, two or four bytes a
character), and its whitespace test differs by width, measured over every code
point with rapidfuzz 3.14:

- A string whose every character is below U+0100 is split on Python's
  whitespace except NEL (U+0085) and the no-break space (U+00A0).
- A string holding any character from U+0100 up is split on exactly Python's
  whitespace, those two included.

So no single regex agrees with the scorer; the split has to look at the
string's widest character first. `match._sorted_words` does that.

## Why it did not matter in the product, and still had to be exact

`fold` turns U+00A0 into a space (NFKD) and collapses U+0085 as whitespace, so
no recording token the matcher builds carries either. The helper is held to the
scorer on any text anyway, because the card's bar is bit identical answers and
the next caller may not fold.

## How it is held

`test_the_word_sort_splits_on_exactly_the_whitespace_the_scorer_splits_on`
checks every whitespace code point and every code point below U+3100 in four
shapes at every width, and
`test_every_pair_scores_the_same_through_the_sorted_form` carries raw tokens of
both widths with both characters. If a rapidfuzz upgrade changes its
whitespace, those tests fail rather than a score moving silently.

## The lesson

A scan that proves two tokenisers agree must be run at every string
representation the library distinguishes, not only on ASCII. A whole matrix
comparison over deliberately odd raw strings is what caught it; the realistic
and tie dense sets, all folded, never could.
