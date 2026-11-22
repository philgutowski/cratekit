"""U42: the two acquisition shells, driven through the real dispatcher.

Both verbs are reachable, the download verb freezes and queues without reaching a provider,
and the audit reports a directory it is refused rather than a clean answer over it.
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



@pytest.mark.parametrize("name", VERBS)
def test_the_verb_is_landed_rather_than_planned(name):
    """A ``planned_in`` marker outliving its unit leaves a verb nothing checks."""
    entry = registry.entry(name)
    assert entry.landed, f"{name} still names a unit it was planned in"
    assert entry.module == "cratekit.acquire.cli"


@pytest.mark.parametrize("name", VERBS)
def test_the_verb_appears_in_help_and_dispatches(name, capsys, configured):  # noqa: F811
    """Reachable by a person. ``capsys`` is used because argparse prints help to the real
    stdout, and the usage LINE is matched since the bare word is in the parent's listing."""
    entry = registry.entry(name)
    code, _, _ = drive([*entry.path, "--help"])
    assert code == int(ExitCode.OK)
    printed = capsys.readouterr().out
    assert f"crate {' '.join(entry.path)}" in printed, printed


def test_neither_verb_is_hidden_behind_a_module_toggle():
    """Row 7 is a POLICY row, realized by ``acquisition.lossless_policy``; a toggle would
    recreate the state R21 forbids."""
    assert 7 in registry.POLICY_ROWS
    for name in VERBS:
        assert registry.entry(name).module_id is None



def test_download_over_an_absent_list_refuses_by_name(configured):  # noqa: F811
    """The list is READ at the queue as of U54, so an absent one is refused here."""
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
    """The shell must not touch the acquisition engines: each entry point is a detonator."""
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
    """The resume argv names the job and no gate run, as a WHOLE token (``--run-id``
    contains ``--run``)."""
    listed = configured.library.root / "l.json"
    listed.write_text(tidal_list([("100", "A", "B")]))
    code, out, _ = drive(["--output", "json", "acquire", "download", str(listed)])
    assert code == int(ExitCode.OK), out
    job_id = json.loads(out)["data"]["job_id"]

    from cratekit.core import jobs

    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
    argv = acquire_cli.download_argv(job)

    # R-668: the job froze the list, so the command that continues it names the job only.
    assert argv == ["acquire", "download", "--job", job_id]
    assert "--run" not in argv


def test_download_argv_is_the_builder_the_registry_names(configured):  # noqa: F811
    """The registry's ``argv_builder`` is looked up by NAME at resume time, as
    ``cli.jobs.argv_for`` does."""
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



def test_every_audio_container_the_renamer_knows_has_a_classification():
    """The three sets partition the renamer's own table, DERIVED not listed."""
    known = frozenset(naming.AUDIO_EXTS)
    assert acquire_cli.LOSSLESS_EXTS | acquire_cli.LOSSY_EXTS | acquire_cli.UNDECIDED_EXTS == known
    assert not acquire_cli.LOSSLESS_EXTS & acquire_cli.LOSSY_EXTS
    assert acquire_cli.LOSSLESS_EXTS - known == frozenset()
    assert acquire_cli.LOSSY_EXTS - known == frozenset()


def test_the_undecided_remainder_is_the_mp4_container_today():
    """Pinned so a format landing in the undecided remainder is read, not absorbed."""
    assert acquire_cli.UNDECIDED_EXTS == frozenset({".m4a"})


def test_audit_over_an_empty_library_is_a_well_formed_empty_review_set(configured):  # noqa: F811
    """An empty answer is an answer: the fresh-install state."""
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
    """Strict reports a lossy track as unacquired, so the marker is irrelevant under it."""
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
    """The naming engine strips the marker, so a lossless file carrying one collapses onto
    another recording."""
    root = tmp_path / "Music"
    root.mkdir()
    (root / "Artist - Title [MP3].flac").write_bytes(b"x")
    (root / "honest.flac").write_bytes(b"x")

    for policy in LosslessPolicy:
        found = _kinds(root, policy=policy)
        assert found == {"Artist - Title [MP3].flac": "marked-lossless"}, policy


def test_an_mp4_container_is_reported_undecided_rather_than_assumed(tmp_path):
    """ALAC and AAC share the container, so the suffix cannot answer under either policy."""
    root = tmp_path / "Music"
    root.mkdir()
    (root / "ambiguous.m4a").write_bytes(b"x")

    for policy in LosslessPolicy:
        assert _kinds(root, policy=policy) == {"ambiguous.m4a": "format-undecided"}, policy


def test_a_configuration_with_no_marker_text_decides_no_marker_question(tmp_path):
    """An empty marker means the marker kind is undecidable; the strict kind still fires."""
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
    """Artwork, playlists and system files are no findings; the marked artwork
    (``Artist - Title [MP3].jpg``) is the half that reaches ``classify``'s unknown branch."""
    root = tmp_path / "Music"
    root.mkdir()
    (root / "cover.jpg").write_bytes(b"x")
    (root / ".DS_Store").write_bytes(b"x")
    (root / "notes.txt").write_bytes(b"x")
    (root / "Artist - Title [MP3].jpg").write_bytes(b"x")

    for policy in LosslessPolicy:
        assert _kinds(root, policy=policy) == {}, policy


def test_a_directory_it_cannot_list_is_reported(tmp_path):
    """A directory the walk is refused is reported, not skipped (``Path.rglob`` swallowed it).

    No skip guard (``tests/test_pending_units.py`` forbids one): the precondition is
    asserted, so root fails saying the environment cannot produce it.
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
    """``unresolved`` must include what could not be read, or the number reassures."""
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
    """Both policies are driven on one library: the shell hands the audit the configured one."""
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
