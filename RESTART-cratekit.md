# Restart: Cratekit

Verified state only. How to work is `docs/METHOD.md`. Why the rules are what
they are is `docs/history/`. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**Last merged: U93, issue #138, `relay/138`, 2026-09-20.**
`analyze restamp` and `analyze vocals` take `--recursive` and queue a whole tree
as ONE resumable job, which CLOSES R-376 on its first arm and NARROWS R-409 to
the calibrate half. One invocation over the library root replaces the 343 leaf
folder invocations R-376 measured.
**ONE WALKER, IN A NEW FILE, `core/discovery.py`.** Both verbs carried an
identical one level `iterdir` scan and both needed the same recursive mode, so
the copy that would have had to stay in agreement is gone: `vocals/cli.py` has
no `_audio_in` and a test fails if one grows back.
**THE ITEM ID BECOMES A POSIX RELATIVE PATH, AND THAT IS FORCED RATHER THAN
CHOSEN.** `job_items` is keyed `PRIMARY KEY (job_id, item_id)`, `core/jobs.py`,
so a recursive walk keeping bare filenames fails the insert the first time a
library holds one track name in two genre folders, which is every library. The
brief called this a decision; the schema had already made it.
**THE DEFAULT IS UNCHANGED AND THE MODE IS FROZEN.** One level is still the
default, byte for byte, so every existing job, every existing resume and
`analyze calibrate` are untouched. The payload now records `recursive` plus the
two omission lists beside `folder`.
**`analyze run` DOES NOT GET THE FLAG.** Its last act on a track is a rename and
its resume marker is the Camelot head on the NAME. The parser rejects
`--recursive` on it and a test drives that.
**THE JOIN IS NOW A GUARD.** `Path(folder) / "/etc/passwd"` is `/etc/passwd`, so
`discovery.item_path` refuses an absolute or `..` id as a defect instead of
joining it. Both verbs' `_folder_and_path` route through it.
**WHAT THE WALK DOES NOT READ IS DECLARED, ON BOTH EXITS.** A directory symlink
is not entered, `followlinks=False`, which makes a loop impossible rather than
survivable, and `linked-folder-skipped` names the ones declined. `os.walk`
swallows an `OSError` without `onerror`, so a folder the process cannot list is
collected too and carries its own code, `folder-unreadable`, because it has its
own remedy. Both ride the RESUME as well as the queue, read back off the frozen
payload and never re-walked, since re-walking would report the tree as it is now
over a job queued against the tree as it was.
**The built in code review raised four findings and all four were driven.** The
swallowed `os.walk` error and the resume half were fixed, the single link case
read "1 folders" and both messages now inflect, and the symlinked FILE case was
pinned and filed rather than changed.
Battery: ruff clean, **9330 passed** and 1 skipped in 63 seconds, 9331
collected, scan clean. No new slow test, and no test identifier removed by this
branch, 60 added.
Mutation table, `docs/mutation/u93-recursive-analysis.md` with its rows file
beside it: **25 rows, the author's own, 24 killed and one zero, D8, promoted to
the full suite.** `followlinks=False` kills nothing because the explicit decline
prunes the link before `os.walk` reaches the question; its composite, D6,
removing the decline, kills 6, and both counts are in the table. The pair was
deliberately not mutated together, because that IS the symlink loop and it would
hang the suite rather than fail it. Three rows logged as dropped. An earlier
pass had a second zero, D19, which was a real test gap and is now one kill. Null
control at zero, baseline green at 9331, every restore verified against
`git show HEAD:`. The driver ran in the FOREGROUND and finished inside the tool
ceiling, because the subset rule keeps a killing row cheap.
Filed: **R-588**, a symlinked TRACK is an item and is tagged through the link
while a symlinked FOLDER is declined, which is what the one level scan always
did and narrowing it would change the default mode; **R-589**, the covered
keyword above; **R-590**, the real library pass has still never been run and
every U93 number is from a fixture; **R-591**, one intermittent in
`test_session_cli.py` seen once, not reproduced, not this unit's code. **None
meets the board bar, so none owes an issue.**
One learning, `docs/solutions/workflow-issues/`, widening a queued verb's item
from a name to a path is decided by the item table's primary key. `CONCEPTS.md`
gains "Frozen walk" and the Item entry gains its uniqueness clause.
**Main's highest residual number is R-591.**

**The session before: U95, issue #140, `relay/140`, 2026-09-20.**
`restore.plan` and `restore.run` derive every path from the directory the open
session authorises, which CLOSES R-20, REOPENS R-8 item 3 and NARROWS R-412. A
`Held` from `bare_metal_session` could be spent on nothing since 2026-08-02,
because both functions resolved from `cfg.library.root` and refused a session
authorising anywhere else, while the ledger recorded the capability closed.
**ONE HELPER, NO NEW PARAMETER, AND THE CHECK IS NOT RELAXED.** `_rooted(cfg,
held)` hands a library session its configuration back unchanged, the same
object, and hands a bare metal session a copy rooted at `Held.authorises` with
its database carried to the same relative position. It is the only place that
asks which guard issued the session. A library session handed a configuration
for another library still refuses, as it always did.
**RECORDED PATHS ARE RE-BASED, because a manifest written on the dead volume
names the dead volume.** The session record's capture path and all four path
fields of a capture manifest move from the configured root onto the target, by
the textual rule `config` already uses for containment, idempotently. Without
it a recovered capture refuses every file, or worse, aims the writes back at the
configured root.
**THE NEW GUARD IS `_assert_plan_is_authorised`, asked in `plan` and again in the
preflight.** Every step target is authorised AND a member of the re-derived
restorable set, and the companion staging directory is authorised AND sits
directly under the one staging store the rooted configuration derives.
**WHAT A PERSON MAY MEET: NOTHING YET.** No shipped verb composes a bare metal
session with a plan, and nothing brings a dead library's log and captures onto a
target. This unit is the seam. The verb and the mirror pull were out of scope
and are what R-8 item 3 and R-412 now say is open. One visible change: a bare
metal plan for an installation whose database is kept OUTSIDE the library root
refuses by name, `recovery-target-refused`, before anything is read.
**THE OLD BYPASS TEST CHANGED SHAPE AND STILL REFUSES.** It used to refuse for
authorising the wrong directory. It now looks for the session under the
replacement, finds nothing recovered there, and refuses for that, with the
refused library's whole tree asserted byte identical. The library path is pinned
by a golden generated from `main`'s `restore.py` before the change, after a hand
written one proved wrong in both an act name and the order.
**The code review raised ten findings. Seven applied, three filed.** The one that
mattered: the staging directory was checked for authorisation only, the
authorised directory itself passes that, and the closing step PRUNES THE STAGING
DIRECTORY'S PARENT, so a plan value staged at the library root would have handed
the prune the directory above the library. Filed: **R-585**, a spendable bare
metal session never takes the target library's own lock, **R-586**,
`list_sessions` cannot be asked through a session, **R-587**, captures name
their library by absolute path, so every capture is unspendable once the root
changes. **R-587 was DRIVEN, predates this unit, meets the board bar's third arm
and OWES an issue**, which no session has created yet because a number is not a
finding's until the entry is on `main`. R-585 and R-586 do not: no shipped verb
reaches them, and the unit that writes the bare metal verb owns both.
Battery: ruff clean, **9270 passed** and 1 skipped in 59 seconds, 9271
collected, scan clean. No new slow test.
Mutation table, four files under `docs/mutation/u95-*`: **25 rows, the author's
own, 24 killed on the first pass and one zero, B1, a test gap, re-measured at one
kill in `u95-b1`** after the moved plan test learned to compare decisions and
not only steps. Two rows logged as dropped and one as an equivalent mutant, null
control at zero in all four runs, every restore verified against
`git show HEAD:`. Twelve of the 25 have exactly one kill. `u95-notes.md` has the
rest. The driver ran in the FOREGROUND, split four ways so each run finished
inside the ten minute tool ceiling, the longest at 5:09.
One learning, `docs/solutions/integration-issues/`, a containment check admits
the directory itself and the operation reaches its parent. `CONCEPTS.md` is
unchanged.
**Main's highest residual number was R-587 at that merge.**

**The session before: U92, issue #137, `relay/137`, 2026-09-20.**
A file too large to decode is refused before vocal scoring, which HALF closes
R-408. `analysis/vocals.VOCAL_MAX_BYTES` is the source system's 250 mebibytes,
`is_oversize` is a stat and a comparison with no read, and the guard sits in
`vocals.analyse`, the one checking path `analyze run` and `analyze vocals` both
go through.
**REFUSED, NOT TAGGED ZERO.** The source system tagged such a file `voxlevel` 0
and this package cannot, because a zero here means the model heard the track and
found it instrumental. So it is a fifth named absence, `vocal-audio-too-large`,
beside the four that existed, and `_inactive` nulls the three vox fields, which
both `_finalize` and the restamp worker skip, so no tag is written and an
existing tag survives.
**THE GUARD SITS AHEAD OF THE MODEL LOAD, not merely ahead of the decode**,
which is the one call the brief left open. Oversize is a property of the file and
holds on every machine, while `vocal-model-unavailable` is a property of this box
and carries a warning saying an install will score these tracks, which is false
about a file nothing would ever decode.
**ONLY HALF OF R-408 IS CLOSED AND THE ENTRY SAYS SO.** `analysis/detect.py`
decodes the same file first, at its own rate, under no cap at all, in a worker
budgeted at 64 mebibytes, so on `analyze run` the big decode has already happened
by the time this guard is reached. That is **R-583**, it OWES an issue under the
board bar's third arm, and no session has created it yet because a number is not
a finding's until the entry is on `main`.
**WHAT A PERSON MAY MEET.** A live set in a folder comes back `inactive` with
`vocal-audio-too-large` in its item artifact and in `by_vocal_reason` on the
envelope, carries no `voxlevel`, keeps whatever vox tags it already had, and is
therefore absent from every "with vox" playlist. No envelope warning names the
count, deliberately, since no install fixes a size. A file exactly at the cap is
still scored: the comparison is strictly greater.
**The code review raised two findings, both real, both applied.** Neither was a
crash. Both were the gap between what the unit claimed and what it closes: the
module docstring claimed the whole of R-408, and the cap reads as a duration
while being a size. 250 mebibytes is about 25 minutes of 16 bit 44.1 kilohertz
stereo and about 8 minutes of 24 bit 96 kilohertz stereo, so a hi res extended
mix is refused as a live set, which is **R-584**.
Battery: ruff clean, **9254 passed** and 1 skipped in about a minute, 9255
collected, scan clean. No new slow test; the one this unit added at 11.9 seconds
was `missing_requirement` importing `panns_inference` and is stubbed.
Mutation table `docs/mutation/u92-author.md`: **9 rows scoped to this unit's new
guards, the author's own, all 9 killed**, two rows logged as dropped, null
control at zero, every restore verified against `git show HEAD:`. `u92-notes.md`
carries what the table cannot: five batches, two of them invalid on the
starvation shape, and which numbers came from which.
One learning, a second incident appended to the existing red baseline entry
under `docs/solutions/workflow-issues/`, because 25 failures in one file does not
look like starvation and rebuilding the driver's environment by hand is a dead
end. `CONCEPTS.md` is unchanged.
Filed: R-583 and R-584. **R-583 meets the board bar and OWES an issue.** R-584
does not: its reachability is unmeasured and the conservative option was taken.
**Main's highest residual number is R-584.**

**The session before: R-290 with R-225, issue #160, `relay/160`, 2026-09-20.**
How a queued job ended now decides how its verb exits, in every queued verb,
which CLOSES R-290 and R-225. Before it, a job a worker PARKED left every queued
verb with `outcome: ok` and exit 0, the block legible only inside `data.cause`,
so a wrapper or a sync pass read success while the provider had just walled the
account. A half failed job did the same in three shells, `master`, `acquire
download` and `acquire fallback fetch`.
**ONE MAPPING, `jobs.raise_for_state`.** Every shell that drives a job calls it
outside the branch that drives, so a job already failed on entry answers the
same way the second time it is asked. A blocked job raises `cause.JobBlocked`, a
cancelled one `cause.JobCancelled`, a failed one its own cause, and the
dispatcher reads the first two as `Outcome.BLOCKED` and `Outcome.CANCELLED`.
The second was declared from the start and had no producer until now.
**THE CAUSE WAS NOT THIRTEEN OMISSIONS.** Every shell had copied one predicate,
closed and carrying a cause, and `blocked` is an OPEN state, so no copy could see
it. A rule about job state that lives in a shell cannot learn about a state
added later.
**THE BIT RIDES THE EXCEPTION TYPE, and that has a cost.** Nothing on a parked
job's cause says parked, since the adapter's own slug also fails single items.
So any hop that rewords a refusal on its way out and builds a new
`CratekitError` turns blocked into failed. Retag did. Then `backup` did, one
merge later, on a `main` that moved while this unit sat unmerged, and it showed
up only as a cherry-pick conflict. `cause.rebuilt` is now the one owner of a
reworded refusal, retag, backup and intake go through it, and a static test
refuses the rebuild spelled by hand.
**THIS UNIT WAS BUILT TWICE.** The first sitting died on 2026-09-20 when the
machine ran out of memory with the mutation table unmeasured. Its commits are
kept under the tag `abandoned/r290-2026-09-20`. This sitting cherry-picked the
code, the tests and the spec, resolved `backup`, ran the review again and redid
the record with fresh numbers, because R-570 to R-574 had been given to other
findings in between. The tag can be deleted once this is on `main`.
**WHAT A PERSON MAY MEET.** `crate master --job ID` over a failed job exits non
zero. Any queued verb over a parked job exits with the cause's own code and says
`blocked`, with `resumable` false, because that field names the gate run and a
parked job continues through its verb with the job id. A cancelled job says
`cancelled` with exit 50. A refusal envelope carries no job data, R-580.
**The code review raised eight findings.** Five were code and were applied, each
reproduced first: the one owner above, the cancelled outcome, a blocked row with
no cause keeping the blocked type, `resumable` excluding a parked job rather than
trusting the cause's code, and five comments this unit made false. Three were
the record and the table, which this commit is.
Battery: ruff clean, **9246 passed** and 1 skipped in about a minute, 9247
collected, scan clean. Mutation table `docs/mutation/r290-author.md`: **25 rows
at the light cap, the author's own, all 25 killed**, two shell rows logged as
dropped, null control at zero, every restore verified against `git show HEAD:`.
Measured in two FOREGROUND passes of 511 and 473 seconds, the first stopped with
an interrupt before the harness ceiling and resumed from the sidecar, which is
the second of the two learnings below.
Two learnings are under `docs/solutions/workflow-issues/`, the one about an
outcome carried on an exception type being dropped by any hop that rebuilds the
exception, and the one about a red mutation baseline on a loaded machine being
starvation before it is a failure. `CONCEPTS.md` is unchanged.
Filed: R-580, R-581 and R-582. **None meets the board bar**, so none gets an
issue: nothing false is said by any of them, R-581's reachability is unmeasured
and R-582 has no producer. The issues OWED from earlier sessions are unchanged.
**Main's highest residual number was R-582 at that merge.**

**The session before: R-118 item 4, issue #171, `relay/171`, 2026-09-20.**
An unreadable credential presence index refuses instead of answering absent,
which CLOSES item 4 of R-118 and leaves the other four items open. The cost was
driven before it was fixed: with a credential in the keychain and its index
unreadable, doctor answered `credential.provider` FAIL, "not recorded
(provider-session) ... Recording it before the run is the difference between a
refusal now and a refusal after the first paid call", remedy
`authenticate-provider`. Every word of that is false about that machine, and the
act it names cannot move the file that refused.
**THREE STATES WHERE THERE WAS ONE.** `secrets._index_read` answers empty for
`FileNotFoundError` ALONE, because a fresh installation has no index and refusing
there would mean the product could not be set up at all. Any other `OSError`
raises a structured refusal naming the file, raised `from` the original so
`cause.classified` turns a permission into `path-permission-denied` with
`grant-path-access`, which is R-118 item 3's machinery doing what it was bought
for. Bytes that are not JSON, or a payload whose `recorded` key is not a list of
names, raise the same slug with a different sentence and keep
`repair-credential-store`. `cause.REASONS` declares `credential-index-unreadable`
on the reserved `PRECONDITION` code, the first structured refusal `core/secrets`
has ever raised: its other four failures are exception types of its own.
**A `CratekitError` RATHER THAN `CredentialIndexUnusable`**, the sibling type the
lock raises. That one is converted at both call sites that take the lock; the
READ has five call sites and a handler at none, so a bare exception would reach
the dispatcher's unstructured blanket and come out as `internal-error` with
"report this defect" over a person's own state directory.
**THE WRITE HALF MATTERED MORE THAN THE READ.** `_record_name` reads the existing
names and writes them back with one added, so an empty answer from a failed read
rewrote the whole index down to a single name.
**WHAT A PERSON MAY MEET.** Doctor's credential checks now FAIL naming the index
file and the act that repairs it, rather than naming a credential they already
have. `crate setup` writes a note for both legs instead of dying after
`config.save`. Nothing changes on a machine whose index reads.
**The code review raised two findings and both were applied.** The refusal
claimed nothing had been stored, over the one call path where the value HAD:
`_record_name` runs only after `keyring.set_password` and its read back have both
succeeded. The sentence about the two stores is now the caller's, three declared
constants, one per position in the cycle, the shape `_index_locked` already uses
for its `action`. And the wizard caught the refusal on the presence PROBE and not
on the WRITE, which reaches the same reader; `CredentialError` is not a
`CratekitError`, so none of the three handlers beside it saw that one.
**The fifth pattern, looked for one file over.** Six readers share the
`except (OSError, ValueError): return empty` shape. Four are caches whose empty
answer costs a re-crawl, `deletion.candidates` errs toward refusing, and one is
the same class: `acrcloud.Ledger._read`, the monthly recognition spend counter.
Its read half is argued in its own docstring and is harmless while
`Budget.monthly` is `None` everywhere; its RECORD half rebuilds the file from a
read that failed, which is the truncation this unit just removed from the
credential index. R-578.
Battery: ruff clean, **9127 passed** and 1 skipped in about a minute, scan clean,
11 of them new. Mutation tables `docs/mutation/r118-a.md`, `r118-b.md` and
`r118-c.md`, summary `r118-notes.md`: **18 distinct mutations and two
re-measures, 20 driver rows under the cap of 25, the author's own, all 18
killed**, null control at zero in each batch, every restore verified against
`git show HEAD:`, three FOREGROUND batches of 6 minutes 48, 6 minutes 41 and 4
minutes 26.
**The two zeros had one cause and it was a test gap, not an inert mutation.**
The remedy the unreadable branch declares and the exit code its slug maps to both
killed nothing, because every test reaching that branch reached it through
`PermissionError` and `cause.classified` discards the site's own slug and act for
a permission. An index path that is a DIRECTORY raises `IsADirectoryError`, which
no classification claims; a test drives that on a real filesystem and `r118-c`
then kills both. Carry that past this unit: a zero under a classification layer
may be measuring the layer.
Two learnings are under `docs/solutions/workflow-issues/`, the one about
`monkeypatch.undo` rolling back the autouse fixtures and running the rest of a
test against the real keychain, and the one about the citation rule's coverage
being contagious. `CONCEPTS.md` is unchanged.
Filed: R-578 and R-579. **Neither meets the board bar**, so neither gets an
issue: R-578's cost is unreachable until a monthly bound is configurable, and
R-579 costs a machine consumer one slug over a report whose code, message and
remedy are all right. The issues OWED from earlier sessions are unchanged:
R-572's, R-570's, R-563's, R-549's, R-523's, R-517's, R-515's, R-512's, R-482's
and R-477's.
**Main's highest residual number was R-579 at that merge.**

**The session before: R-356, issue #158, `relay/158`, 2026-09-20.**
An ISRC several provider tracks share is resolved by the row's own names, which
DISCHARGES R-356's closing condition and moves what it cannot choose to R-572.
`TidalAccount.match_track` takes the row's title and artist, and several tracks
under one ISRC go to `_among`: first the ONE track agreeing with the row's
artist, title and version, read by `acquire.match.read_row` on both sides, then,
when several agree, the ONE the account already hearts. Never by position. A
track the provider will not play is never a candidate, and a track nobody could
read stops a lone agreeing one from being chosen. Anything else stays unmatched
and `unmatched_reason`, an EIGHTH `RemoteAccount` member, says how many tracks
the ISRC named and how many agreed. The names are never sent to the provider.
**THE SEAM WIDENED, AND A NEW ACCOUNT IMPLEMENTATION MUST FOLLOW IT.**
`match_track(identity, isrc, title, artist)`, and `unmatched_reason(identity)`
asked straight after a None. `title` is the RELEASE title: `CollectionEntry.name`
carries the key and tempo head, which agrees with no provider title, so
`source.release_title` strips it through the declared template. `LocalTrack`
keeps the display title beside it, because an unmatched row is reported as the
library shows it. `tests/outbound_fakes.PROTOCOL_METHODS` carries the new member.
**WHAT A PERSON MAY MEET.** `crate export playlist` and `crate sync favorites`
match rows they used to report unmatched, and an unmatched row the provider has
several releases of now says so: each item report carries the sentence and both
envelopes list it under `progress.outbound.reasons`, as "Artist - Title (row N):
the ISRC X names 3 provider tracks, 2 of them agree ... so none was chosen". A
row the provider has never heard of carries no sentence.
**NOT MEASURED LIVE, AND THE AUTHOR EXPECTS THE LARGER HALF TO REMAIN.** A single
and its album cut are usually spelled alike, so both agree, and with neither
hearted nothing chooses. That is R-572, board bar (c). **Owed to an attended
sitting:** the same four track export and the same 109 row sweep R-356 was
measured on, to learn how many rows the two rules resolve.
**The code review raised ten findings, five applied and five recorded.** The
largest was read out of the client's own source: tidalapi reads a track's
version only inside `if self.available`, so a withdrawn extended mix arrived
with no version, read as the plain record, and the first rule would have chosen
it. The suite's fake always kept its version, so no test could see it; the fake
gained `withdrawn()` and the adapter was then driven against the client's real
`Track` class, parsed offline. Also applied: either reading of EITHER side's
title counts, the artist is compared as words so another order, a remixer only
the provider bills and a feat spelling agree while the guest alone does not, and
the reason names the row by artist and title rather than by number. Recorded:
the outage read as not found is R-477 already, and R-573 to R-576.
**The fifth pattern, looked for one file over.** `label.tidal_catalogue.tracks_for_isrc`
returns every track and chooses nothing, and its one caller,
`intake.missing_cli`, already keeps every identifier, so the shape is not there.
The shape IS in this file's own lone track branch, which returns one distinct
identifier whatever it is called: R-573.
Battery: ruff clean, **9113 passed** and 1 skipped in about a minute, scan clean,
29 of them new. Mutation tables `docs/mutation/r356-a.md` and `r356-b.md`,
summary `r356-notes.md`: **25 rows at the cap of 25, the author's own, 25 killed
and no zeros**, null control at zero of 9114 in each batch, every restore
verified against `git show HEAD:`, two FOREGROUND batches of 2 minutes 51 and 5
minutes 42, four considered rows logged as dropped with reasons.
The learning is under `docs/solutions/integration-issues/`, the one about the
client reading a version only off an available track. `CONCEPTS.md` is unchanged.
Filed: R-572 to R-577. **R-572 meets the board bar and its issue is OWED**, along
with R-570's, R-563's, R-549's, R-523's, R-517's, R-515's, R-512's, R-482's and
R-477's from earlier sessions. R-577 is one failure of an untouched test under
xdist, seen once and not explained.
**Main's highest residual number is R-577.**

**The session before: R-221, issue #159, `relay/159`, 2026-09-20.**
A queued backup says which kind of run it was, which NARROWS R-221 and does not
close it. `BackupOutcome` records `dry_run` and `outcome_payload` renders it, so
a rendered run says which kind it was from the run itself; `perform_backup` had
been writing that key on by hand, which made it correct where somebody
remembered and absent everywhere else. On the queued path the source is the
job's FROZEN PAYLOAD and never the command line, so `--dry-run` typed beside
`--job` cannot make a run that really copied report itself as a rehearsal.
**R-221 IS STILL OPEN AND THE HALF LEFT IS R-349'S.** Only the second half of
its closing condition was met, a driven queued rehearsal whose envelope says so.
The rotation warnings the worker built still reach nobody, because that needs a
way for a handler to return a report alongside its `Produced`, and that channel
is issue 102's closing condition word for word. `jobs.Produced` carries two
paths and `job_items.artifact` is one `TEXT` column, so there is nowhere for a
report to go today. The two warnings this verb already lifts are facts about the
CONFIGURATION, which the shell can ask again; the prune warning is a fact about
how the transfer went and only the claimed item knows it.
**WHAT A PERSON MAY MEET.** `crate backup run --dry-run` now says, at queueing,
when a second ask reports the open job, on a successful resume, and on all three
refusals a failed resume can raise, that the run copies nothing and publishes no
backup age and that the age a destructive session reads stays whatever the last
real run left. The sentence is spelled ONCE, in a tense true wherever it rides,
because it states a property of the job rather than of a moment. On the envelope
it is the warning `backup-rehearsal`; on a refusal it is an appended remediation
step, with the cause EXTENDED and never rebuilt. A real backup carries neither.
**THE DECLARED SURFACE IS WHY `dry_run` RIDES UNDER `progress`.** This verb
declares `job_state/1`, `cli.output` closes it at four fields, and the
conformance guard refused the first cut of the key beside them. That guard drives
one sample invocation per verb, so it sees the QUEUEING envelope only, and
driving the resume envelope through `envelope_problems` found `ages` already
shipping as an undeclared field. That is R-570, board bar (b), **its issue is
OWED**, and R-571 is the guard gap behind it.
**The code review raised three findings and all three were applied**, two of
them defects this branch introduced. The largest: `raise _with_rehearsal_step(exc, job) from exc`
is `raise exc from exc` on a real run, since the helper returns the same object,
and a cause that is its own `__cause__` truncates the chain `cause.classified`
walks, so a refusal over a permission error stopped classifying as one and told
a person to retry later instead of to grant access. The second was the fact file
read back, the verb's third refusing exit, left outside the rehearsal word while
its message says "the backup ran and the age it published cannot be read back".
The third was the guard: the refusal tests asserted through their own literals,
so a helper that REBUILT a plausible cause passed green while dropping
`retryable`, `detail` and `scope`. The comparison is now the same failure driven
without the flag, field for field plus exactly one step.
`_refuse` was renamed `_raise_refusal` in the hunts: this module already imports
`cause.refuse`, which builds and raises nothing, and two names a letter apart
meaning opposite things is METHOD's "one symbol meaning two things".
Battery: ruff clean, **9084 passed** and 1 skipped in 54 seconds, scan clean, 14
of them new. No new slow test, none of this unit's in the slowest eight.
Mutation tables `docs/mutation/r221-a.md` and `r221-b.md`, summary
`r221-notes.md`: **20 rows under the cap of 25, the author's own, 19 killed and
one zero**, null control at zero of 9085 in each batch, every restore verified
against `git show HEAD:`, two FOREGROUND batches of 5 minutes 39 and 3 minutes
32, four considered rows logged as dropped with reasons. The one zero is
maintainer facing and its own description PREDICTED it: `dry_run` against
`not publish` is unreachable while no caller passes `publish=False`. A second row
measured a real zero on a user facing surface, the twin branch saying it
unconditionally, which bought a test and kills after it; batch a was then re-run
whole rather than resumed, so every published row is measured on one tree.
The learning is under `docs/solutions/workflow-issues/`, the one about a helper
that can return its argument. `CONCEPTS.md` is unchanged.
Filed: R-570 and R-571. **R-570 meets the board bar and its issue is OWED**,
along with R-563's, R-549's, R-523's, R-517's, R-515's, R-512's, R-482's and
R-477's from earlier sessions.
**Main's highest residual number was R-571 at that merge.**

