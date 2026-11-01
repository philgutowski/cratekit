"""R-678: the renderer's job and import proof cases, and the gates that bound them.

The verbs themselves are driven in human mode beside their own fixtures, in
``tests/intake/test_workers.py``, ``tests/test_acquire_workers.py``,
``tests/test_tag_workers.py`` and ``tests/test_intake_imported.py``. This file
holds what a verb cannot reach: a payload of the right schema from a verb the
case was not written for, and the dispatcher's refusal to name a second driver.
"""

from __future__ import annotations

import pytest

from cratekit import cli
from cratekit.cli import output, render
from cratekit.core import config, jobs
from tests.cli_drive import drive_human
from tests.test_config import valid_data

STARTED = "2026-09-23T00:00:00+00:00"


def envelope(verb: str, schema: str, data: dict) -> output.Envelope:
    return output.build(
        verb=verb, run_id="r", schema=output.current_schema(schema), started=STARTED, data=data
    )


def job_state(verb: str = "tag.folder", **data) -> output.Envelope:
    payload = {"job_id": "j-1", "state": "queued", "cause": None, "progress": {}}
    payload.update(data)
    return envelope(verb, "job_state", payload)


FROZEN_ROWS = [
    {"item": "rc_1", "artist": "Aurora Bloom", "title": "Sun Path", "version": "", "isrc": "X1"},
    {"item": "rc_2", "artist": "", "title": "", "version": "", "isrc": None},
]


def test_job_show_lists_the_frozen_tracks_and_a_payload_without_them_prints_none():
    """R-925. Read by field, and the field is not ``tracks``, which counts elsewhere."""
    shown = render.render_job_state(job_state(verb="job.show", progress={"intake_tracks": FROZEN_ROWS}))
    assert shown[-3:] == ["  tracks: 2", "    1. Aurora Bloom - Sun Path, isrc X1", "    2. item rc_2, no isrc"]
    other = render.render_job_state(job_state(verb="job.show", progress={"tracks": FROZEN_ROWS}))
    assert not any("tracks:" in line or "Sun Path" in line for line in other)


def test_an_intake_tracks_field_that_is_not_a_list_prints_nothing():
    for value in (3, "Aurora Bloom - Sun Path", None):
        lines = render.render_job_state(job_state(verb="job.show", progress={"intake_tracks": value}))
        assert not any("tracks:" in line for line in lines), value


def test_the_renderer_spells_the_field_cli_jobs_writes():
    from cratekit.cli import jobs as cli_jobs

    assert render._INTAKE_TRACKS == cli_jobs.TRACKS_FIELD


def test_a_queued_job_names_its_drive_only_when_one_is_handed_in():
    """The drive command comes from the dispatcher; without it no command is guessed."""
    bare = render.render_job_state(job_state())
    driven = render.render_job_state(job_state(), drive=["tag", "folder", "/x y", "--job", "j-1"])

    assert "  job: j-1, queued" in bare
    assert not any(line.startswith("  drive it with:") for line in bare)
    assert "  drive it with: crate tag folder '/x y' --job j-1" in driven


def test_a_job_that_is_not_queued_names_no_drive_even_when_handed_one():
    lines = render.render_job_state(job_state(state="running"), drive=["tag", "folder", "x"])
    assert not any(line.startswith("  drive it with:") for line in lines)


def test_an_empty_job_id_is_a_queue_that_held_nothing_and_renders_nothing():
    assert render.render_job_state(job_state(job_id="", state="no-tracks")) == []


def test_the_job_case_is_gated_on_the_schema_not_a_job_id_key():
    """A job identifier at the TOP of another surface's data, where the job case reads it.

    Nested under ``summary`` it was stopped by the empty identifier gate instead,
    and the mutation table measured this gate at zero until the key was lifted.
    """
    review_set = envelope(
        "review.list",
        "review_set",
        {"queue": "q", "items": [], "unresolved": 0, "job_id": "j-1", "state": "queued"},
    )
    assert render.render_job_state(review_set) == []
    assert render.render_job_state(review_set, drive=["x"]) == []


