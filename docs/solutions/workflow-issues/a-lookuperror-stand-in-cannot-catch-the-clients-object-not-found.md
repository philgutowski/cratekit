---
title: "A LookupError stand-in cannot catch the client's ObjectNotFound"
date: 2026-09-18
category: workflow-issues
module: "src/cratekit/label/tidal_catalogue.py, tests/label_fakes.py, tests/test_label_tidal_catalogue.py"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "Production catches a live client exception and a fake exception that is a different class"
  - "The suite's not-found path raises only the fake's class"
  - "The live client raises a sibling under a different parent, not a subclass of the fake's class"
  - "A green battery is being taken as evidence that a live 404 is an unresolved seed"
symptoms:
  - "Dropping ObjectNotFound from the except leaves every test green"
  - "FakeArtistLookup raises LookupError, tidalapi raises ObjectNotFound, and ObjectNotFound is not a LookupError"
  - "A live missing artist would propagate instead of refusing the label"
related_components:
  - "label-catalogue"
  - "provider-session"
tags:
  - "fixture"
  - "exception-class"
  - "object-not-found"
  - "silent-failure"
  - "label-catalogue"
---

# A LookupError stand-in cannot catch the client's ObjectNotFound

## Context

R-351 made `TidalCatalogue.artist_for` resolve a seed of the form `id:<digits>`
through `session.artist`. The live client raises `tidalapi.exceptions.ObjectNotFound`
for a 404. The shared fake, `FakeArtistLookup`, raises `LookupError` so a suite
can drive that path without importing the client library.

## What happened

The first except caught `(LookupError, ObjectNotFound)`. The unresolved-id
tests planted `LookupError` (via the fake) and a `ConnectionError` outage.
They did not plant `ObjectNotFound`. Removing that class from the except
killed nothing, because nothing in the suite raises it.

The neighbour is
`docs/solutions/workflow-issues/a-string-stand-in-cannot-catch-str-of-a-provider-object.md`.
There the stand-in was already a string, so `str(artist)` stayed green. Here
the stand-in is already a `LookupError`, so catching only that class stays
green. Two fakes, one shape: the suite's type is not the production type.

## Why the source does not explain it

The except names both classes. A reader sees `ObjectNotFound` and believes
the live 404 is covered. Coverage is which lines ran. The fake never
instantiates that class, so the line that handles it never had to be the
reason a test died.

`LookupError` is also the wrong net for the fake. `KeyError` and `IndexError`
are subclasses. Catching the parent reads a parse failure as a missing id.
The fake should stay a *bare* `LookupError` (`type(exc) is LookupError`),
and the live 404 should be planted as `ObjectNotFound` itself.

## The rule

**When production catches a live client exception and a fake exception, the
suite has to raise both classes.** A fake that is "close enough" is the
R-379 string stand-in again: the green path is the stand-in's type, not the
producer's. Plant the live class. Catch the fake by exact type, not by
parent, when the parent has other children that are not absence.
