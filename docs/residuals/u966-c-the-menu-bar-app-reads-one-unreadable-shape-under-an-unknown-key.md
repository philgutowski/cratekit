---
title: The menu bar app reads only one of the glance's two unreadable shapes under a key it does not know, and some failure paths have no test
found: at review round two of #1085, U966, 2026-11-25.
issue: no
---

**The mechanism.** `Glance.otherUnreadable` (`app/Sources/CrateEngine/Glance.swift`)
says a key this app does not know when its value is `{"unreadable": ...}`,
but not when it is a list holding such an item, the other shape
`status_glance._anything_unreadable` counts; such a glance reads `fail` with
no line naming the source. An unknown key whose `unreadable` member is not a
string fails the whole reading rather than being passed over. The `signalled`
case's standard error clause and the sort of the unknown keys are reached by
no test, and a failure line that carries a long standard error can be about
540 characters wide in a menu row that does not wrap.

**Measured cost.** Driven by review round two through a Python port of the
Swift (no Swift runs here) on glances written by hand: a newer engine adding
a list key at version 1 would give a `fail` icon and heading with no line
naming what failed. The producer, a newer engine, does not exist; the
current `status_glance.glance` builds a fixed key set, so the one candidate
driven does not produce it. The menu row's width was not measured on a Mac.

**Closes when:** the decoder reads both unreadable shapes under an unknown
key and passes over a malformed one, a test drives a signalled call with
standard error and two unknown keys, and the install card (#1088) reads a
long failure line on the Mac. Ledger only: maintainer facing until a newer
engine adds a key at the same version.