def test_the_resolution_counts_belong_to_the_intake_verbs_alone():
    """Another job_state verb whose progress happened to carry the words is not a resolution."""
    counts = {"owned": 1, "offered": 0, "missing": 2, "suppressed": 0, "total": 3, "settled": 3}
    tagged = render.render_job_state(job_state(state="succeeded", progress=counts))
    intake = render.render_job_state(
        job_state(verb="intake.playlist", state="succeeded", progress=counts)
    )

    assert not any(line.startswith("  owned:") for line in tagged)
    assert "  owned: 1 already in the library" in intake
    assert "  next: crate intake missing --job j-1" in intake


def test_a_resolution_word_the_progress_does_not_carry_is_not_printed_as_zero():
    lines = render.render_job_state(
        job_state(verb="intake.set", state="succeeded", progress={"owned": 3, "missing": 0})
    )
    assert "  owned: 3 already in the library" in lines
    assert not any(line.startswith("  offered:") for line in lines)
    assert not any(line.startswith("  next:") for line in lines)


def test_the_reasons_follow_their_count_most_rows_first_and_ties_by_slug():
    """R-682. The order is the count's, then the slug's, so two runs print alike."""
    progress = {
        "owned": 6,
        "missing": 1,
        "by_reason": {
            # Inserted out of slug order, so a sort that drops the tie break shows.
            "owned": {"verdict-accepted": 1, "isrc-exact": 1, "exact": 3, "credited-exact": 1},
            "missing": {"not-in-library": 1},
        },
    }
    lines = render.render_job_state(
        job_state(verb="intake.playlist", state="succeeded", progress=progress)
    )

    owned_at = lines.index("  owned: 6 already in the library")
    assert lines[owned_at + 1] == (
        "    by reason: exact 3, credited-exact 1, isrc-exact 1, verdict-accepted 1"
    )
    missing_at = lines.index("  missing: 1 not in the library")
    assert lines[missing_at + 1] == "    by reason: not-in-library 1"


@pytest.mark.parametrize(
    "by_reason",
    [
        None,
        "exact 3",
        {"owned": ["exact"]},
        {"missing": {"not-in-library": 1}},
    ],
    ids=["absent", "not-a-mapping", "state-not-a-mapping", "other-state"],
)
def test_reasons_an_older_or_malformed_progress_cannot_state_print_no_line(by_reason):
    """A build before R-682 carried no ``by_reason``; nothing is printed as if counted."""
    progress = {"owned": 3} | ({} if by_reason is None else {"by_reason": by_reason})
    lines = render.render_job_state(
        job_state(verb="intake.set", state="succeeded", progress=progress)
    )

    assert "  owned: 3 already in the library" in lines
    assert not any(line.startswith("    by reason:") for line in lines)


@pytest.mark.parametrize(
    ("reasons", "said"),
    [
        ({"exact": 1, "isrc-exact": 1}, "    by reason: exact 1, isrc-exact 1, unstated 2"),
        ({}, "    by reason: unstated 4"),
        ({"exact": "3", "isrc-exact": True, "title-approximate": 0}, "    by reason: unstated 4"),
        ({"exact": 4}, "    by reason: exact 4"),
    ],
    ids=["partial", "empty", "no-whole-count", "complete"],
)
def test_rows_no_reason_explains_are_said_rather_than_read_as_complete(reasons, said):
    """A breakdown that falls short of its count names the shortfall last."""
    progress = {"owned": 4, "by_reason": {"owned": reasons}}
    lines = render.render_job_state(
        job_state(verb="intake.set", state="succeeded", progress=progress)
    )

    assert said in lines


