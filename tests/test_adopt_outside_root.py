"""U956: adoption leaves out a row whose file is outside the library root.

Attended sitting 104 rehearsed ``adopt apply`` on a copy of a real library and
the pass failed ``adopt-entries-failed`` on rekordbox's own sampler presets.
Their rows are recorded under two home folders and prefix rules map them onto
the one Sampler folder on this machine, outside the library root, where the
membership write could not place them: one row alone fails it, since its
resolved path does not resolve back through the rule, and two make it
ambiguous besides (review round one). The census now reads such a row
``outside-root``, excluded, and the gate names it.

Expected values are literals or the fixture's own paths, never asked of the
code under test. D1 applies: nothing names a real volume, person or track.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.adopt import apply as adopt_apply
from cratekit.adopt import apply_cli, collection
from cratekit.adopt import plan as adopt_plan
from cratekit.adopt import scan as adopt_scan
from cratekit.adopt.scan import Disposition, Readability
from cratekit.core import config, locations, preflight, session
from cratekit.core.exit_codes import ExitCode
from cratekit.tagging import rows as tagging_rows
from tests import adopt_fixtures
from tests.cli_drive import approve_and_queue, drive, drive_human
from tests.test_adopt_workers import (
    APPLY,
    DECLARED,
    GATE,
    _configured,
    _memberships,
    _record_cutover,
    _resume,
    _scan_job,
)
from tests.test_adopt_workers import _platform_seams as _platform_seams
from tests.test_adopt_workers import _reader_cache as _reader_cache
from tests.test_adopt_workers import _release_process_locks as _release_process_locks
from tests.test_adopt_workers import library as library
from tests.test_adoption import _bucket_and_genre, _readable

#: The preset every sampler row records, one file on this machine.
PRESET = "Kick 01.wav"

#: The two old home folders the sampler rows are recorded under, both mapped here.
HOMES = ("/old-machine-one/rekordbox/Sampler", "/old-machine-two/rekordbox/Sampler")


def _genre() -> str:
    return _bucket_and_genre(DECLARED)[1]


def _row(content_id: str, recorded: Path | str) -> adopt_scan.CollectionRow:
    return adopt_scan.CollectionRow(
        content_id=content_id, recorded=str(recorded), genre=_genre(), deleted=False
    )


def _scan(rows, root: Path, rules=(), **kwargs) -> dict[str, adopt_scan.ScannedTrack]:
    scanned = adopt_scan.scan_rows(
        rows, DECLARED, root=root, prefix_map=rules, probe=_readable, **kwargs
    )
    return {track.content_id: track for track in scanned}


# ── The containment test the census asks ──


@pytest.mark.parametrize(
    ("path", "root", "inside"),
    [
        ("/vol/lib", "/vol/lib", True),
        ("/vol/lib/Music/a.flac", "/vol/lib", True),
        ("/vol/lib/Music/a.flac", "/vol/lib/", True),
        ("/vol/library/a.flac", "/vol/lib", False),
        ("/vol/libArchive/a.flac", "/vol/lib", False),
        ("/vol/lib/../srv/Sampler/a.wav", "/vol/lib", False),
        ("/vol/lib/Music/../Other/a.flac", "/vol/lib", True),
        ("/srv/Sampler/a.wav", "/vol/lib", False),
        ("/vol/a.flac", "/vol/lib", False),
        ("/anything/at/all.flac", "/", True),
        ("/vol/lib/Cafe\u0301/a.flac", "/vol/lib/Caf\u00e9", True),
        ("/vol/lib/Caf\u00e9/a.flac", "/vol/lib/Cafe\u0301", True),
    ],
)
def test_within_root_is_anchored_on_whole_components_and_reads_no_dots(path, root, inside):
    assert adopt_scan.within_root(path, root) is inside


def test_within_root_reaches_the_root_through_a_name_that_is_the_same_directory(tmp_path):
    """A volume that folds case spells the root two ways; a link stands in for it here."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    alias = tmp_path / "LIBRARY-alias"
    alias.symlink_to(root, target_is_directory=True)
    assert adopt_scan.within_root(str(alias / "Music" / "a.flac"), str(root)) is True
    # A directory below the alias that is gone is asked nothing and is no answer.
    assert adopt_scan.within_root(str(alias / "Gone" / "a.flac"), str(root)) is True
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    assert adopt_scan.within_root(str(elsewhere / "a.flac"), str(root)) is False


# ── The census ──


