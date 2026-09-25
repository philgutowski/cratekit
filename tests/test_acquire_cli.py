"""U42: the two acquisition shells, driven through the real dispatcher.

The engines landed in U15 and sat with no shell for eleven units. What is driven
here is the shell half: that both verbs are reachable, that the long-running one
freezes and queues rather than reaching a provider, and that the audit answers
about files it can see AND about the ones it cannot.

The last of those is the finding this file exists for. The audit's walk was
written with ``Path.rglob`` and reported a clean answer over a directory it had
been refused permission to list, which is the merge bar's "shown a clean report
over state the tool could not read". ``test_a_directory_it_cannot_list_is_reported``
is that drive, kept as a guard.
"""

from __future__ import annotations

import json
import os
import stat

import pytest

from cratekit.acquire import cli as acquire_cli
from cratekit.acquire.adapter import LosslessPolicy
from cratekit.cli import registry
from cratekit.core import config, naming
from cratekit.core.exit_codes import ExitCode
from tests.acquire_fakes import tidal_list
from tests.test_cli_contract import configured, drive, library  # noqa: F401

VERBS = ("acquire.download", "acquire.audit")


# ═══════════════════════════════════════════════════════════════════════════
# The verbs exist, are landed, and dispatch
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("name", VERBS)
def test_the_verb_is_landed_rather_than_planned(name):
    """``planned_in`` gone is what starts the conformance properties driving it.

    An entry marked planned is skipped by the suites that walk the registry, so
    the marker outliving its unit is not a cosmetic staleness: it is a verb
    nothing checks. Both of these named U15, which closed eleven units ago.
    """
    entry = registry.entry(name)
    assert entry.landed, f"{name} still names a unit it was planned in"
    assert entry.module == "cratekit.acquire.cli"


@pytest.mark.parametrize("name", VERBS)
def test_the_verb_appears_in_help_and_dispatches(name, capsys, configured):  # noqa: F811
    """Reachable by a person, which is the whole thing rows 6 and 7 were missing.

    ``capsys`` rather than the ``drive`` helper's captured streams: argparse
    prints help to the real ``sys.stdout``, so the helper's ``StringIO`` comes
    back empty and an assertion against it would pass on a verb that had
    vanished from help entirely. That is not hypothetical, it is what the first
    version of this test did.

    The usage LINE is what is matched, not the bare verb name. A subcommand word
    appears in the parent's subcommand listing whether or not the leaf parser
    exists, so matching the word alone would pass on a verb that cannot be built.
    """
    entry = registry.entry(name)
    code, _, _ = drive([*entry.path, "--help"])
    assert code == int(ExitCode.OK)
    printed = capsys.readouterr().out
    assert f"crate {' '.join(entry.path)}" in printed, printed


def test_neither_verb_is_hidden_behind_a_module_toggle():
    """Row 7 is a POLICY row, so a toggle would recreate the state R21 forbids.

    ``registry.POLICY_ROWS`` names row 7 as realized by
    ``acquisition.lossless_policy`` rather than by a module that could be on and
    unmarked. Asserted here as well as in the parity check because this is the
    file somebody edits when they add a flag to these two verbs.
    """
    assert 7 in registry.POLICY_ROWS
    for name in VERBS:
        assert registry.entry(name).module_id is None


# ═══════════════════════════════════════════════════════════════════════════
# acquire.download: freeze and queue, reaching no provider
# ═══════════════════════════════════════════════════════════════════════════