def test_a_bool_is_not_a_count_in_the_resolution():
    progress = {"owned": True, "missing": True, "by_reason": {"owned": {"exact": 1}}}
    lines = render.render_job_state(
        job_state(verb="intake.set", state="succeeded", progress=progress)
    )

    assert not any(line.startswith(("  owned:", "  missing:", "  next:")) for line in lines)
    assert not any(line.startswith("    by reason:") for line in lines)


def test_the_reasons_belong_to_the_intake_verbs_alone():
    progress = {"owned": 1, "by_reason": {"owned": {"exact": 1}}}
    lines = render.render_job_state(job_state(state="succeeded", progress=progress))
    assert not any(line.startswith("    by reason:") for line in lines)


def test_the_import_proof_is_gated_on_the_verb_as_well_as_the_schema():
    """Every planning verb answers plan/1 and only this one's items carry an action."""
    items = [{"session_id": "s", "action": "imported", "count": 2, "retired_to": "/a/f.xml.imported"}]
    plan = {"digest": "d", "items": items, "totals": {}, "chunk": None}

    assert render.render_import_proof(envelope("profile.set", "plan", plan)) == []
    lines = render.render_import_proof(envelope("intake.imported", "plan", plan))
    assert "  run s: proven imported, 2 track(s); intake file retired to f.xml.imported" in lines
    assert "  proven: 1 run(s), 2 track(s); retired: 1 intake file(s)" in lines


@pytest.mark.parametrize(
    ("item", "said"),
    [
        (
            {"session_id": "s", "action": "imported", "count": 1, "retired_to": None},
            "  run s: proven imported, 1 track(s); no intake file to retire",
        ),
        (
            {"session_id": "s", "action": "unverifiable", "why": "nothing recorded"},
            "  run s: not verifiable, nothing recorded",
        ),
        (
            {"session_id": "s", "action": "retired", "retired_to": "/a/g.xml.imported", "closed": True},
            "  run s: proven earlier; intake file retired to g.xml.imported; run closed",
        ),
        (
            {"session_id": "s", "action": "something-new"},
            "  session_id=s, action=something-new",
        ),
    ],
)
def test_each_proof_action_is_worded_and_an_unknown_one_keeps_its_fields(item, said):
    plan = {"digest": "d", "items": [item], "totals": {}, "chunk": None}
    assert said in render.render_import_proof(envelope("intake.imported", "plan", plan))


def test_a_verb_showing_a_queued_job_it_did_not_queue_names_no_drive(tmp_path, monkeypatch):
    """``job show`` and ``job resume`` answer with a queued job too, and must not name a
    second driver for it. Driven through the dispatcher, because the check lives there."""
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(tmp_path))
    built = config.from_dict(valid_data(tmp_path))
    config.save(built)
    config.reset_cache()
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key="tag.folder",
            payload={"folder": str(tmp_path)},
            cfg=built,
            item_ids=("a.flac",),
        )

    code, text = drive_human(["job", "show", job.job_id])

    assert code == 0, text
    assert f"  job: {job.job_id}, queued" in text.splitlines(), text
    assert "drive it with" not in text, text
    assert cli._drive_argv(job_state(verb="tag.folder", job_id=job.job_id)) == [
        "tag", "folder", str(tmp_path), "--job", job.job_id,
    ]


def test_a_job_the_queue_cannot_find_names_no_drive_rather_than_one_that_refuses(
    tmp_path, monkeypatch
):
    """``job resume`` reads the same row and would refuse the same way, so nothing is named."""
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(tmp_path))
    config.save(config.from_dict(valid_data(tmp_path)))
    config.reset_cache()

    assert cli._drive_argv(job_state(job_id="no-such")) is None


