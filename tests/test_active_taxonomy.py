"""The one loader for a library's active taxonomy (R-685).

The routing plan that reads an edited active copy is in
``tests/test_routing_workers.py``, beside the fixtures that drive a plan.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from cratekit.core import active_taxonomy, config, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import Remedy
from tests.test_config import valid_data

SRC = Path(__file__).resolve().parents[1] / "src" / "cratekit"
LOADER = SRC / "core" / "active_taxonomy.py"
DEFINER = SRC / "core" / "taxonomy.py"


@pytest.fixture
def library(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "library"
    root.mkdir()
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    return root


@pytest.fixture
def cfg(library) -> config.Config:
    return config.from_dict(valid_data(library))


def _active(cfg: config.Config) -> Path:
    return config.state_path("taxonomy_active", cfg)


def write_active(cfg: config.Config, text: str) -> Path:
    """Put ``text`` where setup puts a library's active copy. Other suites use it."""
    path = _active(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _shipped_text() -> str:
    return taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME)


def shipped_without(section: str) -> str:
    """The shipped template's text with one top level table taken out.

    The shape of an active copy made before the shipped template gained that
    table, which is how the tenth sitting's library came to lack ``[long_tracks]``.
    """
    text = _shipped_text()
    header = f"\n[{section}]\n"
    assert text.count(header) == 1, section
    head, _, tail = text.partition(header)
    _, _, rest = tail.partition("\n[")
    return head + "\n[" + rest


# ---------------------------------------------------------------------------
# The guard: no verb reads the shipped template directly
# ---------------------------------------------------------------------------


# Each way a module could come to route by a template that is not the library's,
# and the only modules that may take it. Setup writes the active copy from the
# shipped text, and doctor parses the active copy to report on it. Doctor
# compares the copy against the shipped template by a fingerprint the definer
# computes (R-689), and stays OFF the shipped text list on purpose: a module
# holding the shipped text and the parser is one line from routing by it.
READERS = {
    "default_taxonomy": frozenset({LOADER, DEFINER}),
    "shipped_template_text": frozenset({LOADER, DEFINER, SRC / "cli" / "setup.py"}),
    "load_taxonomy": frozenset({LOADER, DEFINER, SRC / "cli" / "doctor.py"}),
}


def _reader_calls(path: Path) -> list[tuple[str, int]]:
    """Every call in ``path`` to a name in READERS, aliased imports resolved."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    bound = {name: name for name in READERS}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name in READERS:
                    bound[alias.asname or alias.name] = alias.name
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr in READERS:
            found.append((func.attr, node.lineno))
        elif isinstance(func, ast.Name) and func.id in bound:
            found.append((bound[func.id], node.lineno))
    return found


def test_no_module_but_the_loader_reads_the_shipped_template():
    """Every verb reads the ACTIVE copy, so a template is parsed nowhere else.

    An AST walk over every call, not a grep, with ``from ... import X as Y``
    resolved, so an alias or a line break does not hide one. Three spellings
    are watched, because routing by the shipped template can be written as the
    default loader, or as the shipped text handed to the parser.
    """
    offenders = []
    for path in sorted(SRC.rglob("*.py")):
        for name, line in _reader_calls(path):
            if path not in READERS[name]:
                offenders.append(f"{path.relative_to(SRC)}:{line} {name}")
    assert offenders == [], (
        "a module reads a taxonomy other than the library's active copy; read it "
        f"through cratekit.core.active_taxonomy.load: {offenders}"
    )


def test_the_guard_sees_every_spelling_it_should_refuse(tmp_path):
    """The walk above finds each one, so a green guard is not a blind one."""
    probe = tmp_path / "probe.py"
    probe.write_text(
        "from cratekit.core import taxonomy\n"
        "from cratekit.core.taxonomy import default_taxonomy\n"
        "from cratekit.core.taxonomy import default_taxonomy as shipped\n"
        "from cratekit.core.taxonomy import load_taxonomy as parse\n"
        "a = taxonomy.default_taxonomy()\n"
        "b = default_taxonomy()\n"
        "c = shipped()\n"
        "d = parse(taxonomy.shipped_template_text('default'))\n",
        encoding="utf-8",
    )
    assert sorted(_reader_calls(probe)) == [
        ("default_taxonomy", 5),
        ("default_taxonomy", 6),
        ("default_taxonomy", 7),
        ("load_taxonomy", 8),
        ("shipped_template_text", 8),
    ]


# ---------------------------------------------------------------------------
# The loader's answers
# ---------------------------------------------------------------------------


def test_an_edited_active_copy_is_the_answer(cfg):
    shipped = taxonomy.load_taxonomy(_shipped_text())
    bucket = shipped.buckets[0]
    renamed = _shipped_text().replace(
        f'display = "{bucket.display}"', 'display = "Renamed By Hand"', 1
    )
    assert renamed != _shipped_text()
    write_active(cfg, renamed)
    loaded = active_taxonomy.load(cfg)
    assert loaded.buckets[0].display == "Renamed By Hand"
    assert shipped.buckets[0].display != "Renamed By Hand"


def test_an_active_copy_without_a_section_the_shipped_template_gained_has_none(cfg):
    """The tenth sitting's measured case: ``[long_tracks]`` arrived after setup."""
    assert taxonomy.load_taxonomy(_shipped_text()).long_tracks is not None
    write_active(cfg, shipped_without("long_tracks"))
    assert active_taxonomy.load(cfg).long_tracks is None


