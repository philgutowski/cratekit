"""U35: the standalone utilities, the backup-age fact, and the verb declarations.

The plan gives this unit five test scenarios, and each one has a test named after
it below:

1. the set builder produces a sequence from a snapshot index with no network
   call and no write;
2. mastering leaves the source file byte-identical and archived;
3. backup with rekordbox running skips the database portion and says why;
4. backup age is readable from library-scoped state by a core component that does
   not import the backup module;
5. restore into a directory holding stale sidecars removes them before copying.

Everything here runs against a temporary directory. Nothing reaches a real
library, a real remote, or a real rekordbox database, and the two seams that
could (the process probe and the command runner) are injected in every test that
touches them. The one exception is the mastering round trip, which encodes real
audio with ffmpeg into ``tmp_path``: an audio-safety proof that stubs the encoder
proves nothing about the encoder.
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


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


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
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library):
    """A validated config naming the synthetic library and a synthetic remote.

    The destination strings are deliberately generic. A shipped artifact naming a
    real remote, bucket, or account is the thing the repository scan exists to
    reject, and a test file is a shipped artifact.
    """
    return config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(library),
                "volume_id": "F1E2-D3C4",
                "db_path": str(library / "db" / "master.db"),
            },
            "paths": {"download_staging": str(library.parent / "staging")},
            "profile": {"name": "slim"},
            "backup": {
                "remote": "remote",
                "dest": "remote:mirror",
                "archive_root": "remote:mirror-archive",
                "db_dest_root": "remote:database-snapshots",
            },
        }
    )


@pytest.fixture
def rclone_on_path(tmp_path, monkeypatch):
    """A stub rclone that resolves through the binaries override.

    A stub rather than the real program, and an override rather than a PATH edit,
    because the point of every backup test here is the DECISION, not the transfer.
    Nothing below ever executes it: the runner is injected too. What it provides
    is a resolvable absolute path, so the plan under test is the one a machine
    with rclone would build.
    """
    fake = tmp_path / "bin" / "rclone"
    fake.parent.mkdir(parents=True, exist_ok=True)
    fake.write_text("#!/bin/sh\nexit 0\n")
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("CRATEKIT_BIN_RCLONE", str(fake))
    return fake


class Recorder:
    """A runner that records commands and answers with a canned result.

    ``stdout_for`` is keyed on the command LABEL rather than on its arguments, so
    a test states what a stage returns without restating how the stage is spelled.
    """

    def __init__(self, *, stdout_for=None, fail_labels=()):
        self.commands = []
        self.stdout_for = dict(stdout_for or {})
        self.fail_labels = set(fail_labels)

    def __call__(self, command):
        self.commands.append(command)
        rc = 1 if command.label in self.fail_labels else 0
        return backup.CommandResult(
            returncode=rc, stdout=self.stdout_for.get(command.label, "")
        )

    def labels(self):
        return [c.label for c in self.commands]


def snapshot_listing(cfg, *sidecar_suffixes, extra=()):
    """Stdout for a snapshot that holds the database and the named sidecars."""
    database = config.state_path("rekordbox_db", cfg).name
    names = [database, *extra]
    names.extend(database + suffix for suffix in sidecar_suffixes)
    return "".join(name + "\n" for name in names)


def no_processes():
    return ()


def rekordbox_running():
    return ("rekordbox", "rekordboxAgent", "Finder")


# ═══════════════════════════════════════════════════════════════════════════
# The verb declarations U5 consumes
# ═══════════════════════════════════════════════════════════════════════════


def test_every_feature_inventory_row_this_unit_owns_has_a_verb():
    """Rows 29, 30 and 31, one verb each.

    The Definition of Done requires every Feature Inventory row to map to a verb
    at its stated disposition. This is the half of that check this unit can make
    on its own; the registry-wide parity check is U5's and is pending below.
    """
    assert tools.VERB_NAMES == ("setbuild", "master", "backup.run")


def test_every_verb_names_a_feature_toggle_that_actually_exists():
    """A verb whose toggle is not a module cannot be switched off.

    ``profiles.resolve`` raises for an unknown module name, so a mistyped feature
    here does not fail loudly at setup: it makes the config that tries to disable
    the module invalid, which reads to the user as their own mistake.
    """
    for spec in tools.VERBS:
        assert spec.feature in profiles.MODULES, (
            f"{spec.name} answers to the toggle {spec.feature!r}, which is not a "
            f"declared module, so nothing can turn it off"
        )


def test_no_utility_module_is_in_the_slim_profile():
    """Feature Inventory: all three rows are Module, so slim runs none of them."""
    slim = profiles.resolve("slim").modules
    for spec in tools.VERBS:
        assert spec.feature not in slim


def test_the_full_profile_enables_all_three():
    full = profiles.resolve("full").modules
    for spec in tools.VERBS:
        assert spec.feature in full


def test_the_extras_group_is_derived_and_is_none_for_all_three():
    """None is the ANSWER here, not a gap.

    What these need is an external binary, which pip cannot install and an extras
    group therefore cannot promise. Recording the binaries separately is what
    lets doctor check for the thing that is actually missing.
    """
    for spec in tools.VERBS:
        assert spec.extras is None
        assert spec.extras == profiles.install_command(spec.feature)
    assert tools.verb("master").binaries == ("ffmpeg", "ffprobe")
    assert tools.verb("backup.run").binaries == ("rclone",)


def test_the_verb_table_holds_no_imported_object():
    """KTD7: the registry entries stay inert so the import stays lazy.

    A table holding a function object imports the module that defines it the
    moment the table is built, which defeats the whole lazy-import design while
    still looking like it works: ``--help`` on a slim install would then load
    every feature module to print one line each.
    """
    for spec in tools.VERBS:
        assert isinstance(spec.module, str)
    source = (SRC_ROOT / "cratekit" / "modules" / "tools" / "__init__.py").read_text()
    imported = {
        node.module
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.ImportFrom) and node.module
    }
    assert not any(m.startswith("cratekit.modules.tools.") for m in imported), (
        "the verb table imports one of the modules it describes, so building the "
        "table is no longer lazy"
    )


def test_the_backup_verb_is_marked_destructive():
    """KTD24: the gates bind to anything that can destroy user data.

    Restore replaces a live database and its sidecars. Nothing here writes a
    database ROW, so a rule that bound the gates to database writes alone would
    leave this outside the entire safety spine, which is exactly the failure
    KTD24 names.
    """
    assert tools.verb("backup.run").destructive is True
    assert tools.verb("setbuild").destructive is False


def test_every_declared_verb_is_in_the_static_registry():
    """Armed when U5 landed, which is why these verbs carry the registry's names.

    This unit was built before the registry existed and chose its own verb
    names. Integration made the disagreement visible immediately, which is the
    countdown working: the pending entry went red the moment U5 arrived, and the
    only way to green was to reconcile. The registry won, because it is the one
    place a verb name is declared and a module that names its own verbs is how
    two spellings of the same command end up shipping.
    """
    import cratekit.cli.registry as registry

    registered = set(registry.VERB_NAMES)
    missing = set(tools.VERB_NAMES) - registered
    assert not missing, (
        f"these verbs ship but are not registered: {sorted(missing)}. A verb "
        f"outside the registry has no structured output, no exit codes, no gate "
        f"handling, and no stub on a slim install."
    )


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
    assert imports_session, (
        "cratekit.core.session has landed, so the restore path must bind to the "
        "library lock, the backup acknowledgment, and the volume identity "
        "assertion before it clears a sidecar or replaces a database (KTD24, R38)"
    )
    assert any(
        isinstance(node, ast.Attribute) and node.attr.startswith("assert_")
        for node in ast.walk(tree)
    ), "the session module is imported but no gate is asserted"


def test_every_refusal_cause_has_a_reserved_exit_code():
    """S4 applied to this unit: a refusal with no reserved code is a bare status.

    ARMED by U38. The assertion body is the one that was ported and gated; only
    the skip came off, which is what deleting the register entry is for.
    """
    import cratekit.cli.exit_codes as exit_codes

    reserved = set(exit_codes.RESERVED_CAUSES)
    causes = (
        {c.value for c in backup.REFUSALS}
        | {c.value for c in mastering.Refusal}
        | {c.value for c in backup_facts.Remedy}
    )
    assert causes <= reserved, f"unreserved causes: {sorted(causes - reserved)}"


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 1: the set builder, from a snapshot index, no network, no write
# ═══════════════════════════════════════════════════════════════════════════

TEMPLATE = NameTemplate(markers=(MarkerRule(field="lossy", literal="[MP3]"),))


def track(
    artist,
    title,
    key,
    bpm=124.0,
    genre="Deep House",
    energy=5,
    vox=None,
    path="",
):
    return setbuilder.Track(
        artist=artist,
        title=title,
        key=setbuilder.canonical_key(key),
        bpm=bpm,
        genre=genre,
        energy=energy,
        vox=vox,
        voxgender=None,
        match=setbuilder.match_key(artist, title),
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
    """The plan's first scenario, asserted on all three of its clauses.

    No network: nothing is injected and the default web lookup is None, so a call
    would have to come from inside the engine. No write: ``tmp_path`` is not
    touched at all, which the next test asserts structurally.
    """
    plan = setbuilder.build_set(
        "Alder - Anchor Work", snapshot_index, taxonomy=default_taxonomy()
    )

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


def test_the_set_builder_writes_nothing_when_no_cache_path_is_given(tmp_path, snapshot_index):
    """"No write" as a structural assertion rather than a promise."""
    before = sorted(p.name for p in tmp_path.rglob("*"))
    setbuilder.build_set("Alder - Anchor Work", snapshot_index, taxonomy=default_taxonomy())
    assert sorted(p.name for p in tmp_path.rglob("*")) == before


def test_the_same_anchor_always_produces_the_same_answer(snapshot_index):
    """Determinism is the product feature, so it is asserted rather than assumed.

    Equal scores are broken on the match key, which is stable. Without that tie
    break the order would depend on the index's own order, and an index built by
    walking a filesystem is not something a user can reproduce.
    """
    first = setbuilder.build_set("Alder - Anchor Work", snapshot_index, taxonomy=default_taxonomy())
    second = setbuilder.build_set(
        "Alder - Anchor Work", tuple(reversed(snapshot_index)), taxonomy=default_taxonomy()
    )
    assert [s.track.match for s in first.pool] == [s.track.match for s in second.pool]


def test_a_track_in_the_wrong_key_never_enters_the_pool(snapshot_index):
    anchor = setbuilder.resolve_anchor("Alder - Anchor Work", snapshot_index)
    pool = {t.match for t, _ in setbuilder.build_pool(anchor, snapshot_index)}
    assert setbuilder.match_key("Gum", "Wrong Key") not in pool


def test_a_track_in_the_right_key_at_the_wrong_tempo_never_enters_the_pool(snapshot_index):
    """Harmonic compatibility alone is not compatibility.

    100 against 124 is neither the anchor, its half, nor its double, so it is a
    mix that does not exist. The source system's engine excluded it and this must
    keep doing so.
    """
    anchor = setbuilder.resolve_anchor("Alder - Anchor Work", snapshot_index)
    pool = {t.match for t, _ in setbuilder.build_pool(anchor, snapshot_index)}
    assert setbuilder.match_key("Hazel", "Right Key Wrong Tempo") not in pool


def test_half_and_double_time_are_in_the_band():
    assert setbuilder.in_band(62.0, 124.0)
    assert setbuilder.in_band(248.0, 124.0)
    assert not setbuilder.in_band(100.0, 124.0)


def test_an_anchor_with_no_tempo_drops_the_tempo_constraint():
    """A key-only pool is a real answer; excluding everything is not."""
    assert setbuilder.in_band(90.0, None)
    assert not setbuilder.in_band(None, 124.0)


@pytest.mark.parametrize(
    "code, tier",
    [
        ("8A", "perfect"),
        ("9A", "perfect"),
        ("7A", "perfect"),
        ("8B", "perfect"),
        ("10A", "boost"),
        ("6A", "wider"),
        ("11A", "wider"),
        ("7B", "wider"),
        ("9B", "wider"),
    ],
)
def test_the_camelot_tiers_are_the_ported_ones(code, tier):
    assert setbuilder.compatible_keys("8A")[code] == tier


def test_the_wheel_wraps_at_twelve():
    tiers = setbuilder.compatible_keys("12A")
    assert tiers["1A"] == "perfect"
    assert tiers["2A"] == "boost"


@pytest.mark.parametrize("code", ["0A", "13A", "99B", "", "8C", "Am"])
def test_an_off_wheel_key_is_rejected_rather_than_normalized(code):
    """The drift this port removes.

    The source's own normalizer merely uppercased and stripped leading zeros, so
    every one of these became a confident answer for a key that is not on the
    wheel, and a candidate carrying one could join the pool through a wrap-around
    that means nothing.
    """
    assert setbuilder.canonical_key(code) == ""
    assert setbuilder.compatible_keys(code) == {}


def test_an_unowned_anchor_with_no_key_is_unresolved_rather_than_guessed(snapshot_index):
    """No network call ships here, so an unowned anchor asks rather than invents.

    A fabricated key produces a full set that is internally consistent and
    entirely wrong, which is worse than an empty answer because it looks right.
    """
    plan = setbuilder.build_set(
        "Nobody - Not In The Library", snapshot_index, taxonomy=default_taxonomy()
    )
    assert plan.anchor.unresolved
    assert plan.pool == () and plan.sequence == ()


def test_an_unowned_anchor_with_a_supplied_key_builds_but_flags_the_key(snapshot_index):
    plan = setbuilder.build_set(
        "Nobody - Not In The Library",
        snapshot_index,
        taxonomy=default_taxonomy(),
        key="8A",
        bpm=124.0,
    )
    assert plan.anchor.owned is False
    assert plan.anchor.key_needs_confirming is True
    assert plan.pool


def test_the_web_lookup_is_a_seam_that_is_absent_by_default(snapshot_index):
    """The affordance survives; the network call does not ship.

    A caller that wants enrichment supplies it. Nothing in the default path can
    reach one, which is what makes the "no network call" clause of the plan's
    scenario a property rather than a habit.
    """
    calls = []

    def lookup(artist, title):
        calls.append((artist, title))
        return {"key": "8A", "bpm": 124}

    setbuilder.build_set("Nobody - Absent", snapshot_index, taxonomy=default_taxonomy())
    assert calls == []

    plan = setbuilder.build_set(
        "Nobody - Absent", snapshot_index, taxonomy=default_taxonomy(), web_lookup=lookup
    )
    assert calls == [("", "Nobody - Absent")]
    assert plan.anchor.key == "8A"


def test_the_vocal_threshold_is_a_parameter_and_never_imported():
    """D7, asserted twice: by behaviour, and structurally.

    The source fetched this by importing an analysis module from inside the
    ranker, which raises on a slim install that has no analysis module at all.
    """
    assert setbuilder.vocal_score(9, 9, threshold=None) == 0.7
    assert setbuilder.vocal_score(9, 9, threshold=5) == 0.3
    assert setbuilder.vocal_score(9, 1, threshold=5) == 1.0

    source = (SRC_ROOT / "cratekit" / "modules" / "tools" / "setbuilder.py").read_text()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert "analysis" not in node.module
            assert "vocal" not in node.module


def test_two_vocal_forward_tracks_score_below_a_mixed_pair():
    """The clash the vocal signal exists to avoid: two lead vocals at once."""
    assert setbuilder.vocal_score(8, 8, threshold=5) < setbuilder.vocal_score(8, 2, threshold=5)


def test_genre_affinity_comes_from_the_declared_taxonomy(snapshot_index):
    """R19: the soft genre prior is the user's declaration, not a baked-in table.

    Proved by MOVING the declaration and watching the score move with it. The
    source hardcoded one person's genre families as substring rules, so a library
    that is not house-centric got a soft prior describing somebody else's record
    collection, and no configuration could change it.
    """
    from dataclasses import replace

    taxonomy = default_taxonomy()
    anchor = setbuilder.resolve_anchor("Alder - Anchor Work", snapshot_index)
    pool = setbuilder.build_pool(anchor, snapshot_index)
    assert pool, "nothing was pooled, so this would prove nothing"

    baseline = setbuilder.rank(pool, anchor, taxonomy=taxonomy)
    shifted = setbuilder.rank(
        pool,
        anchor,
        taxonomy=replace(
            taxonomy, family=replace(taxonomy.family, same_genre=0.0, unrelated=1.0)
        ),
    )
    assert [s.score for s in baseline] != [s.score for s in shifted], (
        "changing the taxonomy's declared affinities changed no score, so the "
        "ranker is not reading the declaration"
    )


def test_a_genre_signal_of_zero_weight_removes_genre_from_the_score(snapshot_index):
    """The soft prior is soft: it is a weight, never a hard exclude.

    A candidate in the right key at the right tempo but the wrong genre must
    still be rankable, because "wrong genre" is an opinion and "wrong key" is
    arithmetic.
    """
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


def test_unknown_energy_scores_neutral_rather_than_zero():
    """None means unknown. A track with no reading is not a quiet track."""
    assert setbuilder.energy_score(None, 5, "before") == 0.5
    assert setbuilder.energy_score(5, None, "after") == 0.5


def test_weights_that_do_not_sum_to_one_are_refused():
    """Two differently normalized runs produce scores nobody can compare."""
    with pytest.raises(ValueError, match="sum to 1.0"):
        setbuilder.Weights(harmonic=0.9, bpm=0.9, genre=0.0, energy=0.0, vocal=0.0)


# ── The index: parsing, deduplication, and the cache ─────────────────────────


def test_the_index_reads_the_key_and_tempo_out_of_the_declared_head():
    """Not a private regular expression. The template owns the shape (U4)."""
    entry = setbuilder.parse_entry(
        {
            "title": "08A - 124 - Real Title",
            "artist": "Alder",
            "genre": "Deep House",
            "initialkey": None,
            "energylevel": "6",
            "voxlevel": "2",
            "voxgender": None,
        },
        template=TEMPLATE,
    )
    assert entry.key == "8A"
    assert entry.bpm == 124.0
    assert entry.title == "Real Title"


def test_a_marked_lossy_title_loses_its_marker_along_with_the_head():
    """The defect the private regular expression carried.

    A stripper that left the marker behind produced a "clean" title that matched
    nothing, so a marked copy and its lossless twin never deduplicated against
    each other.
    """
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
    assert (
        setbuilder.parse_entry({"title": "Just A Title", "artist": "A"}, template=TEMPLATE)
        is None
    )


def test_the_index_collapses_duplicate_works(tmp_path):
    """A re-import and an extended edit of one work are one index entry.

    Without the collapse a user asking for eight companions gets the same track
    four times, which is the failure the source's normalized match key exists to
    prevent.
    """
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


def test_a_cache_written_by_another_build_is_discarded_rather_than_deserialized(tmp_path):
    """Discarding costs one scan. Deserializing costs a crash mid-run."""
    root = tmp_path / "music"
    root.mkdir()
    (root / "a.flac").write_bytes(b"")
    cache = tmp_path / "cache.json"
    cache.write_text(json.dumps({"cache_version": 0, "entries": {"x": {"nope": 1}}}))

    index = setbuilder.build_index(
        root,
        template=TEMPLATE,
        cache_path=cache,
        reader=lambda p: {"title": "08A - 124 - Title", "artist": "Alder"},
    )
    assert [t.title for t in index] == ["Title"]


def test_a_cache_parsed_under_another_template_is_discarded(tmp_path):
    """A cached entry is the OUTPUT of a parse, and the template is its other input.

    Changing the lossy marker changes every marked file's clean title and match
    key while touching no file's modification time, so a cache keyed on path and
    time alone would serve the old title for ever. Driven with the marker moving
    from one literal to another over a file that never changes.
    """
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
    """A stamp that moved on its own would discard the cache on every run.

    The template holds a frozenset, whose repr follows string hashing and so
    differs between two runs of one build. Asserted against a literal rather
    than against a second call in this process, which would agree with itself
    under any hash seed and prove nothing.

    A stand-in carries the set, because the real template refuses most optional
    sets at construction and one member cannot show an ordering.
    """
    import dataclasses

    @dataclasses.dataclass(frozen=True)
    class Shape:
        head_optional: frozenset[str]
        head_sep: str = " - "

    stamp = setbuilder._template_stamp(Shape(frozenset({"key", "bpm", "energy", "vox"})))
    assert stamp == "head_optional=['bpm', 'energy', 'key', 'vox'];head_sep=' - '"
    assert setbuilder._template_stamp(TEMPLATE) != setbuilder._template_stamp(NameTemplate())


def test_a_cache_with_no_template_stamp_is_discarded(tmp_path):
    root = tmp_path / "lib"
    root.mkdir()
    audio = root / "a.flac"
    audio.touch()
    cache = tmp_path / "cache.json"
    stale = {"mtime": audio.stat().st_mtime, "track": None}
    cache.write_text(
        json.dumps({"cache_version": setbuilder.CACHE_VERSION, "entries": {str(audio): stale}})
    )
    index = setbuilder.build_index(
        root,
        template=TEMPLATE,
        cache_path=cache,
        reader=lambda p: {"title": "08A - 124 - Title", "artist": "Alder"},
    )
    assert [t.title for t in index] == ["Title"], "an unstamped cache was trusted"


def _one_file_library(tmp_path):
    root = tmp_path / "lib"
    root.mkdir()
    audio = root / "a.flac"
    audio.write_bytes(b"first")
    return root, audio, tmp_path / "state" / "cache.json"


GOOD = {"title": "08A - 124 - Title", "artist": "Alder"}


def test_a_read_that_returned_nothing_is_never_cached_as_the_files_answer(tmp_path):
    """Found by the built in review, and newly reachable once a verb passed a path.

    The shared reader answers None for an absent tag and for a file it could not
    open alike. One momentary failure, cached under an unchanged time, dropped an
    analyzed track from the index until somebody touched the file.
    """
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
    """An unmounted volume leaves an empty directory where the library was.

    Creating a state directory inside that leftover mountpoint is how the real
    volume comes to mount under a second name, and every configured path misses.
    """
    root = tmp_path / "lib"
    root.mkdir()
    cache = root / ".state" / "cache.json"
    assert setbuilder.build_index(root, template=TEMPLATE, cache_path=cache) == ()
    assert list(root.iterdir()) == []


def test_the_index_cache_has_a_declared_home_in_the_state_inventory(cfg):
    """A module composing its own path under a state root invents a file the
    inventory cannot find, snapshot, or clear."""
    entry = config.state_file("setbuilder_index_cache")
    assert entry.root is config.StateRoot.LIBRARY
    assert entry.snapshot is config.SnapshotRole.NEVER_RESTORED
    assert config.state_path("setbuilder_index_cache", cfg).is_relative_to(cfg.library.root)


def test_the_index_reads_tags_only_through_the_shared_container_reader():
    """S5: one reader, one container classification, no second opinion.

    A consumer that opened audio with its own container guess is how an AIFF gets
    a bare ID3 stream written over its header, so the index is held to the same
    single path as the writer.
    """
    source = (SRC_ROOT / "cratekit" / "modules" / "tools" / "setbuilder.py").read_text()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert not alias.name.startswith("mutagen")
        if isinstance(node, ast.ImportFrom) and node.module:
            assert not node.module.startswith("mutagen")


def test_the_index_reads_a_real_file_through_the_real_reader(tmp_path):
    """The one end-to-end proof, because the injected reader proves only itself.

    Encodes a real FLAC, writes real tags through the production writer, and
    reads them back through the production index. Without this, every test above
    is a test of a dictionary.
    """
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        pytest.fail(
            "ffmpeg is required to prove the index reads a real audio file. "
            "This fails rather than skips because a skipped end-to-end proof is "
            "indistinguishable from a passing one in every summary anybody reads."
        )
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

    assert write_tags(
        path,
        {
            "title": "08A - 124 - Real Title",
            "artist": "Alder",
            "genre": "Deep House",
            "energylevel": 6,
            "voxlevel": 2,
        },
    )
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


def test_no_structured_payload_in_this_unit_carries_a_tempo_TAG_key(snapshot_index):
    """R17 at the serialization boundary, checked against the guard's own set.

    A payload spelling its tempo the way a Vorbis comment spells it is one
    copy-paste from a tag write, and a tempo tag reaches rekordbox on import
    exactly as a grid element does. The forbidden set is IMPORTED from the
    invariant suite rather than restated, so a spelling added there starts
    biting here on the same commit.
    """
    from tests.test_no_beatgrid_ever import FORBIDDEN_TAG_KEYS

    def keys(value):
        if isinstance(value, dict):
            for key, inner in value.items():
                yield key
                yield from keys(inner)
        elif isinstance(value, list):
            for item in value:
                yield from keys(item)

    payload = setbuilder.as_payload(
        setbuilder.build_set("Alder - Anchor Work", snapshot_index, taxonomy=default_taxonomy())
    )
    offenders = sorted(set(keys(payload)) & FORBIDDEN_TAG_KEYS)
    assert not offenders, f"the set-builder payload carries tempo tag keys: {offenders}"


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 2: mastering leaves the source byte-identical and archived
# ═══════════════════════════════════════════════════════════════════════════


def _synth_wav(tmp_path: Path, name: str = "set.wav", seconds: int = 2) -> Path:
    """A short real recording. Silence would measure as negative infinity."""
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        pytest.fail(
            "ffmpeg is required to prove that mastering leaves the source "
            "unmodified. This fails rather than skips because a skipped "
            "audio-safety proof reads as a passing one."
        )
    out = tmp_path / name
    proc = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=220:r=44100",
         "-t", str(seconds), "-c:a", "pcm_s16le", str(out)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0 and out.exists(), proc.stderr[-400:]
    return out


def test_mastering_leaves_the_source_byte_identical_and_archived(tmp_path):
    """The plan's second scenario, and R18's headline.

    The source of a master is a recording of a performance that happened once.
    Both halves are asserted: the bytes are unchanged, and a verified copy exists
    before anything else runs.
    """
    source = _synth_wav(tmp_path)
    before = mastering.digest(source)
    before_stat = source.stat()

    report = mastering.master(source)

    assert mastering.digest(source) == before
    assert source.stat().st_size == before_stat.st_size
    assert report.archived_to is not None and report.archived_to.is_file()
    assert mastering.digest(report.archived_to) == before
    assert report.archived_to.parent.name == mastering.ARCHIVE_DIRNAME
    assert report.output.is_file() and report.output.suffix == ".flac"


def test_mastering_reports_before_and_after_loudness(tmp_path):
    """A result nobody can check is a result nobody should trust."""
    report = mastering.master(_synth_wav(tmp_path))
    assert report.before.integrated_lufs is not None
    assert report.after.integrated_lufs is not None
    assert report.after.integrated_lufs == pytest.approx(
        mastering.DEFAULT_SETTINGS.target_lufs, abs=1.5
    )
    assert report.bit_depth.startswith("16-bit")


def test_mastering_leaves_no_intermediate_behind(tmp_path):
    """A multi-gigabyte scratch file beside the recording fills a volume."""
    mastering.master(_synth_wav(tmp_path))
    leftovers = [p.name for p in tmp_path.rglob("*.cratekit-drift.wav")]
    assert leftovers == []


def test_mastering_refuses_to_overwrite_an_existing_master(tmp_path):
    """The source passes an unconditional overwrite flag.

    A second run at a different target loudness therefore replaces a master the
    user may already have kept, and the settings that produced the first one are
    recorded nowhere.
    """
    source = _synth_wav(tmp_path)
    mastering.output_path(source).write_bytes(b"already here")
    with pytest.raises(mastering.MasteringRefused) as excinfo:
        mastering.master(source)
    assert excinfo.value.refusal is mastering.Refusal.OUTPUT_EXISTS


def test_an_archive_entry_with_the_same_name_and_different_content_refuses(tmp_path):
    """Recorders name files by counter, so this is the normal case.

    The source skips the copy when the name is taken, which leaves the second
    recording unarchived while reporting that it is safe.
    """
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
    """Order is the safety property, so it is asserted rather than described.

    Archiving after the first stage means a crash between them leaves a
    half-written intermediate and no verified copy, which is the one state this
    module exists to make impossible.
    """
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
    """An incomplete measurement drops the filter out of linear mode silently.

    In its dynamic mode it compresses to hit the target instead of moving the
    whole set, so the output is flatter with nothing reported.
    """
    with pytest.raises(mastering.MasteringRefused) as excinfo:
        mastering.apply_filter(mastering.DEFAULT_SETTINGS, mastering.Loudness())
    assert excinfo.value.refusal is mastering.Refusal.ENCODER_FAILED
    assert "linear" in excinfo.value.detail


def test_the_loudness_report_is_parsed_as_json_not_grepped():
    """The defect this port closes.

    The source greps each key across the whole stream and keeps the last hit, so
    a value from the measurement block pairs with a value from the apply block
    and the resulting "measurement" describes no signal that ever existed.
    """
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


@pytest.mark.parametrize("window", [2, 1, 303, 64])
def test_an_impossible_drift_window_is_refused_at_construction(window):
    """Otherwise ffmpeg fails minutes into an encode, naming its own filter."""
    with pytest.raises(ValueError):
        mastering.Settings(drift_window=window)


def test_a_positive_true_peak_ceiling_is_refused():
    with pytest.raises(ValueError, match="ceiling"):
        mastering.Settings(true_peak_db=1.0)


def test_an_unsupported_container_is_refused_rather_than_attempted(tmp_path):
    stray = tmp_path / "notes.txt"
    stray.write_text("not audio")
    with pytest.raises(mastering.MasteringRefused) as excinfo:
        mastering.master(stray)
    assert excinfo.value.refusal is mastering.Refusal.SOURCE_UNSUPPORTED


def test_joining_split_parts_quotes_a_path_containing_an_apostrophe(tmp_path):
    """ffmpeg's concat list unescapes a doubled quote; a raw one truncates.

    Track and set titles contain apostrophes constantly, so the naive spelling
    fails on ordinary input rather than on an exotic one.
    """
    part = tmp_path / "it's part one.wav"
    part.write_bytes(b"")
    written = {}

    def runner(command):
        listing = Path(command.argv[command.argv.index("-i") + 1])
        written["text"] = listing.read_text()
        # THE STAND-IN WRITES THE DESTINATION, because a real ffmpeg does and
        # U44 made ``concatenate`` read its own output. Before that, a zero exit
        # status was taken as proof the join happened and the path was returned
        # unread, so this runner could report success over a file that was never
        # created. Leaving the write out here would make the fixture assert that
        # the join is unchecked, which is the behaviour that was removed.
        Path(command.argv[-1]).write_bytes(b"joined")
        return mastering.CommandResult(returncode=0)

    mastering.concatenate([part], tmp_path / "joined.wav", runner=runner)
    assert "it''s part one.wav" in written["text"]


def test_a_join_that_exits_zero_and_writes_nothing_refuses_rather_than_returning(tmp_path):
    """Closes B3 in ``docs/mutation/u44-author.md``.

    The test above adapted its stand-in to the check U44 added and asserted
    nothing about the check itself, so the guard could be removed and the file
    stayed green. This is the row's premise: a zero exit status over no output is
    a refusal, not a path.
    """
    part = tmp_path / "part.wav"
    part.write_bytes(b"")
    destination = tmp_path / "joined.wav"

    def silent_success(command):
        return mastering.CommandResult(returncode=0)

    with pytest.raises(mastering.MasteringRefused) as excinfo:
        mastering.concatenate([part], destination, runner=silent_success)
    assert excinfo.value.refusal is mastering.Refusal.ENCODER_FAILED
    assert not destination.exists()


def test_the_mastering_payload_carries_a_version(tmp_path):
    report = mastering.master(_synth_wav(tmp_path))
    payload = mastering.as_payload(report)
    assert payload["payload_version"] == mastering.PAYLOAD_VERSION
    assert payload["archived_to"]


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 3: backup with rekordbox running skips the database and says why
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def library_with_database(cfg):
    """A library whose configured database path actually holds a file."""
    database = config.state_path("rekordbox_db", cfg)
    database.parent.mkdir(parents=True, exist_ok=True)
    database.write_bytes(b"SQLite format 3\x00")
    return database


#: Four dated folders older than any completed mirror a test below records, in
#: the spelling ``stamp_for`` writes, because the rotation compares names with
#: the record's stamp and a word like "one" sorts after every date.
SETTLED_ARCHIVES = "".join(f"2026-0{month}-01T000000Z/\n" for month in (1, 2, 3, 4))


@pytest.fixture
def a_completed_mirror(cfg):
    """A completed mirror to this destination on record, so folders can be settled.

    The rotation purges only what is older than the last completed mirror
    and with no record it purges nothing. A test about WHICH folders a
    purge takes therefore has to start where a second backup starts.
    """
    when = datetime(2026, 6, 1, tzinfo=timezone.utc)
    backup_facts.record(
        cfg, backup_facts.Portion.FILES, completed_at=when, destination=str(cfg.backup.dest)
    )
    return when


def test_backup_with_rekordbox_running_skips_the_database_and_says_why(
    cfg, library_with_database, rclone_on_path
):
    """The plan's third scenario.

    Both halves matter. The database portion refuses, and the file mirror still
    runs: a backup that abandoned everything because rekordbox was open would
    mean a user who never quits rekordbox never backs up their music either.
    """
    plan = backup.plan_backup(cfg, process_lister=rekordbox_running)

    database = plan.portion(backup_facts.Portion.DATABASE)
    assert database.will_run is False
    assert database.refusal is backup.Refusal.REKORDBOX_RUNNING
    assert "rekordbox" in database.detail and "rekordboxAgent" in database.detail
    assert database.commands == ()

    assert plan.portion(backup_facts.Portion.FILES).will_run is True


def test_the_background_agent_alone_is_enough_to_refuse(cfg, library_with_database, rclone_on_path):
    """The fact the source system's original check missed.

    The agent keeps the database handle and mutates the library through Cloud
    Library Sync with the application window closed, which is vendor-confirmed. A
    check watching only the visible application passes while the database is
    being written.
    """
    plan = backup.plan_backup(cfg, process_lister=lambda: ("rekordboxAgent",))
    assert plan.portion(backup_facts.Portion.DATABASE).refusal is backup.Refusal.REKORDBOX_RUNNING


def test_an_unrelated_process_whose_name_contains_rekordbox_does_not_refuse(
    cfg, library_with_database, rclone_on_path
):
    """P7: a guard that refuses correct situations is one people learn to bypass."""
    plan = backup.plan_backup(cfg, process_lister=lambda: ("rekordbox-notes-editor",))
    assert plan.portion(backup_facts.Portion.DATABASE).will_run is True


def test_the_process_probe_cannot_be_switched_off_by_the_environment():
    """The source lets an environment variable fake its answer.

    That variable is readable in production too, so the one guard standing
    between a live database and a torn copy is switchable by anything that can
    set an environment variable. The seam here is a parameter, which a running
    process cannot reach.
    """
    source = (SRC_ROOT / "cratekit" / "modules" / "tools" / "backup.py").read_text()
    tree = ast.parse(source)
    reads = [
        ast.unparse(node)
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and node.attr in {"getenv", "environ"}
    ]
    assert reads == [], f"the backup module reads the environment: {reads}"


def test_the_database_fileset_never_rides_the_file_mirror(cfg, library_with_database, rclone_on_path):
    """A live mirror of an open database captures a torn copy.

    The database comes only from the gated dated snapshot, so the mirror must
    exclude it and both of its sidecars, and those come from the state inventory
    rather than from a list typed here.
    """
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    mirror = plan.portion(backup_facts.Portion.FILES).commands[0]
    excluded = {
        mirror.argv[i + 1] for i, arg in enumerate(mirror.argv) if arg == "--exclude"
    }
    for path in backup.database_fileset(cfg):
        assert "/" + str(path.relative_to(cfg.library.root)) in excluded


def test_the_database_fileset_is_derived_from_the_state_inventory(cfg):
    """A hand-kept list is how a capture loses the write-ahead log."""
    names = [p.name for p in backup.database_fileset(cfg)]
    base = config.state_path("rekordbox_db", cfg).name
    assert names[0] == base
    assert names[1:] == [base + s.suffix for s in config.SQLITE_SIDECARS]


def test_the_mirror_moves_overwritten_files_into_a_dated_archive_first(
    cfg, library_with_database, rclone_on_path
):
    """Without it, a sync propagates local deletions to the only other copy."""
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    mirror = plan.portion(backup_facts.Portion.FILES).commands[0]
    assert "--backup-dir" in mirror.argv
    assert mirror.argv[mirror.argv.index("--backup-dir") + 1].endswith(plan.stamp)


def test_the_dated_stamp_sorts_as_text_in_chronological_order():
    """The prune and the restore both pick "newest" by string order.

    A local-time stamp reverses that order for one hour a year when the clock
    goes back, and the prune would then delete the newest archive.
    """
    earlier = backup.stamp_for(datetime(2026, 1, 1, 12, tzinfo=UTC))
    later = backup.stamp_for(datetime(2026, 1, 1, 13, tzinfo=UTC))
    assert earlier < later
    # An hour that repeats in local time still sorts forward here.
    autumn_first = backup.stamp_for(datetime(2026, 11, 1, 5, 30, tzinfo=UTC))
    autumn_second = backup.stamp_for(datetime(2026, 11, 1, 6, 30, tzinfo=UTC))
    assert autumn_first < autumn_second


def test_every_destination_in_every_command_traces_back_to_configuration(
    cfg, library_with_database, rclone_on_path
):
    """R1, and this unit's own requirement: the source hardcodes four of these.

    Asserted by construction rather than by grepping for the strings that used to
    be there. Every argument that names a remote (rclone spells one
    ``<remote>:<path>``) must be prefixed by one of the four configured values,
    so a destination that came from anywhere else fails here even if nobody
    thought to search for it.
    """
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


def test_the_backup_source_contains_no_remote_literal():
    """The other half: nothing in the source spells a destination at all."""
    source = (SRC_ROOT / "cratekit" / "modules" / "tools" / "backup.py").read_text()
    offenders = [
        node.value
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        # A remote reference is `name:path`. Excluded: the interpolated forms,
        # which carry the configured value, and prose, which has no colon
        # followed immediately by a path segment.
        and re.fullmatch(r"[A-Za-z0-9_-]+:[A-Za-z0-9_./-]*", node.value)
    ]
    assert not offenders, f"remote literals survive in the source: {offenders}"


def test_an_unconfigured_remote_refuses_before_anything_runs(library, rclone_on_path):
    """No remote means no portion could run, so it is one refusal, not two."""
    unconfigured = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(library),
                "volume_id": "F1E2-D3C4",
                "db_path": str(library / "db" / "master.db"),
            },
            "paths": {"download_staging": str(library.parent / "staging")},
            "profile": {"name": "slim"},
        }
    )
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_backup(unconfigured)
    assert excinfo.value.refusal is backup.Refusal.REMOTE_NOT_CONFIGURED


def test_a_missing_rclone_refuses_every_portion_with_one_named_cause(
    cfg, library_with_database, monkeypatch, tmp_path
):
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))
    monkeypatch.delenv("CRATEKIT_BIN_RCLONE", raising=False)
    monkeypatch.setattr(backup.binaries, "fallback_dirs", lambda: ())
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    assert {p.refusal for p in plan.portions} == {backup.Refusal.RCLONE_MISSING}
    assert all(p.commands == () for p in plan.portions)


def test_the_dry_run_and_the_real_run_come_from_one_plan(
    cfg, library_with_database, rclone_on_path
):
    """The preview cannot describe a run different from the one that follows it.

    The source builds its dry run's argument list separately from its real one,
    so a change to either can silently make the preview wrong.
    """
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


def test_a_dry_run_publishes_no_backup_age(cfg, library_with_database, rclone_on_path):
    """A preview that recorded an age would report a library protected by a run
    that copied not one byte."""
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    backup.run_backup(cfg, plan, runner=Recorder(), dry_run=True)
    assert backup.backup_facts.read_facts(cfg) == {}


def test_a_dry_run_never_purges(
    cfg, library_with_database, rclone_on_path, a_completed_mirror
):
    recorder = Recorder(stdout_for={backup.PRUNE_ARCHIVE: SETTLED_ARCHIVES})
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    backup.run_backup(cfg, plan, runner=recorder, dry_run=True)
    assert backup.PRUNE_ARCHIVE_FOLDER not in recorder.labels()


def test_the_prune_keeps_the_newest_and_removes_the_rest(
    cfg, library_with_database, rclone_on_path, a_completed_mirror
):
    recorder = Recorder(
        stdout_for={backup.PRUNE_ARCHIVE: "2026-01-01T000000Z/\n2026-02-01T000000Z/\n2026-03-01T000000Z/\n"}
    )
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    backup.run_backup(cfg, plan, runner=recorder)

    purged = [c for c in recorder.commands if c.label == backup.PRUNE_ARCHIVE_FOLDER]
    assert len(purged) == 2
    assert all("2026-03-01T000000Z" not in c.argv[-1] for c in purged)


def test_the_retention_the_plan_declared_is_the_retention_the_run_applies(
    cfg, library_with_database, rclone_on_path, a_completed_mirror
):
    """One decision, made once.

    Taking the retention again at execution is two places for one number, and the
    two can disagree: a plan built to keep three, executed with a keep of one,
    deletes two archives the preview said it would leave alone.
    """
    recorder = Recorder(stdout_for={backup.PRUNE_ARCHIVE: SETTLED_ARCHIVES})
    plan = backup.plan_backup(cfg, process_lister=no_processes, archive_keep=3)
    assert plan.archive_keep == 3
    backup.run_backup(cfg, plan, runner=recorder)
    assert len([c for c in recorder.commands if c.label == backup.PRUNE_ARCHIVE_FOLDER]) == 1


def test_a_negative_retention_never_prunes_at_all(cfg, library_with_database, rclone_on_path):
    """For a user with room who would rather keep every run's rollback."""
    plan = backup.plan_backup(cfg, process_lister=no_processes, archive_keep=-1)
    labels = [c.label for c in plan.portion(backup_facts.Portion.FILES).commands]
    assert backup.PRUNE_ARCHIVE not in labels


