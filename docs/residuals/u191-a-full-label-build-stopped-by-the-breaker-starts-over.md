---
title: A full label playlists build stopped by the provider's breaker keeps nothing it read, so the next run starts the crawl over
found: at the build of #402, U191, 2026-10-31.
issue: yes
---

**The mechanism.** `crate label playlists LABEL` without `--releases` reads the
listing, then every listed release's tracks through
`catalogue.ReleaseTracks`, two provider calls a release, all in memory. A
breaker trip part way raises out of `_grouped` in
`src/cratekit/label/playlists_cli.py` and everything read is dropped, so the
next run lists and reads from the first release again. The same is true after
a clean read: the explicit gate exits, and the run that carries out the answer
reads the whole catalogue a second time. The brief's fourth requirement asked
for a resume or for the reason there is none.

**Why it is not built in U191.** A resumable read needs a store of release
reads that outlives the run, and a store like that has to decide how long a
read stays true: a release whose tracks the provider changed after it was
cached would be planned from the old rows, and the gate's digest would bind an
answer to a catalogue nobody read that day. That is a choice about what a
person approves, not about code, and it was not this unit's to make without
asking. U191 made the cost visible instead: over 500 estimated calls a full
build stops at `label.playlists.crawl` before any release is read, and a label
sync's releases reach the year playlists through `--releases` without the
crawl.

**Measured cost.** On 2026-10-31 a full build of Defected (12,368 releases
listed) spent 3,026 provider calls, met 43 rate limited answers and was parked
for 15 minutes before any plan was shown; the estimate now in front of that
gate is about 24,700 calls and nearly seven hours at the default pace, so a
full build of a label that size cannot finish inside one breaker window and
starts over each time. Not driven live in the cloud.

**Closes when:** a full build keeps its release reads per label in library
state, with a stated age past which a read is taken again, resumes from them
after a breaker trip or a gate, and shows on its screen how many reads were
reused and how old the oldest is. Earns an issue: a workflow a DJ needs, the
first full build of a large label, cannot finish (board bar c).
