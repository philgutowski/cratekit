"""R-1991: a genre folder renamed in rekordbox that no write recorded.

The check reads a playlist nothing derives into by its folder's declared name,
or by the bucket a write recorded for the folder. Adoption's writer recorded
nothing, so a renamed folder of a tree only adoption filed declared no bucket
and had none on record, and a cleared second genre's track left alone under it
read as a person's own playlist: ``converge`` said matching. Now adoption's
writer records the node it files into, and a folder still unrecorded (a tree
adopted before that) is named as not compared. Over a disposable database,
every expected name asked of the shipped taxonomy. D1 applies.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

from cratekit.cli import converge as converge_cli
from cratekit.core import convergence, rb_writer, tree_registry
from cratekit.write import convergence_check, metadata_cli, rebuild, routing_pass, trees
from tests import test_rebuild as _rebuild_suite
from tests.test_second_genre import (
    DECLARED,
    HIGH,
    LOW,
    ONE,
    TECH,
    THIRD,
    TWO,
    _by_hand,
    _derived,
    _left,
    _truth,
)

cfg = _rebuild_suite.cfg
library = _rebuild_suite.library
db = _rebuild_suite.db
adopted_root = _rebuild_suite.adopted_root
gates_pass = _rebuild_suite.gates_pass
_platform_seams = _rebuild_suite._platform_seams
_release_process_locks = _rebuild_suite._release_process_locks

RENAMED = _rebuild_suite.RENAMED_FOLDER
TREE_ID = _rebuild_suite.TREE_ID
_check = _rebuild_suite._check


def _track(cfg, *, second: str | None = TECH):
    """Track 1: Deep House by its genre and, through its second genre, Tech House."""
    return _truth(_rebuild_suite._music(cfg, _rebuild_suite.COMPOSED), energy=8, second=second)


def _pair(bucket: str, sub: str) -> tuple[str, str]:
    return routing_pass.destination(DECLARED, bucket, sub)


def _adopt(cfg, db, adopted_root, places, *, record_as=None):
    """Track 1 filed into each ``(bucket, sub)`` of ``places``, as ``adopt apply`` writes it."""
    path = _rebuild_suite._music(cfg, _rebuild_suite.COMPOSED)
    return trees.write_tree_membership(
        cfg,
        db,
        tree_id=TREE_ID,
        registry=_rebuild_suite._registry(str(adopted_root.ID)),
        plan={_pair(*place): [path] for place in places},
        rows=_rebuild_suite._rows(cfg),
        root_exists=lambda _root: True,
        analysis_roots=[Path(cfg.library.root) / "Music"],
        record_as={_pair(*place): place for place in places} if record_as is None else record_as,
    )


def _node(db, adopted_root, bucket: str, sub: str) -> rebuild.TreeNode:
    (found,) = [
        node
        for node in rebuild.read_tree(db, str(adopted_root.ID))
        if (node.folder_display, node.playlist_display) == _pair(bucket, sub)
    ]
    return found


def _rename(db, adopted_root, bucket: str, to: str = RENAMED) -> str:
    """Rename the folder bearing ``bucket``'s name, as rekordbox would; answer its id."""
    folder_id = _node(db, adopted_root, bucket, HIGH).folder_id
    db.get_playlist(ID=folder_id).Name = to
    db.session.commit()
    return folder_id


def _recorded(cfg) -> dict[tuple[str, str], tuple[str, str]]:
    record = convergence.read(cfg).tree(TREE_ID)
    return {} if record is None else {
        (one.bucket, one.sub): (one.folder_id, one.playlist_id) for one in record.nodes
    }


def _under(folder: str, bucket: str = TWO, sub: str = HIGH) -> str:
    """How the report names a playlist under ``folder`` bearing ``(bucket, sub)``'s playlist name."""
    return f"{folder}/{_pair(bucket, sub)[1]}"


# 1. The residual, both ways


def test_a_tree_filed_by_adoption_names_its_leftover_under_a_renamed_folder(
    cfg, gates_pass, db, adopted_root
):
    """Adoption's writer recorded the folder, so a rename leaves it read as Tech House."""
    _adopt(cfg, db, adopted_root, [(ONE, HIGH), (TWO, HIGH)])
    filed = _node(db, adopted_root, TWO, HIGH)
    assert _recorded(cfg)[(TWO, HIGH)] == (filed.folder_id, filed.playlist_id)
    assert _check(cfg, db, adopted_root, DECLARED, _derived(_track(cfg))).converged

    _rename(db, adopted_root, TWO)
    report = _check(cfg, db, adopted_root, DECLARED, _derived(_track(cfg, second=None)))
    assert not report.converged
    assert _left(report) == [("1", TWO, HIGH)]
    assert report.foreign == () and report.unidentified == ()
    (leftover,) = report.unexpected
    assert (leftover.folder, leftover.playlist) == (RENAMED, _pair(TWO, HIGH)[1])
    assert rebuild.left_behind(report, DECLARED) == (leftover,)


