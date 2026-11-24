"""Favorites refresh's scenarios: each genre folder's Favorites mirrored behind the gate (U308).

A true mirror writes nothing, and a tree on the bridge is refused before the gate.
"""

from __future__ import annotations

from cratekit.core import tree_registry
from cratekit.core.exit_codes import ExitCode
from tests.test_genre_favorites import AFRO, APPROVE, DEEP, FAVORITES, VERB, Tree, _closed
from tests.test_genre_favorites import db as db  # noqa: PLC0414
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414

OK = int(ExitCode.OK)


def test_genre_favorites_refreshed_behind_the_gate(stage, cfg, gates_pass, db):
    tree = Tree(cfg, db)
    tree.playlist(DEEP, "Med", "1", "2")
    tree.playlist(DEEP, FAVORITES.display, "2")
    tree.playlist(AFRO, "High", "3", "4")
    tree.source("1", "3", "5")
    _closed(db)

    assert stage.crate(*VERB).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*VERB)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, APPROVE, "approve").code == OK
    refreshed = stage.crate("--run", run_id, *VERB)
    assert refreshed.code == OK, refreshed.stderr
    # Run again: the mirror is true, so the gate's approval writes nothing.
    again = stage.json(*VERB)
    assert again.code == int(ExitCode.DECISION_REQUIRED), again.stdout
    assert stage.decide(again.envelope["run_id"], APPROVE, "approve").code == OK
    assert stage.crate("--run", again.envelope["run_id"], *VERB).code == OK

    # A tree on the bridge is refused before the gate.
    tree_registry.write(cfg, tree_registry.Registry())
    assert stage.crate(*VERB).code != int(ExitCode.DECISION_REQUIRED)
