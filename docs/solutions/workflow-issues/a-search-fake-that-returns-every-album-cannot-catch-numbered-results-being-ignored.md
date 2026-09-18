---
title: "A search fake that returns every album cannot catch numbered results being ignored"
date: 2026-09-18
category: workflow-issues
module: "src/cratekit/label/tidal_catalogue.py, tests/test_label_tidal_catalogue.py"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "Production searches several queries and the fake returns the same hits for every query"
  - "A numbered compilation is what found an artist in the live catalogue"
  - "The suite asserts that the numbered queries were issued, and treats that as proof they were read"
  - "A green battery is being taken as evidence that numbered search results expand the roster"
symptoms:
  - "Dropping numbered compilation searches still finds the suite's compilation on the bare name query"
  - "FakeClient.search returns list(self.albums) for every query, ignoring the query string"
  - "A live compilation titled only as Label 042 would never reach the roster if production searched the name alone"
related_components:
  - "label-catalogue"
  - "provider-session"
tags:
  - "fixture"
  - "search-query"
  - "silent-failure"
  - "label-catalogue"
---

# A search fake that returns every album cannot catch numbered results being ignored

## Context

R-352 made `TidalCatalogue.artist_for` search the label name and numbered
compilations `001` through `079`. The live client returns different hits per
query. The shared fake, `FakeClient.search`, returned `list(self.albums)` for
every query so a suite could drive copyright matching without teaching the fake
about titles.

## What happened

The numbered query test pinned that `"Harbour Lights 001"` through `"079"` were
*issued*. Discovery tests planted one compilation on `FakeClient.albums`. The
bare name query returned that compilation, so production never had to read a
numbered result to put the credited artist on the roster. Removing numbered
searches still found the compilation, still issued 80 queries if the issuance
pin used the production helper as its expected list, and stayed green.

The neighbour is
`docs/solutions/workflow-issues/a-lookuperror-stand-in-cannot-catch-the-clients-object-not-found.md`.
There the stand-in was already a `LookupError`. Here the stand-in is already
the full album list. Two fakes, one shape: the suite's input is not the
production input.

## Why the source does not explain it

`album_search_queries` names the numbered titles. A reader sees `001` through
`079` and believes numbered hits are covered. Coverage is which lines ran.
The fake never made a numbered query the only way to see the compilation, so
the line that consumes that query never had to be the reason a test died.

Issuing a query is not reading its results. A pin that the 80 strings left the
client is a pin of the call list. A pin that a compilation exists only under
`"Harbour Lights 042"` is a pin of the read.

## The rule

**When production searches several queries, the suite has to make at least one
hit visible only under a later query.** A fake that returns the whole set on
the first call is the R-351 exception stand-in again: the green path is the
fake's answer, not the producer's. Filter by query, or key albums on the query
string.
