---
name: review-queue
description: Work the adjudication queue: see what is waiting on a person, decide it, and undo a decision. Use when a verb reports items needing review, when someone asks what is pending or why a track was never taken in, when a rejected thing needs asking about again, or when verdicts have to move to another machine. Trigger words include review, verdict, accept, reject, pending decision, suppressed, cleared, export the queue.
---

# The review queue

The one place the product asks a person something. An item lands here when the
product could not decide alone, it waits, and the verdict is recorded against the
item rather than against the run that produced it. That is the whole point: a
decision survives the session that made it, and no later run asks the same
question again.

The queue is scoped to one library and coupled to its database, so a verdict is
visible from any process and any later session against that library, and is not
shared with a different one.

## Outstanding first, everything else on request

A plain listing shows what is OPEN. That is the default because re-entry after
quitting partway through is the normal case, and a listing that re-presented
settled items would make finished work indistinguishable from work nobody has
touched.

```bash
crate review list
crate review list --queue version-match --limit 20
crate review list --kind label-release --kind duplicate-recording
```

`--queue` names one adjudication surface, and the declared ones are
`version-match`, `fallback-source`, `genre`, `label-release`, `duplicates`,
`deletion`, `adoption`, and `path-repair`. `--kind` is the finer cut within a
surface and is repeatable. `--all` adds items that are already settled.
`--suppressed` adds only the ones a rejection is hiding, which is a different
question and gets its own flag for that reason.

Paging is by ordinal, not by offset:

```bash
crate review list --limit 200
crate review list --limit 200 --after 200
```

`--after` continues from the last ordinal the previous page showed. A position
rather than a count, so another process adding items between pages cannot shift
the window and make you skip one.

## One item, whole

A listing is a projection: identifier, queue, kind, ordinal, verdict, chosen
candidate. It deliberately omits the payload, because a large queue rendered with
every payload attached puts megabytes on standard output for somebody who only
wanted to know what was left.

```bash
crate review show rv_9c1f4a2b7e0d5386aa41c2f7
```

That gives the payload, the candidates with their option identifiers, the
recorded actor, and the timestamps. Identifiers carry the `rv_` prefix and are
derived from what the item IS, not from its position in a file, which is why two
producers proposing the same candidate land on one item instead of two.

## Recording a verdict

Two answers. `accepted` settles in favour of one candidate. `rejected` settles
against all of them and suppresses the item until somebody clears it.

```bash
crate review resolve rv_9c1f4a2b7e0d5386aa41c2f7 --verdict accepted --option accept
crate review resolve rv_9c1f4a2b7e0d5386aa41c2f7 --verdict rejected --actor curator
```

Take the value for `--option` from the candidates that `review show` prints. An
option the item does not offer is refused rather than recorded, because a verdict
pointing at a candidate nobody was shown is a decision about nothing.

A verdict is written once. Resolving an item that is already settled refuses and
names clearing as the way through, so two processes disagreeing produces a
refusal instead of a last writer wins. `--actor` records who decided and defaults
to `cli`.

## A hundred items, one decision

`--where FIELD=VALUE` settles every outstanding item matching a predicate. The
fields are `queue`, `kind`, and any payload field written with a `payload.`
prefix.

```bash
crate review resolve --where queue=fallback-source --verdict rejected
crate review resolve --where kind=label-release --where payload.confidence=low --verdict rejected --actor sweep
```

Four rules worth knowing before running one:

- An item identifier and `--where` are mutually exclusive. The two disagree the
  moment the predicate matches something else, so naming both is refused.
- `--option` cannot ride along with `--where`. Each item offers its own
  candidates, so one candidate identifier cannot mean the same thing across a
  subset, and accepting the flag then dropping it would leave a person believing
  a choice was recorded that never was.
- An empty predicate is refused. It would answer a whole backlog nobody looked
  at, and that is one keystroke away from answering a single queue.
- Already settled items are skipped rather than refused, including ones another
  process settles while the sweep is running. The sweep reports what it actually
  changed.

Preview with the same filters before sweeping. `review list` filters on queue and
kind, so a queue or kind predicate can be seen in full first. A payload predicate
has no listing equivalent, so check the reported outstanding count before and
after instead.

## Clearing, which is what makes a rejection reversible

A rejected item stays in the queue rather than being deleted. Deleting it would
let the producer offer it again on the next run, which is exactly the roll
forward this queue exists to end. Clearing revokes the verdict and puts the item
back in front of a person.

```bash
crate review list --queue genre --suppressed
crate review clear rv_9c1f4a2b7e0d5386aa41c2f7 --actor curator
```

Find the item with `--suppressed`, since a rejection is invisible to a plain
listing by design. Clearing an item that carries no verdict changes nothing and
returns it unchanged. On a cleared item the recorded actor names whoever reopened
it rather than whoever decided it, which is the useful answer for something
nobody has decided yet.

This is the answer to "I already said no to that, why is it back" in reverse: it
is back because somebody cleared it, and it stopped appearing because somebody
rejected it.

## Moving verdicts between machines

Export writes a versioned JSON document, settled items included, so the file
carries the decisions and not just the questions.

```bash
crate review export /path/to/queue-export.json
crate review export /path/to/genre-queue.json --queue genre
crate review import /path/to/queue-export.json --actor imported
```

Export refuses to replace an existing file. Name a path that does not exist yet.
That refusal is what keeps the verb out of the destructive class entirely, since
an overwrite would be a file write with nothing gating it.

Import never overwrites a local verdict. Where the file disagrees with a decision
already recorded here, the local verdict stands, the incoming one is reported as
a warning, and every other item still applies. Refusing the whole document would
let one disagreement block a hundred agreements.

Read the warnings, because a conflict is four different situations wearing one
name and the remedies differ. The local verdict stood and the incoming one was
dropped. The file carries a verdict this build has no representation for, which
is reported rather than read as undecided so a real decision is not discarded.
The item is not a shape this queue can take in, so nothing about it was applied.
Or the item came in and its verdict did not, because the verdict names a
candidate the item does not offer or another process settled it first.

Do not hand edit an export. It is a transport, not an editing surface, and the
format it replaces is one where a stray column break silently changed what
somebody decided. Export again rather than repairing a file by hand.

## Reading the result from a script

```bash
crate --output json review list --queue duplicates
crate --output json review resolve rv_9c1f4a2b7e0d5386aa41c2f7 --verdict accepted --option accept
```

Every verb here reports the same payload: the queue it was scoped to, the items
this invocation touched, and the count still outstanding. The outstanding count
is a query against the queue, never the length of the item list, so a fifty item
page out of a three hundred item backlog does not read as finished. An empty
result reports as a no-op rather than as a failure, which is what lets a script
tell "nothing to do" from "something went wrong".

## When it is not this queue

An empty queue usually means the producer has not run yet, not that there is
nothing to decide. Items are offered by the verb that found the ambiguity.

```bash
crate audit duplicates /path/to/collection.xml
crate adopt scan
crate repair paths --root /path/to/library
crate delete review
```

A gate on a long running job is a different mechanism. It stops one run and is
answered against that run, not against a persisted queue item.

```bash
crate run show RUN-IDENTIFIER
crate status
```

Use `run show` for outstanding gates and pending human action on a run, and
`status` for open runs across the library. If a verb is refusing rather than
queuing anything, that is configuration and belongs to the first run path
instead.