def test_download_over_an_absent_list_refuses_by_name(configured):  # noqa: F811
    """The list is READ at the queue as of U54, so an absent one is refused here.

    Until U54 the path was frozen unread and this test asserted a queued job over
    a list that was not there. The zero item rule reversed it: the items are the
    list's tracks, and naming them means reading the list. The refusal is the
    match verb's own, through the one list reader the product has.
    """
    absent = configured.library.root / "no-such-list.txt"
    assert not absent.exists()
    code, out, _ = drive(["--output", "json", "acquire", "download", str(absent)])
    assert code == int(ExitCode.PRECONDITION), out
    envelope = json.loads(out)
    assert envelope["cause"]["reason"] == "intake-list-unusable"
    assert "could not be read" in envelope["cause"]["message"]
    from cratekit.core import jobs

    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_download_reaches_no_provider_and_no_network(configured, monkeypatch):  # noqa: F811
    """The shell must not touch the acquisition engines at all.

    Driven rather than argued, because "it only queues" is the kind of claim that
    stays in a docstring after somebody adds one convenience lookup. Every engine
    entry point the verb could plausibly reach is replaced with a detonator.
    """
    from cratekit.acquire import adapter, download

    def boom(*args, **kwargs):
        raise AssertionError("the shell reached an acquisition engine")

    for module, name in (
        (download, "acquire_paced"),
        (download, "acquire_concurrently"),
        (adapter, "acquire_with_source"),
        (adapter, "acquire_one"),
        (adapter, "dispatch"),
    ):
        monkeypatch.setattr(module, name, boom)

    listed = configured.library.root / "list.json"
    listed.write_text(tidal_list([("100", "A", "B")]))
    code, _, _ = drive(["acquire", "download", str(listed)])
    assert code == int(ExitCode.OK)


def test_download_argv_round_trips_the_frozen_payload_and_carries_no_run(configured):  # noqa: F811
    """The resume argv is what re-invokes the job, and it names no gate run.

    ``--run`` restores a frozen gate decision into a fresh child process. This
    verb declares no gate, so the flag would name a run nothing was recorded
    against. Asserted as a WHOLE token: ``--run-id`` contains ``--run``, and a
    substring check is what reported a broken verb clean once already.
    """
    listed = configured.library.root / "l.json"
    listed.write_text(tidal_list([("100", "A", "B")]))
    code, out, _ = drive(["--output", "json", "acquire", "download", str(listed)])
    assert code == int(ExitCode.OK), out
    job_id = json.loads(out)["data"]["job_id"]

    from cratekit.core import jobs

    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
    argv = acquire_cli.download_argv(job)

    # R-668: the job froze the list, so the command that continues it names
    # the job and nothing else.
    assert argv == ["acquire", "download", "--job", job_id]
    assert "--run" not in argv


def test_download_argv_is_the_builder_the_registry_names(configured):  # noqa: F811
    """The registry's ``argv_builder`` is looked up by NAME at resume time.

    A builder that exists under a different name is a resume that raises
    ``AttributeError`` inside the job engine, which is a place nobody is
    watching. Resolved the way ``cli.jobs.argv_for`` resolves it.
    """
    import importlib

    entry = registry.entry("acquire.download")
    assert entry.argv_builder == "download_argv"
    module = importlib.import_module(entry.module)
    assert callable(getattr(module, entry.argv_builder))


def test_download_on_an_absent_job_refuses_with_a_vocabulary_code(configured):  # noqa: F811
    code, out, _ = drive(
        ["--output", "json", "acquire", "download", "x", "--job", "no-such-job"]
    )
    assert code in {int(c) for c in ExitCode}
    assert code != int(ExitCode.OK)
    assert code != int(ExitCode.USAGE)


# ═══════════════════════════════════════════════════════════════════════════
# acquire.audit: the classification, and what it admits it cannot classify
# ═══════════════════════════════════════════════════════════════════════════


def test_every_audio_container_the_renamer_knows_has_a_classification():
    """The three sets partition the renamer's own table, DERIVED not listed.

    ``UNDECIDED_EXTS`` is the remainder, so this cannot fail by a format going
    unclassified: it fails when a format the renamer no longer knows is still
    named lossless or lossy here, which is the drift in the other direction.
    """
    known = frozenset(naming.AUDIO_EXTS)
    assert acquire_cli.LOSSLESS_EXTS | acquire_cli.LOSSY_EXTS | acquire_cli.UNDECIDED_EXTS == known
    assert not acquire_cli.LOSSLESS_EXTS & acquire_cli.LOSSY_EXTS
    assert acquire_cli.LOSSLESS_EXTS - known == frozenset()
    assert acquire_cli.LOSSY_EXTS - known == frozenset()


