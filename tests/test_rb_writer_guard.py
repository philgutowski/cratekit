"""The guarded writer's refusals: whitelist, two-process refuse, pin, canary, lock.

Every assertion here is ported unchanged in substance from the source system's
guard suite. It is pure and seamed: no live database, no real library, no
rekordbox. That is not a limitation, it is the design. A guard that can only be
tested against a real database is a guard that gets tested rarely, and rarely is
how the source system nearly lost a library.

What the layer this file guards actually promises, and why each promise is
load-bearing rather than decorative:

* **An additive whitelist.** A write session may CREATE rows only in named
  playlist and tag tables, may MODIFY only a named column subset of the content
  table, and may DELETE nothing at all, ever. The commit is rolled back
  otherwise. This is what makes grid and analysis data structurally unwritable
  rather than merely untested, which is R17 stated as a database property.
* **A two-process refusal.** Both the application and its background agent are
  checked, at open and again at commit. The agent is the one that gets missed:
  it mutates the database through cloud sync with the application closed, so
  checking only the application leaves the exact window a long write runs in.
* **A version pin.** The library binding, the schema version, and the installed
  application version. Drift refuses rather than guessing.
* **A cloud canary.** Wired to refuse, deliberately never claiming a positive on
  a signal known to be false. See the parametrized test below, which encodes a
  three-day outage.
* **A cross-process write-session lock**, held from snapshot through smoke test.

THIS FILE WAS SKIPPED UNTIL U7 LANDED. U6 ported the guards before the engine on
purpose, so a violation could not be introduced silently in between. The bodies
were complete and unweakened the whole time, and the production module was never
stubbed to make them green, because a stub turns a real guard into a test of the
stub. The module now exists, the registry entry is gone, and every assertion
below is armed.
"""

from __future__ import annotations

import multiprocessing as mp
import os
from pathlib import Path

import pytest

from cratekit.core import config
from cratekit.core import rb_writer as W
from tests.test_config import valid_data


@pytest.fixture(autouse=True)
def _baseline_registrations():
    """Return the writable-column registry to its baseline around every test.

    The registry is module state by design: an operation registers its fields
    when it is enabled. That makes it exactly the kind of thing one test can
    leave widened for the next, and a widened whitelist is a guard that silently
    stopped guarding.
    """
    W.reset_field_policies()
    yield
    W.reset_field_policies()


# ── the pure whitelist judge ─────────────────────────────────────────────────


def test_permitted_playlist_and_mytag_writes_pass():
    new = [
        ("djmdPlaylist", set()),
        ("djmdSongPlaylist", set()),
        ("djmdMyTag", set()),
        ("djmdSongMyTag", set()),
    ]
    dirty = [("djmdContent", {"ColorID"})]  # the favourites colour write
    assert W.guard_violations(new, dirty, []) == []


def test_creating_a_track_row_is_forbidden():
    """New content rows mean new-track intake, and every ordinary commit refuses one.

    The reason is R15's safety chain: an XML import is something the user
    performs, reviews, and can undo from rekordbox. A row conjured into the
    database directly is none of those things. Since R-746 one commit may admit
    a content row by naming the table, see the creation section below; a
    commit that names nothing is judged exactly as it always was.
    """
    violations = W.guard_violations([("djmdContent", set())], [], [])
    assert len(violations) == 1
    assert "djmdContent" in violations[0] and "intake" in violations[0]


@pytest.mark.parametrize(
    "column", ["BPM", "Analysed", "AnalysisDataPath", "CueUpdated", "AnalysisUpdated"]
)
def test_writing_a_grid_or_analysis_column_is_forbidden(column):
    """R17 as a structural property of the database, not a code review note."""
    violations = W.guard_violations([], [("djmdContent", {column})], [])
    assert len(violations) == 1 and column in violations[0]


def test_new_row_in_unlisted_table_is_forbidden():
    """The whitelist is a whitelist. An unnamed table is refused, not inspected."""
    violations = W.guard_violations([("djmdBeatGrid", set())], [], [])
    assert len(violations) == 1 and "djmdBeatGrid" in violations[0]


def test_deletes_are_forbidden_additive_only():
    """Every delete, from every table, unconditionally.

    Additive-only is what makes the snapshot a real safety net: if nothing is
    ever removed, the worst outcome of a bad run is extra rows, which a person
    can see and remove. Deletion is the one operation whose damage is invisible.
    """
    violations = W.guard_violations([], [], ["djmdSongPlaylist"])
    assert len(violations) == 1 and "additive-only" in violations[0]


def test_bookkeeping_columns_are_ignored_on_dirty_content():
    """The binding bumps sync counters and timestamps on commit by itself.

    Those must not trip the guard, or every legitimate write fails and the guard
    gets disabled, which is the failure mode that actually loses data.
    """
    assert (
        W.guard_violations([], [("djmdContent", {"usn", "rb_local_usn", "updated_at"})], [])
        == []
    )


def test_mixed_session_reports_every_violation():
    """All of them, not the first. A guard that stops at the first finding turns
    one review into several."""
    violations = W.guard_violations(
        [("djmdContent", set()), ("djmdPlaylist", set())],  # one forbidden, one fine
        [("djmdContent", {"BPM", "ColorID"})],  # BPM forbidden, ColorID fine
        ["djmdMyTag"],  # every delete forbidden
    )
    assert len(violations) == 3


# ── the whitelist over a session object ──────────────────────────────────────


class _FakeAttr:
    def __init__(self, key, changed):
        self.key = key
        self._changed = changed

    @property
    def history(self):
        outer = self

        class _History:
            def has_changes(self_inner):
                return outer._changed

        return _History()


class _FakeObj:
    def __init__(self, table, changed_cols):
        class _Table:
            name = table

        self.__table__ = _Table()
        self._attrs = [_FakeAttr(col, True) for col in changed_cols]


class _FakeSession:
    def __init__(self, new=(), dirty=(), deleted=()):
        self.new = list(new)
        self.dirty = list(dirty)
        self.deleted = list(deleted)


@pytest.fixture
def patch_inspect(monkeypatch):
    """Make the ORM's introspection return our fake attribute set.

    Seaming here rather than building real ORM objects keeps the test about the
    guard's decision, which is the part that must never regress, instead of about
    the ORM's object lifecycle, which is not ours.
    """
    import sqlalchemy

    def fake_inspect(obj):
        class _State:
            attrs = obj._attrs

        return _State()

    monkeypatch.setattr(sqlalchemy, "inspect", fake_inspect)


def test_assert_whitelisted_passes_pink_write(patch_inspect):
    session = _FakeSession(dirty=[_FakeObj("djmdContent", {"ColorID"})])
    W.assert_session_whitelisted(session)  # no raise


def test_assert_whitelisted_rejects_beatgrid_write(patch_inspect):
    session = _FakeSession(dirty=[_FakeObj("djmdContent", {"BPM"})])
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_session_whitelisted(session)
    assert "BPM" in str(excinfo.value)


# ── the two-process refusal ──────────────────────────────────────────────────


def test_processes_running_reports_both_names(monkeypatch):
    monkeypatch.setattr(W, "rekordbox_running", lambda: True)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: True)
    assert W.rekordbox_processes_running() == "rekordbox, rekordboxAgent"


def test_agent_only_is_reported(monkeypatch):
    """The gap this check was added to close.

    The background agent mutates the database through cloud sync while the
    application is closed. Checking only the application declares the coast clear
    during exactly the window a long write runs in.
    """
    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: True)
    assert W.rekordbox_processes_running() == "rekordboxAgent"


def test_commit_guarded_refuses_when_agent_running(monkeypatch):
    """Checked again at COMMIT, not only at open.

    A run can take minutes. The user can launch rekordbox during it. Re-checking
    at commit is what makes the open-time check more than a formality.
    """
    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: True)
    with pytest.raises(W.RekordboxRunning) as excinfo:
        W.commit_guarded(object())
    assert "rekordboxAgent" in str(excinfo.value)


# ── the application version pin ──────────────────────────────────────────────


def test_app_version_pin_refuses_on_drift(monkeypatch):
    monkeypatch.setattr(W, "read_installed_app_version", lambda **_: "7.3.0.0001")
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_app_version()
    message = str(excinfo.value)
    assert "7.3.0.0001" in message and str(W.pinned_app_version()) in message


def test_app_version_pin_passes_on_match(monkeypatch):
    monkeypatch.setattr(W, "read_installed_app_version", lambda **_: W.pinned_app_version())
    W.assert_app_version()  # no raise


def test_app_version_pin_skips_when_app_not_found(monkeypatch):
    """A missing application warns and continues; the schema pin still guards.

    Refusing here would break every headless and CI run for no safety gain: if
    the application is not installed, it cannot be holding the database open.
    """
    monkeypatch.setattr(W, "read_installed_app_version", lambda **_: None)
    W.assert_app_version()  # no raise