def test_a_builder_that_raises_leaves_the_queued_verb_a_success(tmp_path, monkeypatch):
    """The lookup runs outside the boundary, so a raise there would be a traceback over a queue."""
    from cratekit.cli import jobs as cli_jobs

    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(tmp_path))
    config.save(config.from_dict(valid_data(tmp_path)))
    config.reset_cache()
    folder = tmp_path / "downloads"
    folder.mkdir()
    (folder / "a.flac").write_bytes(b"")

    def broken(job):
        raise TypeError("a frozen payload this builder did not expect")

    monkeypatch.setattr(cli_jobs, "argv_for", broken)
    code, text = drive_human(["tag", "folder", "--queue-only", str(folder)])

    assert code == 0, text
    assert text.splitlines()[0] == "tag.folder: ok", text
    assert any(line.startswith("  job: ") and line.endswith(", queued") for line in text.splitlines())
    assert "drive it with" not in text, text


def test_a_resolution_that_did_not_succeed_names_no_next_command():
    """``intake missing`` refuses a job that has not succeeded, so it is not offered."""
    counts = {"owned": 1, "offered": 0, "missing": 2, "suppressed": 0}
    lines = render.render_job_state(job_state(verb="intake.playlist", state="running", progress=counts))

    assert "  missing: 2 not in the library" in lines
    assert not any(line.startswith("  next:") for line in lines)


def test_the_proven_run_count_is_the_verbs_own_total():
    items = [{"session_id": "s", "action": "imported", "count": 2, "retired_to": None}]
    plan = {"digest": "d", "items": items, "totals": {"imported": 3}, "chunk": None}
    lines = render.render_import_proof(envelope("intake.imported", "plan", plan))
    assert "  proven: 3 run(s), 2 track(s); retired: 0 intake file(s)" in lines


def test_a_shown_item_value_that_would_break_its_line_is_quoted():
    """R-692: an artist with a comma, a title with an equals sign, or a value
    holding either line break would otherwise read as a field of its own or
    split the item. Each breaker is alone in its value, so dropping one from
    the set is seen. A quoted value keeps its letters, and a plain value and a
    non string one print as they always did."""
    (header, line) = render._shown_lines({
        "items": [{
            "artist": "\u00c2me, Dixon",
            "title": "Dub=Mix",
            "note": "Part\n2",
            "also": "Part\r3",
            "track_id": "11",
            "vocal": "",
            "count": 3,
        }]
    })
    assert header == "  items:"
    assert line == (
        '    artist="\u00c2me, Dixon", title="Dub=Mix", note="Part\\n2", '
        'also="Part\\r3", track_id=11, vocal=, count=3'
    )


# ═══════════════════════════════════════════════════════════════════════════
# R-850: what an export wrote and every track it left out
# ═══════════════════════════════════════════════════════════════════════════


def _exported(state: str = "succeeded", **outbound) -> output.Envelope:
    return job_state("export.playlist", state=state, progress={"outbound": outbound})


def test_an_export_answer_counts_and_names_each_track_it_left_out():
    lines = render.render_job_state(
        _exported(
            counts={"written": 2, "already": 1, "unmatched": 2},
            unmatched_tracks=[
                {"identity": "7", "artist": "A", "title": "T", "reason": "names 2 provider tracks"},
                {"identity": "9", "artist": "", "title": "", "reason": ""},
            ],
        )
    )
    assert "  tracks: 2 written, 1 already there or written before, 2 unmatched" in lines
    assert "    unmatched: A - T: names 2 provider tracks" in lines
    assert "    unmatched: row 9: no reason given" in lines


def test_a_queued_export_prints_no_counts_since_it_has_written_nothing_yet():
    lines = render.render_job_state(
        _exported(state="queued", counts={"written": 0, "already": 0, "unmatched": 0})
    )
    assert not any(line.startswith("  tracks:") for line in lines)