def test_the_undecided_remainder_is_the_mp4_container_today():
    """Pinned so a surprise addition is read rather than absorbed silently.

    The remainder is safe by construction, but a format landing in it without
    anybody noticing means a whole container is reported unclassified in every
    audit from that day. This is the line that makes that visible.
    """
    assert acquire_cli.UNDECIDED_EXTS == frozenset({".m4a"})


def test_audit_over_an_empty_library_is_a_well_formed_empty_review_set(configured):  # noqa: F811
    """An empty answer is an answer, not a failure. That is the fresh-install state."""
    from cratekit.cli import output

    code, out, _ = drive(["--output", "json", "acquire", "audit"])
    assert code == int(ExitCode.OK), out
    envelope = json.loads(out)
    assert output.envelope_problems(envelope) == [], envelope
    assert envelope["verb"] == "acquire.audit"
    assert envelope["data"] == {
        "queue": acquire_cli.AUDIT_QUEUE,
        "items": [],
        "unresolved": 0,
    }


def _kinds(root, *, policy, marker="[MP3]"):
    return {
        item["id"]: item["kind"]
        for item in acquire_cli.findings(root, policy=policy, marker=marker)
    }


def test_strict_policy_reports_every_lossy_file_marked_or_not(tmp_path):
    """Strict says the track is reported unacquired rather than downloaded lossy.

    So the marker is irrelevant under it: a marked lossy file satisfies the
    marking rule and still should not be in the library at all. Reporting only
    the unmarked ones would be applying the permissive policy's test to the
    strict policy, which is the shape of a check that agrees with no consumer.
    """
    root = tmp_path / "Music"
    root.mkdir()
    (root / "plain.mp3").write_bytes(b"x")
    (root / "Artist - Title [MP3].mp3").write_bytes(b"x")
    (root / "keeper.flac").write_bytes(b"x")

    found = _kinds(root, policy=LosslessPolicy.STRICT)
    assert found == {
        "plain.mp3": "lossy-under-strict",
        "Artist - Title [MP3].mp3": "lossy-under-strict",
    }


def test_permissive_policy_reports_only_the_unmarked_lossy_file(tmp_path):
    root = tmp_path / "Music"
    root.mkdir()
    (root / "plain.mp3").write_bytes(b"x")
    (root / "Artist - Title [MP3].mp3").write_bytes(b"x")

    found = _kinds(root, policy=LosslessPolicy.ALLOW_LOSSY_MARKED)
    assert found == {"plain.mp3": "lossy-unmarked"}


def test_a_lossless_file_wearing_the_marker_is_reported(tmp_path):
    """The marker is stripped by the naming engine, so a false one folds two files.

    ``library_template`` declares the marker precisely so a lossy copy and its
    lossless twin resolve to one recording. A lossless file carrying the marker
    is therefore not a cosmetic mistake: it collapses onto a different recording's
    key, which is the duplicate pair that docstring records the source system
    producing.
    """
    root = tmp_path / "Music"
    root.mkdir()
    (root / "Artist - Title [MP3].flac").write_bytes(b"x")
    (root / "honest.flac").write_bytes(b"x")

    for policy in LosslessPolicy:
        found = _kinds(root, policy=policy)
        assert found == {"Artist - Title [MP3].flac": "marked-lossless"}, policy