**The session before: R-185 with R-246, issue #157, `relay/157`, 2026-09-20.**
`crate tag retag` declares the one surface it writes and ends by naming the act
that reconciles the other, which CLOSES R-246 and NARROWS R-185. The registry
entry declared `writes` of `files` and `db_metadata` after the `GenreID` relink
`write/metadata.plan_genre_retag` performs; nothing in `src` calls it, because
`tagging/retag.plan_library` and `tagging/retag.apply_library` are named by their
own module and by nothing else. It now declares `files` alone.
**Dropping the cloud sync gate was forced, not chosen.** `tests/test_cli_contract.py`
refuses a verb declaring a decision its work cannot reach, in both directions, and
that gate binds to write intent on the guarded writer, which this verb never
acquires because it opens no database on any path. `name.apply` is the same shape
already landed, for R-165, down to keeping `rekordbox.pins`, which is R-568.
**R-185 ITSELF IS STILL OPEN AND ITS CLOSING CONDITION DID NOT MOVE.** The two
acts are still two acts and a caller for the database half is still what closes
it. What changed is that the person is told: `retag_cli.library_row_warning`
names one act, reload the folder's tags in rekordbox, carried on all three of the
verb's endings.
**The third ending is the one worth knowing about.** R-225 sends a job that
closed carrying a cause out through that cause rather than through an envelope,
so a warning attached to the resume reaches every run EXCEPT the interrupted one,
whose corrected files have stale rows exactly as a finished sweep's do. That is
the run R-185 is about. The refusal now carries the reload among its remediation
steps, gated on the same artifact count, and the cause is EXTENDED rather than
rebuilt so the origin trail is not shortened. The code review found this and the
tense of the message, which claimed a correction had happened on an envelope
emitted before the detached child looks at a file; both were applied.
**WHAT A PERSON MAY MEET.** `crate tag retag` now says, at queueing, at a
successful resume that corrected something, and on a half corrected refusal, to
select that folder in rekordbox and reload its tags. A resume that corrected
nothing says nothing, and neither does a refusal that wrote nothing.
**The code review raised three findings and all three were applied**, two of them
defects this branch introduced. The third was the record, written here.
Battery: ruff clean, **9070 passed** and 1 skipped in 77 seconds, scan clean, six
of them new. No new slow test. Mutation table `docs/mutation/r185-r246-author.md`:
**14 rows under the cap of 25, the author's own, 14 killed and no zeros**, null
control at zero, every row's restore verified against `git show HEAD:`, three
rows logged as dropped with their reasons. Two rows were re-run after the first
pass: one had deleted an `except` clause and left a bare `try`, which reported as
a collect error rather than a result, and the other measured a real zero on the
cause trail assertion, which bought a stronger one read back from the queue.
The learning is under `docs/solutions/workflow-issues/`, the one about a queued
verb having two exits. `CONCEPTS.md` is unchanged.
Filed: R-567, R-568 and R-569. **None of the three meets the board bar**, judged
per finding in the ledger, so no issue is owed for them. R-563's is still OWED,
along with R-549's, R-523's, R-517's, R-515's, R-512's, R-482's and R-477's from
earlier sessions.
**Main's highest residual number was R-569 at that merge.**

**The session before: R-289 with R-291, issue #167, `relay/167`, 2026-09-20.**
The tagging walk no longer descends into this product's own staging trees, and
the emptied staging of a job that can no longer run is reclaimed, which CLOSES
R-289 and R-291. `tag.audio_files` skips `tag.SKIPPED_DIRNAMES`, the two staging
directory names, matched against the components below the root, and
`tag.APPLEDOUBLE_PREFIX`, which is `._` and not `.`.
**R-289's closing condition was NOT met as written and that is deliberate.** It
asked for "the dot skip its neighbour has", the first cut did exactly that, and
the code review drove what it costs: `...And Justice For All` is an album
directory and `...Ready For It.flac` is a track, so a broad dot skip returned
nothing over a folder holding both and `crate tag folder` reported it held no
audio it could tag. The neighbour, `analysis/cli._audio_in`, still has that rule
and it is now R-563. The master staging tree is covered too, which it was not
before and which matters more, since it lands INSIDE the music library.
`acquire.cli.sweep_staging` reclaims the staging of jobs the queue reports
terminal, and only directories that hold NOTHING. The emptiness question goes to
`rmdir`, not to a listing, so a refused landing kept as evidence survives without
the sweep having to know which files are deliberate, and a directory naming a job
this queue does not hold is left alone. It runs at the HEAD of `acquire download`
and on both paths of `acquire fallback fetch`, which is the second writer of the
same tree; the fallback resume path reads the root off the job's frozen
configuration so it still loads no live config. `jobs.states_of` is new, two
columns for the names present in the tree, because `list_jobs` hydrates every row
it returns: measured at a median 54 ms over 500 succeeded jobs and 224 ms over
2000, each freezing a two hundred track list.
**WHAT A PERSON MAY MEET, two things.** `crate tag folder` over a download
staging root now reports `tag-folder-no-audio` where it used to queue the partial
downloads of a killed attempt and the refused landings, and a track whose title
opens with dots is tagged where the first cut of this fix would have dropped it.
And the staging tree under the download root stops growing by one directory per
item of every job ever run; the refused landing FILES still stay for good, which
is R-564.
**The code review raised four findings and all four were applied**, the first one
a defect this branch introduced: the dot skip above. The other three were the
fallback verb sharing the tree with no sweep of its own, the sweep asking
`list_jobs` for the whole installation to answer a question about a handful of
directories, and the module docstring still arguing the verb deletes nothing.
Battery: ruff clean, **9064 passed** and 1 skipped in 78 seconds, scan clean, 14
of them new. **Two different tests went red once each across six full parallel
runs on this branch and passed alone**, neither in a module this branch touches,
and that is R-566 rather than a fact about the branch. Mutation tables `docs/mutation/r289-a.md`, `r289-b.md` and
`r289-c.md`, summary `r289-notes.md`: 23 rows under the cap of 25, the author's
own, 19 killed, four zeros each with its line or composite, null controls at zero
on every batch, three FOREGROUND batches. Two of batch B's zeros were real holes
and each bought a test, re-measured in batch C and both kill.
The learning is under `docs/solutions/workflow-issues/`, the one about a skip
written against a shape. `CONCEPTS.md` is unchanged.
Filed: R-563 to R-566. **R-563 meets the board bar and its issue is OWED**, along
with R-549's, R-523's, R-517's, R-515's, R-512's, R-482's and R-477's from
earlier sessions.
**Main's highest residual number was R-566.**

**And before that: R-172, issue #155, `relay/155`, 2026-09-20.**
A rename the plan promised is never skipped in silence, which CLOSES R-172, and
both halves of its closing condition were done. The PLAN pass owns a collision:
several movers rendering to one target, or a target a file on disk holds that
nothing here is moving, are marked `collides` in `items`, carry their reason, are
counted under the new `totals.collides` and are left OUT of `totals.count`, so
that count is the number of renames that can actually happen. The detection runs
to a FIXPOINT, because holding a file back makes it an occupant, and the first cut
missed exactly that. A target another mover still holds is deliberately LEFT
promised, since sort order resolves that chain whenever it reaches the occupant
first. Targets are keyed through `_key`, NFC and casefolded, because the volume
this product ships for treats two names differing only in case as one.
The APPLY pass collects every rename it owes and did not perform, by name and
with its reason, and answers the new cause `rename-incomplete` at exit 30 through
`output.from_cause` on the PLAN surface, so the renames that did land are still
reported. Five bare `continue` branches became five named reasons.
**WHAT A PERSON MAY MEET, two things.** `crate name apply` now exits 30 over a
library holding two files that render to one name, where it exited 0 and renamed
one of them, and the cause names both files with the reason and the remediation.
And a file whose title tag could not be written after a successful rename is
outstanding too, named at its NEW path, where the answer `write_tags` returns was
never read.
**The code review raised six findings and all six were applied**, two of them
real defects this branch introduced: the collision pass asked once rather than to
a fixpoint, so three files in one folder produced a plan promising one rename that
no rename could satisfy, and the single collision worded remediation told a person
to hand rename a file over the four reasons that are not a collision. The other
four were the tag failure named at its pre rename path, the hand rolled
`output.build` that restated `from_cause`, the referenced check asked twice per
candidate, and the shipped naming skill plus the registry entry left undocumented.
**Measured against the naming engine, and it is why there is NO case only rename
branch here**: `parse_head` does not read a lowercase Camelot letter as a head at
all, so `05a - 120 - Song.flac` renders unchanged and is not even a candidate. A
target differing from its source only in case is unreachable. Filed as R-562.
Two pinned counts in `tests/test_reserved_causes.py` moved and were re-pinned with
their reasons, the cause population 168 to 169 and its non reserved half 141 to
142, and the kebab literals 464 to 465 with non keys UNCHANGED at 297.
Battery: ruff clean, **9044 passed** and 1 skipped in 81 seconds, scan clean, 11
of them new. Mutation tables `docs/mutation/r172-a.md` and `r172-b.md`, summary
`r172-notes.md`: 25 rows at the cap, the author's own, 25 killed, no zero, null
controls at zero of 9045 collected, two FOREGROUND batches.
The learning is under `docs/solutions/integration-issues/`, the one about a run
that did part of its work. `CONCEPTS.md` gains Held back and Carried out in part.
Filed: R-559 to R-562, none meeting the board bar today. **R-549's, R-523's,
R-517's, R-515's, R-512's, R-482's and R-477's issues are still owed** from
earlier sessions.
**Main's highest residual number is R-562.**

**The session before: R-222 with R-223, issue #154, `relay/154`, 2026-09-19.**
The archive rotation counts a RUN and not an attempt, and asking for a backup
twice is one job, which CLOSES R-222 and R-223. `_prune_archive` reads
`_rotation_floor`, the stamp of the last COMPLETED mirror to this destination,
taken from the files portion's published age. Every dated folder named after it
is HELD as one slot of the keep and the settled folders rotate newest first. It
works because the age is published only on success and only after the prune.
Reusing a stamp across attempts, the brief's sketch, had nowhere durable to
live: a claimed item has no scratch channel and `jobs.retry` clears the cause.
The floor also covers a NEW job filed after a failed one, which a per job stamp
would not.
**WHAT A PERSON MAY MEET, two things.** With no completed mirror on record for
the configured destination, which is every library on the day this lands and
any library after its destination is changed, the rotation purges NOTHING on
that run and rotates normally from the next one. And a second `backup run`
while one is open returns the open job's identifier with the warning
`backup-already-queued`, exit 0, naming the job's FROZEN mirror and archive
root. A rehearsal and a real run are still two jobs.
**The code review raised eight findings, six applied, all on the twin guard**:
whole payload equality, a bare `except Exception`, a message naming the live
mirror when the twin matched on the archive root alone, warnings computed from
the live configuration, no library comparison, and a full table read of the
queue. Not applied and filed: R-556 and R-557.
**A trap this unit nearly walked into, filed as the learning**: making the
rotation purge nothing with no record made the two tests that prove a rehearsal
never purges VACUOUS, green with their guard removed. Seven existing prune tests
now start from the `a_completed_mirror` fixture and dated names, because a word
like "one" sorts after every date and is held.
The kebab literal pin in `tests/test_reserved_causes.py` moved 463 to 464,
non keys 296 to 297, for `backup-already-queued`, a warning and not a cause.
Battery: ruff clean, **9033 passed** and 1 skipped in 87 seconds, scan clean, 29
of them new. Mutation tables `docs/mutation/r222-a.md` and `r222-b.md`, summary
`r222-notes.md`: 25 rows at the cap, the author's own, 25 killed, null controls
at zero of 9034 collected, two FOREGROUND batches of about four minutes each.
The learning is under `docs/solutions/workflow-issues/`, the one about a safer
default. `CONCEPTS.md` gains Rotation floor and Twin.
Filed: R-556 to R-558, none meeting the board bar today, and R-549 gained a
note: a stray folder under the archive root is now HELD for ever instead of
being kept as the newest, same closing condition, **its issue still owed**.
**R-548 was seen a second time, outside the mutation driver**: the pool sizing
test that times a freshly spawned child died in one of four hand made full suite
runs on this branch and passed three of three alone. A red gate naming only
`tests/test_pool_sizing.py::test_the_real_probe_measures_a_freshly_spawned_child`
is that flake and not this unit.
Main's highest residual number was R-558 at that merge.

**The session before: R-154 with R-153, issue #153, `relay/153`, 2026-09-19.**
A snapshot pulled off the remote is now a dated folder name and this library's,
and the confirmation digests the stamp it will really pull, which CLOSES R-154
and R-153. `backup.resolve_snapshot` is the one place a snapshot is chosen. The
verb calls it before its gate, only under `--from-backup`, and `plan_restore`
calls it again under the gates, so the check is on the path every caller takes.
A named value that is not a dated folder name refuses `snapshot-name-invalid`
before the remote is asked anything. The database portion of a backup ends by
writing an empty MARKER, `library-volume.<identity>`, beside `db/`, with
`rclone touch`, after the whole database set; a marker that cannot be written
warns `snapshot-identity-not-written` and does not fail the portion. A named
snapshot marked for another volume, or carrying two markers, refuses
`snapshot-library-mismatch`, and a marker listing that failed refuses and is
never read as unmarked. With no stamp named, OWNERSHIP SELECTS: the newest
`backup.NEWEST_WALK` folders, eight, are read newest first and the first one
marked for this library is pulled. The resolved stamp, whether it was named, the
identity it records and the identity a person stated are in the offer item, so
in the digest, and are handed to the gate as context, since the verb had never
shown the person answering anything. The stamp that was offered is what the
engine is handed, never the flag.
**WHAT A PERSON MAY MEET, three things.** Every snapshot that exists today is
unmarked, so `restore run --from-backup` with no `--snapshot` refuses
`snapshot-identity-unrecorded`, naming the newest stamp, until a backup has been
taken; naming the stamp pulls it. After a drive is replaced its snapshots name
the old volume, the refusal prints that identity, and it is passed back as the
new flag `--snapshot-volume IDENTITY`, checked, used once, recorded nowhere. And
`--snapshot`, `--snapshot-volume` and `--include-mirror` without `--from-backup`
now refuse `restore-flag-needs-pull`, where they were dropped in silence.
**The code review raised ten findings, eight applied, and one was a regression
this branch introduced**: the source system spells its dated folder
`2026-08-01_123456`, same layout, commonly the same remote directory, so the
first cut of the shape check refused every snapshot a person owns and hid them
from the listing. `is_snapshot_name` accepts both spellings. The first cut also
took the newest folder and then vetoed it, which refused under a shared root
whenever the other library backed up last, and told a person to name a folder
that may be an unfinished backup. One finding was DRIVEN AND HALF FALSE: a
saved configuration refuses a missing `library.volume_id`, so the reachable
case is an identity that cannot be a filename. Not applied: merging the marker
listing into the contents listing, R-553. Two pinned counts in
`tests/test_reserved_causes.py` moved and were re-pinned with their reasons,
the cause population 164 to 168, its reserved half 24 to 27, and the kebab
literals 456 to 463. `_fake_rclone` in `tests/test_restore_cli.py` now tells the
three listings apart and can move the remote between the two acts and inside
the second.
Battery: ruff clean, **9004 passed** and 1 skipped, scan clean, 52 of them new.
Mutation tables `docs/mutation/r154-a.md` to `r154-c.md`, summary
`r154-notes.md`: 25 rows at the cap, the author's own, 25 killed, null controls
at zero, three FOREGROUND batches under four minutes each. Two rows kill only
because the author saw the zero and wrote the test first, and eight considered
rows are logged as dropped and NOT MEASURED.
The learning is filed under `docs/solutions/integration-issues/`, the one about
a shape check derived from this product's own writer. `CONCEPTS.md` gains
Snapshot marker.
Filed: R-549 to R-555. **R-549 meets board bar (a) and (d) and its issue is
owed**: the archive rotation sorts every folder name under the archive root, so
a stray folder sorting last is kept and the newest dated archive is PURGED,
driven at the engine over a fake listing, producer not driven. R-555 could meet
it: a snapshot holding no database file is planned, and the live sidecars are
cleared before its copy fails, driven at the plan. R-550 is a person's
decision, the unmarked snapshot pulled by name. **R-523's, R-517's, R-515's,
R-512's, R-482's and R-477's issues are still owed** from earlier sessions.
**Owed to an attended sitting:** one real backup showing the marker on the
remote, and one `restore run --from-backup --target` into a scratch directory
resolving it, R-551.
Main's highest residual number was R-555 at that merge.

**The session before: R-44, issue #152, `relay/152`, 2026-09-19.**
The deletion pass now proves the identity of EVERY volume a prefix rule points
at, not only the library root's, which CLOSES R-44 Open 1 and R-51 and NARROWS
R-44 Open 4. A rule in `library.location_prefix_map` takes an optional
`volume_id`, validated as `library.volume_id` is and written only when set, so
no existing configuration changes fingerprint. `locations.PrefixRule` carries
it, `config.resolved_prefix_rules()` returns the triples, and
`resolved_prefix_map()` is unchanged for its ten readers.
`session.assert_mapped_volume_identities` asks `preflight.assert_library_volume`
about every rule target at destructive strength, from
`deletion/run.py::_assert_library_is_still`, before a path resolves.
`session.assert_mapped_file_volume` probes the DIRECTORY OF EACH FILE, not the
rule's target, at the top of the apply loop and again after the re-check, so it
stands before every permanent act: a retirement, a settlement and a move. **A
rule is held to its own identity, or to the library's when its target is
lexically inside the library root, or to nothing, and nothing recorded
REFUSES.** It is deliberately not defaulted to the library's identity, because
a library on the boot disk shares that disk with an ejected drive's leftover
mount point. One verdict besides OK passes, identity matched with the directory
absent, since the anchor split already refuses that per row. An empty mount
slot refuses BEFORE any identity is compared, through
`preflight.identity_source`, whatever the rule recorded. Two new slugs,
`mapped-volume-unmounted` and `mapped-volume-mismatch`, exit
LIBRARY_UNAVAILABLE, with steps naming the rule by its config key, because the
library slugs carry a remedy sentence that is false for a mapped target.
**WHAT A PERSON MAY MEET: a rule whose target is OUTSIDE the library root with
no `volume_id` now refuses `delete review` and `delete apply`** until the
identity the refusal prints is typed into the configuration by hand. A rule
whose target is inside the root, which is what `docs/cutover.md` describes for
the live library, needs nothing. The live configuration was NOT read, so which
case it is was not confirmed. Setup and doctor know nothing about the new key,
R-547.
**The code review raised nine findings, six applied, and four of the six were
holes in the first cut**: the refusal offered the BOOT disk's identity to
record for an ejected drive, which would have reopened R-51 for good; the
second look sat before the move only, the one branch an ejected drive never
takes, since its re-check answers GONE and GONE is settled with a tombstone;
the rule's target was probed instead of the file's directory; and an `OSError`
from the walk escaped as an internal defect. The seventh finding, that the My
Tags pass writes through a rule, was DRIVEN BY READING AND IS FALSE: nine sites
follow a rule and none writes a file through one today, R-545. Two pinned
counts in `tests/test_reserved_causes.py` moved and were re-pinned with their
reasons, the cause population 162 to 164 and the kebab literals 454 to 456.
`tests/_mounts.py` is new: it stands directories in as mount points and as
mount slots, since every temporary directory sits on one filesystem.
Battery: ruff clean, **8952 passed** and 1 skipped, scan clean. Mutation tables
`docs/mutation/r44-a.md` and `r44-b.md`: 22 rows, the author's own, 21 killed,
one zero that its own description predicted as an equivalent change while the
empty slot guard holds, null controls at zero. Two FOREGROUND batches of about
six and four minutes. The first run of batch a was declared INVALID by the
driver because the null control saw one death in the pool sizing test that
times a spawned child, R-548; the rerun was valid.
The learning is filed under `docs/solutions/integration-issues/`, the one about
a refusal that hands over a value to record.
Filed: R-545 to R-548. None meets the board bar: R-545 has no cost until
adopt's tag write is armed, R-546 and R-547 are unmeasured, R-548 is maintainer
facing. **R-44 Open 4's remainder is a person's decision** and the entry lists
the four options: a rule aimed at the wrong directory on the RIGHT disk still
offers the only copy of a referenced file, driven and pinned in
`test_the_wrong_directory_on_the_right_volume_is_still_offered_and_is_recorded_as_open`.
**Owed to an attended sitting:** one real second volume through `delete
review`, with and without `volume_id` on its rule, and the identity read timed
on an external drive, since the quarter millisecond in the docstring was
measured on the boot disk.
**Main's highest residual number is R-548.**

**The session before: U104, issue #149, `relay/149`, 2026-09-19.**
`crate intake set` and `crate intake identify` take the web address of a mix,
which CLOSES R-303. The address is fetched through a new seam,
`intake/fetch.py`: a `SetFetcher` protocol, a shipped `YtDlpSetFetcher`, and a
`fetched` context manager that owns the scratch folder. **The brief's verified
state was out of date**: it said nothing drives the downloader, and U80 had
since landed `fallback.YtDlpFetcher`. The mix download is THAT argv with two
edits, a numbered output template and a playlist bound of two, so a set page
lands as two files and is refused as several recordings rather than returned
as one. The mix lands under a new installation scoped state entry,
`mix_scratch`, one folder per address named by a digest of it, cleared before
every attempt and removed however the pass ends, a raise included. **A mix
never lands under the library**: the scratch root is refused if it resolves to
the library or under it, by text AND by `samefile` over every existing
ancestor, because `Path.resolve` leaves letter case as typed and the code
review's case finding was DRIVEN true on this machine. The order is the cost
order: a path that names nothing is refused before the gate as before, the
recognition gate and identify's two free checks run before the download, and
the job freezes the ADDRESS as its source, since the file is gone before a
resume reads it and a resume never fetches. Refusals reuse existing slugs, so
the cause population did not move: `yt-dlp-missing` with the install hint, now
raised from `core/binary_refusal.py` for both verb families with `said` and
`origin` required; `unavailable-transient`, retryable, for a TIMEOUT ONLY; and
`intake-list-unusable`, not retryable, for a failed download, a playlist, a bad
landing, a scratch folder that cannot be made and a scratch root under the
library. A refusal raised inside the identifier over a fetched mix is re-raised
about the address, because the file it names is gone. `binary.yt-dlp` is
deliberately NOT a doctor check on either verb, since only an address needs it.
**NO TEST RUNS YT-DLP**: a conftest autouse fixture fails any test that reaches
`fetch.fetcher`, and the shipped fetcher is built only over a fake `run`.
**The code review raised eight findings, seven applied** and one recorded as
R-538. Two pinned counts in `tests/test_reserved_causes.py` moved and were
re-pinned with their reasons: one warning literal, `mix-scratch-left`, and one
holder, the new core module. Battery: ruff clean, **8906 passed** and 1
skipped, scan clean, 42 of them new in `tests/intake/test_set_fetch.py`.
Mutation table `docs/mutation/u104.md`: 25 rows, the author's own, 25 killed,
five null controls at zero, 5 considered rows logged as dropped and NOT
MEASURED. It ran as five FOREGROUND batches, `u104-a` to `u104-e`, because a
Relay session cannot wait on a background job and one 25 row invocation passes
the 600 second tool ceiling; each batch took under three minutes. The learning
is filed under `docs/solutions/workflow-issues/`, the letter case one.
Filed: R-538 to R-544. None meets the board bar, each being unmeasured,
attended, or a person's decision. R-544 is the one to read: thirteen other
containment checks in `src` compare resolved paths as text, found by grep and
NOT driven.
**Owed to an attended sitting:** one real mix address through `crate intake
set`, one set page to see the several recordings refusal, the same address
fetched twice with the two digests compared (R-539), and a measured download
bound in place of 3600 seconds (R-541).
**Main's highest residual number is R-544.**

**The session before: R-424, issue #111, `relay/111`, 2026-09-19.**
`crate sync favorites` now declares only the remote heart it performs, which
CLOSES R-424. The honest report arm, as the card's recorded decision directed:
the local write was NOT built. The entry declares `writes={"remote"}` alone.
`db_tree` and `db_metadata` stood for a colour, a Favorite tag and a playlist
membership the handler never writes, since it passes `colors=None` on every
path; there is no document beside the export, so no `xml`; and the outbound
write ledger is not `files`, because `export.playlist` writes that same ledger
through the same shell and has always declared `remote` alone. The cloud sync
decision went with the database surfaces, and so did `rekordbox.closed` and
`rekordbox.pins`, driven: a sweep hearts both rows with rekordbox and its agent
reported running and with `rb_writer.open_db` replaced by a raise.
`library.mounted` stays, because the ledger is library scoped. The summary no
longer says "both ways", the inbound half being `crate intake playlist
favorites` since U70. The always empty `colored` key is gone from each item
report; in its place a standing warning, `favorites-local-write-unbound`,
spelled once in `favorites/cli.py` and carried by the verb's queueing branch,
its resume through `shell.resume`'s new `standing` argument, and
`sync/cli._plan_favorites`. It is a warning because the default renderer prints
a verb's outcome, its warnings and its run id and nothing of its payload.
`docs/GUIDE.md` and the shipped `sync-and-publish` skill asset both promised
the colour, the tag and the membership; both now describe the outbound half,
and the asset gained the `--export` its example always needed.
**The code review raised five findings, all five applied**, the largest that
both documents claimed every pass reports the sentence while `crate job resume`
spawns the child detached and its report goes to the job log. Collected
**8865** and 1 skipped, 10 of them new, two driving the DEFAULT human renderer
rather than the json helper the rest of `tests/test_outbound_workers.py` uses.
Mutation table `docs/mutation/r424.md`: 12 rows, the author's own, 11 killed,
null control zero, 2 considered rows logged as dropped and NOT MEASURED. The
one zero was the GUARD's fault and not the filter's, a `sync all` test that
raised before it reached the loop it asserted over; repaired, re-measured by
hand, it kills. One row reported 20 kills that are not its own, all in
`tests/test_rebuild.py`, the parallel flake, recorded as a third sighting on
R-520; that row is really a maintainer facing zero. The learning is filed under
`docs/solutions/workflow-issues/`.
Filed: R-536 and R-537. Neither meets the board bar. R-536 is a person's to
decide: `destructive=True` stays on a verb that writes only an add-only remote
surface, and `export.playlist`, its sibling, has never declared it.
**Main's highest residual number is R-537.**

**The session before: R-432, issue #180, `relay/180`, 2026-09-19.**
Two landings under one batch name can no longer take each other's files or
intake file, which CLOSES R-432. `crate intake land` holds
`landing.batch_lock` across the whole of `landing.apply`, after the gate and
never before it. The lock is `jobs.driver_lock`, exclusive and non blocking,
never unlinked, under a new installation scoped state entry `landing_locks`,
on the local state disk because the library volume is commonly exFAT. Its key
is a digest of the casefolded, normalized NAME. A held name refuses as
`job-driver-held`, exit LIBRARY_BUSY, nothing moved, the batch and the holder's
pid named, with two steps, because a first landing that succeeds keeps the
name through its intake file and a retry is then refused `output-exists`.
**The code review raised eight findings, four applied**, the largest that the
guide and the refusal promised a retry that fails whenever the first landing
succeeds. One was driven and needed no change: an unwritable state directory is
already refused by name with nothing moved. The rest are R-534 and R-535.
Collected **8857**, 23 of them new in `tests/test_intake_land.py` and
`tests/test_landing.py`, one of which holds the lock in a second process and
kills it. Mutation tables `docs/mutation/r432-a.md` and `r432-b.md`: 17 rows,
the author's own, 16 distinct and one measured twice, 15 killed, null control
zero in each. The one zero is the release in the lock's `finally`, inert under
CPython, with a composite that kills 7; the learning is filed under
`docs/solutions/workflow-issues/`. Three considered rows are logged as dropped
and NOT MEASURED. Table a's first run was declared invalid by its null control,
20 deaths all in `tests/test_rebuild.py`, the parallel flake, recorded on R-520.
Filed: R-534 and R-535. Neither meets the board bar. One half of R-535 is a
person's to decide: a platform with no `fcntl` gets no lock at all.
**Main's highest residual number is R-535.**

