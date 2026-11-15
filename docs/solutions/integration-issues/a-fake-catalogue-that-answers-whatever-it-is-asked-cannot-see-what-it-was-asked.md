---
title: "A fake catalogue that answers whatever it is asked cannot see what it was asked"
date: 2026-11-15
category: integration-issues
module: src/cratekit/tagging/searchers.py, src/cratekit/tagging/titles.py
problem_type: integration_issue
component: tagging
severity: high
resolution_type: test_fix
applies_when:
  - "A unit changes, or depends on, the query a catalogue or provider is sent"
  - "A fetch fake routes by URL prefix and answers the same page whatever the query says"
  - "A live sweep reports misses that the suite's recorded answers match"
tags: [discogs, beatport, query, fetch-fake, camelot-head, title-tag, u289, sitting-100]
---

# A fake catalogue that answers whatever it is asked cannot see what it was asked

## Problem

Sitting 100 measured 0 of 19 Discogs matches on library files whose title
tags carry the naming verb's `KEY - BPM - ` head, and 15 of 20 asked again
with the head off. The suite was green throughout: every Discogs fake
(`tests/test_discogs_searcher.py:routed`) answered its recorded search page
for any URL starting with the search endpoint, so the `track` field could
hold the head, the whole stem or nothing and the release still came back.
The matcher read the head correctly the whole time; only the question was
wrong, and no test could see a question.

## What to do

- **A fake for a search answers only the question a person would type.**
  `tests/test_discogs_question.py:typed_fetch` parses the query and answers
  a release only for an artist and track it holds, so a question carrying a
  head misses as the live catalogue does. Use it, or the same shape, for any
  test about what is sent.
- **Assert the request, not only the outcome.** Read the URL the fetch was
  handed (`discogs_questions`, `beatport_queries`) and compare it with a
  literal, written out, never computed by the code under test.
- **The question and the match are two readings.** `titles.question` is
  what a catalogue is asked, read past the head, the marker and the artist's
  own part; `titles.read_file` is what a row is matched against, the file's
  own text. Changing one is no change to the other, and a test of either
  says which it pins.
- **A title with no head is asked byte for byte as before**, so a fresh
  download's question is pinned by literal URLs (`FRESH`), never by a
  comparison of the new reader with itself.

## How to tell you are in this trap again

A live run disagrees with a green suite about whether a catalogue answered,
and every fake for that catalogue routes on the URL's prefix alone. Look at
the query a real file produces before trusting any recorded answer.
