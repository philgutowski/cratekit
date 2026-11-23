# U300 S3: the composite on its user facing zero

`S3_restore_from_snapshot_skips_the_process_refusal` reads zero on the full
suite in `docs/mutation/u300.md`: replacing the call
`_writer().assert_rekordbox_closed("restoring the database")` in
`rb_copies.restore_from_snapshot` with `pass` kills no test. No source module
calls `restore_from_snapshot`; only `tests/test_rb_writer_db.py` and
`tests/test_rb_snapshot.py` do, with rekordbox closed, so no verb reaches the
call site the row removes. METHOD asks a user facing zero for a composite: a
mutation of the thing the call guards, with both counts.

**The composite**, measured by hand at `072589f6` (source and tests equal to
the table's head `fd1309d7`): in `core/rb_writer.py`, `assert_rekordbox_closed`
reads `running = None` instead of asking `rekordbox_processes_running()`, so
the refusal every caller shares never sees a process. The subset is the six
files that drive the guarded writer's refusals:
`tests/test_rb_writer_guard.py`, `tests/test_rb_writer_db.py`,
`tests/test_rb_snapshot.py`, `tests/test_write_session.py`,
`tests/test_restore.py`, `tests/test_restore_cli.py`, two workers.

| run | failed | passed |
|---|---|---|
| unmutated | 38, the machine's | 644 |
| the refusal blinded | 42 | 640 |

**4 killed**, each passing unmutated and failing mutated:

- `tests/test_rb_writer_db.py::test_the_commit_refuses_while_the_agent_is_running`
- `tests/test_rb_writer_guard.py::test_commit_guarded_refuses_when_agent_running`
- `tests/test_write_session.py::test_a_disagreement_reports_a_live_rekordbox_separately`
- `tests/test_write_session.py::test_both_the_read_back_failure_and_a_live_rekordbox_travel_together`

So the refusal S3's call reaches is held; what reads zero is only that
`restore_from_snapshot`, which no verb calls, asks it. The 38 failing in both
runs are the same ids, the machine's failures the battery's baseline lists.