def test_the_prune_runs_only_after_the_mirror_succeeded(
    cfg, library_with_database, rclone_on_path
):
    """Each dated folder holds one run's rollback.

    Pruning before the new folder exists leaves a window with no rollback at all,
    so a failed mirror must never reach the prune.
    """
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
    cfg, library_with_database, rclone_on_path
):
    """The drive the finding behind this unit recorded as never performed.

    A remote that refuses ``lsf`` gave a successful backup, a fresh published age
    and NO indication that the rotation had stopped, so dated folders accumulated
    for as long as the condition lasted. Both halves are asserted here in one
    test: the portion still ran and the age is still published, because a stopped
    rotation is not a failed backup, AND the portion now says the rotation did
    not happen.

    The message is built from the return code rather than from ``stderr``,
    because ``Recorder`` sets no ``stderr`` and a guard that read one would be
    asserting the empty string.
    """
    recorder = Recorder(fail_labels={backup.PRUNE_ARCHIVE})
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=recorder)

    files = _files_outcome(outcome)
    assert files.ran is True
    assert outcome.ok is True
    assert backup.backup_facts.ages(cfg)[0].state is not backup_facts.AgeState.NEVER_RECORDED

    assert [w["code"] for w in files.warnings] == [backup.ARCHIVE_LISTING_FAILED]
    assert "accumulate" in files.warnings[0]["message"]
    assert backup.PRUNE_ARCHIVE_FOLDER not in recorder.labels(), (
        "a failed listing purged something, which is how a prune removes the "
        "only archive there is"
    )