def test_a_tree_adopted_before_the_record_names_the_renamed_folder_as_not_compared(
    cfg, gates_pass, db, adopted_root
):
    """THE RESIDUAL: no record, so which genre the folder is cannot be read, and it is said."""
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",), (TWO, HIGH): ("1",)})
    _rename(db, adopted_root, TWO)
    # Before the clear the track is still declared there, so the playlist is
    # missing by its declared name; it is no person's own either way.
    report = _check(cfg, db, adopted_root, DECLARED, _derived(_track(cfg, second=None)))
    assert report.differences == ()
    assert report.foreign == ()
    assert report.unidentified == (_under(RENAMED),)
    # Not a difference: no rebuild can answer it, so the flag's evidence omits it.
    assert report.summaries() == ()


def test_the_converge_verb_never_says_matching_over_an_unrecorded_renamed_folder(
    cfg, db, adopted_root, monkeypatch
):
    """The verb a DJ runs, driven: not compared, naming the folder and how to answer it."""
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",), (TWO, HIGH): ("1",)})
    _rename(db, adopted_root, TWO)
    tree_registry.write(cfg, _rebuild_suite._registry(str(adopted_root.ID)))
    readings = [_track(cfg, second=None)]
    monkeypatch.setattr(rebuild, "library_truth", lambda *_args, **_kwargs: list(readings))

    (check,) = _rebuild_suite._converge()["data"]["checks"]
    assert check["status"] == converge_cli.NOT_COMPARED, check
    assert f"not-compared:{_under(RENAMED)}" in check["detail"]
    assert check["detail"].endswith(converge_cli.UNIDENTIFIED), check
    # The dimension the run left out is still said, as the matching line says it.
    assert "; not compared: vocal;" in check["detail"], check

    # A difference beside it says differing, the folder still named.
    readings[:] = [_track(cfg, second=None), replace(_track(cfg), location=_rebuild_suite._music(
        cfg, _rebuild_suite.PLAIN), energy=1, second_genre=None)]
    (check,) = _rebuild_suite._converge()["data"]["checks"]
    assert check["status"] == converge_cli.DIFFERING, check
    # First, so the cut at twenty never drops it.
    assert check["detail"].startswith(f"not-compared:{_under(RENAMED)}; "), check


def test_the_converge_verb_says_differing_over_a_doubled_row_beside_an_unread_folder(
    monkeypatch,
):
    """A doubled row is damage, whatever else the check could not read."""
    report = convergence_check.ConvergenceReport(
        tree_id=TREE_ID, root_id="root", derived=1,
        doubled=(f"{ONE}/{HIGH}:1",), unidentified=(_under(RENAMED),),
    )
    monkeypatch.setattr(rebuild, "report_convergence", lambda *_args, **_kwargs: report)
    monkeypatch.setattr(metadata_cli, "load_vocal_threshold", lambda _cfg: None)
    status, detail = converge_cli._compare(
        None, SimpleNamespace(get_playlist=list, get_content=list),
        tree_id=TREE_ID, entries=None, declared=DECLARED,
    )
    assert status == converge_cli.DIFFERING
    assert detail == f"not-compared:{_under(RENAMED)}; doubled:{ONE}/{HIGH}:1"


def test_a_rebuild_still_clears_a_restored_flag_over_an_unrecorded_renamed_folder(
    cfg, gates_pass, db, adopted_root
):
    """No rebuild can tie the folder to a genre, so it never holds the flag (round one)."""
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",), (TWO, HIGH): ("1",)})
    _rename(db, adopted_root, TWO)
    convergence.mark_unconverged(cfg, [TREE_ID], reason="a restore")
    report = _rebuild_suite._rebuild(
        cfg, db, adopted_root, DECLARED, [], truth=[_track(cfg, second=None)]
    )
    assert report.cleared
    assert not convergence.read(cfg).tree(TREE_ID).blocking
    assert report.after.unidentified == (_under(RENAMED),)


def test_a_folder_a_rebuild_recorded_is_compared_after_a_rename_as_before(
    cfg, gates_pass, db, adopted_root
):
    """The recorded folder is read by its bucket, so nothing is left unidentified."""
    _rebuild_suite._rebuild(cfg, db, adopted_root, DECLARED, [], truth=[_track(cfg)])
    _rename(db, adopted_root, TWO)
    report = _check(cfg, db, adopted_root, DECLARED, _derived(_track(cfg, second=None)))
    assert _left(report) == [("1", TWO, HIGH)]
    assert report.unidentified == () and report.foreign == ()


# 2. What stays a person's own


