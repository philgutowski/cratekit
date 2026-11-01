---
name: crate-sync
description: One command from the streaming account's new music to filed and analysed in rekordbox. Runs the whole sync pass in an attended session, preflight, crate sync land, the rehearsed landing, the rekordbox visit and its check, then the account's marks and filing, and ends on one report, deciding by the standing rules in CLAUDE.md and asking Phillip only what no rule answers, batched at the end. Use when Phillip says /crate-sync, sync, run a pass, or bring in the new music.
---

# One command sync

Phillip's definition of done, set on 2026-10-27: he runs one sync, and his
latest playlists and hearts are downloaded, tagged, named, analysed on his
standard settings and filed in rekordbox, in a logical folder on the volume
and logical playlists in rekordbox. Sitting 47 reached that state after 25
messages from him over about three hours for 116 tracks;
`docs/plans/2026-10-27-one-command-sync.md` traces every one of them. This
skill is that pass with the messages taken out.

**Attended only.** The pass ends in the rekordbox visit, and rekordbox is
opened by an attended session and by nothing else (CLAUDE.md, the standing
constraints). A cloud session, a job and a test never run this skill.

**Decide, do not ask.** Every stop below is answered by a rule in CLAUDE.md:
the backup rule, the rehearsal rule, the acknowledgment rule, the actor
`session` on every gate. A question goes to Phillip only when no rule answers
it, such as a new vocal cut or a genre for a word the taxonomy does not know,
and every such question waits for the closing report, so the pass never stops
mid run to ask. The shipped `sync-and-publish` skill
(`src/cratekit/skills/assets/sync-and-publish/SKILL.md`) explains the queue,
the cursors and the gates the pass meets; read it there rather than here.

Run every `crate` line with `--output json` when the next step reads a field
from it; the field names below are the JSON's.

## 1. Preflight

Every one of these holds, or the pass does not start.

1. **The copy of Cratekit in use carries the verbs below.** `crate sync land
   --help` and `crate analyze check --help` both answer. If either refuses an
   unknown verb, run every `crate` line from a development checkout's own
   `.venv/bin/crate` until a release carries it, and say so in the report.
2. **Nothing else holds the library.** No Cratekit job is running and no other
   session is driving the library. This lists none:

       crate job list --state running

3. **The backups are fresh enough.** `crate doctor` shows `backup.age.files`
   and `backup.age.database`. At five days or more, or with either unknown,
   run `crate backup run` first and read the ages again, as CLAUDE.md's backup
   rule says. Under five days, no backup.
4. **rekordbox is closed.** `crate doctor` reads `rekordbox.closed` as ok.

## 2. The pass, to its landing gate

    crate --output json sync land

One verb runs the whole pass: `sync all`, the intake jobs it queued, the
missing list, the download, then the tail of `tag folder`, `analyze run`,
`analyze restamp` and `name apply` over the staging folder, and the landing
planned and stopped at its gate. Read `data.summary.stopped_at` and the exit
status:

- **It stopped at `intake.land.native`.** The pass is downloaded, tagged,
  analysed and named, and the landing waits under the run in
  `data.summary.gate_run`. Go to step 3.
- **It stopped at `backup-acknowledgment-missing`.** Mint the acknowledgment
  with `crate session ack`, answering its `session.ack.backup` gate as the
  session as CLAUDE.md's backup acknowledgment rule says (the session reads
  both ages and refuses unless both are under five days), then run the pass
  again, with `--pass-run` and the run in `data.summary.pass_run` when it
  names one, so the jobs already done are read and not queued again:

      crate --output json sync land --pass-run PASS_RUN

- **Several earlier passes hold open intake jobs.** It names each under
  `data.summary.open_passes`. Continue each with `crate sync land --pass-run`
  and the run it names, oldest first; this is a rule, not a question.
- **It ended with nothing to land.** Nothing new on the account. Skip to step 5,
  since an earlier pass may still owe its marks.
- **It failed.** The refusal names the step and its remedy. Act on the remedy
  when a rule covers it, and continue the pass with the `--pass-run` command
  its steps name; otherwise stop, and report the step and its message.