def test_an_unrecorded_app_version_pin_refuses_even_when_the_install_reads_fine(
    monkeypatch, tmp_path
):
    """S2, and the case the three tests above cannot reach.

    Drift, match, and app-absent all assume a pin EXISTS. U2 makes an unset pin a
    refusal to write, on the grounds that a pin the software copies from whatever
    happens to be installed refuses nothing, forever, which is the entire property
    the pin exists to provide. That refusal lives in
    ``Config.assert_rekordbox_pin_recorded`` and it is inert until this writer
    calls it, so the case is registered here against U7 rather than left as a hope.

    The installed version deliberately reads FINE, so nothing but the missing
    recorded decision can be what refuses.

    THE EXPECTED TYPE CHANGED, AND THAT WAS THE DEFECT RATHER THAN THE FIX. This
    used to assert ``config.ConfigInvalid``, which is what the configuration
    layer raises and what escaped the writer unconverted. A configuration error
    carries no reason slug and no exit code, so the same condition exited under
    two different codes depending on whether a config file existed, and it slipped
    past every ``except RekordboxUnavailable`` a caller writes. What was worth
    pinning is that an unrecorded pin refuses AT ALL, which is asserted below,
    unchanged in substance. The configuration error is still reachable underneath.
    """
    library = tmp_path / "library"
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    unpinned = config.from_dict(valid_data(library))
    assert unpinned.rekordbox.pinned_app_version is None

    monkeypatch.setattr(config, "load", lambda *args, **kwargs: unpinned)
    monkeypatch.setattr(W, "read_installed_app_version", lambda **_: "7.2.14.0323")

    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_app_version()
    assert excinfo.value.cause.reason == "app-version-pin-unrecorded"
    assert "pinned_app_version" in str(excinfo.value)
    assert isinstance(excinfo.value.__cause__, config.ConfigInvalid)


def test_an_unrecorded_pin_refuses_with_ONE_code_whether_or_not_config_loads(
    monkeypatch, tmp_path
):
    """The KTD25 collision this repair exists to close, asserted from both sides.

    One condition, two machines. On a machine with a config file the writer used
    to let ``ConfigInvalid`` escape, which the command-line layer rebuilt as a
    configuration precondition. On a machine with no usable config at all the
    writer raised its own version-pin refusal. Same missing decision, two exit
    codes, and the one a caller saw depended on a file it never asked about.

    Both codes are read from the raised causes rather than written down here, so
    the assertion is that they AGREE, not that they equal a number somebody typed.
    """
    library = tmp_path / "library"
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    unpinned = config.from_dict(valid_data(library))
    monkeypatch.setattr(W, "read_installed_app_version", lambda **_: "7.2.14.0323")

    monkeypatch.setattr(config, "load", lambda *args, **kwargs: unpinned)
    with pytest.raises(W.RekordboxUnavailable) as with_config:
        W.assert_app_version()

    def unloadable(*args, **kwargs):
        raise config.ConfigMissing("no configuration on this machine")

    monkeypatch.setattr(config, "load", unloadable)
    with pytest.raises(W.RekordboxUnavailable) as without_config:
        W.assert_app_version()

    assert with_config.value.cause.reason == without_config.value.cause.reason
    assert with_config.value.cause.code == without_config.value.cause.code
    assert (
        with_config.value.cause.remediation.remedy
        == without_config.value.cause.remediation.remedy
    )


# ── the cloud-sync canary ────────────────────────────────────────────────────


class _FakeDB:
    def __init__(self, cloud_rows):
        self._rows = cloud_rows

    class _Session:
        def __init__(self, rows):
            self._rows = rows

        def execute(self, *_args, **_kwargs):
            rows = self._rows

            class _Result:
                def scalar(self_inner):
                    return rows

            return _Result()

    @property
    def session(self):
        return _FakeDB._Session(self._rows)


@pytest.mark.parametrize("rows", [0, 1, 2])
def test_cloud_sync_reports_undetectable(rows):
    """No usable predicate exists, so the probe never claims a positive.

    A registry row USED to be read as "sync is active". A real library carried
    one for years with cloud sync switched off, so that predicate refused every
    open for three days. Refusing on a signal known to be false is the
    blocks-blindly failure this guard exists to avoid. The live protection is the
    agent process check, not this. Encoded as a test so nobody re-derives the
    plausible-looking predicate and repeats the outage.
    """
    assert W.cloud_sync_active(_FakeDB(cloud_rows=rows)) is False


def test_commit_guarded_refuses_on_active_cloud(monkeypatch):
    """The refusal path stays wired for the day a real predicate lands.

    Driven at the seam rather than through the falsified registry count, so the
    wiring is proved without reinstating the false predicate.
    """
    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(W, "cloud_sync_active", lambda _db: True)
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.commit_guarded(_FakeDB(cloud_rows=0))
    assert "Cloud Library Sync" in str(excinfo.value)


# ── the cross-process write-session lock ─────────────────────────────────────


def _hold_lock(path, ready, release):
    with W.write_session_lock(path):
        ready.set()
        release.wait(timeout=10)


def test_second_writer_refuses_while_lock_held(tmp_path):
    """A real second PROCESS, not a second call in this one.

    An in-process test would pass against a lock implemented with a module-level
    flag, which protects nothing: the case that matters is two runs started from
    two terminals against one library.
    """
    lock = tmp_path / "rb_writer.lock"
    # "spawn", not "fork": fork does not exist on Windows and raises there, and
    # the target is already module level with picklable arguments, so spawn
    # proves the same cross-process contention with no platform assumption (R1).
    ctx = mp.get_context("spawn")
    ready, release = ctx.Event(), ctx.Event()
    holder = ctx.Process(target=_hold_lock, args=(lock, ready, release))
    holder.start()
    try:
        assert ready.wait(timeout=10), "holder never acquired the lock"
        with pytest.raises(W.RekordboxUnavailable) as excinfo:
            with W.write_session_lock(lock):
                pass
        assert "write-session lock" in str(excinfo.value)
    finally:
        release.set()
        holder.join(timeout=10)
    # Once released, the lock is acquirable again. Without this the test would
    # pass against a lock that never releases, which is its own outage.
    with W.write_session_lock(lock):
        pass


# ── the version pins, against a RECORDED pin ─────────────────────────────────
#
# The three ported pin tests above run on a machine with no configuration at
# all, where the recorded pin is necessarily absent. These cover the case that
# actually ships: a pin somebody wrote down, and an install compared against it.


def _pinned_config(tmp_path, monkeypatch, **rekordbox):
    library = tmp_path / "library"
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    cfg = config.from_dict(valid_data(library, rekordbox=rekordbox))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: cfg)
    return cfg


def test_a_recorded_pin_that_matches_the_install_proceeds(tmp_path, monkeypatch):
    _pinned_config(
        tmp_path, monkeypatch, pinned_app_version="9.9.9.0001", validated_on="2026-08-01"
    )
    monkeypatch.setattr(W, "read_installed_app_version", lambda **_: "9.9.9.0001")
    W.assert_app_version()  # no raise


@pytest.mark.parametrize("installed", ["9.9.9.0002", "9.9.10.0001", "10.9.9.0001", "9.9.9"])
def test_the_recorded_pin_is_compared_EXACTLY(tmp_path, monkeypatch, installed):
    """No tolerance, no major-and-minor shortcut, no version arithmetic.

    The schema pin cannot see a point release: it held its value across a whole
    major version of rekordbox. Key extraction has broken across a point release
    before, so a comparison that ignores the last field deletes the only pin that
    can see one.
    """
    _pinned_config(
        tmp_path, monkeypatch, pinned_app_version="9.9.9.0001", validated_on="2026-08-01"
    )
    monkeypatch.setattr(W, "read_installed_app_version", lambda **_: installed)
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_app_version()
    assert excinfo.value.cause.reason == "app-version-pin-drift"


def test_a_drifted_pin_can_be_forced_for_a_deliberate_revalidation(tmp_path, monkeypatch):
    """The escape stays, stays loud, and stays off by default."""
    _pinned_config(
        tmp_path, monkeypatch, pinned_app_version="9.9.9.0001", validated_on="2026-08-01"
    )
    monkeypatch.setattr(W, "read_installed_app_version", lambda **_: "9.9.9.0002")
    W.assert_app_version(force=True)  # no raise


def test_the_validation_DATE_travels_with_the_refusal(tmp_path, monkeypatch):
    """A pin without its date is a number somebody typed.

    The health check has to be able to say "pinned to X, validated on Y,
    installed is Z", and it reads the same accessors this refusal carries rather
    than re-deriving them, so the two can never disagree.
    """
    _pinned_config(
        tmp_path, monkeypatch, pinned_app_version="9.9.9.0001", validated_on="2026-08-01"
    )
    monkeypatch.setattr(W, "read_installed_app_version", lambda **_: "9.9.9.0002")
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_app_version()
    assert excinfo.value.cause.detail["validated_on"] == "2026-08-01"
    assert W.pin_validated_on() == "2026-08-01"


def test_the_probe_searches_the_SAME_configuration_the_pin_is_judged_against(
    monkeypatch, tmp_path
):
    """P2, as an identity check rather than as a value comparison.

    The probe used to be called with no argument, so it resolved its own
    configuration by loading one. A caller that passed an explicit config
    therefore had its pin compared against that config and its application
    searched for under a different one. Under KTD9 a queued job runs against the
    configuration frozen when it was queued, so "a different one" is not
    hypothetical: it is whatever the file says at the moment the job runs.

    Asserting object IDENTITY is what makes this fail if the threading is ever
    removed. Comparing values would pass against two equal-but-separately-loaded
    configurations, which is exactly the bug.
    """
    supplied = _pinned_config(
        tmp_path, monkeypatch, pinned_app_version="9.9.9.0001", validated_on="2026-08-01"
    )
    other = config.from_dict(valid_data(tmp_path / "library"))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: other)

    seen: list[object] = []

    def recording_probe(*, cfg=None):
        seen.append(cfg)
        return "9.9.9.0001"

    monkeypatch.setattr(W, "read_installed_app_version", recording_probe)
    W.assert_app_version(cfg=supplied)  # no raise: the pin matches

    assert seen == [supplied], "the probe did not receive the caller's configuration"
    assert seen[0] is not other, "the probe re-loaded instead of taking what it was given"


