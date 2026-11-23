"""R-1950: the guards on U340's second genre paths that no test killed.

A track with a second genre has two plan entries, so a per track count reads
``AdoptionPlan.firsts()`` and never ``entries``; the second bucket files by the
second genre's own word; and a gate's column names both places a track is
filed into. Each test here fails when its one guard is undone. Expected values
are literals or the shipped taxonomy's own words, never asked of the code
under test. Fixtures and stubs only: no real library, no rekordbox.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from cratekit.adopt import apply as apply_engine
from cratekit.adopt import apply_cli
from cratekit.adopt import plan as plan_engine
from cratekit.adopt.scan import Disposition
from cratekit.core import tree_registry
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import filing, native
from cratekit.organize import rekordbox
from cratekit.write import metadata_cli, rebuild, routing_cli, routing_export
from tests.cli_drive import drive
from tests.test_adopt_workers import APPLY, GATE, _record_decision
from tests.test_adopt_workers import _platform_seams as _platform_seams
from tests.test_adopt_workers import _reader_cache as _reader_cache
from tests.test_adopt_workers import _release_process_locks as _release_process_locks
from tests.test_adopt_workers import library as library
from tests.test_adopt_workers import machine as machine
from tests.test_second_genre import DECLARED, DEEP, MED, ONE, TECH, TWO, _plan, _two

#: The shipped words this suite files by, spelled as the taxonomy ships them.
ROMINIMAL = "Rominimal"


def _two_genre_plan(held: dict) -> plan_engine.AdoptionPlan:
    """One Deep House track at energy 8 whose file names Tech House beside it."""
    plan = _plan([_two("t", energy=8)], held)
    assert len(plan.entries) == 2, "the two genre track has an entry per folder"
    return plan


# C01: the nothing applicable warning counts tracks, not placements


def test_nothing_applicable_says_the_per_track_count_of_a_two_genre_plan(machine, monkeypatch):
    """Held in a competing band of both folders, the one track is withheld twice."""
    plan = _two_genre_plan({ONE: {"t": (MED,)}, TWO: {"t": (MED,)}})
    assert plan.applicable() == ()
    monkeypatch.setattr(apply_cli, "current_plan", lambda *_args, **_kwargs: plan)

    run_id = _record_decision(APPLY, GATE)
    code, envelope = drive(["--run", run_id, *APPLY])
    assert code == int(ExitCode.OK), envelope
    assert [warning["message"] for warning in envelope["warnings"]] == [
        "this plan holds 1 track(s) and none of them can be placed, so there is nothing to queue"
    ]


# C02: a landed track is compared against its first genre's entry


def test_a_landed_two_genre_track_files_as_its_first_folder_predicts(monkeypatch):
    plan = _two_genre_plan({})
    monkeypatch.setattr(apply_cli, "current_plan", lambda *_args, **_kwargs: plan)
    written: list[tuple[str, ...]] = []

    def file_plan(_cfg, filed, _declared, *, actor, refuse_unplaced):
        ids = tuple(entry.entry_id for entry in filed.applicable())
        written.append(ids)
        report = SimpleNamespace(failed=(), applied=ids, already_applied=())
        return SimpleNamespace(added=len(ids)), report, (), None

    monkeypatch.setattr(apply_cli, "file_plan", file_plan)
    target = Path("/nowhere/One.flac")
    landed = native.NativeLanded(
        tree_id="t", playlist="p", playlist_id="", present=(), memberships_added=0,
        session_id="s",
        added=(native.AddedRow(target=target, content_id="t", title="t", folder_path="f", empty={}),),
    )
    predicted = (
        filing.Prediction(
            target=target, place=plan_engine.Predicted(Disposition.ROUTE, "deep_house", "high")
        ),
    )
    found = filing.file_landed(None, DECLARED, predicted, landed, actor="session")
    assert (found.state, found.differing) == ("filed", ())
    assert (found.filed, found.memberships) == (2, 2)
    assert len(written) == 1 and len(written[0]) == 2


# C03: the adopt step's tracks read counts tracks


def test_the_adopt_steps_tracks_read_is_the_number_of_tracks(monkeypatch):
    """Both placements already filed by an apply, so the step plans nothing."""
    plan = _two_genre_plan({})
    done = frozenset(entry.entry_id for entry in plan.entries)
    monkeypatch.setattr(apply_cli, "current_plan", lambda *_args, **_kwargs: plan)
    monkeypatch.setattr(apply_engine, "read", lambda _cfg: SimpleNamespace(entry_ids=lambda: done))

    step = rekordbox._adoption(None, DECLARED, None, None, "gate", None)
    assert step.counts == {
        "tracks read": 1, "placeable": 2, "to file": 0, "vocal memberships to add": 0,
    }


# C04: the second bucket files by the second genre's own word


def test_the_second_bucket_files_by_the_second_genres_own_word():
    """The shipped Minimal / Deep Tech bucket declares a genre sub fed by the
    word Rominimal alone, so only the second genre's word reaches it."""
    truth = rebuild.Truth(location="/m/t.flac", genre=DEEP, energy=8, second_genre=ROMINIMAL)
    assert rebuild.filed_genres(DECLARED, truth) == (
        ("deep_house", DEEP),
        ("minimal_deep_tech", ROMINIMAL),
    )
    placements, _gaps = rebuild.derive_from_taxonomy(DECLARED, [truth], vocal_threshold=None)
    assert {(one.bucket, one.sub) for one in placements} == {
        ("deep_house", "high"),
        ("minimal_deep_tech", "high"),
        ("minimal_deep_tech", "rominimal"),
    }


# C05 and C06: a gate's column names both places


def _read_as_two_genres(monkeypatch) -> None:
    def read_truth(path: Path) -> rebuild.Truth:
        return rebuild.Truth(location=str(path), genre=DEEP, energy=8, second_genre=TECH)

    monkeypatch.setattr(rebuild, "read_truth", read_truth)


def test_the_export_decision_names_both_folders_of_a_two_genre_track(monkeypatch):
    _read_as_two_genres(monkeypatch)
    monkeypatch.setattr(routing_export, "_readable_file", lambda location, _cfg: Path(location))
    warnings: list[dict[str, str]] = []
    decision = routing_export._decide(
        None, DECLARED, [("11", {"Location": "/m/two.flac"})], None, warnings
    )
    assert decision.destined == {"11": "Deep House/High; Tech House/High"}
    assert warnings == []


def test_the_inbox_plan_names_both_folders_of_a_two_genre_track(tmp_path, monkeypatch):
    _read_as_two_genres(monkeypatch)
    inbox = tmp_path / "INBOX"
    inbox.mkdir()
    (inbox / "two.flac").write_bytes(b"")
    entries = SimpleNamespace(derivation_source=lambda _tree: tree_registry.DerivationSource.TAXONOMY)
    monkeypatch.setattr(tree_registry, "read", lambda _cfg: entries)
    monkeypatch.setattr(routing_cli, "_routed_trees", lambda _entries, declared: (declared.tree.id,))
    monkeypatch.setattr(metadata_cli, "load_vocal_threshold", lambda _cfg: None)
    cfg = SimpleNamespace(library=SimpleNamespace(root=str(tmp_path), music_dir="Music"))

    planned = routing_cli.plan_inbox(cfg, DECLARED)
    assert [(item["name"], item["destination"]) for item in planned.items] == [
        ("two.flac", "Deep House/High; Tech House/High")
    ]
