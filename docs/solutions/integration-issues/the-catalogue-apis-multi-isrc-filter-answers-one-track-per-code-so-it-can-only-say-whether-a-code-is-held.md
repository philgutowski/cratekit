---
title: "The catalogue API's filter on several ISRCs answers one track per code, so a batch can only say whether a code is held"
date: 2026-11-05
category: integration-issues
module: "src/cratekit/acquire/catalogue_api.py, src/cratekit/acquire/isrc_screen.py"
problem_type: integration_issue
component: tooling
severity: medium
root_cause: wrong_api
resolution_type: code_fix
applies_when:
  - "A lookup asks the official catalogue API about several ISRCs in one request"
  - "Anything reads a track's fields off a catalogue v2 answer rather than off the client library's track"
symptoms:
  - "A batch of codes comes back with one release per code where the same code asked alone names five"
  - "A choice among releases made on a batch answer is the provider's choice, not the row's"
tags:
  - tidal
  - catalogue-api
  - isrc
  - batching
  - absence-read-as-evidence
---

# The catalogue API's filter on several ISRCs answers one track per code, so a batch can only say whether a code is held

## Problem

U207 set out to look many ISRCs up in a few requests. The brief asked for a
read only probe first: does `GET /tracks` take several codes, how many, and
does `include` bring the artists and albums. No app credential existed in the
cloud container that built it, so the probe was the provider's own published
OpenAPI document for `https://openapi.tidal.com/v2` (version 1.10.224, read
2026-11-05 from the developer platform's API reference) rather than a live
request. The live read of one batch answer against the same codes asked one at
a time is owed at an attended sitting.

## What the document says

- `filter[isrc]` is an array of strings, `minItems` 1, **`maxItems` 20**, sent
  in the default form style as repeated parameters
  (`filter[isrc]=A&filter[isrc]=B`).
- Its description: **"When a single ISRC is provided, pagination is supported
  and multiple tracks may be returned. When multiple ISRCs are provided, one
  track per ISRC is returned without pagination."**
- `include` takes `albums` and `artists` among others, so a single code's
  answer carries the names `_among` and `match.read_row` read, in one request
  (U205 already asks this way).
- A track's attributes carry `title`, `version`, `isrc` (nullable) and
  `availability`, an array of `STREAM`, `DJ` and `STEM`, **marked deprecated in
  favour of `usageRules`**, "will be removed in a future version".
- A track's `isrc` may be null.

## Why it matters

A batch is not a faster lookup. One ISRC is often filed under a single, the
album cut and several compilations, and which of them a row means is decided
by `_among` from the row, the account's hearts and the file's album tag. A
batch answer hands back one release the provider picked, which is exactly the
positional choice R-572 refused. Splitting a batch answer back into per code
track lists, as a naive batching would, silently turns every multi release code
into the provider's pick.

What a batch CAN say exactly is whether the catalogue files anything under a
code: a code the answer names is held, and a code it does not name is filed
under nothing, the same answer a single lookup gives as an empty list.

## Fix

`AppCatalogue.isrcs_held(codes)` asks two to twenty well formed codes in one
request and returns the codes the answer names. `acquire.isrc_screen.Screen`
groups a plan's codes into such batches before its first lookup and keeps the
codes no answer named. A lookup of one of those is answered not found with no
request, and every held code is still asked alone, so `_among` sees every
release as before. The saving is on the codes the catalogue lacks: fifty such
codes cost three requests rather than fifty, and a library whose codes are all
held pays three extra.

Four readings keep an absence honest:

- An answer track whose `isrc` is missing or unreadable makes the WHOLE batch
  unavailable, since the code it answers cannot be told, and nothing in that
  batch is read as absent.
- A malformed code, or a spelling that is not its own fold, never enters a
  batch, so one bad code cannot fail the others and a lowercase spelling is
  never screened under its fold.
- A lone code is never screened, since its own lookup costs the same request.
- A failed batch marks nothing. A rate limit stops the screening for the run,
  and the gate has counted it as it counts any call. A gate park propagates.

## How to apply

Do not read track fields off a multi code answer, and do not treat a batch
answer as a code's track list. If the platform later documents that several
codes return every release, the screen can become a lookup, and that change
needs its own live probe.

`availability` is the field `_streamable` reads under the app. When the
platform removes it, every app answer reads as streamable (`None`), and a
withdrawn release becomes a candidate. Nothing in this unit fetches it another
way. If an answer starts arriving without it, move the read to `usageRules`
after a live probe of that field's values.
