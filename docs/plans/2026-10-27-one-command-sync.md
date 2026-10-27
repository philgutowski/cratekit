# One command sync: from `crate sync` to filed and analysed in rekordbox

Written 2026-10-27 from sitting 47 (`docs/cutover.md`), at Phillip's request.
The cards below are the plan; this file is the reasoning and the build
order, so a session picking any one card up can see where it sits.

## The definition of done

Phillip runs one sync. His latest account playlists and hearts are
downloaded, run through the pipeline, and show up in rekordbox fully
processed: analysed on his standard settings, tagged, named, correctly
sorted into BY GENRE + ENERGY, in a logical folder on the volume, with
logical rekordbox playlist folders. He answers only questions no standing
rule answers, and those come batched at the end.

Most of the parts exist. What fails is the path between them.

## What sitting 47 cost

One sync pass, 116 tracks landed, 212 analysed. About three hours from
`crate sync all` (19:07Z) to the last grid checked, and 25 messages from
Phillip, plus five approvals in another session's terminal for messages
between the two sessions. His messages, in order, and what each was for:

| # | Phillip asked or answered | Why it was needed |
|---|---|---|
| 1 | what a sync includes | nothing explains the pass before it runs |
| 2 | `crate sync all` | the verb only queues |
| 3 | what do I do next | nothing drives the four queued jobs or says what follows |
| 4 | `crate acquire download` | a separate verb, which also only queues |
| 5 | I thought we backed up last night | a workspace hook's rescue backup age was confused with the library's |
| 6 | `crate intake land` | the session landed without the tail and stopped at the rehearsal rule |
| 7 | why no vox score | the tail (tag, analyze, restamp, name) had been skipped, nothing refused it |
| 8 | go | to run the tail |
| 9, 10 | status? twice | jobs run detached, `job list` prints nothing in human output |
| 11 | lower the cut to 3 | 80 of 116 scored exactly 0 |
| 12 | the folder structure | the landing does not land in `Processed_Tracks/<year>` |
| 13 | delete the lock file | two sessions shared one desktop control lock and one rehearsal copy |
| 14 | is this finished | a hold on the other session, with no signal |
| 15 | drive rekordbox and analyse | the one step Cratekit may not do |
| 16 to 22 | settings, Dynamic risk, smarter mode, grid history, run both, key twice | the dialog was on remembered settings that were not his standard; nothing checked the result |
| 23 | stop and start over | the run was on Dynamic; the mode control needs a held press |
| 24 | file the key card and the record | key agreement 98 of 212 |
| 25 | trace the session and card the friction | this plan |

## The friction, by kind

1. **Nothing drives the pipeline.** `sync all`, the intake jobs, `intake missing`, `acquire download` and its job, `tag folder`, `analyze run`, `analyze restamp`, `name apply` and `intake land` are each typed, each with an id copied from the last output. Skipping the tail is possible and silent. **#333 (U152)**, updated with this sitting.
2. **The rehearsal rule is a hand procedure.** A script outside the repository, a shared scratch copy, real files moved by the rehearsal and moved back by hand, and digests that never match because they hash the database path. **#342 (U161)**, **#343 (U162)**.
3. **Gates take two or four commands each.** Decide, then re-run with `--run`; the default actor is not the session. **#349 (U168)**.
4. **Answers that look like nothing or like failure.** Empty `job list`, a relative `--root` planning 0, one lossy refusal failing a 116 track download, 17 stale gates in status. **#350 (U169)**, **#351 (U170)**.
5. **The rekordbox visit is long and fragile.** Five selections, Reload Tags first, a dialog on the wrong settings, a control that needs a held press, no check of the result. **#344 (U163)** removes Reload Tags, **#347 (U166)** makes it one playlist, **#348 (U167)** checks it, **#354 (U173)** is the procedure, **#338 (U157)** decides Dynamic per track.
6. **Not sorted and not where expected.** Files land in `Music/<batch>` and need `shelve`; rows need a separate adoption. **#345 (U164)**, **#346 (U165)**.
7. **Quality the pass cannot fix on its own.** Vox zeros **#352 (U171)**, key agreement **#341 (U160)**, genre coverage **#353 (U172)**.
8. **INBOX is a flat run of playlists.** **#356 (U175)**, an idea for Phillip.
9. **The wrapper.** `/crate-sync` **#355 (U174)** chains it all and asks only new questions.

## Build order

```
U161 digest ─┬─ U162 rehearse ──────────────┐
             ├─ U163 row fields ─ U165 filed │
U152 driver ─┼──────────────────────────────┼─ U174 /crate-sync
U166 Analyze playlist ─┬─ U173 visit skill ──┘
U167 check ────────────┘
U164 land in Processed_Tracks, U168 gates, U169, U170: independent, any time
U157 dyn, U160 key, U171 vox, U172 genre (idea), U175 INBOX (idea): quality, in parallel
```

P1 is the critical path to the definition of done: U161, U162, U163, U166, U167, U173, U174, with U152 (already Ready). The rest is P2 or P3.

## Hard limits the plan keeps

- Cratekit never opens rekordbox and never writes a beat grid, tempo or BPM; the analysis stays rekordbox's, done in one attended visit.
- The live database is written only through gated, rehearsed verbs; the session approves on an equal digest.
- Label sync stays guided; outbound hearts stay behind their explicit gate.
