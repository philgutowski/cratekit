"""The configuration read-modify-write goes through one locked cycle (R-116).

Two verbs write ``config.toml``, ``crate setup`` and ``crate profile set``, and
both read it, take their time over a person's answer, and write it back. Until
this file each wrote the WHOLE document it had read, so two of them running at
once both reported success and the second erased the first.

What is pinned here, in the order a regression would hurt:

1. neither set of answers is lost, driven through the real dispatcher in both
   directions, with the second writer landing between the read and the write;
2. a value both writers changed is a refusal that writes nothing, never a pick;
3. the lock is NOT held while a person is being asked, which is the ledger's
   requirement on the fix and the reason the obvious fix is not shippable;
4. the re-read happens under the lock, and the lock excludes real processes;
5. nothing under ``src/`` writes the document any other way.
"""

from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import doctor, gates, output, prompt
from cratekit.cli import setup as setup_verb
from cratekit.cli.verbs import profile as profile_verb
from cratekit.core import config, profiles
from cratekit.core.exit_codes import ExitCode
from tests import doctor_machines

SRC = Path(__file__).resolve().parents[1] / "src" / "cratekit"


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture(autouse=True)
def _trap_standard_input(monkeypatch):
    """The wizard prompts, and a drive that reached a real terminal would BLOCK."""

    class Trapped:
        def __getattr__(self, name):
            raise AssertionError(f"a test in this file read standard input (sys.stdin.{name})")

    monkeypatch.setattr(sys, "stdin", Trapped())


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


def document_for(root: Path) -> dict:
    return {
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(root),
            "volume_id": doctor_machines.VOLUME,
            "db_path": str(root / "db" / "master.db"),
        },
        "paths": {"download_staging": str(root.parent / "staging")},
        "profile": {"name": "full"},
        "rekordbox": {"pinned_app_version": "7.0.1", "validated_on": "2026-08-01"},
    }


@pytest.fixture
def configured(library, monkeypatch):
    config.save(config.from_dict(document_for(library)))
    config.reset_cache()
    cfg = config.load()
    config.atomic_write_bytes(
        setup_verb.template_text("default").encode("utf-8"),
        config.state_path("taxonomy_active", cfg),
    )
    monkeypatch.setattr(doctor, "Probes", lambda: doctor_machines.green())
    return cfg


def drive(argv: list[str]) -> tuple[int, str, str]:
    import io

    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def on_disk() -> dict:
    config.reset_cache()
    return config.load().to_toml_dict()