def test_the_probe_takes_its_configuration_BY_KEYWORD():
    """So a caller cannot hand it an application path by position.

    The parameter is the effective configuration, not a path, and the two are one
    positional slot apart. Keyword-only is what makes that mistake unwritable
    rather than merely undocumented.
    """
    import inspect

    parameter = inspect.signature(W.read_installed_app_version).parameters["cfg"]
    assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
    assert parameter.default is None


def test_the_binding_pin_has_no_escape_at_all():
    """Pins two and three take a force flag. This one does not, by design.

    A mismatched binding maps table shapes this build was never validated
    against, and there is no run in which proceeding is the right answer.
    """
    import inspect

    assert "force" not in inspect.signature(W.assert_binding_version).parameters


def test_the_shipped_pins_have_defaults_and_the_machine_pin_does_not():
    """Which pins may default, and why the answer differs per pin.

    The binding version and the schema version are facts about the SHIPPED build,
    fixed by the lockfile and by what this build was validated against. The
    application version is a fact about the USER's machine, so defaulting it
    would be exactly the tautology S2 forbids.
    """
    assert W.pinned_pyrekordbox() and W.pinned_db_version()
    assert W.pinned_app_version() is None


# ── the cloud-sync canary ────────────────────────────────────────────────────


def _settings(monkeypatch, values):
    monkeypatch.setattr(W, "read_rekordbox_settings", lambda *args, **kwargs: values)


def test_the_marker_is_the_library_sync_setting(monkeypatch):
    _settings(monkeypatch, {W.LIBRARY_SYNC_SETTING: 1})
    verdict = W.cloud_sync_state()
    assert verdict.state is W.CloudSyncState.ON
    assert W.LIBRARY_SYNC_SETTING in verdict.reason


def test_the_setting_switched_off_reads_off(monkeypatch):
    _settings(monkeypatch, {W.LIBRARY_SYNC_SETTING: 0})
    assert W.cloud_sync_state().state is W.CloudSyncState.OFF


@pytest.mark.parametrize("trap", ["CLSSyncMethod", "OverwriteSyncList"])
def test_the_two_settings_traps_do_not_trip_the_canary(monkeypatch, trap):
    """Both read as ENABLED while library sync is off.

    Anything matching a substring of the word "sync" produces an immediate false
    positive on a library whose sync has been off for years, which is the same
    class of mistake as the row-count predicate this canary replaced.
    """
    _settings(monkeypatch, {W.LIBRARY_SYNC_SETTING: 0, trap: 1})
    assert W.cloud_sync_state().state is W.CloudSyncState.OFF


def test_an_unreadable_settings_file_is_unknown_and_says_why(monkeypatch):
    """Self-diagnosing in one line, which the refusal it replaces was not.

    The predicate this replaced named a database table as the cause while the
    same file's docstring recorded that table as a false signal, so a three-day
    outage pointed the reader at the wrong thing the whole time.
    """

    def unreadable(*args, **kwargs):
        raise FileNotFoundError("no settings file here")

    monkeypatch.setattr(W, "read_rekordbox_settings", unreadable)
    verdict = W.cloud_sync_state()
    assert verdict.state is W.CloudSyncState.UNKNOWN
    assert "no settings file here" in verdict.reason


def test_a_settings_file_without_the_key_is_unknown_not_off(monkeypatch):
    """Absence is not a value. Reading a missing key as "off" is a guess."""
    _settings(monkeypatch, {"CLSSyncMethod": 1})
    assert W.cloud_sync_state().state is W.CloudSyncState.UNKNOWN


def test_the_settings_directory_is_named_for_the_previous_major_version():
    """Verified on a machine running the NEXT major version of rekordbox.

    There is no directory named for the installed major version at all, so
    deriving the name from it finds nothing and every machine reads as unknown.
    """
    assert W.SETTINGS_APP_DIRNAME == "rekordbox6"


def test_an_unknown_state_answers_false_to_the_activity_predicate(monkeypatch):
    """And is refused separately, which is the whole reason they are two things.

    Folding "cannot tell" into the activity predicate is what would let the
    falsified row-count signal back in through the same door.
    """

    def unreadable(*args, **kwargs):
        raise OSError("nothing to read")

    monkeypatch.setattr(W, "read_rekordbox_settings", unreadable)
    assert W.cloud_sync_active(object()) is False
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_cloud_sync_readable()
    # The slug moved off ``cloud-sync-active`` deliberately. It was never
    # asserting that this condition IS the active one; it was asserting that this
    # condition refuses, which it still does, under the reason that names it.
    assert excinfo.value.cause.reason == "cloud-sync-unreadable"


def test_the_unknown_refusal_has_a_named_escape(monkeypatch):
    """Because unknown is the ordinary state on a machine that has never run
    rekordbox, and a refusal with no way past it is a lockout."""

    def unreadable(*args, **kwargs):
        raise OSError("nothing to read")

    monkeypatch.setattr(W, "read_rekordbox_settings", unreadable)
    W.assert_cloud_sync_readable(force=True)  # no raise


def test_the_docstring_still_says_the_ON_ENCODING_IS_AN_UNTESTED_INFERENCE():
    """The one clause in this module a tidy-up would delete without noticing.

    The falsification record beside it reads as a list of things that were
    CHECKED, and the positive branch of this predicate was not: the toggle was
    deliberately never exercised, because switching library sync on against a
    library with 2,938,336 unacknowledged local updates starts the cloud agent
    reconciling that backlog. A reader who cannot separate the checked half from
    the unchecked half will trust the wrong one, and the only thing standing
    between them is a sentence. Sentences get tidied. This makes that fail.
    """
    assert "untested inference" in (W.cloud_sync_state.__doc__ or "")


def test_the_canary_reads_the_settings_file_and_NOTHING_ELSE(monkeypatch):
    """A3's verdict, expressed as a property of the code rather than as a note.

    The staleness cross-check was deleted on evidence that rekordbox writes the
    settings file at toggle time rather than at quit. What matters more than the
    tidiness is that the cross-check was the only thing in this canary that
    touched the caller's session, and touching the session is what re-arms the
    autoflush hazard below. So the assertion is not "the helper is gone", it is
    "a database handle passed here is never used", which stays true only while
    nothing queries.
    """

    class _Explodes:
        """Any attribute access at all is a failure."""

        def __getattr__(self, name):
            raise AssertionError(f"the canary reached into the database for {name!r}")

    _settings(monkeypatch, {W.LIBRARY_SYNC_SETTING: 0})
    assert W.cloud_sync_state(_Explodes()).state is W.CloudSyncState.OFF
    assert W.cloud_sync_active(_Explodes()) is False
    W.assert_cloud_sync_readable(_Explodes())  # no raise, and no database read


@pytest.mark.parametrize(
    "gone", ["_recent_sync_evidence", "CLOUD_SYNC_RECENT_DAYS", "LAST_SYNC_ROW", "OPLOG_ROW_PREFIX"]
)
def test_the_deleted_cross_check_is_not_quietly_reintroduced(gone):
    """Named one by one because each is a separate way back to the same shape.

    A future reader looking at a canary that reads one file may reasonably think
    corroborating it against the database is a free improvement. It is not free:
    the last time it was tried it flushed a caller's pending write past the
    additive whitelist. Reinstating any of these fails here first, which is the
    prompt to read ``_no_autoflush`` before writing the query.
    """
    assert not hasattr(W, gone)


# ── the settings file itself, parsed rather than faked ───────────────────────
#
# Every canary test above patches ``read_rekordbox_settings`` and therefore
# proves nothing about the PARSE. This one parses a real file. With
# ``CRATEKIT_TEST_REKORDBOX_SETTINGS`` unset it parses one written here; with it
# set to a real rekordbox application-data directory it parses that instead. The
# assertions are identical either way, which is what makes a supplied fixture
# strengthen the battery rather than switch it on.


def _write_settings_file(app_data_dir, values):
    """Write a settings file in rekordbox's own shape. Returns the directory.

    The shape matters: the binding's reader walks ``VALUE`` elements and reads
    their ``name`` and ``val`` attributes, so a file written any other way would
    make this test prove that our own writer and our own reader agree.
    """
    settings_dir = app_data_dir / W.SETTINGS_APP_DIRNAME
    settings_dir.mkdir(parents=True, exist_ok=True)
    entries = "".join(f'<VALUE name="{name}" val="{val}"/>' for name, val in values.items())
    (settings_dir / "rekordbox3.settings").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><PIONEER>{entries}</PIONEER>'
    )
    return app_data_dir


@pytest.fixture()
def settings_app_data(tmp_path):
    """A rekordbox application-data directory: supplied if there is one, else built.

    Substitution, not a skip. The gate the verification contract asks for is the
    PRESENCE of a fixture, and a skip would let the untested case read as tested
    in a summary line. See ``W.TEST_SETTINGS_ENV``.
    """
    supplied = os.environ.get(W.TEST_SETTINGS_ENV)
    if supplied:
        return Path(supplied)
    return _write_settings_file(tmp_path / "appdata", {W.LIBRARY_SYNC_SETTING: 0})


def test_a_real_settings_file_parses_into_a_verdict(settings_app_data, monkeypatch):
    """The parse, the key lookup, and the verdict, end to end with no patching.

    DEFERRED IN HALF. The supplied-fixture half needs a copy of a real
    ``rekordbox3.settings``, which the offline library volume cannot provide
    today. The written-file half runs everywhere and covers the parse, the
    directory name, and the OFF encoding recorded on 2026-08-01. What only the
    real file can add is whether a live rekordbox writes anything this reader
    mishandles, which is why the assertions are written against whatever the file
    says rather than against a value baked in here.
    """
    read = W.read_rekordbox_settings
    settings = read(settings_app_data)
    assert W.LIBRARY_SYNC_SETTING in settings, (
        f"no {W.LIBRARY_SYNC_SETTING} in the settings file under "
        f"{settings_app_data / W.SETTINGS_APP_DIRNAME}"
    )

    # Bound BEFORE the patch, so the canary drives the real reader against the
    # real directory. Re-entering the module attribute here would call the
    # stand-in and prove only that a lambda can call itself.
    monkeypatch.setattr(
        W, "read_rekordbox_settings", lambda *args, **kwargs: read(settings_app_data)
    )
    verdict = W.cloud_sync_state()
    declared = settings[W.LIBRARY_SYNC_SETTING]
    expected = W.CloudSyncState.OFF if str(declared) in ("0", "False") else W.CloudSyncState.ON
    assert verdict.state is expected
    assert W.LIBRARY_SYNC_SETTING in verdict.reason