**The session before: R-501, issue #182, `relay/182`, 2026-09-19.**
A landed batch can now be followed to a library the cutover precheck passes,
with no hand deletion, which CLOSES R-501, R-433 and R-436. `place_files`
leaves its session `awaiting-import` with the pending action PERSISTED on the
record, opens it after the last refusal that needs none, and abandons it and
removes the file it made on any later failure. A new verb, `crate intake
imported --export`, proves the import against a Fresh Export taken after it,
every Location the run recorded in the routing ledger compared by
`routing_pass.track_id`, then retires the intake file by RENAMING it to
`NAME_inboxed.xml.imported`, never a delete, and moves the run out of
`awaiting-import`. An intake file is refused as its own proof, by name and by
identity. **The decision, and what the brief did not see:** the run cannot be
CLOSED before a cutover, because `routing_pass.close_run` refuses a run holding
a deferred placement and only a native tree can place one. So a proven run
stays `open` with `detail["import_verified"]`, and the precheck excuses a run
that is open, holds no capture and carries that key,
`session.owes_only_deferred_routing`. That is R-528, with the option not
taken, a sixth session state. It is also the learning filed under
`docs/solutions/workflow-issues/`. After a cutover `route pending` records the
pass as the proof when it routed at least one track, and closes the run.
`route pending` with no native tree is a NO-OP with a `no-native-tree` warning
where it answered ok. `intake file` ends PENDING like a landing. `sync mark`
reads its pass off a retired name. A landing made BEFORE this unit is settled
too, and its file is removed by hand, R-529. **The code review raised ten
findings, nine applied**, the largest that the first cut looked only for
`awaiting-import` and so left every earlier landing where it was. The tenth is
in R-533. Collected **8834**, 44 of them in the new
`tests/test_intake_imported.py`; the battery on the committed tree was **8833
passed and 1 skipped**, ruff and the scan clean. Mutation tables
`docs/mutation/r501-a.md` to `r501-d.md`: 25 rows, the author's own, 25 killed,
null control zero in each, eight considered rows logged as dropped, two of them
NOT MEASURED. Table d's first run was declared invalid by its null control, 25
deaths all in `tests/test_rebuild.py`, the parallel flake, recorded on R-520.
Filed: R-528 to R-533. None meets the board bar, each is paid at the attended
cutover or is maintainer facing. **R-523's and R-517's issues are still owed**
from earlier sessions.
**Main's highest residual number is R-533.**

**The session before: R-500, issue #181, `relay/181`, 2026-09-19.**
`name apply` no longer renames a file a collection row names because that row
sat under a volume no prefix rule names, which CLOSES R-500. `_referenced` in
`write/naming_cli.py` collects every DARK row and refuses the whole verb as the
new reason `collection-row-unmapped`, exit PRECONDITION, remedy
`fix-config-values`, count first and the first DECODED location named, on the
checking path, so the plan read and the re read after the gate both get it.
**Dark is two facts together**: the row resolves `UNMAPPED` and its recorded
file is not on this machine. A row under no rule whose file exists has
answered, and its as recorded key protects it. **The case reading, decided:** a
rule differing from the recorded volume only in case REFUSES, pinned by a test,
because the shared resolver compares exactly and matching here alone would be a
second locate. **The locate, lifted in part:** `trees.located` is public,
decodes once and returns the decoded path beside the resolution; the keying
stays in `naming_cli`. **The code review raised nine findings, seven applied.**
The largest was that the first cut refused on EVERY unmapped row, which stops
the verb over a track imported from a downloads folder or rekordbox's demo
tracks; two U67 tests needing an identity rule to pass were the signal, and
that is the learning filed under `docs/solutions/integration-issues/`. Two
findings are recorded and not fixed, R-524 and R-525. **Where the brief was
not followed:** it asked for the refusal before the tree walk, and the
collection is still read after it, R-526, because U67 pinned that an empty
folder needs no database. Collected **8783**, 11 of them this unit's, all in
`tests/test_naming_apply_cli.py`; the battery on the committed tree was **8782
passed and 1 skipped**, ruff and the scan clean. Mutation tables
`docs/mutation/r500-a.md`, `r500-b.md` and `r500-c.md`: fifteen rows, the
author's own, fifteen killed, null control zero in each, three considered rows
logged as dropped. Filed: R-523 to R-527. **R-523 meets board bar (c) and its
issue is owed**, since a Relay session cannot open one before the merge puts
the number on `main`. **R-517's issue is still owed** from three sessions
before.

**The session before: R-503, issue #184, `relay/184`, 2026-09-19.**
An offered track a person answered in review is now listed, owned or left a
question as the answer made it, which CLOSES R-503. `_listed` in
`intake/missing_cli.py` looks each offered report's item up by the
`review_item` the report names, through the new `_answered`, read only. An
unanswered row stays offered and nothing is asked again. An answered row joins
the missing rows in R-502's consult, renamed from `_still_missing` to
`_asked_again`, in report order and one library walk, so a rejection is missing
and listed unless a tombstone stands, a bound yes over a copy still held is
owned, and a yes about a copy that is gone stays a question. Counts say what
each row is now; `answered_missing`, `answered_owned`, `answered_suppressed`
and `answered_offered` are on the summary and a new `intake.missing.answered`
check. **The code review raised one finding, applied**: the step on a refusal
over the job's earlier list was inferred from what changed since the job ran,
and is now read from the earlier list itself by `_changed_since`, naming the
tracks each names that the other does not; R-502's step was reworded with it.
Collected **8772**, 9 of them this unit's, all in `tests/test_intake_missing.py`;
the battery on the committed tree was **8771 passed and 1 skipped**, ruff and
the scan clean. Mutation tables `docs/mutation/r503-a.md` and `r503-b.md`,
summary `r503-notes.md`: twenty one rows, every user facing row killing, three
maintainer zeros. Nothing filed. **R-517's issue is still owed** from two
sessions before.
**Main's highest residual number is R-522.**

**The session before: R-502, issue #183, `relay/183`, 2026-09-19.**
A second `intake missing` over a job no longer lists tracks the library has
gained since, which CLOSES R-502. `_listed` in `intake/missing_cli.py` hands
every missing report to the new `_still_missing` before anything is written,
for `--job` and `--run` alike: `match.resolve_one` over
`match_cli.library_view` against the CURRENT configuration, the worker's
consult, with a question the library raises read back through
`match_cli.adjudicate` under the job's own verb. A row now held, deleted on
purpose or held in another version is counted as `owned_since`,
`suppressed_since` or `offered_since` on the new `intake.missing.since` check
and is neither listed nor handed on; `missing` is what is still missing. The
reports are not rewritten, so `sync mark` is unchanged. An absent music folder
refuses `library-volume-unmounted`, only when a row is missing, and the entry
declares `library.mounted`. **The second run, decided:** unchanged library,
same bytes; every row gained, nothing written, no `next`, `no_op`; some
gained, refused over the job's earlier list by its fixed name, with a step
saying how many, which is R-476's name and noted there. **The code review
raised two findings, both applied**: the frozen root, which refused a moved
library as unmounted, and the doctor declaration. Collected **8763**, 11 of
them this unit's, all in `tests/test_intake_missing.py`; the battery on the
committed tree was **8762 passed and 1 skipped**, ruff and the scan clean.
Mutation tables `docs/mutation/r502-a.md`, `r502-a2.md`, `r502-b.md`,
`r502-b2.md`, summary `r502-notes.md`: nineteen rows, the author's own, every
user facing row killing after G7 and G13's tests were fixed, two maintainer
zeros. G7's zero was the env override trap already filed under
`docs/solutions/workflow-issues/`, met again. Filed: R-522, `--job` over
another library's job rechecks against this one, read and not driven, no
issue. **R-517's issue is still owed** from the session before.

