"""U35: the standalone utilities, the backup age fact, and the verb declarations.

Each of the plan's five scenarios has a test named after it. Everything runs in
a temporary directory with the process probe and the command runner injected;
the one exception is the mastering round trip, which encodes real audio with
ffmpeg, since a safety proof that stubs the encoder proves nothing about it.
"""

from __future__ import annotations

import ast
import json
import re
import shutil
import stat
import subprocess
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit.core import backup_facts, config, profiles
from cratekit.core.naming import MarkerRule, NameTemplate
from cratekit.core.taxonomy import default_taxonomy
from cratekit.modules import tools
from cratekit.modules.tools import backup, mastering, setbuilder

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_ROOT = REPO_ROOT / "src"

UTC = timezone.utc


# ── Fixtures ─────────────────────────────────────────────────────────────────


@contextmanager
def _open_gates():
    """A destructive-session guard that is already satisfied."""
    yield None


def open_gates():
    """The gates seam, injected wherever a test is asserting something else.

    The residual
    "The backup restore is not yet bound to the destructive-session gates"
    binds the library lock, the backup acknowledgment and the volume identity
    assertion to a restore. Those need a real volume identity and a person's
    recorded acknowledgment, neither of which belongs in a test about the ORDER
    the sidecars are cleared in. Injecting the seam here is what keeps this file
    hermetic while the gate itself is asserted, with the real guard restored, in
    the tests further down that exist for it.
    """
    return _open_gates()


@pytest.fixture
def library(tmp_path, monkeypatch):
    """A synthetic library root, aligned with the suite's isolation fixture."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    # A library holds its music: an empty folder at the root is what an
    # unmounted volume leaves, and a backup now refuses it.
    (root / "Music" / "fixture.flac").write_bytes(b"one track")
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library):
    """A validated config naming the synthetic library and a synthetic remote."""
    return _config(library, backup={
        "remote": "remote", "dest": "remote:mirror", "archive_root": "remote:mirror-archive",
        "db_dest_root": "remote:database-snapshots",
    })


def _config(library, **sections):
    """A validated slim config over ``library``, with any further sections given."""
    return config.from_dict({
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(library), "volume_id": "F1E2-D3C4",
            "db_path": str(library / "db" / "master.db"),
        },
        "paths": {"download_staging": str(library.parent / "staging")},
        "profile": {"name": "slim"},
        **sections,
    })


@pytest.fixture
def rclone(tmp_path, monkeypatch):
    """A stub rclone that resolves through the binaries override."""
    fake = tmp_path / "bin" / "rclone"
    fake.parent.mkdir(parents=True, exist_ok=True)
    fake.write_text("#!/bin/sh\nexit 0\n")
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("CRATEKIT_BIN_RCLONE", str(fake))
    return fake


class Recorder:
    """A runner that records commands and answers with a canned result."""

    def __init__(self, *, stdout_for=None, fail_labels=(), absent_labels=()):
        self.commands = []
        self.stdout_for = dict(stdout_for or {})
        self.fail_labels = set(fail_labels)
        # Answered with rclone's directory not found exit rather than a failure.
        self.absent_labels = set(absent_labels)

    def __call__(self, command):
        self.commands.append(command)
        rc = (
            backup.RCLONE_DIRECTORY_NOT_FOUND if command.label in self.absent_labels
            else 1 if command.label in self.fail_labels
            else 0
        )
        return backup.CommandResult(returncode=rc, stdout=self.stdout_for.get(command.label, ""))

    def labels(self):
        return [c.label for c in self.commands]


def snapshot_listing(cfg, *sidecar_suffixes, extra=()):
    """Stdout for a snapshot that holds the database and the named sidecars."""
    database = config.state_path("rekordbox_db", cfg).name
    names = [database, *extra]
    names.extend(database + suffix for suffix in sidecar_suffixes)
    return "".join(name + "\n" for name in names)


def _restore(cfg, **kwargs):
    """``plan_restore`` confirmed, with nothing running and the gates seam open."""
    defaults = {"confirmed": True, "process_lister": no_processes, "gates": open_gates}
    return backup.plan_restore(cfg, **{**defaults, **kwargs})


def _restore_refused(cfg, **kwargs) -> backup.BackupRefused:
    """The ``BackupRefused`` a ``_restore`` raises."""
    with pytest.raises(backup.BackupRefused) as excinfo:
        _restore(cfg, **kwargs)
    return excinfo.value


def _record(cfg, portion: str, completed_at, destination):
    """One completed portion on record, through ``backup_facts.record``."""
    portion = getattr(backup_facts.Portion, portion)
    return backup_facts.record(cfg, portion, completed_at=completed_at, destination=destination)


def _scratch(cfg, tmp_path):
    """A scratch restore target whose database folder exists."""
    target = tmp_path / "scratch"
    backup.database_target_for(cfg, target).parent.mkdir(parents=True, exist_ok=True)
    return target


def _listing(cfg, *sidecar_suffixes, extra=(), identity=None, **kwargs):
    """A ``Recorder`` whose snapshot holds the database, the named sidecars and ``identity``."""
    listed = snapshot_listing(cfg, *sidecar_suffixes, extra=extra)
    stdout_for = {backup.LIST_SNAPSHOT_CONTENTS: listed}
    if identity is not None:
        stdout_for[backup.LIST_SNAPSHOT_IDENTITY] = identity
    return Recorder(stdout_for=stdout_for, **kwargs)


def no_processes():
    return ()


def rekordbox_running():
    return ("rekordbox", "rekordboxAgent", "Finder")


# ── The verb declarations U5 consumes ────────────────────────────────────────


def test_every_feature_inventory_row_this_unit_owns_has_a_verb():
    """Rows 29, 30 and 31, one verb each."""
    assert tools.VERB_NAMES == ("setbuild", "master", "backup.run")


def test_every_verb_names_a_real_toggle_that_slim_leaves_off_and_full_turns_on():
    """A verb whose toggle is not a module cannot be switched off; all three rows are Module."""
    slim, full = profiles.resolve("slim").modules, profiles.resolve("full").modules
    for spec in tools.VERBS:
        assert spec.feature in profiles.MODULES, f"{spec.name}'s toggle is not a declared module"
        assert spec.feature not in slim
        assert spec.feature in full


def test_the_extras_group_is_derived_and_is_none_for_all_three():
    """None is the ANSWER here, not a gap."""
    for spec in tools.VERBS:
        assert spec.extras is None
        assert spec.extras == profiles.install_command(spec.feature)
    assert tools.verb("master").binaries == ("ffmpeg", "ffprobe")
    assert tools.verb("backup.run").binaries == ("rclone",)


def test_the_verb_table_holds_no_imported_object():
    """KTD7: the registry entries stay inert so the import stays lazy."""
    for spec in tools.VERBS:
        assert isinstance(spec.module, str)
    source = (SRC_ROOT / "cratekit" / "modules" / "tools" / "__init__.py").read_text()
    imported = {
        node.module
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.ImportFrom) and node.module
    }
    assert not any(m.startswith("cratekit.modules.tools.") for m in imported), "not lazy"


def test_the_backup_verb_is_marked_destructive():
    """KTD24: the gates bind to anything that can destroy user data."""
    assert tools.verb("backup.run").destructive is True
    assert tools.verb("setbuild").destructive is False


def test_every_declared_verb_is_in_the_static_registry():
    """Armed when U5 landed, which is why these verbs carry the registry's names."""
    import cratekit.cli.registry as registry

    registered = set(registry.VERB_NAMES)
    missing = set(tools.VERB_NAMES) - registered
    assert not missing, f"these verbs ship but are not registered: {sorted(missing)}"


def test_the_destructive_verb_is_wired_to_the_destructive_session_gates():
    """KTD24 and R38, armed now that the session boundary has landed.

    The residual
    "The backup restore is not yet bound to the destructive-session gates" is the
    one this drives.

    A backup restore replaces a live database and its sidecars while writing no
    database row, so a rule binding the gates to database writes alone would
    leave it outside the entire safety spine.

    The check is on THIS unit's source rather than on U8's API, because what had
    to change is here: U8 provides the gates, and the destructive verb declared
    here goes through them. The behavioural half, driving a restore into a gate
    refusal, is in ``tests/test_write_session.py``.
    """
    source = (SRC_ROOT / "cratekit" / "modules" / "tools" / "backup.py").read_text()
    tree = ast.parse(source)
    imports_session = any(
        (isinstance(node, ast.ImportFrom) and (node.module or "").startswith("cratekit.core"))
        and any(alias.name == "session" for alias in node.names)
        or (isinstance(node, ast.Import) and any(a.name == "cratekit.core.session" for a in node.names))
        for node in ast.walk(tree)
    )
    assert imports_session, "cratekit.core.session has landed"
    assert any(
        isinstance(node, ast.Attribute) and node.attr.startswith("assert_")
        for node in ast.walk(tree)
    ), "the session module is imported but no gate is asserted"


def test_every_refusal_cause_has_a_reserved_exit_code():
    """S4 applied to this unit: a refusal with no reserved code is a bare status."""
    import cratekit.cli.exit_codes as exit_codes

    reserved = set(exit_codes.RESERVED_CAUSES)
    causes = (
        {c.value for c in backup.REFUSALS}
        | {c.value for c in mastering.Refusal}
        | {c.value for c in backup_facts.Remedy}
    )
    assert causes <= reserved, f"unreserved causes: {sorted(causes - reserved)}"


# ── Scenario 1: the set builder, from a snapshot index, no network, no write ───

TEMPLATE = NameTemplate(markers=(MarkerRule(field="lossy", literal="[MP3]"),))


def track(artist, title, key, bpm=124.0, genre="Deep House", energy=5, vox=None, path=""):
    return setbuilder.Track(
        artist=artist, title=title, key=setbuilder.canonical_key(key), bpm=bpm, genre=genre,
        energy=energy, vox=vox, voxgender=None, match=setbuilder.match_key(artist, title),
        path=path,
    )


@pytest.fixture
def snapshot_index():
    """A frozen index. Every track is owned by construction, which is the point."""
    return (
        track("Alder", "Anchor Work", "8A", 124.0, energy=6),
        track("Birch", "Same Key Lower", "8A", 124.0, energy=4),
        track("Cedar", "Neighbour Up", "9A", 125.0, energy=8),
        track("Deodar", "Relative Major", "8B", 123.0, energy=6),
        track("Elm", "Energy Boost", "10A", 124.0, energy=9),
        track("Fir", "Diagonal", "9B", 124.0, energy=3),
        track("Gum", "Wrong Key", "3B", 124.0, energy=5),
        track("Hazel", "Right Key Wrong Tempo", "8A", 100.0, energy=5),
    )


def test_the_set_builder_produces_a_sequence_from_a_snapshot_index(snapshot_index):
    """The plan's first scenario, asserted on all three of its clauses."""
    plan = setbuilder.build_set("Alder - Anchor Work", snapshot_index, taxonomy=default_taxonomy())

    assert plan.anchor.owned is True
    assert plan.anchor.key == "8A"
    assert plan.sequence, "no sequence was produced for an owned anchor"
    assert plan.pool, "no companions were produced for an owned anchor"

    # Every recommendation came out of the index. This is the grounding rule, and
    # it is asserted at the output boundary rather than trusted mid-pipeline.
    owned = {t.match for t in snapshot_index}
    for scored in plan.pool + plan.sequence:
        assert scored.track.match in owned

    # The anchor is never its own companion.
    assert all(s.track.match != plan.anchor.track.match for s in plan.pool)


def test_the_set_builder_writes_nothing_and_always_gives_the_same_answer(tmp_path, snapshot_index):
    """"No write" and determinism, as assertions rather than promises."""
    before = sorted(p.name for p in tmp_path.rglob("*"))
    first = setbuilder.build_set("Alder - Anchor Work", snapshot_index, taxonomy=default_taxonomy())
    assert sorted(p.name for p in tmp_path.rglob("*")) == before
    second = setbuilder.build_set(
        "Alder - Anchor Work", tuple(reversed(snapshot_index)), taxonomy=default_taxonomy()
    )
    assert [s.track.match for s in first.pool] == [s.track.match for s in second.pool]


def test_the_wrong_key_and_the_right_key_at_the_wrong_tempo_never_enter_the_pool(snapshot_index):
    """Harmonic compatibility alone is not compatibility."""
    anchor = setbuilder.resolve_anchor("Alder - Anchor Work", snapshot_index)
    pool = {t.match for t, _ in setbuilder.build_pool(anchor, snapshot_index)}
    assert setbuilder.match_key("Gum", "Wrong Key") not in pool
    assert setbuilder.match_key("Hazel", "Right Key Wrong Tempo") not in pool


