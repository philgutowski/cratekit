---
title: A full label build's estimate counts kept reads among the releases listed, so a kept release the verifier now drops still lowers the calls it shows
found: at the review of #410, R-1091, 2026-11-01.
issue: no
---

**The mechanism.** `estimate` in `src/cratekit/label/playlists_cli.py`
counts the listed releases whose kept read is fresh and takes them off the
calls the crawl gate shows, before the verifier has confirmed anything. The
build reads only the confirmed releases, so a release kept on one run and
dropped by the verifier on the next is counted as a call saved that the
build would never have made. The estimate already counts every listed
release, confirmed or not, so it was an overestimate before R-1091 and is
now less of one by that count.

**Measured cost.** Driven at round 1 on the fixture: the verifier answering
mismatch for one kept release on the second run, the crawl screen said six
read by an earlier run and the build reused five. Off by the count of kept
releases the verifier drops between runs, on a number the screen calls a
floor; the live frequency is unmeasured.

**Closes when:** the estimate counts kept reads among the releases it will
read, or says the count is of listed releases.