**The session before: R-431, issue #179, `relay/179`, 2026-09-19.**
A track deleted on purpose whose library row kept a featured credit is no
longer listed for download, which CLOSES R-431 and R-69. Option 1 of the
brief's two was taken, since `intake missing` only reads the states `intake
playlist` committed and a review step at the list verb would have left that
report saying missing. `deletion.stores.record_tombstone` writes a COMPANION
beside the tombstone of a row whose composed title carries a bracketed credit:
`stores.uncredited_version_of(row)`, which is `version_of(row)` with
`core.tombstone.uncredited_title` applied, under the new kind
`tombstone.KIND_VERSION_UNCREDITED`, `version-uncredited`, replicated in
`match.UNCREDITED_KIND` and compared by the armed parity guard.
`match.standing_tombstone` asks under it second, through the new
`Wanted.uncredited_spellings`, which answers nothing unless the `Wanted` was
SEEN to credit nobody: it has a `spelled` title, so it was read from a listing
and not built by hand, the title spells no bracketed credit, and the new field
`Wanted.several_artists` is false, set by `_bills_several(row)` in `_from_row`.
**That field crosses the intake freeze**, `intake.cli._frozen` and `thawed`,
and a payload frozen before it existed thaws as billed. `standing_tombstone`
takes `companions=False`, which `match_cli`'s stale record report passes over
a MATCHED row. **One write per decision:** `DecisionStore.record(beside=)`
writes the companion in the same write and only when the tombstone itself is
written, and `DecisionStore.revoke(also=)` decides under the lock and lifts in
one write. `stores.revoke_tombstone` lifts the companion unless another
standing tombstone still accounts for it, by the tombstone's own pointer
`uncredited_id` first and by stripping second, and `run.revoke` routes a
tombstone through it. `stores.summarize` emits `credited_id` and
`uncredited_id`. **The identity stamp did not move**, still
`is2_5b356bbb451de9cc`, because `uncredited_version_of` sits on top of
`version_of` and is not reachable from it. `UNRECONCILED` in
`tests/test_match_states.py` is empty, and
`test_the_verbatim_consult_alone_still_misses_the_credited_row` pins that the
verbatim consult did not widen. The claim that nothing widened past what the
engine already calls one version is measured:
`test_the_companion_reaches_exactly_what_ownership_reached`. **The code review
raised ten findings and eight were applied**: the two writes, the lift decided
outside the lock, the shared companion's accounting by stripping alone, the
hand built `Wanted`, the guest billed in the artists list, the stale report
over a held file crediting somebody else, the listing fields, and two comments
that claimed more than the code did. Two are recorded, R-517 and R-518.
Collected **8752**, 56 of them this unit's, 35 in the new
`tests/test_uncredited_tombstone.py`, 19 in the match suite and 2 in the list
verb's; the battery on the committed tree was **8751 passed and 1 skipped**,
ruff and the scan clean. The kebab literal population was re-pinned 450 to 451
for the one kind. Mutation tables `docs/mutation/r431-a.md` and `r431-b.md`, 25
rows at the cap, 25 killing, the author's own, with seven considered and
dropped with their reasons. Filed: **R-517**, a credited tombstone written
before the companion existed still misses, board bar (a) and (b), **its issue
is owed**; R-518, the label sweep asks under the verbatim
kind only, read and not driven; R-519, a listing that names a guest anywhere
cannot reach the companion of the deletion crediting that same guest, the cost
of the guards; R-520, one test of `tests/test_deletion.py` fails on some full
parallel runs, two of six here, R-470's family; R-521, a stale credited
tombstone leaves no trace for a listing that spelled no credit. A learning is
filed under `docs/solutions/integration-issues/`, on the intake freeze, and
`CONCEPTS.md` gains Companion. **Main's highest residual number is R-521.**

**The session before: R-504, issue #185, `relay/185`, 2026-09-19.**
A hearts listing shorter than the account declares is reported, which CLOSES
R-504. `listing.favorite_tracks_declared(session)` returns the rows and the
count the walk ended on, recorded through the `declared_total` callable rather
than asked again, `None` for a zero or sentinel count. The adapter's
`favourite_tracks` compares them and raises the new seam exception
`catalogue.HeartsShortfall(rows, declared)`, with `listed`, `withheld`,
`summary()` ("197 declared, 185 listed, 12 withheld by the provider") and
`block()`. It is an exception and not a return shape so an unaware caller
fails closed as `label-playlist-unreadable`; no fake had to change.
`label_cli.favourite_tracks_or_refuse` now returns `(rows, shortfall | None)`.
`intake_cli.list_favorites(found)` is the hearts path and returns
`(tracks, shortfall)`, and `list_playlist` is playlists only. `intake playlist
favorites` queues what came back, warns `intake-hearts-withheld`
(`HEARTS_WITHHELD`, `withheld_warning`) and carries `shortfall` under
`progress`, and an all withheld listing is a no-op that still warns. `sync
all`'s inbound block gains `shortfall` and its check FAILS naming the same
numbers, over an empty listing too. `/code-review` found no correctness bug
and one design point, that the row fails on every pass for a steady
withholding, recorded as R-516 with the brief's fail kept. Collected **8696**,
17 of them this unit's; the battery on the committed tree was **8695 passed
and 1 skipped**, ruff and the scan clean. The kebab literal population in
`tests/test_reserved_causes.py` was re-pinned 449 to 450 for the one warning
code. Mutation tables `docs/mutation/r504-a.md` and `r504-b.md`, 22 rows under
the cap, 22 killing, the author's own; one row in each was considered and
dropped with its reason, and B5 was refused once as ambiguous and widened.
R-515 (a playlist or release listing returns short the same way, driven at the
listing only, meets the board bar, **its issue is owed**) and R-516 are filed.
**Owed to an attended sitting:** R-423's live hearts count.

**The session before: U103, issue #148, `relay/148`, 2026-09-19.**
`crate intake identify` asks the library, writes its tracklist, and recognition
is paid for once, which CLOSES R-422 and NARROWS R-304. The resolve step is
shared: `match_cli.resolve_list(cfg, wanted, handler_key=, run_id=)` is the
body of `match_list` lifted out, returns a `ListResolved` of the result, the
pending action and the warnings, and both verbs call it. Identify therefore
reports `matched`, `needs_review` and `missing` for real, offers a version
question under its own key (the registry entry is now `adjudicates`, and its
doctor checks gain `library.mounted`), and ends PENDING_HUMAN over an open
question exactly as `match run` does. The order in `intake_identify` is the
spend order: config, recording, presence gate, `--out` is not a file,
`_library_or_refuse` (an absent music folder is `library-volume-unmounted`),
THEN the identifier, then the tracklist, then the library walk. The tracklist
is `<stem>-<12 digest characters>.tracklist.txt` (`tracklist_name`) in `--out`
or `tracklists` under download staging, replaced and not refused, and its path
rides a `tracklist-written` note on the warnings channel because `match/1` is
closed at three arrays. **The recognition cache** is `acrcloud.RecognitionCache`
over the new declared state entry `identify_cache` (installation, directory,
never restored): one JSON document per recording named by `ChunkPlan.key()`, a
sha256 over `content_digest` (the recording's BYTES), the offsets, chunk
length, interval, sample rate and host. It keeps the service's RAW answer per
offset, only for a match or a miss, and the same rule is applied again on the
way back in; a document that is unreadable, of another version or carrying
another plan is a miss. A kept chunk skips the carve, the ledger and the
transport, and a fully kept recording never RETRIEVES a credential, though the
presence gate still runs. The per run bound reads the whole grid and the
monthly bound reads only what is owed. The write is a locked merge under a
sibling `.lock`, and it runs in a `finally`, so a pass that RAISED keeps what
it paid for; a process that dies does not, which is what R-304 still holds.
`Identified` and `IdentifyResult` gain `cached`, `cache_unwritten` and
`digest`. Both verbs take `--refresh`, which reads nothing kept and pays for
every chunk, and both say `recognition-cached` when kept answers were read and
`recognition-cache-unwritten` when paid answers could not be kept; `intake set`
reads the same cache with no code of its own, through `bound_identifier`.
**The code review raised ten findings and eight were applied**: the absent
library refusal, the digest in the tracklist name, the locked merge, keep on
raise, `--refresh` and the served note, the dropped warnings on set's nothing
identified path, a refusal message that promised a free rerun over a gap, and
two redundant directory creations. The two not applied are recorded, the
account missing from the cache key in R-513 and the digest being read before
the monthly bound, which cannot move because what is owed depends on it.
Collected **8679**, of which 46 are this unit's, 25 in
`tests/intake/test_recognition.py`, 20 in `tests/intake/test_workers.py` and
one new conformance 4 case; the battery on the committed tree was **8678
passed and 1 skipped** in 88 seconds, ruff and the scan clean, and no test of
this unit's is among the five slowest. Two pinned populations in
`tests/test_reserved_causes.py` were re-pinned with their notes, three warning
code literals and one in-range integer, the digest length 12. Mutation tables
`docs/mutation/u103-a.md` and `u103-b.md`, 25 rows at the cap, run in the
foreground under Relay in two tables to stay under the harness ceiling, 25 of
25 killing, the author's tables and not independent ones; table a's one first
pass zero got a test and was re-run killing, M1 reads collect-error because
the flag it removes also removes a parametrized case, and nine rows considered
and dropped are logged with reasons. A learning is filed,
`docs/solutions/workflow-issues/the-shared-library-view-answers-an-absent-music-folder-with-an-empty-index.md`.
R-512 (an absent music folder is an empty library to `match run` and the
intake worker, DRIVEN, meets the board bar, **its issue is owed** because a
Relay session cannot file one after the merge), R-513 and R-514 are filed.
**Owed to an attended sitting:** one real identify then set over a real
recording. **Main's highest residual number is R-514.**

**The session before: U81, issue #126, `relay/126`, 2026-09-19.**
Accepted second source candidates download, which CLOSES R-404: the one
sanctioned lossy exception is an act again and not only a marker.
`crate acquire fallback-fetch PATH` is a new queued verb in
`acquire/fallback_cli.py`, registry entry `acquire.fallback-fetch`,
`job_state/1`, long running, `argv_builder="fetch_argv"`, `adjudicates`,
writes files, destructive, no gate (the `acquire.download` argument), doctor
checks `library.mounted`, `binary.yt-dlp`, `binary.ffmpeg`, and bound in
`cli/handlers.py` to `fallback_cli:handle_fetch`. It resolves the list through
`missing_rows`, now shared with `acquire fallback`, and `accepted_rows` queues
one item per row whose `fallback-candidate` is ACCEPTED, keyed on the review
item id, with artist, listed title and URL frozen under `ROWS`. Owned rows,
provider routed rows (`provider_routed`, factored out) and unanswered,
rejected or stalled rows are not queued; nothing accepted is a `no_op` with
state `nothing-accepted`. The worker: strict policy refuses `lossy-refused`
before any download; a non web address or a nameless row is
`unavailable-permanent`; the name is the ROW's, `Artist - Title [marker].mp3`
through `fetch_stem` and `acquire_cli.marked_name`, and a taken name is
`output-exists` before the download and after it; the download lands in
`acquire_cli.staging_dir` through the `FallbackFetcher` seam in
`acquire/fallback.py` (`YtDlpFetcher`, MP3 at quality 0, a fixed `fetched`
stem, `--` before the URL); `checked_landing`; then the NEW
`core.tags.strip_tags` removes every tag the upload carried before
`write_tags` writes artist and title from the row; a missing yt-dlp PARKS the
job; a failed fetch or an untaggable file is `unavailable-transient`. **The
code review's one finding was fixed:** yt-dlp does not run its audio
postprocessor on an upload already in MP3, so `-map_metadata -1` never
stripped an uploader's TBPM; `strip_tags` is the guard now, and
`docs/solutions/integration-issues/yt-dlp-skips-its-audio-postprocessor-when-the-upload-is-already-the-target-format.md`
records why. `acquire fallback`'s accepted check names the fetch command and
its summary gains `fetch_next`. Collected **8626**, main's 8583 plus 34 in the
new `tests/test_acquire_fallback_fetch.py` and 9 conformance cases for the new
verb; the battery on the committed tree was **8625 passed and 1 skipped** in 65
seconds, ruff and the scan clean. Mutation tables `docs/mutation/u81-fetch-a.md`
and `u81-fetch-b.md`, 25 rows at the cap, run in the foreground under Relay;
two zeros got tests and were re-run killing, and Q2's zero was fixed by
removing the covering URL half and NOT re-measured, read in
`u81-fetch-notes.md`. **The `u81` mutation prefix was already R-322's**, so
this unit's files are `u81-fetch-*` and R-322's `u81-notes.md` is unchanged.
R-498 (the real tool never ran) and R-499 (no per row purchase link override)
are filed, and neither meets the board bar. **Owed to an attended sitting:**
one real fallback download, R-498. **Main's highest residual number is
R-499.**

**The session before: U85, issue #130, `relay/130`, 2026-09-19.**
`crate tag folder` fetches and embeds album art for a file carrying no
picture, which CLOSES R-399: the registry's "genre and album art" is now true.
`tagging/tag.py`: `SearchHit.art`, the bytes field nothing read, is gone and
`SearchHit.art_url` replaces it. `tag_one(path, *, searcher, fetch_image=None)`
skips the search only for a file with BOTH a genre and a picture, never
overwrites a genre, and embeds only when `core/art.py:read_pictures` finds no
picture at all, the source system's never re-download rule, so a zeroed block
is U84's repair and is not fetched over. The bytes go through
`to_cdj_jpeg` (800 square) and `write_front_cover`, AFTER the genre save.
`TagResult` gains `art_fetch` and `art_fetch_detail`, one of
`tag.ART_FETCH_STATUSES`: `embedded`, `present`, `unavailable`, `error`,
`unchecked`. A failed fetch, a fetch that raises, or bytes that are not an
image are `unavailable` and never fail the item. **The code review's one
finding was fixed:** a tagged file searched only for its art now turns a
catalogue refusal into `unavailable` naming the refusal's slug, because it had
been a clean `has-genre` skip before and a parse break is not retryable. An
untagged file still propagates the refusal. `tagging/searchers.py`: the URL
comes off the SAME best scored row as the genre, `_beatport_best` returning a
`_Pick(genre, art_url)`. Beatport is `release.release_image_uri` with
`image_size/NxN/` rewritten to `BEATPORT_IMAGE_EDGE` 1400. Bandcamp is the
listing's `f4.bcbits.com` image, else the track page's `og:image`, rewritten
to `_10.jpg`, and the track page is now fetched when the listing lacks a genre
OR a picture. Traxsource names none, which is parity. Only http and https
values become a URL. `default_image_fetch` is paced and shares the page
fetch's 429 policy through `_answered`, answering bytes or None.
`tagging/cli.py`'s worker binds `searchers.for_images()` at call time, the
item artifact carries both keys, and `progress.tagging.art_fetch` counts every
status, zero filled. 36 new test cases by count, collected 8583: 19 in
`tests/test_tagging_engine.py`, 16 in `tests/test_catalogue_searcher.py`, 1 in
`tests/test_tag_workers.py`. Three existing tests now plant a picture on the
tagged file they assert is never searched, because the brief reversed that.
Mutation tables `docs/mutation/u85-a.md` and `u85-b.md`, 25 rows at the cap,
23 killed, two maintainer facing zeros, read in `u85-notes.md`. R-495 (the
payload shapes were never read live), R-496 (the image fetch has no byte
ceiling) and R-497 (a tagged file whose track names no picture is searched
every run) are filed, and none meets the board bar. **Owed to an attended
sitting:** one live folder run, R-495, and one embedded cover on a real CDJ or
XDJ. **Main's highest residual number is R-497.**

**The session before: U80, issue #125, `relay/125`, 2026-09-19.**
A track the provider does not carry gets second source candidates, which closes
R-404's search half. `crate acquire fallback PATH` is `acquire/fallback_cli.py`,
registry entry `acquire.fallback`, `diagnostic/1`, `adjudicates`, no write
surface, doctor checks `library.mounted` and `binary.yt-dlp`. PATH is the
unlisted text list or any list `match run` reads. Rows are resolved against the
library exactly as `intake missing --list` resolves them. A row carrying the
provider's own id (`missing_cli.provider_ref`, public now) or with a provider
candidate waiting or accepted in review is NOT searched and is counted
`provider_routed`. Every other missing row is searched on SoundCloud and then
YouTube through the `FallbackSearcher` protocol in the new `acquire/fallback.py`.
The shipped `YtDlpSearcher` runs yt-dlp in flat playlist mode through an
injectable runner, WITHOUT `--ignore-errors`, so a nonzero exit, a timeout or a
program that cannot start is `FallbackUnavailable` and never an empty answer.
**NO TEST RUNS YT-DLP**: the suite binds `fallback_cli.searcher` to a fake and
drives the shipped searcher through a fake runner. The score is the source
system's, half similarity and half word coverage over `match.fold`, with a mix
over 900 seconds scaled by 0.4. It orders the screen and drops nothing. Ranked
candidates are offered on the `fallback-source` queue under the NEW KIND
`fallback-candidate`, one item per row keyed on the folded artist, title and
version, each option an upload page URL. Nothing is picked and nothing
downloads. The queue is read before any search. Rows are offered as their
answers arrive, so a failed search refuses `unavailable-transient` naming every
item already offered this run. A missing yt-dlp refuses under the NEW CAUSE
`yt-dlp-missing`, carrying the binaries module's own remedy token and install
hint, and only when a row needs a search. **THE TRAP:** the reserved binary keys
(`install-binary` and its three siblings) are remedy tokens and not declared
reasons, so a refusal spelled with one exits 1 as an internal error. Filed under
`docs/solutions/integration-issues/`. No candidate anywhere refuses
`intake-list-unusable`. An accepted upload is reported with its URL, and the
verb says nothing downloads it yet. **`/code-review` raised two findings, both
driven red and fixed** in one round: a row carrying the provider's own id was
searched on a second source, and a track typed with and without a key was
searched twice, because rows were deduplicated on the match id and the item
is keyed without the key. The same dedupe shape one file over, in
`intake missing --list`, is R-493. 43 new test cases by collected count, 8504
to 8547: 36 in the new `tests/test_acquire_fallback.py` and 7 that
`tests/test_cli_contract.py` parametrizes over the new verb.
`tests/test_reserved_causes.py` re-pinned: causes 160 to 161 and non-reserved
136 to 137, kebab literals 442 to 444 with 283 to 284 non-keys, holders 98 to
99. Mutation tables `docs/mutation/u80.md` and `u80-b.md`, 25 rows at the cap,
22 killed on the first pass and the three zeros killed after a test each, six
rows logged as dropped. R-404 is narrowed to its download half, which is the
act and the lossy marking. R-492, R-493 and R-494 are filed, and none is on
the board. **Owed to an attended sitting:** one real search, one row with
uploads and one with none, which is R-494's measurement. Battery on the
recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 8546 passed and 1
skipped in 76 seconds, and no test of this unit's among the ten slowest.
**Main's highest residual number is R-494.**

**The session before: U79, issue #124, `relay/124`, 2026-09-19.**
A row nothing names exactly has a route to a download, which closes R-415 and
narrows R-302 to its registry flags. `crate intake missing --list PATH` is a
third chooser beside `--job` and `--run`. PATH is the unlisted list a set job
wrote, or any list `match run` reads. Every row is resolved against the
library first, through `match_cli.library_view`, `resolve_all` and
`adjudicate`, so an owned track, a version question and a tombstoned track are
never searched for, and a music folder that is not there refuses
`library-volume-unmounted` rather than listing every row. A row still missing
is asked by ISRC when it has one, then handed to the new
`intake/candidates.py`. **A SEARCH IS A PROPOSAL, NEVER A PICK.** The ninth
`Catalogue` member is `search_tracks(artist, title)`, one track search on the
retry ladder, at most `catalogue.TRACK_SEARCH_PAGE` rows, choosing nothing. A
row is listed without a person only when the exact candidates, under `match`'s
own `recording_token` and `version_token`, carry ONE distinct identifier,
every row of the answer was readable, the answer did not fill the page, and
the title reads one way. Anything else with a candidate worth showing is
offered on the `version-match` queue under a NEW KIND, `provider-candidate`,
NOT a new queue, since that surface's legacy file is the source system's
provider search review. The identity is the folded artist, title and version,
the option id is the provider track id, and the option's detail carries the
frozen track through a new public `intake_cli.frozen`. Exact candidates lead,
then score, and `CANDIDATE_FLOOR` of 60 drops hits that resemble nothing. A
score never lists anything. The queue is read BEFORE the provider through a new
`review.find`: an accepted candidate is listed with no search spent, unless
the library now holds it, state `held`; a rejected row stays rejected until
cleared; an open one is not searched again; an acceptance naming none of
several candidates stalls. Every search answer is in hand before any offer, so
a provider that fails part way refuses `unavailable-transient` with no
candidate offered and no list written. No candidate is a failing `unfound`
check, and a run that listed nothing and asked nothing refuses
`intake-list-unusable`. The list is `<input stem>-found-<12 hex>.list.json`,
the digest over the rows and their provenance, source `list`. The `--job`
flow's `unlisted_next` now names `intake missing --list`, since `match run`
was a dead end for those rows. The registry entry declares `adjudicates`.
**`/code-review` raised nine findings, two of them reproduced.** Seven were
fixed in one round: the run after a review answer was REFUSED, because the
found list had one fixed name and the emitter refuses other bytes, now the
digest, and filed as a second way into the trap already under
`docs/solutions/integration-issues/`; a missing row of another service's list
was in no file and on no check at exit zero, because its ref is that service's
id and the emitter strips it; a full page was read as the whole answer; a
title with two readings was listed on one candidate; the failed search said
nothing was offered over a queue holding the library's own question; the
catalogue was resolved twice; and the unknown item lookup had two spellings.
Two are R-489 and R-491. The hunt after it read `listdoc.write`'s failure
paths as this unit's own and gave both paths of the verb one helper that turns
a failed write into the verb's refusal. 61 new test cases by collected count,
8443 to 8504: 52 in the new `tests/test_intake_missing_search.py`, 8 in
`tests/test_label_tidal_catalogue.py`, and 1 that `tests/test_cli_contract.py`
parametrizes over the newly adjudicating verb. `tests/test_reserved_causes.py`
re-pinned to 442 kebab literals and 283 non-keys, holders unchanged at 98, and
the also-holds-an-integer half 18 to 19 for `TRACK_SEARCH_PAGE`. Mutation
tables `docs/mutation/u79-a.md`, `u79-b.md` and `u79-c.md`, 25 rows at the cap,
25 killed on the first pass, three of them over guards that were given a test
before the table because the author could see the zero, read in
`u79-notes.md`. R-488 (the floor, the query and the page were never measured
against a live provider), R-489 (one row whose search fails every run refuses
the whole list, reachability unmeasured), R-490 (each differing run leaves the
earlier found list beside the new one) and R-491 (rows are searched one after
another) are filed, and none is on the board: R-489 could meet the bar and
says a producer has to be driven first. `CONCEPTS.md` gains Provider
candidate. The guide and the intake skill describe the route. **Owed to an
attended sitting:** one real typed tracklist, which is also the first live call
of `search_tracks` and R-488's measurement. Battery on the recorded tree: ruff
clean, `scan_repo.py` exit 0, pytest 8503 passed and 1 skipped in 71 seconds,
and no test of this unit's among the ten slowest.
**Main's highest residual number is R-491.**

**The session before: U84, issue #129, `relay/129`, 2026-09-19.**
`crate tag folder` repairs zeroed or progressive FLAC picture blocks in place,
without the web, which closes R-399's repair clause. New
`core/art.py:repair_in_place(path)` returns an `ArtRepair(status, detail)` and
never raises. A block is broken when it declares a zero width, height or depth,
or its data is not a baseline JPEG after a full decode, which is the source
system's `fix_flac_art` test (that file is at
`DJ_tools/src/dj_tools/DJ_tagging/fix_flac_art.py`, not at the path the brief
gave). Each broken block is re-encoded through `to_cdj_jpeg(size=None)` at
native resolution, and its width, height and depth come from the new bytes.
Its type, description and order are kept, and so is every sound block. Sound
art is never written, so its mtime holds. One unrepairable block makes the
file `error` with nothing written. **TWO DEPARTURES FROM THE BRIEF, both
deliberate.** A fifth status, `unchecked`, is reported for any container that
is not FLAC, because `none` would say "no art" where nothing looked. And
`/code-review` drove a native picture over the 450 KB cap being refused and
left blank for good, so `_repaired` shrinks such a picture into the 800 pixel
box, keeping its shape and never enlarging it, and the detail says so. The
source system saved over cap bytes instead. `tagging/tag.py:tag_one` runs the
repair BEFORE the has-genre return. `TagResult` gains `art_repair` and
`art_repair_detail`, NOT `art`, because `SearchHit.art` in the same file
already means picture bytes. The item artifact carries both keys, and
`progress.tagging.art_repair` counts every status, zero filled, skipping a
report committed before this unit. `/code-review` raised two findings. One was
fixed and one was filed as R-486. The `to_cdj_jpeg` failure paths were
then read as this unit's own, and the repair loop's catch was widened to
every exception. 23 new test cases by collected count, 8420 to 8443: 21 in
`tests/test_tagging_engine.py` and 2 in `tests/test_tag_workers.py`. Mutation
tables `docs/mutation/u84-a.md`, `u84-b.md` and `u84-a4.md`, 25 rows at the
cap plus one re-measure, 24 killed on the first pass and the one zero killed
after a test, read in `u84-notes.md`. R-486 and R-487 are filed, and neither
meets the board bar. **Still open under R-399:** the fetch for a file with no
art and the verb's art write (U85), and the registry summary. **Owed to an
attended sitting:** one repaired FLAC shown on a real CDJ or XDJ. Battery on
the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 8442 passed and 1
skipped in 71 seconds, and no test of this unit's among the ten slowest.
**Main's highest residual number is R-487.**

**The session before: U82, issue #127, `relay/127`, 2026-09-19.**
A landed sync pass can mark the playlists it finished, which discharges the
production half of R-358 and closes R-397 and R-398. `crate sync mark --xml X`
is `src/cratekit/sync/mark_cli.py`, registry entry `sync.mark`, appended at the
end of the tuple, `plan/1`, writes `remote`, destructive, one EXPLICIT gate
`sync.mark.confirm` with apply and abort and `digest_source="plan"`. X is the
intake file `intake land` wrote under the name `intake missing --run` printed.
The pass is found by that name: the playlist jobs whose own run spells it, on
this library. A playlist is planned only when its job SUCCEEDED and every track
its reports call `offered` or `missing` resolves now in `acquire match`'s
library view, counted `landed` when the intake file names the file, `owned`
when it does not, and `suppressed` when it has since been deleted on purpose.
One track outstanding leaves the playlist alone with the track named. The
other reasons a playlist is left out are `already-marked`, `not-listed`,
`job-unfinished` and `reports-unreadable`. The answered run marks through
`mark_swept` with a new `only` set, whose recheck against a second listing
skips a playlist that changed, reported `changed-since-plan`. A rename that
fails part way refuses naming what was already renamed: a refusal the account
raised keeps its reason, anything else is `internal-error`. An intake file of
no pass on this library is a gated plan of nothing, NO_OP under the warning
`sync-mark-no-pass`, decided before the account is listed, which is what lets
conformance 3 drive the verb on an empty install. **THE BRIEF NAMED THE
MANIFEST AND THE UNIT READS THE INTAKE REPORTS INSTEAD.** `/code-review` drove a
playlist marked over a track the pass had offered for review: the manifest is
a download list and drops offered rows and handed on rows. Filed under
`docs/solutions/integration-issues/`. The verb takes no `--manifest`.
`sync/marks.py`'s file check is one `os.stat` in `require_output`, every
`OSError` is `sync-marks-blocked`, and a permission error is re-slugged
`path-permission-denied` by `core.cause`. `playlists.marking_sweep` builds the
sweep WITHOUT reconciling, so the cursor is read, never written, and its policy
is unchanged. `playlists.playlist_of` and `missing_cli.job_reports` are new
public names. The name ban guard over `sync/cli.py` is deleted and replaced by
one that binds the account and asserts a pass renames nothing. A pass still
says `"mark": "unbound"`, R-481. `/code-review` raised ten findings, all
applied in whole or in part in one fix round. 37 new test cases by collected
count, 8383 to 8420: 30 in the new `tests/test_sync_mark.py` and 7 that
`tests/test_cli_contract.py` parametrizes over the new verb.
`tests/test_reserved_causes.py` re-pinned to 440 kebab literals, 281 non-keys
and 98 literal holders. Mutation tables `docs/mutation/u82-a.md` to `u82-d.md`,
25 rows at the cap plus one re-measure, 24 killed on the first pass and the one
zero killed after a test, read in `u82-notes.md`. R-481 to R-485 are filed.
**R-482 meets the board bar and its issue is owed**, to be filed after this
merge lands on `main`: a track accepted through review still holds its
playlist's mark back, because the mark resolves without the review store.
**Owed to an attended sitting:** the first live rename, which is Phillip's. No
rename has been made on a real account by this product. Battery on the
recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 8419 passed and 1
skipped in 63 seconds, and no test of this unit's among the ten slowest.
**Main's highest residual number is R-485.**

**The session before: U78, issue #123, `relay/123`, 2026-09-19.**
A finished `intake set` job now lists its missing tracks for download, which
closes R-401. `crate intake missing --job JOB` asks the catalogue, through a new
eighth `Catalogue` member `tracks_for_isrc(isrc)`, about every missing row that
carries no provider id, and only when such a row has a well formed ISRC, so a
job with none spends no login. The code is folded of hyphens and spaces and
upper cased first, and one question is asked per distinct code. Exactly one
distinct id in the answer lists the row with that id. No ISRC, a malformed one,
none filed, several filed (R-356, 2 of 4 rows live), or an answer holding a
track with no id hand the row on, each with a word in `why` (`none`,
`malformed`, `unknown`, `several`, `unreadable`) and a sentence in `reason`.
Handed on rows go to `<name>.unlisted.json` beside the list, a TEXT origin list
document `match run` reads, each line under a `#` row carrying its reason,
which the text reader skips. `listdoc` stays the one writer: `write` takes
`handed_on`, checks all three files before writing any, and `text_line` reads
every line back through the text reader. A row that would re-read as another
track or as none (an artist carrying ` - `, a leading ordinal, a leading `#`)
is not written. It is named on a failing `intake.missing.unwritable` check and
marked `in_file` false (R-478), and the verb refuses only when nothing at all
was written. A provider that cannot answer refuses `unavailable-transient` with
nothing written, and a product refusal from the catalogue passes through
unrelabelled. **THE TRAP:** tidalapi 0.8.11 raises `InvalidISRC` for every HTTP
error on that endpoint but 404 and 429, so the adapter treats only a not found
as an answer and lets `InvalidISRC` climb the ladder. Filed under
`docs/solutions/integration-issues/`. The outbound `match_track` still reads it
as no match, driven, R-477. The summary gains `by_isrc`, `unlisted_list`,
`unlisted_next`, and `isrc`, `why`, `reason` and `in_file` on each
`unlisted_tracks` entry. A job whose missing rows were all handed on is now OK
with the text list named, where U69 refused it. `/code-review` drove two
findings, both fixed: one unwritable row refused the whole verb under a remedy
that could not work, and a repeat run could refuse over provider order, now
sorted. The half it cannot fix, a catalogue that really changed, is R-476. 33
new test cases by collected count, 8350 to 8383: 15 in the new
`tests/test_intake_missing_isrc.py` over real set jobs, 9 in
`tests/test_listdoc.py`, 8 in `tests/test_label_tidal_catalogue.py` and 1 in
`tests/test_intake_missing.py`. Mutation tables `docs/mutation/u78-a.md` to
`u78-d.md`, 25 rows, 22 killed on the first pass and the three zeros killed
after a test each, read in `u78-notes.md`. R-401 is closed in place. R-475 (set
play order, the brief's decision), R-476, R-477, R-478, R-479 and R-480 are
filed. **R-477 meets the board bar and its issue is owed**, to be filed after
this merge lands on `main`: an outbound heart reports a track unmatched over a
lookup that failed. **Owed to an attended sitting:** one real set, identified,
listed, downloaded and landed, the first sitting `intake set` has had. Battery
on the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 8382 passed
and 1 skipped in 62 seconds, and no test of this unit's among the ten slowest.
**Main's highest residual number is R-480.**

**The session before: U83, issue #128, `relay/128`, 2026-09-19.**
The product has an art engine and no verb calls it yet. New `core/art.py` sits
beside `core/tags.py` and borrows its `_open` and `_save`, so both writers
classify containers through one table. Nothing was added to `tags.FIELDS`.
`to_cdj_jpeg(data, *, size=800, max_bytes=450_000)` returns a baseline RGB
JPEG with the dimensions Pillow reads back, at 800 by 800 or at native
resolution when `size=None`. It applies an EXIF orientation and flattens
transparency onto white first, and it raises `ArtError` rather than return
bytes over the cap. `write_front_cover(path, jpeg, *, max_bytes)` checks the
bytes BEFORE opening the file, refusing anything undecodable, not JPEG,
progressive, not RGB, or over the cap, so a refused write never touches the
audio file. It fills the FLAC block's width, height and depth from Pillow,
goes through `add_tags()` on AIFF and WAV, removes every existing picture, and
saves through `tags._save`. `read_pictures(path)` reports what a player is
told, a FLAC block's declared dimensions with zeroes kept, plus `progressive`,
`decoded` and the `format` Pillow measured beside the claimed `mime`. A file
that could not be read raises `UnreadableFile`, which is not an `ArtError`.
Ogg, Opus and unknown suffixes raise `tags.UnsupportedContainer`. While
building, the suite caught a ladder that stepped 88, 83 and on to 53 then 48
and never tried the floor of 50. `/code-review` raised ten findings: seven
fixed, two declined with the reason in the fix commit, one filed as R-473.
83 new test cases by collected count, 8267 to 8350, all in
`tests/test_art.py`. Mutation tables `docs/mutation/u83-a.md`, `u83-b.md` and
`u83-c.md`: 25 rows, 24 killed on the first pass and the save seam at zero,
because a lone ID3v1 trailer survives any save. The fixture was rebuilt with
both tags disagreeing and the row re-measured as killed, and
`docs/solutions/workflow-issues/` carries that trap. Six rows logged as
dropped. **R-399 is narrowed, not closed**: U84 (the repair pass) and U85 (the
fetch and the verb) still owe everything a user sees. R-471 (a non square
cover is stretched), R-472 (every picture type is removed), R-473 (a native
resolution picture over the cap is refused) and R-474 (failures return a
quiet False, as `write_tags` does) are filed, and none meets the board bar
while no verb calls the engine. **Owed to an attended sitting:** one file
written by this engine, shown on a real CDJ or XDJ. Battery on the recorded
tree: ruff clean, `scan_repo.py` exit 0, pytest 8349 passed and 1 skipped, and
no test of this unit's among the ten slowest.
**Main's highest residual number is R-474.**

**The session before: R-261 with R-393, issue #162, `relay/162`, 2026-09-19.**
A label sweep that could not read part of a label's catalogue now says so
instead of reporting a complete crawl. Two skips were silent before: a client
artist exposing `get_albums` and not `get_ep_singles` (R-261), and a discovered
artist whose listing hit a 429 during the BFS walk (R-393). Both skips stay,
because refusing the label would withhold everything the crawl did read. Each
now leaves a `label.catalogue.Unread` record (artist, listing, reason,
transient). `listing.artist_releases` takes an optional `skipped` collector.
`LabelRoster` carries `unread`: discovery's failed listings plus every member
missing a listing, since the roster always exposes both and a crawl over it
could never see the gap. `Catalogue.artist_for`'s docstring states that
contract. `sweep._crawl_or_refuse` returns the records beside the releases,
`LabelListing.unread` and `LabelSource.unread` carry them, and `label.cli`'s
worker refuses `label-sweep-incomplete` AFTER the increment, so every offer is
already durable. The refusal names each artist and listing. It is `resume-job`
and retryable when anything unread is transient, and `report-defect` when
only a missing method is. Discovery's listing climbs the ladder through
`tidal_catalogue._pause`, so the suite drives a 429 without sleeping 31
seconds. `/code-review` found one defect, fixed: an artist the roster already
holds was recorded when its discovery listing failed, although the roster
reads it again. No watermark moves either way, since the labels source never
acquires. 8 new test cases by collected count, 8259 to 8267: 7 in
`tests/test_label_tidal_catalogue.py` and 1 in `tests/test_adapter_listing.py`.
Mutation table `docs/mutation/r261.md`, 14 rows, 14 killed, one row logged as
dropped. R-467 (a discovery search 429 is still silent, the same shape one
loop over), R-468 (a held artist that failed in discovery is not expanded),
R-469 (a mixed refusal says resume) and R-470 (`tests/test_rebuild.py` flakes
25 tests on some full parallel runs, seen twice this session) are filed.
**R-467 and R-468 meet the board bar and their issues are owed**, to be filed
after this merge lands on `main` per METHOD's board bar. **Owed to an attended
sitting:** none; whether a live 429 happens during a label crawl stays
unmeasured. Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0,
pytest 8266 passed and 1 skipped, and no test of this unit's among the ten
slowest. **Main's highest residual number is R-470.**

**The session before: R-259, issue #161, `relay/161`, 2026-09-19.**
A label sweep no longer offers releases the library already holds, which
closes R-259 and, by the same change, R-137. The worker used to hand the
increment an empty owned set. It now builds `label.sweep.OwnedReleases`, a
container rather than a set: membership reads a release's tracks through
`Catalogue.release_tracks` and resolves each against the library index
`match_cli.library_view` builds, the one `label approved` uses. A release is
owned when it lists at least one track and every track resolves matched. No
track, an unreadable row, a track held only in another version, a release that
is gone, and a track read the provider could not answer all answer not owned,
so the release is offered. One instance goes to the source and to the
increment, so each release is read once, and the job shares one library walk
across its labels. Ownership is asked after verification now, so an
unconfirmed release is never read and the "confirmed none" refusal counts what
it did before. `LabelSource` hands the container to every label's listing, so
owned is dropped before the per label cap (R-137). `/code-review` found two
costs, and both were fixed: a library walk per label, and a failed track read
refusing the whole label. That read now offers the release, and three failures
in a row stop the asking. 13 new test cases by collected count, 8246 to 8259:
12 in `tests/test_label_workers.py` section 12 and 1 in
`tests/modules/test_labels.py`. Mutation tables `docs/mutation/r259.md`, 24
rows with 19 killed, and `r259-b.md`, which re-measured the two user facing
zeros after the tests they bought and killed both. Read them in
`r259-notes.md`. The three zeros left face maintainers and get a line each. A
first `r259` attempt had a null control that killed 25 tests in
`tests/test_rebuild.py`. It did not reproduce and was discarded. R-464 (harvest
offers a label the registry already holds, driven), R-465 (owned releases are
read again on every sweep) and R-466 (an offer whose ownership was not read
says nothing) are filed and not on the board. **Owed to an attended sitting:**
none. Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest
8258 passed and 1 skipped, and no test of this unit's among the ten slowest.
**Main's highest residual number is R-466.**

**The session before: U101, issue #146, `relay/146`, 2026-09-19.**
`crate label approved` consults the genre gate, which narrows R-420. It is the
first caller of `core/routing.gate_decisions`. The verb now reads every
accepted release first, runs the gate once per label over one genre per
release, and resolves and lists only what the gate passes. The share is a
fraction of a label's releases, so a release judged alone could never be held,
and one call per label is load bearing. A held release is never offered for
review and never listed. It is named on a `held.<release>` line with its
family, its count and the taxonomy's share, and in `summary.held`, never
silently dropped. The genre is what the catalogue's track rows report, read
from a mapping or an attribute. Rows reporting none, rows that disagree, and
every release of a label that had a release unread this run are listed and
named on a failing `ungated` line, since the gate cannot judge them. The last
case was the one `/code-review` finding and was fixed: the share moved with
which releases the provider failed on. A release naming no label is judged
alone, so it is never held. **No shipped catalogue reports a genre**, since the
streaming client carries none on an album or a track, so in the shipped build
every release is listed unjudged and the verb says so. That is what R-420 is
narrowed to. The taxonomy is `taxonomy.default_taxonomy()`, as in every other
verb. 16 new test cases by collected count, 8230 to 8246, all in
`tests/test_label_approved.py` against the fake catalogue. Mutation table
`docs/mutation/u101.md`, 23 rows, read in `u101-notes.md`: 21 of 21 new guards
killed, and two engine samples at zero. One was an equivalent mutant. The other
was the share bound, which bought a boundary test. R-462, the share is over one
sitting's acceptances, and R-463, a held release has no way through, are filed
and not on the board, since nothing is held in the shipped build. **Owed to an
attended sitting:** none. Battery on the recorded tree: ruff clean,
`scan_repo.py` exit 0, pytest 8245 passed and 1 skipped in 70 seconds, and no
test of this unit's among the ten slowest. **Main's highest residual number is
R-463.**

**The session before: U100, issue #145, `relay/145`, 2026-09-19.**
An accepted harvested label is added to the registry, which closes R-419. A new
action, `crate label registry adopt`, reads every `harvested-label` item on the
label release queue through a new `harvest.decided`, and hands the accepted
names to a new `RegistryStore.adopt`. It is a verb of its own, NOT a side effect
of `review resolve`, so answering a review stays a write to one store. A name
is present when it resolves the way every other verb resolves one, identifier,
then NFC folded display name, then slug, and the resolution runs inside the
registry lock against the entries the same run has added. So a label carried
over as `Sueño` under the source system's `sueno`, which slugs to `sue-o`
today, is reported as held and not filed twice (the R-381 hazard; R-381 itself
stays open), and two spellings accepted in one run add once. Adopt never
rewrites a held entry, unlike `add`, which re-adds by identifier and replaces
the display name. `RegistryStore.update` now skips the write when its mutator
returns `False`, and adopt uses that when it added nothing, because a save of
what `recognize` loaded drops any record it could not read. Rejected and open
items are counted in the summary and not added; a verdict this build cannot
read counts as open. A name that yields no identifier, and an accepted item
naming no label, each fail on their own check line keyed `adopt.<item id>` and
the rest still land. A name, `--to`, or any field flag on adopt refuses and
writes nothing. The outcome is `ok` when something was added and `no_op`
otherwise. The label catalogues skill and `docs/GUIDE.md` name adopt as the step
after accepting. `/code-review` raised no finding. 16 new test cases by
collected count, 8213 passed to 8229, all in the new
`tests/test_label_registry_adopt.py`, with the items offered by the real
`harvest.from_tracks` and answered through `review resolve` on the real
dispatcher. Mutation tables `docs/mutation/u100-a.md`, `u100-b.md` and
`u100-c.md`, 24 rows, read in `u100-notes.md`: three zeros, the write skip
twice and a refused name counted as present, each of which bought a test and
then killed. R-419 is closed in place. R-461, an adopt whose every accepted
label was refused exits zero, is filed and not on the board, since each
failure is on the screen and in the summary. **Owed to an attended sitting:**
none. Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest
8229 passed and 1 skipped in 66 seconds, and no test of this unit's among the
ten slowest.

**The session before: U99, issue #144, `relay/144`, 2026-09-19.**
The label registry verbs set a track limit and seed artists, which closes
R-418. `crate label registry add` takes `--track-limit N` and a repeatable
`--seed VALUE`, and a new `set` action edits a held entry without re-adding it:
`crate label registry set some-label --track-limit 100`. The store method is
`RegistryStore.edit`, NOT the `update` the brief named, because `update` was
already the store's locked read, modify, write, which `edit` calls. `edit`
resolves the entry inside the lock by identifier or display name, refuses
`label-unknown` by name rather than creating one, and keeps every field it was
not handed. A `--seed` list replaces the held one. The guards sit in the store,
so a Python caller is held to them too: a seed that starts with `id:` in any
case and is not `id:` followed by ASCII digits refuses, as does a blank seed,
because the adapter reads anything else as an artist name and would match
nobody; a track limit below one refuses, at the parser for the verb and in the
store for a caller. Each refusal writes nothing. A field flag on `list`,
`remove` or `rename` refuses rather than being ignored, and `set` with no field
refuses rather than reporting an edit. NO NEW CAUSE SLUG: every field refusal
reuses `label-name-invalid`, whose comment in `core/cause.py` is widened to
say so, so `tests/test_reserved_causes.py` is not re-pinned. `list` now names
the limit and the seeds in each check's detail, and carries every entry's JSON
in `summary.labels`. `Registry.by_name` compares NFC folded names through a new
`_name_key`, so an accented name typed decomposed still finds its entry, the
R-381 hazard; the slug itself is untouched and R-381 stays open as issue 97.
The helper is not called `_folded` because `rbxml._folded` already means NFC
and never case. The label catalogues skill gains a section on the two flags
and `set`, checked by the skills lint. `/code-review` raised no finding in the
diff and named one older gap in the same shape, `--match` ignored on `list`,
`remove` and `rename`, which the field flag guard now covers. 31 new test
cases by collected count, 8182 passed to 8213, all in the new
`tests/test_label_registry_verbs.py` and all but one driven through the real
dispatcher. Mutation tables `docs/mutation/u99-a.md`
and `u99-b.md`, 23 rows, read in `u99-notes.md`: one zero, the store's limit
floor behind the parser, which bought a store level test and then killed.
R-418 is closed in place. R-460, no verb clears the seeds or the limit back to
none, is filed and not on the board, since remove and add again keeps the
identifier and loses nothing. **Owed to an attended sitting:** none. Battery on
the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 8213 passed and 1
skipped in 64 seconds, and no test of this unit's among the ten slowest.
**Main's highest residual number is R-460.**

**The session before: U77, issue #122, `relay/122`, 2026-09-19.**
A landing given a manifest files its label tracks in the same intake file,
which closes R-402. `crate intake land --manifest M` reads the provenance
sidecar `label approved` writes, through a new `listdoc.read_manifest` that
refuses any version but its own whole. The manifest is read ONCE, before the
gate, for both its rows and a fingerprint of its bytes, in
`landing.read_label_manifest`. So a list passed where the manifest belongs
refuses before an answer is spent, the gate screen names every label playlist
listed, the bytes are in the plan digest, and `landing.apply` is handed the
fingerprint and refuses `decision-stale` with nothing moved if the file it
reads again is not the one that was shown. After the move and the splice,
`landing._file_labels` builds a `Wanted` for each row whose `source` is `label`
through `match.read_row`, resolves it with `match.resolve_one` over
`match.index_library` of the BATCH FOLDER ONLY, read with
`match_cli.library_template(cfg)`, and keeps only paths this call placed.
`insert_record_labels_tree` has its first caller through a new
`trees.insert_record_labels_trees`, one read and one atomic replace for every
label together, last name first so a new tree reads A to Z. One XML carries the
intake playlist and the tree. A row with no file, a row whose batch holds
another version and a row with no year are each reported by name, as an
`unfiled` plan item and a warning, codes `label-row-unmatched`,
`label-row-needs-review` and `label-row-incomplete`. The plan surface is closed
at four fields, so filed playlists and unfiled rows ride in `items` and
`totals`. EVERYTHING THE WRITER CAN REFUSE IS ASKED OF A COPY BEFORE THE FIRST
MOVE, in `trees.check_record_labels_tree`: the undeclared catalog tree, a
doubled folder or playlist, a held playlist it cannot extend and a tree the
database owns. A layout refusal reaches a person as `library-export-unusable`
with steps, not as the writer's `internal-error`. The registry is read once,
before the first move. A tree the disk refuses AFTER the moves is a
`label-tree-unwritten` warning per row over an intake file that stays, because
every landed file already has a routing intent naming it, R-456. The unit's
`/code-review` raised ten findings. Seven were fixed, two of them driven red
first: the trial handed every year an empty id list, so the writer returned
from a held playlist before its three layout refusals and the check passed an
export the write then refused after the moves, now filed under
`docs/solutions/integration-issues/`; and the batch index used the bare name
template, so a marked lossy file with no title tag matched nothing. One was
half fixed, the unmatched sentence is now true and its noise on a second
landing is R-457. Two are recorded and not taken: matching before the move,
R-455, because the brief decided the other way, and the second tag read, R-459.
The first caller hunt found the one failure the writer raises and does not
return, the database owned tree, driven to refuse before the moves, R-458. It
looked one file over for the empty trial shape and `insert_intake_playlist` has
no refusal that depends on its ids. 60 new test cases by collected count, 27 of
them in the new `tests/test_landing_labels.py`, and a tenth golden,
`land_label_tree`, named in `NOT_PORTED` so the count of ported goldens stays
nine. `tests/test_reserved_causes.py` is re-pinned for four new warning codes,
none a cause. Mutation tables `docs/mutation/u77-a.md`, `u77-b.md`, `u77-c.md`
and `u77-a2.md`, 25 rows, all killed, read in `u77-notes.md`. R-402 is closed
in place. R-455 to R-459 are filed and none is on the board: none loses data,
says something false, blocks a workflow or guards nothing. **Owed to an
attended sitting:** import one labelled intake file into rekordbox and read the
tree it makes. Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0,
pytest 8182 passed and 1 skipped in 66 seconds, and no test of this unit's among
the ten slowest. **Main's highest residual number is R-459.**

**The session before: U76, issue #121, `relay/121`, 2026-09-19.**
The catalog writer merges into a folder the document already holds, and refuses
a duplicated sibling, which closes R-129's writer half.
`rbxml.insert_catalog_folder`, the producer `trees.insert_record_labels_tree`
calls and still the only writer that emits a folder subtree, used to REPLACE a
held label folder. Now it merges into it. A year playlist it holds keeps every
member, including duplicates the document already carried, gains only the ids
it lacks, and has its `Entries` raised by that number. A year it lacks is placed
before the first held playlist whose name sorts below its own, and last when
none does, so each folder stays newest first. The folder's `Count` rises by the
playlists created. A self closed folder or playlist is opened first. Writing
the same catalog twice writes the same bytes, and that is pinned against the
single write golden `label_library_insert`. `_sole_child` gives
`direct_child`'s answers plus a fourth: two siblings of one name refuse at the
tree under ROOT, the folder under the tree and each playlist under the folder.
Merging into the first of two would leave a document that rekordbox doubles
again on import. Names compare through `_folded`, which applies NFC and never
case, R-453. `_merged_pairs` joins a caller's pairs by name and dedupes each
playlist's ids before anything is written. Every edit is made on a copy, so a
refusal writes nothing. A merge point whose tag shares its line with another
tag refuses rather than writing inside it. Still no caller in `src`, and that
is U77's work. The unit's `/code-review` drove one finding and it is fixed: a
new year was placed by the caller's own list alone, so the folder holding 2025
and the caller naming 2026 and 2024 wrote 2025, 2026, 2024. The hunt afterward
found the same first of two locate in the five other writers, R-454. 15 new test
cases, 14 in `tests/test_rbxml.py` and 1 in `tests/test_xml_splice_golden.py`.
The rerun test in `tests/test_tree_writer.py` now says merged. Mutation tables
`docs/mutation/u76-a.md`, `u76-b.md` and `u76-zeros.md`, 25 rows, 23 killed on
the first run and both zeros killed by a new test each, read in
`u76-notes.md`. R-129 is narrowed to its snapshot time reading. R-453 and R-454
are filed, and neither is on the board: R-453 closes only at an attended
sitting, and R-454 was not driven. **Owed to an attended sitting:** R-453's two
imports into a scratch copy. Battery on the recorded tree: ruff clean,
`scan_repo.py` exit 0, pytest 8122 passed and 1 skipped in 58 seconds, and no
test of this unit's among the ten slowest. **Main's highest residual number is
R-454.**

**The session before: U75, issue #120, `relay/120`, 2026-09-19.**
`crate label approved` turns the label releases accepted in review into the
list `acquire download` reads, which is the acquire half of R-402. It lists the
accepted items of kind `label-release` on the label queue BEFORE the catalogue
is resolved, so nothing accepted is a no-op that spends no login. Each accepted
release is read again by identifier through a seventh `Catalogue` member,
`release_tracks(release_id)`, returning the tracks and the year. Nothing a
review payload says about a track is used, because the 98 live rows carry a
memory address where the artist belongs, R-379. Every track is resolved with
`match.resolve_one`, a track held in another version is offered through
`match_cli.adjudicate` under the key `label.approved`, and only MISSING is
written, through `listdoc.write`, with provenance `source` label, `label_id`,
`label_name`, `year` and `release_id`. The same recording on two releases is
listed once, on the match id. There is no handed off state: ownership makes a
second run idempotent. The list is named `label-approved-` plus six bytes of
digest over the rows AND their provenance, in `approved_cli.list_name`, so the
same work rewrites the same bytes and any other work takes another name. The
new module is `label/approved_cli.py`, and the entry is `diagnostic/1`, not
destructive, no write surface, `adjudicates`. A release that cannot be read is
a failing check by KIND: `gone` and `no-identifier` end in
`crate review clear ITEM`, `provider` and `not-asked` end in run again. Three
provider failures in a row stop the asking, `OUTAGE_AFTER`. No release read,
nothing listable, nothing listed with releases unread, and a refused write all
refuse `label-list-unusable`, a new PRECONDITION slug, and a permission failure
stays `path-permission-denied`. The live adapter raises the seam's own
`catalogue.ReleaseUnresolvable` for a not found answer, at once and with no
retry, and reads gone from the class name or a 404 status and never from the
message. The unit's `/code-review` raised ten findings. Six were driven red and
fixed: `except LookupError` reading a `KeyError` as a withdrawn release, the
digits 404 in a request URL read as gone, permanent failures told to wait, no
outage bound, one unreadable row costing its release, and a name digested from
identifiers alone meeting the emitter's whole file comparison. One did not hold
as stated, since a permission failure was already a structured refusal, and its
`ENOSPC` half was fixed. Three are R-448, R-449 and R-451. The hunt after found
`PROVENANCE_SOURCE` meaning two things in two modules, renamed, and the same
two shapes one file over, R-450 and R-452. 71 new test cases, 41 in
`tests/test_label_approved.py` and 30 in `tests/test_label_tidal_catalogue.py`,
and `tests/test_reserved_causes.py` re-pinned by measured difference: causes
159 to 160, literals 423 to 427 with 268 non-keys, holders 96 to 97. Mutation
tables `docs/mutation/u75-a.md`, `u75-b.md`, `u75-c.md` and `u75-zeros.md`, 25
rows, 23 killing on the first run and both zeros killed by a new test each,
read in `u75-notes.md`. R-402 is narrowed to its tree half, which is U77's.
R-448 to R-452 filed, none on the board: no producer outside this unit was
driven, and R-450, the one that could meet the bar, says so and asks for that
drive first. One learning filed,
`docs/solutions/integration-issues/a-list-named-from-its-identifiers-meets-the-emitters-whole-file-comparison.md`.
The guide and the labels skill have a section on the verb. **Owed to an
attended sitting:** the first live call of `release_tracks`, whose album shape
was read off the installed client's source at 0.8.11 and never driven, and the
98 live offered releases, after review. Battery on the recorded tree: ruff
clean, `scan_repo.py` exit 0, pytest 8107 passed and 1 skipped in 67 seconds,
and no test of this unit's among the ten slowest. **Main's highest residual
number is R-452.**

**The session before: U91, issue #136, `relay/136`, 2026-09-19.**
`crate route unplaced --export X` places what the routing tree does not hold,
which closes R-313's placing arm. Every collection track that no playlist under
the export's routing tree holds, at any depth, is routed by the decision
`route inbox --export` makes, now one function, `routing_cli._decide`, and
written to `<X stem>_placed.xml` beside X through `trees.apply_unplaced_changes`,
the creating writer and now its first caller. The suffix is not `_routed.xml`, so
the sweep never replaces an inbox routing nobody has imported. A bucket with no
sub gets one, named in `totals.created`; a missing genre folder is a
`route-write-skipped` warning, never invented. A track filed anywhere under the
tree is left alone, even in a sub the rules would not pick. The tree is read as
a direct child of the playlist root, the writer's own scope, and an absent or
wrong typed tree refuses `governed-tree-absent`. A cut over routing tree refuses
`tree-unconverged` and an absent root `library-volume-unmounted`, through
`_refuse_off_the_bridge`, now shared with the inbox sweep. A written file ends
PENDING with a `rekordbox_import` action whose verify verb is `route.unplaced`;
no file is `route-blocked` when warnings were left and `nothing-to-route` when
not. The registry entry declares `xml` only, is not destructive and names no
gate, the brief's decision; the export path opens no database. Without
`--export` the verb is the R-313 report, and with nothing native it now carries
a `no-native-tree` warning naming `--export`. The unit's `/code-review` found
nothing. The hunt after it found the creating writer, over a bare LF line before
a genre folder's close, writing a file no parser reads as a success; the path
this verb calls now asks `rbxml._break_before` and warns instead, and the four
sibling inserts are R-447. 20 new test cases in `tests/test_routing_workers.py`, and
`tests/test_reserved_causes.py` re-pinned 422 to 423 distinct, 264 to 265
non-keys, for the plan kind `unplaced-export`. The route skill has a section on
the flag. Mutation tables `docs/mutation/u91.md` and `u91-b.md`, 24 rows, all
killing after two tests were added for the zeros, read in `u91-notes.md`. R-446
(the sweep does not rate) filed, not on the board. **R-447 meets the board bar
and its issue is owed after this merge**, titled from its ledger heading.
**Owed to an attended sitting:** one `_placed.xml` imported into rekordbox.
Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 8036
passed and 1 skipped in 56 seconds, and no test of this unit's among the ten
slowest. **Main's highest residual number is R-447.**

**The session before: U90, issue #135, `relay/135`, 2026-09-19.**
`crate analyze calibrate --vocal-cut N` sets the with vox cut by hand, which
closes R-374. The flag and the folder are mutually exclusive in the parser. A
cut outside 0 to 100, the presence score's range, or not a number, refuses
`vocal-cut-out-of-range`, a new PRECONDITION slug, and writes nothing.
`analysis/cli._write_vocal_calibration` is the one writer, used by the Otsu fit
and the hand cut alike. A hand cut is recorded as `method` hand, `note` "set by
hand on DATE" and `set_on` DATE. `write/metadata_cli.load_vocal_calibration` is
the one reader and returns the checked record, with the threshold converted to
a float. `load_vocal_threshold` wraps it and behaves as before. Both paths report
the cut they replace, and a fit over a hand cut names it as set by hand, with its
date. A corrupt calibration is replaced by a hand cut and reported as
unreadable. A file the account cannot open refuses the hand cut as
`path-permission-denied`. Under the fit it fails the vocal check rather than the
verb, because the energy calibration is already written by then. The fit's
report no longer says no routing pass reads the cut. The unit's `/code-review`
found one docstring promising a slug it did not name. Driven, the behaviour was
right, and the docstring now names `path-permission-denied`. The hunt after the
review found the fit refusing over its own energy write, and that is fixed. 19
new test cases in `tests/test_analysis_workers.py`, and `tests/test_reserved_causes.py`
is re-pinned for the slug. The `analyze-audio` skill gains a section on the flag.
Mutation tables are read in `docs/mutation/u90-notes.md`, 22 rows, 21 killing on
the first run, and the zero, C5, was killed by a new test. **Owed to an attended
sitting:** nothing. The live library's hand written 5.0 stays as the sitting
wrote it until the next hand cut or fit replaces it. Battery on the recorded
tree: ruff clean, `scan_repo.py` exit 0, pytest 8016 passed and 1 skipped in 55
seconds, and no test of this unit's among the ten slowest. **Main's highest
residual number is R-445.**

**The session before: U89, issue #134, `relay/134`, 2026-09-19.**
Calibrate, then file, and tracks land under "with vox". This closes R-276 and
R-417. `write/metadata_cli.load_vocal_threshold` is the one reader of the vocal
calibration. It returns None when the file is absent and refuses
`vocal-calibration-unreadable` when the file is corrupt, the R-342 body moved
rather than copied. `vocal_cut` keeps the default cut of 12.0 over it for My
Tags. Every routing caller that passed `vocal_threshold=None` now reads the cut
through that loader: the inbox apply, the export route, `converge`, both
workers and both resumes. `rebuild_governed_tree` takes the threshold with no
default. `governed_not_compared` takes the threshold the resume read, so the
R-316 warning fires only on an uncalibrated library. A resume reads the cut
before driving, so a corrupt file refuses before any item is claimed. On the
export medium a calibrated run calls `trees.add_vox_playlists`, its first
caller, on the bytes before routing. Each created sub is a plan item with no
track and a count in `totals.vox_created`, and a created sub counts as a change,
so a file is written. Every export item gains `vocal`, the vocal sub a track
also files into. The vocal writer's unreachable tree and per folder refusals are
`route-write-skipped` warnings. On the database medium the membership writer
creates the sub where a vocal track lands. `registry.py`'s `dj-vox-backfill`
claim and `CUT.md`'s `dj-create-vox-playlists` cut stay as written and are now
true. The unit's `/code-review` found two things, both fixed. The refusal's
delete step promised the default cut on surfaces where absence files nothing,
and the comments called the cut frozen when only its path is. The second
became R-445, not on the board. R-443 is narrowed to its taxonomy half.
23 new test cases in `tests/test_routing_workers.py`, and two existing ones there
now assert the threshold. Mutation table `docs/mutation/u89.md`, 21 of 23
killing; E6 was then killed by a new test, confirmed in `u89-e6.md`; R2 is a
maintainer zero. **Owed to an attended sitting:** one filing pass on the live
library after a calibration. Battery on the recorded tree: ruff clean,
`scan_repo.py` exit 0, pytest 7997 passed and 1 skipped in 63 seconds.
**Main's highest residual number is R-445.**

**The session before: R-313, issue #106, `relay/106`, 2026-09-19.**
`route.unplaced` now declares itself a report. The registry entry has no write
surface, is not destructive, names no gate, and asks doctor for
`library.mounted` and `rekordbox.pins`. `rekordbox.closed` and the cloud-sync
decision are gone, and no sweep was added. Driven with rekordbox and its agent
reported running and no acknowledgment recorded, `crate route unplaced`
reports both unplaced rows, leaves the database file byte identical and takes
no session lock. The brief said drop `rekordbox.pins` as well. The unit's
`/code-review` found that wrong: the writer checks the binding pin on every
open, and driven with the binding version patched the report refuses
`pyrekordbox-pin-drift`, exit 23, so the pins stay. Doctor's report is profile
wide and still requires rekordbox closed in `slim`, `full` and `custom`,
because the core write verbs declare it, so what `crate doctor` prints is
unchanged today. The route skill no longer says all four routing verbs want
rekordbox closed. 4 new tests in `tests/test_routing_workers.py`. Mutation
table `docs/mutation/r313.md`, 7 of 7 killing. R-444 filed, not on the board:
`converge` reads the database without declaring the pins, and the pins check
mixes a pin every open needs with one only a write needs. Battery on the
recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 7974 passed and 1
skipped in 59 seconds. **Main's highest residual number is R-444.**

**The session before: R-316, issue #107, `relay/107`, 2026-09-19.**
A declared vocal sub-playlist that a run did not derive is now said on the
envelope. A confirmed `crate route inbox` and a driven `crate rebuild --job` or
`crate route resort --job` carry a `vocal-dimension-not-compared` warning,
`{code, message}`, beside any `config-drift` warning. The shipped taxonomy
declares `with_vox` as additive and nothing reads a vocal calibration, so on
this build that warning is on every such run. The inbox apply keeps the gaps
`declared_membership` returns instead of dropping them, and the plan totals do
not change. The resumes cannot read the rebuild's report, because `handle`
still returns None and nothing persists it, so they ask
`rebuild.governed_not_compared()`, which applies `not_derived` to the shipped
taxonomy with no threshold. `not_derived` is the rule `derive_from_taxonomy`
now calls, and `not_compared_warnings` is the one wording. R-443 records that
choice and when it stops holding. A queue-only answer and a job finished on
entry carry no vocal warning. The export route is unchanged, since it already
reports the gaps as `totals.not_derived`, and a warning there would read as
`route-blocked`. Nothing derives vocals. The unit's `/code-review` found no
defect, and its one aside became a docstring correction. 10 new tests in
`tests/test_routing_workers.py`, and the kebab literal pin in
`tests/test_reserved_causes.py` moved 420 to 421. Mutation table
`docs/mutation/r316.md`, 14 of 14 killing, the first row restoring the dropped
gaps. R-443 filed, not on the board. Battery on the recorded tree: ruff clean,
`scan_repo.py` exit 0, pytest 7971 passed and 1 skipped in 59 seconds.
**Main's highest residual number is R-443.**

**The session before: U88, issue #133, `relay/133`, 2026-09-18.**
`crate route inbox --export X` now builds the "Sets and Long Tracks" playlist
as it files and rates, which closes R-406. Every collection track, not only
the intake, whose `TotalTime` is over the bound is added to one playlist that
is a direct child of the playlist root, in the same written file.
`TotalTime` is seconds, confirmed on the fixture and on
`intake/collection_xml.py`'s own emitter. The name and the bound are the
taxonomy's: a new optional `[long_tracks]` section with `id`, `display` and
`over_seconds`, keyed on presence like `[catalog]`. The shipped template
declares "Sets and Long Tracks" over 1200 seconds, the source system's values.
`over_seconds` defaults to 1200 when omitted, must be a whole number above
zero, and is strict, so exactly twenty minutes is not a member. The write is
`trees.add_to_root_playlist`, which is add only: the members the playlist
held are written back ahead of the new ones through one call of
`rbxml.insert_root_playlist`, now its first caller in `src`.
`trees.root_playlist_members` is the one read of those members, used by the
planner and the writer alike. A track already a member is not planned, so a
second run adds nothing and still answers `nothing-to-route`. A pass whose
only change is a long track writes a file and ends PENDING. No long track
means no playlist, never an empty one. An absent, non integer or zero
`TotalTime` is counted in `totals.duration_unreadable`, not warned, since a
warning would make every re-run `route-blocked`. A same named playlist inside
a folder is neither read nor touched. A FOLDER of that name at the root is a
`route-write-skipped` warning and is left alone, and the plan then offers
nothing for it. Each item gains `long_track`, and a long track outside the
intake gets an item of its own, so the additions are inside the digest. The
totals gain `long_added` and `duration_unreadable`, and the pending summary
names the additions. The unit's `/code-review` found nothing. Its one
observation, that a hand removal is undone by the next pass, is in R-442,
which also records the brief's add only decision. 22 new tests, 13 in
`tests/test_routing_workers.py` and 9 in `tests/test_taxonomy.py`. Mutation
tables `docs/mutation/u88.md` and `u88-b.md`, 21 of 25 killing, the four zeros
maintainer rows, read in `u88-notes.md`. R-442 filed, not on the board. Owed
to an attended sitting: the playlist seen in rekordbox after one import.
Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 7961
passed and 1 skipped in 59 seconds. **Main's highest residual number is
R-442.**

**The session before: U87, issue #132, `relay/132`, 2026-09-18.**
`crate route inbox --export X` now rates as it files, which closes R-405's
first clause. Every intake track the pass places whose export `Rating` is
empty or `"0"` gets the star value `routing.energy_rating` gives its energy,
the reading the routing decision already took, written into the same bytes
before the file is written through `trees.apply_rating_changes`, now its first
caller in `src`. The values are the export scale, 51 to 255, the taxonomy's
own, so R-414's database scale is not on this path and no database is
written. A rating a person set is never touched, a `rates = false` bucket
(NonElectronic, Chill / Ambient) is skipped, a track with no energy reading
is not rated, and a row with no `Rating` attribute is not planned, since the
writer patches a value and cannot add one. Each item gains `rating`, so the
ratings are inside the digest the person approves; the totals gain `rated`,
the writer's count; the pending summary names both counts. A pass that
inserts nothing but rates writes a file and ends PENDING, so a filed and
unrated track is never answered `nothing-to-route`. The re-spread after a
recalibration is NOT built and R-405 stays open for it. The unit's
`/code-review` found nothing; its one observation is filed as R-441, that the
import check now assumes rekordbox carries a rating onto a track it already
holds. 12 new tests in `tests/test_routing_workers.py`, whose U86 fixture
rows still carry no `Rating`. Mutation tables `docs/mutation/u87.md`,
`u87-b.md`, `u87-c.md`, 12 of 13 killing, the zero a maintainer row, read in
`u87-notes.md`. R-441 filed, not on the board, since it closes only at an
attended sitting. Owed to an attended sitting: the ratings seen in rekordbox
after one import. Battery on the recorded tree: ruff clean, `scan_repo.py`
exit 0, pytest 7939 passed and 1 skipped in 63 seconds.
**Main's highest residual number is R-441.**

**The session before: R-342, issue #108, `relay/108`, 2026-09-18.**
A corrupt vocal calibration now refuses instead of reading as the default cut,
which closes R-342. `write/metadata_cli.vocal_cut` still returns 12.0 for a
missing file. An existing file that cannot be read, or whose threshold is not
a finite number, a boolean, or too large for a float, raises
`vocal-calibration-unreadable`, a PRECONDITION declared in `cause.REASONS`
beside `energy-calibration-unreadable` and outside the reserved table, as that
sibling is. A permission refusal reaches the reader as `path-permission-denied`
through `cause.classified`, and still refuses. The remedy steps are prose,
because the write layer may not spell a CLI invocation. Driven before the fix:
`metadata mytags-vocals --apply` over a truncated calibration exited OK and
wrote the vox My Tags from 12.0; now it exits PRECONDITION and writes nothing.
The brief's `AttributeError` is not in the tuple, since this reader calls no
mapping method and a list payload raises TypeError, pinned by a test. The
unit's `/code-review` drove one finding, fixed: a four hundred digit threshold
raised OverflowError past the tuple. `tests/test_reserved_causes.py` re-pinned
population 157 to 158, non-reserved 133 to 134, distinct kebab literals 419 to
420, non-keys unchanged at 263. 14 new tests in `tests/test_metadata_cli.py`.
Mutation table `docs/mutation/r342.md`, 14 of 14 killing, the author's and not
independent. No residual filed. Battery on the recorded tree: ruff clean,
`scan_repo.py` exit 0, pytest 7928 collected, all passing but one skip.
**Main's highest residual number is R-440.**

**The session before: U86, issue #131, `relay/131`, 2026-09-18.**
`crate route inbox --export X` files the INBOX playlist of a fresh export on a
library whose routing tree has not cut over, which closes R-416 for the INBOX
half. It writes `<X stem>_routed.xml` beside X, atomically, never in place,
through `trees.apply_playlist_changes`, the non creating writer and now its
first caller, over the governed routing tree. The intake is the export's
intake folder, a direct child of the playlist root, not the disk folder. The
routing decision is the native path's: `rebuild.read_truth` reads each file the
export's Location names, through the prefix map, and `derive_from_taxonomy`
places it, so the file's genre wins over the export's `Genre` attribute. A
routing tree that has cut over refuses `tree-unconverged` before the plan is
offered, and the emitter guard refuses it again behind that. An absent library
root refuses `library-volume-unmounted`, an absent intake folder
`intake-flow-absent`. A key with no collection row, a Location naming no file
here, and a skipped write are warnings, and the track is not routed. A run
that inserted nothing writes no file; it answers `nothing-to-route` only when
it left no warning, and `route-blocked` otherwise, because `nothing-to-route`
is what the pending action's check reads. A written file ends PENDING with a
`rekordbox_import` action whose verify verb is `route.inbox` itself, taken from
the registry entry since the write layer may not spell a verb. Without
`--export` the `no-native-tree` answer now carries a warning naming
`--export`. The registry entry writes `xml` as well. The unit's `/code-review`
drove one finding, fixed: a run whose every write was skipped answered
`nothing-to-route`. The same shape one step earlier, every file unreadable, was
found by the author and fixed. `tests/test_reserved_causes.py` re-pinned 413 to
419 distinct, 257 to 263 non-keys, none a cause. 18 tests in
`tests/test_routing_workers.py`. Mutation tables `docs/mutation/u86.md` and
`u86-b.md`, 19 of 24 killing, the five zeros maintainer rows, read in
`u86-notes.md`. R-439 and R-440 filed, not on the board. Owed to an attended
sitting: one routed file imported into rekordbox. Battery on the recorded
tree: ruff clean, `scan_repo.py` exit 0, pytest 7913 passed and 1 skipped in
59 seconds. **Main's highest residual number is R-440.**

**The session before: U74, issue #119, `relay/119`, 2026-09-18.**
`crate sync all` queues the account's hearts even when the outbound confirm is
declined, which closes R-423. `SourceSpec` gained `inbound_key`, set to
`intake.playlist` on the favourites spec alone, so the half runs only when the
favourites module is enabled and the `PLANNERS` to `SPECS` pin did not move.
`_plan_favorites` plans the half FIRST, into an `_Inbound` on the plan with its
own queue callable, refusal and jobs, and then catches the outbound export
refusal itself, because raising it to `_plan` built a fresh plan and dropped
the read. The hearts are listed at plan time through `intake.cli.list_playlist`
with the reserved reference and queued with the shared `run_id` and `source_id`
favorites, exactly as `crate intake playlist favorites` queues them. An open
hearts job for this library, from a pass or queued by hand, holds the half as
`in-flight`; an empty listing is `empty`; both reuse `playlists.Excluded`, so
no kebab literal was added and `tests/test_reserved_causes.py` did not move. A
catalogue refusal is recorded against the half and the other sources run. The
summary gains `favorites.inbound`, the checks gain `sync.favorites.inbound`,
the gate screen gains `inbound`, the job counts toward `queued` and
`sync.next`, and a hearts refusal joins the refusal list after the outbound
one, so a declined pass it alone stopped is that refusal, not a no-op.
`not_queued.favorites` is still the outbound half only. The unit's
`/code-review` drove two findings, both fixed: the check said "not listed" over
a queue refusal, and the gate screen said nothing about the read. Mutation
tables `docs/mutation/u74.md` and `u74-b.md`, 24 of 24 killing, read in
`u74-notes.md`. R-438 filed, not on the board: a full pass opens the catalogue
twice. Issue 110, the board's record of R-423, closes by keyword in this
branch's record commit when `main` is pushed. Owed to the `sync all` sitting: one live
pass with the heart count compared against the account's 197. Battery on the
recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 7895 passed and 1
skipped in 53 seconds. **Main's highest residual number is R-438.**

**The session before: R-239, issue #156, `relay/156`, 2026-09-18.**
Every open of the rekordbox database asks the file whether it needs the key,
which closes R-239. `rb_writer.open_db` and `rb_writer.integrity_ok` default
`unlock` to `None`, and `None` asks `unlock_needed(target)` just before the
binding is constructed. No caller in `src` names an answer, and
`test_no_caller_in_src_answers_the_key_question_for_itself` in
`tests/test_rb_writer_db.py` walks the source and refuses one, exempting by
shape only `integrity_ok` forwarding its own argument. Five verb sites passed
`unlock=False` and failed at the open on every real, encrypted library:
`route inbox`, `route unplaced`, `route pending`, `rebuild` and `converge`, and
`converge` answered "not compared" for every native tree. The session read-back
and the snapshot capture check used the old `True` default and failed on a
plain database; both now ask. `deletion.cli._needs_unlock` is gone. **The suite
now builds an ENCRYPTED disposable database**, `_encrypt_in_place` in
`tests/test_rb_writer_db.py`, through `sqlcipher3` and the binding's own key,
and a test proves it refuses to open with the key withheld. Driven on it through
the command line, `route inbox`, `route unplaced`, a queued `rebuild` and
`route resort`, and `converge` each failed before the fix and pass after it.
`tests/test_routing_workers.py` no longer patches `integrity_ok` to
`unlock=False`, since that patch refuses an encrypted capture; other write
suites still carry it harmlessly. `tests/test_reserved_causes.py` re-pinned the
also-holds-an-integer half 19 to 18, holders still 96, because
`deletion/cli.py` lost its bare 16. Mutation tables `docs/mutation/r239-a.md`
and `r239-b.md`, 21 rows, 20 killing, read in `r239-notes.md`; the zero is the
unreadable file branch of the probe, maintainer facing. The learning is
`docs/solutions/integration-issues/an-encrypted-library-can-be-built-in-the-suite-so-the-key-path-needs-no-real-snapshot.md`.
No residual filed. Owed to an attended sitting: one read verb, `route unplaced`
or `converge`, run against the live library to see it open. Battery on the
recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 7876 passed and 1
skipped in 55 seconds. **Main's highest residual number is R-437.**

**The session before: U73, issue #118, `relay/118`, 2026-09-18.**
`crate intake missing --run RUN_ID` writes ONE list for a whole `sync all`
pass, which closes R-403 and records R-130 as superseded. `--job` and `--run`
are a required exclusive pair, and `--run` writes dest `sync_run`, because the
dispatcher's global `--run` reads `args.run` to load a gate run and a
subcommand flag of that name hands it a sync run. The jobs are the intake jobs
whose payload `run_id` is the run AND whose `library_id` is this library's.
Any open job refuses the run, naming each with its resume command. A failed or
cancelled job is named and refuses unless `--skip-failed`, which lists the rest
and reports the skipped as a failing `intake.missing.skipped` check; a run whose
every job was skipped, or whose skip leaves nothing listed, refuses rather than
reading as a no-op. `--skip-failed` with `--job` refuses. Missing rows are
unioned oldest job first into one `listdoc.write` named `<run without
colons>_synced`, first source wins, and `listdoc.Provenance` gained
`source_refs`, written to a manifest entry ONLY when an id came from more than
one reference, so a single source manifest keeps its earlier bytes and a repeat
listing is not refused. The output names the download and `intake land --export
XML --name <run>_synced`. `crate sync all` ends with one `sync.next` info check
naming `crate intake missing --run RUN_ID` whenever the pass filed an intake
job, and `summary.next` carries the same command or None. `_append_intake` is
left unreachable, R-437, maintainer facing and not on the board. Mutation tables
`docs/mutation/u73.md`, `u73-b.md`, `u73-c.md`, 22 rows, 21 killing, read in
`u73-notes.md`. `tests/test_reserved_causes.py` did not move: no new kebab
literal. Owed to an attended sitting: one `sync all` through to a landed
`_synced` intake file. Battery on the recorded tree: ruff clean, `scan_repo.py`
exit 0, pytest 7858 passed and 1 skipped in 56 seconds. **Main's highest
residual number is R-437.**

**The session before: U72, issue #117, `relay/117`, 2026-09-18.**
`crate intake land [FOLDER] --export XML [--name NAME]` lands a staged batch,
which closes R-413. It is `src/cratekit/intake/land_cli.py`, registry entry
`intake.land`, appended at the end of the tuple, `plan/1`, writes `xml` and
`files`, destructive, one gate `intake.land.confirm` with apply and abort and
`digest_source="plan"`. FOLDER defaults to download staging and NAME to the
run id with its colons removed, since a colon cannot be in an exFAT folder
name. The batch goes to `library.root / music_dir / NAME` and the intake file
to `library.root / NAME_inboxed.xml`, a suffix `pending_intake_xml` walks. The
first run stops at the gate and moves nothing, and the gate screen shows the
folder, where the files land, the intake file and every file name. The digest
covers folder, batch, target, intake file, export and the engine fingerprint.
An answered run ends PENDING, exit PENDING_HUMAN, with a `rekordbox_import`
pending action naming the intake file, `verify_verb` `route.pending`, `blocks`
empty. A file the engine refused is a warning and is marked in the payload.
**An empty folder is a plan of nothing, not a refusal**, gated and then NO_OP,
because conformance 3 drives every gated verb to OK on an empty library and
`name apply` and `route inbox` set the precedent; the engine gained a public
`landing.listing` for it. GUIDE's acquisition walkthrough now runs tag, name
with `--root` staging, land, route inbox, route pending, and the gate table has
the new row. Mutation tables `docs/mutation/u72.md` and `u72-b.md`, 24 rows,
all killing, read in `u72-notes.md`. R-432 is now reachable through this verb
and narrowed by the unique default name. R-436 filed, not on the board: before
any tree is database native, `route pending` answers OK without reading the
import it is named as verifying. `tests/test_reserved_causes.py` did not move,
since the new module names no cause. Owed to an attended sitting: one real
staged batch landed and imported, the same sitting U71 owes. **Main's highest
residual number is R-436.**

**The session before: R-359, issue #104, `relay/104`, 2026-09-18.**
Swept means resolved, not acquired, and `crate sync all` now says so on both
surfaces. Every playlists block in `summary.playlists` carries `swept_means`,
`resolved-not-acquired`. The `sync.playlists` check, which is what the default
human output prints for this verb, ends with one sentence: a recorded playlist
had its tracks resolved, not acquired, a missing track is still not in the
library, `crate intake missing` lists it, and no later sync offers that
playlist again. The words are `playlists.said(block)`, read off the block's own
token and handed to `_check` through a new `_Plan.note`, so dropping the field
drops the sentence. The sentence shows on every pass that reaches the
playlists planner, recorded or not. `reconcile` and the cursor are unchanged
and nothing composes `acquire download`. The guards drive the real producer, a
succeeded intake job with two missing tracks and none acquired, through json
and through `cli.run` in the default human mode. Mutation table
`docs/mutation/r359.md`, 11 rows, all killing, null control 0 of 7814.
`tests/test_reserved_causes.py` re-pinned to 413 kebab literals and 257
non-keys, for the one new token. No residual filed. The one other surface
that reads the cursor, the doctor's `source.playlists.watermark` row, prints
counts and a time and never the word swept, so it claims no acquisition.
R-435 filed, maintainer facing and not on the board: one full parallel run
errored in the setup of a real database deletion test this branch does not
touch, then passed alone, on the next full run, and on three runs of its file.
Battery on the recorded tree: ruff clean, `scan_repo.py` exit 0, pytest 7813
passed and 1 skipped in 48 seconds. **Main's highest residual number is
R-435.**

**The session before: U71, issue #116, `relay/116`, 2026-09-18.**
The landing engine, `src/cratekit/intake/landing.py`, moves acquired files
out of download staging into the library and splices them into one intake
file, which closes R-413's engine half. `plan(folder, cfg, batch)` lists the
folder one level deep, audio only, skipping dotfiles and
`.cratekit-acquire-staging`, and fingerprints each item by name, size and
modification time. `apply(plan, cfg=, export=, destination=)` lists the
folder again and refuses a stale plan as `decision-stale`. Every whole batch
refusal runs before the first move: an absent library root, a source folder
inside the library that is not staging, a target under staging, a staging
folder on another device (refused by name, never copied), an existing intake
file, and every export refusal `place_files` makes, tried on a copy. Files go
to `library.root / music_dir / <batch>` by `os.replace` only. A file whose
target exists is refused alone and never replaced, and a file with no
declared sub is left in staging with a sentence naming `crate tag folder`.
Driven: an untagged file lands in `electronica_other` / `unsorted`, so the
shipped taxonomy never takes that branch. `place_files` runs over the moved
paths, and `Landed.placed` carries each TrackID for the label tree unit. A
failure after the first move names the moved files, which stay in the
library, and leaves no intake file and no empty batch folder. **No verb
calls it yet**, which is R-413's open half. R-432 (a check then replace
window), R-433 (`place_files` leaves its session open) and R-434 (a landed
batch marks nothing lossy) filed, none on the board, since no shipped verb
reaches them. Mutation tables `docs/mutation/u71.md`, `u71-b.md` and
`u71-c.md`, 25 rows, all killing after one test was strengthened, read in
`docs/mutation/u71-notes.md`. `tests/test_reserved_causes.py` re-pinned to 96
literal holders, measured as a set difference. Main's highest residual
number was then R-434. Owed to an attended sitting: one real landed batch imported
into rekordbox.