def test_an_mp4_container_is_reported_undecided_rather_than_assumed(tmp_path):
    """ALAC and AAC share the container, so the suffix cannot answer.

    Counting it either way would be a guess presented as a measurement. Under
    both policies it reports the same thing, because the container's ambiguity is
    not a function of the policy.
    """
    root = tmp_path / "Music"
    root.mkdir()
    (root / "ambiguous.m4a").write_bytes(b"x")

    for policy in LosslessPolicy:
        assert _kinds(root, policy=policy) == {"ambiguous.m4a": "format-undecided"}, policy


def test_a_configuration_with_no_marker_text_decides_no_marker_question(tmp_path):
    """Empty marker means no file carries one, so neither marker kind is decidable.

    ``library_template`` answers an empty marker by returning a template with no
    marker rule rather than refusing the run, and this agrees with it. The strict
    kind still fires, because it never consulted the marker.
    """
    root = tmp_path / "Music"
    root.mkdir()
    (root / "plain.mp3").write_bytes(b"x")
    (root / "Artist - Title [MP3].flac").write_bytes(b"x")

    assert _kinds(root, policy=LosslessPolicy.ALLOW_LOSSY_MARKED, marker="") == {}
    assert _kinds(root, policy=LosslessPolicy.STRICT, marker="") == {
        "plain.mp3": "lossy-under-strict"
    }


def test_a_music_directory_that_does_not_exist_is_empty_rather_than_an_error(tmp_path):
    assert acquire_cli.findings(
        tmp_path / "nothing-here", policy=LosslessPolicy.STRICT, marker="[MP3]"
    ) == ()


def test_non_audio_files_are_not_reported(tmp_path):
    """A music directory holds artwork, playlists and system files. None are findings.

    THE MARKED ARTWORK IS THE HALF THAT MATTERS, and the first version of this
    test did not have it. Cover art is routinely named after the track it belongs
    to, so ``Artist - Title [MP3].jpg`` sits beside ``Artist - Title [MP3].mp3``
    in a real library. Without that file here, mutating ``classify``'s unknown
    suffix from ``other`` to ``lossless`` killed NOTHING, promoted to the full
    suite and still killed nothing: the three unmarked files below take the same
    path either way, so the guard looked untested because the test never reached
    it. With the marked one, the mutation reports a JPEG as a lossless file
    wearing a lossy marker, which is a finding about a file that is not audio.
    """
    root = tmp_path / "Music"
    root.mkdir()
    (root / "cover.jpg").write_bytes(b"x")
    (root / ".DS_Store").write_bytes(b"x")
    (root / "notes.txt").write_bytes(b"x")
    (root / "Artist - Title [MP3].jpg").write_bytes(b"x")

    for policy in LosslessPolicy:
        assert _kinds(root, policy=policy) == {}, policy


def test_a_directory_it_cannot_list_is_reported(tmp_path):
    """THE FINDING THIS FILE EXISTS FOR, driven 2026-08-28.

    Written first with ``Path.rglob``, which swallows the ``PermissionError``
    raised by ``scandir`` and yields only what it reached. Over a root holding
    ``open/a.mp3`` and a mode 0o000 ``locked/`` containing ``b.mp3``, the audit
    reported one finding and said nothing whatever about ``locked``: its answer
    over a library it had audited half of was indistinguishable from its answer
    over a library it had audited all of.

    The producer is ordinary rather than contrived. The library root is a
    removable volume and macOS puts directories a walk cannot enter at the root
    of one as a matter of course, so an audit that silently skips them is an
    audit that silently skips them on every real library.

    Revert ``findings`` to ``root.rglob("*")`` and this is the row that dies.

    NO SKIP GUARD, deliberately. Running the battery as root would make the mode
    0o000 directory listable and the precondition unreachable, and the obvious
    reflex is ``skipif(os.geteuid() == 0)``. ``tests/test_pending_units.py``
    forbids that and is right to: a skip is a guard switched off with no record of
    when it switches back on, which is METHOD's own argument for deselecting
    nothing. So the precondition is ASSERTED instead. Under root this fails
    saying the environment cannot produce the state, which is a true report,
    where a skip would have read as a pass in every summary anybody looks at.
    """
    root = tmp_path / "Music"
    (root / "open").mkdir(parents=True)
    (root / "open" / "a.mp3").write_bytes(b"x")
    locked = root / "locked"
    locked.mkdir()
    (locked / "b.mp3").write_bytes(b"x")
    os.chmod(locked, 0o000)
    try:
        assert not os.access(locked, os.R_OK), (
            "this test needs a directory the walk cannot list, and this process "
            "can list it anyway; running the battery as root removes the state "
            "the guard below is measuring"
        )
        found = _kinds(root, policy=LosslessPolicy.STRICT)
    finally:
        os.chmod(locked, stat.S_IRWXU)

    assert found == {
        "open/a.mp3": "lossy-under-strict",
        "locked": "path-unreadable",
    }


