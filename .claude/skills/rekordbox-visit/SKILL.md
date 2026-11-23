---
name: rekordbox-visit
description: The one attended step Cratekit may not do itself. Open rekordbox and answer its Auto Analysis dialog when it shows every field of Phillip's standard and nothing else, or else analyse INBOX / Analyze with Analyze Tracks on those settings, wait for the analysis files, quit, check the result with crate analyze check, give the titles that differ rekordbox's key and tempo with crate analyze adopt, and clear the analysed rows. Use in an attended session when a landing has left rows waiting for analysis, when Phillip asks for the rekordbox visit, or when a sync pass stops at the visit.
---

# The rekordbox visit

A native landing puts every row it adds into one playlist, INBOX / Analyze
(U166), and writes nothing about the audio: no tempo, no grid, no key. The
analysis is rekordbox's, and rekordbox is opened by an attended session and
by nothing else (CLAUDE.md, the standing constraints). This is that visit,
written so a session follows it without asking. At sitting 47 it took about
forty minutes and nine of Phillip's messages; every step below is one of
those messages.

**Attended only.** A cloud session, a job, a verb and a test never open
rekordbox or its background agent. If this session is not one Phillip is
present for, stop here.

**Two paths, the short one first** (U319). With Auto Analysis on in
rekordbox's preferences, a launch brought to the front raises one dialog and
its OK analyses the waiting rows with no selection: the Auto Analysis path,
in step 2. With Auto Analysis off, or with that dialog not showing every
field of Phillip's standard, or showing any field set otherwise, the visit is
the Analyze Tracks path: select INBOX / Analyze and set every field by hand.
Both wait the same way, run rows marked `dyn` with Dynamic, end with the
shared Analysis Mode on Normal (step 5), quit the same way and end on the
same check and clear.

**The two dialogs share one Analysis Mode** (U954). Sitting 104 (A190)
measured it: the launch's Auto Analysis dialog read Dynamic, every other
field the standard, and the Analyze Tracks dialog then opened on the same
fields, because the last Analyze Tracks OK writes the mode both show.
Sitting 103 had ended on its Dynamic run, so it set up the next visit to
cancel. So **the visit's last OK is always Normal**: on the Analyze Tracks
path the Dynamic run comes first and the Normal run last, and on the Auto
Analysis path a closing Normal run follows the Dynamic run. `docs/solutions/workflow-issues/rekordboxs-auto-analysis-dialog-shows-the-mode-the-last-analyze-tracks-ok-wrote.md`
is the learning.

**Phillip has not yet chosen to keep Auto Analysis on** (asked 2026-11-21),
and sitting 101 put it back to off, so today the launch raises no dialog
and the visit is the Analyze Tracks path. The Auto Analysis path is for the
visits after he turns it on, or after an attended session does on his
answer; the visit itself never does.

The steps say what to do, not which tool does it. Desktop control is the
tool that drives rekordbox; the shell runs every `crate` verb and every
check.

## 1. Before rekordbox opens

Every one of these holds, or the visit does not start.

0. **The copy of Cratekit in use carries the verbs below.** `crate analyze
   check` landed after v0.4.0 (U167). If `crate analyze check --help` refuses
   an unknown verb, run every `crate` line here from a development checkout's
   own `.venv/bin/crate` until a release carries it, and say so in the record.

1. **No Cratekit job is running**, and no other session is driving the
   library. This lists none:

       crate job list --state running

2. **Both backup ages are under five days.** `crate doctor` shows them as
   `backup.age.files` and `backup.age.database`. At five days or more, or with
   either unknown, run `crate backup run` first, as CLAUDE.md's backup rule
   says, and read the ages again. A quick run or a skip resets the ages as a
   full one does, since each proves the remote holds the library; a failed
   run resets nothing. One refused `library-root-unproven` or
   `library-root-foreign` found no library at the root, most often the volume
   not mounted: mount it and run the backup again, and never reach for
   `--library-emptied`, which is for a library emptied on purpose.

3. **rekordbox and rekordboxAgent are both gone.** `crate doctor` reads
   `rekordbox.closed` as ok, and from the shell `pgrep -x rekordbox` and
   `pgrep -x rekordboxAgent` both print nothing.

4. **The desktop control lock is free.** If another session on the machine
   holds it, that session releases it by turning desktop control off for
   itself from `/mcp`. Never delete the lock file: the forced handover at
   sitting 46 left the server unable to take a screenshot.