def test_a_row_mapped_outside_the_root_is_excluded_and_keeps_its_path(tmp_path):
    root = tmp_path / "library"
    old_volume = "/old-drive/Music"
    old_home = "/old-machine/rekordbox/Sampler"
    here = tmp_path / "home" / "Sampler"
    rules = (
        locations.PrefixRule(old_volume, str(root / "Music")),
        locations.PrefixRule(old_home, str(here)),
        locations.PrefixRule("/twin-drive", f"{root}Archive"),
    )
    found = _scan(
        [
            _row("inside", root / "Music" / "a.flac"),
            _row("remapped-in", f"{old_volume}/b.flac"),
            _row("sampler", f"{old_home}/{PRESET}"),
            _row("sibling", "/twin-drive/c.flac"),
        ],
        root,
        rules,
    )

    assert found["inside"].disposition is Disposition.ROUTE
    assert found["remapped-in"].disposition is Disposition.ROUTE
    for content_id, path in (
        ("sampler", str(here / PRESET)),
        ("sibling", f"{root}Archive/c.flac"),
    ):
        track = found[content_id]
        assert track.readability is Readability.OUTSIDE_ROOT, content_id
        assert track.disposition is Disposition.EXCLUDED, content_id
        assert track.path == path, content_id
        assert track.bucket == "", content_id
    assert str(Readability.OUTSIDE_ROOT) == "outside-root"


def test_an_outside_row_is_never_probed(tmp_path):
    """Opening a file the plan will not touch could fetch an online only one."""
    asked: list[Path] = []

    def probe(path: Path) -> Readability:
        asked.append(path)
        return Readability.READABLE

    root = tmp_path / "library"
    rules = (locations.PrefixRule("/old-machine/Sampler", str(tmp_path / "Sampler")),)
    list(
        adopt_scan.scan_rows(
            [_row("s", f"/old-machine/Sampler/{PRESET}")],
            DECLARED,
            root=root,
            prefix_map=rules,
            probe=probe,
        )
    )
    assert asked == []


def test_the_tagging_walk_still_reads_a_row_outside_the_root(tmp_path, monkeypatch):
    """Out of scope: the tag verbs read the sampler rows as they did."""
    root = tmp_path / "library"
    here = tmp_path / "Sampler"
    found = _scan(
        [_row("s", f"/old-machine/Sampler/{PRESET}")],
        root,
        (locations.PrefixRule("/old-machine/Sampler", str(here)),),
        confine_to_root=False,
    )
    assert found["s"].readability is Readability.READABLE
    assert found["s"].disposition is Disposition.ROUTE

    seen: dict[str, object] = {}
    real = adopt_scan.scan_rows

    def spy(*args, **kwargs):
        seen.update(kwargs)
        return real(*args, **kwargs)

    monkeypatch.setattr(adopt_scan, "scan_rows", spy)
    cfg = config.from_dict(_data(root))
    list(tagging_rows.scanned(cfg, {}, DECLARED, _readable))
    assert seen.get("confine_to_root") is False


def _data(root: Path) -> dict:
    from tests.test_config import valid_data

    root.mkdir(parents=True, exist_ok=True)
    return valid_data(root)


# ── The plan and its gate ──


def _outside_plan(tmp_path: Path, ids: tuple[str, ...]) -> adopt_plan.AdoptionPlan:
    root = tmp_path / "library"
    rules = (locations.PrefixRule("/old-machine/Sampler", str(tmp_path / "Sampler")),)
    rows = [_row("inside", root / "Music" / "a.flac"), _row("unmapped", "/no-rule/a.flac")]
    rows += [_row(content_id, f"/old-machine/Sampler/{content_id}.wav") for content_id in ids]
    scanned = list(
        adopt_scan.scan_rows(rows, DECLARED, root=root, prefix_map=rules, probe=_readable)
    )
    return adopt_plan.build_adoption_plan(scanned, DECLARED, tree=DECLARED.tree.id)


def test_the_plan_counts_and_names_every_row_it_leaves_outside(tmp_path):
    plan = _outside_plan(tmp_path, ("s-1", "s-2"))
    document = adopt_plan.to_json(plan)

    assert [entry.content_id for entry in plan.applicable()] == ["inside"]
    assert plan.counts()["outside-root"] == 2
    assert plan.counts()["excluded"] == 3
    assert plan.counts()["unmapped"] == 1
    assert document["outside_root"] == [
        {
            "content_id": "s-1",
            "location": "/old-machine/Sampler/s-1.wav",
            "path": str(tmp_path / "Sampler" / "s-1.wav"),
        },
        {
            "content_id": "s-2",
            "location": "/old-machine/Sampler/s-2.wav",
            "path": str(tmp_path / "Sampler" / "s-2.wav"),
        },
    ]


