---
name: restore-and-converge
description: Roll the library back to a recorded write session, and get a governed tree back to its declared membership afterwards. Use when someone wants to undo what a sync, an intake, or a routing pass did, when a drive was replaced and the database has to come back off the off machine mirror, when a verb refuses saying a tree is unconverged or that declared membership no longer matches the database, or when someone asks what a rollback would discard before they authorise it. Covers the session listing, the explicit confirmation and its digest, the mirror pull, the per tree convergence report, and the rebuild that is the only exit from an unconverged tree.
---

# Restore and converge

Putting the library back to a recorded write session, and putting a governed tree
back to what the declaration says.

Nothing here needs a skill installed. It exists because the restore is the most
destructive thing this product does and there is no undo for the undo, and
because the verb that reports on a damaged tree is deliberately not the verb that
repairs it.

## Read the history before spending any of it

The listing is free. It opens no session, takes no lock, and resolves no path on
the library volume, and that is a decision rather than an accident: "what could I
roll back to" has to stay answerable on a library that is busy, and on a machine
where the thing being decided is whether a usable history exists at all.

```bash
crate restore list
crate --output json restore list
```

Each row carries the session identifier, when it started, the workflow that wrote
it, and the per tree count of what that session created and updated. A row can
also carry a sentence saying its capture cannot be spent. Those rows are listed
on purpose rather than filtered away, because a capture somebody deleted by hand,
or that retention removed, is exactly the session a person is about to go looking
for, and dropping it answers their question with silence.

## What a restore replaces, and what it does not

The database and the state coupled to it, together, as one capture. Not the
values this product wrote into audio files on disk. A genre tag written during an
adoption is in no capture, and the ledger that adoption kept is the only
surviving copy of what those tags held beforehand. A restore does not put them
back, so losing the state directory loses that undo rather than just a log.

The session a restore opens asserts three things before it writes anything: the
library volume is mounted, the volume that answered is the volume that was
recorded, and rekordbox is not running. Expect a refusal rather than a partial
write when the drive that answers is not the drive that was recorded.

```bash
crate doctor
crate status
```

## Choosing a session, and naming what dies with it

Bare, it means the newest session whose capture is spendable, which is not the
same thing as the newest session. Name one to be exact.

```bash
crate restore run
crate restore run SESSION-ID
```

A restore that reaches back past a later session which committed destroys work
somebody did on purpose. That case refuses, and the way past it is to name each
of those sessions explicitly. The discard flag takes repeated identifiers and is
never a boolean, because a flag that says yes is an answer to a question nobody
read, and the set has to match what the refusal listed rather than merely be
non empty.

```bash
crate restore run SESSION-ID --discard LATER-SESSION --discard LATER-STILL
```

Walk it first. The dry run performs no step and passes through the same gates and
the same single session as the real thing, so it proves the refusals as well as
the plan.

```bash
crate restore run SESSION-ID --dry-run
```

## The confirmation is a separate recorded act

There is no `--yes` and no `--confirm`, in this verb or anywhere in the package.
The first invocation works out what it is being asked to do, offers the gate a
digest of that, records the run, and exits asking for a decision. The answer is
recorded against the run by a named person, and then the same run is continued.

```bash
crate restore run SESSION-ID
crate run show RUN-ID
crate run decide RUN-ID restore.run.confirm restore --actor NAME
crate --run RUN-ID restore run SESSION-ID
```

The run flag goes before the verb path because it belongs to the root parser. A
fresh invocation instead of a continued run mints a new run, meets the same gate
with nothing recorded against it, and refuses again.

What the digest covers is the restore's identity, the session, its recorded
change summary, the sessions being discarded, and whether the mirror is being
pulled. That is the value that moves when the world moves. A later session
committing between the offer and the answer changes the summary, so the digest
moves and the recorded decision is refused as stale rather than honoured against
a library that is no longer the one it described. Read the offer again and decide
again; there is no way around it, and the digest is the only thing standing
between an approval and a library it was never given for.

A second gate can fire mid run when the cloud sync state cannot be read. It is
answered the same way, against the same run.

```bash
crate run decide RUN-ID write.cloudsync.unreadable proceed --actor NAME
```

Nothing to restore still asks. An empty history is a plan a person can still
abort, and skipping the question there would make the library that most needs
asking the one that is never asked.

## When the volume itself is gone

The backup flag pulls the database back from the off machine mirror first, for
the case where the disk was replaced and no local capture survived it. The two
halves compose in one order only, and it is the order they run in: the mirror
lays down the database the volume lost, then the capture rolls that database and
its coupled state back to a recorded session. The reverse would restore a session
and then overwrite it with whatever the remote happened to hold.

