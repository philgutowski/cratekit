---
title: A ceiling or a cooldown met while an export batch is matched writes none of the batch
found: at the build of #699, U270, 2026-11-13.
issue: no
---

**The mechanism.** `export.cli.run_export_items` matches each track of a
batch of up to a hundred before it writes any of them, and a `jobs.Parked`
raised by the provider gate during that matching releases the whole batch.
Before U270 each track was matched and written as its own item, so the tracks
matched before the park were on the playlist and done.

**Measured cost.** Not driven. Reasoned from the code: no track is lost or
added twice, since nothing of the batch was written, and the resume matches
the batch again, its ISRC lookups read from the on disk ISRC cache where the
first run reached them. What is lost is the time of the matches made before
the park, at most a hundred. Whether a hundred matches can need more than the
command's ceiling of 500 calls, which would make every resume park at the same
batch, was not measured; the match makes one ISRC lookup a track and more only
for a row several releases carry.

**Closes when:** a live export reads its matches per track against the
ceiling, or a park during matching writes the tracks already matched before
it stops. Ledger only: the cost is time, never a write.
