---
title: A cloud session cannot cut a release, because the proxy refuses tag pushes, the git tags API and the releases API
found: at the first release cut after #340, U159, 2026-10-28.
issue: no
---

**The mechanism.** `scripts/release.py cut` on a cloud container passed every
refusal (clean `main` equal to `origin/main`, a clean battery verdict on
00a8965), wrote 0.2.0 into both files and committed `release: v0.2.0`, and its
one atomic push of `main` and the tag was refused with HTTP 403, so neither
ref landed. A tag pushed alone was refused the same way, while a branch push
of the same commit was accepted. The REST fallbacks were refused as well:
`POST git/tags` answered "write access to this GitHub API path is not
permitted through this proxy", and `POST releases` answered "creating,
editing, or deleting releases is not permitted for this session type".

**Measured cost.** Driven, 2026-10-28: no v0.2.0 exists, `main` stays at
0.1.0, and the release commit sits only on the pushed branch
`cloud/release-v0.2.0`. The atomic push is what kept `main` from carrying a
version no tag names.

**Closes when:** a release is cut where tags and releases are permitted, on
Phillip's Mac with `scripts/release.py cut --bump <kind> --mac-battery`, and
the release skill and METHOD say a cloud session plans a release and hands
the cut to the Mac, as they now do. Ledger only.
