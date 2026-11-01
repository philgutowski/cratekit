---
title: Only a native label landing with a manifest records each row's provider track, so a bridge landing's or a --label landing's batch is matched by ISRC
found: at the build of #331, U150, 2026-11-01.
issue: no
---

**The mechanism.** `label_filing.PROVIDER_KEY` is written by the native
landing from the manifest rows its files were tied to. A landing on the xml
bridge writes an intake file and records nothing of the kind, and a landing
given `--label` has no manifest to name a track. Those rows reach the INBOX
mirror through the ordinary matcher, by ISRC, and a row whose code ties two
agreeing releases is unmatched and named, the tie R-1032 records.

**Measured cost.** Not driven on the live library. A label batch landed that
way has its tied rows missing from its `INBOX <batch>` playlist, each named on
the gate.

**Closes when:** the tie break lands, or the downloader's own record of each
file's provider track reaches the landing. Ledger only.