def test_a_failed_purge_reports_how_many_folders_survived_it(
    cfg, library_with_database, rclone_on_path, a_completed_mirror
):
    """The second condition, which has a different fix from the first.

    A listing this account cannot get is a remote or credential problem and
    nothing was removed. A purge that failed on a folder the listing named is
    that folder, and the rest of the rotation happened. One code over both would
    leave the difference in the message, which is the only part nothing can
    branch on.
    """
    recorder = Recorder(
        stdout_for={
            backup.PRUNE_ARCHIVE: "2026-01-01T000000Z/\n2026-02-01T000000Z/\n2026-03-01T000000Z/\n"
        },
        fail_labels={backup.PRUNE_ARCHIVE_FOLDER},
    )
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=recorder)

    files = _files_outcome(outcome)
    assert files.ran is True
    assert [w["code"] for w in files.warnings] == [backup.ARCHIVE_PURGE_FAILED]
    assert "2 dated folder(s)" in files.warnings[0]["message"], files.warnings
    assert files.results[0].returncode == 0, (
        "the listing is reported as having failed, so the two conditions are "
        "not being told apart"
    )


def test_a_prune_that_completed_warns_about_nothing(
    cfg, library_with_database, rclone_on_path, a_completed_mirror
):
    """The companion to the two above, and not an assertion of absence.

    A guard that only checked ``warnings == ()`` would be satisfied by a prune
    that never ran, by a portion that refused and by a key that was never
    populated. So the rotation is asserted to have HAPPENED in the same test:
    three folders listed, two purged, the newest kept.
    """
    recorder = Recorder(
        stdout_for={
            backup.PRUNE_ARCHIVE: "2026-01-01T000000Z/\n2026-02-01T000000Z/\n2026-03-01T000000Z/\n"
        }
    )
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=recorder)

    purged = [c for c in recorder.commands if c.label == backup.PRUNE_ARCHIVE_FOLDER]
    assert len(purged) == 2
    assert all(w == () for w in (p.warnings for p in outcome.portions))


