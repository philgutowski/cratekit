---
title: no real stack test holds the two warm up calls U344 added, and the reason for measuring energy from a file in the warm up is not measured
found: at round two of the review of #996, U344, 2026-11-23.
issue: no
---

**The mechanism.** U344 closed R-1491 by two calls: `features_from_path`
asks `warm.kernels()` before it decodes, and the warm up's own head also
measures energy from its file, so the restamp's and calibrate's measure
compile the same kernel specialisations a worker's head does. The first is
held by `test_the_energy_measure_asks_for_the_warm_up_before_it_decodes`
against a librosa stand in. On the real stack (librosa and soundfile),
dropping either call fails no test, since no test measures a worker's head
against the driver's restamp across two processes; that was measured by
hand (23 of 23 and 32 of 32 identical, against 21 of 23 and 19 of 32
before). The review dropped the warm up's file measure and found 10 of 10
files bit identical head against plain measure over fresh caches in both
orders, so `warm.py`'s reason for the file measure ("that path compiles a
kernel specialisation of its own") stands unmeasured.

**Cost today.** None measured: every comparison made on the branch agreed.
A later edit dropping either call fails nothing on any stack.

**Closes when:** a real stack test runs a head in one process and the
restamp's measure in another over a fresh kernel cache, in both orders, and
asserts the features bit equal; and either a measurement shows the file
measure is needed, or it is removed with that test green. Ledger only.
