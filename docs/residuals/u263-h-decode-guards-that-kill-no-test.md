---
title: Seven guards in analysis/decode.py kill no test when reverted
found: at the review of #692, U263, round one, 2026-11-12.
issue: no
---

**The mechanism.** The review's mutation rows removing `-nostdin`, the
libsndfile guard in `decode.duration`, the empty frames guard,
`TimeoutExpired` in the caught exceptions, and `env=binaries.subprocess_env()`
(the line that keeps opted in credentials out of ffmpeg's environment) each
killed none of 773 tests in round one; in round two `-xerror`, and the exit
code half of the failure condition alone, killed none of 46, since every
tested non zero exit also says something. Each was read and is correct as
shipped.

**Measured cost.** None measured. A later change that dropped one would
pass the suite: ffmpeg could read the terminal, an error could go on decoding past
itself, a silent non zero exit would be read, a damaged FLAC's length
could be asked of ffmpeg, an empty decode would reach the mix, a stuck
ffmpeg would fail the item as an internal error, and a credential could
reach ffmpeg's environment.

**Closes when:** a test drives each. Ledger only.