def test_the_portion_with_no_prune_command_carries_no_warning(
    cfg, library_with_database, rclone_on_path
):
    """The database portion never prunes, so it has nothing to report."""
    recorder = Recorder(fail_labels={backup.PRUNE_ARCHIVE})
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=recorder)

    database = [
        p for p in outcome.portions if p.portion is backup_facts.Portion.DATABASE
    ][0]
    assert database.warnings == ()


def test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing(
    cfg, library_with_database, rclone_on_path
):
    """The branch this replaced ran the listing and read nothing.

    A preview whose remote refuses ``lsf`` was describing a rotation it had
    already discovered it could not perform.
    """
    recorder = Recorder(fail_labels={backup.PRUNE_ARCHIVE})
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=recorder, dry_run=True)

    assert [w["code"] for w in _files_outcome(outcome).warnings] == [
        backup.ARCHIVE_LISTING_FAILED
    ]
    assert backup.PRUNE_ARCHIVE_FOLDER not in recorder.labels()


def test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing(
    cfg, library_with_database, rclone_on_path, a_completed_mirror
):
    """What the fold must not have changed.

    ``purge`` defaults to the real rotation, so this is the guard that says the
    rehearsal still passes False and that suppressing the purge did not start
    reporting a rotation that was never attempted.
    """
    recorder = Recorder(stdout_for={backup.PRUNE_ARCHIVE: SETTLED_ARCHIVES})
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=recorder, dry_run=True)

    assert _files_outcome(outcome).warnings == ()
    assert backup.PRUNE_ARCHIVE_FOLDER not in recorder.labels()