5. **Something waits, and it waits in INBOX / Analyze.** Run the check before
   the visit and read its JSON:

       crate --output json analyze check

   Read `data.summary.scope` first. It must read `analyze`: any other scope
   means INBOX / Analyze is empty and the rows waiting are somewhere else, so
   stop and report what it named rather than analyse a playlist that holds
   none of them. Then the exit status:

   - It must exit 12 with `data.summary.not_analysed` above zero for the
     visit to go on, or 27 with a `data.summary.grids` count above zero under
     `variable`, `absent`, `missing` or `unreadable`, which is a run on the
     wrong settings that the visit's Normal run analyses again. A title key
     or tempo that differs from rekordbox's never reads 27 (U327).
   - Exit 0 means nothing waits. With `data.summary.rows` above zero the rows
     are analysed, or gone from the collection (`data.summary.gone`), and
     were never cleared, so skip to the adopt and the clear in step 7; with none there is
     no visit to make.

   Write down three numbers from it: the batch the Analyze Tracks path's
   playlist count reads, which is `data.summary.analysed` plus
   `data.summary.not_analysed` (a row that left the collection is in
   `data.summary.rows` and in no count rekordbox shows);
   `data.summary.not_analysed`, which the Auto Analysis path's wait counts
   to, since Auto Analysis analyses only the rows rekordbox reads as not
   analysed; and the count of `data.summary.items` whose `dyn` is true, the
   rows the Dynamic run is for. The Analyze Tracks path's Normal run counts
   to the batch less that `dyn` count. A check that exited 27 has rows to
   analyse again, which Auto Analysis leaves alone, so that visit takes the Analyze
   Tracks path whatever the launch shows.

## 2. Open rekordbox: the Auto Analysis path first

**Auto Analysis is Phillip's standing setting, and the visit never changes
it.** It never turns Auto Analysis on or off and never changes a field of
rekordbox's Analysis preference; it reads them only through the dialog below.
Auto Analysis analyses every track rekordbox finds not analysed, by any
route, which is why it is his to choose.

What sitting 101 measured (A33): with Auto Analysis on, a launch whose
window stayed in the background analysed nothing in two minutes; brought to
the front, it raised one dialog, "Analysis Setting ... Auto Analysis is
starting.", showing the analysis fields with OK and Cancel, and OK analysed
every row waiting, before anything was selected, on the preference's own
fields, its mode Normal among them. The preference itself was read back as
nine fields: high precision off, Normal, BPM range 78 to 155, BPM / Grid, KEY
and Phrase on, Vocal off, Cloud Analysis off, Radar Analysis on. It holds no
CUE field. The launch dialog's own field list was not recorded.

1. Write the marker the launch is measured from, before rekordbox opens:

       opened=$(mktemp -t rekordbox-visit.XXXXXX); echo "$opened"

2. Open rekordbox through desktop control, wait for its main window, bring
   it to the front, and take a screenshot. Wait a further thirty seconds with
   the window in front and take another.
3. **No dialog on either screenshot**: Auto Analysis is off, as it is unless
   Phillip turned it on. Take the Analyze Tracks path below.
4. **The dialog is showing**: read back every field of the table in step 3
   from the dialog's screenshot, one by one. A table field the dialog does
   not show is unread, and unread is not equal, CUE included: until a visit
   has recorded the dialog's fields and that an Auto Analysis run sets no
   cue, a dialog that shows no CUE field is cancelled. A field it shows that
   the table has no row for must read as the preference read back above
   (BPM range 78 to 155, Cloud Analysis off, Radar Analysis on); any other
   field it shows, or another value, is not equal.
   - **Every field equal, and the check in step 1.5 exited 12**: write the
     marker the wait counts from, as step 3 gives it, then press OK. Wait as
     step 4 says, with `expected` the `data.summary.not_analysed` count from
     step 1.5, not the batch. Then go to step 5.
   - **Any field differs or is unread**, or the check exited 27: press
     Cancel, never OK, and touch no field of the dialog. Then wait thirty
     seconds and count whether rekordbox wrote anyway:

         find "<the analysis store>" -name ANLZ0000.DAT -newer "<the path step 2.1 printed>" | wc -l

     Zero: Cancel held; take the Analyze Tracks path below. Above zero:
     Cancel did not stop it, and rekordbox is analysing on its own fields.
     Wait as step 4 says with `marker` the path step 2.1 printed and
     `expected` the `data.summary.not_analysed` count, so nothing is
     selected while it runs, then take the Analyze Tracks path below, whose
     runs on the table's fields analyse every row of the batch again.
   - **A dialog reading Analysis Mode Dynamic** after a visit with `dyn`
     rows is this cause: that visit's last OK was its Dynamic run, which left
     the shared mode on Dynamic (U954, the note at the head of this skill).
     It is not equal: cancel it as above, and the Analyze Tracks path then
     sets every field, its last OK on Normal.

   Record the dialog's fields as it showed them, its Analysis Mode among
   them, and which button was pressed, either way.