def test_a_persons_folder_holding_no_filed_track_stays_foreign(
    cfg, gates_pass, db, adopted_root
):
    """A playlist bearing a band's name holds track 2, which nothing files: no evidence."""
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",)})
    folder = rb_writer.ensure_folder(db, RENAMED, parent=adopted_root)
    rb_writer.add_membership(db, rb_writer.ensure_playlist(db, _pair(TWO, HIGH)[1], folder), "2")
    db.session.commit()
    report = _check(cfg, db, adopted_root, DECLARED, _derived(_track(cfg, second=None)))
    assert report.converged, report.summaries()
    assert report.foreign == (_under(RENAMED),)


def test_a_persons_playlist_whose_name_declares_nothing_stays_foreign_whatever_it_holds(
    cfg, gates_pass, db, adopted_root
):
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",)})
    folder = rb_writer.ensure_folder(db, RENAMED, parent=adopted_root)
    own = rb_writer.ensure_playlist(db, _rebuild_suite.CURATED_PLAYLIST, folder)
    rb_writer.add_membership(db, own, "1")
    db.session.commit()
    report = _check(cfg, db, adopted_root, DECLARED, _derived(_track(cfg, second=None)))
    assert report.converged, report.summaries()
    assert report.foreign == (f"{RENAMED}/{_rebuild_suite.CURATED_PLAYLIST}",)


def test_a_removed_playlist_under_an_unrecorded_folder_is_not_named(
    cfg, gates_pass, db, adopted_root
):
    made = _by_hand(db, adopted_root, {(ONE, HIGH): ("1",), (TWO, HIGH): ("1",)})
    _rename(db, adopted_root, TWO)
    setattr(db.get_playlist(ID=made[(TWO, HIGH)]), rb_writer.SOFT_DELETE_COLUMN, 1)
    db.session.commit()
    report = _check(cfg, db, adopted_root, DECLARED, _derived(_track(cfg, second=None)))
    assert report.converged, report.summaries()
    assert report.unidentified == ()


def test_a_vocal_playlist_the_run_did_not_compare_stays_foreign_under_an_unrecorded_folder(
    cfg, gates_pass, db, adopted_root
):
    """Its only reading is a dimension this run did not judge (U119)."""
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",), (TWO, trees.VOX_SUB_CLASS): ("1",)})
    folder_id = _node(db, adopted_root, TWO, trees.VOX_SUB_CLASS).folder_id
    db.get_playlist(ID=folder_id).Name = RENAMED
    db.session.commit()
    placements = _derived(_track(cfg, second=None))
    unjudged = _check(
        cfg, db, adopted_root, DECLARED, placements, not_compared=(rebuild.VOCAL_DIMENSION,)
    )
    assert unjudged.converged, unjudged.summaries()
    assert unjudged.foreign == (_under(RENAMED, TWO, trees.VOX_SUB_CLASS),)
    judged = _check(cfg, db, adopted_root, DECLARED, placements)
    assert judged.unidentified == (_under(RENAMED, TWO, trees.VOX_SUB_CLASS),)


def test_a_renamed_folder_a_record_names_for_a_dropped_bucket_is_named_as_not_compared(
    cfg, gates_pass, db, adopted_root
):
    """The record names no bucket this taxonomy declares, so it ties the folder to none."""
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",), (TWO, HIGH): ("1",)})
    folder_id = _rename(db, adopted_root, TWO)
    convergence.record_nodes(cfg, TREE_ID, [convergence.DestinationNode(
        bucket="retired_genre", sub=HIGH, folder_id=folder_id, playlist_id="gone-1"
    )])
    report = _check(cfg, db, adopted_root, DECLARED, _derived(_track(cfg, second=None)))
    assert report.unidentified == (_under(RENAMED),)
    assert report.foreign == ()


def test_a_leftover_beside_a_folder_a_write_made_again_is_named_as_not_compared(
    cfg, gates_pass, db, adopted_root
):
    """ROUND ONE: the record ties the renamed folder to Tech House, but its Low is bound elsewhere.

    A write that finds its playlists by name made Tech House / Low again, so
    the leftover's playlist reads as a second node of a bound destination,
    which :func:`namesakes` leaves alone; it is named rather than read clean.
    """
    _by_hand(db, adopted_root, {(ONE, LOW): ("1",), (TWO, LOW): ("1",)})
    _adopt(cfg, db, adopted_root, [(TWO, HIGH)])
    _rename(db, adopted_root, TWO)
    _by_hand(db, adopted_root, {(TWO, LOW): ("2",)})
    one = _truth(_rebuild_suite._music(cfg, _rebuild_suite.COMPOSED), energy=1, second=None)
    two = replace(one, location=_rebuild_suite._music(cfg, _rebuild_suite.PLAIN), genre=TECH)
    (held,) = [
        node
        for node in rebuild.read_tree(db, str(adopted_root.ID))
        if f"{node.folder_display}/{node.playlist_display}" == _under(RENAMED)
    ]
    rb_writer.remove_memberships(db, db.get_playlist(ID=held.playlist_id), ["1"])
    db.session.commit()

    report = _check(cfg, db, adopted_root, DECLARED, _derived(one, two))
    assert report.differences == (), report.summaries()
    assert report.unidentified == (_under(RENAMED, TWO, LOW),)