def test_a_failed_portion_publishes_no_age(cfg, library_with_database, rclone_on_path):
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    backup.run_backup(cfg, plan, runner=Recorder(fail_labels={backup.MIRROR}))
    facts = backup_facts.read_facts(cfg)
    assert backup_facts.Portion.FILES not in facts


def test_no_provider_specific_flag_is_baked_into_the_commands(
    cfg, library_with_database, rclone_on_path
):
    """The remote is configuration, so a one-provider flag belongs in rclone's own
    configuration rather than in a command this builds for every provider."""
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    for entry in plan.portions:
        for command in entry.commands:
            assert not any(arg.startswith("--drive-") for arg in command.argv)


def test_the_settings_directories_ride_the_database_portion(
    cfg, library_with_database, rclone_on_path, tmp_path
):
    """They hold the pointer to where the database lives.

    A database snapshot restored without them can be restored to a rekordbox that
    then looks somewhere else entirely, so they inherit the database's gate
    rather than becoming a portion nobody was warned about. The directories are
    INJECTED so the assertion is the same on every platform: resolving them from
    the running machine would make this test pass on one and vacuously skip on
    another.
    """
    settings = tmp_path / "settings"
    settings.mkdir()
    plan = backup.plan_backup(
        cfg, process_lister=no_processes, settings_dirs=(settings,)
    )
    labels = [c.label for c in plan.portion(backup_facts.Portion.DATABASE).commands]
    assert backup.SNAPSHOT_SETTINGS in labels


def test_the_settings_directories_are_skipped_when_rekordbox_is_running(
    cfg, library_with_database, rclone_on_path, tmp_path
):
    """They share the database's gate because a live application is writing them."""
    settings = tmp_path / "settings"
    settings.mkdir()
    plan = backup.plan_backup(
        cfg, process_lister=rekordbox_running, settings_dirs=(settings,)
    )
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


# ═══════════════════════════════════════════════════════════════════════════
# The rotation counts a run, not an attempt
# ═══════════════════════════════════════════════════════════════════════════


class ArchiveRemote:
    """A runner that HOLDS the dated archive folders, the way a remote does.

    ``Recorder`` answers a listing with a canned string, which cannot reproduce
    the retried portion at all: the defect is that one attempt's purge removes a folder an
    earlier attempt wrote, so the folders have to outlive a single run. Here a
    mirror writes the folder its ``--backup-dir`` names, as rclone does the
    moment it overwrites one file, a listing reads the set back, and a purge
    removes from it.
    """

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
    plan = backup.plan_backup(cfg, now=at, process_lister=no_processes, archive_keep=keep)
    return backup.run_backup(cfg, plan, runner=remote, now=at)


ROTATION_DAY = datetime(2026, 9, 1, 12, 0, 0, tzinfo=timezone.utc)


def _stamp(days: float) -> str:
    return backup.stamp_for(ROTATION_DAY + timedelta(days=days))


def test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote(
    cfg, library_with_database, rclone_on_path
):
    """The retried portion's closing condition, driven against a remote that remembers.

    The failed attempt overwrote files before it died, and its dated folder holds
    the only copies of what they were. At a keep of one, counting ATTEMPTS, the
    retry that succeeds purges it. Counting the RUN, both attempts are one slot.
    The settled folder from the run before still rotates out, so this is the
    rotation still working and not a rotation that stopped.
    """
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


def test_the_run_after_a_retried_one_rotates_every_attempt_out_together(
    cfg, library_with_database, rclone_on_path
):
    """Held is not kept for ever. One run is one slot, and the slot rotates."""
    remote = ArchiveRemote()
    _mirror_at(cfg, remote, ROTATION_DAY)
    remote.fail_mirror = True
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1))
    remote.fail_mirror = False
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1, hours=2))

    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=2))
    assert remote.folders == {_stamp(2)}


def test_a_remote_with_no_completed_mirror_on_record_is_never_purged(
    cfg, library_with_database, rclone_on_path
):
    """No record is not a record of nothing (METHOD's first pattern).

    This is a first backup onto a remote something else already mirrored to, or a
    first attempt that failed: with no completed mirror on record, no folder can
    be called settled, because any of them may be what an unfinished run wrote.
    The next completed run has a record and rotates them.
    """
    remote = ArchiveRemote("2026-08-01T000000Z", "2026-08-02T000000Z", fail_mirror=True)
    _mirror_at(cfg, remote, ROTATION_DAY)
    remote.fail_mirror = False
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(hours=1))
    assert remote.purged == []

    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1))
    assert remote.folders == {_stamp(1)}


def test_a_completed_mirror_to_another_destination_settles_nothing_here(
    cfg, library_with_database, rclone_on_path
):
    """The record names a destination, and a floor taken from another remote's
    run says nothing about which folders on this one are finished."""
    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=ROTATION_DAY,
        destination="elsewhere:mirror",
    )
    remote = ArchiveRemote("2026-08-01T000000Z", "2026-08-02T000000Z")
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1))
    assert remote.purged == []


def test_a_run_that_overwrote_nothing_still_keeps_the_newest_settled_archive(
    cfg, library_with_database, rclone_on_path
):
    """rclone writes no dated folder for a run that replaced nothing, so nothing
    is held and the keep applies to the settled folders exactly as it did."""
    remote = ArchiveRemote("2026-08-01T000000Z", "2026-08-02T000000Z", overwrites=False)
    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=ROTATION_DAY,
        destination=str(cfg.backup.dest),
    )
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1))
    assert remote.folders == {"2026-08-02T000000Z"}


def test_the_folder_the_last_completed_run_wrote_is_settled_not_held(
    cfg, library_with_database, rclone_on_path
):
    """THE BOUNDARY. The last completed run's own folder carries the stamp of the
    instant on record, so the comparison has to be strict: at or before the floor
    is settled. Held at equality, that folder would survive every later run."""
    remote = ArchiveRemote(_stamp(0), overwrites=False)
    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=ROTATION_DAY,
        destination=str(cfg.backup.dest),
    )
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1), keep=0)
    assert remote.folders == set()


def test_a_wider_keep_counts_the_held_run_as_one_of_its_slots(
    cfg, library_with_database, rclone_on_path
):
    remote = ArchiveRemote("2026-08-01T000000Z", "2026-08-02T000000Z", "2026-08-03T000000Z")
    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=ROTATION_DAY,
        destination=str(cfg.backup.dest),
    )
    remote.fail_mirror = True
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=1))
    remote.fail_mirror = False
    _mirror_at(cfg, remote, ROTATION_DAY + timedelta(days=2), keep=2)
    assert remote.folders == {"2026-08-03T000000Z", _stamp(1), _stamp(2)}


def test_a_keep_of_zero_is_still_a_keep_of_zero(cfg, library_with_database, rclone_on_path):
    """Asking to keep no archive is a choice, and holding a run's folders against
    it would be this rule overruling the person who made it."""
    remote = ArchiveRemote("2026-08-01T000000Z")
    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=ROTATION_DAY,
        destination=str(cfg.backup.dest),
    )
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
def test_the_plan_describes_the_rotation_the_run_applies(
    cfg, library_with_database, rclone_on_path, keep, said, unsaid
):
    """The preview and the run are one decision. A keep of zero holds nothing, so
    a plan that described the held run there would promise what the run undoes."""
    plan = backup.plan_backup(cfg, process_lister=no_processes, archive_keep=keep)
    detail = plan.portion(backup_facts.Portion.FILES).detail
    assert said in detail and unsaid not in detail, detail


def test_a_record_that_cannot_be_read_purges_nothing(
    cfg, library_with_database, rclone_on_path
):
    """Unreadable is not absent, and it is not a floor either. The purge is the
    one command here that deletes, so it does not run on a record nobody could
    read, and the exception is the one the publish would raise a moment later."""
    backup_facts.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    backup_facts.path_for(cfg).write_text("{ not json")
    remote = ArchiveRemote("2026-08-01T000000Z", "2026-08-02T000000Z")
    with pytest.raises(backup_facts.BackupFactsUnreadable):
        _mirror_at(cfg, remote, ROTATION_DAY)
    assert remote.purged == []


def test_a_rehearsal_does_not_read_the_record_to_list_a_rotation(
    cfg, library_with_database, rclone_on_path
):
    """A rehearsal purges nothing, so it needs no floor, and reading the record
    for one would fail a preview over a file the preview never touches."""
    backup_facts.path_for(cfg).parent.mkdir(parents=True, exist_ok=True)
    backup_facts.path_for(cfg).write_text("{ not json")
    remote = ArchiveRemote("2026-08-01T000000Z")
    plan = backup.plan_backup(cfg, now=ROTATION_DAY, process_lister=no_processes)
    outcome = backup.run_backup(cfg, plan, runner=remote, now=ROTATION_DAY, dry_run=True)
    assert _files_outcome(outcome).ran is True
    assert remote.purged == []


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 4: the age fact is readable by core, which does not import backup
# ═══════════════════════════════════════════════════════════════════════════


def test_backup_age_is_readable_from_library_scoped_state(cfg, library_with_database, rclone_on_path):
    """The plan's fourth scenario.

    Written by the module, resolved through the state inventory, and read back by
    a core function that knows nothing about how it got there.
    """
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
    """The whole point of publishing a FACT instead of exposing a function.

    An import would make core depend on a toggleable feature module (KTD23), and
    it would fail on the slim install that has no backup module, inside a warning
    that runs immediately before the riskiest operation in the product.
    """
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


def test_a_refused_portion_leaves_its_previous_age_untouched(
    cfg, library_with_database, rclone_on_path
):
    """The number R15 needs is exactly this one.

    A run that mirrored the files while rekordbox was open must not make the
    database look freshly captured, and it must not erase the last time it
    genuinely was.
    """
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


def test_the_reported_age_covers_every_declared_portion(cfg):
    """P3: the set is derived from the enum, so a new portion cannot be absent."""
    reported = backup_facts.ages(cfg)
    assert {a.portion for a in reported} == set(backup_facts.Portion)


def test_never_recorded_is_a_different_answer_from_very_old(cfg):
    """They have different fixes, so collapsing them costs the caller the choice."""
    now = datetime(2026, 8, 1, tzinfo=UTC)
    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=now - timedelta(days=400),
        destination="remote:mirror",
    )
    by_portion = {a.portion: a for a in backup_facts.ages(cfg, now=now)}
    assert by_portion[backup_facts.Portion.FILES].state is backup_facts.AgeState.KNOWN
    assert by_portion[backup_facts.Portion.FILES].age == timedelta(days=400)
    assert (
        by_portion[backup_facts.Portion.DATABASE].state
        is backup_facts.AgeState.NEVER_RECORDED
    )