def test_the_band_holds_half_and_double_time_and_drops_when_the_anchor_has_no_tempo():
    """A key-only pool is a real answer; excluding everything is not."""
    assert setbuilder.in_band(62.0, 124.0)
    assert setbuilder.in_band(248.0, 124.0)
    assert not setbuilder.in_band(100.0, 124.0)
    assert setbuilder.in_band(90.0, None)
    assert not setbuilder.in_band(None, 124.0)


@pytest.mark.parametrize(
    "code, tier",
    [("8A", "perfect"), ("9A", "perfect"), ("7A", "perfect"), ("8B", "perfect"), ("10A", "boost"),
     ("6A", "wider"), ("11A", "wider"), ("7B", "wider"), ("9B", "wider")],
)
def test_the_camelot_tiers_are_the_ported_ones(code, tier):
    assert setbuilder.compatible_keys("8A")[code] == tier


def test_the_wheel_wraps_at_twelve():
    tiers = setbuilder.compatible_keys("12A")
    assert tiers["1A"] == "perfect"
    assert tiers["2A"] == "boost"


@pytest.mark.parametrize("code", ["0A", "13A", "99B", "", "8C", "Am"])
def test_an_off_wheel_key_is_rejected_rather_than_normalized(code):
    """The drift this port removes."""
    assert setbuilder.canonical_key(code) == ""
    assert setbuilder.compatible_keys(code) == {}


def test_an_unowned_anchor_with_no_key_is_unresolved_rather_than_guessed(snapshot_index):
    """No network call ships here, so an unowned anchor asks rather than invents."""
    absent = "Nobody - Not In The Library"
    plan = setbuilder.build_set(absent, snapshot_index, taxonomy=default_taxonomy())
    assert plan.anchor.unresolved
    assert plan.pool == () and plan.sequence == ()

    taxonomy = default_taxonomy()
    plan = setbuilder.build_set(absent, snapshot_index, taxonomy=taxonomy, key="8A", bpm=124.0)
    assert plan.anchor.owned is False
    assert plan.anchor.key_needs_confirming is True
    assert plan.pool


def test_the_web_lookup_is_a_seam_that_is_absent_by_default(snapshot_index):
    """The affordance survives; the network call does not ship."""
    calls = []

    def lookup(artist, title):
        calls.append((artist, title))
        return {"key": "8A", "bpm": 124}

    setbuilder.build_set("Nobody - Absent", snapshot_index, taxonomy=default_taxonomy())
    assert calls == []

    taxonomy = default_taxonomy()
    plan = setbuilder.build_set(
        "Nobody - Absent", snapshot_index, taxonomy=taxonomy, web_lookup=lookup
    )
    assert calls == [("", "Nobody - Absent")]
    assert plan.anchor.key == "8A"


def test_the_vocal_threshold_is_a_parameter_and_never_imported():
    """D7, asserted twice: by behaviour, and structurally."""
    assert setbuilder.vocal_score(9, 9, threshold=None) == 0.7
    assert setbuilder.vocal_score(9, 9, threshold=5) == 0.3
    assert setbuilder.vocal_score(9, 1, threshold=5) == 1.0
    # The clash the signal exists to avoid: two lead vocals at once.
    assert setbuilder.vocal_score(8, 8, threshold=5) < setbuilder.vocal_score(8, 2, threshold=5)

    source = (SRC_ROOT / "cratekit" / "modules" / "tools" / "setbuilder.py").read_text()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert "analysis" not in node.module
            assert "vocal" not in node.module


def test_genre_affinity_comes_from_the_declared_taxonomy(snapshot_index):
    """R19: the soft genre prior is the user's declaration, not a baked-in table."""
    from dataclasses import replace

    taxonomy = default_taxonomy()
    anchor = setbuilder.resolve_anchor("Alder - Anchor Work", snapshot_index)
    pool = setbuilder.build_pool(anchor, snapshot_index)
    assert pool, "nothing was pooled, so this would prove nothing"

    baseline = setbuilder.rank(pool, anchor, taxonomy=taxonomy)
    inverted = replace(taxonomy, family=replace(taxonomy.family, same_genre=0.0, unrelated=1.0))
    shifted = setbuilder.rank(pool, anchor, taxonomy=inverted)
    assert [s.score for s in baseline] != [s.score for s in shifted], "the declaration is unread"


def test_a_genre_signal_of_zero_weight_removes_genre_from_the_score(snapshot_index):
    """The soft prior is soft: it is a weight, never a hard exclude."""
    taxonomy = default_taxonomy()
    anchor = setbuilder.resolve_anchor("Alder - Anchor Work", snapshot_index)
    off_genre = track("Juniper", "Different World", "8A", 124.0, genre="Drum & Bass")
    pool = setbuilder.build_pool(anchor, (*snapshot_index, off_genre))
    ranked = setbuilder.rank(pool, anchor, taxonomy=taxonomy)
    assert off_genre.match in {s.track.match for s in ranked}


def test_role_falls_out_of_energy_with_the_wheel_as_the_tiebreak(snapshot_index):
    anchor = setbuilder.resolve_anchor("Alder - Anchor Work", snapshot_index)
    lower = track("Birch", "Same Key Lower", "8A", 124.0, energy=4)
    higher = track("Cedar", "Neighbour Up", "9A", 125.0, energy=8)
    assert setbuilder.assign_role(lower, anchor) == "before"
    assert setbuilder.assign_role(higher, anchor) == "after"

    # Equal energy: the wheel direction decides, upward reads as "after".
    equal_up = track("Ivy", "Equal Up", "9A", 124.0, energy=6)
    assert setbuilder.assign_role(equal_up, anchor) == "after"


def test_unknown_energy_scores_neutral_and_weights_must_sum_to_one():
    """None means unknown; two differently normalized runs produce incomparable scores."""
    assert setbuilder.energy_score(None, 5, "before") == 0.5
    assert setbuilder.energy_score(5, None, "after") == 0.5
    with pytest.raises(ValueError, match="sum to 1.0"):
        setbuilder.Weights(harmonic=0.9, bpm=0.9, genre=0.0, energy=0.0, vocal=0.0)


# ── The index: parsing, deduplication, and the cache ─────────────────────────


def test_the_index_reads_the_key_and_tempo_out_of_the_declared_head():
    """Not a private regular expression. The template owns the shape (U4)."""
    raw = {
        "title": "08A - 124 - Real Title", "artist": "Alder", "genre": "Deep House",
        "initialkey": None, "energylevel": "6", "voxlevel": "2", "voxgender": None,
    }
    entry = setbuilder.parse_entry(raw, template=TEMPLATE)
    assert entry.key == "8A"
    assert entry.bpm == 124.0
    assert entry.title == "Real Title"


def test_a_marked_lossy_title_loses_its_marker_along_with_the_head():
    """The defect the private regular expression carried."""
    entry = setbuilder.parse_entry(
        {"title": "08A - 124 - [MP3] Real Title", "artist": "Alder"}, template=TEMPLATE
    )
    assert entry.title == "Real Title"


def test_the_initialkey_tag_wins_over_the_head():
    """The tag is what analysis wrote; the head is a copy a renamer made from it."""
    entry = setbuilder.parse_entry(
        {"title": "08A - 124 - Title", "artist": "A", "initialkey": "3B"},
        template=TEMPLATE,
    )
    assert entry.key == "3B"


def test_a_track_with_no_usable_key_is_left_out_of_the_index():
    """It cannot be placed on the wheel, so it cannot be compared to anything."""
    keyless = {"title": "Just A Title", "artist": "A"}
    assert setbuilder.parse_entry(keyless, template=TEMPLATE) is None


def test_the_index_collapses_duplicate_works(tmp_path):
    """A re-import and an extended edit of one work are one index entry."""
    root = tmp_path / "music"
    root.mkdir()
    for name in ("a.flac", "b.flac", "c.flac"):
        (root / name).write_bytes(b"")

    def reader(path):
        if path.name == "c.flac":
            return {"title": "08A - 124 - Other", "artist": "Birch"}
        return {"title": "08A - 124 - Same Work", "artist": "Alder"}

    index = setbuilder.build_index(root, template=TEMPLATE, reader=reader)
    assert [t.title for t in index] == ["Same Work", "Other"]


def test_the_index_cache_skips_unchanged_files_and_re_reads_changed_ones(tmp_path):
    """mtime-keyed, so an edited file invalidates only itself."""
    root = tmp_path / "music"
    root.mkdir()
    first = root / "a.flac"
    first.write_bytes(b"")
    cache = tmp_path / "cache.json"
    reads = []

    def reader(path):
        reads.append(path.name)
        return {"title": "08A - 124 - Title", "artist": "Alder"}

    setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=reader)
    assert reads == ["a.flac"]

    setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=reader)
    assert reads == ["a.flac"], "an unchanged file was re-read despite the cache"

    import os

    os.utime(first, (1, 1))
    setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=reader)
    assert reads == ["a.flac", "a.flac"]


@pytest.mark.parametrize("stamped", [False, True], ids=["other-build", "unstamped"])
def test_a_cache_from_another_build_or_with_no_template_stamp_is_discarded(tmp_path, stamped):
    """Discarding costs one scan; deserializing or trusting it costs a wrong answer mid-run."""
    root = tmp_path / "lib"
    root.mkdir()
    audio = root / "a.flac"
    audio.touch()
    cache = tmp_path / "cache.json"
    if stamped:
        stale = {"mtime": audio.stat().st_mtime, "track": None}
        document = {"cache_version": setbuilder.CACHE_VERSION, "entries": {str(audio): stale}}
    else:
        document = {"cache_version": 0, "entries": {"x": {"nope": 1}}}
    cache.write_text(json.dumps(document))
    index = setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=lambda p: GOOD)
    assert [t.title for t in index] == ["Title"], "a stale cache was trusted"


def test_a_cache_parsed_under_another_template_is_discarded(tmp_path):
    """A cached entry is the OUTPUT of a parse, and the template is its other input."""
    root = tmp_path / "lib"
    root.mkdir()
    (root / "a.flac").touch()
    cache = tmp_path / "cache.json"

    def reader(path):
        return {"title": "08A - 124 - [LOSSY] Title", "artist": "Alder"}

    other = NameTemplate(markers=(MarkerRule(field="lossy", literal="[LOSSY]"),))
    first = setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=reader)
    second = setbuilder.build_index(root, template=other, cache_path=cache, reader=reader)
    assert [t.title for t in first] == ["[LOSSY] Title"]
    assert [t.title for t in second] == ["Title"], "the old template's parse was served"


def test_the_template_stamp_is_the_same_string_in_every_process():
    """A stamp that moved on its own would discard the cache on every run."""
    import dataclasses

    @dataclasses.dataclass(frozen=True)
    class Shape:
        head_optional: frozenset[str]
        head_sep: str = " - "

    stamp = setbuilder._template_stamp(Shape(frozenset({"key", "bpm", "energy", "vox"})))
    assert stamp == "head_optional=['bpm', 'energy', 'key', 'vox'];head_sep=' - '"
    assert setbuilder._template_stamp(TEMPLATE) != setbuilder._template_stamp(NameTemplate())


def _one_file_library(tmp_path):
    root = tmp_path / "lib"
    root.mkdir()
    audio = root / "a.flac"
    audio.write_bytes(b"first")
    return root, audio, tmp_path / "state" / "cache.json"


GOOD = {"title": "08A - 124 - Title", "artist": "Alder"}


def test_a_read_that_returned_nothing_is_never_cached_as_the_files_answer(tmp_path):
    """Found by the built in review, and newly reachable once a verb passed a path."""
    root, audio, cache = _one_file_library(tmp_path)
    failed = dict.fromkeys(setbuilder.INDEX_FIELDS)
    first = setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=lambda p: failed)
    second = setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=lambda p: GOOD)
    assert first == () and [t.title for t in second] == ["Title"]


def test_a_keyless_file_that_did_read_is_still_cached_as_nothing(tmp_path):
    """The other half, so the fix above did not quietly end the keyless cache."""
    root, audio, cache = _one_file_library(tmp_path)
    reads = []

    def reader(path):
        reads.append(path)
        return {"title": "No Head Here", "artist": "Alder"}

    setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=reader)
    setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=reader)
    assert len(reads) == 1


def test_new_bytes_under_an_old_modification_time_are_re_read(tmp_path):
    """``rsync -a``, ``cp -p`` and rclone all restore a file under its old time."""
    import os

    root, audio, cache = _one_file_library(tmp_path)
    before = audio.stat()
    setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=lambda p: GOOD)
    audio.write_bytes(b"different bytes, longer")
    os.utime(audio, ns=(before.st_atime_ns, before.st_mtime_ns))
    assert audio.stat().st_mtime_ns == before.st_mtime_ns

    other = {"title": "09A - 126 - Replaced", "artist": "Alder"}
    index = setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=lambda p: other)
    assert [(t.title, t.key) for t in index] == [("Replaced", "9A")]


