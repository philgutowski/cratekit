---
title: The brief's process wide parse memo was built, measured to cost more than it saved, and narrowed to one test
found: at the build of #687, U258, 2026-11-12.
issue: no
---

**The mechanism.** The brief asked that "within one test process a source text
is parsed once however many guards ask". The first build did exactly that,
`tests/_parse_memo.py` holding every tree for the life of the worker. Measured
on the touched test files in the suite's own distribution, four workers, two
runs each: wall time 85 to 91 s on `main` against 97 to 99 s with the memo, and
peak worker memory about 200 to 290 MB on `main` against 410 to 970 MB. Every
swept tree is about 720 MB in one process, and the collector walking that many
live nodes made the permissive soft delete sweep slower, 19.5 s to 22.5 s alone,
which outside pytest was 19.7 s without the memo, 25.0 s with it and 17.9 s with
it and the collector switched off. The guards that share files across tests
spend most of their time in analysis, so retaining trees bought them nothing.

The memo now shares a tree only inside one test that opens a scope, and drops
it when that test ends. The reading of the brief recorded here: its goal, that
a guard stops repeating the reading and parsing that feed it, is met inside
each test, where the repetition was; its literal wording, across tests, is not,
on measurement.

**Measured cost.** None to a person using the verbs. A future card that wants
cross test sharing would have to beat the collector's cost first; this entry
says what it is.

**Closes when:** ledger only. It records a decision and its measurement.
