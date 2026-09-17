---
title: "A string stand-in cannot catch str of a provider object"
date: 2026-09-17
category: workflow-issues
module: "src/cratekit/label/sweep.py, tests/modules/test_labels.py, tests/label_fakes.py"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "A production field is filled with str of a provider attribute"
  - "The suite's stand-in for that attribute is already a string"
  - "A live run stored a memory address or a repr where a name belongs"
  - "A green battery is being taken as evidence that a stored payload is readable"
symptoms:
  - "Live review rows carry values like <tidalapi.artist.Artist object at 0x...>"
  - "Every test that reads payload artist still passes, because the fake assigned a string"
  - "str of the stand-in is the name, so a test that only checks the stored string cannot see the defect"
related_components:
  - "label-sweep"
  - "review-queue"
tags:
  - "fixture"
  - "provider-object"
  - "stringification"
  - "silent-failure"
  - "label-sweep"
  - "review-queue"
---

# A string stand-in cannot catch str of a provider object

## Context

The first live label sweep, 2026-09-17, offered 98 releases whose payload
artist was a Python object address. `sweep._artist_of` did
`str(getattr(release, "artist", "") or "")`. On this provider, `album.artist`
is an Artist object, and `str` of that object is a memory address.

The suite never saw it. `Album` and `FakeRelease` both take `artist` as a
string. `str` of a string is the string. Every green battery was a measurement
taken on a fixture whose type was not the production type.

The fix is not only to read `.name`. A stand-in whose `__str__` is the name
hides the defect a second time. The test that pins this uses an object whose
`str` is an address and whose `.name` is the artist.

## Guidance

When production stringifies a provider attribute, the test's stand-in for
that attribute has to be the provider's shape, not the stored shape. If the
stored shape is a string, the fake must be an object that would stringify
badly, and the assertion must be that the stored value is the name and is
not the object's repr.

## When to Apply

- A stored payload field is filled from a provider object.
- The suite's fake for that field is already a string or an int.
- A live run wrote a repr, a memory address, or a default object spelling.