def test_a_settings_file_the_reader_cannot_find_reads_as_unknown(tmp_path, monkeypatch):
    """The other branch of the same parse: a directory with no file in it.

    Driven through the real reader rather than a stand-in that raises, because
    "unknown" is the state a machine that has never run rekordbox is in, and that
    machine is the one most likely to be running this software for the first
    time. What is under test is that a genuine read failure becomes a REFUSAL
    with the reason attached, not a crash and not a quiet "off".
    """
    empty = tmp_path / "empty"
    (empty / W.SETTINGS_APP_DIRNAME).mkdir(parents=True)
    read = W.read_rekordbox_settings  # bound before the patch, as above
    monkeypatch.setattr(W, "read_rekordbox_settings", lambda *args, **kwargs: read(empty))

    verdict = W.cloud_sync_state()
    assert verdict.state is W.CloudSyncState.UNKNOWN
    assert W.LIBRARY_SYNC_SETTING in verdict.reason

    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_cloud_sync_readable()
    assert excinfo.value.cause.reason == "cloud-sync-unreadable"


# ── the writable-column registration seam ────────────────────────────────────


def test_nothing_is_writable_when_no_operation_is_registered():
    """R14 as a property rather than as a sentence.

    The source shipped a static maximal union, so a slim install with every
    metadata operation disabled still had four content columns structurally
    writable. Here the gate is closed until something opens it.
    """
    W._REGISTERED.clear()
    try:
        assert W.content_writable_columns() == frozenset()
        violations = W.guard_violations([], [("djmdContent", {"ColorID"})], [])
        assert len(violations) == 1 and "ColorID" in violations[0]
    finally:
        W.reset_field_policies()


def test_a_registration_widens_the_gate_by_exactly_its_declared_fields():
    W.register_field_policy(
        W.FieldPolicy(owner="genre-retag", fields={"GenreID": W.Ownership.OWNED})
    )
    assert W.content_writable_columns() == {"ColorID", "GenreID"}
    assert W.guard_violations([], [("djmdContent", {"GenreID"})], []) == []
    assert W.guard_violations([], [("djmdContent", {"Rating"})], []) != []


def test_the_permitted_TABLES_are_static_and_no_registration_widens_them():
    """The structural guarantee, which is a different thing from the column gate.

    Grid and analysis rows are unwritable because their tables are not listed,
    and nothing an operation declares may add one. If registration could widen
    this, R17 would become a matter of what happens to be enabled.
    """
    W.register_field_policy(
        W.FieldPolicy(owner="anything", fields={"BPM": W.Ownership.OWNED})
    )
    assert "djmdBeatGrid" not in W.PERMITTED_ROW_TABLES
    assert W.guard_violations([("djmdBeatGrid", set())], [], []) != []


def test_the_judge_takes_the_column_set_as_a_parameter_and_stays_pure():
    """So a second taxonomy of operations can be judged in one process.

    A function that reads a module-level registry cannot be exercised against
    two configurations at once, and proving the seam works needs exactly that.
    """
    dirty = [("djmdContent", {"Rating"})]
    assert W.guard_violations([], dirty, [], content_columns={"Rating"}) == []
    assert W.guard_violations([], [("djmdContent", {"ColorID"})], [], content_columns=set()) != []


def test_the_bookkeeping_exemption_covers_ten_columns():
    """Ten, not nine.

    Counted because a missing exemption makes the binding's own commit-time
    bookkeeping trip the guard, which fails every legitimate write, and a guard
    that fires on correct code gets switched off.
    """
    assert len(W.BOOKKEEPING_COLUMNS) == 10
    bumped = set(W.BOOKKEEPING_COLUMNS) - {W.SOFT_DELETE_COLUMN}
    assert W.guard_violations([], [("djmdContent", bumped)], []) == []


# ── the one removal, R-758 ───────────────────────────────────────────────────

#: Every table the binding maps a row class for that carries the marker, read
#: off the binding so a table it gains is a table these tests cover.
def _tables_with_a_marker() -> list[str]:
    from pyrekordbox.db6 import tables

    return sorted(
        mapper.class_.__table__.name
        for mapper in tables.Base.registry.mappers
        if W.SOFT_DELETE_COLUMN in mapper.class_.__table__.columns
    )


def test_the_binding_maps_the_tables_the_removal_tests_walk():
    found = _tables_with_a_marker()
    assert W.MEMBERSHIP_TABLE in found and W.CONTENT_TABLE in found
    assert len(found) > 10, found


@pytest.mark.parametrize("table", _tables_with_a_marker())
def test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one(table):
    """The marker is a bookkeeping column, so a row whose only change was the
    marker read as untouched, in any table, the collection included."""
    for columns in ({W.SOFT_DELETE_COLUMN}, {W.SOFT_DELETE_COLUMN, "updated_at", "rb_local_usn"}):
        violations = W.guard_violations([], [(table, columns)], [])
        assert len(violations) == 1, (table, violations)
        assert "soft delete marker" in violations[0] and repr(table) in violations[0]


def test_the_removable_tables_are_exactly_the_membership_table():
    assert W.REMOVABLE_TABLES == frozenset({"djmdSongPlaylist"})
    assert W.MEMBERSHIP_TABLE == "djmdSongPlaylist"


def test_a_commit_that_asks_may_remove_a_membership_and_nothing_else():
    removal = {W.SOFT_DELETE_COLUMN, "updated_at", "rb_local_usn"}
    asked = {W.MEMBERSHIP_TABLE}
    assert W.guard_violations([], [(W.MEMBERSHIP_TABLE, removal)], [], removals=asked) == []
    for table in _tables_with_a_marker():
        if table == W.MEMBERSHIP_TABLE:
            continue
        violations = W.guard_violations([], [(table, removal)], [], removals=asked)
        assert len(violations) == 1 and repr(table) in violations[0], table


@pytest.mark.parametrize(
    "table", [name for name in _tables_with_a_marker() if name != "djmdSongPlaylist"]
)
def test_asking_for_a_removal_in_any_other_table_is_itself_refused(table):
    """The set is a ceiling a caller cannot raise by asking."""
    violations = W.guard_violations(
        [], [(table, {W.SOFT_DELETE_COLUMN})], [], removals={table}
    )
    assert len(violations) == 2, violations
    assert any("asks to remove" in line for line in violations)
    assert any("soft delete marker" in line for line in violations)
    # Asked for and unused, it is still refused.
    assert W.guard_violations([], [], [], removals={table}) != []


def test_an_admitted_removal_admits_no_hard_delete():
    """A hard delete is refused in the membership table as it is everywhere."""
    violations = W.guard_violations(
        [], [], [W.MEMBERSHIP_TABLE], removals={W.MEMBERSHIP_TABLE}
    )
    assert len(violations) == 1 and "additive-only" in violations[0]


def test_an_admitted_removal_still_judges_the_other_columns_of_the_row():
    violations = W.guard_violations(
        [],
        [(W.CONTENT_TABLE, {"BPM"}), (W.MEMBERSHIP_TABLE, {W.SOFT_DELETE_COLUMN})],
        [],
        removals={W.MEMBERSHIP_TABLE},
    )
    assert len(violations) == 1 and "BPM" in violations[0]


# ── the one creation beyond the whitelist, R-746 ─────────────────────────────


#: What the binding's ``add_content`` declares on the row it makes, read off
#: its source on 2026-09-29 (pyrekordbox 0.4.4), plus the title a landing sets.
#: None of it is an analysis column, which is what makes the bare row admissible.
_LANDED_ROW = {
    "ID",
    "UUID",
    "ContentLink",
    "DateCreated",
    "DeviceID",
    "FileNameL",
    "FileSize",
    "FileType",
    "FolderPath",
    "HotCueAutoLoad",
    "MasterDBID",
    "MasterSongID",
    "StockDate",
    "rb_file_id",
    "Title",
}


def test_the_admittable_tables_are_exactly_the_content_table():
    assert W.ADMITTABLE_ROW_TABLES == frozenset({"djmdContent"})
    assert W.CONTENT_TABLE not in W.PERMITTED_ROW_TABLES


def test_a_commit_that_asks_may_create_a_content_row_carrying_what_the_file_says():
    asked = {W.CONTENT_TABLE}
    assert W.guard_violations([(W.CONTENT_TABLE, _LANDED_ROW)], [], [], creations=asked) == []
    # And the same row with nothing asked is the refusal it always was.
    assert W.guard_violations([(W.CONTENT_TABLE, _LANDED_ROW)], [], []) != []


@pytest.mark.parametrize("column", sorted(W.CONTENT_ROW_EMPTY_COLUMNS))
def test_an_admitted_content_row_declaring_an_analysis_column_is_refused(column):
    """The admission is a ceiling on the table, never on what the row may carry.

    Ten columns, not the five the playlist tables are held to: a content row is
    the one row an analysis pass writes into, so the key, the rates and the
    artwork path are analysis outputs here and nowhere else.
    """
    violations = W.guard_violations(
        [(W.CONTENT_TABLE, _LANDED_ROW | {column})], [], [], creations={W.CONTENT_TABLE}
    )
    assert len(violations) == 1, violations
    assert column in violations[0] and "analysis" in violations[0]