@pytest.mark.parametrize(
    "entry",
    [
        [],
        "text",
        {"mtime_ns": "IDENTITY", "size": "IDENTITY", "track": []},
        {"mtime_ns": "IDENTITY", "size": "IDENTITY", "track": {"artist": 7}},
    ],
    ids=["list", "text", "track-not-a-mapping", "track-missing-fields"],
)
def test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run(tmp_path, entry):
    root, audio, cache = _one_file_library(tmp_path)
    setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=lambda p: GOOD)
    document = json.loads(cache.read_text())
    stat = audio.stat()
    if isinstance(entry, dict):
        entry = {**entry, "mtime_ns": stat.st_mtime_ns, "size": stat.st_size}
    document["entries"][str(audio)] = entry
    cache.write_text(json.dumps(document))

    index = setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=lambda p: GOOD)
    assert [t.title for t in index] == ["Title"]


@pytest.mark.parametrize(
    ("field", "value"),
    [("bpm", "124"), ("energy", True), ("vox", [3]), ("title", None), ("voxgender", 4)],
)
def test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read(tmp_path, field, value):
    """``Track(**raw)`` constructs it without complaint and the ranking fails later."""
    root, audio, cache = _one_file_library(tmp_path)
    setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=lambda p: GOOD)
    document = json.loads(cache.read_text())
    document["entries"][str(audio)]["track"][field] = value
    cache.write_text(json.dumps(document))
    reads = []

    def reader(path):
        reads.append(path)
        return GOOD

    index = setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=reader)
    assert reads == [audio], "a track of the wrong types was served from the cache"
    assert [(t.title, t.bpm) for t in index] == [("Title", 124.0)]


def test_the_cache_is_renamed_into_place_and_leaves_nothing_beside_it(tmp_path):
    root, audio, cache = _one_file_library(tmp_path)
    setbuilder.build_index(root, template=TEMPLATE, cache_path=cache, reader=lambda p: GOOD)
    assert sorted(p.name for p in cache.parent.iterdir()) == ["cache.json"]
    assert stat.S_IMODE(cache.stat().st_mode) == 0o600


def test_an_empty_walk_writes_no_cache(tmp_path):
    """An unmounted volume leaves an empty directory where the library was."""
    root = tmp_path / "lib"
    root.mkdir()
    cache = root / ".state" / "cache.json"
    assert setbuilder.build_index(root, template=TEMPLATE, cache_path=cache) == ()
    assert list(root.iterdir()) == []


def test_the_index_cache_has_a_declared_home_in_the_state_inventory(cfg):
    """A module composing its own path under a state root invents a file the inventory cannot find,
    snapshot, or clear.
    """
    entry = config.state_file("setbuilder_index_cache")
    assert entry.root is config.StateRoot.LIBRARY
    assert entry.snapshot is config.SnapshotRole.NEVER_RESTORED
    assert config.state_path("setbuilder_index_cache", cfg).is_relative_to(cfg.library.root)


def test_the_index_reads_tags_only_through_the_shared_container_reader():
    """S5: one reader, one container classification, no second opinion."""
    source = (SRC_ROOT / "cratekit" / "modules" / "tools" / "setbuilder.py").read_text()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert not alias.name.startswith("mutagen")
        if isinstance(node, ast.ImportFrom) and node.module:
            assert not node.module.startswith("mutagen")


def test_the_index_reads_a_real_file_through_the_real_reader(tmp_path):
    """The one end-to-end proof, because the injected reader proves only itself."""
    if shutil.which("ffmpeg") is None:
        pytest.fail("ffmpeg is required to prove the index reads a real audio file, and fails "
                    "rather than skips, since a skipped proof reads as a passing one.")
    from cratekit.core.tags import write_tags

    root = tmp_path / "music"
    root.mkdir()
    path = root / "probe.flac"
    proc = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=440:r=44100",
         "-t", "1", str(path)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr[-400:]

    written = {"title": "08A - 124 - Real Title", "artist": "Alder", "genre": "Deep House",
               "energylevel": 6, "voxlevel": 2}
    assert write_tags(path, written)
    index = setbuilder.build_index(root, template=TEMPLATE)
    assert len(index) == 1
    entry = index[0]
    assert (entry.artist, entry.title, entry.key, entry.bpm) == ("Alder", "Real Title", "8A", 124.0)
    assert (entry.genre, entry.energy, entry.vox) == ("Deep House", 6, 2)


def test_the_structured_payload_carries_a_version(snapshot_index):
    """R32: a schema change without a version bump must be visible."""
    payload = setbuilder.as_payload(
        setbuilder.build_set("Alder - Anchor Work", snapshot_index, taxonomy=default_taxonomy())
    )
    assert payload["payload_version"] == setbuilder.PAYLOAD_VERSION
    assert payload["anchor"]["key"] == "8A"
    assert payload["anchor"]["tempo"] == 124.0
    assert all("score" in row for row in payload["pool"])

    # R17 at the serialization boundary, checked against the guard's own set.
    from tests.test_no_beatgrid_ever import FORBIDDEN_TAG_KEYS

    def keys(value):
        if isinstance(value, dict):
            for key, inner in value.items():
                yield key
                yield from keys(inner)
        elif isinstance(value, list):
            for item in value:
                yield from keys(item)

    offenders = sorted(set(keys(payload)) & FORBIDDEN_TAG_KEYS)
    assert not offenders, f"the set-builder payload carries tempo tag keys: {offenders}"


# ── Scenario 2: mastering leaves the source byte-identical and archived ──────


def _synth_wav(tmp_path: Path, name: str = "set.wav", seconds: int = 2) -> Path:
    """A short real recording. Silence would measure as negative infinity."""
    if shutil.which("ffmpeg") is None:
        pytest.fail("ffmpeg is required to prove that mastering leaves the source unmodified, "
                    "and fails rather than skips, since a skipped proof reads as a passing one.")
    out = tmp_path / name
    if seconds in _SYNTHESIZED:
        out.write_bytes(_SYNTHESIZED[seconds])
        return out
    proc = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=220:r=44100",
         "-t", str(seconds), "-c:a", "pcm_s16le", str(out)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0 and out.exists(), proc.stderr[-400:]
    _SYNTHESIZED[seconds] = out.read_bytes()
    return out


#: ffmpeg's rendering of the sine above, by length, copied after the first.
_SYNTHESIZED: dict[int, bytes] = {}


@pytest.fixture(scope="module")
def mastered(tmp_path_factory):
    """One real master of a real recording, read by every test below that needs one."""
    folder = tmp_path_factory.mktemp("mastered")
    source = _synth_wav(folder)
    before, size = mastering.digest(source), source.stat().st_size
    return folder, source, before, size, mastering.master(source)


def test_mastering_leaves_the_source_byte_identical_and_archived(mastered):
    """The plan's second scenario, and R18's headline."""
    _, source, before, size, report = mastered
    assert mastering.digest(source) == before
    assert source.stat().st_size == size
    assert report.archived_to is not None and report.archived_to.is_file()
    assert mastering.digest(report.archived_to) == before
    assert report.archived_to.parent.name == mastering.ARCHIVE_DIRNAME
    assert report.output.is_file() and report.output.suffix == ".flac"


def test_mastering_reports_before_and_after_loudness(mastered):
    """A result nobody can check is a result nobody should trust."""
    report = mastered[-1]
    assert report.before.integrated_lufs is not None
    assert report.after.integrated_lufs is not None
    target = mastering.DEFAULT_SETTINGS.target_lufs
    assert report.after.integrated_lufs == pytest.approx(target, abs=1.5)
    assert report.bit_depth.startswith("16-bit")


def test_mastering_leaves_no_intermediate_behind(mastered):
    """A multi-gigabyte scratch file beside the recording fills a volume."""
    leftovers = [p.name for p in mastered[0].rglob("*.cratekit-drift.wav")]
    assert leftovers == []


def test_mastering_refuses_to_overwrite_an_existing_master(tmp_path):
    """The source passes an unconditional overwrite flag."""
    source = _synth_wav(tmp_path)
    mastering.output_path(source).write_bytes(b"already here")
    with pytest.raises(mastering.MasteringRefused) as excinfo:
        mastering.master(source)
    assert excinfo.value.refusal is mastering.Refusal.OUTPUT_EXISTS


def test_an_archive_entry_with_the_same_name_and_different_content_refuses(tmp_path):
    """Recorders name files by counter, so this is the normal case."""
    source = _synth_wav(tmp_path)
    archive = tmp_path / mastering.ARCHIVE_DIRNAME
    archive.mkdir()
    (archive / source.name).write_bytes(b"a different recording entirely")

    with pytest.raises(mastering.MasteringRefused) as excinfo:
        mastering.archive_source(source, archive)
    assert excinfo.value.refusal is mastering.Refusal.ARCHIVE_HOLDS_A_DIFFERENT_RECORDING
    assert (archive / source.name).read_bytes() == b"a different recording entirely"


def test_an_identical_archive_entry_is_accepted_as_already_archived(tmp_path):
    source = _synth_wav(tmp_path)
    archive = tmp_path / mastering.ARCHIVE_DIRNAME
    assert mastering.archive_source(source, archive) == archive / source.name
    assert mastering.archive_source(source, archive) == archive / source.name


def test_the_archive_is_taken_before_any_encoding_stage(tmp_path):
    """Order is the safety property, so it is asserted rather than described."""
    source = _synth_wav(tmp_path)
    archived_when = []

    def runner(command):
        archived_when.append((tmp_path / mastering.ARCHIVE_DIRNAME / source.name).is_file())
        return mastering.CommandResult(returncode=1, stderr="stopped on purpose")

    with pytest.raises(mastering.MasteringRefused):
        mastering.master(source, runner=runner)
    assert archived_when and archived_when[0] is True


def test_a_sixteen_bit_source_is_dithered_and_a_deeper_one_is_not():
    """Forcing 24-bit on a 16-bit set produces a file LARGER than the source."""
    sixteen = mastering.SourceProbe(sample_rate=44100, sample_fmt="s16", size_bytes=1)
    deeper = mastering.SourceProbe(sample_rate=48000, sample_fmt="s32", size_bytes=1)

    _, extra, depth = mastering.encoder_args(sixteen)
    assert "dither_method" in extra and depth.startswith("16-bit")

    encoder, extra, depth = mastering.encoder_args(deeper)
    assert extra == "" and depth == "24-bit"
    assert "-bits_per_raw_sample" in encoder


def test_the_apply_stage_refuses_without_a_complete_measurement():
    """An incomplete measurement drops the filter out of linear mode silently."""
    with pytest.raises(mastering.MasteringRefused) as excinfo:
        mastering.apply_filter(mastering.DEFAULT_SETTINGS, mastering.Loudness())
    assert excinfo.value.refusal is mastering.Refusal.ENCODER_FAILED
    assert "linear" in excinfo.value.detail


def test_the_loudness_report_is_parsed_as_json_not_grepped():
    """The defect this port closes."""
    stderr = (
        '{\n"input_i" : "-20.0",\n"input_tp" : "-3.0",\n"input_lra" : "5.0",\n'
        '"input_thresh" : "-30.0",\n"target_offset" : "0.5"\n}\n'
        '{\n"input_i" : "-14.2",\n"input_tp" : "-1.5",\n"input_lra" : "7.0",\n'
        '"input_thresh" : "-24.0",\n"target_offset" : "0.2",\n"output_i" : "-14.0"\n}\n'
    )
    measured = mastering.parse_loudness(stderr)
    assert measured.integrated_lufs == -14.2
    assert measured.true_peak_db == -1.5
    assert measured.target_offset == 0.2
    assert mastering.parse_output_loudness(stderr).integrated_lufs == -14.0


def test_a_silent_signal_reports_unknown_rather_than_negative_infinity():
    """loudnorm answers "-inf" for silence. That is a fact, not a number."""
    stderr = '{"input_i" : "-inf", "input_tp" : "-inf", "input_lra" : "0.0"}'
    assert mastering.parse_loudness(stderr).integrated_lufs is None


def test_an_impossible_drift_window_or_a_positive_ceiling_is_refused_at_construction():
    """Otherwise ffmpeg fails minutes into an encode, naming its own filter."""
    for window in (2, 1, 303, 64):
        with pytest.raises(ValueError):
            mastering.Settings(drift_window=window)
    with pytest.raises(ValueError, match="ceiling"):
        mastering.Settings(true_peak_db=1.0)


