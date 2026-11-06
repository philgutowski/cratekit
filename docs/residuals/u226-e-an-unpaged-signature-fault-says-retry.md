---
title: A provider client that cannot read a playlist with no window is reported as a wait to retry, and refuses a whole sync pair run
found: at round two of U226's review (#578), 2026-11-06.
issue: no
---

**The mechanism.** `acquire.listing.playlist_tracks_unpaged` turns a
`TypeError` from the client's `tracks()` into `ListingNotPaginated`, "the
provider client changed shape", at once rather than climbing the retry
ladder. Through the account adapter that is translated to
`unavailable-transient`, whose remedy is to resume the job to retry; through
`label_cli._listed` it is `label-playlist-unreadable`, which `crate sync
pair` does not leave out per pair, so one pair refuses the whole run.

**Measured cost.** Driven at round two on stand ins whose `tracks` requires a
limit: exit 41 with a retry remedy, and a sync of every pair refused for one
pair. The installed client, tidalapi 0.8.11, accepts the bare call, so the
producer is a client upgrade that changes the signature: 0 live candidates.

**Closes when:** a signature fault from the unpaged read carries the
adapter-broken remedy the paged walk's own `ListingNotPaginated` should, the
same rule for both. Ledger only.