Write down for the report: `data.summary.download_refused` (a lossy only track,
above all), `data.summary.land_name` (the pass's name, which step 5 marks by),
and `data.summary.staging`.

## 3. The landing, rehearsed, then answered as the session

The landing writes the database, so its gate is answered by CLAUDE.md's
rehearsal rule. Rehearse the same landing on a scratch copy of its own:

    crate --output json intake land STAGING --pass PASS --rehearse

with `STAGING` the folder in `data.summary.staging` and `PASS` the name in
`data.summary.land_name`. It writes nothing live and reports the rehearsal's
digest. Then plan the live landing again on its own run, which now names the
rehearsal on its gate screen:

    crate --output json --run GATE_RUN intake land STAGING --pass PASS

`GATE_RUN` is `data.summary.gate_run` from step 2. It stops at the same gate.
Read `cause.detail.shown.rehearsal`:

- **It ends "equal to this plan's".** Answer and apply in one command:

      crate run decide GATE_RUN intake.land.native apply --actor session --continue

- **It names a digest that differs.** Read the lines under
  `cause.detail.shown["differs from the rehearsal"]`. A difference in a path,
  a run or the database's location is approved as above and recorded in the
  report. A difference in what is written (a row, a playlist, a file that is
  in one plan and not the other), or a rehearsal that failed, stops the pass:
  report both and answer nothing.

Read the applied envelope for the report: the rows added, the batch folder on
the volume, the playlists the batch joined, the rows that got the `vox` My
Tag, and every warning.

## 4. The rekordbox visit and its check

Follow the project's `rekordbox-visit` skill step by step: its preflight, the
analysis of INBOX / Analyze on Phillip's standard settings, the wait counted
in analysis files, the second run for rows marked `dyn`, the quit, `crate
analyze check`, and the clear with `crate inbox analyzed`. It is the one
procedure for the visit, and nothing it says is repeated here. Its verdict is
this pass's: a check that ends waiting or suspect stops the pass there, and
the report says what it named.

## 5. The account's tail: every finished pass marked, then filed

Both steps write the streaming account, so each stops at its own explicit
gate, `organize.account.apply`, answered as the session once its plan is read.
Neither writes the database.

**Mark every pass whose playlists landed and were never marked**, not only
this one. At sitting 48 a playlist from the 2026-10-14 pass sat at the account
root unrenamed because only the latest pass was marked. Organize plans one
step per landed pass, each listing its playlists with whether it is marked
and why not:

    crate --output json organize --only marks

Read every step under `data.summary.areas.account.steps`. A playlist held back
with a track still outstanding is left; the report names it. Then answer:

    crate run decide RUN_ID organize.account.apply apply --actor session --continue

**Then file what is marked**, a second run, since filing reads the marks as
they stood when it was planned:

    crate --output json organize --only file

Read its plan, then answer it the same way under its own run. **Never `crate
organize --only root`** as part of a pass: at sitting 48 it would have moved
all 53 playlists out of `2026 Custom Playlists`, which Phillip arranges by
hand, and he declined it.

To mark one playlist of a pass and not the others, `crate sync mark --pass
PASS --playlist ID` plans only that playlist and refuses one the pass did not
complete. The pass itself always marks whole passes.

## 6. One closing report

One message, in this order, and nothing before it except a stop:

1. **What landed.** The count, the batch folder on the volume, and the
   playlists in rekordbox it joined, from step 3.
2. **The visit.** `crate analyze check`'s verdict, its key agreement, and the
   rows cleared from INBOX / Analyze.
3. **The account.** The playlists marked, by pass, and where each was filed.
4. **What was refused or left.** Every download refused (`lossy-refused`
   above all), every track with no genre (it waits in INBOX for a hand tag),
   every review item, every playlist left unmarked with its reason, and every
   difference the rehearsal showed.
5. **The questions no rule answers**, each as a multiple choice with a
   recommendation first, batched here: a vocal cut that reads wrong, a genre
   word outside the taxonomy, anything else the pass could not decide.
6. **State.** The installed copy against the latest release (`crate doctor`'s
   `install.release`), whether the checkout that ran it is clean and current,
   and the attended cards now ready on the board.

Record the pass in `docs/cutover.md` as a sitting: one row per step, with its
run or job and its result, and the number of messages Phillip sent and the
wall time from start to report, against sitting 47's 25 messages and about
three hours.
