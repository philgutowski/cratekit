---
title: test_the_detector_asks_for_the_warm_up_before_it_decodes now depends on whether ffmpeg is installed
found: at the review of #692, U263, round one, 2026-11-12.
issue: no
---

**The mechanism.** The test stands in for librosa with a file that is not
there; since U263 a load failure on a file libsndfile cannot open goes on to
ffmpeg, so with the extra installed and ffmpeg absent the head answers
`skipped-no-decoder` and the test's expectation fails.

**Measured cost.** Driven by the review under librosa 1.0 with ffmpeg off
the PATH: the test fails. The suite already fails without ffmpeg by design
(`require_ffmpeg`), so no machine the suite is run on is affected.

**Closes when:** the test binds its decode at `decode.load` rather than at
the file. Ledger only.
