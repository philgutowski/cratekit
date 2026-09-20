---
title: "The provider client reads a track's version only off an available track, so a withdrawn remix reads as the plain record"
date: 2026-09-20
category: integration-issues
module: "src/cratekit/modules/outbound/tidal_account.py"
problem_type: integration_issue
component: tooling
severity: medium
root_cause: logic_error
resolution_type: code_fix
applies_when:
  - "Code compares a tidalapi Track's version, isrc, key or bpm against anything"
  - "Several provider tracks are compared with each other and one may be withdrawn"
symptoms:
  - "A withdrawn extended mix agrees with a library row for the plain record"
  - "A test fake that always sets version cannot reproduce it"
tags:
  - tidalapi
  - version
  - availability
  - absence-read-as-evidence
---

# The provider client reads a track's version only off an available track

## Problem

R-356 chooses among several provider tracks sharing one ISRC by the library
row's artist, title and version. The first cut compared every track the ISRC
named. The built in code review pointed at the client's own source, and it was
right: at tidalapi 0.8.11, `media.Track.parse_track` reads `version`, `isrc`,
`bpm`, `key` and a dozen more fields inside `if self.available:`, and the class
default for each is `None`. A track the provider has withdrawn therefore arrives
with its title and artists intact and NO VERSION, whatever the catalogue says.

So for a row spelled `Sun Path`, with the ISRC naming a streamable radio edit and
a withdrawn extended mix, the withdrawn one read as the plain record, was the
only track that agreed, and was chosen: a heart on a greyed out track of the
wrong version, reported as a match.

## What made it hard to see

The suite's fake `Track` took a version argument and kept it. Nothing about the
fake was wrong as a description of an AVAILABLE track, and no test could fail.
This is METHOD's fourth pattern, a measurement taken on something authored
alongside the fix.

## Solution

`tidal_account._streamable` leaves a track whose `available` is `False` out of
the choice altogether, rather than comparing it. It is counted in the unmatched
reason. The fake gained `withdrawn()`, which sets `available` false AND blanks
the version, because that pair is what the client really hands out.

It was then driven against the client's own class with no network:
`tidalapi.media.Track(tidalapi.Session()).parse_track(obj)` over a mapping whose
missing keys answer `None`. Constructing a `Session` makes no request.

## Prevention

Before comparing any field of a tidalapi object, open `media.py` and check
whether that field is read inside the availability branch. When a fake stands in
for a client object, build one real object offline once and compare the two.
The neighbouring entry on `InvalidISRC` is the same lesson about the same
client: its names describe the happy path.
