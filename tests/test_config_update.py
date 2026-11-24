"""The configuration read-modify-write goes through one locked cycle (R-116).

Two writers of the whole document erased each other, so: no answers lost; a value both
changed is a refusal; no lock while a person is asked; the re-read is under the lock;
nothing under ``src/`` writes any other way.
"""

from __future__ import annotations

import ast
import copy
import json
import os
import subprocess
import sys
import textwrap
import unicodedata
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.cli import doctor, gates, prompt
from cratekit.cli import setup as setup_verb
from cratekit.cli.verbs import profile as profile_verb
from cratekit.core import config, profiles
from cratekit.core.exit_codes import ExitCode
from tests import doctor_machines
from tests.test_config import parsed

SRC = Path(__file__).resolve().parents[1] / "src" / "cratekit"
PROFILE_SET_SLIM = ["--output", "json", "-d", "profile.set.apply=apply", "profile", "set", "slim"]


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
    template = setup_verb.template_text("default").encode("utf-8")
    config.atomic_write_bytes(template, config.state_path("taxonomy_active", cfg))
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
    """Whether the write lock is free, asked through a second open file description."""
    import fcntl  # noqa: PLC0415

    path = config.config_path()
    lock = path.with_name(path.name + ".migrate.lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(fd, fcntl.LOCK_UN)
        return True
    except BlockingIOError:
        return False
    finally:
        os.close(fd)


def once(act):
    """``act`` the first time only, since some seams are crossed again under the lock."""
    fired = []

    def fire():
        if not fired:
            fired.append(True)
            act()

    return fire


def _another_writer(table: str, key: str, value):
    """Another command's ``config.update`` answering one key."""

    def write():
        def revise(document):
            document.setdefault(table, {})[key] = value
            return document

        config.update(revise)

    return write


def _between_the_read_and_the_write(monkeypatch, owner, name: str, act) -> None:
    """``owner.name`` patched so ``act`` runs, once, before the real one answers."""
    second_writer = once(act)
    original = getattr(owner, name)

    def between_the_read_and_the_write(*args, **kwargs):
        second_writer()
        return original(*args, **kwargs)

    monkeypatch.setattr(owner, name, between_the_read_and_the_write)


def _between_setup_read_and_write(monkeypatch, act) -> None:
    _between_the_read_and_the_write(monkeypatch, setup_verb, "_propose_pin", act)


def test_a_profile_change_made_while_the_wizard_was_deciding_survives_the_wizard(
    configured, monkeypatch, tmp_path
):
    """R-116's cost: the wizard never asked about the profile, so it may not write one."""
    elsewhere = str(tmp_path / "elsewhere")
    _between_setup_read_and_write(
        monkeypatch, lambda: config.update(lambda document: profiles.apply(document, "slim"))
    )
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
    act = _another_writer("paths", "download_staging", elsewhere)
    _between_the_read_and_the_write(monkeypatch, profile_verb.output, "digest_of", act)
    code, out, err = drive(PROFILE_SET_SLIM)
    assert code == int(ExitCode.OK), (out, err)
    written = on_disk()
    assert written["paths"]["download_staging"] == elsewhere, "profile set erased the wizard"
    assert written["profile"]["name"] == "slim"


def test_two_wizards_answering_one_key_differently_refuse_and_write_nothing(
    configured, monkeypatch, tmp_path
):
    ours, theirs = str(tmp_path / "ours"), str(tmp_path / "theirs")
    _between_setup_read_and_write(monkeypatch, _another_writer("paths", "download_staging", theirs))
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
    """A module toggled between the answer and the write makes the decision stale."""
    full, slim = profiles.resolve("full", {}), profiles.resolve("slim", {})
    toggled = sorted(full.modules - slim.modules)[0]
    second_writer = once(_another_writer("modules", toggled, False))
    original_require = gates.Gates.require

    def answered_and_then_the_document_moves(self, spec, **kwargs):
        chosen = original_require(self, spec, **kwargs)
        second_writer()
        return chosen

    monkeypatch.setattr(gates.Gates, "require", answered_and_then_the_document_moves)
    code, out, _err = drive(PROFILE_SET_SLIM)
    envelope = json.loads(out)
    assert envelope["cause"]["reason"] == "decision-stale", envelope
    assert code == int(ExitCode.DECISION_STALE)
    written = on_disk()
    assert written["profile"]["name"] == "full", "a stale decision was applied"
    assert written["modules"] == {toggled: False}


def test_the_wizard_does_not_hold_the_write_lock_while_it_asks(library, monkeypatch, tmp_path):
    """The question is reached with the lock free, so no command waits on someone typing."""
    monkeypatch.setattr(doctor, "Probes", lambda: doctor_machines.green())
    observed: list[bool] = []

    def answer():
        observed.append(lock_is_free())
        return "slim\n"

    real_prompter = prompt.Prompter
    monkeypatch.setattr(setup_verb.prompt, "Prompter", lambda: real_prompter(
        read_line=answer, read_secret=lambda _q: "", write=lambda _text: None))
    drive([
        "--output", "json", "setup", "--library-root", str(library),
        "--db-path", str(library / "db" / "master.db"), "--volume-id", doctor_machines.VOLUME,
        "--staging", str(tmp_path / "staging"), "--taxonomy", "default",
    ])
    assert observed, "the profile was never asked, so this test observed nothing"
    assert all(observed), "the write lock was held while a person was being asked"
    assert on_disk()["profile"]["name"] == "slim"


def test_update_reads_the_document_after_it_holds_the_lock(configured, monkeypatch, tmp_path):
    """Another process finishes as this one takes the lock (see test_config_migration)."""
    elsewhere = str(tmp_path / "elsewhere")
    moved = dict(document_for(configured.library.root))
    moved["paths"] = {"download_staging": elsewhere}
    original_enter = config.exclusive_lock.__enter__

    def another_process_finished_while_we_waited(self):
        acquired = original_enter(self)
        config.atomic_write_bytes(config.from_dict(moved).to_toml_bytes(), config.config_path())
        return acquired

    monkeypatch.setattr(config.exclusive_lock, "__enter__", another_process_finished_while_we_waited)
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
    """Three processes each read, wait for the others, and write one toggle; all survive."""
    import time  # noqa: PLC0415

    modules = list(profiles.MODULES[:3])
    go = tmp_path / "go"
    workers = []
    try:
        for module in modules:
            ready = tmp_path / f"ready-{module}"
            worker = subprocess.Popen(
                [sys.executable, "-c", _WORKER, module, str(ready), str(go)],
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, stderr=subprocess.PIPE,
            )
            workers.append((ready, worker))
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


BASE = {"a": {"x": 1, "y": 2}, "b": {"z": [1, 2]}, "top": "t"}


def _doc(**changes) -> dict:
    document = copy.deepcopy(BASE)
    for dotted, value in changes.items():
        table, _, key = dotted.rpartition("__")
        node = document[table] if table else document
        if value is None:
            node.pop(key, None)
        else:
            node[key] = value
    return document


@pytest.mark.parametrize(
    "desired,current,merged",
    [
        (_doc(a__x=9), _doc(), _doc(a__x=9)),
        (_doc(a__x=9), _doc(a__y=7, top="moved"),
         {"a": {"x": 9, "y": 7}, "b": {"z": [1, 2]}, "top": "moved"}),
        # The distinction the repair rests on: carried is not answered.
        (_doc(), _doc(top="moved"), _doc(top="moved")),
        (_doc(a__x=9), _doc(a__x=9), _doc(a__x=9)),
        ({**_doc(a__y=None), "c": {"new": True}}, _doc(top="moved"),
         {"a": {"x": 1}, "b": {"z": [1, 2]}, "c": {"new": True}, "top": "moved"}),
    ],
    ids=["unmoved-document-is-simply-replaced", "only-the-callers-leaves-are-applied",
         "carried-value-never-overwrites-the-other-writer", "one-value-from-both-is-agreement",
         "removed-key-removed-and-added-key-added"],
)
def test_merge_changes(desired, current, merged):
    assert config.merge_changes(BASE, desired, current) == merged


@pytest.mark.parametrize(
    "desired,current,keys",
    [
        # Every conflicting key is named, not only the first.
        (_doc(a__x=9, top="ours"), _doc(a__x=8, top="theirs"), ("a.x", "top")),
        (_doc(a__x=9), _doc(a__x=None), ("a.x",)),
        # A list is one answer and is never merged element by element.
        (_doc(b__z=[1, 2, 3]), _doc(b__z=[0, 1, 2]), ("b.z",)),
    ],
    ids=["every-conflicting-key-named", "changed-here-removed-there", "a-list-is-one-answer"],
)
def test_a_value_both_writers_changed_is_a_conflict(desired, current, keys):
    with pytest.raises(config.ConfigConflict) as refused:
        config.merge_changes(BASE, desired, current)
    assert refused.value.keys == keys
    assert ", ".join(keys) in str(refused.value)


def test_a_merge_shares_nothing_mutable_with_the_documents_it_was_given():
    desired, current = _doc(b__z=[5]), _doc(top="moved")
    merged = config.merge_changes(BASE, desired, current)
    merged["b"]["z"].append(6)
    merged["a"]["x"] = "changed"
    assert desired["b"]["z"] == [5]
    assert current["a"]["x"] == 1


def test_a_conflict_carries_the_setup_remedy_as_a_token():
    assert config.ConfigConflict.remedy is config.Remedy.RUN_SETUP


def _calls_config_save(tree: ast.AST) -> list[int]:
    """Lines calling ``cratekit.core.config.save``, through the module's imports and aliases."""
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
        func = node.func if isinstance(node, ast.Call) else None
        named = isinstance(func, ast.Name) and func.id in function_names
        held = isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name)
        if named or (held and func.attr == "save" and func.value.id in module_names):
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
    """Every shipped writer goes through ``config.update``, never ``config.save`` (R-116)."""
    offenders = {}
    for path in sorted(SRC.rglob("*.py")):
        relative = path.relative_to(SRC).as_posix()
        if relative == "core/config.py" or relative.startswith("_vendor/"):
            continue
        text = path.read_text(encoding="utf-8")
        # A file that never spells ``save`` as Python reads identifiers (NFKC) is not parsed.
        if "save" not in unicodedata.normalize("NFKC", text):
            continue
        found = _calls_config_save(parsed(text))
        if found:
            offenders[relative] = found
    assert not offenders, (
        f"config.save is called at {offenders}. It writes the whole document over "
        f"whatever another command wrote since this one read it. Use "
        f"config.update, and config.merge_changes when the caller holds answers."
    )
