---
title: A 404 page on one track read inside the client's ISRC lookup reads the whole ISRC as filed under nothing
found: at the build of #561, R-1313, 2026-11-06.
issue: no
---

**The mechanism.** tidalapi 0.8.11's `get_tracks_by_isrc` reads each track the
ISRC answer names with its own track read, and skips one that answers a not
found it can decode, `ObjectNotFound`. A track read answered 404 with a body
that is not JSON raises the decode error instead, which the client does not
catch, so the whole lookup fails with the 404 three context links down. Since
R-1313 every reader of a not found reads that 404, so the account and the
catalogue answer the ISRC as filed under nothing and keep that answer for a
week, where the client meant to skip one track and return the rest. Before
R-1313 it was retried and failed as an outage, so a match was missed either
way; now it is missed for a week rather than until the outage clears.

**Measured cost.** Not driven against the provider. It needs a v1 track read
answered with a 404 page while the v2 ISRC answer names that track; whether the
provider answers 404 with a page at all is the attended measurement R-1313
left out of scope. Driven on the installed client only as the chain's shape:
the track read's decode error escapes `get_tracks_by_isrc` uncaught.

**Closes when:** the ISRC readers tell a 404 on the lookup itself from one on
a track it read, by the request the 404 answered (the HTTP error's response
URL names the v1 track path), or the attended measurement shows the provider
never answers a track read with a page. Ledger only: the reachability is
unmeasured and the cost is a match missed for at most a week.