def test_a_future_timestamp_is_named_rather_than_read_as_the_freshest_possible(cfg):
    """A naive age comparison treats a negative age as the freshest value.

    So a record written by a machine with a skewed clock, or edited by hand,
    silently satisfies the very check it was meant to fail.
    """
    now = datetime(2026, 8, 1, tzinfo=UTC)
    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=now + timedelta(days=2),
        destination="remote:mirror",
    )
    by_portion = {a.portion: a for a in backup_facts.ages(cfg, now=now)}
    entry = by_portion[backup_facts.Portion.FILES]
    assert entry.state is backup_facts.AgeState.RECORDED_IN_THE_FUTURE
    assert entry.age is None


def test_a_small_clock_difference_between_machines_is_tolerated(cfg):
    """Two installations of one library will not agree on the second."""
    now = datetime(2026, 8, 1, tzinfo=UTC)
    backup_facts.record(
        cfg,
        backup_facts.Portion.FILES,
        completed_at=now + timedelta(minutes=5),
        destination="remote:mirror",
    )
    by_portion = {a.portion: a for a in backup_facts.ages(cfg, now=now)}
    assert by_portion[backup_facts.Portion.FILES].state is backup_facts.AgeState.KNOWN


def test_the_quoted_age_is_none_unless_every_portion_has_a_usable_one(cfg):
    """A number derived from half the portions describes a half-protected library
    as though it were fully protected."""
    now = datetime(2026, 8, 1, tzinfo=UTC)
    backup_facts.record(
        cfg, backup_facts.Portion.FILES, completed_at=now - timedelta(days=1),
        destination="remote:mirror",
    )
    assert backup_facts.oldest_usable_age(cfg, now=now) is None

    backup_facts.record(
        cfg, backup_facts.Portion.DATABASE, completed_at=now - timedelta(days=9),
        destination="remote:database-snapshots",
    )
    assert backup_facts.oldest_usable_age(cfg, now=now) == timedelta(days=9)


def test_an_unreadable_fact_file_is_not_reported_as_no_backup(cfg):
    """They have opposite remediations, and one of them is alarming and wrong."""
    path = backup_facts.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{ this is not json")
    with pytest.raises(backup_facts.BackupFactsUnreadable) as excinfo:
        backup_facts.read_facts(cfg)
    assert excinfo.value.remedy is backup_facts.Remedy.REPAIR_BACKUP_FACTS


def test_a_fact_file_from_a_newer_build_refuses_rather_than_guessing(cfg):
    path = backup_facts.path_for(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"schema_version": backup_facts.SCHEMA_VERSION + 1, "portions": {}})
    )
    with pytest.raises(backup_facts.BackupFactsUnreadable) as excinfo:
        backup_facts.read_facts(cfg)
    assert excinfo.value.remedy is backup_facts.Remedy.UPGRADE_CRATEKIT


def test_a_naive_timestamp_is_refused_where_it_is_produced(cfg):
    """The failure lands on the code that made the value, not on a user weeks on."""
    with pytest.raises(ValueError, match="time zone"):
        backup_facts.record(
            cfg,
            backup_facts.Portion.FILES,
            completed_at=datetime(2026, 8, 1, 12),
            destination="remote:mirror",
        )


def test_the_fact_file_is_written_owner_only_under_any_umask(cfg, monkeypatch):
    """P1: a state file whose mode came from the umask is the recorded defect,
    and this one records when a user's data was last protected."""
    monkeypatch.setattr("os.umask", lambda mask: 0)
    import os

    old = os.umask(0)
    try:
        path = backup_facts.record(
            cfg,
            backup_facts.Portion.FILES,
            completed_at=datetime(2026, 8, 1, tzinfo=UTC),
            destination="remote:mirror",
        )
        assert stat.S_IMODE(path.stat().st_mode) == config.PRIVATE_FILE_MODE
        assert stat.S_IMODE(path.parent.stat().st_mode) == config.PRIVATE_DIR_MODE
    finally:
        os.umask(old)


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 5: restore clears stale sidecars BEFORE copying
# ═══════════════════════════════════════════════════════════════════════════


def test_restore_removes_stale_sidecars_before_copying(cfg, tmp_path, rclone_on_path):
    """The plan's fifth scenario, asserted on the ORDER rather than the outcome.

    A write-ahead log left beside a freshly restored database belongs to the
    database that was just replaced, and SQLite replays it onto the new file,
    corrupting it in a way that opens without complaint. Copying first and
    clearing afterwards would already have handed it both.
    """
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

    plan = backup.plan_restore(
        cfg,
        target=target,
        confirmed=True,
        snapshot="2026-08-01T000000Z",
        runner=runner,
        process_lister=no_processes, gates=open_gates)
    assert set(plan.clears) == set(stale)

    backup.run_restore(plan, cfg, runner=runner, gates=open_gates)

    assert not any(p.exists() for p in stale), "stale sidecars survived the restore"
    assert observed, "no copy command was issued"
    # Every transfer ran with both sidecars already gone. The listing is a
    # probe at plan time, before anything is cleared, and is not a transfer.
    for _, present in observed:
        assert present == [False, False]


def test_a_rehearsed_restore_does_not_clear_the_live_sidecars(cfg, tmp_path, rclone_on_path):
    """Clearing is itself destructive, so a preview must not do it.

    A rehearsal that removed the write-ahead log and then transferred nothing
    would leave the user's database without the log it needs: the damage done,
    the repair skipped.
    """
    target = tmp_path / "scratch"
    database = backup.database_target_for(cfg, target)
    database.parent.mkdir(parents=True, exist_ok=True)
    database.write_bytes(b"live database")
    sidecars = []
    for sidecar in config.SQLITE_SIDECARS:
        path = database.with_name(database.name + sidecar.suffix)
        path.write_bytes(b"live log")
        sidecars.append(path)

    recorder = Recorder(
        stdout_for={backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg)}
    )
    plan = backup.plan_restore(
        cfg, target=target, confirmed=True, snapshot="2026-08-01T000000Z",
        runner=recorder, process_lister=no_processes, gates=open_gates)
    backup.run_restore(plan, cfg, runner=recorder, dry_run=True, gates=open_gates)

    assert all(p.exists() for p in sidecars), "a rehearsal deleted the live sidecars"
    issued = [c for c in recorder.commands if c.label == backup.RESTORE_DATABASE]
    assert issued and all(c.argv[-1] == "--dry-run" for c in issued)


def test_restore_writes_back_the_log_and_never_the_shared_memory_index(
    cfg, tmp_path, rclone_on_path
):
    """The source system's asymmetry, carried across as a declaration.

    The shared-memory index is derived from the log, so restoring a stale one
    beside a fresh log hands SQLite two disagreeing views of one database. Which
    sidecars come back is read from ``Sidecar.restored`` rather than retyped.
    The listing includes both so presence is not what decides: the inventory is.
    """
    target = tmp_path / "scratch"
    backup.database_target_for(cfg, target).parent.mkdir(parents=True, exist_ok=True)
    plan = backup.plan_restore(
        cfg,
        target=target,
        confirmed=True,
        snapshot="2026-08-01T000000Z",
        runner=Recorder(
            stdout_for={
                backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg, "-wal", "-shm"),
            }
        ),
        process_lister=no_processes, gates=open_gates)
    sources = [c.argv[c.argv.index("copy") + 1] for c in plan.commands]
    restored = {s.suffix for s in config.SQLITE_SIDECARS if s.restored}
    for suffix in (s.suffix for s in config.SQLITE_SIDECARS):
        matching = [s for s in sources if s.endswith(suffix)]
        assert bool(matching) == (suffix in restored), (
            f"a restore that copies {suffix} back is not what the inventory declares"
        )


def test_the_file_half_of_a_restore_copies_and_never_syncs(cfg, tmp_path, rclone_on_path):
    """A sync makes the target MATCH the remote, which means deleting.

    The target of a restore is frequently a partially-recovered volume holding
    files the user salvaged by other means, and a sync would remove every one of
    them for not being on the remote. Copy adds and overwrites; it never removes.
    """
    target = tmp_path / "scratch"
    backup.database_target_for(cfg, target).parent.mkdir(parents=True, exist_ok=True)
    plan = backup.plan_restore(
        cfg, target=target, confirmed=True, snapshot="2026-08-01T000000Z",
        include_mirror=True, runner=Recorder(), process_lister=no_processes, gates=open_gates)
    mirror = [c for c in plan.commands if c.label == backup.RESTORE_MIRROR]
    assert len(mirror) == 1
    assert "copy" in mirror[0].argv and "sync" not in mirror[0].argv
    # And it is FIRST, so the database lands last, after the bulk transfer.
    assert plan.commands[0].label == backup.RESTORE_MIRROR


def test_the_file_half_is_off_by_default(cfg, tmp_path, rclone_on_path):
    """The two halves cost very differently and are wanted at different times.

    Recovering from a bad write means the database alone. Recovering from a dead
    drive means both, and the second is hundreds of gigabytes.
    """
    target = tmp_path / "scratch"
    backup.database_target_for(cfg, target).parent.mkdir(parents=True, exist_ok=True)
    plan = backup.plan_restore(
        cfg, target=target, confirmed=True, snapshot="2026-08-01T000000Z",
        runner=Recorder(
            stdout_for={backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg)}
        ),
        process_lister=no_processes, gates=open_gates)
    assert backup.RESTORE_MIRROR not in [c.label for c in plan.commands]


def test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar(
    cfg, tmp_path, rclone_on_path
):
    """The residual
    "A restore from a snapshot taken with rekordbox closed always reports failure".

    The only snapshot this product takes has no write ahead log.
    ``plan_database_snapshot`` copies a sidecar only when it is present.
    ``plan_restore`` used to copy the log unconditionally, rclone exited 3, and
    the person was told the restore failed after the database had already landed.
    """
    target = tmp_path / "scratch"
    backup.database_target_for(cfg, target).parent.mkdir(parents=True, exist_ok=True)
    database = backup.database_target_for(cfg, target).name
    recorder = Recorder(
        stdout_for={backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg)}
    )
    plan = backup.plan_restore(
        cfg, target=target, confirmed=True, snapshot="2026-08-01T000000Z",
        runner=recorder, process_lister=no_processes, gates=open_gates)
    sources = [c.argv[c.argv.index("copy") + 1] for c in plan.commands]
    assert any(source.endswith(database) for source in sources)
    assert not any(source.endswith(database + "-wal") for source in sources)
    assert plan.absent_sidecars == ("-wal",)
    results = backup.run_restore(plan, cfg, runner=recorder, gates=open_gates)
    assert results and all(result.returncode == 0 for result in results)


def test_a_restore_from_a_snapshot_holding_the_log_copies_it(
    cfg, tmp_path, rclone_on_path
):
    """The other shape: a snapshot taken while the database still had a log."""
    target = tmp_path / "scratch"
    backup.database_target_for(cfg, target).parent.mkdir(parents=True, exist_ok=True)
    database = backup.database_target_for(cfg, target).name
    recorder = Recorder(
        stdout_for={
            backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg, "-wal"),
        }
    )
    plan = backup.plan_restore(
        cfg, target=target, confirmed=True, snapshot="2026-08-01T000000Z",
        runner=recorder, process_lister=no_processes, gates=open_gates)
    sources = [c.argv[c.argv.index("copy") + 1] for c in plan.commands]
    assert any(source.endswith(database) for source in sources)
    assert any(source.endswith(database + "-wal") for source in sources)
    assert plan.absent_sidecars == ()
    results = backup.run_restore(plan, cfg, runner=recorder, gates=open_gates)
    assert results and all(result.returncode == 0 for result in results)