def test_the_wider_content_policy_contains_the_playlist_policy():
    assert W.GRIDLESS_ON_CREATE_COLUMNS < W.CONTENT_ROW_EMPTY_COLUMNS
    assert {"KeyID", "SampleRate", "BitRate", "BitDepth", "ImagePath"} < W.CONTENT_ROW_EMPTY_COLUMNS


@pytest.mark.parametrize("table", ["djmdArtist", "djmdGenre", "djmdAlbum", "djmdBeatGrid"])
def test_asking_for_a_creation_in_any_other_table_is_itself_refused(table):
    """The set is a ceiling a caller cannot raise by asking (P5)."""
    violations = W.guard_violations([(table, set())], [], [], creations={table})
    assert len(violations) == 2, violations
    assert any("asks to create" in line for line in violations)
    assert any("non-whitelisted" in line for line in violations)
    # Asked for and unused, it is still refused.
    assert W.guard_violations([], [], [], creations={table}) != []


def test_an_admitted_creation_admits_no_removal_and_no_delete():
    """Naming the content table on ``creations`` says nothing about the other two loops."""
    asked = {W.CONTENT_TABLE}
    assert W.guard_violations([], [], [W.CONTENT_TABLE], creations=asked) != []
    violations = W.guard_violations(
        [], [(W.CONTENT_TABLE, {W.SOFT_DELETE_COLUMN})], [], creations=asked
    )
    assert len(violations) == 1 and "soft delete marker" in violations[0]


def test_an_admitted_creation_still_refuses_a_second_content_row_nobody_asked_about():
    """One admission covers the commit, and every content row in it is judged."""
    violations = W.guard_violations(
        [(W.CONTENT_TABLE, _LANDED_ROW), (W.CONTENT_TABLE, _LANDED_ROW | {"Analysed"})],
        [],
        [],
        creations={W.CONTENT_TABLE},
    )
    assert len(violations) == 1 and "Analysed" in violations[0]


def test_every_other_writer_in_the_package_asks_for_no_creation():
    """The callers that pass ``creations`` are the native landing and nobody else.

    A source guard rather than a runtime one, because the property is about who
    may ask: a membership writer that learned to name the content table would
    pass every runtime check and still be the hazard the whitelist exists for.
    """
    import re

    root = Path(__file__).resolve().parents[1] / "src" / "cratekit"
    askers = sorted(
        str(path.relative_to(root))
        for path in root.rglob("*.py")
        if re.search(r"commit_guarded\([^)]*creations=", path.read_text(encoding="utf-8"), re.S)
    )
    assert askers == ["intake/native.py"], askers


# ── the per-field policy ─────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "mode, current, expected",
    [
        (W.Ownership.OWNED, "old", W.Decision.WRITE),
        (W.Ownership.OWNED, "new", W.Decision.SKIP_SAME),
        (W.Ownership.FILL_IF_EMPTY, None, W.Decision.WRITE),
        (W.Ownership.FILL_IF_EMPTY, "", W.Decision.WRITE),
        (W.Ownership.FILL_IF_EMPTY, "old", W.Decision.SKIP_PRESENT),
    ],
)
def test_the_per_field_policy_decides_one_write(mode, current, expected):
    policies = {"an-operation": W.FieldPolicy(owner="an-operation", fields={"Title": mode})}
    decision = W.metadata_decision("an-operation", "Title", current, "new", policies=policies)
    assert decision is expected


def test_an_unregistered_operation_and_an_undeclared_field_both_write_nothing():
    """Closed at both levels, which is what makes a hand-set value safe.

    A rating a person chose, a colour a person picked, and a comment a person
    typed have no policy entry, so they are unwritable by automation rather than
    protected by a rule somebody has to remember.
    """
    policies = {
        "an-operation": W.FieldPolicy(owner="an-operation", fields={"Title": W.Ownership.OWNED})
    }
    assert (
        W.metadata_decision("another-operation", "Title", None, "x", policies=policies)
        is W.Decision.SKIP_UNOWNED
    )
    assert (
        W.metadata_decision("an-operation", "Rating", None, 5, policies=policies)
        is W.Decision.SKIP_UNOWNED
    )


def test_a_numeric_identifier_column_counts_zero_as_empty():
    """The reason emptiness is a per-column table rather than one rule.

    An identifier column spells "unset" as null, empty, zero, or the STRING
    zero, and a rule covering the four identifier columns would miss the rating,
    which is numeric but is not an identifier.
    """
    policies = {
        "a-fill": W.FieldPolicy(owner="a-fill", fields={"KeyID": W.Ownership.FILL_IF_EMPTY})
    }
    assert W.metadata_decision("a-fill", "KeyID", 0, "5", policies=policies) is W.Decision.WRITE
    present = W.metadata_decision("a-fill", "KeyID", "3", "5", policies=policies)
    assert present is W.Decision.SKIP_PRESENT


def test_writing_a_field_applies_the_decision_and_reports_it():
    class _Row:
        Title = "old"

    row = _Row()
    policies = {"an-op": W.FieldPolicy(owner="an-op", fields={"Title": W.Ownership.OWNED})}
    written = W.write_metadata_field(row, "an-op", "Title", "new", policies=policies)
    assert written is W.Decision.WRITE
    assert row.Title == "new"
    assert (
        W.write_metadata_field(row, "unregistered", "Title", "other", policies=policies)
        is W.Decision.SKIP_UNOWNED
    )
    assert row.Title == "new"


# ── a read must never flush the caller's pending work past the guard ─────────


class _FlushingSession:
    """A session that empties its pending sets on a query, as a real one does.

    Not a caricature. An object-mapper session flushes before a query so the
    query can see pending changes, and a flush is exactly what empties the
    collections the whitelist reads.
    """

    def __init__(self):
        self.new = []
        self.dirty = [_FakeObj("djmdContent", {"BPM"})]
        self.deleted = []
        self.autoflush = True

    def query(self, *_args, **_kwargs):
        if self.autoflush:
            self.dirty.clear()  # the flush

        class _Query:
            def filter(self_inner, *_a, **_k):
                return self_inner

            def first(self_inner):
                return None

        return _Query()

    @property
    def no_autoflush(self):
        outer = self

        class _Suspended:
            def __enter__(self_inner):
                outer.autoflush = False

            def __exit__(self_inner, *_exc):
                outer.autoflush = True
                return False

        return _Suspended()


class _FlushingDB:
    def __init__(self):
        self.session = _FlushingSession()
        self.rolled_back = False
        self.committed = False

    def rollback(self):
        self.rolled_back = True

    def commit(self):
        self.committed = True


def test_a_probe_that_queries_cannot_flush_a_forbidden_write_past_the_guard(
    monkeypatch, patch_inspect
):
    """The sharpest failure in this module, caught and pinned.

    The canary in the source read nothing at all, so running it before the
    whitelist was safe by accident. Giving it a real predicate made it a query,
    and a query flushes: the pending analysis-column write vanished from the
    session and the guard approved a commit it could no longer see. Found against
    a real database while building this unit.
    """
    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(
        W, "read_rekordbox_settings", lambda *args, **kwargs: {W.LIBRARY_SYNC_SETTING: 0}
    )

    db = _FlushingDB()
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.commit_guarded(db)
    assert "BPM" in str(excinfo.value)
    assert db.rolled_back and not db.committed


def test_the_containment_is_still_armed_for_the_NEXT_probe(monkeypatch, patch_inspect):
    """P6, and the reason the test above is no longer sufficient on its own.

    The probe that exposed this hazard was the canary's database cross-check, and
    that has been deleted: nothing on the pre-commit path queries any more, so
    the test above now passes because no flush is attempted rather than because
    one was contained. A guard that passes for the wrong reason is a guard that
    can be removed without anything going red.

    So this one puts a querying probe back on that path deliberately, standing in
    for whatever gets added there next, and asserts the caller's pending work
    survives it. It fails the moment the suspension is dropped from
    ``commit_guarded``, which is exactly the change a future tidy-up would make
    after noticing that the current occupant no longer needs it.
    """
    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: False)

    def querying_probe(db):
        db.session.query(object)  # the flush, if it is not suspended
        return False

    monkeypatch.setattr(W, "cloud_sync_active", querying_probe)
    monkeypatch.setattr(
        W, "read_rekordbox_settings", lambda *args, **kwargs: {W.LIBRARY_SYNC_SETTING: 0}
    )

    db = _FlushingDB()
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.commit_guarded(db)
    assert "BPM" in str(excinfo.value), (
        "a probe on the pre-commit path flushed the caller's pending write out of "
        "the session and the whitelist approved a commit it could no longer see"
    )
    assert db.rolled_back and not db.committed


def test_every_pre_commit_check_runs_inside_the_suspension():
    """Read from the source, so it cannot drift from what the function does.

    The rule is not "some checks are contained". Any check left outside the
    ``with`` block is a check that can flush, and the whitelist runs last, so
    outside-the-block is upstream of the only guard that would notice.
    """
    import ast
    import inspect

    body = ast.parse(inspect.getsource(W.commit_guarded).lstrip()).body[0].body
    suspensions = [
        node
        for node in body
        if isinstance(node, ast.With)
        # The context manager must be ``_no_autoflush`` ITSELF, not merely some
        # ``with`` block. A block that keeps the shape and drops the suspension
        # is the exact mutation this is here to catch, and matching on any
        # ``with`` would sail past it.
        and any(
            isinstance(item.context_expr, ast.Call)
            and getattr(item.context_expr.func, "id", None) == "_no_autoflush"
            for item in node.items
        )
    ]
    assert suspensions, "commit_guarded no longer suspends the automatic flush at all"

    contained = ast.dump(suspensions[0])
    for check in ("cloud_sync_active", "assert_cloud_sync_readable", "assert_session_whitelisted"):
        assert check in contained, f"{check} runs outside the suspended-flush block"


