---
title: A guard the verb consults only when there is work is not proven by a live run with no work, so a first live no-op is not a first live run
date: 2026-09-23
category: integration-issues
module: "src/cratekit/write/naming_cli.py"
problem_type: integration_issue
component: recorded_path_resolution
root_cause: guard_never_reached_on_the_live_tree
resolution_type: code_fix
severity: high
symptoms:
  - "A verb that reached its gate at one attended sitting refuses before the gate at the next, over the same folder, with no change to the library"
  - "A refusal counts hundreds of collection rows nothing in the configuration can honestly map, and its remedy asks for a prefix rule"
  - "A guard's docstring names a shape it excuses, and the live data carries that shape spelled another way"
applies_when:
  - "A verb reads the collection, the database or the account only when its plan is non empty, and a sitting records the verb as having run live over an empty plan"
  - "A guard was written against a fixture form of a value, a colon pseudo-location, a demo track, and the live form of the same thing is spelled differently"
  - "A refusal's remedy asks a person to add configuration for rows that are not files"
tags:
  - "name-apply"
  - "dark-row"
  - "prefix-map"
  - "streaming"
  - "live-proof"
  - "r675"
  - "r500"
---

# A guard the verb consults only when there is work is not proven by a live run with no work

## Context

Sitting 7 ran `name apply --root` over 54 acquired files and reached the
gate with an empty plan (R-669). Sitting 8, after R-669's fix, ran the same
verb over the same 54 files and it refused before the gate over 582
collection rows (R-675). The library had not changed between the two.

## What happened

`_plan_for` reads the collection only when something would be renamed. An
empty plan never consults R-500's dark row guard, so the sitting 7 record
"ran, to the gate" said nothing about that guard, and the first live plan
with renames was the first time the guard ever saw the live collection. It
refused on 137 streamed tracks, which rekordbox 7 records as
`/v4/catalog/tracks/<id>/`, a slash path the resolver reads as unmapped with
no file behind it, on 437 tombstones under folders that are gone, and on 9
rows from another account. The guard's own docstring excused "a streaming
pseudo-location", meaning the colon form the fixture used. The live form is
spelled with a slash.

## The two lessons

**A verb's live proof is per path, not per verb.** When a verb takes a read
only on a non empty plan, an attended run over an empty plan proves the walk
and the gate and nothing after the read. The record should say which reads
the run reached, and a sitting that wants the guard proven needs a plan with
work in it. Sitting 7's "to the gate" was true and covered less than it
read as.

**A guard that refuses on absence needs the live population counted before
it ships.** R-500's guard was driven on fixtures that carried one dark row
each. The live library carries 582, and no honest prefix rule maps rows that
name no file, so the remedy the refusal offered could not be followed. The
first cut of R-500 made the same mistake one step earlier and the built in
review caught it on the demo tracks; the second cut moved the line to
"absent file" and the live library was still on the wrong side of it. The
question to ask of a guard that refuses on a row's absence is: how many rows
of the live collection satisfy this today, and what does the remedy ask of
each one.

## The rule that landed

A dark row refuses only when its file name is the name of a file the pass
would rename. A renamed volume or a moved mount changes a path's prefix and
never its leaf, so a dark row under another name cannot be any candidate
under another spelling. That is the narrowest rule that keeps R-500's
driven case refusing, and it needs no configuration for rows that are not
files.

## Also true at this seam

- The colon form `tidal:tracks:N` is `NOT_A_PATH` to the resolver and the
  slash form `/v4/catalog/tracks/N/` is `UNMAPPED`. Any guard that branches
  on the resolution and means "streamed" must handle both, or, as here,
  stop branching on it.
- The refusal now names the candidates in doubt, `could_name`, so a person
  sees which renames are at risk rather than which rows are dark.