5. **A dialog that appears after the Analyze Tracks path has begun** is
   answered Cancel, never OK, and recorded.

### The Analyze Tracks path

1. In the tree, open Playlists, then the INBOX folder, then the playlist
   `Analyze` directly under it. Its track count matches the batch from step
   1.5; if it does not, stop and report both numbers.
2. **The Dynamic run first**, when step 1.5 counted rows whose `dyn` is
   true: make it now, steps 5.1 to 5.4, then come back here. With no `dyn`
   row there is none.
3. Select the rows without `dyn`: click one track in the list, then select
   all (Command A), then Command click each row carrying the My Tag `dyn` to
   take it out of the selection. The status line reads the batch less the
   `dyn` count; with no `dyn` row, the batch. The Normal run's selection is
   the rows whose `dyn` is false, so the two runs never overlap and no row
   is analysed twice. With every row marked `dyn` there is no Normal run, so
   go to step 6 and record that the visit ended on Dynamic.
4. Open Analyze Tracks on the selection (right click, Analyze Track). Its
   OK, on the table's fields in step 3, is the visit's last, and leaves the
   shared Analysis Mode on Normal.

**No Reload Tags, for rows landed by v0.4.0 or later.** Since U163 a landed
row carries its artist, album, genre and year from the commit that made it,
so the visit is Analyze Tracks alone. Rows landed by an earlier copy carry
none of them until rekordbox reads the file: for those, run Reload Tags on
every row of the playlist first, before step 2, as sitting 52 did.

## 3. Set and read back every field before OK

This table is the standard for both paths. The Auto Analysis dialog of step
2 is only read against it, never set. The Analyze Tracks dialog
opens on whatever the last run used, which at sitting 47 was
Dynamic, high precision on and KEY off, and that last run's mode is the one
the next launch's Auto Analysis dialog shows (sitting 104). Never trust it.
Set each field, then take a screenshot of the dialog and read every field back against this table
before pressing OK:

| Field | Set to |
|---|---|
| Analysis Mode | Normal |
| High precision | off |
| BPM / Grid | on |
| Phrase | on |
| KEY | on |
| Vocal | off |
| CUE | off |

These are Phillip's standard, Vocal off included, confirmed by him on
2026-11-01. Sitting 52 ran with Vocal on as a one off; follow the table.

**The Analysis Mode list opens only while the mouse is held down on it.** A
click does nothing. Press and hold on the control, move to the item while
still holding, and release on it. Read the control back afterwards, since a
release in the wrong place leaves the old value showing.

Just before pressing OK, write the marker the wait counts from:

    marker=$(mktemp -t rekordbox-visit.XXXXXX); echo "$marker"

Then press OK. The path it printed is the marker the wait in step 4 needs.
On the Auto Analysis path the same line is run just before that dialog's OK.

**A run started on the wrong settings has no cancel that works.** Quit
rekordbox from its application menu (step 6), confirm both processes gone,
and start again from step 1.5, so the check is read again before step 2:
the rows the wrong run analysed are no longer waiting, which Auto Analysis
would leave alone, and a grid it made wrong reads 27, which takes the
Analyze Tracks path. Their second run overwrites what the first wrote.

## 4. Wait by counting analysis files, never by sleeping on a guess

