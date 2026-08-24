---
name: remove-tracks
description: Take tracks somebody removed from the collection and move their files to the system Trash, after a review and a separate confirmation, then read or lift the tombstones that record what was removed. Use when files are left behind by rows deleted in rekordbox, when somebody asks to clean up orphans or free space, when a question is what was deleted and when, or when a version that was deleted needs to become acquirable again, which is revoking a tombstone.
---

# Remove tracks

Two verbs and one direction of travel. `crate delete review` offers the files
behind rows that were removed from the collection and moves the confirmed ones
to the Trash. `crate tombstone list` reads the record those removals leave
behind and lifts one when a deletion is regretted.

```bash
crate delete review
crate tombstone list
```

Removing is the one workflow where being slow is the feature. Everything below
is an argument for a step that exists to make the pass refuse rather than
proceed.

## A file goes to the Trash and nowhere else

A confirmed removal is a rename into the system Trash. Nothing is unlinked, no
database row is created, edited or deleted, and no streaming service is
consulted, because a deletion here is a fact about this disk. The pass opens the
database, reads it, and closes it.

That also explains an absence that looks like an omission. Every other
destructive session in this product captures the database first. This one has no
row to protect, and a capture of a database does not hold a music file, so it
takes none. The session is still recorded, and the listing says so plainly:

```bash
crate restore list
```

A deletion session shows up there marked as recording no capture, so there is
nothing to restore. What reverses a wrong deletion is the Trash itself, plus
revoking the tombstone so the version can be acquired again.

## The order, and why it is this order

```bash
crate doctor
crate delete review
```

The health check first, because this verb declares four preconditions and one of
them is unique to it. The volume has to be mounted, its recorded identity has to
match, that volume has to have a usable Trash, and rekordbox has to be closed,
application and background agent both. rekordbox is the application most likely
to be open here, since the natural way to reach this verb is to remove tracks in
rekordbox and then run it, and a library open in rekordbox holds rows in memory
that the file on disk does not show. Every one of those checks is asserted again
immediately before the first move rather than only at review time.

Volume identity is the check worth understanding. A restored clone of the
library mounted where the real one belongs is internally consistent all the way
down, its rows resolve and its sizes match, and the files this pass would trash
are the backup the recovery story depends on. No other check can catch that,
because all of them are evaluated against whatever is mounted.

## A first run baselines instead of presenting history

The pass tracks how far it has read using rekordbox's own update sequence, held
against the identity of the database it was taken from. On a library that has
never run this verb, the first run records that position, reports how many prior
removals it passed over, and offers nothing. That is deliberate. Presenting a
whole library's worth of old removals as though they had just happened is how a
person approves a hundred things they never looked at.

Rebuilding a library from an export produces a database whose counter starts
near zero. The recorded identity is what catches that, so the pass re-baselines
rather than reporting nothing to do forever while removals pile up invisibly.

## What is offered, and what is only reported

Only a candidate proved unreferenced and proved to be the file the row described
is offered. Everything else is reported and never asked about, because there is
no question a person can answer, and offering it would train somebody to approve
things the software has already said it cannot prove. The other answers are the
path resolving nowhere this machine can name, the file being the same file an
active row points at by inode, the file not being the size the removed row
recorded, a playlist still pointing at it, and the file already being gone.

```bash
crate --output json delete review
```

Read those categories rather than working around them, since each one clears
through a different act: fix the volume prefix map, work out which of two rows
is the mistake, find out why the file changed size, or take the track out of the
playlist. A row that is not finished business does not get passed over, so
fixing the cause and re-running brings it back.

## The confirmation is a separate recorded act

The gate is explicit, which means it cannot be answered inline on the invocation
that discovered it. Supplying `--decision` there is refused on purpose, because
a gate that one more flag satisfies is a gate that eventually gets satisfied by
habit. The first run refuses with a decision-required exit and leaves the run
resumable, naming the run and the gate.

```bash
crate delete review --actor operator
crate run show RUN-ID
crate run decide RUN-ID delete.review.confirm trash --actor operator
crate --run RUN-ID delete review --actor operator
```

The options are `trash` and `abort`, and aborting is a no-op that moves nothing.
The recorded decision carries a digest of the plan it was made against, taken
from what the run offered rather than from anything typed, so a resume against a
set of removals that has since changed refuses as stale instead of trashing
files nobody reviewed. Re-run the verb for a fresh offer when that happens.

Two more refusals belong to the destructive session rather than to this verb.
It needs a recorded backup acknowledgment of this library, and it will not open
while an earlier session is unresolved or a restore is unreconciled. Both name
the action to take, and neither is something a flag on this command can answer.

## Keeping a file that is offered

Answering the gate with `trash` accepts every offered item that has no verdict
yet, so a file to keep has to be settled before the confirmation.

```bash
crate review list --queue deletion
crate review show ITEM-ID
crate review resolve ITEM-ID --verdict rejected --actor operator
```

A rejection records a decline, which suppresses that row rather than that
version, and the pass deliberately does not retire the row. Retiring it would
be a one way door, and a decline is revocable, so the revocation would have
nothing left to reach.

## Tombstones, and what they answer

Every completed deletion writes one. It identifies a version rather than a
recording, artist and title with the mix name composed into the title, so
deleting a remix never suppresses the original. An acquisition pass consults it
and reports the suppression instead of quietly omitting the track, which is the
answer to why an intake or a label sweep stopped bringing something back.

```bash
crate tombstone list
crate tombstone list --all
```

The default listing is what is suppressed now, which is the ordinary question.
`--all` adds records somebody already revoked, which is the auditing question,
and it is the only way to tell a version nobody ever deleted from one somebody
deleted and then changed their mind about.

Read `trashed_to` first. Empty means this pass moved no file, and that is a
statement rather than a gap: the row was confirmed, the file was not at its
recorded path, and the record says a deletion happened by somebody's hand. The
listing also carries the version, the spelling the identity rules did not
believe, the recording code, and the identity scheme that composed it. Those
four are the whole answer to why a tombstone missed a track it should have
matched, and an empty scheme means a record written before the stamp existed.

## Making a deleted version acquirable again

```bash
crate tombstone list --revoke SUPPRESSION-ID --actor operator
```

Revoking lives on the listing verb because the two are one act with a pause in
the middle. The identifier is derived from the record itself, so the listing is
the only place to get one, and a separate revoke verb would be a command whose
only legal input is another command's output.

The same flag lifts a decline, so nobody has to know which of the two stores an
identifier came from. The difference shows up afterwards. Lifting a decline also
reopens the review item it settled, so that file is offered again on the next
pass. Lifting a tombstone does not, because no item in the queue is holding it,
and the version simply stops being suppressed for acquisition. The listing
printed after a revoke includes revoked records whether or not `--all` was
given, since the record just acted on is the one worth seeing.

## When a confirmed file does not move

The apply rebuilds the plan from scratch under the session lock and re-runs the
same categoriser rather than trusting what the review was built from. A verdict
is durable by design, so days may have passed and the track may have been
re-imported, restored over, or added to a playlist in the meantime.

A candidate whose re-check no longer holds is reported and skipped, because that
is a fact about one track. A move the filesystem refuses stops the pass, because
that is a fact about the disk and the next file will meet it too. Neither loses
work. Each file already moved has its tombstone written with it, and the read
position only advances at the end, so a re-run sees the moved files as already
gone and picks up the rest.