**The session before: U69, issue #114, `relay/114`, 2026-09-18.**
`crate intake missing --job JOB` writes the list document `acquire download`
reads, from a finished intake job, the first verb to call `listdoc.write`. It
is `src/cratekit/intake/missing_cli.py`, registry entry `intake.missing`,
`diagnostic/1`, no write surface, not destructive, no gate. It reads the
job's committed reports with the frozen config and lists only `missing` rows,
so owned, offered and suppressed are counted and left out. The list goes to
`<download_staging>/lists/intake-JOB.list.json` with its manifest, provenance
`playlist` and the job's source, or under `--out`. It refuses, as
`intake-list-unusable`, a job that is not succeeded, a job with no items,
reports that do not cover the items one for one by identifier, a report with
an unreadable state, an `--out` that is a file, and a job whose missing rows
none carry a provider id. A job of another verb is `job-unknown`. A mixed job
with some unlisted rows writes the rest and shows a FAIL check. The human
output names the path and the literal next command, and it is driven through
`cli.run` in the default mode. The written list is queued and downloaded by
the real download verb against `FakeAdapter`. R-400 and R-423 narrowed,
neither closed. **R-431 filed and on the board.** A deleted track whose
tombstone the consult cannot reach, R-69's `UNRECONCILED` shape, is now
listed for download. It is pinned by a test that fails when it closes. Mutation tables
`docs/mutation/u69.md` and `u69-b.md`, 19 of 20 killing. The zero is inert,
because the job queue is installation scoped, and is read in
`docs/mutation/u69-notes.md`. `tests/test_reserved_causes.py` re-pinned to 95
literal holders, measured as a set difference. **Main's highest residual number
is R-431.** Owed to an attended sitting: one real `intake playlist`, `intake
missing`, `acquire download` on a small playlist.