def test_a_failed_database_copy_still_refuses_when_the_sidecar_is_absent(
    cfg, tmp_path, rclone_on_path
):
    """Skipping an absent sidecar does not swallow a failed database transfer."""
    target = tmp_path / "scratch"
    backup.database_target_for(cfg, target).parent.mkdir(parents=True, exist_ok=True)
    recorder = Recorder(
        stdout_for={backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg)},
        fail_labels={backup.RESTORE_DATABASE},
    )
    plan = backup.plan_restore(
        cfg, target=target, confirmed=True, snapshot="2026-08-01T000000Z",
        runner=recorder, process_lister=no_processes, gates=open_gates)
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.run_restore(plan, cfg, runner=recorder, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.RESTORE_TRANSFER_FAILED


def test_a_snapshot_that_cannot_be_listed_refuses_before_clearing(
    cfg, tmp_path, rclone_on_path
):
    """A failed listing is not an empty snapshot.

    Treating it as no sidecars would skip the log and report a complete restore
    against a remote that never answered.
    """
    target = tmp_path / "scratch"
    database = backup.database_target_for(cfg, target)
    database.parent.mkdir(parents=True, exist_ok=True)
    wal = database.with_name(database.name + "-wal")
    wal.write_bytes(b"live log")
    recorder = Recorder(fail_labels={backup.LIST_SNAPSHOT_CONTENTS})
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=target, confirmed=True, snapshot="2026-08-01T000000Z",
            runner=recorder, process_lister=no_processes, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.NO_SNAPSHOT_AVAILABLE
    assert wal.exists() and wal.read_bytes() == b"live log"
    assert backup.RESTORE_DATABASE not in recorder.labels()


def test_the_snapshot_listing_is_of_the_database_folder(
    cfg, tmp_path, rclone_on_path
):
    """Listing the snapshot root would see dated folder names, never the log."""
    target = tmp_path / "scratch"
    backup.database_target_for(cfg, target).parent.mkdir(parents=True, exist_ok=True)
    recorder = Recorder(
        stdout_for={backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg, "-wal")}
    )
    backup.plan_restore(
        cfg, target=target, confirmed=True, snapshot="2026-08-01T000000Z",
        runner=recorder, process_lister=no_processes, gates=open_gates)
    listed = [c for c in recorder.commands if c.label == backup.LIST_SNAPSHOT_CONTENTS]
    assert len(listed) == 1
    assert listed[0].argv[-2].endswith("/2026-08-01T000000Z/db/")
    assert "--files-only" in listed[0].argv


def test_the_sidecars_are_cleared_before_the_mirror_too(cfg, tmp_path, rclone_on_path):
    """The invariant at its strongest: no stale log ever sits beside a database
    that has started to change."""
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

    plan = backup.plan_restore(
        cfg, target=target, confirmed=True, snapshot="2026-08-01T000000Z",
        include_mirror=True, runner=runner, process_lister=no_processes, gates=open_gates)
    backup.run_restore(plan, cfg, runner=runner, gates=open_gates)
    assert observed[0][0] == backup.RESTORE_MIRROR
    assert all(present is False for _, present in observed)


def test_restore_is_a_named_decision_and_never_a_prompt(cfg, tmp_path, rclone_on_path):
    """R33. The source blocks on standard input before overwriting a library.

    That cannot be answered by a detached job and cannot be recorded as having
    been answered by anyone.
    """
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=False, runner=Recorder(),
            process_lister=no_processes, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.RESTORE_NOT_CONFIRMED


def test_no_module_in_this_unit_reads_standard_input():
    """The structural half of R33: a prompt cannot appear where none is written."""
    for name in ("backup.py", "mastering.py", "setbuilder.py"):
        source = (SRC_ROOT / "cratekit" / "modules" / "tools" / name).read_text()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id != "input", f"{name} prompts on standard input"
            if isinstance(node, ast.Attribute):
                assert node.attr not in {"stdin"}, f"{name} reads standard input"


def test_restore_refuses_while_rekordbox_holds_the_database(cfg, tmp_path, rclone_on_path):
    """Replacing the file a live application holds open leaves the application
    and the disk describing two different libraries."""
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=True, runner=Recorder(),
            process_lister=rekordbox_running, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.REKORDBOX_RUNNING


def test_the_restore_target_is_derived_from_the_configured_database_path(cfg, tmp_path):
    """Not from an assumed vendor layout.

    The source composes a fixed path under the target, which is right for one
    installation and silently wrong for a user who moved their database: it
    restores to a path rekordbox does not read, and reports success.
    """
    target = tmp_path / "scratch"
    relative = config.state_path("rekordbox_db", cfg).relative_to(cfg.library.root)
    assert backup.database_target_for(cfg, target) == target / relative


def test_a_restore_with_no_snapshot_available_refuses_by_name(cfg, tmp_path, rclone_on_path):
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=True, runner=Recorder(),
            process_lister=no_processes, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.NO_SNAPSHOT_AVAILABLE


def test_the_latest_snapshot_is_the_newest_by_sortable_stamp(cfg, tmp_path, rclone_on_path):
    recorder = Recorder(
        stdout_for={
            backup.LIST_SNAPSHOTS: "2026-01-01T000000Z/\n2026-03-01T000000Z/\n2026-02-01T000000Z/\n"
        }
    )
    assert backup.latest_snapshot(cfg, runner=recorder) == "2026-03-01T000000Z"


def test_an_absent_restore_target_refuses_rather_than_creating_one(cfg, tmp_path, rclone_on_path):
    """Creating the target would silently restore a library into a directory the
    user never mounted, on the boot disk."""
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path / "not-mounted", confirmed=True, runner=Recorder(),
            process_lister=no_processes, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.RESTORE_TARGET_ABSENT


def test_the_backup_payload_carries_a_version(cfg, library_with_database, rclone_on_path):
    plan = backup.plan_backup(cfg, process_lister=no_processes)
    payload = backup.plan_payload(plan)
    assert payload["payload_version"] == backup.PAYLOAD_VERSION
    assert {p["portion"] for p in payload["portions"]} == {
        p.value for p in backup_facts.Portion
    }

    outcome = backup.run_backup(cfg, plan, runner=Recorder())
    assert backup.outcome_payload(outcome)["ok"] is True


# ═══════════════════════════════════════════════════════════════════════════
# Snapshot provenance. A pulled snapshot is a stamp, and it is this library's.
# ═══════════════════════════════════════════════════════════════════════════

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
    cfg, tmp_path, rclone_on_path, typed
):
    """The ledger's measured cost, reproduced: the first value is its own.

    It reached the remote path by interpolation and planned a copy out of
    another directory with exit 0. Refused on SHAPE, and before any listing, so
    a value that is a path never becomes part of an argument to the program that
    talks to the remote.
    """
    recorder = marked(cfg)
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=True, snapshot=typed,
            runner=recorder, process_lister=no_processes, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.SNAPSHOT_NAME_INVALID
    assert recorder.commands == [], (
        f"the remote was asked {recorder.labels()} about a value that is not a stamp"
    )


def test_every_stamp_the_backup_writes_passes_the_shape_the_restore_demands():
    """The two ends of one coupling, held together by a test rather than by hope.

    A shape check written from memory of the format drifts the day the format
    does, and would then refuse every snapshot this product takes.
    """
    for moment in (
        datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        datetime(1999, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
        datetime(2026, 8, 1, 9, 5, 7, tzinfo=timezone(timedelta(hours=-4))),
    ):
        assert backup.is_stamp(backup.stamp_for(moment)), backup.stamp_for(moment)
    assert backup.is_stamp(backup.STAMP_EXAMPLE), "the refusal shows a stamp it would refuse"


def test_a_snapshot_marked_for_another_library_is_refused(cfg, tmp_path, rclone_on_path):
    """The half the shape check cannot close: a well formed stamp, someone else's.

    Two libraries sharing one remote root write into one directory of stamps, so
    a perfectly spelled stamp can name the other library's database.
    """
    recorder = marked(cfg, "0000-AAAA")
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=True, snapshot=STAMP,
            runner=recorder, process_lister=no_processes, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH
    assert "0000-aaaa" in excinfo.value.detail, excinfo.value.detail
    assert not any(c.label in backup.TRANSFERRING_LABELS for c in recorder.commands)


def test_a_snapshot_marked_for_this_library_is_planned_and_says_so(
    cfg, tmp_path, rclone_on_path
):
    plan = backup.plan_restore(
        cfg, target=tmp_path, confirmed=True, snapshot=STAMP,
        runner=marked(cfg), process_lister=no_processes, gates=open_gates)
    assert plan.snapshot == STAMP
    assert plan.recorded_volume == "f1e2-d3c4"


def test_the_identity_is_compared_case_blind_like_the_volume_gate(
    cfg, tmp_path, rclone_on_path
):
    """``diskutil`` prints uppercase and the adapters report lowercase."""
    recorder = Recorder(
        stdout_for={
            backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg),
            backup.LIST_SNAPSHOT_IDENTITY: "library-volume.F1E2-d3c4\n",
        }
    )
    plan = backup.plan_restore(
        cfg, target=tmp_path, confirmed=True, snapshot=STAMP,
        runner=recorder, process_lister=no_processes, gates=open_gates)
    assert plan.recorded_volume == "f1e2-d3c4"


def test_a_snapshot_carrying_two_identities_is_refused(cfg, tmp_path, rclone_on_path):
    """Two libraries backing up in one second share one dated folder.

    One of the markers is this library's, and the database beside them is
    whichever copy landed last, so a match on either marker proves nothing.
    """
    recorder = Recorder(
        stdout_for={
            backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg),
            backup.LIST_SNAPSHOT_IDENTITY: (
                marker_for(cfg.library.volume_id) + "\n" + marker_for("0000-AAAA") + "\n"
            ),
        }
    )
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=True, snapshot=STAMP,
            runner=recorder, process_lister=no_processes, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH


def test_a_marker_with_no_identity_after_its_prefix_is_not_read_as_unmarked(
    cfg, tmp_path, rclone_on_path
):
    recorder = Recorder(
        stdout_for={
            backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg),
            backup.LIST_SNAPSHOT_IDENTITY: "library-volume.\n",
        }
    )
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=True, snapshot=STAMP,
            runner=recorder, process_lister=no_processes, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH


def test_an_identity_listing_that_fails_is_not_read_as_an_unmarked_snapshot(
    cfg, tmp_path, rclone_on_path
):
    """Absence read as evidence of absence, the first pattern.

    A named snapshot with no marker is accepted, so a listing that FAILED must
    not arrive looking like one, or an unreachable remote becomes the way past
    the identity check.
    """
    recorder = Recorder(
        stdout_for={backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg)},
        fail_labels={backup.LIST_SNAPSHOT_IDENTITY},
    )
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=True, snapshot=STAMP,
            runner=recorder, process_lister=no_processes, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.NO_SNAPSHOT_AVAILABLE
    assert not any(c.label in backup.TRANSFERRING_LABELS for c in recorder.commands)


def test_an_unmarked_snapshot_is_pulled_only_when_a_person_named_it(
    cfg, tmp_path, rclone_on_path
):
    """Every snapshot taken before the marker existed is unmarked.

    Refusing them all would strand a person whose drive died the day after this
    landed, and accepting them as the default would leave the hole open for the
    newest folder under a shared root. Naming the stamp is the act that tells
    the two apart.
    """
    unmarked = {
        backup.LIST_SNAPSHOTS: STAMP + "/\n",
        backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg),
    }
    named = backup.plan_restore(
        cfg, target=tmp_path, confirmed=True, snapshot=STAMP,
        runner=Recorder(stdout_for=unmarked), process_lister=no_processes, gates=open_gates)
    assert named.snapshot == STAMP
    assert named.recorded_volume is None

    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=True,
            runner=Recorder(stdout_for=unmarked), process_lister=no_processes,
            gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.SNAPSHOT_IDENTITY_UNRECORDED
    assert STAMP in excinfo.value.detail


