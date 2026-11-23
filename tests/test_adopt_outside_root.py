"""U956: adoption leaves out a row whose file is outside the library root.

Attended sitting 104 rehearsed ``adopt apply`` on a copy of a real library and
the pass failed ``adopt-entries-failed`` on rekordbox's own sampler presets.
Their rows are recorded under two home folders, both prefix rules map them onto
the one Sampler folder on this machine, so each file has two live rows and the
membership write could place neither. The file is outside the library root, so
the census now reads it ``outside-root``, excluded, and the gate names it.

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
)
from tests.test_adopt_workers import _platform_seams as _platform_seams
from tests.test_adopt_workers import _reader_cache as _reader_cache
from tests.test_adopt_workers import _release_process_locks as _release_process_locks
from tests.test_adopt_workers import library as library
from tests.test_adoption import _bucket_and_genre, _readable

#: The preset every sampler row records, one file on this machine.
PRESET = "Kick 01.wav"

#: The two old home folders the sampler rows are recorded under, both mapped here.
HOMES = ("/Users/old-one/Music/rekordbox/Sampler", "/Users/old-two/Music/rekordbox/Sampler")


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
        ("/vol/lib/../home/Sampler/a.wav", "/vol/lib", False),
        ("/vol/lib/Music/../Other/a.flac", "/vol/lib", True),
        ("/home/Sampler/a.wav", "/vol/lib", False),
        ("/vol/a.flac", "/vol/lib", False),
        ("/anything/at/all.flac", "/", True),
        ("/vol/lib/Café/a.flac", "/vol/lib/Café", True),
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
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    assert adopt_scan.within_root(str(elsewhere / "a.flac"), str(root)) is False


# ── The census ──


def test_a_row_mapped_outside_the_root_is_excluded_and_keeps_its_path(tmp_path):
    root = tmp_path / "library"
    old_volume = "/Volumes/Old Drive/Music"
    old_home = "/Users/someone-else/Music/rekordbox/Sampler"
    here = tmp_path / "home" / "Sampler"
    rules = (
        locations.PrefixRule(old_volume, str(root / "Music")),
        locations.PrefixRule(old_home, str(here)),
        locations.PrefixRule("/Volumes/Twin", f"{root}Archive"),
    )
    found = _scan(
        [
            _row("inside", root / "Music" / "a.flac"),
            _row("remapped-in", f"{old_volume}/b.flac"),
            _row("sampler", f"{old_home}/{PRESET}"),
            _row("sibling", "/Volumes/Twin/c.flac"),
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
    rules = (locations.PrefixRule("/Users/x/Sampler", str(tmp_path / "Sampler")),)
    list(
        adopt_scan.scan_rows(
            [_row("s", f"/Users/x/Sampler/{PRESET}")],
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
        [_row("s", f"/Users/x/Sampler/{PRESET}")],
        root,
        (locations.PrefixRule("/Users/x/Sampler", str(here)),),
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
    rules = (locations.PrefixRule("/Users/x/Sampler", str(tmp_path / "Sampler")),)
    rows = [_row("inside", root / "Music" / "a.flac")]
    rows += [_row(content_id, f"/Users/x/Sampler/{content_id}.wav") for content_id in ids]
    scanned = list(
        adopt_scan.scan_rows(rows, DECLARED, root=root, prefix_map=rules, probe=_readable)
    )
    return adopt_plan.build_adoption_plan(scanned, DECLARED, tree=DECLARED.tree.id)


def test_the_plan_counts_and_names_every_row_it_leaves_outside(tmp_path):
    plan = _outside_plan(tmp_path, ("s-1", "s-2"))
    document = adopt_plan.to_json(plan)

    assert [entry.content_id for entry in plan.applicable()] == ["inside"]
    assert plan.counts()["outside-root"] == 2
    assert plan.counts()["excluded"] == 2
    assert document["outside_root"] == [
        {
            "content_id": "s-1",
            "location": "/Users/x/Sampler/s-1.wav",
            "path": str(tmp_path / "Sampler" / "s-1.wav"),
        },
        {
            "content_id": "s-2",
            "location": "/Users/x/Sampler/s-2.wav",
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