**The session before: U70, issue #115, `relay/115`, 2026-09-18.**
`crate intake playlist favorites` answers "is every heart in my library". The
reserved reference `favorites` is checked in `intake.cli._playlist_rows` before
`playlist_for` could see it, and lists the account's hearts through a sixth
`Catalogue` member, `favourite_tracks`, which `TidalCatalogue` answers through
`listing.favorite_tracks` and refuses when the client exposes no favourites.
The rows go through the same reader, freeze and worker a playlist uses, so each
heart reports owned, offered or missing by the match engine's one rule; a heart
held in another version is offered, not owned. The job is an `intake.playlist`
job whose source is the canonical `favorites`, so the resume argv is unchanged,
with `source_id` favorites. The listing crosses
`label_cli.favourite_tracks_or_refuse`, the playlist boundary's twin, so
`ListingTruncated` refuses whole as `label-playlist-unreadable` and an adapter's
own refusal passes through. No placeholder playlist, no account write, no
cursor: a re-run is idempotent through ownership. `tests/label_fakes.py`
declares six methods and `FakeCatalogue(hearts=...)` answers the sixth; a test
holds the fake's set equal to the protocol's. `intake missing` landed in the
unit after, U69, which drove the hearts through to a download on fakes;
R-423 is narrowed, not closed. R-429 and R-430 filed, neither meeting the board
bar. Mutation table `docs/mutation/u70.md`, 14 of 14 killing, null control 0 of
7751. **Main's highest residual number is R-430.** Owed to an attended sitting:
one live run of `crate intake playlist favorites`, with the heart count
compared against the account's 197.

**The session before: U68, issue #113, `relay/113`, 2026-09-18.**
The product has a writer for the list document `acquire download` reads, which
closes R-400's engine half. `src/cratekit/acquire/listdoc.py` is ONE shared
emitter, not a document per source, and it is pure. `rows_of` takes `Wanted`
tracks or `frozen_tracks` items. `document` builds `{"list": 1, "origin":
"tidal", "tracks": [...]}`, reading every listed row back through
`match.read_row` first, so a row the reader would refuse is refused here by
position as `ListDocRefused` rather than costing the whole list. `write` puts
`<name>.list.json` and a `<name>.manifest.json` provenance sidecar into a
directory through `config.atomic_write_bytes`. Every file check runs before
either write: an absent file is written, an identical one left alone, and a
different one refuses. No listable row writes nothing and returns `None` paths.
First id wins, compared stripped. A row with no provider id, or a `Wanted` from
another service, comes back `unlisted` and is never written. A `Wanted` is
written in the source's own spelling when that re-reads to the same version
token, otherwise as its raw title plus its declared version; writing the split
title instead lost bracketed parts and featured credits, which the unit's
`/code-review` drove and the unit fixed. **Nothing calls `write`
yet**, which is R-400's open verb half and the entrances' units. A frozen
mapping re-reads as the plain record, which is R-428, filed without an issue.
Mutation table `docs/mutation/u68.md`, 23 rows, 20 killing, null control 0 of
7733, the first real table the driver has run under parallel workers, and its
collected counts held at the baseline. Two zeros were equivalent comparisons,
since removed; the third is a maintainer zero, read in
`docs/mutation/u68-notes.md`. **Main's highest residual number is R-428.**
Nothing is owed to an attended sitting. Battery at the branch head: ruff clean,
7,732 passed and 1 skipped, scan clean.

**The session before: U67, issue #112, `relay/112`, 2026-09-18.**
`name apply` never renames or retags a file the rekordbox collection references,
which closes R-407, the one open finding that could lose data library wide.
`write/naming_cli._recorded` reads every row's `FolderPath`, tombstones
included, through `rb_writer.open_db` with `require_closed` False, the
`metadata_cli` pattern, because `tests/test_layering.py` forbids `write` from
importing `adopt.collection`. `_referenced` keys each row as recorded and as
prefix mapped, NFC normalised and casefolded; `_is_referenced` asks a
candidate's absolute and resolved spellings. `_plan_for` marks each item
`"action": "rename"` or `"referenced"`, both in the digest, `totals.count`
stays the rename count and `totals.referenced` is new. `name_apply` reads the
collection AGAIN after the gate and re-checks each item before the rename. Any
failed read refuses as the new slug `collection-unreadable`, exit 25, carrying
the inner cause and its remedy; there is no force flag. **The read is skipped
when nothing would be renamed**, because the conformance suite drives this
verb over a library with no database and the collection cannot change an
empty outcome. Every other test in `tests/test_naming_apply_cli.py` stubs
`_recorded` as a read, empty collection; the U67 tests use a disposable
database. **A library with cloud sync ON now refuses `name apply`**, since the
read open's canary refuses it; kept, recorded as R-425. The at-risk population
re-pin moved 156 to 157 causes and 411 to 412 literals. Mutation tables
`docs/mutation/u67.md` and `docs/mutation/u67-round-2.md`, 21 rows, all killed
after round two added a collision test for the existing target claim, which
had none. New residuals R-425 to R-427. **R-426 meets the board bar**, a row
recorded through a link is unprotected, and its issue is owed after this
merge. **Main's highest residual number is R-427.** Owed to an attended
sitting: one plan only run against the live library to read `referenced`.
Battery at the branch head: ruff clean, 7,698 passed and 1 skipped, scan clean.

**The session before: the battery speed chore and the Phase G plan, `chore/battery-speed`, 2026-09-18.**
Attended, not a board unit. Four things landed together.
**The suite is parallel.** `addopts` carries `-n auto` and the dev extra carries
`pytest-xdist`. Measured on 11 cores at 7,678 tests: 532 seconds serial, 86 at
eight workers, 61 to 67 at auto, green each time including the disk image tests.
A venv older than this merge needs `pip install -e '.[dev]'` once. `-n 0` runs
in process, for a debugger. `scripts/mutate.py` inherits `addopts`, so its
baselines are parallel too. Its reporting plugin now writes from the xdist
controller only and reads the collected count off
`pytest_xdist_node_collection_finished`, and the driver scrubs the inherited
`PYTEST_XDIST_WORKER` identity from its child. Three tests in
`tests/test_mutation_driver.py` drive it against a fixture with `-n 2`. **The
driver has NOT yet run a real table under parallel workers**, so the first unit
to run one should read its null control and collected counts with that in mind.
**A product defect came out of the slowest test.** `listing.fetch_with_retry`
retried a `credential-missing` refusal five times and slept 31 seconds before
re-raising it, per listing. A `CratekitError` whose cause says
`retryable=False` now passes through on the first attempt, and a paired test
holds that a retryable refusal still climbs the ladder. No mutation table was
run over this change, it is two lines behind two new tests.
**The ledger gained R-413 to R-424**, twelve entries from the reads that planned
Phase G: the landing gap R-413, the rating scale hazard R-414, a correction to
R-400's wording R-415, the uncalled export routing writers R-416, six smaller
parity gaps, and the two entries issues 110 and 111 said they were owed, R-423
and R-424.
**METHOD changed.** Native Relay is in the loop and has a section. The
serialized order list is gone, spent. A board bar says which residuals earn an
issue, and a session now files that issue itself. The battery section says the
full suite is the merge gate and not the edit loop.
**The board gained Phase G**, units U67 onward, plus a card for every residual
that met the bar, from `docs/ideation/2026-09-18-parity-to-feature-complete.md`.
The two analysis tests near 30 seconds each spin a real process pool and were
left alone. Battery at the merge: ruff clean, 7,678 passed and 1 skipped, scan
clean.

**Two sessions before: R-358 code half, issue #105, `relay/105`.**
`modules.outbound.service.RemoteAccount` declares a seventh member,
`rename_playlist(playlist_id, name)`, and `TidalAccount` implements it over the
playlist object `add_to_playlist` already edits. A retitle is not a removal, so
the add-only scans still pass. Three refusals: a playlist the session does not
own comes back without an editor, the client answering `False` is a refused
write rather than a raise, and a blank title is `internal-error` at source
scope, spelled here rather than through `provider_failure`, because the client
reads a falsy title as keep the current one and answers True. The retry is kept,
unlike a create's, since a retitle asks for one fixed title.
`sync.playlists.pending_marks` and `mark_swept` are the application.
**The mark set is the WHOLE cursor, `Sweep.recorded`, not `recorded_now`**, and
the recheck is a second fresh listing, not the plan's own read. Both were review
findings; the first is the learning below. `mark_swept` takes an optional
`applied` list appended to as each rename lands, on `queue`'s pattern.
**Production is deliberately unwired.** No sweep writes an importable file, so
nothing calls `mark_swept`, `sync.cli` still reports `"mark": "unbound"`, and a
guard over `sync/cli.py` holds that until the live half is done. The report
block gained a `marked` list, and `"mark"` now separates a step that never ran
from one that ran and marked nothing. The at-risk population re-pin moved 93 to
94: `tidal_account.py` names a cause literal for the first time. Mutation tables
`docs/mutation/r358.md` and `docs/mutation/r358-round-2.md`, 20 rows then 4,
ending 18 of 20 killing, null control 0 of 7672 and 0 of 7674, no collect drift,
every restore verified against `git show HEAD`. The two surviving zeros mutate
test code and are recorded as such. The live mark stays attended and is
Phillip's. New residuals R-397 and R-398. The learning is
`docs/solutions/integration-issues/a-set-shaped-cursor-that-commits-before-a-side-effect-makes-the-next-increment-will-see-it-again-false.md`.
**Main's highest residual number is R-412**, not R-398. A docs merge landed after
this unit: the parity audit against DJ_tools, fourteen findings, R-399 through
R-412. They were numbered 397 through 410 on their branch and each moved up by
two at the merge, because this unit already held 397 and 398. R-400 is their
common cause, the list document `acquire download` reads and nothing produces.

**Three sessions before: R-368, issue #101, `relay/101`.**
`crate restore run` takes `--target DIRECTORY`, a database restore into a
directory that is not the live library, which is how a restore is rehearsed.
Valid only with `--from-backup`. It rolls no session back: a named session
refuses, `--discard` refuses, and the default that means the newest spendable
capture is suppressed. Omitting the flag is the live restore unchanged. Two
destination refusals share `restore-target-is-live-root`, the target being the
library root or holding it or sitting inside it, and the database landing on
the live one, which is the acknowledged outside-root layout that containment
cannot see. The two invocation refusals share `restore-target-invalid`. Both
slugs live in `core.cause.REASONS` and not in the reservation table, which
reserves what a module's refusal enum raises. A target that is not a directory
still raises `restore-target-absent` from `plan_restore`. The target and
`dry_run` are both digested into the offer, the second being a hole this
branch's review found one flag over. The branch's review also found the
guard comparing resolved paths as strings, which accepted a case folded
spelling of the live library on the filesystems this product runs on; both
checks ask `samefile` now. Mutation tables `docs/mutation/r368.md` and
`docs/mutation/r368-round-2.md`, 16 rows then 5, ending 21 of 21 killing, null
control 0 of 7649 and 0 of 7651, no collect drift, every restore verified
against `git show HEAD`. R-368 is closed against its RESTATED close and is not
fully closed: a rehearsal still takes the live library lock and still needs
rekordbox gone, which is R-396. The learning is
`docs/solutions/integration-issues/a-resolved-path-compared-with-equals-is-not-a-same-directory-test.md`.

**Two sessions before, 2026-09-18, R-352, issue #94, `unit/issue94-the-adapter-s-roster-is-narrower-than-th`.**
After own page and seeds, `TidalCatalogue.artist_for` searches the label
name and numbered compilations `001` through `079`, keeps copyright matches
via Cratekit `labels_from_copyright` and `labels_match`, and walks credited
artists through `session.artist` and `listing.artist_releases`. Discovery
runs when the roster is already non empty. An unresolved seed still refuses
first. A rate limited album query skips that query and keeps a resolved own
page. `AuthenticationError` on search still refuses. Catalogue members are
unchanged. The V/A shortfall is R-392. Mutation table
`docs/mutation/r352.md`, 17 of 17 killing, null control 0 of 7633, no
collect drift, every restore verified against `git show HEAD`. R-352 is
closed in place. The learning is
`docs/solutions/workflow-issues/a-search-fake-that-returns-every-album-cannot-catch-numbered-results-being-ignored.md`.
Main's highest residual number is R-394.

**The session before, 2026-09-18, R-351, issue #93, `unit/issue93-a-seed-artist-cannot-be-pinned-by-identi`.**
A seed of the form `id:<digits>` is looked up via `session.artist` with no
search. A name seed stays exact fold and still refuses when two provider
artists carry that name. An identifier seed plus a colliding same name
artist succeeds. A missing identifier refuses the label. A provider outage,
and a KeyError or IndexError, is not read as absence. `ObjectNotFound` is
the live client's missing shape. Bare `LookupError` is the fake's.
Registry `add` stores `id:` seeds. Catalogue members are unchanged.
Discovery landed as issue 94. Mutation
table `docs/mutation/r351.md`, 13 of 13 killing, null control 0 of 7619, no
collect drift, every restore verified against `git show HEAD`. R-351 is
closed in place. The learning is
`docs/solutions/workflow-issues/a-lookuperror-stand-in-cannot-catch-the-clients-object-not-found.md`.
Main's highest residual number is R-391.

**The session before, 2026-09-18, R-380, issue #92, `unit/issue92-a-job-whose-failures-are-permanent-repor`.**
A job whose every item failure is non retryable reports itself non retryable
and does not offer resume-job. When those failures share a reason, that
reason is the job's reason. A mixed job that still has a retryable failure
stays retryable and names both counts. `no-evidence` stays the all failed
slug; its retryable flag follows the items. `jobs.retry` is unchanged, DONE
items stay done. R-266's remaining engine half closed with this. Mutation
table `docs/mutation/r380.md`, 6 of 6 killing, null control 0 of 7608, no
collect drift, every restore verified against `git show HEAD`. R-380 is
closed in place. R-390 and R-391 filed. The learning is
`docs/solutions/workflow-issues/a-job-cause-that-ignores-item-retryable-tells-a-person-to-resume.md`.
Main's highest residual number is R-391.

**The session before, 2026-09-18, R-378, issue #91, `unit/issue91-the-harvest-prints-nothing-a-person-can-`.**
The default human rendering of a harvest names the harvested labels and the
unresolved count. `cli.render.render_review_set` is gated on `review_set/`
the way the diagnostic table is gated on `diagnostic/`. A harvest item's
`name` is its own indented line. Other review_set items keep their own
fields. Tests drive the real dispatcher in the default human mode, because
`tests.cli_drive.drive` always requests json and that is why every harvest
test stayed green over a blank answer. Mutation table
`docs/mutation/r378.md`, 6 of 6 killing, null control 0 of 7603, no collect
drift, every restore verified against `git show HEAD`. R-378 is closed in
place. The learning is
`docs/solutions/workflow-issues/a-json-only-driver-cannot-see-a-blank-human-renderer.md`.
Main's highest residual number is R-389.

**The session before, 2026-09-17, R-379, issue #90, `unit/issue90-every-offered-release-records-its-artist`.**
A label sweep offer records the artist's name, never a provider object's
repr. `_artist_of` reads a string as the name and an object's `name`
attribute otherwise. The suite's stand-ins passed a string, which is why
every green battery missed the address the live sweep wrote. A new test
drives an object whose `str` is a memory address. Mutation table
`docs/mutation/r379.md`, 4 of 4 killing, null control 0 of 7598, no collect
drift, every restore verified against `git show HEAD`. R-379's producer
half is closed. The 98 live rows still carry addresses, filed as R-389.
The learning is
`docs/solutions/workflow-issues/a-string-stand-in-cannot-catch-str-of-a-provider-object.md`.
Main's highest residual number is R-389.

**The session before, 2026-09-17, R-367, issue #87, `unit/issue87-a-restore-from-a-snapshot-taken-with-rek`.**
A restore from a snapshot holding only the database completes and names the
absent write ahead log, rather than failing on a copy the snapshot never
held. `plan_restore` lists the snapshot's database folder and copies only
the sidecars it holds. A listing that fails refuses before anything is
cleared. A failed database copy still refuses. Mutation table
`docs/mutation/r367.md`, 14 of 15 killing, G9 a user facing zero on the
wording with G2 as composite (1 kill), null control 0 of 7596, no collect
drift, every restore verified against `git show HEAD`. R-387 and R-388
filed. R-367 is closed in place. Main's highest residual number is R-388.

