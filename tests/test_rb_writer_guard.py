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
    """New content rows mean new-track intake, and intake stays in XML.

    The reason is R15's safety chain: an XML import is something the user
    performs, reviews, and can undo from rekordbox. A row conjured into the
    database directly is none of those things.
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
    monkeypatch.setattr(W, "read_installed_app_version", lambda: "7.3.0.0001")
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_app_version()
    message = str(excinfo.value)
    assert "7.3.0.0001" in message and str(W.pinned_app_version()) in message


def test_app_version_pin_passes_on_match(monkeypatch):
    monkeypatch.setattr(W, "read_installed_app_version", lambda: W.pinned_app_version())
    W.assert_app_version()  # no raise


def test_app_version_pin_skips_when_app_not_found(monkeypatch):
    """A missing application warns and continues; the schema pin still guards.

    Refusing here would break every headless and CI run for no safety gain: if
    the application is not installed, it cannot be holding the database open.
    """
    monkeypatch.setattr(W, "read_installed_app_version", lambda: None)
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
    """
    library = tmp_path / "library"
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    unpinned = config.from_dict(valid_data(library))
    assert unpinned.rekordbox.pinned_app_version is None

    monkeypatch.setattr(config, "load", lambda *args, **kwargs: unpinned)
    monkeypatch.setattr(W, "read_installed_app_version", lambda: "7.2.14.0323")

    with pytest.raises(config.ConfigInvalid, match="pinned_app_version"):
        W.assert_app_version()


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
    monkeypatch.setattr(W, "read_installed_app_version", lambda: "9.9.9.0001")
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
    monkeypatch.setattr(W, "read_installed_app_version", lambda: installed)
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_app_version()
    assert excinfo.value.cause.reason == "app-version-pin-drift"


def test_a_drifted_pin_can_be_forced_for_a_deliberate_revalidation(tmp_path, monkeypatch):
    """The escape stays, stays loud, and stays off by default."""
    _pinned_config(
        tmp_path, monkeypatch, pinned_app_version="9.9.9.0001", validated_on="2026-08-01"
    )
    monkeypatch.setattr(W, "read_installed_app_version", lambda: "9.9.9.0002")
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
    monkeypatch.setattr(W, "read_installed_app_version", lambda: "9.9.9.0002")
    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_app_version()
    assert excinfo.value.cause.detail["validated_on"] == "2026-08-01"
    assert W.pin_validated_on() == "2026-08-01"


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
    assert excinfo.value.cause.reason == "cloud-sync-active"


def test_the_unknown_refusal_has_a_named_escape(monkeypatch):
    """Because unknown is the ordinary state on a machine that has never run
    rekordbox, and a refusal with no way past it is a lockout."""

    def unreadable(*args, **kwargs):
        raise OSError("nothing to read")

    monkeypatch.setattr(W, "read_rekordbox_settings", unreadable)
    W.assert_cloud_sync_readable(force=True)  # no raise


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
    assert W.guard_violations([], [("djmdContent", set(W.BOOKKEEPING_COLUMNS))], []) == []


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