def test_a_favourites_answer_counts_in_its_own_words_and_names_each_unhearted_row():
    """R-856: the sweep's counts are printed as hearts, not as playlist writes."""
    lines = render.render_job_state(
        job_state(
            "sync.favorites",
            state="succeeded",
            progress={
                "outbound": {
                    "counts": {"hearted": 2, "already_hearted": 1, "unmatched": 1},
                    "unmatched_tracks": [
                        {"identity": "3", "artist": "A", "title": "T", "reason": "names 2"},
                    ],
                }
            },
        )
    )
    assert "  tracks: 2 hearted, 1 already hearted or hearted before, 1 unmatched" in lines
    assert "    unmatched: A - T: names 2" in lines


def test_an_outbound_summary_that_does_not_count_prints_no_track_line():
    """A summary carrying lists and no ``counts``, the favourites sweep's shape
    before R-856 and what any outbound verb that does not count still is."""
    lines = render.render_job_state(
        _exported(hearted=["1"], already=[], unmatched=["2"], reasons=[])
    )
    assert not any("tracks:" in line or "unmatched:" in line for line in lines)


def test_a_count_this_build_cannot_read_is_left_out_rather_than_shown_as_zero():
    lines = render.render_job_state(
        _exported(counts={"written": 3, "already": True, "unmatched": "1"})
    )
    assert "  tracks: 3 written" in lines


def test_an_unmatched_title_holding_a_line_break_stays_on_its_line():
    lines = render.render_job_state(
        _exported(
            counts={"written": 0, "already": 0, "unmatched": 1},
            unmatched_tracks=[{"identity": "4", "artist": "A, B", "title": "T\nU", "reason": "r"}],
        )
    )
    assert '    unmatched: A, B - "T\\nU": r' in lines


# ═══════════════════════════════════════════════════════════════════════════
# U169: ``job list`` prints the jobs it found, not only a run id
# ═══════════════════════════════════════════════════════════════════════════


def _listed(handler: str, state: str, *, settled: int = 0, total: int = 0, **extra) -> dict:
    row = {
        "job_id": f"{handler}-{state}",
        "handler": handler,
        "worker": "bound",
        "worker_reason": None,
        "state": state,
        "progress": {"total": total, "settled": settled, "counts": {}},
        "cause": None,
    }
    row.update(extra)
    return row


def _job_list(rows: list[dict], **counts) -> output.Envelope:
    every = {"queued": 0, "running": 0, "blocked": 0, "succeeded": 0, "failed": 0, "cancelled": 0}
    every.update(counts)
    return job_state(
        verb="job.list",
        job_id="",
        state="all",
        progress={"jobs": rows, "counts": every},
    )


def test_job_list_prints_one_line_per_job_with_its_verb_state_progress_and_cause():
    """Sitting 47: 22 jobs queued and four run, and the human output was a run id."""
    refused = {"reason": "lossy-refused", "message": "the provider offers it lossy only"}
    rows = [
        _listed("acquire.download", "failed", settled=117, total=117, cause=refused),
        _listed("tag.folder", "running", settled=3, total=10),
        _listed("intake.playlist", "queued", total=40),
        _listed("analyze.run", "succeeded", settled=8, total=8),
    ]
    lines = render.render_job_list(_job_list(rows, failed=1, running=1, queued=1, succeeded=1))

    assert "  jobs: 4 (queued 1, running 1, succeeded 1, failed 1)" in lines, lines
    assert (
        "  acquire.download-failed, acquire.download, failed, 117 of 117 settled, lossy-refused"
        in lines
    ), lines
    assert "  tag.folder-running, tag.folder, running, 3 of 10 settled" in lines, lines
    assert "  intake.playlist-queued, intake.playlist, queued, 0 of 40 settled" in lines, lines
    assert "  analyze.run-succeeded, analyze.run, succeeded, 8 of 8 settled" in lines, lines
    assert lines[-1] == "  each job in full: crate job show JOB_ID", lines