def test_an_unsupported_container_is_refused_rather_than_attempted(tmp_path):
    stray = tmp_path / "notes.txt"
    stray.write_text("not audio")
    with pytest.raises(mastering.MasteringRefused) as excinfo:
        mastering.master(stray)
    assert excinfo.value.refusal is mastering.Refusal.SOURCE_UNSUPPORTED


def test_a_recording_is_read_whatever_the_case_of_its_suffix(tmp_path):
    """A recorder that names its files in capitals is not refused as a stranger."""
    loud = tmp_path / "REC001.WAV"
    loud.write_bytes(b"")
    mastering._check_source(loud)


def test_joining_split_parts_quotes_a_path_containing_an_apostrophe(tmp_path):
    """ffmpeg's concat list unescapes a doubled quote; a raw one truncates."""
    part = tmp_path / "it's part one.wav"
    part.write_bytes(b"")
    written = {}

    def runner(command):
        listing = Path(command.argv[command.argv.index("-i") + 1])
        written["text"] = listing.read_text()
        # The stand-in writes the destination, as ffmpeg does: ``concatenate``
        # reads its own output and refuses a join that wrote nothing.
        Path(command.argv[-1]).write_bytes(b"joined")
        return mastering.CommandResult(returncode=0)

    mastering.concatenate([part], tmp_path / "joined.wav", runner=runner)
    assert "it''s part one.wav" in written["text"]


def test_a_join_that_exits_zero_and_writes_nothing_refuses_rather_than_returning(tmp_path):
    """Closes B3 in ``docs/mutation/u44-author.md``."""
    part = tmp_path / "part.wav"
    part.write_bytes(b"")
    destination = tmp_path / "joined.wav"

    def silent_success(command):
        return mastering.CommandResult(returncode=0)

    with pytest.raises(mastering.MasteringRefused) as excinfo:
        mastering.concatenate([part], destination, runner=silent_success)
    assert excinfo.value.refusal is mastering.Refusal.ENCODER_FAILED
    assert not destination.exists()


def test_the_mastering_payload_carries_a_version(mastered):
    payload = mastering.as_payload(mastered[-1])
    assert payload["payload_version"] == mastering.PAYLOAD_VERSION
    assert payload["archived_to"]


# ── Scenario 3: backup with rekordbox running skips the database and says why ───


@pytest.fixture
def db_file(cfg):
    """A library whose configured database path actually holds a file."""
    database = config.state_path("rekordbox_db", cfg)
    database.parent.mkdir(parents=True, exist_ok=True)
    database.write_bytes(b"SQLite format 3\x00")
    return database


#: Four dated folders older than any completed mirror a test below records, in
#: the spelling ``stamp_for`` writes, because the rotation compares names with
#: the record's stamp and a word like "one" sorts after every date.
SETTLED_ARCHIVES = "".join(f"2026-0{month}-01T000000Z/\n" for month in (1, 2, 3, 4))
THREE_ARCHIVES = "".join(f"2026-0{month}-01T000000Z/\n" for month in (1, 2, 3))


@pytest.fixture
def mirrored(cfg):
    """A completed mirror to this destination on record, so folders can be settled."""
    when = datetime(2026, 6, 1, tzinfo=timezone.utc)
    _record(cfg, "FILES", when, str(cfg.backup.dest))
    return when


def test_backup_with_rekordbox_running_skips_the_database_and_says_why(cfg, db_file, rclone):
    """The plan's third scenario."""
    plan = backup.plan_backup(cfg, process_lister=rekordbox_running)

    database = plan.portion(backup_facts.Portion.DATABASE)
    assert database.will_run is False
    assert database.refusal is backup.Refusal.REKORDBOX_RUNNING
    assert "rekordbox" in database.detail and "rekordboxAgent" in database.detail
    assert database.commands == ()

    assert plan.portion(backup_facts.Portion.FILES).will_run is True


def test_the_agent_alone_refuses_and_an_unrelated_process_named_rekordbox_does_not(
    cfg, db_file, rclone
):
    """The fact the original check missed, and P7: a guard that over-refuses gets bypassed."""
    plan = backup.plan_backup(cfg, process_lister=lambda: ("rekordboxAgent",))
    assert plan.portion(backup_facts.Portion.DATABASE).refusal is backup.Refusal.REKORDBOX_RUNNING
    plan = backup.plan_backup(cfg, process_lister=lambda: ("rekordbox-notes-editor",))
    assert plan.portion(backup_facts.Portion.DATABASE).will_run is True


def test_the_engine_helpers_keep_their_shapes(cfg):
    """A warning's keys in envelope order, a refused portion never runs, the log
    reader keeps only objects, and each destination is required up front."""
    import dataclasses

    assert list(backup._warning("code", "message")) == ["code", "message"]
    refused = backup.PortionPlan(
        portion=backup_facts.Portion.FILES,
        refusal=backup.Refusal.REKORDBOX_RUNNING,
        kind=backup.KIND_SKIPPED,
    )
    assert refused.will_run is False
    assert backup._logged('{"level": "info"}\n[1]\n2\nnot json\n') == [{"level": "info"}]
    for key in ("dest", "archive_root", "db_dest_root"):
        bare = dataclasses.replace(cfg, backup=dataclasses.replace(cfg.backup, **{key: ""}))
        with pytest.raises(backup.BackupRefused) as excinfo:
            backup._require_destinations(bare)
        assert excinfo.value.refusal is backup.Refusal.DESTINATION_NOT_CONFIGURED
        assert f"backup.{key}" in excinfo.value.detail


def test_the_quick_walk_reads_hashes_globs_and_names_as_rclone_does():
    """Two readings agree only with their hashes, an exclude reads as rclone's
    glob at the root or at any depth, and a decomposed name is found."""
    from cratekit.modules.tools import backup_record

    one = backup_record.Entry(size=1, mtime_ns=2, sha256="a")
    assert one.agrees(backup_record.Entry(size=1, mtime_ns=2, sha256="a"))
    assert not one.agrees(backup_record.Entry(size=1, mtime_ns=2, sha256="b"))

    matcher = backup_record._excludes(["/top/**", "*.tmp", "cache/**"])
    assert matcher.file("top/x/y") and not matcher.file("sub/top/x")
    assert matcher.file("a/b/c.tmp") and matcher.file("deep/cache/f")
    assert matcher.directory("top") and matcher.directory("deep/cache")
    assert not matcher.directory("sub/top")

    composed, decomposed = "café.wav", "café.wav"
    assert backup_record.first_uncomposed([composed, decomposed]) == decomposed


def test_the_backup_source_reads_no_environment_and_spells_no_remote():
    """The source system's probe could be faked by the environment, and it spelled destinations."""
    tools = SRC_ROOT / "cratekit" / "modules" / "tools"
    # Every file the backup engine is split across, so a move cannot leave the check.
    source = "\n".join(path.read_text() for path in sorted(tools.glob("backup*.py")))
    tree = ast.parse(source)
    reads = [
        ast.unparse(node)
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute) and node.attr in {"getenv", "environ"}
    ]
    assert reads == [], f"the backup module reads the environment: {reads}"
    offenders = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        # A remote reference is `name:path`; the interpolated forms and prose are not.
        and re.fullmatch(r"[A-Za-z0-9_-]+:[A-Za-z0-9_./-]*", node.value)
    ]
    assert not offenders, f"remote literals survive in the source: {offenders}"


def test_the_database_fileset_never_rides_the_file_mirror(cfg, db_file, rclone):
    """A live mirror of an open database captures a torn copy."""
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    mirror = plan.portion(backup_facts.Portion.FILES).commands[0]
    excluded = {mirror.argv[i + 1] for i, arg in enumerate(mirror.argv) if arg == "--exclude"}
    for path in backup.database_fileset(cfg):
        assert "/" + str(path.relative_to(cfg.library.root)) in excluded
    # Derived from the state inventory: a hand-kept list is how a capture loses the log.
    names = [p.name for p in backup.database_fileset(cfg)]
    base = config.state_path("rekordbox_db", cfg).name
    assert names[0] == base
    assert names[1:] == [base + s.suffix for s in config.SQLITE_SIDECARS]


def test_the_mirror_moves_overwritten_files_into_a_dated_archive_first(cfg, db_file, rclone):
    """Without it, a sync propagates local deletions to the only other copy."""
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    mirror = plan.portion(backup_facts.Portion.FILES).commands[0]
    assert "--backup-dir" in mirror.argv
    assert mirror.argv[mirror.argv.index("--backup-dir") + 1].endswith(plan.stamp)


def test_the_dated_stamp_sorts_as_text_in_chronological_order():
    """The prune and the restore both pick "newest" by string order."""
    earlier = backup.stamp_for(datetime(2026, 1, 1, 12, tzinfo=UTC))
    later = backup.stamp_for(datetime(2026, 1, 1, 13, tzinfo=UTC))
    assert earlier < later
    # An hour that repeats in local time still sorts forward here.
    autumn_first = backup.stamp_for(datetime(2026, 11, 1, 5, 30, tzinfo=UTC))
    autumn_second = backup.stamp_for(datetime(2026, 11, 1, 6, 30, tzinfo=UTC))
    assert autumn_first < autumn_second
    # And every stamp the backup writes passes the shape the restore demands.
    for moment in (
        datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        datetime(1999, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
        datetime(2026, 8, 1, 9, 5, 7, tzinfo=timezone(timedelta(hours=-4))),
    ):
        assert backup.is_stamp(backup.stamp_for(moment)), backup.stamp_for(moment)
    assert backup.is_stamp(backup.STAMP_EXAMPLE), "the refusal shows a stamp it would refuse"


def test_every_destination_in_every_command_traces_back_to_configuration(cfg, db_file, rclone):
    """R1, and this unit's own requirement: the source hardcodes four of these."""
    configured = (cfg.backup.dest, cfg.backup.archive_root, cfg.backup.db_dest_root)
    plan = backup.plan_backup(cfg, process_lister=no_processes)

    seen = 0
    for entry in plan.portions:
        for command in entry.commands:
            for arg in command.argv[1:]:
                if ":" not in arg or arg.startswith("-") or Path(arg).is_absolute():
                    continue
                seen += 1
                assert arg.startswith(configured), (
                    f"{arg!r} names a remote that came from neither the config "
                    f"nor the library root"
                )
    assert seen, "no remote destination appeared at all, so this proved nothing"


def test_an_unconfigured_remote_refuses_before_anything_runs(library, rclone):
    """No remote means no portion could run, so it is one refusal, not two."""
    unconfigured = _config(library)
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_backup(unconfigured)
    assert excinfo.value.refusal is backup.Refusal.REMOTE_NOT_CONFIGURED


def test_a_missing_rclone_refuses_every_portion_with_one_named_cause(
    cfg, db_file, monkeypatch, tmp_path
):
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))
    monkeypatch.delenv("CRATEKIT_BIN_RCLONE", raising=False)
    monkeypatch.setattr(backup.binaries, "fallback_dirs", lambda: ())
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    assert {p.refusal for p in plan.portions} == {backup.Refusal.RCLONE_MISSING}
    assert all(p.commands == () for p in plan.portions)


def test_the_dry_run_and_the_real_run_come_from_one_plan(cfg, db_file, rclone):
    """The preview cannot describe a run different from the one that follows it."""
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    preview = Recorder()
    backup.run_backup(cfg, plan, runner=preview, dry_run=True)

    for command, issued in zip(
        [c for p in plan.portions for c in p.commands], preview.commands
    ):
        assert issued.label == command.label
        if command.label in backup.TRANSFERRING_LABELS:
            assert issued.argv == (*command.argv, "--dry-run")
        else:
            assert issued.argv == command.argv


def test_a_dry_run_publishes_no_backup_age(cfg, db_file, rclone):
    """A preview that recorded an age would report a library protected by a run that copied not one
    byte.
    """
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    backup.run_backup(cfg, plan, runner=Recorder(), dry_run=True)
    assert backup.backup_facts.read_facts(cfg) == {}


def test_the_prune_keeps_the_newest_removes_the_rest_and_warns_about_nothing(
    cfg, db_file, rclone, mirrored
):
    """A prune that completed is not an assertion of absence: it purged two."""
    recorder = Recorder(stdout_for={backup.PRUNE_ARCHIVE: THREE_ARCHIVES})
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=recorder)

    purged = [c for c in recorder.commands if c.label == backup.PRUNE_ARCHIVE_FOLDER]
    assert len(purged) == 2
    assert all("2026-03-01T000000Z" not in c.argv[-1] for c in purged)
    assert all(w == () for w in (p.warnings for p in outcome.portions))