def test_the_unreadable_row_counts_toward_the_outstanding_total(configured, tmp_path):  # noqa: F811
    """``unresolved`` must include what could not be read, or the number reassures.

    A count that silently excludes the directories the walk was refused is a
    count that says "nothing to do" to a person whose library is half unaudited.
    """
    music = configured.library.root / configured.library.music_dir
    locked = music / "locked"
    locked.mkdir(parents=True, exist_ok=True)
    (locked / "b.mp3").write_bytes(b"x")
    os.chmod(locked, 0o000)
    try:
        assert not os.access(locked, os.R_OK), "see the test above: no skip, an assertion"
        code, out, _ = drive(["--output", "json", "acquire", "audit"])
    finally:
        os.chmod(locked, stat.S_IRWXU)

    assert code == int(ExitCode.OK), out
    data = json.loads(out)["data"]
    assert data["unresolved"] == len(data["items"])
    assert [item["kind"] for item in data["items"]] == ["path-unreadable"]


def test_the_audit_writes_nothing(configured):  # noqa: F811
    """Declared as writing no surface, so a drive must leave the tree untouched."""
    music = configured.library.root / configured.library.music_dir
    (music / "plain.mp3").write_bytes(b"x")
    before = {p: p.stat().st_mtime_ns for p in sorted(music.rglob("*"))}

    assert registry.entry("acquire.audit").writes == frozenset()
    code, _, _ = drive(["acquire", "audit"])
    assert code == int(ExitCode.OK)

    after = {p: p.stat().st_mtime_ns for p in sorted(music.rglob("*"))}
    assert after == before


def test_the_audit_reads_the_policy_the_configuration_actually_holds(configured):  # noqa: F811
    """Not a default baked into the verb. Both policies are driven on one library.

    AE4's two halves are one function called with two policies, and the shell's
    job is to hand it the configured one. A verb that read a default would agree
    with the strict library and be silently wrong on the permissive one, which is
    the half a person only discovers by trusting a clean report.
    """
    music = configured.library.root / configured.library.music_dir
    (music / "Artist - Title [MP3].mp3").write_bytes(b"x")

    code, out, _ = drive(["--output", "json", "acquire", "audit"])
    assert code == int(ExitCode.OK), out
    strict = json.loads(out)["data"]
    assert strict["unresolved"] == 1, "strict refuses a lossy file even when marked"
    assert strict["items"][0]["kind"] == "lossy-under-strict"

    relaxed = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(configured.library.root),
                "volume_id": configured.library.volume_id,
                "db_path": str(configured.library.db_path),
            },
            "paths": {"download_staging": str(configured.paths.download_staging)},
            "profile": {"name": "full"},
            "acquisition": {"lossless_policy": "allow_lossy_marked"},
        }
    )
    config.save(relaxed)
    config.reset_cache()

    code, out, _ = drive(["--output", "json", "acquire", "audit"])
    assert code == int(ExitCode.OK), out
    assert json.loads(out)["data"] == {
        "queue": acquire_cli.AUDIT_QUEUE,
        "items": [],
        "unresolved": 0,
    }, "the permissive policy admits a MARKED lossy file"
