"""The outbound module's scenarios: the export engine and the two prunes (U309).

Every account call is recorded. The window lag is the real adapter's refusal,
met through the lag suite's lagging client. ``account_calls`` lives here; the
organize and export scenarios import it.
"""

from __future__ import annotations

import json

from cratekit.cli import jobs as cli_jobs
from cratekit.core import jobs
from cratekit.core.exit_codes import ExitCode
from tests import outbound_fakes
from tests.test_outbound_order import _adapter
from tests.test_outbound_window_lag import _window_lagging
from tests.test_outbound_workers import bind, catalog, export_verb
from tests.test_outbound_workers import exported as exported  # noqa: PLC0414
from tests.test_outbound_workers import installed as installed  # noqa: PLC0414
from tests.test_prune import EXPORT_PRUNE, LABEL, PRUNE, _exported, _hold
from tests.test_prune import built as built  # noqa: PLC0414

OK = int(ExitCode.OK)
DECISION = int(ExitCode.DECISION_REQUIRED)


def _plain(value):
    """``value`` as JSON can hold it: a mapping's keys as text, a set sorted."""
    if isinstance(value, dict):
        return {str(key): _plain(one) for key, one in value.items()}
    if isinstance(value, (set, frozenset)):
        return sorted(str(one) for one in value)
    if isinstance(value, (list, tuple)):
        return [_plain(one) for one in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def account_calls(stage, account, name: str = "account") -> None:
    """Write everything the fake account recorded under the stage, where the capture reads files."""
    path = stage.root / f"{name}-calls.json"
    # A method a scenario put on the instance is code, and its address moves.
    held = {key: value for key, value in vars(account).items() if not callable(value)}
    path.write_text(json.dumps(_plain(held), indent=1, sort_keys=True) + "\n")


def gated(stage, argv, gate: str, option: str = "apply"):
    """The gate as a person reads it, its two acts, and the acting run as a person reads it."""
    assert stage.crate(*argv).code == DECISION
    refused = stage.json(*argv)
    assert refused.code == DECISION, refused.stdout
    assert refused.envelope["cause"]["detail"]["gate"] == gate, refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, gate, option).code == OK
    return stage.crate("--run", run_id, *argv)


def test_a_playlist_exported_through_its_confirm_and_the_jobs_resume(
    stage, installed, exported, monkeypatch
):
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3))
    bind(monkeypatch, account)
    verb = export_verb(exported)

    queued = gated(stage, verb, "export.playlist.confirm", "export")
    assert queued.code == OK, queued.stderr
    with jobs.open_store() as store:
        (job,) = jobs.list_jobs(store)
    resumed = stage.crate(*cli_jobs.argv_for(job))
    assert resumed.code == OK, resumed.stderr
    assert account.playlist_tracks("pl-1") == ("tid-1", "tid-2", "tid-3")
    account_calls(stage, account)


def test_an_exported_playlist_pruned_of_the_track_its_library_playlist_lost(
    stage, installed, monkeypatch
):
    account = outbound_fakes.FakeAccount(catalog=catalog(1, 2, 3))
    bind(monkeypatch, account)
    _exported(installed, account)
    now = outbound_fakes.write_export(installed.library.root / "outbound", crate=(1, 2))
    verb = ("export", "prune", outbound_fakes.CRATE, "--export", str(now))

    assert gated(stage, verb, EXPORT_PRUNE).code == OK
    assert account.playlists["pl-1"] == ["tid-1", "tid-2"]
    # Run again: the track is off and recorded so, so nothing is planned.
    assert gated(stage, verb, EXPORT_PRUNE).code == OK
    assert account.taken == [("pl-1", ("tid-3",))]
    account_calls(stage, account)


def test_a_label_year_pruned_of_a_held_release(stage, built):
    _hold(built.cfg, "r3")
    verb = ("label", "prune", LABEL)

    assert gated(stage, verb, PRUNE).code == OK
    assert built.account.playlists["pl-3"] == ["t6", "t7"]
    account_calls(stage, built.account)


def test_a_prune_whose_removal_the_accounts_window_lags_is_refused(stage, built):
    """The adapter reads the playlist through a window that never catches up, so nothing is sent."""
    _hold(built.cfg, "r3")
    provider = _window_lagging(["b", "a", "c"], 0, unpaged=2, walk_lags=True)
    provider.previous = (["a", "b", "c"], 0)
    provider.lagging = 99
    adapter = _adapter(built.cfg, provider, [])

    def lagging(_playlist_id, _remote_ids):
        return adapter.remove_tracks("mine", ("b",))

    built.monkeypatch.setattr(built.account, "remove_tracks", lagging)
    refused = gated(stage, ("label", "prune", LABEL), PRUNE)
    assert refused.code == int(ExitCode.PRECONDITION), refused.stderr
    assert "nothing was taken off it" in refused.stderr, refused.stderr
    assert provider.removals == []
    assert built.account.playlists["pl-3"] == ["t4", "t5", "t6", "t7"]
    account_calls(stage, built.account)