def test_the_retention_the_plan_declared_is_the_retention_the_run_applies(
    cfg, db_file, rclone, mirrored
):
    """One decision, made once."""
    recorder = Recorder(stdout_for={backup.PRUNE_ARCHIVE: SETTLED_ARCHIVES})
    plan = backup.plan_backup(cfg, process_lister=no_processes, archive_keep=3)
    assert plan.archive_keep == 3
    backup.run_backup(cfg, plan, runner=recorder)
    assert len([c for c in recorder.commands if c.label == backup.PRUNE_ARCHIVE_FOLDER]) == 1
    # A negative retention never prunes at all, for a user who keeps every rollback.
    plan = backup.plan_backup(cfg, process_lister=no_processes, archive_keep=-1)
    labels = [c.label for c in plan.portion(backup_facts.Portion.FILES).commands]
    assert backup.PRUNE_ARCHIVE not in labels


def test_the_prune_runs_only_after_the_mirror_succeeded(cfg, db_file, rclone):
    """Each dated folder holds one run's rollback."""
    recorder = Recorder(fail_labels={backup.MIRROR})
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=recorder)

    assert backup.PRUNE_ARCHIVE not in recorder.labels()
    assert backup.PRUNE_ARCHIVE_FOLDER not in recorder.labels()
    files = [p for p in outcome.portions if p.portion is backup_facts.Portion.FILES][0]
    assert files.ran is False


def _files_outcome(outcome):
    return [p for p in outcome.portions if p.portion is backup_facts.Portion.FILES][0]


def test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful(
    cfg, db_file, rclone
):
    """The drive the finding behind this unit recorded as never performed."""
    recorder = Recorder(fail_labels={backup.PRUNE_ARCHIVE})
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=recorder)

    files = _files_outcome(outcome)
    assert files.ran is True
    assert outcome.ok is True
    assert backup.backup_facts.ages(cfg)[0].state is not backup_facts.AgeState.NEVER_RECORDED

    assert [w["code"] for w in files.warnings] == [backup.ARCHIVE_LISTING_FAILED]
    assert "accumulate" in files.warnings[0]["message"]
    assert backup.PRUNE_ARCHIVE_FOLDER not in recorder.labels(), "a failed listing purged something"


def test_a_failed_purge_reports_how_many_folders_survived_it(cfg, db_file, rclone, mirrored):
    """The second condition, which has a different fix from the first."""
    recorder = Recorder(
        stdout_for={backup.PRUNE_ARCHIVE: THREE_ARCHIVES},
        fail_labels={backup.PRUNE_ARCHIVE_FOLDER},
    )
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=recorder)

    files = _files_outcome(outcome)
    assert files.ran is True
    assert [w["code"] for w in files.warnings] == [backup.ARCHIVE_PURGE_FAILED]
    assert "2 dated folder(s)" in files.warnings[0]["message"], files.warnings
    assert files.results[0].returncode == 0, "the listing is reported as having failed"


def test_the_portion_with_no_prune_command_carries_no_warning(cfg, db_file, rclone):
    """The database portion never prunes, so it has nothing to report."""
    recorder = Recorder(fail_labels={backup.PRUNE_ARCHIVE})
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=recorder)

    database = [
        p for p in outcome.portions if p.portion is backup_facts.Portion.DATABASE
    ][0]
    assert database.warnings == ()


def test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing(cfg, db_file, rclone):
    """The branch this replaced ran the listing and read nothing."""
    recorder = Recorder(fail_labels={backup.PRUNE_ARCHIVE})
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=recorder, dry_run=True)

    assert [w["code"] for w in _files_outcome(outcome).warnings] == [
        backup.ARCHIVE_LISTING_FAILED
    ]
    assert backup.PRUNE_ARCHIVE_FOLDER not in recorder.labels()


def test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing(
    cfg, db_file, rclone, mirrored
):
    """What the fold must not have changed."""
    recorder = Recorder(stdout_for={backup.PRUNE_ARCHIVE: SETTLED_ARCHIVES})
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=recorder, dry_run=True)

    assert _files_outcome(outcome).warnings == ()
    assert backup.PRUNE_ARCHIVE_FOLDER not in recorder.labels()


def test_a_failed_portion_publishes_no_age(cfg, db_file, rclone):
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    backup.run_backup(cfg, plan, runner=Recorder(fail_labels={backup.MIRROR}))
    facts = backup_facts.read_facts(cfg)
    assert backup_facts.Portion.FILES not in facts


def test_no_provider_specific_flag_is_baked_into_the_commands(cfg, db_file, rclone):
    """The remote is configuration, so a one-provider flag belongs in rclone's own configuration
    rather than in a command this builds for every provider.
    """
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    for entry in plan.portions:
        for command in entry.commands:
            assert not any(arg.startswith("--drive-") for arg in command.argv)


def test_the_settings_directories_ride_the_database_portion_and_share_its_gate(
    cfg, db_file, rclone, tmp_path
):
    """They point at the database, and a live application is writing them."""
    settings = tmp_path / "settings"
    settings.mkdir()
    plan = backup.plan_backup(cfg, process_lister=no_processes, settings_dirs=(settings,))
    labels = [c.label for c in plan.portion(backup_facts.Portion.DATABASE).commands]
    assert backup.SNAPSHOT_SETTINGS in labels
    plan = backup.plan_backup(cfg, process_lister=rekordbox_running, settings_dirs=(settings,))
    assert plan.portion(backup_facts.Portion.DATABASE).commands == ()


@pytest.mark.parametrize("platform", ["darwin", "win32"])
def test_the_settings_location_is_resolved_per_platform_not_assumed(platform, tmp_path):
    """R1: no macOS-only assumption. Adding a platform is a row, not a rewrite."""
    home = tmp_path / "home"
    for relative in backup._SETTINGS_DIRS_BY_PLATFORM[platform]:
        (home / relative).mkdir(parents=True)
    resolved = backup.settings_directories(home=home, platform=platform)
    assert resolved and all(p.is_dir() for p in resolved)
    # A platform with no row contributes nothing rather than guessing.
    assert backup.settings_directories(home=home, platform="haiku") == ()


# ── The rotation counts a run, not an attempt ────────────────────────────────


class ArchiveRemote:
    """A runner that HOLDS the dated archive folders, the way a remote does."""

    def __init__(self, *folders, fail_mirror=False, overwrites=True):
        self.folders = set(folders)
        self.fail_mirror = fail_mirror
        self.overwrites = overwrites
        self.purged = []

    def __call__(self, command):
        if command.label == backup.MIRROR:
            if self.overwrites:
                archive = command.argv[command.argv.index("--backup-dir") + 1]
                self.folders.add(archive.rsplit("/", 1)[1])
            if self.fail_mirror:
                return backup.CommandResult(returncode=1, stderr="connection reset")
        if command.label == backup.PRUNE_ARCHIVE:
            return backup.CommandResult(
                returncode=0, stdout="".join(f"{name}/\n" for name in sorted(self.folders))
            )
        if command.label == backup.PRUNE_ARCHIVE_FOLDER:
            name = command.argv[-1].rsplit("/", 1)[1]
            self.folders.discard(name)
            self.purged.append(name)
        return backup.CommandResult(returncode=0)


def _mirror_at(cfg, remote, at, *, keep=backup.DEFAULT_ARCHIVE_KEEP):
    """One attempt at the whole plan at one instant, the way one claim makes it."""
    plan = backup.plan_backup(
        cfg, now=at, process_lister=no_processes, archive_keep=keep, check=True
    )
    return backup.run_backup(cfg, plan, runner=remote, now=at)


ROTATION_DAY = datetime(2026, 9, 1, 12, 0, 0, tzinfo=timezone.utc)


def _stamp(days: float) -> str:
    return backup.stamp_for(ROTATION_DAY + timedelta(days=days))


def test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote(cfg, db_file, rclone):
    """The retried portion's closing condition, driven against a remote that remembers."""
    remote = ArchiveRemote()
    _mirror_at(cfg, remote, ROTATION_DAY)
    settled = _stamp(0)
    assert remote.folders == {settled}

    remote.fail_mirror = True
    failed = _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1))
    assert _files_outcome(failed).ran is False
    remote.fail_mirror = False
    retried = _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1, hours=2))
    assert _files_outcome(retried).ran is True

    assert _stamp(1) in remote.folders, (
        f"the retry purged {remote.purged}, which includes the failed attempt's "
        f"archive: the only copies of what that attempt overwrote are gone"
    )
    assert remote.folders == {_stamp(1), _stamp(1 + 2 / 24)}
    assert remote.purged == [settled]


def test_the_run_after_a_retried_one_rotates_every_attempt_out_together(cfg, db_file, rclone):
    """Held is not kept for ever. One run is one slot, and the slot rotates."""
    remote = ArchiveRemote()
    _mirror_at(cfg, remote, ROTATION_DAY)
    remote.fail_mirror = True
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1))
    remote.fail_mirror = False
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1, hours=2))

    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=2))
    assert remote.folders == {_stamp(2)}


def test_a_remote_with_no_completed_mirror_on_record_is_never_purged(cfg, db_file, rclone):
    """No record is not a record of nothing (METHOD's first pattern)."""
    remote = ArchiveRemote("2026-08-01T000000Z", "2026-08-02T000000Z", fail_mirror=True)
    _mirror_at(cfg, remote, ROTATION_DAY)
    remote.fail_mirror = False
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(hours=1))
    assert remote.purged == []

    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1))
    assert remote.folders == {_stamp(1)}


def test_a_completed_mirror_to_another_destination_settles_nothing_here(cfg, db_file, rclone):
    """The record names a destination."""
    _record(cfg, "FILES", ROTATION_DAY, "elsewhere:mirror")
    remote = ArchiveRemote("2026-08-01T000000Z", "2026-08-02T000000Z")
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1))
    assert remote.purged == []


def test_a_run_that_overwrote_nothing_still_keeps_the_newest_settled_archive(cfg, db_file, rclone):
    """rclone writes no dated folder for a run that replaced nothing."""
    remote = ArchiveRemote("2026-08-01T000000Z", "2026-08-02T000000Z", overwrites=False)
    _record(cfg, "FILES", ROTATION_DAY, str(cfg.backup.dest))
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1))
    assert remote.folders == {"2026-08-02T000000Z"}


def test_the_folder_the_last_completed_run_wrote_is_settled_not_held(cfg, db_file, rclone):
    """THE BOUNDARY. The last completed run's own folder carries the stamp of the instant on record,
    so the comparison has to be strict: at or before the floor is settled.
    """
    remote = ArchiveRemote(_stamp(0), overwrites=False)
    _record(cfg, "FILES", ROTATION_DAY, str(cfg.backup.dest))
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1), keep=0)
    assert remote.folders == set()


def test_a_wider_keep_counts_the_held_run_as_one_of_its_slots(cfg, db_file, rclone):
    remote = ArchiveRemote("2026-08-01T000000Z", "2026-08-02T000000Z", "2026-08-03T000000Z")
    _record(cfg, "FILES", ROTATION_DAY, str(cfg.backup.dest))
    remote.fail_mirror = True
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1))
    remote.fail_mirror = False
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=2), keep=2)
    assert remote.folders == {"2026-08-03T000000Z", _stamp(1), _stamp(2)}


def test_a_keep_of_zero_is_still_a_keep_of_zero(cfg, db_file, rclone):
    """Asking to keep no archive is a choice."""
    remote = ArchiveRemote("2026-08-01T000000Z")
    _record(cfg, "FILES", ROTATION_DAY, str(cfg.backup.dest))
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1), keep=0)
    assert remote.folders == set()


@pytest.mark.parametrize(
    ("keep", "said", "unsaid"),
    [
        (-1, "keeping every", "last completed mirror"),
        (0, "keeping no", "last completed mirror"),
        (1, "last completed mirror", "keeping no"),
    ],
)
def test_the_plan_describes_the_rotation_the_run_applies(cfg, db_file, rclone, keep, said, unsaid):
    """The preview and the run are one decision."""
    plan = backup.plan_backup(cfg, process_lister=no_processes, archive_keep=keep)
    detail = plan.portion(backup_facts.Portion.FILES).detail
    assert said in detail and unsaid not in detail, detail


def test_a_record_that_cannot_be_read_purges_nothing(cfg, db_file, rclone):
    """Unreadable is not absent, and it is not a floor either."""
    backup_facts.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    backup_facts.path_for(cfg).write_text("{ not json")
    remote = ArchiveRemote("2026-08-01T000000Z", "2026-08-02T000000Z")
    with pytest.raises(backup_facts.BackupFactsUnreadable):
        _mirror_at(cfg, remote, ROTATION_DAY)
    assert remote.purged == []