def lock_is_free() -> bool:
    """Whether another holder could take the write lock right now.

    A non-blocking attempt through a SECOND open file description, which is what
    another process would hold. ``flock`` excludes between descriptions even
    inside one process, so this answers the question a second ``crate`` would ask
    without starting one.
    """
    import fcntl  # noqa: PLC0415

    path = config.config_path()
    lock = path.with_name(path.name + ".migrate.lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return False
        fcntl.flock(fd, fcntl.LOCK_UN)
        return True
    finally:
        os.close(fd)


def once(act):
    """``act`` the first time it is called and never again.

    The second writer is injected at a seam the verb crosses between its read
    and its write. Some of those seams are crossed AGAIN under the lock, where a
    second write from this process would wait on itself for ever.
    """
    fired = []

    def fire():
        if not fired:
            fired.append(True)
            act()

    return fire


# ═══════════════════════════════════════════════════════════════════════════
# 1. Neither set of answers is lost
# ═══════════════════════════════════════════════════════════════════════════


def test_a_profile_change_made_while_the_wizard_was_deciding_survives_the_wizard(
    configured, monkeypatch, tmp_path
):
    """THE COST IN R-116, reproduced through the real dispatcher.

    The wizard reads the document, another command adopts the slim profile, and
    the wizard then writes. It recorded ``profile.name`` as ``full`` at its
    first read and never asked about it, so it holds no answer about the profile
    and may not write one. Before the fix this ended with ``full`` on disk, the
    other command's success notwithstanding.
    """
    elsewhere = str(tmp_path / "elsewhere")
    second_writer = once(
        lambda: config.update(lambda document: profiles.apply(document, "slim"))
    )
    original = setup_verb._propose_pin

    def between_the_read_and_the_write(*args, **kwargs):
        second_writer()
        return original(*args, **kwargs)

    monkeypatch.setattr(setup_verb, "_propose_pin", between_the_read_and_the_write)

    code, out, err = drive(["--output", "json", "setup", "--staging", elsewhere])
    assert code == int(ExitCode.OK), (out, err)

    written = on_disk()
    assert written["profile"]["name"] == "slim", "the wizard erased the other command's answer"
    assert written["paths"]["download_staging"] == elsewhere, "the wizard lost its own answer"


def test_a_wizard_that_finished_while_a_profile_change_was_deciding_survives_it(
    configured, monkeypatch, tmp_path
):
    """The same cycle from the other verb, which is why the lock is not setup's."""
    elsewhere = str(tmp_path / "elsewhere")

    def the_wizard_writes():
        def revise(document):
            document["paths"]["download_staging"] = elsewhere
            return document

        config.update(revise)

    second_writer = once(the_wizard_writes)
    original = output.digest_of

    def between_the_read_and_the_write(payload):
        second_writer()
        return original(payload)

    monkeypatch.setattr(profile_verb.output, "digest_of", between_the_read_and_the_write)

    code, out, err = drive(
        ["--output", "json", "-d", "profile.set.apply=apply", "profile", "set", "slim"]
    )
    assert code == int(ExitCode.OK), (out, err)

    written = on_disk()
    assert written["paths"]["download_staging"] == elsewhere, "profile set erased the wizard"
    assert written["profile"]["name"] == "slim"


# ═══════════════════════════════════════════════════════════════════════════
# 2. A value both changed is a refusal, never a pick
# ═══════════════════════════════════════════════════════════════════════════


def test_two_wizards_answering_one_key_differently_refuse_and_write_nothing(
    configured, monkeypatch, tmp_path
):
    ours, theirs = str(tmp_path / "ours"), str(tmp_path / "theirs")

    def the_other_wizard_writes():
        def revise(document):
            document["paths"]["download_staging"] = theirs
            return document

        config.update(revise)

    second_writer = once(the_other_wizard_writes)
    original = setup_verb._propose_pin

    def between_the_read_and_the_write(*args, **kwargs):
        second_writer()
        return original(*args, **kwargs)

    monkeypatch.setattr(setup_verb, "_propose_pin", between_the_read_and_the_write)

    code, out, _err = drive(["--output", "json", "setup", "--staging", ours])
    envelope = json.loads(out)
    assert code == int(ExitCode.PRECONDITION)
    assert envelope["cause"]["reason"] == "config-unusable"
    assert envelope["cause"]["detail"]["kind"] == "ConfigConflict"
    assert "paths.download_staging" in envelope["cause"]["message"]
    assert envelope["cause"]["remediation"]["remedy"] == "run-setup"

    assert on_disk()["paths"]["download_staging"] == theirs, "a refusal wrote something"


def test_a_profile_decision_is_stale_when_the_membership_moved_before_the_write(
    configured, monkeypatch
):
    """The gate's own rule, held at the moment it matters.

    ``profile set`` shows a membership delta and the answer is to THAT delta.
    The gate compares digests when it is asked, which is before the write, so a
    module toggled between the answer and the write used to be applied under a
    decision nobody gave. The re-decision under the lock recomputes the delta
    from the document that is actually there.
    """
    full, slim = profiles.resolve("full", {}), profiles.resolve("slim", {})
    toggled = sorted(full.modules - slim.modules)[0]

    def a_module_is_switched_off_by_hand():
        def revise(document):
            document.setdefault("modules", {})[toggled] = False
            return document

        config.update(revise)

    second_writer = once(a_module_is_switched_off_by_hand)
    original_require = gates.Gates.require

    def answered_and_then_the_document_moves(self, spec, **kwargs):
        chosen = original_require(self, spec, **kwargs)
        second_writer()
        return chosen

    monkeypatch.setattr(gates.Gates, "require", answered_and_then_the_document_moves)

    code, out, _err = drive(
        ["--output", "json", "-d", "profile.set.apply=apply", "profile", "set", "slim"]
    )
    envelope = json.loads(out)
    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert code == int(ExitCode.DECISION_STALE)

    written = on_disk()
    assert written["profile"]["name"] == "full", "a stale decision was applied"
    assert written["modules"] == {toggled: False}


# ═══════════════════════════════════════════════════════════════════════════
# 3. The lock is not held while a person is being asked
# ═══════════════════════════════════════════════════════════════════════════


def test_the_wizard_does_not_hold_the_write_lock_while_it_asks(library, monkeypatch, tmp_path):
    """R-116's REQUIREMENT ON THE FIX, which the obvious fix fails.

    One lock from the first read to the final write closes the race and blocks
    every other command on somebody typing, for as long as they take. So the
    question is reached with the lock FREE, observed from inside the prompt
    itself, on a clean machine where the profile has to be asked.
    """
    monkeypatch.setattr(doctor, "Probes", lambda: doctor_machines.green())
    observed: list[bool] = []

    def answer():
        observed.append(lock_is_free())
        return "slim\n"

    real_prompter = prompt.Prompter
    monkeypatch.setattr(
        setup_verb.prompt,
        "Prompter",
        lambda: real_prompter(
            read_line=answer, read_secret=lambda _q: "", write=lambda _text: None
        ),
    )

    drive(
        [
            "--output", "json", "setup",
            "--library-root", str(library),
            "--db-path", str(library / "db" / "master.db"),
            "--volume-id", doctor_machines.VOLUME,
            "--staging", str(tmp_path / "staging"),
            "--taxonomy", "default",
        ]
    )
    assert observed, "the profile was never asked, so this test observed nothing"
    assert all(observed), "the write lock was held while a person was being asked"
    assert on_disk()["profile"]["name"] == "slim"


# ═══════════════════════════════════════════════════════════════════════════
# 4. The cycle itself
# ═══════════════════════════════════════════════════════════════════════════


def test_update_reads_the_document_after_it_holds_the_lock(configured, monkeypatch, tmp_path):
    """The lock is worthless if the read it protects already happened outside it.

    Another process finishes its write at the moment this one stops waiting for
    the lock, simulated inside ``__enter__`` for the reason
    ``test_config_migration.py`` gives: it is the only interleaving that
    reproduces it, and a real second process makes it a race rather than a proof.
    """
    elsewhere = str(tmp_path / "elsewhere")
    moved = dict(document_for(configured.library.root))
    moved["paths"] = {"download_staging": elsewhere}
    original_enter = config._exclusive_lock.__enter__

    def another_process_finished_while_we_waited(self):
        acquired = original_enter(self)
        config.atomic_write_bytes(
            config.from_dict(moved).to_toml_bytes(), config.config_path()
        )
        return acquired

    monkeypatch.setattr(
        config._exclusive_lock, "__enter__", another_process_finished_while_we_waited
    )
    seen: list[str] = []

    def revise(document):
        seen.append(document["paths"]["download_staging"])
        return profiles.apply(document, "slim")

    config.update(revise)
    assert seen == [elsewhere]
    written = on_disk()
    assert written["paths"]["download_staging"] == elsewhere
    assert written["profile"]["name"] == "slim"


def test_update_holds_the_lock_for_the_whole_cycle_and_releases_it(configured):
    held: list[bool] = []

    def revise(document):
        held.append(not lock_is_free())
        return document

    config.update(revise)
    assert held == [True]
    assert lock_is_free()


def test_save_takes_the_same_lock_so_it_cannot_land_inside_another_cycle(
    configured, monkeypatch
):
    held: list[bool] = []
    original = config.atomic_write_bytes

    def observed(payload, path, **kwargs):
        if path == config.config_path():
            held.append(not lock_is_free())
        return original(payload, path, **kwargs)

    monkeypatch.setattr(config, "atomic_write_bytes", observed)
    config.save(configured)
    assert held == [True]


def test_a_refusal_inside_the_cycle_writes_nothing_and_releases_the_lock(configured):
    before = config.config_path().read_bytes()

    def revise(_document):
        raise config.ConfigConflict(["library.root"])

    with pytest.raises(config.ConfigConflict):
        config.update(revise)
    assert config.config_path().read_bytes() == before
    assert lock_is_free()


def test_an_invalid_revision_is_refused_before_a_byte_is_written(configured):
    before = config.config_path().read_bytes()

    def revise(document):
        del document["library"]["volume_id"]
        return document

    with pytest.raises(config.ConfigInvalid):
        config.update(revise)
    assert config.config_path().read_bytes() == before


def test_update_on_a_machine_with_no_configuration_starts_from_an_empty_document(library):
    seen: list[dict] = []

    def revise(document):
        seen.append(dict(document))
        return document_for(library)

    cfg, path = config.update(revise)
    assert seen == [{}]
    assert path == config.config_path()
    assert cfg.to_toml_dict() == on_disk()


def test_update_will_not_write_over_a_document_it_cannot_understand(library):
    path = config.config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("this is not = = toml")
    with pytest.raises(config.ConfigCorrupt):
        config.update(lambda _document: document_for(library))
    assert path.read_text() == "this is not = = toml"


def test_an_incomplete_document_reaches_the_revision_as_it_is_spelled(library):
    """``crate setup`` completes an incomplete file, so it has to be able to see one."""
    path = config.config_path()
    incomplete = {"schema_version": config.CURRENT_SCHEMA_VERSION, "profile": {"name": "slim"}}
    config.atomic_write_bytes(__import__("tomli_w").dumps(incomplete).encode("utf-8"), path)
    seen: list[dict] = []

    def revise(document):
        seen.append(document)
        return {**document_for(library), "profile": document["profile"]}

    config.update(revise)
    assert seen == [incomplete]
    assert on_disk()["profile"]["name"] == "slim"


_WORKER = textwrap.dedent(
    """
    import sys, time
    from pathlib import Path
    from cratekit.core import config

    module, ready, go = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    ready.touch()
    deadline = time.monotonic() + 60
    while not go.exists():
        if time.monotonic() > deadline:
            sys.exit(3)
        time.sleep(0.005)

    def revise(document):
        time.sleep(0.4)
        document.setdefault("modules", {})[module] = False
        return document

    config.update(revise)
    """
)


def test_three_real_processes_writing_at_once_all_keep_their_answers(configured, tmp_path):
    """The exclusion, observed between processes rather than argued from ``flock``.

    Each worker reads, waits long enough for the others to read the same bytes,
    and writes one module toggle. Unlocked, every worker reads the document
    before any of them writes and the last write is the only survivor. They are
    released together from a file they poll, so process start-up skew is not
    what separates them.
    """
    import time  # noqa: PLC0415

    modules = list(profiles.MODULES[:3])
    go = tmp_path / "go"
    workers = []
    try:
        for module in modules:
            ready = tmp_path / f"ready-{module}"
            workers.append(
                (
                    ready,
                    subprocess.Popen(
                        [sys.executable, "-c", _WORKER, module, str(ready), str(go)],
                        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                        stderr=subprocess.PIPE,
                    ),
                )
            )
        deadline = time.monotonic() + 60
        while not all(ready.exists() for ready, _ in workers):
            assert time.monotonic() < deadline, "a worker never started"
            time.sleep(0.01)
        go.touch()
        for _ready, worker in workers:
            _out, err = worker.communicate(timeout=60)
            assert worker.returncode == 0, err.decode()
    finally:
        for _ready, worker in workers:
            if worker.poll() is None:
                worker.kill()
                worker.wait()

    assert on_disk()["modules"] == {module: False for module in sorted(modules)}


# ═══════════════════════════════════════════════════════════════════════════
# 5. merge_changes
# ═══════════════════════════════════════════════════════════════════════════


BASE = {"a": {"x": 1, "y": 2}, "b": {"z": [1, 2]}, "top": "t"}


def _doc(**changes) -> dict:
    import copy  # noqa: PLC0415

    document = copy.deepcopy(BASE)
    for dotted, value in changes.items():
        table, _, key = dotted.rpartition("__")
        node = document[table] if table else document
        if value is None:
            node.pop(key, None)
        else:
            node[key] = value
    return document


def test_an_unmoved_document_is_simply_replaced():
    desired = _doc(a__x=9)
    assert config.merge_changes(BASE, desired, _doc()) == desired


def test_only_the_leaves_the_caller_changed_are_applied():
    merged = config.merge_changes(BASE, _doc(a__x=9), _doc(a__y=7, top="moved"))
    assert merged == {"a": {"x": 9, "y": 7}, "b": {"z": [1, 2]}, "top": "moved"}


def test_a_value_the_caller_carried_through_never_overwrites_the_other_writer():
    """The distinction the repair rests on: carried is not answered."""
    merged = config.merge_changes(BASE, _doc(), _doc(top="moved"))
    assert merged["top"] == "moved"


def test_both_writers_arriving_at_one_value_is_agreement():
    assert config.merge_changes(BASE, _doc(a__x=9), _doc(a__x=9))["a"]["x"] == 9


def test_every_conflicting_key_is_named_and_not_only_the_first():
    with pytest.raises(config.ConfigConflict) as refused:
        config.merge_changes(BASE, _doc(a__x=9, top="ours"), _doc(a__x=8, top="theirs"))
    assert refused.value.keys == ("a.x", "top")
    assert "a.x, top" in str(refused.value)


def test_a_key_the_caller_removed_is_removed_and_one_it_added_is_added():
    desired = _doc(a__y=None)
    desired["c"] = {"new": True}
    merged = config.merge_changes(BASE, desired, _doc(top="moved"))
    assert merged == {"a": {"x": 1}, "b": {"z": [1, 2]}, "c": {"new": True}, "top": "moved"}


def test_a_key_the_caller_changed_and_the_other_writer_removed_is_a_conflict():
    with pytest.raises(config.ConfigConflict) as refused:
        config.merge_changes(BASE, _doc(a__x=9), _doc(a__x=None))
    assert refused.value.keys == ("a.x",)


def test_a_list_is_one_answer_and_is_never_merged_element_by_element():
    with pytest.raises(config.ConfigConflict):
        config.merge_changes(BASE, _doc(b__z=[1, 2, 3]), _doc(b__z=[0, 1, 2]))


def test_a_merge_shares_nothing_mutable_with_the_documents_it_was_given():
    desired, current = _doc(b__z=[5]), _doc(top="moved")
    merged = config.merge_changes(BASE, desired, current)
    merged["b"]["z"].append(6)
    merged["a"]["x"] = "changed"
    assert desired["b"]["z"] == [5]
    assert current["a"]["x"] == 1


def test_a_conflict_carries_the_setup_remedy_as_a_token():
    assert config.ConfigConflict.remedy is config.Remedy.RUN_SETUP


# ═══════════════════════════════════════════════════════════════════════════
# 6. Nothing writes the document any other way
# ═══════════════════════════════════════════════════════════════════════════


def _calls_config_save(tree: ast.AST) -> list[int]:
    """Line numbers of calls that resolve to ``cratekit.core.config.save``.

    Resolved through the module's own imports rather than matched on the text
    ``config.save``, so an alias, ``from cratekit.core import config as c``, or a
    bare ``from cratekit.core.config import save`` is found as well.
    """
    module_names: set[str] = set()
    function_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "cratekit.core":
            module_names |= {a.asname or a.name for a in node.names if a.name == "config"}
        elif isinstance(node, ast.ImportFrom) and node.module == "cratekit.core.config":
            function_names |= {a.asname or a.name for a in node.names if a.name == "save"}
        elif isinstance(node, ast.Import):
            module_names |= {
                a.asname for a in node.names if a.name == "cratekit.core.config" and a.asname
            }
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id in function_names:
            found.append(node.lineno)
        elif (
            isinstance(func, ast.Attribute)
            and func.attr == "save"
            and isinstance(func.value, ast.Name)
            and func.value.id in module_names
        ):
            found.append(node.lineno)
    return found


def test_the_guard_below_can_see_every_spelling_of_the_call():
    """A guard that cannot fail is not one, so it is shown a violation first."""
    for source in (
        "from cratekit.core import config\nconfig.save(cfg)",
        "from cratekit.core import config as c\nc.save(cfg)",
        "from cratekit.core.config import save\nsave(cfg)",
        "import cratekit.core.config as settings\nsettings.save(cfg)",
    ):
        assert _calls_config_save(ast.parse(source)) == [2], source
    assert _calls_config_save(ast.parse("from cratekit.cli import gates\ngates.save(s)")) == []


def test_nothing_under_src_writes_the_whole_document_after_reading_it():
    """Every shipped writer goes through ``config.update``.

    ``config.save`` replaces the document with whatever its caller holds. A verb
    holds what it READ, so a verb calling it is the R-116 cycle again, and it
    would pass every test above because those drive the two verbs that exist
    today. The vendored downloader is skipped: it has a ``save`` of its own and
    never imports this module.
    """
    offenders = {}
    for path in sorted(SRC.rglob("*.py")):
        relative = path.relative_to(SRC).as_posix()
        if relative == "core/config.py" or relative.startswith("_vendor/"):
            continue
        found = _calls_config_save(ast.parse(path.read_text(encoding="utf-8")))
        if found:
            offenders[relative] = found
    assert not offenders, (
        f"config.save is called at {offenders}. It writes the whole document over "
        f"whatever another command wrote since this one read it. Use "
        f"config.update, and config.merge_changes when the caller holds answers."
    )