def test_job_list_says_how_many_tracks_a_succeeded_job_skipped():
    """Review round one: a skipped track is settled, not landed, and the line
    said only ``3 of 3 settled`` over it."""
    progress = {"total": 3, "settled": 3, "counts": {"done": 2, "skipped": 1, "failed": 0}}
    rows = [_listed("acquire.download", "succeeded", progress=progress)]
    lines = render.render_job_list(_job_list(rows, succeeded=1))

    assert (
        "  acquire.download-succeeded, acquire.download, succeeded, 3 of 3 settled, 1 skipped"
        in lines
    ), lines
    none_skipped = {"total": 2, "settled": 2, "counts": {"done": 2, "skipped": 0}}
    quiet = render.render_job_list(
        _job_list([_listed("tag.folder", "succeeded", progress=none_skipped)], succeeded=1)
    )
    assert not any("skipped" in line for line in quiet), quiet


def test_job_list_says_when_a_verb_has_no_worker_to_run_its_job():
    rows = [_listed("label.sweep", "queued", total=2, worker="none")]
    lines = render.render_job_list(_job_list(rows, queued=1))

    assert "  label.sweep-queued, label.sweep, queued, 0 of 2 settled, no worker" in lines


def test_an_empty_job_list_says_none_rather_than_printing_nothing():
    lines = render.render_job_list(_job_list([]))

    assert lines == ["", "  jobs: none"], lines


def test_a_filtered_empty_job_list_names_the_states_it_was_filtered_to():
    lines = render.render_job_list(
        job_state(verb="job.list", job_id="", state="failed,blocked", progress={"jobs": [], "counts": {}})
    )

    assert lines == ["", "  jobs: none in failed,blocked"], lines


def test_the_job_list_case_belongs_to_the_listing_alone():
    """Another verb's ``job_state`` with a jobs key is not a listing, and a
    listing is never read as a single job."""
    rows = [_listed("tag.folder", "queued", total=1)]
    other = job_state(verb="job.show", job_id="", progress={"jobs": rows, "counts": {}})

    assert render.render_job_list(other) == []
    assert render.render_job_state(_job_list(rows, queued=1)) == []


@pytest.mark.parametrize("progress", [None, {}, {"jobs": "not a list"}, {"jobs": [3, None]}])
def test_a_listing_progress_this_build_cannot_read_prints_nothing_rather_than_none(progress):
    """Absence is not evidence: an unreadable listing is not an empty queue."""
    assert render.render_job_list(job_state(verb="job.list", job_id="", progress=progress)) == []


def test_job_list_is_driven_end_to_end_in_the_default_output(tmp_path, monkeypatch):
    """The dispatcher's own answer, so a renderer nobody calls cannot pass."""
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(tmp_path))
    built = config.from_dict(valid_data(tmp_path))
    config.save(built)
    config.reset_cache()
    with jobs.open_store() as store:
        queued = jobs.enqueue(
            store,
            handler_key="tag.folder",
            payload={"folder": str(tmp_path)},
            cfg=built,
            item_ids=("a.flac", "b.flac"),
        )

    code, text = drive_human(["job", "list"])

    assert code == 0, text
    assert f"  {queued.job_id}, tag.folder, queued, 0 of 2 settled" in text.splitlines(), text
    assert "  jobs: 1 (queued 1)" in text.splitlines(), text


# ═══════════════════════════════════════════════════════════════════════════
# U182: the playlist an intake job was made for, and the stale cancel's list
# ═══════════════════════════════════════════════════════════════════════════


def test_the_renderer_spells_the_playlist_and_stale_fields_cli_jobs_writes():
    from cratekit.cli import jobs as cli_jobs

    assert render._PLAYLIST == cli_jobs.PLAYLIST_FIELD
    assert render._SOURCE == cli_jobs.SOURCE_FIELD
    assert render._STALE_DAYS == cli_jobs.STALE_FIELD
    assert render._DRY_RUN == cli_jobs.DRY_RUN_FIELD
    assert [field for field, _done, _would in render._CANCEL_LISTS] == [
        cli_jobs.CANCEL_LIST,
        cli_jobs.KEPT_LIST,
        cli_jobs.LEFT_LIST,
    ]