def test_a_rehearsal_does_not_read_the_record_to_list_a_rotation(cfg, db_file, rclone):
    """A rehearsal purges nothing, so it needs no floor, and reading the record for one would fail a
    preview over a file the preview never touches.
    """
    backup_facts.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    backup_facts.path_for(cfg).write_text("{ not json")
    remote = ArchiveRemote("2026-08-01T000000Z")
    plan = backup.plan_backup(cfg, now=ROTATION_DAY, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=remote, now=ROTATION_DAY, dry_run=True)
    assert _files_outcome(outcome).ran is True
    assert remote.purged == []


# ── Scenario 4: the age fact is readable by core, which does not import backup ───


def test_backup_age_is_readable_from_library_scoped_state(cfg, db_file, rclone):
    """The plan's fourth scenario."""
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    now = datetime(2026, 8, 1, 12, tzinfo=UTC)
    backup.run_backup(cfg, plan, runner=Recorder(), now=now)

    entry = config.state_file(backup_facts.STATE_KEY)
    assert entry.root is config.StateRoot.LIBRARY
    assert backup_facts.path_for(cfg).is_relative_to(cfg.library.root)

    reported = backup_facts.ages(cfg, now=now + timedelta(hours=6))
    by_portion = {a.portion: a for a in reported}
    assert by_portion[backup_facts.Portion.FILES].age == timedelta(hours=6)
    assert by_portion[backup_facts.Portion.DATABASE].age == timedelta(hours=6)


def test_the_core_reader_does_not_import_the_backup_module(cfg):
    """The whole point of publishing a FACT instead of exposing a function."""
    source = (SRC_ROOT / "cratekit" / "core" / "backup_facts.py").read_text()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert not alias.name.startswith("cratekit.modules")
        if isinstance(node, ast.ImportFrom) and node.module:
            assert not node.module.startswith("cratekit.modules")

    # And it answers on a machine where the module was never installed at all.
    assert backup_facts.read_facts(cfg) == {}
    assert all(
        a.state is backup_facts.AgeState.NEVER_RECORDED for a in backup_facts.ages(cfg)
    )


def test_a_refused_portion_leaves_its_previous_age_untouched(cfg, db_file, rclone):
    """The number R15 needs is exactly this one."""
    first = datetime(2026, 7, 1, 9, tzinfo=UTC)
    backup.run_backup(
        cfg,
        backup.plan_backup(cfg, process_lister=no_processes),
        runner=Recorder(),
        now=first,
    )
    second = datetime(2026, 8, 1, 9, tzinfo=UTC)
    backup.run_backup(
        cfg,
        backup.plan_backup(cfg, process_lister=rekordbox_running),
        runner=Recorder(),
        now=second,
    )

    facts = backup_facts.read_facts(cfg)
    assert facts[backup_facts.Portion.FILES].completed_at == second
    assert facts[backup_facts.Portion.DATABASE].completed_at == first


def test_never_recorded_is_a_different_answer_from_very_old(cfg):
    """They have different fixes; and every declared portion is reported (P3)."""
    assert {a.portion for a in backup_facts.ages(cfg)} == set(backup_facts.Portion)
    now = datetime(2026, 8, 1, tzinfo=UTC)
    _record(cfg, "FILES", now - timedelta(days=400), "remote:mirror")
    by_portion = {a.portion: a for a in backup_facts.ages(cfg, now=now)}
    assert by_portion[backup_facts.Portion.FILES].state is backup_facts.AgeState.KNOWN
    assert by_portion[backup_facts.Portion.FILES].age == timedelta(days=400)
    assert by_portion[backup_facts.Portion.DATABASE].state is backup_facts.AgeState.NEVER_RECORDED


@pytest.mark.parametrize(
    ("ahead", "state"),
    [(timedelta(days=2), "RECORDED_IN_THE_FUTURE"), (timedelta(minutes=5), "KNOWN")],
    ids=["future", "small-clock-difference"],
)
def test_a_future_timestamp_is_named_and_a_small_clock_difference_tolerated(cfg, ahead, state):
    """A negative age is not the freshest value; two machines will not agree on the second."""
    now = datetime(2026, 8, 1, tzinfo=UTC)
    _record(cfg, "FILES", now + ahead, "remote:mirror")
    entry = {a.portion: a for a in backup_facts.ages(cfg, now=now)}[backup_facts.Portion.FILES]
    assert entry.state is getattr(backup_facts.AgeState, state)
    if state == "RECORDED_IN_THE_FUTURE":
        assert entry.age is None


def test_the_quoted_age_is_none_unless_every_portion_has_a_usable_one(cfg):
    """A number derived from half the portions describes a half-protected library as though it were
    fully protected.
    """
    now = datetime(2026, 8, 1, tzinfo=UTC)
    _record(cfg, "FILES", now - timedelta(days=1), "remote:mirror")
    assert backup_facts.oldest_usable_age(cfg, now=now) is None

    _record(cfg, "DATABASE", now - timedelta(days=9), "remote:database-snapshots")
    assert backup_facts.oldest_usable_age(cfg, now=now) == timedelta(days=9)


@pytest.mark.parametrize(
    ("text", "remedy"),
    [
        ("{ this is not json", "REPAIR_BACKUP_FACTS"),
        (json.dumps({"schema_version": backup_facts.SCHEMA_VERSION + 1, "portions": {}}),
         "UPGRADE_CRATEKIT"),
    ],
    ids=["unreadable", "newer-build"],
)
def test_a_fact_file_that_cannot_be_read_refuses_rather_than_reporting_no_backup(cfg, text, remedy):
    """No backup and an unreadable record have opposite remediations."""
    path = backup_facts.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    with pytest.raises(backup_facts.BackupFactsUnreadable) as excinfo:
        backup_facts.read_facts(cfg)
    assert excinfo.value.remedy is getattr(backup_facts.Remedy, remedy)


def test_a_naive_timestamp_is_refused_where_it_is_produced(cfg):
    """The failure lands on the code that made the value, not on a user weeks on."""
    with pytest.raises(ValueError, match="time zone"):
        _record(cfg, "FILES", datetime(2026, 8, 1, 12), "remote:mirror")


def test_the_fact_file_is_written_owner_only_under_any_umask(cfg, monkeypatch):
    """P1: a state file whose mode came from the umask is the recorded defect, and this one records
    when a user's data was last protected.
    """
    monkeypatch.setattr("os.umask", lambda mask: 0)
    import os

    old = os.umask(0)
    try:
        path = _record(cfg, "FILES", datetime(2026, 8, 1, tzinfo=UTC), "remote:mirror")
        assert stat.S_IMODE(path.stat().st_mode) == config.PRIVATE_FILE_MODE
        assert stat.S_IMODE(path.parent.stat().st_mode) == config.PRIVATE_DIR_MODE
    finally:
        os.umask(old)


# ── Scenario 5: restore clears stale sidecars BEFORE copying ─────────────────


def test_restore_removes_stale_sidecars_before_copying(cfg, tmp_path, rclone):
    """The plan's fifth scenario, asserted on the ORDER rather than the outcome."""
    target = tmp_path / "scratch"
    database = backup.database_target_for(cfg, target)
    database.parent.mkdir(parents=True, exist_ok=True)
    database.write_bytes(b"old database")
    stale = []
    for sidecar in config.SQLITE_SIDECARS:
        path = database.with_name(database.name + sidecar.suffix)
        path.write_bytes(b"stale")
        stale.append(path)

    observed = []

    def runner(command):
        if command.label in backup.TRANSFERRING_LABELS:
            observed.append((command.label, [p.exists() for p in stale]))
        if command.label == backup.LIST_SNAPSHOT_CONTENTS:
            return backup.CommandResult(returncode=0, stdout=snapshot_listing(cfg))
        return backup.CommandResult(returncode=0)

    plan = _restore(cfg, target=target, snapshot="2026-08-01T000000Z", runner=runner)
    assert set(plan.clears) == set(stale)

    backup.run_restore(plan, cfg, runner=runner, gates=open_gates)

    assert not any(p.exists() for p in stale), "stale sidecars survived the restore"
    assert observed, "no copy command was issued"
    # Every transfer ran with both sidecars already gone. The listing is a
    # probe at plan time, before anything is cleared, and is not a transfer.
    for _, present in observed:
        assert present == [False, False]


def test_a_rehearsed_restore_does_not_clear_the_live_sidecars(cfg, tmp_path, rclone):
    """Clearing is itself destructive, so a preview must not do it."""
    target = tmp_path / "scratch"
    database = backup.database_target_for(cfg, target)
    database.parent.mkdir(parents=True, exist_ok=True)
    database.write_bytes(b"live database")
    sidecars = []
    for sidecar in config.SQLITE_SIDECARS:
        path = database.with_name(database.name + sidecar.suffix)
        path.write_bytes(b"live log")
        sidecars.append(path)

    recorder = _listing(cfg)
    plan = _restore(cfg, target=target, snapshot="2026-08-01T000000Z", runner=recorder)
    backup.run_restore(plan, cfg, runner=recorder, dry_run=True, gates=open_gates)

    assert all(p.exists() for p in sidecars), "a rehearsal deleted the live sidecars"
    issued = [c for c in recorder.commands if c.label == backup.RESTORE_DATABASE]
    assert issued and all(c.argv[-1] == "--dry-run" for c in issued)


def test_restore_writes_back_the_log_and_never_the_shared_memory_index(cfg, tmp_path, rclone):
    """The source system's asymmetry, carried across as a declaration."""
    target = _scratch(cfg, tmp_path)
    plan = _restore(
        cfg, target=target, snapshot="2026-08-01T000000Z", runner=_listing(cfg, "-wal", "-shm"),
    )
    sources = [c.argv[c.argv.index("copy") + 1] for c in plan.commands]
    restored = {s.suffix for s in config.SQLITE_SIDECARS if s.restored}
    for suffix in (s.suffix for s in config.SQLITE_SIDECARS):
        matching = [s for s in sources if s.endswith(suffix)]
        assert bool(matching) == (suffix in restored), (
            f"a restore that copies {suffix} back is not what the inventory declares"
        )


def test_the_file_half_of_a_restore_copies_and_never_syncs(cfg, tmp_path, rclone):
    """A sync makes the target MATCH the remote, which means deleting."""
    target = _scratch(cfg, tmp_path)
    plan = _restore(
        cfg, target=target, snapshot="2026-08-01T000000Z", include_mirror=True, runner=Recorder(),
    )
    mirror = [c for c in plan.commands if c.label == backup.RESTORE_MIRROR]
    assert len(mirror) == 1
    assert "copy" in mirror[0].argv and "sync" not in mirror[0].argv
    # And it is FIRST, so the database lands last, after the bulk transfer.
    assert plan.commands[0].label == backup.RESTORE_MIRROR
    # It is off by default: the two halves cost very differently.
    plan = _restore(cfg, target=target, snapshot="2026-08-01T000000Z", runner=_listing(cfg))
    assert backup.RESTORE_MIRROR not in [c.label for c in plan.commands]


def test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar(
    cfg, tmp_path, rclone
):
    """The residual
    "A restore from a snapshot taken with rekordbox closed always reports failure".

    The only snapshot this product takes has no write ahead log.
    ``plan_database_snapshot`` copies a sidecar only when it is present.
    ``plan_restore`` used to copy the log unconditionally, rclone exited 3, and
    the person was told the restore failed after the database had already landed.
    """
    target = _scratch(cfg, tmp_path)
    database = backup.database_target_for(cfg, target).name
    recorder = _listing(cfg)
    plan = _restore(cfg, target=target, snapshot="2026-08-01T000000Z", runner=recorder)
    sources = [c.argv[c.argv.index("copy") + 1] for c in plan.commands]
    assert any(source.endswith(database) for source in sources)
    assert not any(source.endswith(database + "-wal") for source in sources)
    assert plan.absent_sidecars == ("-wal",)
    results = backup.run_restore(plan, cfg, runner=recorder, gates=open_gates)
    assert results and all(result.returncode == 0 for result in results)


def test_a_restore_from_a_snapshot_holding_the_log_copies_it(cfg, tmp_path, rclone):
    """The other shape: a snapshot taken while the database still had a log."""
    target = _scratch(cfg, tmp_path)
    database = backup.database_target_for(cfg, target).name
    recorder = _listing(cfg, "-wal")
    plan = _restore(cfg, target=target, snapshot="2026-08-01T000000Z", runner=recorder)
    sources = [c.argv[c.argv.index("copy") + 1] for c in plan.commands]
    assert any(source.endswith(database) for source in sources)
    assert any(source.endswith(database + "-wal") for source in sources)
    assert plan.absent_sidecars == ()
    results = backup.run_restore(plan, cfg, runner=recorder, gates=open_gates)
    assert results and all(result.returncode == 0 for result in results)


