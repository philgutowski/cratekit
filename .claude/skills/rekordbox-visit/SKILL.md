---
name: rekordbox-visit
description: The one attended step Cratekit may not do itself. Open rekordbox and answer its Auto Analysis dialog when it shows every field of Phillip's standard and nothing else, or else analyse INBOX / Analyze with Analyze Tracks on those settings, wait for the analysis files, quit, check the result with crate analyze check, and clear the analysed rows. Use in an attended session when a landing has left rows waiting for analysis, when Phillip asks for the rekordbox visit, or when a sync pass stops at the visit.
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
Both wait the same way, run the same second run for rows marked `dyn`, quit
the same way and end on the same check and clear.

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
   run resets nothing.

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
     wrong settings that the visit's Normal run analyses again. A 27 for key
     agreement alone, with none of those grids, is not the visit's to fix:
     stop and report its message.
   - Exit 0 means nothing waits. With `data.summary.rows` above zero the rows
     are analysed, or gone from the collection (`data.summary.gone`), and
     were never cleared, so skip to the clear in step 7; with none there is
     no visit to make.

   Write down three numbers from it: the batch the Analyze Tracks path's
   wait counts to, which is `data.summary.analysed` plus
   `data.summary.not_analysed` (a row that left the collection is in
   `data.summary.rows` and in no count rekordbox shows);
   `data.summary.not_analysed`, which the Auto Analysis path's wait counts
   to, since Auto Analysis analyses only the rows rekordbox reads as not
   analysed; and the count of `data.summary.items` whose `dyn` is true, the
   rows the second run is for. A check that exited 27 has rows to analyse
   again, which Auto Analysis leaves alone, so that visit takes the Analyze
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
     run on the table's fields analyses every row of the batch again.

   Record the dialog's fields as it showed them, and which button was
   pressed, either way.
5. **A dialog that appears after the Analyze Tracks path has begun** is
   answered Cancel, never OK, and recorded.

### The Analyze Tracks path

1. In the tree, open Playlists, then the INBOX folder, then the playlist
   `Analyze` directly under it. Its track count matches the batch from step
   1.5; if it does not, stop and report both numbers.
2. Click one track in the list, then select all (Command A). The status line
   reads the same count.
3. Open Analyze Tracks on the selection (right click, Analyze Track).

**No Reload Tags, for rows landed by v0.4.0 or later.** Since U163 a landed
row carries its artist, album, genre and year from the commit that made it,
so the visit is Analyze Tracks alone. Rows landed by an earlier copy carry
none of them until rekordbox reads the file: for those, run Reload Tags on
the same selection first, as sitting 52 did.

## 3. Set and read back every field before OK

This table is the standard for both paths. The Auto Analysis dialog of step
2 is only read against it, never set. The Analyze Tracks dialog
opens on whatever the last run used, which at sitting 47 was
Dynamic, high precision on and KEY off. Never trust it. Set each field, then
take a screenshot of the dialog and read every field back against this table
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
`store` that directory, `expected` the batch from step 1.5, and `marker` the
path step 3 printed. On the Auto Analysis path `expected` is
`data.summary.not_analysed`, as step 2 says:

    store="<the analysis store>"; expected=<the batch>; marker="<the path step 3 printed>"
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

## 5. A second run with Dynamic, only for rows marked dyn

Only when step 1.5 counted rows whose `dyn` is true. A row is marked by a My
Tag value named `dyn`, which a native landing writes for a track whose tempo
moves (U157).

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

Record in the sitting record how the selection was made.

## 6. Quit and confirm both processes gone

Quit from the application menu (rekordbox, Quit rekordbox), never by killing
the process. Then wait until both of these print nothing, checking every few
seconds, since the agent can outlive the window:

    pgrep -x rekordbox
    pgrep -x rekordboxAgent

No verb runs until both are gone. If the agent is still running after two
minutes, report it rather than kill it.

## 7. Check the result, then clear the analysed rows

    crate --output json analyze check

`data.summary.scope` must still read `analyze`. Any other scope means the
playlist was emptied while rekordbox was open, by another session or a clear
nobody here ran, so its verdict is over other rows: stop and report it.
Otherwise the exit status is the verdict:

- **0, done.** Every row analysed, every grid one tempo (or moving on a row
  marked `dyn`), and the title keys agreeing with rekordbox's at the
  recorded rate. The check reports the Key column and does not judge it, so
  read it here: `data.summary.key_filled` must equal
  `data.summary.analysed`. A row with the Key column empty was analysed with
  KEY off, by an Auto Analysis on other fields or a run before this visit:
  stop and report the rows its message names, and clear nothing. Otherwise
  go on to the clear below.
- **12, waiting.** Rows are still not analysed. Stop and report the rows it
  names. Nothing is cleared, and the playlist keeps them for the next visit.
- **27, suspect.** What rekordbox wrote looks wrong: a variable grid on a row
  not marked `dyn`, a grid the check could not read, or keys agreeing far
  below the rate. Stop and report its message and its steps. Nothing is
  cleared.

On done, take the analysed rows out of the playlist:

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
three numbers; which path ran and why (no dialog, a dialog whose fields were
equal, or one cancelled, with the field that differed or went unread, and
whether rekordbox wrote after Cancel); the settings read back from the
dialog, field by field; the
wait's result and how long it took; the second run if there was one; both
processes confirmed gone; `crate analyze check`'s verdict, grids and key
agreement; the clear's rehearsed and live digests and what it read back. A
visit that stopped records where and what the screen or the verb said.