def test_the_digest_moves_when_a_different_row_is_left_outside(tmp_path):
    """The same count over other rows is another screen, so another digest."""
    one = _outside_plan(tmp_path, ("s-1",))
    other = _outside_plan(tmp_path, ("s-9",))
    assert one.counts() == other.counts()
    assert one.digest() != other.digest()


# ── The real shape, end to end through the worker ──


@pytest.fixture
def sampled(library, tmp_path, monkeypatch):
    """A cut over library holding two readable rows inside the root and one
    sampler preset recorded under two old home folders, both mapped onto one
    file outside the root, as the sitting found."""
    here = tmp_path / "home" / "Sampler"
    adopt_fixtures.write_audio(here / PRESET)
    resolved = _configured(
        library,
        location_prefix_map=[{"from": home, "to": str(here)} for home in HOMES],
    )
    config.save(resolved)
    config.reset_cache()
    genre = _genre()
    adopt_fixtures.build(
        resolved,
        (
            adopt_fixtures.Track("r-one", "one.flac", genre),
            adopt_fixtures.Track("r-two", "two.flac", genre),
            adopt_fixtures.Track("s-one", PRESET, genre, recorded_at=Path(HOMES[0])),
            adopt_fixtures.Track("s-two", PRESET, genre, recorded_at=Path(HOMES[1])),
        ),
    )
    collection.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: lambda _path: resolved.library.volume_id
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    session.record_acknowledgment(resolved, terminal=lambda: True)
    _cut_over(resolved)
    return resolved


def _cut_over(cfg: config.Config) -> None:
    from cratekit.core import rb_writer

    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        root = rb_writer.ensure_folder(handle, DECLARED.tree.display)
        handle.session.commit()
        root_id = str(root.ID)
    finally:
        rb_writer.close_db(handle)
    _record_cutover(cfg, root_id)


def test_an_apply_over_sampler_rows_files_the_rest_and_records_no_sampler_row(sampled):
    """The sitting's failure, driven: the pass finishes, the rows inside the root
    are filed, and neither sampler row reaches a playlist or the ledger."""
    _run_id, job_id = approve_and_queue(APPLY, GATE)
    code, resumed = drive(_resume(job_id))
    assert code == int(ExitCode.OK), resumed

    members = {member for rows in _memberships(sampled).values() for member in rows}
    assert {"r-one", "r-two"} <= members
    assert not members & {"s-one", "s-two"}
    applied = adopt_apply.read(sampled).entry_ids()
    plan = apply_cli.current_plan(sampled, DECLARED)
    by_content = {entry.content_id: entry.entry_id for entry in plan.entries}
    assert {by_content["r-one"], by_content["r-two"]} <= applied
    assert not applied & {by_content["s-one"], by_content["s-two"]}


def test_the_gate_names_each_sampler_row_it_leaves_out(sampled, tmp_path):
    """Named on the structured screen and the printed one, beside its count."""
    code, refused = drive(APPLY)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    shown = refused["cause"]["detail"]["shown"]
    here = str(tmp_path / "home" / "Sampler" / PRESET)
    assert shown["outside_root"] == [
        {
            "content_id": "s-one",
            "location": locations.location_url(Path(HOMES[0]) / PRESET),
            "path": here,
        },
        {
            "content_id": "s-two",
            "location": locations.location_url(Path(HOMES[1]) / PRESET),
            "path": here,
        },
    ]
    assert shown["counts"]["outside-root"] == 2
    assert {item["content_id"] for item in shown["items"]} == {"r-one", "r-two"}

    _code, text = drive_human(APPLY)
    assert "outside_root:" in text
    for content_id in ("s-one", "s-two"):
        assert f"content_id={content_id}" in text, content_id


def test_a_row_inside_the_root_that_cannot_be_placed_still_fails_the_pass(sampled):
    """All or nothing for the rows it routes: two live rows for one file inside
    the root refuse the pass, and nothing is recorded as adopted."""
    from tests.test_adopt_workers import _sql

    location = adopt_fixtures.recorded_location(Path(sampled.library.root), "one.flac")
    _sql(
        sampled,
        "INSERT INTO djmdContent (ID, FolderPath, GenreID, rb_local_deleted, created_at, "
        "updated_at) SELECT 'r-twin', ?, GenreID, 0, created_at, updated_at "
        "FROM djmdContent WHERE ID = 'r-one'",
        (location,),
    )
    _run_id, job_id = approve_and_queue(APPLY, GATE)
    code, resumed = drive(_resume(job_id))

    assert code != int(ExitCode.OK)
    assert resumed["cause"]["inner"]["reason"] == "adopt-entries-failed", resumed
    assert adopt_apply.read(sampled).entry_ids() == frozenset()