def test_a_resolved_stamp_handed_down_is_not_mistaken_for_one_a_person_named(
    cfg, tmp_path, rclone_on_path
):
    """The verb resolves the newest stamp for its offer and passes it on.

    Without the flag, a stamp that came off the listing would arrive looking
    typed, and the unmarked refusal above would never fire on the path a person
    actually takes.
    """
    unmarked = {backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg)}
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=True, snapshot=STAMP, accept_unrecorded=False,
            runner=Recorder(stdout_for=unmarked), process_lister=no_processes,
            gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.SNAPSHOT_IDENTITY_UNRECORDED


def test_a_replaced_drive_restores_the_old_volumes_snapshot_by_naming_it(
    cfg, tmp_path, rclone_on_path
):
    """A dead drive is the reason to pull a mirror, and its replacement is a new volume.

    A strict compare against the configured identity would refuse exactly the
    restore this verb exists for, so the person states the identity the snapshot
    is expected to record. The statement is held to: it excuses nothing else.
    """
    plan = backup.plan_restore(
        cfg, target=tmp_path, confirmed=True, snapshot=STAMP, snapshot_volume="0000-AAAA",
        runner=marked(cfg, "0000-aaaa"), process_lister=no_processes, gates=open_gates)
    assert plan.recorded_volume == "0000-aaaa"

    for recorder in (
        marked(cfg),
        marked(cfg, "9999-BBBB"),
        Recorder(stdout_for={backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg)}),
    ):
        with pytest.raises(backup.BackupRefused) as excinfo:
            backup.plan_restore(
                cfg, target=tmp_path, confirmed=True, snapshot=STAMP,
                snapshot_volume="0000-AAAA", runner=recorder,
                process_lister=no_processes, gates=open_gates)
        assert excinfo.value.refusal is backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH


def test_the_newest_snapshot_ignores_folders_that_are_not_stamps(cfg, rclone_on_path):
    """The same shape one function over. A stray folder sorts after every stamp."""
    recorder = Recorder(
        stdout_for={
            backup.LIST_SNAPSHOTS: "2026-01-01T000000Z/\nold/\n2026-03-01T000000Z/\nzz-scratch/\n"
        }
    )
    assert backup.latest_snapshot(cfg, runner=recorder) == "2026-03-01T000000Z"


def test_the_capture_marks_the_snapshot_after_the_database_and_never_before_it(
    cfg, library_with_database, rclone_on_path
):
    """The marker says "this folder holds this library's database".

    Written first, a run whose database copy then failed would leave a folder
    that claims an identity and holds nothing, so it follows every file of the
    database set and the executor stops before it when one of them fails.
    """
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


def test_what_the_capture_writes_is_what_the_restore_reads(
    cfg, library_with_database, tmp_path, rclone_on_path
):
    """One round trip through both ends, so the two cannot drift apart.

    Every other test here hands the restore a marker built by the helper. This
    one takes the name off the capture's own command.
    """
    plan = backup.plan_backup(
        cfg, now=datetime(2026, 8, 1, tzinfo=timezone.utc),
        process_lister=no_processes, settings_dirs=())
    database = next(p for p in plan.portions if p.portion is backup_facts.Portion.DATABASE)
    marker = next(c for c in database.commands if c.label == backup.SNAPSHOT_IDENTITY)
    written = marker.argv[-1].rsplit("/", 1)[-1]
    recorder = Recorder(
        stdout_for={
            backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg),
            backup.LIST_SNAPSHOT_IDENTITY: written + "\n",
        }
    )
    restored = backup.plan_restore(
        cfg, target=tmp_path, confirmed=True, snapshot=plan.stamp,
        runner=recorder, process_lister=no_processes, gates=open_gates)
    assert restored.recorded_volume == "f1e2-d3c4"


@pytest.mark.parametrize("identity", [None, "has/slash", "has space", "..", ".hidden"])
def test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so(
    cfg, library_with_database, rclone_on_path, identity
):
    """No marker is better than a marker that names a path, and silence is worse than both."""
    import dataclasses

    bare = dataclasses.replace(
        cfg, library=dataclasses.replace(cfg.library, volume_id=identity)
    )
    plan = backup.plan_backup(bare, process_lister=no_processes, settings_dirs=())
    database = next(p for p in plan.portions if p.portion is backup_facts.Portion.DATABASE)
    assert backup.SNAPSHOT_IDENTITY not in [c.label for c in database.commands]
    assert backup.SNAPSHOT_IDENTITY_NOT_WRITTEN in [w["code"] for w in database.warnings]


# ── The review round. Every one of these is a finding the built in review drove. ──

LEGACY = "2026-08-01_123456"


class RemoteOf:
    """A runner over a remote described as ``{snapshot name: marker identities}``.

    The label keyed recorder above answers one string per label, which cannot
    say that two dated folders carry different markers, and the newest-by-default
    walk is exactly the code that reads more than one folder.
    """

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
            return backup.CommandResult(
                0, "".join(f"{marker_for(i)}\n" for i in self.holds[name])
            )
        if command.label == backup.LIST_SNAPSHOT_CONTENTS:
            return backup.CommandResult(0, snapshot_listing(self.cfg))
        return backup.CommandResult(0)

    def asked_about(self):
        return [
            c.argv[2].rstrip("/").rsplit("/", 1)[-1]
            for c in self.commands
            if c.label == backup.LIST_SNAPSHOT_IDENTITY
        ]


def test_a_snapshot_the_source_system_wrote_is_still_a_name_and_still_pulled(
    cfg, tmp_path, rclone_on_path
):
    """The source system spells its dated folder with an underscore, in local time.

    It writes the same layout into what is commonly the same remote directory,
    so on the day of a cutover this is how EVERY snapshot a person owns is
    spelled. The first cut of the shape check refused them all by name and hid
    them from the listing, which the built in review drove.
    """
    assert backup.is_snapshot_name(LEGACY)
    assert not backup.is_stamp(LEGACY), "the narrow check is what a backup WRITES"
    assert not backup.is_snapshot_name("2026-08-01_1234567")
    assert not backup.is_snapshot_name("2026-02-30_123456")

    plan = backup.plan_restore(
        cfg, target=tmp_path, confirmed=True, snapshot=LEGACY,
        runner=RemoteOf(cfg, {LEGACY: ()}), process_lister=no_processes, gates=open_gates)
    assert plan.snapshot == LEGACY

    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=True,
            runner=RemoteOf(cfg, {LEGACY: ()}), process_lister=no_processes,
            gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.SNAPSHOT_IDENTITY_UNRECORDED
    assert LEGACY in excinfo.value.detail


def test_the_default_takes_the_newest_snapshot_that_is_this_librarys(
    cfg, tmp_path, rclone_on_path
):
    """Ownership selects. It does not veto the newest and stop.

    Under a shared root the newest folder is whichever library backed up last,
    and a backup cut off before its marker leaves an unmarked folder in front of
    a good one. Both are stepped over, and the walk stops at the first match.
    """
    remote = RemoteOf(
        cfg,
        {
            "2026-08-01T000000Z": ("F1E2-D3C4",),
            "2026-08-02T000000Z": ("F1E2-D3C4",),
            "2026-08-03T000000Z": ("0000-AAAA",),
            "2026-08-04T000000Z": (),
        },
    )
    plan = backup.plan_restore(
        cfg, target=tmp_path, confirmed=True, runner=remote,
        process_lister=no_processes, gates=open_gates)
    assert plan.snapshot == "2026-08-02T000000Z"
    assert remote.asked_about()[:3] == [
        "2026-08-04T000000Z", "2026-08-03T000000Z", "2026-08-02T000000Z",
    ]
    assert "2026-08-01T000000Z" not in remote.asked_about()


def test_the_default_walk_is_bounded_and_the_refusal_says_how_far_it_looked(
    cfg, tmp_path, rclone_on_path
):
    own_but_old = {"2026-01-01T000000Z": ("F1E2-D3C4",)}
    foreign = {
        f"2026-08-{day:02d}T000000Z": ("0000-AAAA",)
        for day in range(1, backup.NEWEST_WALK + 1)
    }
    remote = RemoteOf(cfg, {**own_but_old, **foreign})
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=True, runner=remote,
            process_lister=no_processes, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH
    assert len(remote.asked_about()) == backup.NEWEST_WALK
    assert f"{backup.NEWEST_WALK} newest" in excinfo.value.detail
    assert "0000-aaaa" in excinfo.value.detail


def test_the_replaced_drive_identity_selects_the_newest_of_the_old_volumes(
    cfg, tmp_path, rclone_on_path
):
    remote = RemoteOf(
        cfg,
        {
            "2026-08-01T000000Z": ("0000-AAAA",),
            "2026-08-02T000000Z": ("0000-AAAA",),
            "2026-08-03T000000Z": ("F1E2-D3C4",),
        },
    )
    plan = backup.plan_restore(
        cfg, target=tmp_path, confirmed=True, snapshot_volume="0000-aaaa",
        runner=remote, process_lister=no_processes, gates=open_gates)
    assert (plan.snapshot, plan.recorded_volume) == ("2026-08-02T000000Z", "0000-aaaa")


@pytest.mark.parametrize("stated", ["", "   "])
def test_an_empty_expected_identity_never_matches_an_empty_marker(
    cfg, tmp_path, rclone_on_path, stated
):
    """A marker with nothing after its prefix reads back as the empty string.

    An expected value of nothing folds to the same, so the two matched each
    other and a snapshot naming nobody was pulled as verified.
    """
    recorder = Recorder(
        stdout_for={
            backup.LIST_SNAPSHOT_CONTENTS: snapshot_listing(cfg),
            backup.LIST_SNAPSHOT_IDENTITY: "library-volume.\n",
        }
    )
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=True, snapshot=STAMP, snapshot_volume=stated,
            runner=recorder, process_lister=no_processes, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH


def test_two_markers_are_refused_without_offering_an_identity_to_pass(
    cfg, tmp_path, rclone_on_path
):
    """The reserved step says to pass the volume the refusal names.

    With two markers no stated volume can ever be accepted, so a message that
    named two and sent the person to that step would have them retry for ever.
    """
    remote = RemoteOf(cfg, {STAMP: ("F1E2-D3C4", "0000-AAAA")})
    for stated in (None, "0000-AAAA", "F1E2-D3C4"):
        with pytest.raises(backup.BackupRefused) as excinfo:
            backup.plan_restore(
                cfg, target=tmp_path, confirmed=True, snapshot=STAMP, snapshot_volume=stated,
                runner=remote, process_lister=no_processes, gates=open_gates)
        assert excinfo.value.refusal is backup.Refusal.SNAPSHOT_LIBRARY_MISMATCH
        assert "No expected volume can vouch" in excinfo.value.detail


def test_a_snapshot_root_that_cannot_be_listed_is_not_reported_as_empty(
    cfg, tmp_path, rclone_on_path
):
    remote = RemoteOf(cfg, {STAMP: ("F1E2-D3C4",)}, fail={backup.LIST_SNAPSHOTS})
    with pytest.raises(backup.BackupRefused) as excinfo:
        backup.plan_restore(
            cfg, target=tmp_path, confirmed=True, runner=remote,
            process_lister=no_processes, gates=open_gates)
    assert excinfo.value.refusal is backup.Refusal.NO_SNAPSHOT_AVAILABLE
    assert "could not be listed" in excinfo.value.detail


def test_a_marker_that_cannot_be_written_warns_and_does_not_fail_the_backup(
    cfg, library_with_database, tmp_path, rclone_on_path
):
    """By the time the marker is tried, the database set has already copied.

    Failing the portion skipped the settings, published no age and reported a
    failed backup over a remote holding a good one, on every run, for a remote
    that cannot hold an empty file.
    """
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
