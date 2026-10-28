---
title: A fact taken out of a digest so a rehearsal can match must be pinned on the run, or the answer is freed of it
date: 2026-10-28
category: workflow-issues
module: "cratekit gates, native intake writes, copy rehearsal"
problem_type: workflow_issue
component: development_workflow
severity: high
applies_when:
  - "A gate's digest names a path, a file or another fact a copy rehearsal differs by"
  - "A session wants a rehearsal digest to equal the live one"
  - "The cutover or revert gate is given the same treatment as the native landing"
tags:
  - "digest"
  - "copy-rehearsal"
  - "gate"
  - "pinned-fact"
  - "decision-stale"
related_components:
  - "database"
---

# A fact taken out of a digest so a rehearsal can match must be pinned on the run, or the answer is freed of it

## Context

U161 took the database path out of the native landing's digest (R-922), so a rehearsal on a copy at another path could digest as the live plan. The suite was green and the change was one line. The review then drove what it cost: the digest is the only thing a recorded answer is checked against, so an answer given over the live file was honoured by a continuation whose config named a copy, and the row landed in the copy the screen never named.

## Guidance

A digest does two jobs at once: it is what two runs are compared by, and it is what one run's answer is bound to. Removing a fact from it for the first job removes it from the second. When a fact must be left out so two runs can compare equal, keep it bound within the run: pass it to `Gates.require` as `pinned`, which records it on `RunState.pins` while the gate is open and refuses the recorded answer `decision-stale` when the continuation reads another value or none. `land_cli.ask_then_write` is the worked example; it pins the file its handle opened.

Check both sides when you do it: the comparison must run before anything replaces the pin (the offer is overwritten on every call, the pin must not be), and a pin absent on either side is a difference, not agreement.

## Why This Matters

The equal digest rule is what lets a session approve a live write with nobody present. A digest that matches across runs because a fact was dropped, with nothing else holding that fact, approves a write to a target nobody was shown.

## When to Apply

Any change that narrows a gate's digest, and the cutover and revert gates' residual from U161 in particular, whose items digest the database and registry paths.