def test_adopt_move_reads_the_same_disposition(sampled, monkeypatch):
    """The move verb plans over adoption's own plan, so it reads the sampler rows
    excluded, outside the root, as the apply does."""
    from cratekit.adopt import move as adopt_move
    from cratekit.adopt import move_cli

    seen: list[adopt_plan.AdoptionPlan] = []
    real = adopt_move.build_move_plan

    def spy(plan, *args, **kwargs):
        seen.append(plan)
        return real(plan, *args, **kwargs)

    monkeypatch.setattr(adopt_move, "build_move_plan", spy)
    move_cli.current_plan(sampled, DECLARED)

    (plan,) = seen
    entries = {entry.content_id: entry for entry in plan.entries}
    for content_id in ("s-one", "s-two"):
        assert entries[content_id].disposition is Disposition.EXCLUDED, content_id
        assert entries[content_id].category is Readability.OUTSIDE_ROOT, content_id
    assert entries["r-one"].disposition is Disposition.ROUTE


def test_adopt_scan_counts_each_sampler_row_outside_the_root(sampled):
    """The census verb's own call reads the rows as the apply does (review R3)."""
    from cratekit.adopt import artifacts

    code, queued = drive(["adopt", "scan"])
    assert code == int(ExitCode.OK), queued
    job = _scan_job()
    code, resumed = drive(["adopt", "scan", "--job", job.job_id])
    assert code == int(ExitCode.OK), resumed

    census = resumed["data"]["progress"]["census"]
    assert census["categories"]["outside-root"] == 2
    assert census["categories"]["readable"] == 2
    reports = {report["content_id"]: report for report in artifacts.committed(sampled, job.job_id)}
    for content_id in ("s-one", "s-two"):
        assert reports[content_id]["readability"] == "outside-root", content_id
        assert reports[content_id]["disposition"] == "excluded", content_id


# ── tag set's closing message (review D2) ──


def _set_item(content_id: str, path: Path):
    from cratekit.tagging import genre_set as gs

    return gs.Item(content_id, str(path), content_id, "House", "House", "write", leaves="house")


def _said(tmp_path: Path, items, took) -> list[str]:
    from types import SimpleNamespace

    from cratekit.tagging import genre_set_cli

    plan = SimpleNamespace(genre="Deep House", writes=tuple(items))
    written = SimpleNamespace(
        files=SimpleNamespace(read_back=tuple(took)),
        written=len(took),
        read_back=len(took),
        session_id="s",
    )
    return [one["message"] for one in genre_set_cli._written(plan, written, tmp_path / "library")]


def test_tag_set_promises_adoption_only_for_rows_inside_the_root(tmp_path):
    """A written row outside the root is named as one neither verb files, and is
    not counted among the rows `adopt move` takes out of a genre folder."""
    inside = _set_item("r-in", tmp_path / "library" / "Music" / "a.flac")
    outside = _set_item("s-out", tmp_path / "Sampler" / PRESET)

    said = _said(tmp_path, (inside, outside), ("r-in", "s-out"))

    assert len(said) == 3, said
    assert said[1].startswith("to file the rows under 'Deep House', run `crate adopt apply`")
    assert "takes the 1 row(s) the tree filed" in said[1]
    assert said[2] == (
        "1 written row(s) have their file outside the library root, which adoption "
        "leaves alone, so neither verb files or moves them: s-out"
    )


def test_tag_set_promises_no_adoption_when_every_written_row_is_outside(tmp_path):
    """Review round two: with only outside rows written, no adoption verb is named."""
    outside = _set_item("s-out", tmp_path / "Sampler" / PRESET)

    said = _said(tmp_path, (outside,), ("s-out",))

    assert len(said) == 2, said
    assert "adopt apply" not in said[1]
    assert said[1].endswith("neither verb files or moves them: s-out")


def test_tag_set_names_only_rows_whose_file_took_the_genre(tmp_path):
    """Review round two: a planned row whose file did not take is not called written."""
    one = _set_item("s-one", tmp_path / "Sampler" / PRESET)
    two = _set_item("s-two", tmp_path / "Sampler" / PRESET)

    said = _said(tmp_path, (one, two), ("s-one",))

    assert said[-1] == (
        "1 written row(s) have their file outside the library root, which adoption "
        "leaves alone, so neither verb files or moves them: s-one"
    )
