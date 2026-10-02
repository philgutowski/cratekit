# Guided label sync

Written 2026-10-02 from an attended brainstorm with the author. Every decision
below is his, made in dialogue with the alternatives in view. The board cards
cut from it are U107, U108 and U109, issues #246, #247 and #248, and each
issue is its unit's brief. This note is the reasoning behind them, read for
that and never for instruction.

## The problem

Following a label is meant to bring in its new music. Today it fills review
with back catalogue instead: 2,416 label releases waited in review on
2026-10-02, most of them old, and taking any of them is a chain of steps,
`review resolve` per item, then `label approved`, then a download. The labels
sweep also rides inside `sync all`, so a routine sync sweeps every label
whether the author wanted that today or not. The sweep records no cursor by
design (R-140, the `labels` entry in `src/cratekit/sync/sources.py`), so every
sweep lists the back catalogue again, and that is how the queue grew.

Solved means label music arrives only when the author asks for it, one decision
per label, and a no stays a no.

## What gets built

Label syncing leaves `sync all` and becomes its own verb. It walks the
favourite labels in the terminal, one at a time, and asks only about labels
holding releases the author has not been asked about. For each label it shows
the release count, the track count and an estimated size, and takes one of four
answers:

- **Download all new**, every new release from this label in this run.
- **Pick releases**, the label's new releases chosen one by one.
- **Not now**, nothing from this label this run.
- **Stop following**, the label leaves the favourites registry on the spot.

Answers are saved as they are given, so a session can stop at any label and
resume where it stopped. When every label is answered, one summary shows the
labels, releases, tracks, estimated size and estimated time, and a single start
runs the download on its own: paced through the provider gate, resumable, and
landing the way any intake lands.

The first run also offers, once, the label releases already waiting in review,
as a catch up under the same four answers. After that a label shows only what
is new since it was last asked.

## Decisions, each the author's

1. **A question covers what is new since that label was last asked**, chosen
   over the newest N every time and over everything waiting. A release is seen
   once and back catalogue never returns. A quiet label is not asked about.
2. **The four answers above**, all four offered.
3. **Not now moves the label's marker forward**, chosen over carrying the
   releases forward and over carrying them once. Every answer moves it, so
   nothing answered comes back. A skipped release is still reachable through
   `label import`. This is what keeps a backlog from rebuilding.
4. **The existing review backlog is offered once, in the first run**, chosen
   over retiring it unseen and over leaving it in review beside the new verb.
5. **Answer every label, then one go, then unattended**, chosen over a
   download per label as answered and over answering only with a later
   download command.
6. **Asked in the terminal, and drivable by an agent session**, chosen over an
   answer file and over a Claude only skill. The product must work for any DJ
   without Claude, and saving each answer as it is given is what lets a
   session relay each question as a multiple choice.

## What follows from them, stated in the synthesis and confirmed

- A per label marker, "last asked", is new. It reverses R-140's no cursor
  design for this source, deliberately: the sweep no longer only offers, it
  asks, and an answer is the event the marker records.
- The genre gate still runs before a label is asked about, so a release that
  does not fit the label's kind never reaches a question. The releases the gate
  already holds, 339 on 2026-10-02, stay held, `label held return` still
  returns one, and the first run's catch up covers only what waits in review.
- There is no "always download this label" answer. The author's standing rule
  is that a sync never downloads label releases without asking first.
- `sync all` stops touching labels entirely and makes no provider call for
  them. Its summary names the new verb, so a routine sync can never start the
  large download.
- A track the library already holds in another version goes to the match
  queue rather than downloading twice, as `label approved` does today.
- The first run's catch up is long, about 30 labels, some over a hundred
  releases, which is why resuming midway is a requirement.
- A newly followed label starts from its newest few releases, the
  `labels.offer_per_sweep` count, not its whole catalogue. A whole catalogue
  stays `label import`'s job.

## Out of scope here

- **The label manager**, making it easy to add and remove favourite labels.
  `crate label registry` already lists, adds, sets, removes, renames and
  adopts, as a command line verb. Making it easy is the next brainstorm. Stop
  following is the only manager act inside the guided sync.
- Deciding any label release on the author's behalf, by rule or in bulk.
- Changing the genre gate's rules or the label kinds.

## How the cards cut it

- **U107**, the asking half. The marker, the questions, the four answers, save
  and resume, the first run catch up, the genre gate before asking, stop
  following. Downloads nothing.
- **U108**, the go. The summary over every answer, the single start, the paced
  unattended download that lands as an intake. Depends on U107.
- **U109**, the cut from `sync all`. Its summary names the new verb, and the
  old `sync labels` path is retired. Depends on U108, so labels never sit with
  no way to download them.
