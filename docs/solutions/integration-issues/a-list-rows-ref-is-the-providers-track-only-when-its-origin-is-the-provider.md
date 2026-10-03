---
title: A list row's ref is the provider's track only when its origin is the provider
date: 2026-10-03
category: integration-issues
module: src/cratekit/acquire/match.py
problem_type: integration_issue
component: tooling
severity: medium
root_cause: wrong_assumption
resolution_type: code_fix
applies_when:
  - "A verb reads a list through match_cli.read_list and hands a row's identifier to the streaming account or the downloader"
tags: [outbound, list-document, provenance]
---

# A list row's ref is the provider's track only when its origin is the provider

## Problem

R-837's `export set` reads a tracklist or a list document and makes a playlist
on the account. The first build took any row carrying `Wanted.ref` as the
provider track to add, skipping the ISRC and the search. The built in review
found it: a list document of origin `spotify` fills `ref` with each row's
Spotify identifier, which would have been handed to the account, refused
there, and recorded as refused, so never asked for again.

## Cause

`Wanted.ref` is PROVENANCE, the identifier the row's own source gave it, and
`Wanted.origin` says which source that was. Nothing in the field's name says
so, and every reader that wants a provider track has to check the origin
itself. `acquire/listdoc.py` already does, `wanted.ref if wanted.origin ==
match.TIDAL else ""`, which is where the rule was found.

## Fix

`export set` uses `ref` only when `origin == match.TIDAL`, and a row of any
other origin goes to the ISRC and then the search. A test drives a Spotify
list document and asserts the row is searched for.

## The rule

Read `ref` as the provider's track only beside an origin check. A new reader
of `match_cli.read_list` that hands identifiers on should grep for
`origin == match.TIDAL` and copy it, not read `ref` alone.