def test_no_active_copy_on_a_present_library_falls_back_to_the_named_template(cfg):
    assert not _active(cfg).exists()
    loaded = active_taxonomy.load(cfg)
    assert loaded == taxonomy.load_taxonomy(_shipped_text())


def test_the_fallback_is_the_template_the_configuration_names(cfg, monkeypatch):
    """Not always ``default``: the name configuration recorded is the one read."""
    asked = []
    real = _shipped_text()

    def text(name):
        asked.append(name)
        return real

    monkeypatch.setattr(taxonomy, "shipped_template_text", text)
    named = config.from_dict(valid_data(cfg.library.root, taxonomy={"template": "friend"}))
    active_taxonomy.load(named)
    assert asked == ["friend"]


def test_a_named_template_nothing_ships_refuses(cfg):
    named = config.from_dict(valid_data(cfg.library.root, taxonomy={"template": "nothing_ships"}))
    with pytest.raises(CratekitError) as caught:
        active_taxonomy.load(named)
    assert caught.value.cause.reason == "config-unusable"
    assert caught.value.cause.remediation.remedy is Remedy.RUN_SETUP


def test_an_absent_library_root_refuses_rather_than_falling_back(cfg):
    """An unmounted volume is "could not look", never "no active copy"."""
    cfg.library.root.rmdir()
    with pytest.raises(CratekitError) as caught:
        active_taxonomy.load(cfg)
    assert caught.value.cause.reason == "library-volume-unmounted"
    assert caught.value.cause.remediation.remedy is Remedy.MOUNT_LIBRARY_VOLUME


def test_an_active_copy_that_does_not_parse_refuses_rather_than_falling_back(cfg):
    write_active(cfg, "this is = = not toml")
    with pytest.raises(CratekitError) as caught:
        active_taxonomy.load(cfg)
    assert caught.value.cause.reason == "config-unusable"
    assert caught.value.cause.remediation.remedy is Remedy.RUN_SETUP


def test_an_active_copy_that_is_not_a_taxonomy_refuses(cfg):
    write_active(cfg, "schema_version = 1\n")
    with pytest.raises(CratekitError) as caught:
        active_taxonomy.load(cfg)
    assert caught.value.cause.reason == "config-unusable"


def test_an_active_copy_that_is_not_text_refuses(cfg):
    path = _active(cfg)
    path.parent.mkdir(parents=True)
    path.write_bytes(b"\xff\xfe\x00bad")
    with pytest.raises(CratekitError) as caught:
        active_taxonomy.load(cfg)
    assert caught.value.cause.reason == "config-unusable"
    assert caught.value.cause.remediation.remedy is Remedy.REPORT_DEFECT


def test_an_active_copy_this_account_cannot_read_refuses_with_the_access_remedy(cfg):
    path = write_active(cfg, _shipped_text())
    path.chmod(0)
    try:
        with pytest.raises(CratekitError) as caught:
            active_taxonomy.load(cfg)
    finally:
        path.chmod(0o644)
    assert caught.value.cause.reason == "config-unusable"
    assert caught.value.cause.remediation.remedy is not Remedy.REPORT_DEFECT