def test_job_show_and_list_print_the_playlist_and_its_source_when_it_differs():
    shown = render.render_job_state(
        job_state(verb="job.show", progress={"playlist": "Warmup", "source": "pl-a"})
    )
    assert "  playlist: Warmup (pl-a)" in shown
    same = render.render_job_state(
        job_state(verb="job.show", progress={"playlist": "pl-z", "source": "pl-z"})
    )
    assert "  playlist: pl-z" in same
    listed = render.render_job_list(
        job_state(
            verb="job.list",
            job_id="",
            progress={"jobs": [{"job_id": "j-1", "handler": "intake.playlist", "state": "queued", "playlist": "Warmup"}]},
        )
    )
    assert "  j-1, intake.playlist, queued, playlist Warmup" in listed


def _stale_payload(dry_run: bool) -> output.Envelope:
    row = {
        "job_id": "j-old",
        "label": "playlist 'Warmup' (pl-a)",
        "age_days": 44,
        "tracks": 144,
        "same_tracks": ["j-new"],
        "reason": "a copy of the tracks job j-new holds; j-new is kept",
        "frees": "frees playlist 'Warmup' (pl-a), so the next pass queues it again",
    }
    kept = {**row, "job_id": "j-new", "same_tracks": ["j-old"], "reason": "kept, the newest", "frees": None}
    return job_state(
        verb="job.cancel",
        job_id="",
        state="dry_run" if dry_run else "cancelled",
        progress={"stale_days": 30, "dry_run": dry_run, "cancel": [row], "kept": [kept], "left": []},
    )


def test_a_stale_cancel_prints_each_job_its_playlist_age_copies_and_what_it_frees():
    lines = render.render_stale_cancel(_stale_payload(dry_run=False))
    assert lines[1] == "  queued intake jobs older than 30 day(s)"
    assert lines[2] == (
        "  cancelled: j-old, playlist 'Warmup' (pl-a), 44 day(s) old, 144 track(s), "
        "same tracks as j-new: a copy of the tracks job j-new holds; j-new is kept; "
        "frees playlist 'Warmup' (pl-a), so the next pass queues it again"
    )
    assert lines[3].startswith("  kept: j-new,")
    assert lines[-1] == "  a cancelled job reopens with: crate job resume JOB_ID"


def test_a_dry_run_says_would_and_names_no_resume():
    lines = render.render_stale_cancel(_stale_payload(dry_run=True))
    assert lines[1].endswith(", a dry run")
    assert lines[2].startswith("  would cancel: j-old,")
    assert lines[3].startswith("  would keep: j-new,")
    assert not any("job resume" in line for line in lines)


def test_a_single_cancel_renders_no_stale_list():
    single = job_state(verb="job.cancel", state="cancelled", progress={"total": 1, "settled": 0})
    assert render.render_stale_cancel(single) == []


def test_a_set_or_hearts_job_with_no_playlist_name_is_listed_by_its_source():
    listed = render.render_job_list(
        job_state(
            verb="job.list",
            job_id="",
            progress={"jobs": [{"job_id": "j-2", "handler": "intake.set", "state": "queued", "playlist": "", "source": "/x.txt"}]},
        )
    )
    assert "  j-2, intake.set, queued, source /x.txt" in listed
    shown = render.render_job_state(job_state(verb="job.show", progress={"playlist": "", "source": "favorites"}))
    assert "  source: favorites" in shown


def test_a_stale_cancel_that_found_no_open_job_says_none_open():
    empty = job_state(
        verb="job.cancel",
        job_id="",
        state="unchanged",
        progress={"stale_days": 30, "dry_run": False, "cancel": [], "kept": [], "left": []},
    )
    assert render.render_stale_cancel(empty) == [
        "",
        "  queued intake jobs older than 30 day(s)",
        "  none open",
    ]