def test_a_failed_database_copy_still_refuses_when_the_sidecar_is_absent(cfg, tmp_path, rclone):
    """Skipping an absent sidecar does not swallow a failed database transfer."""
    target = _scratch(cfg, tmp_path)
    recorder = _listing(cfg, fail_labels={backup.RESTORE_DATABASE})
    plan = _restore(cfg, target=target, snapshot="2026-08-01T000000Z", runner=recorder)
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.run_restore(plan, cfg, runner=recorder, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.RESTORE_TRANSFER_FAILED


def test_a_snapshot_that_cannot_be_listed_refuses_before_clearing(cfg, tmp_path, rclone):
    """A failed listing is not an empty snapshot."""
    target = tmp_path / "scratch"
    database = backup.database_target_for(cfg, target)
    database.parent.mkdir(parents=True, exist_ok=True)
    wal = database.with_name(database.name + "-wal")
    wal.write_bytes(b"live log")
    recorder = Recorder(fail_labels={backup.LIST_SNAPSHOT_CONTENTS})
    refused = _restore_refused(cfg, target=target, snapshot="2026-08-01T000000Z", runner=recorder)
    assert refused.refusal is backup.Refusal.SNAPSHOT_LISTING_FAILED
    assert wal.exists() and wal.read_bytes() == b"live log"
    assert backup.RESTORE_DATABASE not in recorder.labels()


def test_the_snapshot_listing_is_of_the_database_folder(cfg, tmp_path, rclone):
    """Listing the snapshot root would see dated folder names, never the log."""
    target = _scratch(cfg, tmp_path)
    recorder = _listing(cfg, "-wal")
    _restore(cfg, target=target, snapshot="2026-08-01T000000Z", runner=recorder)
    listed = [c for c in recorder.commands if c.label == backup.LIST_SNAPSHOT_CONTENTS]
    assert len(listed) == 1
    assert listed[0].argv[-2].endswith("/2026-08-01T000000Z/db/")
    assert "--files-only" in listed[0].argv


def test_the_sidecars_are_cleared_before_the_mirror_too(cfg, tmp_path, rclone):
    """The invariant at its strongest."""
    target = tmp_path / "scratch"
    database = backup.database_target_for(cfg, target)
    database.parent.mkdir(parents=True, exist_ok=True)
    database.write_bytes(b"old")
    stale = []
    for sidecar in config.SQLITE_SIDECARS:
        path = database.with_name(database.name + sidecar.suffix)
        path.write_bytes(b"stale")
        stale.append(path)

    observed = []

    def runner(command):
        if command.label in backup.TRANSFERRING_LABELS:
            observed.append((command.label, any(p.exists() for p in stale)))
        if command.label == backup.LIST_SNAPSHOT_CONTENTS:
            return backup.CommandResult(returncode=0, stdout=snapshot_listing(cfg))
        return backup.CommandResult(returncode=0)

    plan = _restore(
        cfg, target=target, snapshot="2026-08-01T000000Z", include_mirror=True, runner=runner,
    )
    backup.run_restore(plan, cfg, runner=runner, gates=open_gates)
    assert observed[0][0] == backup.RESTORE_MIRROR
    assert all(present is False for _, present in observed)


def test_restore_is_a_named_decision_and_never_a_prompt(cfg, tmp_path, rclone):
    """R33. The source blocks on standard input before overwriting a library."""
    refused = _restore_refused(cfg, target=tmp_path, confirmed=False, runner=Recorder())
    assert refused.refusal is backup.Refusal.RESTORE_NOT_CONFIRMED


def test_no_module_in_this_unit_reads_standard_input():
    """The structural half of R33: a prompt cannot appear where none is written."""
    for path in sorted((SRC_ROOT / "cratekit" / "modules" / "tools").glob("*.py")):
        name, source = path.name, path.read_text()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id != "input", f"{name} prompts on standard input"
            if isinstance(node, ast.Attribute):
                assert node.attr not in {"stdin"}, f"{name} reads standard input"


def test_restore_refuses_while_rekordbox_holds_the_database(cfg, tmp_path, rclone):
    """A live application and the disk would describe two different libraries."""
    refused = _restore_refused(
        cfg, target=tmp_path, runner=Recorder(), process_lister=rekordbox_running
    )
    assert refused.refusal is backup.Refusal.REKORDBOX_RUNNING


def test_the_restore_target_is_derived_from_the_configured_database_path(cfg, tmp_path):
    """Not from an assumed vendor layout."""
    target = tmp_path / "scratch"
    relative = config.state_path("rekordbox_db", cfg).relative_to(cfg.library.root)
    assert backup.database_target_for(cfg, target) == target / relative


def test_a_restore_with_no_snapshot_available_refuses_by_name(cfg, tmp_path, rclone):
    refused = _restore_refused(cfg, target=tmp_path, runner=Recorder())
    assert refused.refusal is backup.Refusal.NO_SNAPSHOT_AVAILABLE


def test_the_latest_snapshot_is_the_newest_by_sortable_stamp(cfg, tmp_path, rclone):
    recorder = Recorder(
        stdout_for={
            backup.LIST_SNAPSHOTS: "2026-01-01T000000Z/\n2026-03-01T000000Z/\n2026-02-01T000000Z/\n"
        }
    )
    assert backup.latest_snapshot(cfg, runner=recorder) == "2026-03-01T000000Z"


def test_an_absent_restore_target_refuses_rather_than_creating_one(cfg, tmp_path, rclone):
    """Creating the target would silently restore a library into a directory the user never mounted,
    on the boot disk.
    """
    refused = _restore_refused(cfg, target=tmp_path / "not-mounted", runner=Recorder())
    assert refused.refusal is backup.Refusal.RESTORE_TARGET_ABSENT


def test_the_backup_payload_carries_a_version(cfg, db_file, rclone):
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    payload = backup.plan_payload(plan)
    assert payload["payload_version"] == backup.PAYLOAD_VERSION
    assert {p["portion"] for p in payload["portions"]} == {
        p.value for p in backup_facts.Portion
    }

    outcome = backup.run_backup(cfg, plan, runner=Recorder())
    assert backup.outcome_payload(outcome)["ok"] is True


# ── Snapshot provenance. A pulled snapshot is a stamp, and it is this library's. ───

STAMP = "2026-08-01T000000Z"


def marker_for(identity):
    """The marker filename the capture writes for one identity."""
    name = backup.identity_marker(identity)
    assert name is not None, f"{identity!r} produced no marker at all"
    return name


def marked(cfg, identity=None, *, snapshots=None):
    """A recorder whose remote holds the database and one identity marker."""
    stdout_for = {
        backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg),
        backup.LIST_SNAPSHOT_IDENTITY: marker_for(identity or cfg.library.volume_id) + "\n",
    }
    if snapshots is not None:
        stdout_for[backup.LIST_SNAPSHOTS] = "".join(name + "/\n" for name in snapshots)
    return Recorder(stdout_for=stdout_for)


@pytest.mark.parametrize(
    "typed",
    [
        "../another-library-snapshots/2020-01-01T000000Z",
        "2026-08-01T000000Z/../../elsewhere",
        "2026-08-01",
        "newest",
        "",
        "2026-13-01T000000Z",
        "2026-08-01T000000Z ",
        # A real date the calendar parse accepts and the pattern does not: the
        # parser is lenient about padding, which is why neither check stands alone.
        "2026-8-01T000000Z",
    ],
)
def test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked(
    cfg, tmp_path, rclone, typed
):
    """The ledger's measured cost, reproduced: the first value is its own."""
    recorder = marked(cfg)
    refused = _restore_refused(cfg, target=tmp_path, snapshot=typed, runner=recorder)
    assert refused.refusal is backup.Refusal.SNAPSHOT_NAME_INVALID
    assert recorder.commands == [], (
        f"the remote was asked {recorder.labels()} about a value that is not a stamp"
    )


def test_a_snapshot_marked_for_another_library_is_refused(cfg, tmp_path, rclone):
    """The half the shape check cannot close: a well formed stamp, someone else's."""
    recorder = marked(cfg, "0000-AAAA")
    refused = _restore_refused(cfg, target=tmp_path, snapshot=STAMP, runner=recorder)
    assert refused.refusal is backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH
    assert "0000-aaaa" in refused.detail, refused.detail
    assert not any(c.label in backup.TRANSFERRING_LABELS for c in recorder.commands)


def test_a_snapshot_marked_for_this_library_is_planned_and_compared_case_blind(
    cfg, tmp_path, rclone
):
    """``diskutil`` prints uppercase and the adapters report lowercase."""
    plan = _restore(cfg, target=tmp_path, snapshot=STAMP, runner=marked(cfg))
    assert plan.snapshot == STAMP
    assert plan.recorded_volume == "f1e2-d3c4"
    recorder = _listing(cfg, identity="library-volume.F1E2-d3c4\n")
    plan = _restore(cfg, target=tmp_path, snapshot=STAMP, runner=recorder)
    assert plan.recorded_volume == "f1e2-d3c4"


def test_two_identities_or_an_empty_marker_refuse_as_another_librarys(cfg, tmp_path, rclone):
    """Two libraries backing up in one second share one folder; an empty marker is not unmarked."""
    both = marker_for(cfg.library.volume_id) + "\n" + marker_for("0000-AAAA") + "\n"
    for identity in (both, "library-volume.\n"):
        recorder = _listing(cfg, identity=identity)
        refused = _restore_refused(cfg, target=tmp_path, snapshot=STAMP, runner=recorder)
        assert refused.refusal is backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH


def test_an_identity_listing_that_fails_is_not_read_as_an_unmarked_snapshot(cfg, tmp_path, rclone):
    """Absence read as evidence of absence, the first pattern."""
    recorder = _listing(cfg, fail_labels={backup.LIST_SNAPSHOT_IDENTITY})
    refused = _restore_refused(cfg, target=tmp_path, snapshot=STAMP, runner=recorder)
    assert refused.refusal is backup.Refusal.SNAPSHOT_LISTING_FAILED
    assert not any(c.label in backup.TRANSFERRING_LABELS for c in recorder.commands)


@pytest.mark.parametrize(
    "failing", [backup.LIST_SNAPSHOT_IDENTITY, backup.LIST_SNAPSHOT_CONTENTS]
)
def test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote(
    cfg, tmp_path, rclone, failing
):
    """The snapshot exists; the remote or its credential is what failed."""
    from cratekit.cli import exit_codes

    recorder = Recorder(fail_labels={failing})
    refused = _restore_refused(cfg, target=tmp_path, snapshot=STAMP, runner=recorder)
    assert refused.refusal is backup.Refusal.SNAPSHOT_LISTING_FAILED
    assert str(refused.refusal) == "snapshot-listing-failed"
    assert f"the snapshot {STAMP}" in refused.detail
    assert "could not be listed" in refused.detail
    steps = exit_codes.remediation_for(str(refused.refusal)).steps
    assert steps, "the listing refusal reserves no steps for a person to follow"
    assert "remote" in steps[0] and "reachable" in steps[0]
    assert any("credential" in step for step in steps)
    assert not any("take a backup" in step for step in steps)


def test_no_snapshot_at_all_still_says_to_take_a_backup(cfg, tmp_path, rclone):
    """Absence keeps its own slug, and its step is still the right act."""
    from cratekit.cli import exit_codes

    refused = _restore_refused(cfg, target=tmp_path, runner=Recorder())
    assert refused.refusal is backup.Refusal.NO_SNAPSHOT_AVAILABLE
    assert "no dated database snapshot was found" in refused.detail
    steps = exit_codes.remediation_for(str(refused.refusal)).steps
    assert any("take a backup" in step for step in steps)


@pytest.mark.parametrize(
    "absent, named, phrase",
    [
        (backup.LIST_SNAPSHOTS, None, "no dated database snapshot was found"),
        (backup.LIST_SNAPSHOT_IDENTITY, STAMP, f"the snapshot {STAMP} was not found"),
        (backup.LIST_SNAPSHOT_CONTENTS, STAMP, "holds no database folder"),
    ],
)
def test_a_folder_rclone_says_is_absent_is_not_a_listing_failure(
    cfg, tmp_path, rclone, absent, named, phrase
):
    """Directory not found is an absence, so the remote is not what to check."""
    recorder = Recorder(absent_labels={absent})
    refused = _restore_refused(cfg, target=tmp_path, snapshot=named, runner=recorder)
    assert refused.refusal is backup.Refusal.NO_SNAPSHOT_AVAILABLE
    assert phrase in refused.detail
    if named is not None:
        # "No snapshot exists yet" is false for a stamp that was typed, so the
        # reservation has to reach that person with a step of its own.
        from cratekit.cli import exit_codes

        steps = exit_codes.remediation_for(str(refused.refusal)).steps
        assert any("--snapshot" in step and "check the stamp" in step for step in steps)


