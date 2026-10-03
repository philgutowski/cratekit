---
title: "The folder endpoint's totalNumberOfItems counts every kind of item, whatever includeOnly asks for"
date: 2026-10-03
category: integration-issues
module: src/cratekit/acquire/listing.py
problem_type: integration_issue
component: provider_listing
severity: high
root_cause: wrong_assumption
resolution_type: code_fix
applies_when:
  - "A provider listing is filtered on the server by a parameter such as includeOnly"
  - "The walk checks what it collected against a total the response declares"
  - "A fake endpoint written for the tests applies the filter to the count as well as the items"
tags:
  - tidal
  - cursor
  - declared-total
  - include-only
  - fake-fidelity
---

# The folder endpoint's totalNumberOfItems counts every kind of item, whatever includeOnly asks for

## The trap

The provider's `my-collection/playlists/folders` endpoint takes `includeOnly`
(`FOLDER` or `PLAYLIST`) and filters the items it serves. It does not filter
the count. On the author's account the root declared `totalNumberOfItems` 55
whether the request asked for folders, for playlists or for both, and served 26
folders, 29 playlists, or all 55.

R-878's cursor walk asked for folders only and refused unless it collected the
declared total. It collected 26 of 55 and refused on every real account that
holds a playlist at the root. Its suite was green, because the fake endpoint
written for it counted only the kind it served, which is the assumption the
code made, so the tests agreed with the code and not with the provider.

## The rule

A total a response declares is only comparable with an unfiltered walk. Ask
for everything, count every raw item served (by its `trn`) against the total,
then keep the kind wanted (R-887, `paginate_cursor(keep=...)`). And when a fake
stands in for a provider, take its counting rule from a live probe of the
provider, not from the code under test.

## How it was found

Only by running `crate label playlists` against the real account after R-878
landed. The probe that settled it walked the endpoint three times by cursor at
pages of ten, with `includeOnly=FOLDER`, `PLAYLIST` and absent, and printed the
declared total each time: 55, 55, 55.

## Related

`the-clients-playlist-parser-makes-a-network-request-of-its-own-so-parsing-outside-the-fetch-leaves-the-retry-ladder.md`,
the same walk's other trap. R-878, R-887 in the ledger.