def test_a_playlist_under_a_genre_named_folder_is_never_unidentified(
    cfg, gates_pass, db, adopted_root
):
    """A folder bearing a bucket's name is read by it; a playlist it does not compare stays foreign."""
    _by_hand(db, adopted_root, {(ONE, HIGH): ("1",)})
    folder = rb_writer.ensure_folder(db, DECLARED.bucket(TWO).display, parent=adopted_root)
    own = rb_writer.ensure_playlist(db, _pair(THIRD, "candy")[1], folder)
    rb_writer.add_membership(db, own, "1")
    db.session.commit()
    report = _check(cfg, db, adopted_root, DECLARED, _derived(_track(cfg, second=None)))
    assert report.unidentified == ()


# 3. What adoption's writer records


def test_the_writer_records_nothing_unless_asked(cfg, gates_pass, db, adopted_root):
    """The rebuild's and the routing pass's calls keep their own recording."""
    _adopt(cfg, db, adopted_root, [(TWO, HIGH)], record_as={})
    assert _recorded(cfg) == {}


def test_the_writer_never_moves_a_destination_the_record_already_binds(
    cfg, gates_pass, db, adopted_root
):
    bound = convergence.DestinationNode(
        bucket=TWO, sub=HIGH, folder_id="kept-folder", playlist_id="kept-playlist"
    )
    convergence.record_nodes(cfg, TREE_ID, [bound])
    _adopt(cfg, db, adopted_root, [(ONE, HIGH), (TWO, HIGH)])
    filed = _node(db, adopted_root, ONE, HIGH)
    assert _recorded(cfg) == {
        (TWO, HIGH): ("kept-folder", "kept-playlist"),
        (ONE, HIGH): (filed.folder_id, filed.playlist_id),
    }


def test_the_writer_gives_no_node_a_second_destination(cfg, gates_pass, db, adopted_root):
    """The record stays one to one, so nothing raises after the write has landed."""
    made = _by_hand(db, adopted_root, {(TWO, HIGH): ("2",)})
    held = _node(db, adopted_root, TWO, HIGH)
    assert made[(TWO, HIGH)] == held.playlist_id
    convergence.record_nodes(cfg, TREE_ID, [convergence.DestinationNode(
        bucket=THIRD, sub=HIGH, folder_id=held.folder_id, playlist_id=held.playlist_id
    )])
    _adopt(cfg, db, adopted_root, [(TWO, HIGH)])
    assert _recorded(cfg) == {(THIRD, HIGH): (held.folder_id, held.playlist_id)}


def test_the_writer_records_no_node_rekordbox_removed(cfg, gates_pass, db, adopted_root):
    """The writer may file into a removed row it found by name; that row is nobody's destination."""
    made = _by_hand(db, adopted_root, {(TWO, HIGH): ("2",)})
    setattr(db.get_playlist(ID=made[(TWO, HIGH)]), rb_writer.SOFT_DELETE_COLUMN, 1)
    db.session.commit()
    _adopt(cfg, db, adopted_root, [(TWO, HIGH)])
    assert _recorded(cfg) == {}


def test_the_writer_never_chooses_between_two_live_nodes_at_one_pair(
    cfg, gates_pass, db, adopted_root
):
    folder_name, playlist_name = _pair(TWO, HIGH)
    for _ in range(2):
        folder = db.create_playlist_folder(folder_name, parent=adopted_root)
        db.create_playlist(playlist_name, parent=folder)
    db.session.commit()
    _adopt(cfg, db, adopted_root, [(TWO, HIGH)])
    assert _recorded(cfg) == {}


def test_the_writer_records_only_a_pair_it_filed_into(cfg, gates_pass, db, adopted_root):
    """A pair whose rows matched nothing made no node, and a standing one it did not fill is not recorded."""
    _by_hand(db, adopted_root, {(TWO, LOW): ("2",)})
    _adopt(
        cfg, db, adopted_root, [(ONE, HIGH)],
        record_as={_pair(ONE, HIGH): (ONE, HIGH), _pair(TWO, LOW): (TWO, LOW)},
    )
    filed = _node(db, adopted_root, ONE, HIGH)
    assert _recorded(cfg) == {(ONE, HIGH): (filed.folder_id, filed.playlist_id)}