Each track rekordbox finishes writes an `ANLZ0000.DAT` into the analysis
store, `share/PIONEER/USBANLZ` beside the configured database
(`library.db_path` in Cratekit's configuration). For a library on its own
volume that is `PIONEER/Master/share/PIONEER/USBANLZ` under the volume root.
Run this as a background job that notifies when it exits. A background job
is its own shell and does not see step 3's variable, so fill in all three:
`store` that directory, `expected` the count the run selected, and `marker`
the path step 3 printed. On the Analyze Tracks path's Normal run that is the
batch from step 1.5 less its `dyn` count; on the Auto Analysis path
`expected` is `data.summary.not_analysed`, as step 2 says; step 5 gives its
own runs':

    store="<the analysis store>"; expected=<the count the run selected>; marker="<the path step 3 printed>"
    last=-1; quiet=0
    while :; do
      n=$(find "$store" -name ANLZ0000.DAT -newer "$marker" | wc -l | tr -d ' ')
      if [ "$n" = "$last" ]; then quiet=$((quiet + 5)); else quiet=0; last=$n; fi
      if [ "$n" -ge "$expected" ] && [ "$quiet" -ge 20 ]; then echo "done: $n of $expected"; exit 0; fi
      if [ "$quiet" -ge 300 ]; then echo "stalled: $n of $expected"; exit 1; fi
      sleep 5
    done

It ends when the count reaches `expected` and the store has been quiet for
twenty seconds. Auto Analysis also analyses any other row rekordbox finds not
analysed, so on that path the count can pass `expected`; the quiet still ends
the wait, and the check in step 7 reads the batch's own rows. Roughly five seconds a track. `-newer` reads the modification
time, so a file rewritten by the run counts as well as a new one. **A stall**,
five minutes with no file written short of `expected`, means look at the
screen: a dialog rekordbox raised, or a run that stopped. Report what it shows
and do not quit until the screen has been read.

## 5. The Dynamic run for rows marked dyn, and the mode left on Normal

Only when step 1.5 counted rows whose `dyn` is true. A row is marked by a My
Tag value named `dyn`, which a native landing writes for a track whose tempo
moves (U157).

Its place in the visit is set by the shared Analysis Mode (the note at the
head of this skill), so the visit's last OK is Normal:

- **On the Analyze Tracks path it comes first**, at that path's step 2,
  steps 5.1 to 5.4 only; the Normal run on the rows without `dyn` follows
  it, and after that run's wait the visit goes on to step 6.
- **On the Auto Analysis path it comes after the Auto Analysis OK**, which
  analysed every waiting row on Normal before anything was selected, and
  step 5.5, the closing Normal run, follows it.

1. In INBOX / Analyze, show only the rows carrying the My Tag `dyn` (the
   track list's My Tag filter), and select all; a click and Command clicks
   on each such row serve as well. On the Auto Analysis path nothing is open
   yet: open the playlist as the Analyze Tracks path's first step says. The
   count equals the `dyn` count from step 1.5, or stop and report both.
2. Analyze Tracks with every field as the table in step 3 says except
   Analysis Mode, which is **Dynamic**, set with the same held press and read
   back.
3. Write a new marker just before OK and wait as step 4 says, with `expected`
   the `dyn` count.
4. Clear the filter.
5. **The closing Normal run, on the Auto Analysis path only**, the step
   that leaves Normal set. Click one row of INBOX / Analyze without the My
   Tag `dyn`, and open Analyze Tracks on it with every
   field as the table in step 3 says, Analysis Mode **Normal**, set with the
   same held press and read back. Write a new marker just before OK and wait
   as step 4 says, with `expected` 1. That row is analysed again on the
   standard's fields, the ones the Auto Analysis dialog showed equal, and
   this OK, the visit's last, leaves
   the shared mode on Normal. With every row of the batch marked `dyn` there
   is no row for it: skip it, and record that the visit ended on Dynamic, so
   the next launch's dialog reads Dynamic and step 2 cancels it.

Record in the sitting record how each selection was made.

## 6. Quit and confirm both processes gone

Quit from the application menu (rekordbox, Quit rekordbox), never by killing
the process. Then wait until both of these print nothing, checking every few
seconds, since the agent can outlive the window:

    pgrep -x rekordbox
    pgrep -x rekordboxAgent

No verb runs until both are gone. If the agent is still running after two
minutes, report it rather than kill it.

## 7. Check the result, adopt rekordbox's answer, then clear the analysed rows

    crate --output json analyze check

`data.summary.scope` must still read `analyze`. Any other scope means the
playlist was emptied while rekordbox was open, by another session or a clear
nobody here ran, so its verdict is over other rows: stop and report it.
Otherwise the exit status is the verdict:

- **0, done.** Every row analysed and every grid one tempo (or moving on a row
  marked `dyn`). Titles whose key or tempo differs from rekordbox's are
  counted in `data.summary.differs` and never hold the visit; the adopt below
  gives them rekordbox's. The check reports the Key column and does not judge it, so
  read it here: `data.summary.key_filled` must equal
  `data.summary.analysed`. A row with the Key column empty was analysed with
  KEY off, by an Auto Analysis on other fields or a run before this visit:
  stop and report the rows its message names, and clear nothing. Otherwise
  go on to the adopt below.
- **12, waiting.** Rows are still not analysed. Stop and report the rows it
  names. Nothing is cleared, and the playlist keeps them for the next visit.
- **27, suspect.** What rekordbox wrote looks wrong: a variable grid on a row
  not marked `dyn`, or a grid the check could not read. Stop and report its
  message and its steps, and clear nothing. Keys that differ never read 27:
  Phillip decided on 2026-11-22 that where a title's key or tempo differs
  from rekordbox's, rekordbox's wins, and the adopt below writes it. Reload
  Tags is never run on these rows, since it puts the file's key over
  rekordbox's.

On done, give every title that differs rekordbox's key and tempo, before the
clear, while the rows are still in INBOX / Analyze:

    crate --output json analyze adopt

It needs the backup acknowledgment, which the session mints with `crate
session ack --as session` as CLAUDE.md's backup acknowledgment rule says, the
clear below reading the same one, and stops at its own gate, `analyze.adopt.confirm`, listing every row before and after with
its key relation and tempo. It writes the row's title in the database and the
file's title tag and key tag, and never the Key or BPM columns, a grid or a
file name. That gate is a database write, so it is answered by CLAUDE.md's
rehearsal rule as the clear's is, with one difference: **the rehearsal stops
at the gate and never goes past it**, since the copy's rows name the real
files and an apply on the copy would write their tags. The rehearsed digest
names no path, so it equals the live plan's when the rows are the same; then
answer the live gate as the session:

    crate run decide --actor session --continue RUN_ID analyze.adopt.confirm apply

Read the answer: `data.totals.written` rows took rekordbox's, and every row
left is named with why in the warnings. A file it could not write keeps its
row's old title and is named; report it. With `data.summary.differs` at zero
the plan writes nothing, and the gate is still answered, ending as a no op. An
`adopt-scope-empty` warning means INBOX / Analyze is absent or holds no row, so
nothing was planned: after a check whose scope read `analyze` that is a stop,
so report it. An intake tree that cannot be read refuses before the gate with
its own reason: stop and report it. An exit with `analyze-adopt-unwritten`
means the named files could not take their new title, their rows kept the old
one, and the rest landed, with every row left still named in the warnings:
report them and go on to the clear. **The clear's
rehearsal copy is taken after the live adopt**, since the clear's digest covers
each row's title and a copy taken before it rehearses the old titles. Then
take the analysed rows out of the playlist:

    crate inbox analyzed

It needs the backup acknowledgment, which the session mints with `crate
session ack --as session` as CLAUDE.md's backup acknowledgment rule says, and
it stops at its own gate,
`inbox.analyzed.approve`. That gate is a database write, so it is answered by
CLAUDE.md's rehearsal rule: the same verb driven on a disposable copy with
library state redirected, as `docs/solutions/workflow-issues/a-disposable-database-copy-does-not-make-library-state-disposable.md`
sets out, its digest compared with the live plan's, then the live gate
answered as the session:

    crate run decide --actor session --continue RUN_ID inbox.analyzed.approve apply

It reads INBOX / Analyze back, which then holds only the rows still waiting:
none, after a visit that ended done. A row that left the collection stays,
named as removed, and the record says so.

## When desktop control cannot take a screenshot

The clicks still work, so do not stop with rekordbox open. Take the picture
from the shell after each action, `screencapture -x -C -t png <file>`, and
read that file. With no server screenshot, click coordinates are the
capture's own pixels, scaled by the factor the image reader states when it
downsamples. Check the mapping once per session before the first click: move
the mouse to a known point, capture with the cursor, and read where the tip
landed. `docs/solutions/workflow-issues/desktop-controls-screenshot-can-fail-while-its-clicks-work-so-the-shell-capture-is-the-eyes-and-its-pixels-are-the-coordinates.md`
is the learning and has the measured numbers.

## What to record

One row per step in the sitting record in `docs/cutover.md`: the pre check's
three numbers; the Analysis Mode the launch's Auto Analysis dialog showed, or
that no dialog showed; which path ran and why (no dialog, a dialog whose fields were
equal, or one cancelled, with the field that differed or went unread, and
whether rekordbox wrote after Cancel); the settings read back from the
dialog, field by field; the
wait's result and how long it took; the Dynamic run if there was one, the
runs in the order they ran and the Analysis Mode the last OK set; both
processes confirmed gone; `crate analyze check`'s verdict, grids, key
agreement and the titles that differ; `crate analyze adopt`'s rehearsed and
live digests, the rows written and the rows left; the clear's rehearsed and
live digests and what it read back. A
visit that stopped records where and what the screen or the verb said.