**The session before, 2026-09-17, U66, issue #89, `unit/u66-every-guarded-listing-method-has-a-plant`.**
Every member of `acquire.listing.GUARDED_METHODS` now has a planted pagination
loop case in `tests/test_adapter_listing.py`. The planted names live in the test
file and equal the production set, so adding a name arms its own case and
removing one fails that case rather than dropping it. U65's F2, removing
`get_ep_singles`, now kills 2 on the listing file. R-386 is closed in place.
Mutation table `docs/mutation/u66.md`, 6 of 6 killing, null control 0 of 7590,
no collect drift, every restore verified against `git show HEAD`. The learning
is `docs/solutions/workflow-issues/a-parametrize-over-the-live-set-drops-the-case-the-mutation-is-supposed-to-fail.md`:
a parametrize over the live set makes the mutation delete the case that would
have caught it.

**The session before, 2026-09-17, U65, issue #88, `unit/u65-every-listing-declares-its-own-stop-rule`.**
Every provider listing now declares its own stop rule and its own request budget,
in `STOP_RULES` and `PAGE_CAPS` beside the page sizes, and `paginate` takes both
as required keyword arguments so a wrapper that forgets to choose fails to call.

**R-383's code half is done and R-383 is still OPEN**, because its closing
condition is a live read and a live provider call is attended. Two corrections
matter more than the fix itself:

1. **The recorded cause was wrong.** R-383 and its solutions entry both blamed the
   client for dropping unplayable tracks from each page. tidalapi 0.8.11 does no
   such thing: `Favorites.tracks` hands the response to `map_json`, which maps
   every item with no filtering, and the `Track ... is unavailable` line seen
   during the sitting comes from `session.track()`, off the listing path. The
   omission is the API's, and `get_tracks_count` documents it, saying the total
   "also includes track that may not be available for playback". Both records are
   corrected and the measurements are untouched.
2. **The obvious fix is wrong too, and this unit wrote it first.** Stopping on an
   empty page instead of a short one only moves the boundary, because an empty
   page is a page shape as well: a window whose every counted item is unservable
   comes back empty in the MIDDLE of a collection. Reproduced at 300 rows with
   rows 100 to 199 unservable, returning 100 of 200 servable rows silently. The
   unit's own `/code-review` found it.

**No page SHAPE says where a filtered collection ends.** Only a count the provider
publishes for the collection it is serving. `favorite_tracks` ends on
`get_tracks_count` and `playlist_tracks` on the `numberOfTracks` already parsed
onto the object, and neither costs a request, since the count replaces the page
that would have ended the walk. `account_playlists` and `artist_releases` have no
honest count, so they take the weaker empty page rule and carry **R-385** saying
they are narrowed rather than closed. `Favorites.get_playlists_count` is the near
miss and is refused in a docstring: it counts a different collection.

Also in this unit: `max_pages` became a budget of REQUESTS that RAISES
`ListingTruncated` when spent, rather than returning quietly; and a listing that
cannot page now refuses at once instead of being slept on for 31 seconds by the
retry ladder, which was costing this repository's own test file 31 of its 32
seconds and would have cost a 200 artist label crawl over three hours before
reporting a fault it knew about at the first request.

Mutation table `docs/mutation/u65.md`, 25 rows of 27 written, 23 killed, 2 zeros,
both maintainer facing and each given a line, no collect drift, every restore
verified against `git show HEAD`, null control 0. The table was measured at
`42fc8a2` and the file names the two changes that landed after it. Filed: R-384
the request cost, R-385 the two narrowed shapes, R-386 a guarded method name no
test exercises, closed in place by U66. Main's highest residual number is still
R-386. R-383's live half and R-384's live measurement stay attended.

**A METHOD rule could not be followed and needs correcting.** METHOD says run
`scripts/mutate.py` in the foreground. Its fixed overhead on this suite is over
600 seconds, which is the harness tool ceiling, so all three foreground attempts
were killed mid row and two left a partial mutation in
`src/cratekit/acquire/listing.py` that was restored from `git show HEAD:`. The
run that succeeded was a tracked background job, waited on, with nothing else
touching the tree. On this harness foreground is the CONTAMINATING option, which
is the opposite of what the rule assumes.

**Last sitting 2026-09-17, afternoon, attended, six workflows on
`sitting/tidal-runs`.** Not a unit. The three adapters U62, U63 and U64 landed
in September have now each run against the live Tidal account, which is what
`docs/cutover.md` said they owed, and its Sitting 4 table is the record. **R-355
was fixed inside the sitting**: the rows both outbound verbs build carried no
ISRC, so a live export or sweep matched nothing and reported a clean job.
`modules/outbound/source.isrc_for` now resolves each row's `Location` through the
configured prefix map and reads the file's own tag, `isrc` is a field in
`core/tags.py` (`TSRC` in ID3), a value that is not ISRC shaped reads as none,
and an absent library root refuses rather than reading as a library of untagged
files, which the review of the fix found. Live: 103 of 109 favourites and 8246 of
9937 collection rows carry an ISRC where none did before.

With that, `crate export playlist` ran twice on a real four track playlist, one
remote playlist created, 2 added, 2 unmatched, the second run adding nothing, and
`crate sync favorites` ran twice over 109 rows, 18 hearted and verified present on
the account, the second pass hearting nothing and reading all 59 matched rows as
already. **R-144 is CLOSED on the ledger.** Also live: one harvest, one intake
playlist, one 47 label sweep of which 32 labels refused, and one `crate sync all`
that listed 599 playlists and queued 19 jobs, **none of them resumed**, 11 being
source system label debris.

Six findings filed, R-378 to R-383. **R-383 is the one that matters beyond the
sitting**: `listing.paginate` stops at the first short page, and this provider's
favourites listing serves short pages because the client drops unplayable tracks,
so the account's 197 favourites read as 93. Playlists and playlist membership were
measured clean, so it is the filtered listings rather than the helper being wrong
everywhere. Phillip decided it is a unit, not a sitting fix. Mutation table
`docs/mutation/sitting4.md`, 10 rows, 8 killing; `sitting4-notes.md` records that
G9's remeasure was killed by memory pressure and is asserted rather than
measured, and that both driver runs were moved to the background by the harness.
Battery on the committed tree is in the merge commit. Do not take #29.

**The sitting before, 2026-09-17, morning, attended, R-133 on
`sitting/r133-vocal-restamp`.** Not a unit. The vocal restamp ran on the live
library and R-133 is CLOSED on the ledger. It took two fixes, both driven and
both landed in the sitting: R-370, the shipped loader built the clip level
PANNs wrapper against a checkpoint this machine does not hold and the scorer
read the speech columns rather than the singing ones, so no real track could
score; R-371, a tail chunk under a third of a second failed a track. With
them, `crate analyze vocals` over a real 36 track folder completed twice on
the 18 GB machine, 102 and 100 seconds, 1.3 GB peak, every score within one
point of what DJ_tools stamped. `metadata mytags-vocals --apply` then wrote
four associations to the live database inside the acknowledgment window,
1892 already present, after the plan first read clean over 9770 rows it could
not resolve (R-372, the location prefix rule for rekordbox's renamed drive,
added to the config by hand) and after DJ_tools' hand set 5.0 cut was carried
into the calibration state by hand (R-374). Also filed: R-373, R-375, R-376,
and R-377 from the review, which drove ten findings against the fix and
nine are applied.
The analysis and vocals extras are now installed in the venv, which changed
what one slim assumption test drives. `docs/cutover.md` carries the sitting
table. Main's highest residual is R-377. Battery on the committed tree is in
the merge commit. Do not take #29.

**The sitting before, 2026-09-16, evening, attended, R-9 on
`docs/r9-restore-rehearsal`.** Not a unit. The real backup job
`2026-09-16T16:30:43Z-4c99` reports succeeded and was read back on Drive: the
dated archive holds the 1139 objects the dry run predicted and the snapshot's
`master.db` matches the live file. The restore rehearsal ran to a scratch
directory through the engine's `target` seam under the real gates, landed the
database byte for byte, MD5 matched, `integrity_check` ok, and the verb then
reported the restore failed because it copies a write ahead log the snapshot
never holds. R-9 is CLOSED on observation and issue #46 can close back to it.
Three findings filed: R-367, the unconditional sidecar copy, which is a fix
unit; R-368, no verb restores anywhere but the live root; R-369, an
acknowledgment answered from a shell with no terminal cannot be continued
there. The backup acknowledgment is minted, by the author from a Terminal
window, valid until 2026-09-17T13:11Z. The live database was not touched.
`docs/cutover.md` carries the sitting table. Main's highest residual is R-369.
Battery on the committed tree is in the merge commit. Do not take #29.

**The session before, 2026-09-16, #83 on `relay/83`, unattended.** Not a unit. The four
small defects the first attended sitting found are fixed and closed in the
ledger. R-344: `preflight.same_identity` folds the case on both sides of both
identity compares, and setup still records the identity as given, because it is
also the `library_id` jobs and watermarks match exactly. R-346: the prompter
flushes, so setup from a real terminal no longer needs `PYTHONUNBUFFERED=1`.
R-347: an empty secret raises `prompt.NothingEntered` and the credential offer
records it as the INFO note a no gets. R-348: `adapter.raise_if_defect` makes an
`AttributeError`, `TypeError` or `NameError` under an offer or a fetch an
`AdapterBroken` with the adapter's new `report-defect` token, asked before the
vendored token heuristic. Review raised one plausible finding, filed as R-365;
the hunt one file over filed R-366. Mutation tables `docs/mutation/r83.md`, 17
rows, 14 killing, and `r83-round-2.md` after the fold tests moved off an all
digit identity that was its own uppercase, 3 of 3 killing. The two remaining
zeros are maintainer rows, the strip in `normalize_identity` and the sweep's None
guard, which is an equivalent mutation. **Both tables ran in a harness moved
background job.** Each driver call was started in the foreground, outlived the
600 second tool ceiling, and was moved to the background by the harness, and the
session then waited on the output file with nothing edited meanwhile. Every row
reports its restore verified against HEAD and the tree held only the driver's own
output afterwards, which is the same shape
`docs/solutions/workflow-issues/a-relay-task-finished-a-mutation-table-by-backgrounding-the-driver-the-rule-forbids.md`
says is not validated. Phillip may want the tables rerun attended. Main's highest residual was R-366 once
`relay/83` merged. Battery on the committed tree before the record: ruff clean,
`scan_repo.py` exit 0, pytest 7543 passed and 1 skipped in 393 seconds. Do not
take #29.

