"""The one loader for a library's active taxonomy (R-685).

The routing plan that reads an edited active copy is in
``tests/test_routing_workers.py``, beside the fixtures that drive a plan.
"""

from __future__ import annotations

import ast
import shutil
import tomllib
from pathlib import Path

import pytest

from cratekit.core import active_taxonomy, config, taxonomy
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import Remedy
from tests._taxonomy_parses import counted, renamed_in_place, rewrite_keeping_time, unique
from tests.test_config import parsed, valid_data

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
    """The shipped text with one top level table out, as a copy made before the
    template gained it has it. Other suites use it."""
    text = _shipped_text()
    header = f"\n[{section}]\n"
    assert text.count(header) == 1, section
    head, _, tail = text.partition(header)
    _, _, rest = tail.partition("\n[")
    return head + "\n[" + rest


# The guard: no verb reads the shipped template directly. Each way a module
# could route by a template that is not the library's, and the only modules
# that may. Setup writes the copy from the shipped text; doctor parses the copy
# and compares it by the definer's fingerprint (R-689), so it stays off the
# shipped text list: a module holding the shipped text and the parser is one
# line from routing by it. The upgrade planner (U132) holds both, and the off
# taxonomy word answers (U194) parse the copy; both return text, never a parsed
# taxonomy, so nothing routes by what they read.
UPGRADER = SRC / "core" / "taxonomy_upgrade.py"
ANSWERER = SRC / "core" / "taxonomy_word.py"
READERS = {
    "default_taxonomy": frozenset({LOADER, DEFINER}),
    "shipped_template_text": frozenset({LOADER, DEFINER, UPGRADER, SRC / "cli" / "setup.py"}),
    "load_taxonomy": frozenset({LOADER, DEFINER, UPGRADER, ANSWERER, SRC / "cli" / "doctor.py"}),
}


def _reader_calls(path: Path) -> list[tuple[str, int]]:
    """Every call in ``path`` to a name in READERS, aliased imports resolved.

    A file naming none of them is skipped unparsed: every call the walk finds
    needs a READERS name written in the source, as an attribute or an import.
    """
    source = path.read_text(encoding="utf-8")
    if not any(name in source for name in READERS):
        return []
    tree = parsed(source)
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
    """Every verb reads the ACTIVE copy. An AST walk, not a grep, with aliased
    imports resolved, watching the default loader and the shipped text parsed."""
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


# The loader's answers.


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


def _named_nothing_ships(cfg):
    return config.from_dict(valid_data(cfg.library.root, taxonomy={"template": "nothing_ships"}))


def _unmounted(cfg):
    cfg.library.root.rmdir()
    return cfg


def _holding(content):
    def put(cfg):
        if isinstance(content, bytes):
            _active(cfg).parent.mkdir(parents=True)
            _active(cfg).write_bytes(content)
        else:
            write_active(cfg, content)
        return cfg

    return put


@pytest.mark.parametrize(
    ("arrange", "reason", "remedy"),
    [
        (_named_nothing_ships, "config-unusable", Remedy.RUN_SETUP),
        # An unmounted volume is "could not look", never "no active copy".
        (_unmounted, "library-volume-unmounted", Remedy.MOUNT_LIBRARY_VOLUME),
        (_holding("this is = = not toml"), "config-unusable", Remedy.RUN_SETUP),
        (_holding("schema_version = 1\n"), "config-unusable", None),
        (_holding(b"\xff\xfe\x00bad"), "config-unusable", Remedy.REPORT_DEFECT),
    ],
    ids=["named-template-nothing-ships", "library-root-absent", "copy-not-toml", "copy-not-a-taxonomy", "copy-not-text"],
)
def test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back(cfg, arrange, reason, remedy):
    with pytest.raises(CratekitError) as caught:
        active_taxonomy.load(arrange(cfg))
    assert caught.value.cause.reason == reason
    if remedy is not None:
        assert caught.value.cause.remediation.remedy is remedy


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


# Parsed once per text, read on every call (U247).


def test_a_copy_read_again_with_the_same_text_is_not_parsed_again(cfg, monkeypatch):
    text = unique(_shipped_text())
    write_active(cfg, text)
    parses = counted(monkeypatch)

    first, second = active_taxonomy.load(cfg), active_taxonomy.load(cfg)

    assert parses.of(text) == 1
    assert first == second == taxonomy.build_taxonomy(tomllib.loads(text))


def test_a_copy_rewritten_between_two_loads_is_read_and_judged_again(cfg, monkeypatch):
    """A person's edit between two items is what the second item is judged by.
    The edit keeps the length, the time and the inode, so only the text, the
    key, tells the two apart."""
    display = taxonomy.load_taxonomy(_shipped_text()).buckets[0].display
    before = unique(_shipped_text())
    after, renamed = renamed_in_place(before, display)
    path = write_active(cfg, before)
    parses = counted(monkeypatch)

    assert active_taxonomy.load(cfg).buckets[0].display == display
    rewrite_keeping_time(path, after)
    assert active_taxonomy.load(cfg).buckets[0].display == renamed
    rewrite_keeping_time(path, before)
    assert active_taxonomy.load(cfg).buckets[0].display == display

    assert (parses.of(before), parses.of(after)) == (1, 1)


def test_two_libraries_each_answer_their_own_copy(tmp_path, monkeypatch):
    """Two copies at two paths are two declarations, whichever was read first."""
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "config"))
    texts, cfgs = [], []
    for name in ("one", "two"):
        root = tmp_path / name
        root.mkdir()
        monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
        cfgs.append(config.from_dict(valid_data(root)))
        assert cfgs[-1].library.root == root
        text = unique(_shipped_text()).replace(
            f'display = "{taxonomy.load_taxonomy(_shipped_text()).buckets[0].display}"',
            f'display = "Library {name}"',
            1,
        )
        write_active(cfgs[-1], text)
        texts.append(text)

    assert _active(cfgs[0]) != _active(cfgs[1])
    assert active_taxonomy.load(cfgs[0]).buckets[0].display == "Library one"
    assert active_taxonomy.load(cfgs[1]).buckets[0].display == "Library two"
    assert active_taxonomy.load(cfgs[0]).buckets[0].display == "Library one"


def test_a_library_unmounted_after_a_good_load_still_refuses(cfg):
    """The memo answers a text, never a library: a copy nobody could read refuses."""
    write_active(cfg, _shipped_text())
    active_taxonomy.load(cfg)
    shutil.rmtree(cfg.library.root)
    for _ in range(2):
        with pytest.raises(CratekitError) as caught:
            active_taxonomy.load(cfg)
        assert caught.value.cause.reason == "library-volume-unmounted"


def test_a_copy_that_does_not_parse_refuses_on_every_load(cfg, monkeypatch):
    text = unique("this is = = not toml")
    write_active(cfg, text)
    parses = counted(monkeypatch)
    for _ in range(2):
        with pytest.raises(CratekitError) as caught:
            active_taxonomy.load(cfg)
        assert caught.value.cause.reason == "config-unusable"
    assert parses.of(text) == 2


def test_a_copy_that_breaks_after_a_good_load_refuses(cfg):
    """A good text's memo is never the answer for the broken text that replaced it."""
    path = write_active(cfg, _shipped_text())
    active_taxonomy.load(cfg)
    path.write_text("this is = = not toml", encoding="utf-8")
    with pytest.raises(CratekitError) as caught:
        active_taxonomy.load(cfg)
    assert caught.value.cause.reason == "config-unusable"