# ── every refusal this module raises is in the reserved vocabulary ───────────


def _raised_reasons() -> set[str]:
    """Every reason slug this module raises, read from its own source.

    Derived by walking the syntax tree rather than by listing, because a test
    that enumerates is a test that misses the next refusal somebody adds (P3).
    """
    import ast
    import inspect

    reasons: set[str] = set()
    for node in ast.walk(ast.parse(inspect.getsource(W))):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        name = getattr(node.func, "id", None)
        first = node.args[0]
        if name == "_unavailable" and isinstance(first, ast.Constant):
            reasons.add(first.value)
        if name == "_running":
            reasons.add("rekordbox-running")
    return reasons


def test_every_refusal_this_module_raises_has_a_reserved_code_and_a_remedy():
    """S4 from the writer's side. U5 reserved them; this proves they are consumed.

    A refusal with no reserved code collapses to a bare status one hop
    downstream and cannot be recovered, which is the defect the whole cause type
    exists to prevent.
    """
    from cratekit.core.cause import REASONS
    from cratekit.core.exit_codes import ExitCode, meaning_of

    raised = _raised_reasons()
    assert raised, "the scan found no refusals at all, so it is not scanning"
    for reason in sorted(raised):
        assert reason in REASONS, f"{reason!r} is not a declared reason"
        assert REASONS[reason] is not ExitCode.OK
        assert meaning_of(REASONS[reason]).remedy is not None


def test_the_reserved_writer_vocabulary_is_actually_used():
    """Every condition U5 reserved a code for is raised by this module.

    The other direction of the same seam. A reserved code nothing raises is a
    promise that was never kept, and it looks identical to one that was.
    """
    from tests.test_cli_contract import WRITER_REFUSALS

    raised = _raised_reasons()
    unused = {slug for slug in WRITER_REFUSALS.values() if slug not in raised}
    assert not unused, f"reserved for the guarded writer but never raised: {sorted(unused)}"


def test_no_refusal_returns_a_bare_integer_or_raises_a_bare_exception():
    """Never a literal status, never an untyped error. Both are KTD25 failures.

    The source system documented its exit codes in a comment inside a CONSUMER
    while every producer wrote a bare integer, so nothing could detect a producer
    changing its code.
    """
    import inspect

    source = inspect.getsource(W)
    assert "RuntimeError(" not in source
    assert "SystemExit" not in source


# ── the soft-delete marker: read it, never default it ────────────────────────
#
# THREE TIMES ON ONE COLUMN. U18 removed the permissive default, U19 shipped it
# again and its review caught it as a blocking defect, and U21 shipped it a third
# time on the genre lookup at ``write/metadata.py:195``, where it reached main.
# That is not three careless authors, it is a rule that lived in a docstring.
# ``tests/_source_guards.py:permissive_soft_delete_reads`` is the rule as code and
# these are its fixtures, in both directions (P7).


def _source_guard():
    from tests import _source_guards

    return _source_guards


def test_the_soft_delete_guard_fires_on_every_evasion():
    """The literal, the indirection, the mapping row, and the named default.

    Each of these is a shape somebody reaches for when a guard is in the way, and
    a guard that recognizes only the first is one rename from being switched off.
    That is not hypothetical here: the armed copy of the comma-separated-writer
    question in this repository was defeated by ``import csv as spreadsheet``.
    """
    guard = _source_guard()
    fires = guard.permissive_soft_delete_reads

    assert fires('x = getattr(row, "rb_local_deleted", 0)'), "the shape that reached main"
    assert fires('x = getattr(row, "rb_local_deleted", False)')
    assert fires('x = getattr(row, "rb_local_deleted", None)'), (
        "bool(None) is the same permissive answer as 0, wearing a different word"
    )
    assert fires(
        'COLUMN = "rb_local_deleted"\nx = getattr(row, COLUMN, 0)\n'
    ), "the column named through a constant, which is one hop of indirection"
    assert fires(
        'ACTIVE = 0\nx = getattr(row, "rb_local_deleted", ACTIVE)\n'
    ), "the same evasion pointed at the default instead of at the column"
    assert fires(
        "from cratekit.core.rb_writer import SOFT_DELETE_COLUMN\n"
        "x = getattr(row, SOFT_DELETE_COLUMN, 0)\n"
    ), "correct spelling of the column, still a permissive read"
    assert fires(
        "from cratekit.core import rb_writer as w\n"
        "x = getattr(row, w.SOFT_DELETE_COLUMN, 0)\n"
    ), "an aliased module is what defeated the last guard in this repository"
    assert fires('def g(row):\n    return row.get("rb_local_deleted", 0)\n'), (
        "a row that arrived as a mapping"
    )
    assert fires('def g(row):\n    return row.get("rb_local_deleted")\n'), (
        "a one-argument get defaults to None all by itself, which is the "
        "permissive answer arrived at by omission rather than by decision"
    )
    assert fires(
        "import cratekit.core.rb_writer as W\n"
        "M = W\n"
        "x = getattr(row, M.SOFT_DELETE_COLUMN, 0)\n"
    ), (
        "an alias OF an alias. The previous version claimed one hop of "
        "indirection in both directions and that claim was false for a module "
        "alias at even one hop"
    )
    assert fires('x = getattr(row, "rb_local_deleted", int())'), (
        "zero written as a constructor call rather than as the digit"
    )
    assert fires('x = getattr(row, "rb_local_deleted", 1 - 1)'), "zero written as arithmetic"
    assert fires('x = getattr(row, "rb_local_deleted", "")'), "the empty string is falsey too"
    assert fires('pair = ("rb_local_deleted", 0)\nx = getattr(row, *pair)\n'), (
        "the arguments packed into a tuple and splatted back out"
    )


def test_the_soft_delete_guard_catches_a_read_laundered_one_line_later():
    """The routes that are correct AT THE CALL and permissive by the next statement.

    These matter more than the plain default, not less. The sentinel route is a
    SINGLE EDIT from the shape this repository sanctions, and it reads as somebody
    being careful: the sentinel is there, the comparison is there, and the branch
    quietly answers "active" instead of refusing. A guard that checked only the
    call site would certify it.

    The try route is what a person reaches for first, because "the attribute
    might not exist" is an AttributeError-shaped thought. The ternary is the same
    idea written shorter. To an analyzer all three are one question: does a name
    holding the marker get assigned something falsey in the same scope, or does
    the marker sit in a conditional whose other branch is falsey.
    """
    guard = _source_guard()
    fires = guard.permissive_soft_delete_reads

    assert fires(
        "_ABSENT = object()\n"
        "def read(row):\n"
        '    marker = getattr(row, "rb_local_deleted", _ABSENT)\n'
        "    if marker is _ABSENT:\n"
        "        marker = 0\n"
        "    return marker\n"
    ), "the sentinel taken and then thrown away, one edit from the correct shape"

    assert fires(
        "def read(row):\n"
        "    try:\n"
        "        marker = row.rb_local_deleted\n"
        "    except AttributeError:\n"
        "        marker = 0\n"
        "    return marker\n"
    ), "the shape somebody writes when the thought is 'it might not be there'"

    assert fires(
        'marker = row.rb_local_deleted if hasattr(row, "rb_local_deleted") else 0'
    ), "the same idea as a conditional expression"

    assert not fires(
        "_ABSENT = object()\n"
        "def read(row):\n"
        '    marker = getattr(row, "rb_local_deleted", _ABSENT)\n'
        "    if marker is _ABSENT:\n"
        "        raise Refused()\n"
        "    return marker\n"
    ), "the sanctioned shape must survive the launder check, or nothing can pass"

    # THE CONTROL THAT WAS INERT. This fixture used to write the read as
    # `return getattr(...)`, which is not an assignment, so `holders` stayed
    # empty and the assertion passed without exercising scoping at all. Written
    # as an assignment to `marker` it is the same shape the real readers use, and
    # against the previous `ast.walk` scoping it FAILS.
    assert not fires(
        "_ABSENT = object()\n"
        "def unrelated():\n"
        "    marker = 0\n"
        "    return marker\n"
        "def read(row):\n"
        '    marker = getattr(row, "rb_local_deleted", _ABSENT)\n'
        "    if marker is _ABSENT:\n"
        "        raise Refused()\n"
        "    return marker\n"
    ), (
        "two functions using the name 'marker' are not talking about one "
        "variable; scoping this file-wide fires on unrelated code"
    )


def test_the_soft_delete_guard_survives_an_unrelated_edit_to_the_files_it_protects():
    """The failure mode that ends a guard: firing on a one-line unrelated change.

    Not a constructed fixture. Both shipped readers assign the sanctioned read to
    a local named ``marker``, so this appends an ordinary helper that uses that
    name as a counter to each REAL file and asserts the guard stays quiet. Under
    the previous scoping, which yielded the module and then walked it, "module
    scope" was the whole file and both fired.

    A guard that goes red because somebody added an unrelated function to
    `metadata.py` is a guard that gets deleted by the third person it stops, and
    the column it protects is the one this repository has already got wrong three
    times.
    """
    guard = _source_guard()
    unrelated = (
        "\n\ndef _unrelated_counter(rows):\n"
        "    marker = 0\n"
        "    for _ in rows:\n"
        "        marker = marker + 1\n"
        "    return marker\n"
    )
    for path, source in _package_sources():
        if path not in SOFT_DELETE_READERS:
            continue
        assert not guard.permissive_soft_delete_reads(source), f"{path} is not clean"
        assert not guard.permissive_soft_delete_reads(source + unrelated), (
            f"appending a helper that uses the name 'marker' to {path} arms the "
            f"guard against the file it exists to protect"
        )


