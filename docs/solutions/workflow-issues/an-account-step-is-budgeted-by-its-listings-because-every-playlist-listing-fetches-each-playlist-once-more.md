---
title: An account step is budgeted by its listings, because every playlist listing fetches each playlist once more
date: 2026-10-14
category: workflow-issues
module: "acquire/listing.py, core/provider_gate.py, organize account steps"
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "A sitting schedules organize, export or sync steps against the streaming account and has to say how long they take"
  - "An account read through the product's client runs past twenty minutes with nothing printed"
  - "The provider pace in the live config is being changed"
tags:
  - "account-listing"
  - "provider-pace"
  - "organize"
  - "live-sitting"
  - "timing"
related_components:
  - "tooling"
---

# An account step is budgeted by its listings, because every playlist listing fetches each playlist once more

## Context

Sitting 41 (2026-10-14, `docs/cutover.md` "Sitting 41") was given an hour for
four account steps. A plain read of the account root through the product's
client ran 24 minutes and was stopped. Instrumented, with every request
counted by path, the cost was not the folders but the playlists: 624
playlists cost 637 calls, 31 folders' playlists 648 calls, and 1,233 of the
1,285 were `GET /v1/playlists/<id>`, one per playlist parsed, against 53 page
requests. The provider gate paces every call at `provider.min_interval_s`,
one second by default, so a listing is eleven minutes and the pages are
noise. Filed as R-1016 with a card.

## Guidance

**1. Count the listings, not the writes.** `organize` lists the account when
it plans and again when it applies, so an account step is two listings before
its writes, and a read back is a third. At one call a second that is about
eleven minutes a listing; at half a second, five and a half. Sitting 39's 22
minute report and 45 minute apply of the filing step were this. A sitting that
has an hour has time for two or three account steps, not for a rehearsal and a
live run of each.

**2. The pace is a config line, bounded only below zero.** `[provider]
min_interval_s` in the live config; the validator refuses zero and negatives
and nothing else. Halved to 0.5 on 2026-10-14 on Phillip's ask, with the
previous file beside it as `config.toml.bak-2026-10-14-before-pacing`. 5,500
calls at that pace drew no rate limit answer, and the breaker still parks a
run on one. Check `provider_gate.json` for `rate_limited` and `trips` before
and after a change; the lifetime count was 166,884 calls and 0 of either.

**3. Run an account step under nohup with a pid waiter, and read its plan from
the envelope.** The harness ends a foreground command at ten minutes and a
background one at thirty; a listing alone can pass the first. The two phase
driver of sitting 41 (plan to an `act1.json`, read the gate's `shown` block,
then `run decide` as session and continue under `--run`) is the shape; a
driver that decides in the same breath as it plans, as sitting 39's did, is
fine once the digest was rehearsed and wrong when the plan is being read for
the first time.

**4. A rehearsal on a copy buys nothing for an account only step.** The copy
redirects the database and library state; the account is not copied, so the
rehearsal lists the same live account and shows the same plan, at the same
cost. Rehearse database writes. For account steps, read the live plan at its
gate.

## Why This Matters

A live sitting is planned against a clock, and a step whose cost is hidden in
a listing nobody counted is a step that runs past the hour with nothing
written, which is what happened twice at sitting 41 before the cause was
measured.

## When to Apply

Any attended or unattended sitting that drives organize, export or sync verbs
against the account, and any change to the provider pace.

## Examples

Sitting 41's root step: planned in 18 minutes and 33 seconds at half a second
(2,213 calls, two listings plus the debris copies' tracks), and its apply was
still in its second listing 17 minutes later when it was stopped, having
written nothing.
