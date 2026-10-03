"""U113: the rotation ages an account playlist by its landing record, never by its name.

An account playlist lands as ``Sunset Warmup``, a name with no date in it. The
native landing names it on its record by identifier, which the landing suite
drives end to end in ``tests/test_intake_land_account_playlists_native.py``.
An intake file's playlist has no identifier until rekordbox imports it, so its
record names it and the batch folder it landed in, and these are the rules for
that name: the batch folder must still be there, an abandoned landing names
nothing, and the latest landing of a name is the one INBOX shows.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

from cratekit.core import config, session
from cratekit.intake import ingest, native, rotate
from tests.test_inbox_rotate import TODAY, _node, _plan
from tests.test_inbox_rotate import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_inbox_rotate import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_inbox_rotate import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_inbox_rotate import machine as machine  # noqa: PLC0414
from tests.test_inbox_rotate import native_library as native_library  # noqa: PLC0414

BATCH = "2026-08-24 Tidal playlists"


def _intake_record(
    cfg: config.Config,
    landed: date,
    entries: list[dict],
    *,
    state: session.SessionState = session.SessionState.AWAITING_IMPORT,
    tag: str = "landing",
) -> None:
    """An intake file's session record, as ``place_files`` leaves it, naming account playlists."""
    started = datetime.combine(landed, datetime.min.time().replace(hour=12)).astimezone()
    session.write_record(
        session.SessionRecord(
            session_id=f"{started.strftime('%Y%m%dT%H%M%S')}-{tag}",
            workflow=native.WORKFLOW,
            started=started.isoformat(),
            state=state,
            detail={ingest.INBOX_PLAYLISTS_KEY: entries},
        ),
        cfg,
    )


def _batch_folder(cfg: config.Config, name: str = BATCH) -> None:
    (Path(cfg.library.root) / cfg.library.music_dir / name).mkdir(parents=True)


def _shown(plan: rotate.RotationPlan) -> dict[str, object]:
    return {
        **{batch.name: batch for batch in (*plan.moves, *plan.removals, *plan.kept)},
        **{left.name: left for left in plan.left},
    }


def test_an_intake_files_playlist_is_recognised_by_its_recorded_name_and_aged_from_it(
    native_library,
):
    cfg, root_id = native_library
    # Imported today, so the row's own date says nothing about when it landed.
    _node(cfg, "Sunset Warmup", under=root_id, age=0)
    _batch_folder(cfg)
    _intake_record(cfg, TODAY - timedelta(days=40), [{"name": "Sunset Warmup", "batch": BATCH}])

    batch = _shown(_plan(cfg))["Sunset Warmup"]

    assert isinstance(batch, rotate.Batch)
    assert batch.recognised_by == rotate.BY_RECORDED_NAME
    assert batch.aged_from == rotate.AGED_FROM_RECORD
    assert batch.age_days == 40
    assert batch.action == rotate.MOVE


def test_a_recorded_name_whose_batch_folder_is_gone_is_left_alone(native_library):
    cfg, root_id = native_library
    _node(cfg, "Sunset Warmup", under=root_id, age=0)
    _intake_record(cfg, TODAY - timedelta(days=40), [{"name": "Sunset Warmup", "batch": BATCH}])

    left = _shown(_plan(cfg))["Sunset Warmup"]

    assert isinstance(left, rotate.Left)
    assert left.kind == "playlist"


def test_an_abandoned_landing_names_nothing(native_library):
    cfg, root_id = native_library
    _node(cfg, "Sunset Warmup", under=root_id, age=0)
    _batch_folder(cfg)
    _intake_record(
        cfg,
        TODAY - timedelta(days=40),
        [{"name": "Sunset Warmup", "batch": BATCH}],
        state=session.SessionState.ABANDONED,
    )

    assert isinstance(_shown(_plan(cfg))["Sunset Warmup"], rotate.Left)


def test_the_latest_landing_of_a_name_is_the_one_it_is_aged_by(native_library):
    cfg, root_id = native_library
    _node(cfg, "Sunset Warmup", under=root_id, age=0)
    _batch_folder(cfg)
    later = "2026-09-23 Tidal playlists"
    _batch_folder(cfg, later)
    _intake_record(
        cfg, TODAY - timedelta(days=40), [{"name": "Sunset Warmup", "batch": BATCH}], tag="a"
    )
    _intake_record(
        cfg, TODAY - timedelta(days=10), [{"name": "Sunset Warmup", "batch": later}], tag="b"
    )

    batch = _shown(_plan(cfg))["Sunset Warmup"]

    assert isinstance(batch, rotate.Batch)
    assert batch.age_days == 10
    assert batch.action == rotate.KEEP


def test_an_entry_with_an_identifier_is_never_read_by_its_name(native_library):
    cfg, root_id = native_library
    # A native landing's entry names another row by identifier; a playlist of
    # the same name a person made is not the landing's.
    _node(cfg, "Sunset Warmup", under=root_id, age=0)
    _batch_folder(cfg)
    _intake_record(
        cfg,
        TODAY - timedelta(days=40),
        [{"id": "999999", "name": "Sunset Warmup", "batch": BATCH}],
    )

    assert isinstance(_shown(_plan(cfg))["Sunset Warmup"], rotate.Left)