def test_the_soft_delete_guard_stays_quiet_on_correct_code():
    """The half that gets skipped, and the half that decides whether a guard survives.

    A guard that fires on correct code gets switched off, and this repository has
    already shipped that mistake once. Every shape here is a correct reader, and
    every one of them fails loudly or not at all rather than answering "active"
    for a row that never said so.
    """
    guard = _source_guard()
    fires = guard.permissive_soft_delete_reads

    assert not fires(
        "_ABSENT = object()\n"
        'marker = getattr(row, "rb_local_deleted", _ABSENT)\n'
        "if marker is _ABSENT or marker is None:\n"
        "    raise Refused()\n"
    ), "the sanctioned shape: a sentinel the caller then compares against"
    assert not fires('marker = getattr(row, "rb_local_deleted")'), (
        "no default at all raises AttributeError, which is loud, not permissive"
    )
    assert not fires("marker = row.rb_local_deleted"), "a plain attribute access"
    assert not fires('SOFT_DELETE_COLUMN = "rb_local_deleted"'), (
        "defining the column is not reading it, or the module that owns the "
        "name would have to be carved out of its own guard"
    )
    assert not fires('columns = {"rb_local_deleted", "usn"}'), "naming it in a set"
    assert not fires('x = getattr(row, "rb_local_synced", 0)'), (
        "a different bookkeeping column entirely, which this guard has no "
        "opinion about"
    )
    assert not fires('x = getattr(row, "rb_local_deleted", SENTINEL)'), (
        "an unresolvable name is not assumed permissive; assuming it would fire "
        "on the correct shape whenever the sentinel is imported"
    )
    assert not fires(
        "import cratekit.core.rb_writer as W\n"
        "COLUMN_TYPES = {}\n"
        "def kind():\n"
        "    return COLUMN_TYPES.get(W.SOFT_DELETE_COLUMN)\n"
    ), (
        "a per-column lookup table asked about this column is not a row read, "
        "and this repository already ships BOOKKEEPING_COLUMNS and "
        "GRIDLESS_ON_CREATE_COLUMNS, so it is the in-house shape most likely to "
        "arm the guard against correct code"
    )
    assert not fires(
        'COLUMN = "rb_local_deleted"\n'
        "LABELS = {}\n"
        "def label():\n"
        '    return LABELS.get(COLUMN, "")\n'
    ), "the same table reached through the named constant"
    assert not fires('line = f"deleted={row.rb_local_deleted}" if row else ""'), (
        "an ordinary summary string. The conditional rule fired on any ternary "
        "with the column on one side and a falsey literal on the other; what "
        "makes the real shape a defect is that the CONDITION is about whether "
        "the column is there"
    )


def test_the_lookup_table_exclusion_recognizes_this_repository_s_own_style():
    """A guard that misses the house style fires on the house.

    `MappingProxyType({...})` is how this package freezes a per-column table, and
    all nineteen uses of it here are the BARE IMPORTED NAME, six of them in
    `write/metadata.py`, which is a declared soft-delete reader. The exclusion
    matched only the dotted `types.MappingProxyType(...)` form, which this
    repository never writes, so it named the house style in its own comment and
    then did not recognize it.

    Driven against the REAL reader rather than a fixture, because that is where
    it fired.
    """
    guard = _source_guard()
    table = (
        "\n\nSOFT_DELETE_LABEL: Mapping[str, str] = MappingProxyType(\n"
        '    {rb_writer.SOFT_DELETE_COLUMN: "tombstoned"}\n)\n\n'
        "def _label_for_soft_delete() -> str:\n"
        '    return SOFT_DELETE_LABEL.get(rb_writer.SOFT_DELETE_COLUMN, "")\n'
    )
    for path, source in _package_sources():
        if path != "src/cratekit/write/metadata.py":
            continue
        assert not guard.permissive_soft_delete_reads(source + table), (
            "a frozen per-column table written the way this repository writes "
            "every one of them arms the guard against a declared reader"
        )
        break
    else:  # pragma: no cover - the corpus must contain the reader
        raise AssertionError("write/metadata.py is not in the corpus")


def test_the_lookup_table_exclusion_is_scope_aware_not_just_name_keyed():
    """Shadowing, driven. The previous test claimed this and did not exercise it.

    It used `row = None` at module level, which is excluded for a DIFFERENT
    reason, that it is not a container, so it passed without a shadowing case
    anywhere in it. A module-level `row = {}` IS a container, and the exclusion
    was keyed on the name alone, so it silenced `row.get(SOFT_DELETE_COLUMN, 0)`
    inside every function whose PARAMETER is named `row`. Round 3 narrowed the
    evasion from any binding to any container-shaped binding; it did not close
    it.

    A name a scope binds itself is not the module-level name it happens to spell
    the same way, and Python agrees.
    """
    guard = _source_guard()
    fires = guard.permissive_soft_delete_reads
    assert fires(
        'COLUMN = "rb_local_deleted"\n'
        "row = {}\n"
        "def read(row):\n"
        "    return row.get(COLUMN, 0)\n"
    ), "a parameter shadows the module-level table of the same name"
    assert fires(
        'COLUMN = "rb_local_deleted"\n'
        "row = dict(fetch_one())\n"
        "def read(row):\n"
        "    return row.get(COLUMN, 0)\n"
    ), "a dict() call over a row is still a row to every caller of it"
    assert fires(
        'COLUMN = "rb_local_deleted"\n'
        "row = {}\n"
        "def read(rows):\n"
        "    row = rows[0]\n"
        "    return row.get(COLUMN, 0)\n"
    ), "an assignment shadows it as surely as a parameter does"
    assert not fires(
        'COLUMN = "rb_local_deleted"\n'
        "LABELS = {}\n"
        "def label():\n"
        '    return LABELS.get(COLUMN, "")\n'
    ), "a table nothing shadows is still a table"


def test_the_launder_rules_reach_a_class_body_and_a_nonlocal_rebinding():
    """Two blind spots the scope fix opened, both of which fired before it.

    `_own_nodes` stops at every scope boundary, which is what made scoping
    correct, but `_scopes` yielded only functions and the module. So no scope
    ever walked a CLASS BODY and the launder rules could not see a statement
    written directly in a class. Adding `ClassDef` restores it without
    reintroducing the false positive, because a class body is genuinely its own
    scope.

    And a nested function declaring `nonlocal marker` rebinds the OUTER
    variable. `_own_nodes` stops at that function, so the overwrite was invisible
    from the enclosing scope while the nested scope held no marker of its own,
    and the launder was unseen in both. Python's semantics say it is one
    variable, so the walk follows the declaration rather than the indentation.
    """
    guard = _source_guard()
    fires = guard.permissive_soft_delete_reads

    assert fires(
        "_ABSENT = object()\n"
        "class Reader:\n"
        '    marker = getattr(_row, "rb_local_deleted", _ABSENT)\n'
        "    marker = 0\n"
    ), "a class body is a scope, and nothing was walking it"

    assert fires(
        "_ABSENT = object()\n"
        "def outer(row):\n"
        '    marker = getattr(row, "rb_local_deleted", _ABSENT)\n'
        "    def clean():\n"
        "        nonlocal marker\n"
        "        marker = 0\n"
        "    clean()\n"
        "    return marker\n"
    ), "nonlocal rebinds the outer variable; the indentation says otherwise"

    assert not fires(
        "_ABSENT = object()\n"
        "def outer(row):\n"
        '    marker = getattr(row, "rb_local_deleted", _ABSENT)\n'
        "    def unrelated():\n"
        "        marker = 0\n"
        "        return marker\n"
        "    return marker\n"
    ), (
        "without a nonlocal declaration the inner name is a new variable, and "
        "firing on it is the whole false positive the scope fix removed"
    )


def test_a_conditional_defaulting_the_marker_fires_and_a_summary_string_does_not():
    """The kept branch must BE the read, which is not the same as containing it.

    Gating on the TEST killed one false positive and gave up five real shapes
    with it. `deleted = row.rb_local_deleted if row else False` is the defect
    class exactly, a missing row read as active, and the test names no column so
    it went silent. Requiring the branch to be the read itself keeps the summary
    string silent, because there the branch is a formatted string that merely
    quotes the value.
    """
    guard = _source_guard()
    fires = guard.permissive_soft_delete_reads
    assert fires("deleted = row.rb_local_deleted if row else False")
    assert fires('marker = row.rb_local_deleted if hasattr(row, "rb_local_deleted") else 0')
    assert fires('marker = 0 if not row else row.rb_local_deleted')
    assert not fires('line = f"deleted={row.rb_local_deleted}" if row else ""'), (
        "an ordinary summary string quoting the value is not a defaulted read"
    )


def test_a_presence_flag_is_not_a_marker_holder():
    """`hasattr` binds a boolean about the column, not the column's value.

    It became a recognized read so the conditional rule could see the shape it
    is the condition of, and that made `present = hasattr(row, COL)` followed by
    `present = False` look like a laundered marker. It is somebody tracking
    their own flag.

    The widening it DID cause is intended and is not walked back: a module doing
    only a presence test now counts as a reader against the exact-membership pin,
    because asking whether the column is there is being in this conversation.
    """
    guard = _source_guard()
    assert not guard.permissive_soft_delete_reads(
        'COLUMN = "rb_local_deleted"\n'
        "def read(row):\n"
        "    present = hasattr(row, COLUMN)\n"
        "    present = False\n"
        "    return present\n"
    )
    assert guard.reads_soft_delete_marker(
        'COLUMN = "rb_local_deleted"\n'
        "def read(row):\n"
        "    return hasattr(row, COLUMN)\n"
    ), "a presence test is a read for the purposes of the reader pin"


