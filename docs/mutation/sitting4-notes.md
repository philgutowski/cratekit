# Fourth attended sitting, mutation notes, 2026-09-17

The table is `sitting4.md`, ten rows over the guards the R-355 fix added.
**Eight killed, two measured zero.** Rows are scoped to the round's own diff,
well inside METHOD's cap of 25, so nothing was dropped for room.

## The driver ran in a harness moved background job, twice

METHOD says run rows synchronously in the foreground. Both invocations were
started in the foreground and outlived the 600 second tool ceiling, so the
harness moved them to the background, which is the shape
`docs/solutions/workflow-issues/a-relay-task-finished-a-mutation-table-by-backgrounding-the-driver-the-rule-forbids.md`
records as not validated. The first run completed and reported every restore
verified against HEAD. The second did not, see below. Nothing in `tests/` was
edited while either ran.

## G7, zero, maintainer facing, equivalent mutation

Dropping the `path.is_file()` check before the tag read changes no behaviour,
because `tags.read_tag` opens the file inside a `try` and returns `None` for
anything it cannot read. The check is there so a missing file costs no open, not
to produce a different answer. One line, no composite, as METHOD allows for a
maintainer facing guard.

## G9, zero, user facing, and it found a real gap

Naming the wrong ID3 frame for the ISRC survived the whole suite. The round trip
test writes and reads through the SAME table, so a wrong key round trips
perfectly and only a file tagged by something else can tell the difference. That
is pattern four, a guard justified by a fixture that cannot fail it.

**Fixed rather than argued:** `test_an_isrc_another_tagger_wrote_is_read_from_the_standard_frame`
writes a bare `TSRC` frame with mutagen into a real AIFF and a real MP3 and
asserts the shipped reader returns it. It passes, and it fails against the
mutated table by construction.

**The remeasure was never run, and this is the honest statement of it.** The
round two row file was written and the driver was launched; the run was killed
by the operating system for memory pressure, with several unrelated Relay runs
holding the machine. It left the driver's null control comment appended to
`src/cratekit/core/tags.py`, which was restored from `git show HEAD:` and
verified clean. The round two row file was then deleted rather than left
implying a measurement. **So G9's kill is asserted by construction and not
measured.** The next session that touches `core/tags.py` should remeasure it:

    ./.venv/bin/python scripts/mutate.py docs/mutation/sitting4-rows.toml --resume

`--resume` reuses the eight rows already measured and runs only what changed.