```bash
crate restore run --from-backup
crate restore run SESSION-ID --from-backup --snapshot STAMP
```

The snapshot flag picks a dated snapshot other than the newest. The mirror flag
pulls the music and everything else the mirror carried rather than the database
alone, which is hundreds of gigabytes, which is why it is off by default.

```bash
crate restore run --from-backup --include-mirror
```

Both halves are reported separately, and that matters when only one of them ran.
A run that pulled a whole mirror and named no session is not a run that did
nothing, and the report says which half happened rather than reporting zero steps
over hundreds of gigabytes of transfer.

## Convergence is the question a recovery leaves behind

Once a tree cuts over to the database, the database is the only copy of its
membership. There is no export to re-import. Anything that puts the database back
to an earlier state leaves that tree short, and incremental sync will not close
the gap, because the files an older database no longer places are still on disk
and therefore still read as owned.

A restore this product performed is not the case to worry about. A capture is
atomic over the database and the record that tracks convergence, so the two go
back together and agree by construction. The case that matters is a database
recovered out of band, off the mirror after a drive failure or from a copy
somebody made by hand, where nothing this product wrote was involved and so
nothing it wrote can be trusted to have noticed. It is detected anyway, from the
database's own monotonically increasing update count: a count that went backward
is a database that went backward, and a row count that moved while that number
stood still is the same fact from the other side.

```bash
crate converge
crate converge --tree TREE-ID
```

## Reading the convergence report

Every check is one of three answers, and there is no fourth answer that looks
like the first: compared and matching, compared and differing, or not compared
with the reason it did not run. A library whose volume is unmounted, or whose
database this build cannot open, produces no comparison at all, and reporting an
empty comparison as a clean one is how a tool tells somebody their damaged tree
is fine. A derivation that produced zero placements is not converged either.

Three things worth expecting in the output.

- A tree still on the XML bridge reports not compared, because its membership is
  the export's and there is nothing here to hold against the database.
- A matching row can still name a dimension that was not compared. Nothing in
  this build reads the calibration file, so the analysis threshold is a value
  nobody supplied, and the report names what it therefore skipped rather than
  assuming it away.
- Naming a tree the registry does not govern is a refusal, not a clean report.
  "No such tree" and "that tree is fine" are the two sentences this verb exists
  to keep apart.

The report stays read only under every condition, including the one where the
record holding the convergence flags cannot itself be parsed. That is a finding
inside the report rather than the end of the run, because this is the verb
somebody is told to run when their library is already refusing writes, and a
diagnostic that died with the document would leave them nothing to look at.

The library status carries the same flags without needing a tree identifier
first, which is the faster way in when you do not know which tree is unhappy.

```bash
crate status
```

## Rebuild is the exit, and it is the only exit

An unconverged tree refuses that tree's writes and nothing else. A library can
hold one governed tree and five playlists somebody curates by hand, and a
damaged tree says nothing about the rest. The flag is cleared by the rebuild
engine and by nothing else, so there is no state file to edit and no flag that
waves it away.

```bash
crate rebuild --tree TREE-ID --actor NAME
```

The actor has no default and an empty one is refused. An actor nobody typed is
the product answering for the user, and this is a write to somebody's library
membership taken on a named person's say so. A rebuild derives that membership
from the declared sources and the library's own rows, keyed on stable identifiers
rather than on folder names, so a folder renamed in rekordbox converges rather
than being filed a second time.

A tree still on the XML bridge is refused rather than rebuilt, because the
membership written would be overwritten by the next import. Cut it over first.

## The rebuild is queued, so something has to drive it

Rebuilding a live tree is long work, so it is enqueued and driven by the engine
rather than swept inline in the shell that asked for it. That is what gives it a
record, a resume, and an answer to "what is it doing" from a session other than
the one that started it.

```bash
crate job list --state running
crate job show JOB-ID
crate job resume JOB-ID
crate rebuild --actor NAME --job JOB-ID
```

The job flag continues the work already queued under that identifier rather than
queueing a second record for one piece of work. A stalled rebuild is answered by
resuming it, never by starting a fresh one beside it.

## The order, at the end

Converge, rebuild what differs, converge again. The second report is the one that
says whether the repair landed, and that is a different question from whether the
rebuild's job succeeded.

```bash
crate converge
crate rebuild --tree TREE-ID --actor NAME
crate converge --tree TREE-ID
```

Then ask coverage separately. Convergence answers whether the tree holds what the
declaration says. Coverage answers whether the declaration reaches the whole
collection. A single reading of "did it work" collapses two different questions
into one, and the disagreement between them is the interesting result.

```bash
crate audit coverage --limit 200
crate route unplaced
```