def test_an_unmarked_snapshot_is_pulled_only_when_a_person_named_it(cfg, tmp_path, rclone):
    """Every snapshot taken before the marker existed is unmarked."""
    unmarked = {
        backup.LIST_SNAPSHOTS: STAMP + "/\n",
        backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg),
    }
    named = _restore(cfg, target=tmp_path, snapshot=STAMP, runner=Recorder(stdout_for=unmarked))
    assert named.snapshot == STAMP
    assert named.recorded_volume is None

    refused = _restore_refused(cfg, target=tmp_path, runner=Recorder(stdout_for=unmarked))
    assert refused.refusal is backup.Refusal.SNAPSHOT_IDENTITY_UNRECORDED
    assert STAMP in refused.detail


def test_a_resolved_stamp_handed_down_is_not_mistaken_for_one_a_person_named(cfg, tmp_path, rclone):
    """The verb resolves the newest stamp for its offer and passes it on."""
    unmarked = {backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg)}
    refused = _restore_refused(
        cfg, target=tmp_path, snapshot=STAMP, accept_unrecorded=False,
        runner=Recorder(stdout_for=unmarked),
    )
    assert refused.refusal is backup.Refusal.SNAPSHOT_IDENTITY_UNRECORDED


def test_a_replaced_drive_restores_the_old_volumes_snapshot_by_naming_it(cfg, tmp_path, rclone):
    """A dead drive is the reason to pull a mirror, and its replacement is a new volume."""
    plan = _restore(
        cfg, target=tmp_path, snapshot=STAMP, snapshot_volume="0000-AAAA",
        runner=marked(cfg, "0000-aaaa"),
    )
    assert plan.recorded_volume == "0000-aaaa"

    for recorder in (
        marked(cfg),
        marked(cfg, "9999-BBBB"),
        _listing(cfg),
    ):
        refused = _restore_refused(
            cfg, target=tmp_path, snapshot=STAMP, snapshot_volume="0000-AAAA", runner=recorder,
        )
        assert refused.refusal is backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH


def test_the_newest_snapshot_ignores_folders_that_are_not_stamps(cfg, rclone):
    """The same shape one function over. A stray folder sorts after every stamp."""
    recorder = Recorder(
        stdout_for={
            backup.LIST_SNAPSHOTS: "2026-01-01T000000Z/\nold/\n2026-03-01T000000Z/\nzz-scratch/\n"
        }
    )
    assert backup.latest_snapshot(cfg, runner=recorder) == "2026-03-01T000000Z"


def test_the_capture_marks_the_snapshot_after_the_database_and_never_before_it(
    cfg, db_file, rclone
):
    """The marker says "this folder holds this library's database"."""
    plan = backup.plan_backup(
        cfg, now=datetime(2026, 8, 1, tzinfo=timezone.utc),
        process_lister=no_processes, settings_dirs=())
    database = next(p for p in plan.portions if p.portion is backup_facts.Portion.DATABASE)
    labels = [c.label for c in database.commands]
    assert labels.count(backup.SNAPSHOT_IDENTITY) == 1
    assert labels.index(backup.SNAPSHOT_IDENTITY) > max(
        i for i, label in enumerate(labels) if label == backup.SNAPSHOT_DATABASE
    )
    marker = next(c for c in database.commands if c.label == backup.SNAPSHOT_IDENTITY)
    # SPELLED OUT, not built with the helper the other tests use for their INPUT.
    # An expected value that came from ``identity_marker`` would hold this to
    # whatever that function returns, which is X equals X.
    assert marker.argv[1] == "touch"
    assert marker.argv[-1] == f"{cfg.backup.db_dest_root}/{STAMP}/library-volume.f1e2-d3c4"
    assert backup.SNAPSHOT_IDENTITY in backup.TRANSFERRING_LABELS
    assert backup.dry_run_argv(marker)[-1] == "--dry-run"

    failing = Recorder(fail_labels={backup.SNAPSHOT_DATABASE})
    backup.run_backup(cfg, plan, runner=failing, publish=False)
    assert backup.SNAPSHOT_IDENTITY not in failing.labels()


def test_what_the_capture_writes_is_what_the_restore_reads(cfg, db_file, tmp_path, rclone):
    """One round trip through both ends, so the two cannot drift apart."""
    plan = backup.plan_backup(
        cfg, now=datetime(2026, 8, 1, tzinfo=timezone.utc),
        process_lister=no_processes, settings_dirs=())
    database = next(p for p in plan.portions if p.portion is backup_facts.Portion.DATABASE)
    marker = next(c for c in database.commands if c.label == backup.SNAPSHOT_IDENTITY)
    written = marker.argv[-1].rsplit("/", 1)[-1]
    recorder = _listing(cfg, identity=written + "\n")
    restored = _restore(cfg, target=tmp_path, snapshot=plan.stamp, runner=recorder)
    assert restored.recorded_volume == "f1e2-d3c4"


@pytest.mark.parametrize("identity", [None, "has/slash", "has space", "..", ".hidden"])
def test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so(
    cfg, db_file, rclone, identity
):
    """No marker is better than a marker that names a path, and silence is worse than both."""
    import dataclasses

    bare = dataclasses.replace(cfg, library=dataclasses.replace(cfg.library, volume_id=identity))
    plan = backup.plan_backup(bare, process_lister=no_processes, settings_dirs=())
    database = next(p for p in plan.portions if p.portion is backup_facts.Portion.DATABASE)
    assert backup.SNAPSHOT_IDENTITY not in [c.label for c in database.commands]
    assert backup.SNAPSHOT_IDENTITY_NOT_WRITTEN in [w["code"] for w in database.warnings]


# ── The review round. Every one of these is a finding the built in review drove. ──

LEGACY = "2026-08-01_123456"


class RemoteOf:
    """A runner over a remote described as ``{snapshot name: marker identities}``."""

    def __init__(self, cfg, holds, *, fail=()):
        self.cfg, self.holds, self.fail = cfg, dict(holds), set(fail)
        self.commands = []

    def __call__(self, command):
        self.commands.append(command)
        if command.label in self.fail:
            return backup.CommandResult(returncode=1)
        if command.label == backup.LIST_SNAPSHOTS:
            return backup.CommandResult(0, "".join(f"{name}/\n" for name in self.holds))
        if command.label == backup.LIST_SNAPSHOT_IDENTITY:
            name = command.argv[2].rstrip("/").rsplit("/", 1)[-1]
            return backup.CommandResult(0, "".join(f"{marker_for(i)}\n" for i in self.holds[name]))
        if command.label == backup.LIST_SNAPSHOT_CONTENTS:
            return backup.CommandResult(0, snapshot_listing(self.cfg))
        return backup.CommandResult(0)

    def asked_about(self):
        return [
            c.argv[2].rstrip("/").rsplit("/", 1)[-1]
            for c in self.commands
            if c.label == backup.LIST_SNAPSHOT_IDENTITY
        ]


def test_a_snapshot_the_source_system_wrote_is_still_a_name_and_still_pulled(cfg, tmp_path, rclone):
    """The source system spells its dated folder with an underscore, in local time."""
    assert backup.is_snapshot_name(LEGACY)
    assert not backup.is_stamp(LEGACY), "the narrow check is what a backup WRITES"
    assert not backup.is_snapshot_name("2026-08-01_1234567")
    assert not backup.is_snapshot_name("2026-02-30_123456")

    plan = _restore(cfg, target=tmp_path, snapshot=LEGACY, runner=RemoteOf(cfg, {LEGACY: ()}))
    assert plan.snapshot == LEGACY

    refused = _restore_refused(cfg, target=tmp_path, runner=RemoteOf(cfg, {LEGACY: ()}))
    assert refused.refusal is backup.Refusal.SNAPSHOT_IDENTITY_UNRECORDED
    assert LEGACY in refused.detail


def test_the_default_takes_the_newest_snapshot_that_is_this_librarys(cfg, tmp_path, rclone):
    """Ownership selects. It does not veto the newest and stop."""
    remote = RemoteOf(
        cfg,
        {
            "2026-08-01T000000Z": ("F1E2-D3C4",),
            "2026-08-02T000000Z": ("F1E2-D3C4",),
            "2026-08-03T000000Z": ("0000-AAAA",),
            "2026-08-04T000000Z": (),
        },
    )
    plan = _restore(cfg, target=tmp_path, runner=remote)
    assert plan.snapshot == "2026-08-02T000000Z"
    assert remote.asked_about()[:3] == [
        "2026-08-04T000000Z", "2026-08-03T000000Z", "2026-08-02T000000Z",
    ]
    assert "2026-08-01T000000Z" not in remote.asked_about()


def test_the_default_walk_is_bounded_and_the_refusal_says_how_far_it_looked(cfg, tmp_path, rclone):
    own_but_old = {"2026-01-01T000000Z": ("F1E2-D3C4",)}
    foreign = {
        f"2026-08-{day:02d}T000000Z": ("0000-AAAA",)
        for day in range(1, backup.NEWEST_WALK + 1)
    }
    remote = RemoteOf(cfg, {**own_but_old, **foreign})
    refused = _restore_refused(cfg, target=tmp_path, runner=remote)
    assert refused.refusal is backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH
    assert len(remote.asked_about()) == backup.NEWEST_WALK
    assert f"{backup.NEWEST_WALK} newest" in refused.detail
    assert "0000-aaaa" in refused.detail


def test_the_replaced_drive_identity_selects_the_newest_of_the_old_volumes(cfg, tmp_path, rclone):
    remote = RemoteOf(
        cfg,
        {
            "2026-08-01T000000Z": ("0000-AAAA",),
            "2026-08-02T000000Z": ("0000-AAAA",),
            "2026-08-03T000000Z": ("F1E2-D3C4",),
        },
    )
    plan = _restore(cfg, target=tmp_path, snapshot_volume="0000-aaaa", runner=remote)
    assert (plan.snapshot, plan.recorded_volume) == ("2026-08-02T000000Z", "0000-aaaa")


@pytest.mark.parametrize("stated", ["", "   "])
def test_an_empty_expected_identity_never_matches_an_empty_marker(cfg, tmp_path, rclone, stated):
    """A marker with nothing after its prefix reads back as the empty string."""
    recorder = _listing(cfg, identity="library-volume.\n")
    refused = _restore_refused(
        cfg, target=tmp_path, snapshot=STAMP, snapshot_volume=stated, runner=recorder,
    )
    assert refused.refusal is backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH


def test_two_markers_are_refused_without_offering_an_identity_to_pass(cfg, tmp_path, rclone):
    """The reserved step says to pass the volume the refusal names."""
    remote = RemoteOf(cfg, {STAMP: ("F1E2-D3C4", "0000-AAAA")})
    for stated in (None, "0000-AAAA", "F1E2-D3C4"):
        refused = _restore_refused(
            cfg, target=tmp_path, snapshot=STAMP, snapshot_volume=stated, runner=remote,
        )
        assert refused.refusal is backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH
        assert "No expected volume can vouch" in refused.detail


def test_a_snapshot_root_that_cannot_be_listed_is_not_reported_as_empty(cfg, tmp_path, rclone):
    remote = RemoteOf(cfg, {STAMP: ("F1E2-D3C4",)}, fail={backup.LIST_SNAPSHOTS})
    refused = _restore_refused(cfg, target=tmp_path, runner=remote)
    assert refused.refusal is backup.Refusal.SNAPSHOT_LISTING_FAILED
    assert "could not be listed" in refused.detail


def test_a_marker_that_cannot_be_written_warns_and_does_not_fail_the_backup(
    cfg, db_file, tmp_path, rclone
):
    """By the time the marker is tried, the database set has already copied."""
    settings = tmp_path / "rekordbox-settings"
    settings.mkdir()
    plan = backup.plan_backup(cfg, process_lister=no_processes, settings_dirs=(settings,))
    failing = Recorder(fail_labels={backup.SNAPSHOT_IDENTITY})
    outcome = backup.run_backup(cfg, plan, runner=failing, publish=False)
    database = next(p for p in outcome.portions if p.portion is backup_facts.Portion.DATABASE)
    assert database.ran is True
    assert backup.SNAPSHOT_SETTINGS in failing.labels(), "the settings were skipped"
    assert backup.SNAPSHOT_IDENTITY_NOT_WRITTEN in [w["code"] for w in database.warnings]


def test_the_identity_warning_can_be_asked_of_the_configuration_alone(cfg):
    """The backup verb asks it this way, because a plan's warning reaches nobody there."""
    import dataclasses

    assert backup.snapshot_identity_warning(cfg) == ()
    bare = dataclasses.replace(cfg, library=dataclasses.replace(cfg.library, volume_id=None))
    assert [w["code"] for w in backup.snapshot_identity_warning(bare)] == [
        backup.SNAPSHOT_IDENTITY_NOT_WRITTEN
    ]