**The session before, 2026-09-16, U64 (#86) on `relay/86`, unattended.** The playlists
source runs. `crate sync all` lists the account through a fifth `Catalogue` read,
`account_playlists`, which `TidalCatalogue` answers through `listing` and keeps to
playlists whose creator is the logged in user, refusing a client that cannot name
its account. `sync.playlists` excludes, in this order, the `DOWNLOADED ` prefix,
an id in the playlists cursor, a favourites placeholder by
`favorites.placeholders.PLACEHOLDER_NAME` (a dated quarter or the undated
backlog), an open job this source queued, and an empty playlist, then queues each
remaining one through `intake.cli.queue_playlist` under the pass's run id with
`source_id` `playlists`. A plan in `sync/cli.py` now carries every job its source
filed, and the summary gains a `playlists` block. The cursor is a `swept` id list
on the watermark record, written by `WatermarkStore.record_swept`, and
`reconcile` records a playlist at the start of a pass once its job SUCCEEDED, for
this library only. The mark is reported `unbound` every pass, because the account
seam has no rename. Review drove one finding, the undated backlog placeholder.
Mutation table `docs/mutation/u64.md`, 25 rows through the driver's own functions
on subsets, 24 killing, C2's zero closed with a test, C3 a maintainer zero on the
full suite. Three reserved cause population pins moved and are re-pinned with
their sets named. **R-358 and R-359 are the ones to read before the attended
sitting**: a swept playlist is never renamed, and swept means resolved rather than
acquired. R-360 to R-364 are filed beside them. Battery on the recorded tree: ruff clean,
`scan_repo.py` exit 0, pytest 7522 passed and 1 skipped in 392 seconds. Do not
take #29.

**The session before, 2026-09-16, U63 (#85) on `relay/85`, unattended.** The outbound
account seam is bound. `modules.outbound.tidal_account.TidalAccount` implements
the six add only `RemoteAccount` members over U62's `client_session`, imports
nothing vendored, and pages through `acquire.listing`. `account.resolve` refuses
`credential-missing` with no session, logs in ONCE and holds the adapter for the
process, because both workers resolve per item; `account.forget()` drops it, and
a conftest autouse calls it around every test. `bound()` answers whether the
adapter imports, so the queued warning is gone in a shipped build. Matching is an
ISRC naming exactly one track, then an exact provider track URL, else `None`.
`has_heart` answers from one paged favourites read, `add_heart` and
`add_to_playlist` check first, writes retry once, a create never. A provider
failure is an ITEM scoped cause through `account.provider_failure`: 401, 403 or
the client's authentication error is `credential-missing` and drops the held
account, everything else `unavailable-transient`. Review drove four findings: an
add the client answers without the track, a 400 read as a rejected session, the
dead client kept, and `bound()` not importing the client library. Mutation table
`docs/mutation/u63.md`, 25 rows, all killing on subsets, checked by hand for
R-329's reason, three zeros closed with tests. R-226's agent half is closed.
**R-355 is the one to read before the attended sitting: no shipped row carries an
ISRC, so a live sweep or export today matches nothing and writes nothing.** R-356
and R-357 are filed beside it. Next unit is U64 (#86). Do not take #29.

**The session before, 2026-09-16, U62 (#84) on `relay/84`, unattended.** The label
catalogue seam is bound. `acquire.provider_session.client_session` is the one
factory that logs a provider client in from the keychain inside the materialised
scope; U63 is meant to reuse it. `label.tidal_catalogue.TidalCatalogue`
implements the four `Catalogue` reads, pages through `acquire.listing`, imports
nothing vendored, and raises named errors rather than returning `None`.
`catalogue.bound()` answers whether that module imports, so the enqueue warning
is gone in a shipped build. A conftest autouse guard replaces
`provider_session.CLIENT_FACTORY` so no test can reach the live provider; a test
that wants a client sets it. The factory's tests live in
`tests/test_label_tidal_catalogue.py` rather than `tests/test_adapter_contract.py`.
Review drove three findings: an outage is `unavailable-transient` rather than a
new login, the roster lists once at construction, and a name two artists share
refuses. Mutation table `docs/mutation/u62.md`, 24 rows, 23 killed, the one zero
removed as redundant. R-258's agent half is closed; its live half and R-350 to
R-354 are the next attended sitting's, listed in `docs/cutover.md`. Next unit is
U63 (#85). Do not take #29.

**The session before, 2026-09-16, the first attended U29 sitting, on `main` with
Phillip present.** Not a unit. `docs/cutover.md` now exists and is the record.
Setup ran for real against the live library volume, the pin 7.2.18.0311 is
recorded, three credentials are in the keychain, the doctor reports no failing
check, and the commit-msg hook is installed in this checkout so `repo.commit_hook`
is green. **R-210 is CLOSED on observation**: a real FLAC landed with no tempo
tag through the PKCE session, and a fresh device-flow session on the same
account and track was served AAC. The first real download found **#82**, the
adapter handing the vendored tool a function where it calls a logger, fixed and
merged as `8f89efc` with a guard that reads the method set off the vendored
tree. R-9's dry run ran and its real run, job `2026-09-16T16:30:43Z-4c99`,
ended succeeded; the second sitting that evening read it back on Drive, ran
the restore rehearsal and closed R-9. Seven findings are filed, R-343 to R-349.
R-346 is fixed on `relay/83`, so setup from a real terminal no longer needs
`PYTHONUNBUFFERED=1`.

**THE BOARD IS COMPLETE AND THE PRODUCT CANNOT SYNC.** `docs/cutover.md` says
why in one section: R-258 and R-226 are unbound adapter seams and the playlists
source has no listing, so nothing in the product lists Tidal. That was the
remaining build, on the board as U62 (#84), U63 (#85) and U64 (#86), with #29 declared dependent on all three. U62, U63 and U64 have since landed their agent halves, R-355 means the account half matches nothing live yet, and R-358 means a playlist Cratekit sweeps is not marked on the account. R-9 is closed on the ledger; the restore verb's defect is R-367. Do not take #29.

**The session before, 2026-09-11, U25 on `unit/u25-vocal-restamp-and-my-tags-shells`.**
The two remaining vocal CLI shells landed. `cratekit.vocals.cli` queues
`analyze.vocals` and scores files that already carry a Camelot head, which
closes R-277. `analyze.run` still skips a prefixed name. `cratekit.write.metadata_cli`
plans My Tags by default and writes them when apply is requested, through the guarded
writer on the configured database, never the live one. Both `planned_in`
markers are gone, `analyze.vocals` is bound in `HANDLERS`, and
`owed_by_unit()` no longer lists 25. Nineteen landed verbs now queue and
eighteen are bound; `job.resume` remains the unbound exemption. R-133's 18 GB
run stays attended. Do not take #29.

**THE DRIVER RAN.** Twenty five rows in `docs/mutation/u25-rows.toml`,
measured by `scripts/mutate.py` in 6131 seconds, eleven killing, thirteen
zero on the full suite, one refused. Null control 0 of 7401. The zeros
have no composite, which is R-341. A corrupt vocal calibration still
defaults to the 12.0 cut, which is R-342. The reading is
`docs/mutation/u25-notes.md`.

**The session before, 2026-09-11, brief rewrite for U25, not a unit.** #80 is closed.
U25 was not finished. That was the answer R-324 asked for, and the 2026-09-10
reopen of #25 had already taken it. What was still missing was a brief a session
could build against: the issue body still described the DSP port, which is in the
tree. The body then named the two remaining shells, `analyze.vocals` and
`metadata.mytags-vocals`, the engines they sit on, R-277, and R-133 left
attended.

**The session before, 2026-09-11, R-102 on `relay/54`, taken from the board as issue #54
and run as relay task 54.** The twelfth residual issue worked, and the last of
METHOD's guard group. Test work, closed in place, with one piece filed. The
reports allowlist audit in `tests/modules/test_reports.py` now walks the IMPORT
CLOSURE of `ALLOWED_IMPORTS`, not the list: `_admitted_closure` follows import
statements, `__import__` and `importlib.import_module` in one worklist pass and
returns what it cannot follow, which the audit refuses. Driven on the real tree,
`cause` calling a planted `access_probe` reads clean to the one hop walk and red
to the closure. **The closure is eighteen modules and reaches `rb_writer`**
through `rbxml`, `tree_registry` and `session`, so forty nine writers are now
named in `QUALIFIED_MUTATIONS`. **A unit that adds a writer to the write path
will now fail `test_reports.py`**, and the learning is
`docs/solutions/workflow-issues/the-reports-allowlist-audit-reaches-the-write-path-so-a-new-writer-there-fails-test-reports.md`.
The built in review drove three holes in the first version, `import_module`
unread, an unconditional package fallback, and a resolver asking the real tree
for a planted one, and all three are fixed and driven. R-340 is the report side:
a report calling a named writer through another module's attribute is not
caught. Sixteen rows are in `docs/mutation/r-102-rows.toml`, fourteen killing
and two predicted maintainer facing zeros, checked by hand on the one file and
recorded in `docs/mutation/r-102.md`, and unrun by the driver, for R-329's
reason.

**The session before, 2026-09-11, R-15 on `relay/53`, taken from the board as issue #53
and run as relay task 53.** The eleventh residual issue worked, and the third of
METHOD's guard group. Test work, closed in place, with one piece filed. Measured
before any pin: a sixth permitted table and a bookkeeping column swapped for a
content column killed nothing in the full suite. `tests/test_whitelist_membership.py`
pins `PERMITTED_ROW_TABLES`, `BOOKKEEPING_COLUMNS`, and the content allow list,
which is registry derived here and so is pinned at baseline, per metadata
operation with its ownership mode, and fully enabled. The two deny lists beside
them, `GRIDLESS_ON_CREATE_COLUMNS` and the unwritable metadata fields, are pinned
too, since a removal is their widening. An AST audit holds every
`Rekordbox6Database` call in `src` to an explicit non empty `path=`. The built in
review found that `db_dir` also sets the binding's share directory, and that the
rows file's batch name would have let the driver overwrite the hand record, now
`r-15-driver`. Checking which file the connection opened is R-339. Ten widening
rows are in `docs/mutation/r-15-rows.toml`, all ten checked red by hand on the pin
file and recorded in `docs/mutation/r-15.md`, and unrun by the driver, for R-329's
reason.

**The session before, 2026-09-11, R-14 on `relay/52`, taken from the board as issue #52
and run as relay task 52.** The tenth residual issue worked, and the first of
METHOD's correctness group. A fix, closed in place, with one piece filed. Read
against the tree, nothing in `src` joined `AnalysisDataPath` to anything. What
did exist was seven call sites arming the analysis watch over the library root
alone. With an acknowledged database outside the root, the share and every grid
sit outside it too, so each of those sessions watched nothing. `core.analysis_store`
now owns the join. `share_root` is the directory beside the configured database,
`analysis_file` joins a stored value to it, and `watch_roots` adds the share when it
sits outside the root. The seven sites take `watch_roots`, and an AST guard in
`tests/test_analysis_store.py` refuses a hand listed root. The backup carries the
share only when it sits under the root. Outside it, the plan, the outcome and the
verb's envelope now say `analysis-share-not-carried`, which the built in review
found reached nobody until the envelope asked for it. Carrying the share is R-338.
The kebab literal pin moved 401 to 402. Ten mutation rows are in
`docs/mutation/r-14-rows.toml`, two checked red first by hand and the rest unrun,
for R-329's reason.

**The session before, 2026-09-11, R-11 on `relay/48`, taken from the board as issue #48
and run as relay task 48.** The ninth residual issue worked, and the last of
METHOD's surface group. Two of its four findings closed, two stay on the ledger.
The CRLF absorption was three copies, not the four R-11 counted, since the
catalog writer takes the break after a node rather than before it. The three are
now `rbxml._absorb_lead_break`, and the goldens pass unchanged. The analysis
watch is now driven through the database half:
`test_a_grid_rewritten_during_a_membership_write_refuses_the_session` plants a
real ANLZ file under the library root and asserts the `anlz-modified` refusal.
`apply_rating_changes` stays kept, since the wrapper has grown nothing. The real
label in two fixtures is still the author's decision about D1. Nothing new was
filed. Six mutation rows are in `docs/mutation/r-11-rows.toml`, two checked red
first by hand and the rest unrun, for R-329's reason.

**The session before, 2026-09-11, R-10 on `relay/47`, taken from the board as issue #47
and run as relay task 47.** The eighth residual issue worked, and the second of
METHOD's correctness group. A fix, not a close. `rb_writer.add_memberships`
takes one playlist and many content ids, reads what the playlist holds in one
query, and returns the ids it inserted. `add_membership` is a one id call into
it, so the only when absent rule still lives in one place. `write_tree_membership`
makes one call per playlist instead of one per track, and resolves each folder
once per session instead of once per plan entry. What remains per inserted track
is the binding's own content lookup and track count inside `add_to_playlist`,
which R-10 did not describe. R-10 is closed in place and nothing new was filed.
Eight mutation rows are committed in `docs/mutation/r-10-rows.toml` and unrun,
for R-329's reason.

**The session before, 2026-09-11, R-7 on `relay/44`, taken from the board as issue #44
and run as relay task 44.** The seventh residual issue worked, and the third of
METHOD's surface group. A close, since U27's doctor already reports a trashing
remote with its option unset, and setup runs doctor. Read against rclone
1.74.3's own backend help, two of that check's rows were wrong and are fixed.
Dropbox's row named an option the Dropbox backend does not have, so it failed
every run with a fix nothing could apply. OneDrive's `hard_delete` does nothing
on a personal drive and read green there. `TrashPolicy.applies_when` now gates
it on `drive_type`. R-336 and R-337 are filed. Six mutation rows are committed in
`docs/mutation/r-7-rows.toml` and unrun, for R-329's reason.

**The session before, 2026-09-11, R-6 on `relay/43`, taken from the board as issue #43
and run as relay task 43.** The sixth residual issue worked, and the second of
METHOD's surface group. Another close, measured on the registry: sixty four
entries, sixty two landed, and conformance 1, 2 and 3 parametrise over all
sixty two rather than the four R-6 described. The two markers left are U25's
vocals verbs, which R-324 and the reopened issue already own, so R-6 did not
carry them a second time. The `cratekit.cli.verbs` docstring said the package
held exactly U5's four verbs and it also holds `login`; it is corrected. No guard
changed, so there is no mutation table, and nothing new was filed.

**The session before, 2026-09-10, R-5 on `relay/42`, taken from the board as issue #42
and run as relay task 42.** The fifth residual issue worked, and the one METHOD's
ninth line names first. It was a close, as that line guessed. R-5's closing
condition was already true: U11 and U27 are closed, conformance 4 drives the
review queue and conformance 8 drives the doctor, and neither is an existence
check. What was false was the claim, in R-5 and in the docstrings of conformance
4 and 6, that no adjudicating or destructive verb had landed. Every adjudicating
verb has, and twenty two of twenty four destructive ones. The docstrings are
corrected. The gap they described, that neither assertion drives a landed verb
through the dispatcher, is still real and is R-335. No guard changed, so there is
no mutation table.

**The session before, 2026-09-10, R-4 on `relay/41`, taken from the board as
issue #41 and run as relay task 41.** The fourth residual issue worked, and the first of
METHOD's surface group. R-4's written closing condition was already true: each
of the nine toggles U5 declared gates a landed verb and none carries
`planned_in`. `registry.Entry` now refuses an `extras` group that is not the
verb's own `module_id` or is missing from `EXTRAS_BACKED`, because the stub
prints that field as the install command and nothing tied it to pyproject. A
derived parametrized test drives all thirteen toggles with landed verbs through
the resolver and parser in both directions. R-4 is closed in place, nothing new
was filed, and six mutation rows are committed in `docs/mutation/r-4-rows.toml`
and unrun, for R-329's reason.

**Two sessions back, 2026-09-10, R-3 on `relay/40`, taken from the board as issue #40
and run as relay task 40.** The third residual issue worked, and the second of
METHOD's guard group. `scripts/scan_repo.py` REFUSES a tracked archive now
instead of skipping it, by suffix and by header, so a renamed archive is refused
too. R-3's written closing condition was already true on the tree, since U13
committed the downloader unpacked, and nothing kept it true. R-3 is closed in
place. R-334 is the list still being closed, plus the same silent skip for a
`.db` or `.sqlite` file, and the choice there is Phillip's. Fifteen mutation rows
are committed in `docs/mutation/r-3-rows.toml` and unrun, for R-329's reason.

**Three sessions back, 2026-09-10, R-1 on `relay/38`, taken from the board as
issue #38 and run as relay task 38.** The second residual issue worked rather than a unit,
from the guard group in METHOD's ninth line. `crate doctor`'s `repo.commit_hook`
now reads every hook type `.pre-commit-config.yaml` names and checks each
installed hook, not only `.git/hooks/pre-commit`. R-1 is closed in place, and
R-333 is the one conservative call, a FAIL when PyYAML is not importable.

**THE PRIMARY CHECKOUT FAILS THAT CHECK, AND IT IS RIGHT TO.** It has a
pre-commit hook and no `.git/hooks/commit-msg`, so the board closing hook has
never run locally. Only CI has been judging trailers. The fix is Phillip's,
because it writes into `.git/hooks`:
`pre-commit install --hook-type pre-commit --hook-type commit-msg`. Twenty five
mutation rows, all killing, are in `docs/mutation/r-1.md`. The driver outran
the ten minute foreground ceiling twice, and a polling wait in the foreground
carried it through.

**Four sessions back, 2026-09-10, U61 on `relay/79`, taken from the board as
issue #79 and run as relay task 79.** `crate sync all` is a COMPOSER now. It plans every
enabled source, asks the favourites confirm once, then queues each source through
that source's own `queue_sweep` under that source's own handler key, with one
intake run. Nothing is queued under `sync.all`, so its entry dropped
`long_running` and `argv_builder` and **R-203 CLOSED**: `HANDLERS_NOT_YET_BOUND`
holds only the `job.resume` exemption. Playlists has no worker and is reported as
not built, so a slim pass is a no-op rather than an ok.

**A COMPOSED JOB NEEDS A RUN ITS OWN VERB OWNS.** The dispatcher refuses a `--run`
whose record belongs to another verb, so the favourites job could not carry the
pass's run as its gate run. `Gates.hand_off` copies the recorded answer onto a new
run owned by `sync.favorites`. The learning is
`docs/solutions/integration-issues/a-verb-that-queues-another-verbs-job-must-hand-it-a-run-that-verb-owns.md`.

**U61 HAS NO MUTATION TABLE EITHER, and the reason is now measured.** The null
control is hardcoded to the full suite at `scripts/mutate.py:1002`, so the
driver's preflight is two full runs, about 720 seconds, whatever the rows say.
R-329 carries the correction, `docs/mutation/u61-notes.md` the sampled timing.

**Five sessions back, 2026-09-10, U60 on `relay/78`, taken from the board as
issue #78 and run as relay task 78.** `delete.review` stopped claiming a queue. Its entry
dropped `long_running` and `argv_builder`, `delete_argv` is gone, and the verb
left `HANDLERS_NOT_YET_BOUND`, so R-149 closed in the direction it left open.
R-134 closed too, at a schema cost of zero fields: the first run's baseline rides
the gate's existing context onto the refusal as `cause.detail.shown`, which
`render_gate` prints for a person, and `review_set/1` is untouched.

**A NEW REGISTRY GUARD HOLDS THE CLASS.**
`test_a_verb_declaring_the_queueing_contract_has_a_shell_that_queues` parses every
landed long-running verb's module for an `enqueue` call, with `job.resume` exempt
by role. It failed on `main` for `delete.review` alone. Its module-wide bar is
R-328.

**U60 HAS NO MUTATION TABLE, AND THAT IS A MEASURED GAP, NOT A CLEAN ONE.**
`scripts/mutate.py` reruns a six minute full baseline on every call, and a relay
task runs every command in the foreground under a ten minute ceiling, so two
attempts ended in preflight with no row measured. The rows are committed and
ready, `docs/mutation/u60-notes.md` holds the measurements, and R-329 is the gap
with three options, all Phillip's. The learning is
`docs/solutions/workflow-issues/the-mutation-driver-does-not-fit-a-ten-minute-foreground-call.md`.

**Six sessions back, 2026-09-10, R-322 closed on `relay/81`, taken from the
board as issue #81 and run as relay task 81.** The first residual issue to be worked
rather than a unit, and the first work of the ninth line in METHOD's serialized
order. It added SEVEN tests and thirteen lines of `scripts/board.py`, no new
behaviour, and it closed the audit's detector being driven by nothing.

**THE CONTRADICTION DETECTOR HAS A DRIVER NOW.** `contradictions()`,
`units_by_issue_number`'s exclusion of unlabelled unit-shaped titles, the
residual repoint half of the return, the default register read, and
`cmd_audit`'s exit codes are all driven. Both rows R-322 was built out of went
from zero to killing, re-run verbatim from U59's row file so the comparison is
two measurements of one experiment. `docs/mutation/u81-notes.md` is the reading
and it carries one correction to its own first row file.

**THE DOUBLE IS THE `gh` PAYLOAD, NOT THE GRAPH, AND THAT IS THE DECISION R-322
ASKED FOR.** A hand-built graph would type every key `build_graph` derives, so
the producer could drift and the tests would stay green. The fixture is the issue
list JSON, `build_graph` runs on it for real, and the field list is read out of
`load_issues`'s syntax tree and compared against the double's keys. The learning
is filed at
`docs/solutions/workflow-issues/a-double-belongs-at-the-producer-boundary-not-at-the-shape-it-produces.md`
and it carries two traps that cost a round here.

**The pending register is still EMPTY** and nothing in this session touched it,
so no `@requires` decorator exists anywhere.

**U59, the session before this one, built on `relay/77`.** It ran the whole
pipeline in one session: plan, the merge, the built in `/code-review`, a six
finding fix round, a twenty five row mutation table with one composite, and its
record. The merge is what kept the pending register empty: git took `main`'s
empty `PENDING` and only the branch's three-state `module_state` probe, so
nothing was re-armed.

**THE SOFT DELETE DEFECT IS OFF MAIN.** `write/metadata.resolve_genre_id` no
longer defaults the marker. A row that cannot report it refuses with
`soft-delete-marker-unreadable` at run scope rather than reading as active, and
the rule is driven through the SHIPPED reader, `crate tag retag` into
`plan_library` into `plan_genre_retag`, not only through the function's own
rows. R-186 closes.

**THE CONFORMANCE BRANCH IS LANDED AND ITS WORKTREE IS UNTOUCHED.**
`.worktrees/conformance` and `fix/conformance-3-and-soft-delete-reader` are
exactly as they were; the merge was taken on `relay/77` in the primary checkout.
**Two of its eleven commits were already on `main`**, the conformance 3 pair, so
`tests/test_cli_contract.py` is byte identical to `main` and this merge armed
three guards rather than the five the brief names. That is R-326.

**PHASE E'S AGENT HALF IS DONE.** Three verbs stopped reporting work nobody had
done. `route.inbox` applies on the confirmed branch instead of returning the
plan on both. `route.unplaced` reads the library instead of being
`_plan([], ...)`. `rebuild` and `route.resort` queue one item per governed tree
and drive them, and a library that has flipped no tree files no job at all
rather than an empty one. Both workers go through
`rebuild.rebuild_governed_tree`, which is the FIRST CALLER of `rebuild_tree`
anywhere in `src`.

**EVERY QUEUED VERB HAS A WORKER**, with `job.resume` exempt by role. Measured:
eighteen landed verbs queue and seventeen are bound. `delete.review` left the
population in U60 by ceasing to be queued, and `sync.all` left it in U61 by
queueing its work under keys that have workers. R-203 is closed with a note in
place. Its title stays at eighteen on purpose, because the title names what was
true when the entry was written.

**R-131 IS DOWN TO ITS ATTENDED HALF.** Everything in it that a session could do
is done and driven against a disposable database copy. Nothing has run on a live
tree, which is the whole of what the entry now says.

## Main, verify before trusting it

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 1 on the In review card, R-265

**Main's highest residual is R-357 once `relay/85` merges**, R-355 to R-357 being
U63's, with R-226's agent half closed in place, no duplicate heading and no
heading moved. U63's full suite before the review round was **7491 passed and 1
skipped** in 400 seconds on a committed tree, and after the review round, the
zero row tests and the record it was **7500 passed and 1 skipped** in 397 seconds.
The nine are six review fix tests and three zero row tests, all in
`tests/test_outbound_tidal_account.py`.

**Main's highest residual was R-342 once U25 merged**, R-341 and R-342
being U25's, with R-277 closed in place, no duplicate heading and no heading
moved. Mutation baseline collected **7401** on a committed tree. The last
full battery before the record was **7399 passed and 1 skipped**, in 374
seconds, then one more test landed (the missing My Tag template through
the dispatcher).

**Main's highest residual was R-340 once `relay/54` merged**, R-340 being that
branch's only filing, with R-102 closed in place, no duplicate heading and no
heading moved. Its suite was **7379 passed and 1 skipped**, in 358 seconds, on
`relay/54` on a committed tree. The eight since R-15's 7371 are this branch's
eight new identifiers in `tests/modules/test_reports.py`: six cases of
`test_the_audit_follows_an_admitted_module_to_the_module_that_writes`,
`test_the_closure_reports_an_import_it_cannot_follow`, and
`test_a_symbol_imported_from_a_package_follows_the_package_initializer`. That is
the new names matched against the delta, not the full collection differenced
against `main`. The R-15 record follows.

R-15's suite was **7371 passed and 1 skipped**, in 356 seconds, on
`relay/53` on a committed tree. The nineteen since R-14's 7352 are all in the new
`tests/test_whitelist_membership.py`: seven membership pins, the tree open audit,
ten audit refusals and one acceptance. The R-14 record follows.

R-14's suite was **7352 passed and 1 skipped**, in 352 seconds, on `relay/52` at
the record commit. The fourteen since R-11's 7338 are this branch's own: eleven in the new
`tests/test_analysis_store.py`, `test_the_analysis_watch_reaches_a_share_outside_the_library_root`
in `tests/test_adopt_apply_cli.py`, and the outside and contained drives in
`tests/test_backup_cli.py`. The R-11 record follows.

The last measured suite was **7338 passed and 1 skipped**, in 352 seconds, taken
on `relay/48` on a committed tree. One of the four since R-7's 7334 is R-11's
`test_a_grid_rewritten_during_a_membership_write_refuses_the_session`; the other
three arrived with R-10, whose own count was not recorded, so that split is not
reconciled by identifier. **Main's highest residual stays R-337 once this branch
merges**, since R-11 filed nothing. The earlier record follows. Against R-6's
7328 the six are R-7's own in
`tests/test_doctor.py`: four cases of
`test_a_onedrive_remote_where_hard_delete_does_nothing_is_a_note` and two of
`test_dropbox_is_not_told_to_set_an_option_rclone_does_not_have`. **Main's
highest residual is R-337 once this branch merges**, R-336 and R-337 being this
branch's, with no duplicate headings and none deleted. R-5 and R-6 changed no
test. Against R-3's 7312 the 16 before those are R-4's
own, reconciled by identifier in `tests/test_cli_contract.py`: two rejection
rows in `test_an_entry_missing_its_metadata_fails_to_register`,
`test_every_live_toggle_is_driven_by_the_toggle_test_below`, and thirteen cases
of `test_a_module_toggle_alone_switches_its_landed_verbs_on_and_off`. **Main's
highest residual stays R-335 once this branch merges**, no duplicate headings, no
heading deleted, and R-6 gained its closing note in place rather than moving.
Append only, and gaps are fine.

**The kebab literal pin in `tests/test_reserved_causes.py` moved 401 to 402** on
R-14, for `analysis-share-not-carried`, a warning code and not a cause. Before
that it moved 391 to 401 for ten git hook type names, differenced as sets
against `main`, none of them a cause.

**THE AUDIT EXITS 1 NOW, NOT 2, AND THE REASON IS A BOARD WRITE NOBODY RECORDED.**
Measured on 2026-09-10 while closing R-322: issue #25 is OPEN with a state reason
of REOPENED, so `contradictions()` returns nothing and the exit 2 U59 predicted
is gone. The registry still owes U25 two modules, which is now the register
working rather than a contradiction, and R-324 and #80 stay open because whether
that is U25's answer is #80's judgement. Do not weaken the check to get a green
audit; **the detector is now driven and softening it fails tests.**

**The one thing the audit does report is R-265, and `sync` is the wrong answer to
it.** `#81 status is In review, should be Ready`. `derive_status` knows five
statuses and the field has six, so every relay card reads as drift for the whole
of its run, and the remedy the audit prints would drag the card back to Ready
mid review. Leave it. Confirmed a second time on #81.

## Read this before touching a write path again

**A GUARD THAT REFUSES AN EMPTY LIST CANNOT SEE A BARREN ONE.** The unit's
learning, filed at
`docs/solutions/integration-issues/a-guard-that-refuses-an-empty-list-cannot-see-a-barren-one.md`.
Both new writes named `root/Music` as their `analysis_roots`, which is one entry
so it passed `write_tree_membership`'s empty-list refusal, and which holds no
ANLZ file, so the beat grid watch fingerprinted nothing and would have reported
a clean session whatever happened to the grids. Every other caller in the
package names the library root. **Judge a new call site's argument against what
the existing call sites pass, not against whether the callee accepted it.**

**THE ITEMS ARE THE DECISION, NOT THE CALL SITE.** Binding a queued verb is one
line at the call site and two real decisions before it: what an item IS, and
what the per item worker does. For these two the item is a TREE, which is what
makes a partial failure recoverable rather than a single collapsed failure.

**A RESUME OWES THREE CHECKS, and the corrected shape is in `intake/cli.py`.**
Refuse a job queued for another verb, because `handlers.run_job` reads the worker
off the JOB ROW and not off the verb somebody typed. Refuse a job with no items,
because every rebuild and resort queued before U53 has none. Re-raise the job's
own cause when it did not end well, which is R-225: `drive` raises only when
EVERY item failed, so a partial failure returns normally and an unconditional OK
exits zero over half a library.

**THE RESORT IS ADDITIVE**, which is R-312. There is no database removal path in
this build, so a genre change leaves the track in its old sub as well as its new
one and the convergence check names the leftovers.

## What U61 left behind

Three residuals, two notes in place, one learning and one learning corrected.

- **R-330.** A job an older build queued under `sync.all` stays in the queue with
  no worker and reads as a defect until somebody cancels it.
- **R-331.** A handed decision carries no record that it was handed, so a run
  record alone cannot tell it from one given directly.
- **R-332.** A pass where every source refused raises the first refusal, so the
  person sees one remedy and meets the other on the next pass.
- **R-329's second option was written on a wrong reading of the driver**, and the
  learning about the ten minute ceiling said the same thing. Both are corrected.

## What U60 left behind

Two residuals and one learning.

- **R-328.** The new queueing guard accepts an `enqueue` call anywhere in a
  verb's module, so two verbs sharing a module pass on one call. Nothing
  exploits it today: every shared-module pair also shares a worker.
- **R-329.** The mutation driver cannot finish a batch inside a relay task's ten
  minute foreground ceiling. U60's twenty rows are committed and unmeasured.
  **Read the learning before an unattended session plans a table**: if the
  battery's full suite is past roughly four minutes, commit the rows, record the
  gap and land, rather than spending ceiling length calls finding out.

## What U59 left behind, beyond the code

Seven residuals, R-320 and R-321 renumbered in from the branch and R-322 through
R-326 filed by this session, plus one learning. Four are worth knowing before
touching the board tooling or a source guard again:

- **R-324.** The registry owes U25 two modules. Its issue was reopened by
  somebody between the U59 merge and 2026-09-10, so the audit no longer exits 2
  and the loud half is discharged while the substantive half is not. The section
  above carries the measurement. #80 is still the decision.
- **R-322. CLOSED on `relay/81`, and the head of this file says what it took.**
  Both zero rows kill now. What replaced it is R-327, the board's WRITE half,
  which is a harder case rather than the same one: `reconcile` reads a user-owned
  project that a repository-scoped token cannot see at all, so there is no local
  payload seam to build an honest double at.
- **R-323.** A trailer names an ISSUE and both registers name a UNIT. Twenty
  four units are mismatched today and none of them is owed a module, which is why
  this was never seen. `audit` resolves the mapping through the issue titles now.
  The network-free hook cannot, so it says that it guessed.
- **R-326.** Two of the parked branch's eleven commits were already on `main`.
  Found by reconciling the collected count BY IDENTIFIER; a total-only check
  showed a healthy rise and would have said nothing.

**A GUARD THAT GOES RED AT A MERGE HAS TWO POSSIBLE CAUSES AND ONLY ONE IS THE
GUARD.** Four went red here and all four were right about their rule and stale
about the tree. Filed at
`docs/solutions/workflow-issues/a-guard-written-against-an-old-tree-goes-red-holding-a-rule-that-is-still-right.md`.
The dangerous reading is the other one: weaken a stale guard to get green, and
the rule it was holding goes with it.

## What U53 left behind, still current

Eight residuals, R-312 through R-319, corrections to R-203 and R-131, and one
learning. Four are worth knowing before touching routing again:

- **R-312.** The resort adds and never removes, so a re-place doubles a track's
  membership until somebody takes the old one out by hand.
- **R-314.** `assert_addressable` kills ZERO tests, and so does the composite
  over the refusal inside it, measured over the full suite twice. Nothing in the
  repository produces a colliding destination set. The extraction into
  `plan_destinations` is what made that measurable; the gap predates it.
- **R-316, closed 2026-09-19.** Neither worker derives the vocal dimension,
  and both now report the gap as a `vocal-dimension-not-compared` warning.
  Deriving it is still open.
- **R-313, closed 2026-09-19.** `route.unplaced` declares no write and is not
  destructive. It keeps `rekordbox.pins`, because a read checks the binding
  pin, and R-444 records the same shape in `converge`.

## What U57 left behind, still current

**THE RECOGNITION IDENTIFIER IS REAL AND HAS SPENT NOTHING.** The spend is known
BEFORE the first call, not counted after it, and a spend refusal is its own cause
and never a miss. Identifying at the queue is un-resumable spend, R-304, and the
ledger counts attempts the service never received, R-306. No live key is bound,
so the response table has met no real answer, which is R-300.

**A SEAM THAT RETURNS ONLY ROWS READS ABSENCE AS EVIDENCE OF ABSENCE**, filed at
`docs/solutions/workflow-issues/a-seam-that-returns-only-rows-reads-absence-as-evidence-of-absence.md`.

**R-308.** `core.artifacts` landed and the four feature copies are not migrated
onto it.

## What U54 and U58 left behind, still current

**R-289**, the acquisition staging tree is a dotfile and `tagging.tag.audio_files`
walks dotfiles. **R-290**, a blocked job reports outcome `ok` and exits 0 in every
queued verb, was CLOSED on `relay/160`, 2026-09-20, without the envelope contract
change its entry feared. See the top of this file.

**The resume reads a rename intent, never the folder**, filed at
`docs/solutions/workflow-issues/a-worker-that-renames-its-item-owes-the-resume-an-exact-record.md`.
It applies to every remaining R-203 worker that moves files.

**The heavy stack stays behind the extra**, because `cli.jobs.argv_for` imports
the verb module by name to build a resume line.

**A fallback must not fill an absence somebody meant**, filed at
`docs/solutions/workflow-issues/a-remedy-fallback-overwrites-an-absence-somebody-meant.md`.

## What is open

In METHOD's serialized order, which is what picks the work:

| order | issue | unit | state |
|---|---|---|---|
| 7 | | Phase E explanation, Phillip's and not a session's | |
| 8 | #77 | U59, land the conformance branch | DONE on `relay/77` |
| | #78 | U60, the deletion pass | DONE on `relay/78`, no mutation table (R-329) |
| | #79 | U61, `crate sync all` composes the source increments | DONE on `relay/79`, no mutation table (R-329) |
| 9 | #38 | R-1, doctor checks every configured hook type | DONE on `relay/38`, 25 of 25 rows killing. Halted `partial_landing`, repaired by hand 2026-09-11 |
| | #40 | R-3, the scan refuses a tracked archive | DONE on `relay/40`, 15 rows committed and unrun (R-329) |
| | #41 | R-4, extras tied to their module and every toggle driven | DONE on `relay/41`, 6 rows committed and unrun (R-329) |
| | #42 | R-5, conformance 4 and 8 already drive behaviour, closed in place | DONE on `relay/42`, no guard changed, R-335 filed |
| | #43 | R-6, the conformance drives cover sixty two landed verbs, closed in place | DONE on `relay/43`, no guard changed, nothing filed |
| | #44 | R-7, doctor reports a trashing remote, closed in place with two rows fixed | DONE on `relay/44`, 6 rows committed and unrun (R-329), R-336 and R-337 filed |
| | #47 | R-10, one membership call per playlist and one folder lookup per folder | DONE on `relay/47`, 8 rows committed and unrun (R-329) |
| | #48 | R-11, the lead break helper and the watch driven through the database half | DONE on `relay/48`, 6 rows committed and unrun (R-329), two findings still open in the ledger |
| 10 | #25 | U25, vocal restamp and My Tags shells | DONE on `unit/u25-vocal-restamp-and-my-tags-shells` |
| 11 | | Phase F explanation, Phillip's and not a session's | |
| 12 | #29 | U29, cutover | Ready by dependencies, ATTENDED, not a session's to take |

**#38 is the one task in that run that did not verify itself.** It landed at
`d3fe927` with its whole pipeline complete, seven commits through the review
round, the mutation table, the record and the restart, and only the tracker
writes failed, so the record halted `partial_landing`. Repaired by hand on
2026-09-11: the issue was closed with a comment naming `d3fe927`, `relay/38` was
deleted, and `verify` then returned every check green. **Its record still reads
`halted` and always will**, because that manifest is finished and nothing will
start against it again. See the `verify` confirms section below before treating
that as a second repair.

**The board after this merge**: 61 units, 60 done, 1 ready, 0 blocked, once
main is pushed. The one ready is #29, attended and not a session's. METHOD
line 10 is done. Line 11 is Phillip's. Do not take #29.

**Phase E is complete with the U53 merge.** Line 7 is Phillip's, the explainer
over the range from `46d5a4c` to the U53 merge commit. A session does not run
it. Phase F's explainer is line 11, over the U59 merge and the residual
commits plus this one.

#78 and #79 are not in METHOD's list, which was serialized before they existed.
Each was taken as a relay task, which is Phillip placing it.

**#42, R-5 was a close**, read against the tree rather than assumed. Its
successor is R-335, which has no issue.

Residual issues carry the `residual` label. They are the queue after the units,
each done or closed back to the ledger. A2 is attended. **#81, R-322, is the
first of them to be worked and it is done**, which leaves the rest of that label
as the live list; run
`gh issue list --repo philgutowski/cratekit --label residual --state open` rather
than trusting a count written here. R-324 is closed on #80. R-327 has no
issue, which is the normal state for a residual: the ledger holds it until
somebody decides to act on it.

**Every unit in METHOD's serialized list is built except #29, and so
are #78 and #79.** What is left is Phillip's: the two explanations, #46 and
#39, and #29.

## Do this first

1. `CLAUDE.md`, then `docs/METHOD.md`. The pipeline section is the sequence and
   the do-not-touch section binds. Line 10 is done. Line 12 is #29, attended.
2. `board.py next`. It names #29 first by reach. Do not take it. There is no
   unit left that a session may take.
3. Grep `docs/solutions/` for the module you are about to touch. A unit that
   opens a destructive write reads the barren list entry before it names an
   `analysis_roots`; a worker that moves files reads the rename intent entry
   before it binds. Read R-277 before touching `analyze.vocals`.

## The branches

| branch | state |
|---|---|
| `relay/48` | R-11, the branch this record is on; delete after the merge |
| `relay/47` | R-10, merged to `main`; delete if it still exists |
| `relay/44` | R-7, merged to `main`; delete if it still exists |
| `relay/43` | R-6, merged to `main`; delete if it still exists |
| `relay/42` | R-5, merged to `main`; delete if it still exists |
| `relay/41` | R-4, merged to `main`; delete if it still exists |
| `relay/40` | R-3, merged to `main`; delete if it still exists |
| `relay/38` | R-1, merged to `main`; delete if it still exists |
| `relay/79` | U61, merged to `main`; delete if it still exists |
| `relay/78` | U60, merged to `main`; delete if it still exists |
| `relay/81` | R-322, merged to `main`; delete if it still exists |
| `relay/77` | U59, merged to `main`; delete if it still exists |
| `fix/conformance-3-and-soft-delete-reader` | LANDED into `relay/77` by merge. Still in `.worktrees/conformance`, untouched, and now redundant. Deleting it and the worktree is Phillip's call, not a session's, because the merge is not pushed yet |

## When a relay run is cut off mid unit

It has happened three times, all three on a usage limit, and the shape is worth
recognising. The endings differ:

- **The runner had already merged.** Its own verify then refuses to call the
  task landed, `halt_class: partial_landing`, and the tracker issue stays open.
  So `main` carries a unit whose review, table and record never happened. That
  was #72.
- **The runner had not merged.** The task branch holds the work and the tree is
  left dirty, `halt_class: unclean_exit`, and the run stops there whatever
  `on_halt.continue_past_task_halt` says. That was #75.

The state lives in `~/.relay/<run>/state.json`: `tasks.<n>.status`, `halt_class`,
`halt_message`, `findings`, and `transcript_path`. Read the task's last assistant
messages to learn which pipeline step it reached. Finish it on the task's own
branch, merge, and close the issue from there. **Do not re-run the unit from the
board as though nothing had landed.**

**`verify` needs the issue named as `#N`.** After a hand landing, `relay_cli.py
verify <manifest> <task>` reaches a landed verdict only when it can find the
link. It derives one from a default branch commit naming `#N` when the record
carries no `landing_ref`; when the record already carries one, as a
`partial_landing` record does, it instead wants a tracker COMMENT naming that
sha, and one comment is the whole repair. native-relay's own `docs/solutions/`
carries both halves.

**`verify` confirms, it does not promote.** `cmd_verify` computes the verdict,
prints the checks, and returns an exit code; it writes nothing to the record
(`cli.py:395`). A halted record stays halted, reading `partial_landing`, however
green the verdict is. Promotion happens at the NEXT run's startup, where
`startup_reverify` re-runs the full verdict on every halted record and promotes
the ones that now pass. So a repaired task whose manifest is finished keeps a
halted record forever, and that is cosmetic rather than a second repair to chase.
Measured on #38, 2026-09-11: every check green, `38: landed` printed, record
still `halted`.

## Standing decisions

- **The board is the BUILD, the ledger is the LEDGER.** Do not backfill.
- **Residual numbers are APPEND ONLY.** Take numbers above main's highest at
  branch time, and renumber the incoming branch's at the merge, never main's.
- **The pending register is empty.** Re-opening any countdown re-arms it.
- **CI does not run the suite.** A step in the workflow must be able to pass.
- **Use `scripts/mutate.py`**, cap 25 rows, author's table, gap recorded in one
  line. Run `git status --porcelain` after every return; R-256 says why. **Never
  run `git checkout` on a file while a fix is uncommitted**: this session reverted
  one of its own review fixes that way and had to re-apply it, which is METHOD's
  driver rule arriving by hand instead of through a driver.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **Re-pinning a population means naming what moved.** Difference the SETS
  against `main`'s own tree. A count that moved by the right amount is not a
  measurement of what moved, and U59 hit the sharper version: the soft delete
  reader pin went from two members to a DIFFERENT two, so the count did not move
  at all while both members did.
- **A guard that goes red at a merge is usually right and out of date.** Ask
  whether the RULE moved or the TREE did, and drive the answer. Weakening a stale
  guard to get green takes the rule with it. Four of them in U59, all four right.
- **The audit's exit code is a measurement, not a constant.** It exited 2 for
  R-324 until issue #25 was reopened and it exits 1 now for R-265, the `In
  review` card. Read what it printed rather than what a record predicted, and do
  not soften `contradictions()` either way. Softening it now fails tests, which
  is new: R-322 put seven of them behind that function.
- **A double belongs at the PRODUCER's boundary, not at the shape it produces.**
  Hand-build the payload the network returns and let the real derivation run over
  it. Hand-building the derived structure asserts what its author believes the
  producer makes. And making an input injectable moves the undriven path one
  frame UP, to the caller that supplies nothing, so write the row for the default
  branch too.
- **Never write a closing keyword next to an issue number in prose**, not even
  inside backticks and not even to quote one. GitHub reads the text and not the
  intent.
- **Explanations are batched per phase.** No explainer inside a unit.
- **Do not touch** U30's board state, U20, R-9, A1, A2, `.worktrees/conformance`.
  The worktree stays on that list even though its branch has landed, because
  removing it is a cleanup Phillip takes once the merge is pushed.