def test_the_lookup_table_exclusion_is_not_an_evasion_route():
    """A row is not a dict literal, and the earlier test could not tell.

    The exclusion that stops `COLUMN_TYPES.get(...)` firing was keyed on the NAME
    being bound at module level, with no test of what it was bound TO. So one
    module-level `row = fetch_one()` bought silence for every `row.get(COL, 0)`
    below it, and two genuine false positives had been traded for a one-line
    evasion. The binding must now be a container literal.
    """
    guard = _source_guard()
    fires = guard.permissive_soft_delete_reads
    assert fires(
        'COLUMN = "rb_local_deleted"\n'
        "row = fetch_one()\n"
        "def read():\n"
        "    return row.get(COLUMN, 0)\n"
    ), "a module-level row is still a row"
    assert fires(
        'COLUMN = "rb_local_deleted"\n'
        "row = None\n"
        "def read(row):\n"
        "    return row.get(COLUMN, 0)\n"
    ), "a module-level name shadowed by a parameter is not a lookup table either"


@pytest.mark.parametrize(
    ("label", "body"),
    (
        ("plain assignment", "    TABLE = rows[0]\n    return TABLE.get(COLUMN, 0)\n"),
        ("tuple unpacking", "    TABLE, meta = rows[0]\n    return TABLE.get(COLUMN, 0)\n"),
        (
            "nested unpacking",
            "    (a, [TABLE, b]) = rows[0]\n    return TABLE.get(COLUMN, 0)\n",
        ),
        ("with as", "    with rows as TABLE:\n        return TABLE.get(COLUMN, 0)\n"),
        ("for target", "    for TABLE, _ in rows:\n        return TABLE.get(COLUMN, 0)\n"),
        (
            "except as",
            "    try:\n        pass\n"
            "    except ValueError as TABLE:\n        return TABLE.get(COLUMN, 0)\n",
        ),
    ),
)
def test_every_way_of_shadowing_a_lookup_table_still_fires(label, body):
    """The exclusion is only as good as the ways it knows a name can be bound.

    A real per-column lookup table at module level is excused, correctly. The
    evasion is to spell a local by the same name and read a real row off it, and
    `_local_names` recognized exactly one spelling of that, the bare assignment.
    Measured on 2026-09-10: tuple unpacking, `with ... as`, a tuple `for` target
    and `except ... as` were each silent while the plain form fired, so the
    exclusion swallowed a permissive read through four routes the two tests
    above claimed were closed.

    Parametrized rather than written as one row with four asserts, because a
    single row stops at its first failure and would report one open route while
    three others stayed hidden.
    """
    guard = _source_guard()
    source = 'COLUMN = "rb_local_deleted"\nTABLE = {}\ndef read(rows):\n' + body
    assert guard.permissive_soft_delete_reads(source), (
        f"{label} shadows the module-level table with a real row, and the read "
        f"was excused as a per-column lookup"
    )


def test_a_genuine_module_level_lookup_table_is_still_excused():
    """The control the row above is worthless without.

    Widening `_local_names` until everything fires would pass every row in that
    parametrization and destroy the exclusion, which exists because this
    repository writes `COLUMN_TYPES.get(SOFT_DELETE_COLUMN)` for real and a guard
    that fires on the code most likely to be correct is a guard somebody deletes.
    """
    guard = _source_guard()
    assert not guard.permissive_soft_delete_reads(
        'COLUMN = "rb_local_deleted"\n'
        "COLUMN_TYPES = {}\n"
        "def kind():\n"
        "    return COLUMN_TYPES.get(COLUMN, 0)\n"
    ), "a per-column lookup table is not a row and must stay excused"


def test_no_module_in_the_package_reads_the_soft_delete_marker_permissively():
    """The guard, armed over every module we author. This is the assertion.

    Walked rather than aimed at the two modules known to read the column, because
    a check that names its targets is blind to the third one, and the third one is
    always the defect.
    """
    guard = _source_guard()
    offenders: dict[str, list[str]] = {}
    for path, source in _package_sources():
        found = guard.permissive_soft_delete_reads(source)
        if found:
            offenders[path] = found
    assert not offenders, (
        f"a soft-deleted row would read as active in: {offenders}. The column is "
        f"bookkeeping, so a binding that stops exposing it applies this default "
        f"to every row at once and nothing reports it."
    )


#: EXACT MEMBERSHIP, which is the only shape that catches a widening (R-15). The
#: assertion above says what must not happen; this says who is allowed to be in
#: the conversation at all, and a fourth reader is a two-line diff that passes
#: every other assertion in this suite.
#:
#: IT IS ALSO THE RECONCILIATION MECHANISM, and the mechanism is not the one an
#: earlier version of this comment claimed. U24 lands
#: ``trees.soft_delete_marker`` as the single sanctioned implementation AND moves
#: `routing_pass`'s direct read into it, so `routing_pass` drops OUT of this set
#: while `trees` comes in. Simulated against that tree the pin goes from two
#: readers to a DIFFERENT two, not from two to three. It still goes red, by set
#: inequality rather than by growth, so the outcome the pin exists for is intact
#: and the merge cannot quietly leave two implementations of one rule in the
#: tree. The reason is corrected here because a pin whose stated mechanism is
#: wrong is a pin somebody deletes when it fires the way it was not described.
#:
#: RE-PINNED AT THE U59 MERGE, AND THE PREDICTION ABOVE HELD EXACTLY. The set is
#: differenced against the merged tree rather than adjusted to match a count.
#: ``routing_pass`` left, because its direct read is now
#: ``trees.soft_delete_marker(row)`` at ``routing_pass.py:695``. ``trees`` joined,
#: because it holds that single sanctioned implementation at ``trees.py:204``.
#: Two readers before, two after, a different two, which is the set inequality
#: the pin was built to catch rather than a growth check that would have missed
#: it. The third member the raw measurement reported,
#: ``tests/test_adopt_collection.py``, was NOT admitted: it defines
#: ``self.rb_local_deleted`` on a stand-in row and reads it nowhere, and
#: ``_soft_delete_reads`` was narrowed to load context so a row double stops
#: counting as a reader.
#:
#:
#: RE-PINNED AT R-758, AS A DECISION, and the count stays at two. The read moved
#: DOWN a layer: ``core/rb_writer`` joined and ``write/trees`` left. A membership
#: can now be removed, so the membership primitives have to read the marker, and
#: they live below ``trees`` and cannot reach up to its reader. Rather than a
#: third copy, ``rb_writer.soft_deleted`` holds the one read and the one
#: refusal, and ``trees.soft_delete_marker``, ``rb_writer.membership_removed``
#: and ``rb_writer.node_removed`` each supply the words for their kind of row.
#: The first version of this unit added a second reader beside the first and
#: the built in review named it.
SOFT_DELETE_READERS = {
    "src/cratekit/core/rb_writer.py",
    "src/cratekit/write/metadata.py",
}


def test_defining_the_marker_on_a_row_double_is_not_reading_it():
    """The narrowing, driven from both sides, because one side alone proves nothing.

    A stand-in row assigns the attribute and is not a reader; anything that takes
    the value back out is. Both halves are asserted here, so reverting the load
    context test kills this row rather than quietly re-admitting every fixture in
    the tree into the membership pin above.

    The write shape is not invented. It is what ``tests/test_adopt_collection.py``
    does at line 187, and it is the shape every stand-in row here is built from.
    """
    guard = _source_guard()
    assert not guard.reads_soft_delete_marker(
        "class Row:\n"
        "    def __init__(self, deleted):\n"
        "        self.rb_local_deleted = deleted\n"
    ), "a row double DEFINING the column is a fixture, not a place the rule lives"
    assert guard.reads_soft_delete_marker(
        "def read(row):\n    return row.rb_local_deleted\n"
    ), "taking the value back out is a read, and narrowing must not have lost it"


def test_only_the_declared_modules_read_the_soft_delete_marker_at_all():
    guard = _source_guard()
    readers = {
        path for path, source in _package_sources() if guard.reads_soft_delete_marker(source)
    }
    assert readers == SOFT_DELETE_READERS, (
        f"the modules reading the soft-delete marker are {sorted(readers)}, and "
        f"the pin declares {sorted(SOFT_DELETE_READERS)}. Every reader is a place "
        f"the rule has to be got right again, so adding one is a decision rather "
        f"than a diff."
    )


def _package_sources() -> list[tuple[str, str]]:
    """Every module we author: the package, the scripts, and the test tree.

    NOT JUST ``src``. A permissive read in a script or a test helper is a
    permissive read, and the whole reason this guard exists is that the rule kept
    being reimplemented by whoever needed it next. `scripts/` reads the registers
    and `tests/` builds row doubles, so both are places somebody writes
    `getattr(row, ..., 0)` without thinking of themselves as writing product
    code. None exists in either today, which is the moment to arm it.

    The vendored downloader is excluded. It is not ours to restyle and knows
    nothing about rekordbox; holding it to a rule written after it was published
    would only produce a suppression comment somebody later reads as permission.
    """
    repo = Path(W.__file__).resolve().parent.parent.parent.parent
    trees = [repo / "src" / "cratekit", repo / "scripts", repo / "tests"]
    return [
        (path.relative_to(repo).as_posix(), path.read_text())
        for root in trees
        if root.is_dir()
        for path in sorted(root.rglob("*.py"))
        if "_vendor" not in path.parts
    ]
