"""KTD23 layering and R19 stable identifiers, enforced as tests rather than as review.

**Import direction (KTD23).** Layers depend downward only: foundation,
domain, infrastructure, write, modules, CLI. The whole syntax tree is walked,
since both of the source system's violations hid behind a LAZY import (a
router reaching an optional analysis module, a shared helper importing a
feature module in a real cycle).

**No persisted display name (R19).** A taxonomy entry has a stable identifier
and a display name; records key on the identifier, because in the source
system renaming one genre touched six places and orphaned state keyed on the
old name.

Each checker is a pure function over source text, proved to bite on
synthetic sources before it runs over the real package.
"""

from __future__ import annotations

import ast
import importlib.util
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

# ── The layer ladder. Index is rank: lower index means lower layer. ──────────
LAYERS = ("foundation", "domain", "infrastructure", "write", "modules", "cli")
RANK = {name: index for index, name in enumerate(LAYERS)}

# Module-to-layer assignment. A module placed BY NAME is looked up first, so a
# directory never silently overrules a role; every other module takes its
# directory's layer from the patterns below. One line per placed module,
# sorted (U296), so a part split from a placed module adds its own line.
#
# The output envelope and the exit-code vocabulary live under cli/ but are
# foundation concepts every layer must use (KTD25); the tree registry lives
# under core/ but is a WRITE concern.
_PLACED: dict[str, str] = {
    "cratekit.cli.envelope": "foundation",
    "cratekit.cli.exit_codes": "foundation",
    "cratekit.cli.output": "foundation",
    # ``prompt`` is foundation (U107): the ONE reader of standard input, importing
    # nothing of this package, so a verb like ``label.sync_cli`` can ask through it.
    "cratekit.cli.prompt": "foundation",
    # ``cause`` is foundation for the reason ``exit_codes`` is (KTD25): every layer
    # builds one, and the envelope names it.
    "cratekit.core.cause": "foundation",
    "cratekit.core.config": "foundation",
    "cratekit.core.config_base": "foundation",
    "cratekit.core.config_schema": "foundation",
    "cratekit.core.config_validate": "foundation",
    #     * the convergence record is a WRITE concern under core/, so the
    #       assertion every tree writer makes ships below the writers.
    "cratekit.core.convergence": "write",
    "cratekit.core.exit_codes": "foundation",
    "cratekit.core.identity": "domain",
    "cratekit.core.locations": "foundation",
    "cratekit.core.match": "domain",
    "cratekit.core.naming": "foundation",
    "cratekit.core.output": "foundation",
    "cratekit.core.profiles": "foundation",
    # The restore takes the same exception: a WRITE concern under core/ that reads
    # the tree registry. Nothing beneath the write layer imports it.
    "cratekit.core.restore": "write",
    # U300: the restore's three parts take its place, one line each.
    "cratekit.core.restore_perform": "write",
    "cratekit.core.restore_recovery": "write",
    "cratekit.core.restore_retention": "write",
    "cratekit.core.routing": "domain",
    "cratekit.core.secrets": "foundation",
    "cratekit.core.state_files": "foundation",
    "cratekit.core.taxonomy": "domain",
    "cratekit.core.taxonomy_build": "domain",
    "cratekit.core.taxonomy_model": "domain",
    "cratekit.core.tombstone": "domain",
    "cratekit.core.tree_registry": "write",
    "cratekit.core.types": "foundation",
}

# Every module not placed by name, first match wins.
_LAYER_RULES: tuple[tuple[str, str], ...] = (
    (r"^cratekit\.core\.", "infrastructure"),
    (r"^cratekit\.write\.", "write"),
    (r"^cratekit\.cli\.", "cli"),
    # Package __init__ files rank at the TOP of the layers they contain, since an
    # initializer re-exports its members; the root package ranks at the bottom, so
    # ``import cratekit`` and ``crate --help`` stay cheap.
    (r"^cratekit\.core$", "infrastructure"),
    (r"^cratekit\.write$", "write"),
    (r"^cratekit\.cli$", "cli"),
    (r"^cratekit\.[a-z_]+\.", "modules"),
    (r"^cratekit\.[a-z_]+$", "modules"),
    (r"^cratekit$", "foundation"),
)

# Dotted paths that are PACKAGES rather than modules, so ``from cratekit.core
# import taxonomy`` is read as a module and ``from cratekit.core.config import
# load`` as a symbol.
_PACKAGE_DEPTH = 2  # "cratekit" and "cratekit.<subpackage>"

# Toggleable feature-module package names. A lower layer must not name one,
# even as a string, which is all a dynamic import needs.
MODULE_PACKAGES = frozenset(
    {
        "acquire", "intake", "analysis", "vocals", "label", "favorites",
        "setbuilder", "reports", "backup", "web", "desktop", "sync",
        "maintenance", "tagging", "master", "deletion", "export", "outbound",
        # U23. Adoption is always available (R5), which makes a dynamic import of it
        # from below more likely, not less.
        "adopt",
    }
)

# Taxonomy DISPLAY names (R19): in the template and config, never in code below
# the modules layer.
TAXONOMY_LITERALS = frozenset(
    {
        "BY GENRE + ENERGY", "BY GENRE", "INBOX", "Record Labels",
        "with vox", "High Energy", "Low Energy", "Med Energy",
        "Deep House", "Melodic House", "Progressive House", "Organic House",
        "Drum & Bass", "Electronica", "Downtempo", "Techno",
    }
)

# Operation names that identify a higher-layer verb, curated and compound so
# common words like "review" do not fire. Read from the CLI registry once it exists.
_FALLBACK_VERBS = frozenset(
    {
        "label-sweep", "set-builder", "vocal-restamp", "vocal-calibrate",
        "fetch-others", "playlist-labels", "label-import", "sort-inbox",
        "sort-unplaced", "audit-genre-playlists", "retag-electronica",
    }
)


def verb_names() -> frozenset[str]:
    """The authoritative verb list, from the CLI registry once it exists, never a hand-kept copy."""
    try:
        if importlib.util.find_spec("cratekit.cli.registry") is not None:
            import cratekit.cli.registry as registry  # noqa: PLC0415

            names = getattr(registry, "VERB_NAMES", None)
            if names:
                return frozenset(names)
    except (ImportError, ModuleNotFoundError):
        pass
    return _FALLBACK_VERBS


# The text a user types: a package-manager install line or Cratekit's own
# entry point. D2 says only the CLI renders a remediation token into a command,
# since the command depends on platform, package manager and interface. Matched
# anywhere in a constant, since a docstring is one.
_SHELL_COMMAND = re.compile(
    r"\b(?:brew|apt|apt-get|pipx|pip|sudo|port|winget|choco|dnf|yum|npm)\s+install\b"
)

# The entry point followed by a SUBCOMMAND, IN A COMMAND CONTEXT: quoted as
# code, after a shell prompt, or after an imperative. Bare flags are the entry
# point's own identity, and "crate" as an ordinary noun ("the crate registry")
# is correct prose a guard must not fail, or it gets worked around.
_CLI_INVOCATION = re.compile(
    r"(?:[`$]\s*|\b(?:run|runs|running|type|typing|invoke|invoking|execute|executing)\s+)"
    r"crate\s+(?!-)[a-z][a-z0-9]*(?:-[a-z0-9]+)*\b"
)


def layer_of(module: str) -> str:
    """Return the layer name for a dotted module path."""
    placed = _PLACED.get(module)
    if placed is not None:
        return placed
    for pattern, layer in _LAYER_RULES:
        if re.match(pattern, module):
            return layer
    raise AssertionError(
        f"{module!r} matches no layer rule. Every module must be placed in the "
        f"KTD23 ladder explicitly; an unplaced module is an unguarded one."
    )


# ── Rule 1: imports point downward only ──────────────────────────────────────


def import_direction_violations(source: str, module: str) -> list[str]:
    """One message per upward import in ``source``, function bodies included."""
    problems: list[str] = []
    own_rank = RANK[layer_of(module)]
    tree = ast.parse(source)

    for node in ast.walk(tree):
        targets: list[str] = []
        if isinstance(node, ast.Import):
            targets = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                # A relative import needs package context this pure checker lacks; the real
                # tree scan reports absolute paths and covers it there.
                continue
            if node.module:
                # Expand imported names into module paths ONLY when the source is a package,
                # so a symbol is never read as a module.
                if len(node.module.split(".")) <= _PACKAGE_DEPTH:
                    # Even from a package, dunders and CapWords are symbols, so
                    # ``from cratekit import __version__`` is not placed as a module.
                    targets = [
                        f"{node.module}.{a.name}"
                        for a in node.names
                        if a.name.islower() and not a.name.startswith("_")
                    ]
                if not targets:
                    targets = [node.module]
        if not targets:
            continue

        for candidate in targets:
            if not candidate.startswith("cratekit"):
                continue
            target_layer = layer_of(candidate)
            if RANK[target_layer] > own_rank:
                lazy = " (lazy import inside a function)" if _is_nested(tree, node) else ""
                problems.append(
                    f"{module} ({layer_of(module)}) imports {candidate} "
                    f"({target_layer}){lazy}; layers depend downward only (KTD23)"
                )
    return problems


def _is_nested(tree: ast.AST, node: ast.AST) -> bool:
    """True when ``node`` sits inside a function or class body: a lazy import."""
    for parent in ast.walk(tree):
        if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for child in ast.walk(parent):
                if child is node:
                    return True
    return False


# ── Rule 2: a lower layer never NAMES a higher-layer concept ─────────────────


def higher_concept_violations(source: str, module: str) -> list[str]:
    """One message per higher-layer name appearing as a string literal.

    This is Rule 1 written as data, ``importlib.import_module("cratekit.analysis.vocal")``,
    plus R19's half: no taxonomy display name below the modules layer.
    """
    if RANK[layer_of(module)] >= RANK["modules"]:
        return []

    problems: list[str] = []
    verbs = verb_names()

    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        value = node.value

        head = value.split(".")
        if len(head) >= 2 and head[0] == "cratekit" and head[1] in MODULE_PACKAGES:
            problems.append(
                f"{module} ({layer_of(module)}) names module {value!r} as a string; "
                f"a dynamic import is still an upward dependency (KTD23)"
            )
        if value in verbs:
            problems.append(
                f"{module} ({layer_of(module)}) names the verb {value!r}; "
                f"verbs belong to the CLI layer (KTD23)"
            )
        if value in TAXONOMY_LITERALS:
            problems.append(
                f"{module} ({layer_of(module)}) hardcodes the taxonomy display name "
                f"{value!r}; taxonomy is declared configuration, not a literal (R19)"
            )

        spelled = _SHELL_COMMAND.search(value)
        if spelled is not None:
            problems.append(
                f"{module} ({layer_of(module)}) spells the command "
                f"{spelled.group(0)!r}; remediation below the CLI is a structured "
                f"token the CLI renders, never the text a user types (D2)"
            )
        if _CLI_INVOCATION.search(value):
            problems.append(
                f"{module} ({layer_of(module)}) spells an invocation of a CLI "
                f"subcommand; remediation below the CLI is a structured token the "
                f"CLI renders, never the text a user types (D2)"
            )
    return problems


# ── Rule 3: no persisted record is keyed by a display name (R19) ─────────────

# Mapping operations whose FIRST argument is a key.
_KEY_METHODS = frozenset({"get", "setdefault", "pop", "__getitem__", "__contains__"})


def _names_a_display_name(node: ast.AST) -> bool:
    """True when the expression ends in a display-name attribute access."""
    return isinstance(node, ast.Attribute) and node.attr in {"display_name", "displayName"}


def persisted_display_name_violations(source: str, module: str) -> list[str]:
    """One message per record keyed by a display name.

    Structural: a display name may be read, printed and messaged, never placed
    in a key position, a dict literal key, a subscript, or a mapping lookup's
    first argument.
    """
    problems: list[str] = []

    def report(what: str, where: str) -> None:
        problems.append(
            f"{module}: {what} used as {where}; persisted records key on the "
            f"stable identifier, never the display name, so a rename does not "
            f"orphan history (R19)"
        )

    def describe(node: ast.AST) -> str | None:
        if _names_a_display_name(node):
            return f"display name {ast.unparse(node)!r}"
        if isinstance(node, ast.Constant) and node.value in TAXONOMY_LITERALS:
            return f"taxonomy display literal {node.value!r}"
        return None

    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Dict):
            for key in node.keys:
                if key is None:
                    continue
                what = describe(key)
                if what:
                    report(what, "a dict key")
        elif isinstance(node, ast.Subscript):
            what = describe(node.slice)
            if what:
                report(what, "a subscript key")
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr in _KEY_METHODS and node.args:
                what = describe(node.args[0])
                if what:
                    report(what, f"the key argument to .{func.attr}()")
        elif isinstance(node, ast.Compare):
            for op, comparator in zip(node.ops, node.comparators):
                if isinstance(op, (ast.In, ast.NotIn)):
                    what = describe(node.left)
                    if what:
                        report(what, f"a membership key against {ast.unparse(comparator)}")
    return problems


# ── Fixture tests: each rule bites ───────────────────────────────────────────


def test_layer_ladder_is_the_ktd23_order():
    assert LAYERS == ("foundation", "domain", "infrastructure", "write", "modules", "cli")


@pytest.mark.parametrize(
    "module, layer",
    [
        ("cratekit.core.config", "foundation"),
        ("cratekit.core.naming", "foundation"),
        ("cratekit.cli.output", "foundation"),
        ("cratekit.core.taxonomy", "domain"),
        ("cratekit.core.routing", "domain"),
        ("cratekit.core.rb_writer", "infrastructure"),
        ("cratekit.core.session", "infrastructure"),
        ("cratekit.core.tree_registry", "write"),
        ("cratekit.core.convergence", "write"),
        ("cratekit.write.rbxml", "write"),
        ("cratekit.write.trees", "write"),
        ("cratekit.write.rebuild", "write"),
        ("cratekit.acquire.download", "modules"),
        ("cratekit.intake.collection_xml", "modules"),
        ("cratekit.cli.sync", "cli"),
    ],
)
def test_every_planned_module_has_a_layer(module, layer):
    """The ladder covers the planned package, so the architecture decides a file's layer."""
    assert layer_of(module) == layer


def test_a_part_split_from_a_placed_module_is_placed_by_one_line_of_its_own(monkeypatch):
    """U296: a part split from ``core.config`` is placed by one line of its own and no other."""
    source = "from cratekit.core.config_locks import exclusive_lock\n"
    assert layer_of("cratekit.core.config_locks") == "infrastructure"
    assert len(import_direction_violations(source, "cratekit.core.config")) == 1

    monkeypatch.setitem(_PLACED, "cratekit.core.config_locks", "foundation")
    assert layer_of("cratekit.core.config_locks") == "foundation"
    assert import_direction_violations(source, "cratekit.core.config") == []
    assert layer_of("cratekit.core.config") == "foundation"


def test_the_placement_table_is_sorted_and_names_only_layers_of_the_ladder():
    """Sorted, so two cards adding parts add lines in different places."""
    assert list(_PLACED) == sorted(_PLACED)
    assert set(_PLACED.values()) <= set(LAYERS)
    # A module placed where its directory already puts it is a line that says nothing.
    for module, layer in _PLACED.items():
        by_directory = next(
            ranked for pattern, ranked in _LAYER_RULES if re.match(pattern, module)
        )
        assert by_directory != layer, f"{module} is placed where its directory already puts it"


def test_downward_and_same_layer_imports_pass():
    source = (
        "from cratekit.core.config import load\n"
        "from cratekit.core.naming import build\n"
    )
    assert import_direction_violations(source, "cratekit.core.routing") == []


def test_upward_import_from_a_lower_layer_fails():
    """The planted violation is the exact shape of the live one in the source."""
    source = "from cratekit.analysis.vocal_calibrate import load_threshold\n"
    problems = import_direction_violations(source, "cratekit.core.routing")
    assert len(problems) == 1
    assert "domain" in problems[0] and "modules" in problems[0]


def test_a_lazy_upward_import_is_still_a_violation():
    """A deferred import is a hidden dependency, the source system's slim install ImportError."""
    source = (
        "def clears_vocal_cut(level):\n"
        "    from cratekit.analysis.vocal_calibrate import load_threshold\n"
        "    return level >= load_threshold()\n"
    )
    problems = import_direction_violations(source, "cratekit.core.routing")
    assert len(problems) == 1
    assert "lazy import inside a function" in problems[0]


def test_a_cycle_masked_by_a_lazy_import_is_a_violation():
    """A shared helper importing a feature module is a real cycle, hidden by deferral."""
    source = (
        "def prepare(playlist):\n"
        "    from cratekit.intake import collection_xml\n"
        "    return collection_xml.prepare(playlist)\n"
    )
    problems = import_direction_violations(source, "cratekit.core.sweep_prep")
    assert len(problems) == 1
    assert "infrastructure" in problems[0]


def test_a_core_module_naming_a_feature_operation_fails():
    """Rule 1 written as data still has to fail. Otherwise the fix is one line."""
    source = 'MODULE = "cratekit.analysis.vocal_calibrate"\n'
    problems = higher_concept_violations(source, "cratekit.core.routing")
    assert len(problems) == 1 and "as a string" in problems[0]


def test_a_core_module_naming_a_verb_fails():
    """The planted verb name comes from the registry, so a rename cannot stale the fixture."""
    planted = sorted(verb_names())[0]
    source = f'WORKFLOW = "{planted}"\n'
    problems = higher_concept_violations(source, "cratekit.core.jobs")
    assert len(problems) == 1 and "names the verb" in problems[0]


def test_a_core_module_hardcoding_a_taxonomy_literal_fails():
    source = 'ROOT_FOLDER = "BY GENRE + ENERGY"\n'
    problems = higher_concept_violations(source, "cratekit.core.routing")
    assert len(problems) == 1 and "taxonomy display name" in problems[0]


def test_a_module_layer_file_may_name_its_own_concepts():
    """The rule is directional. A feature module naming its own verb is normal."""
    planted = sorted(verb_names())[0]
    source = f'WORKFLOW = "{planted}"\nFOLDER = "BY GENRE + ENERGY"\n'
    assert higher_concept_violations(source, "cratekit.label.sweep") == []


# ── D2: remediation below the CLI is a token, never a command line ───────────


def test_a_foundation_module_spelling_an_install_command_fails():
    """"brew install ffmpeg" below the CLI is an upward dependency written as English (D2)."""
    source = 'HINTS = {"ffmpeg": "brew install ffmpeg"}\n'
    problems = higher_concept_violations(source, "cratekit.core.binaries")
    assert len(problems) == 1 and "brew install" in problems[0]


def test_a_foundation_module_spelling_a_cli_invocation_fails():
    source = 'MESSAGE = "no configuration found; run crate setup to create it"\n'
    problems = higher_concept_violations(source, "cratekit.core.config")
    assert len(problems) == 1 and "invocation of a CLI subcommand" in problems[0]


@pytest.mark.parametrize(
    "source",
    [
        '"""The crate registry lives here."""\n',
        '"""crate state is per install, and each crate module declares its own."""\n',
        'NOTE = "one crate directory per library, one crate lock beside it"\n',
    ],
)
def test_prose_using_crate_as_an_ordinary_noun_passes(source):
    """"crate" as an ordinary noun passes, or the guard gets muted."""
    assert higher_concept_violations(source, "cratekit.core.config") == []


@pytest.mark.parametrize(
    "source",
    [
        'MESSAGE = "run crate setup first"\n',
        'DOC = "Fix it with `crate doctor --repair`."\n',
        'HELP = "$ crate label-sweep"\n',
    ],
)
def test_an_invocation_in_a_command_context_still_fails(source):
    """An invocation after an imperative, quoted as code, or after a prompt still fails."""
    problems = higher_concept_violations(source, "cratekit.core.config")
    assert len(problems) == 1 and "invocation of a CLI subcommand" in problems[0]


def test_a_foundation_module_may_name_the_entry_point_by_its_own_flags():
    """``crate --help`` is the entry point describing itself; a remediation names a subcommand."""
    source = '"""Cheap enough that crate --help runs before setup."""\n'
    assert higher_concept_violations(source, "cratekit.core.config") == []


def test_a_command_buried_in_a_docstring_still_fails():
    """A docstring is one string constant, so a check on its first words is not a check."""
    source = '"""Resolve binaries.\n\n    Missing ones need pipx install yt-dlp first.\n    """\n'
    problems = higher_concept_violations(source, "cratekit.core.binaries")
    assert len(problems) == 1 and "pipx install" in problems[0]


def test_prose_about_installing_without_a_command_passes():
    """Saying something must be installed, without a command, is this layer's own knowledge."""
    source = (
        'PLATFORM = "provided by the operating system; there is nothing to install"\n'
        'REMEDY = "install-keychain-backend"\n'
    )
    assert higher_concept_violations(source, "cratekit.core.secrets") == []


def test_a_module_layer_file_may_spell_its_own_remediation():
    """Directional, like every other rule here. The CLI is allowed to say it."""
    source = 'HELP = "brew install ffmpeg"\n'
    assert higher_concept_violations(source, "cratekit.cli.doctor") == []


# ── R19: display names are never keys ────────────────────────────────────────


def test_a_state_record_keyed_by_a_display_name_fails():
    source = "def save(entry, state):\n    state[entry.display_name] = {'done': True}\n"
    problems = persisted_display_name_violations(source, "cratekit.core.session")
    assert len(problems) == 1 and "subscript key" in problems[0]


def test_a_dict_literal_keyed_by_a_display_name_fails():
    source = "record = {entry.display_name: entry.count}\n"
    problems = persisted_display_name_violations(source, "cratekit.write.trees")
    assert len(problems) == 1 and "dict key" in problems[0]


def test_a_lookup_keyed_by_a_display_name_fails():
    source = "seen = state.get(entry.display_name)\n"
    problems = persisted_display_name_violations(source, "cratekit.core.session")
    assert len(problems) == 1 and ".get()" in problems[0]


def test_a_membership_test_on_a_display_name_fails():
    source = "if entry.display_name in watermarks:\n    pass\n"
    problems = persisted_display_name_violations(source, "cratekit.core.session")
    assert len(problems) == 1 and "membership key" in problems[0]


def test_a_taxonomy_display_literal_as_a_state_key_fails():
    """The literal form of the same mistake, and the more common one."""
    source = 'state["Deep House"] = {"last_synced": 0}\n'
    problems = persisted_display_name_violations(source, "cratekit.core.session")
    assert len(problems) == 1 and "taxonomy display literal" in problems[0]


def test_keying_on_the_stable_identifier_passes():
    """What correct code looks like, asserted so the guard cannot forbid it."""
    source = (
        "def save(entry, state):\n"
        "    state[entry.id] = {'display': entry.display_name, 'done': True}\n"
    )
    assert persisted_display_name_violations(source, "cratekit.core.session") == []


def test_displaying_a_display_name_passes():
    """A display name is for display. Reading and printing it is the whole point."""
    source = 'print(f"routed into {entry.display_name}")\nlabel = entry.display_name\n'
    assert persisted_display_name_violations(source, "cratekit.write.trees") == []


# ── The real package ─────────────────────────────────────────────────────────


def _package_modules() -> list[tuple[str, str]]:
    """Every module under src/ as (dotted name, source text)."""
    out: list[tuple[str, str]] = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
        relative = path.relative_to(SRC_ROOT).with_suffix("")
        parts = list(relative.parts)
        if parts[-1] == "__init__":
            parts.pop()
        out.append((".".join(parts), path.read_text()))
    return out


def test_the_package_imports_downward_only():
    problems: list[str] = []
    for module, source in _package_modules():
        problems += import_direction_violations(source, module)
    assert not problems, "KTD23 import-direction violations:\n" + "\n".join(problems)


def test_no_lower_layer_names_a_higher_layer_concept():
    problems: list[str] = []
    for module, source in _package_modules():
        problems += higher_concept_violations(source, module)
    assert not problems, "KTD23 naming violations:\n" + "\n".join(problems)


def test_no_persisted_record_is_keyed_by_a_display_name():
    problems: list[str] = []
    for module, source in _package_modules():
        problems += persisted_display_name_violations(source, module)
    assert not problems, "R19 violations:\n" + "\n".join(problems)


def test_every_package_module_is_placed_in_the_ladder():
    """An unplaced module is an unguarded one, so absence must be loud."""
    for module, _ in _package_modules():
        layer_of(module)  # raises with a clear message if unplaced


#: The write-ranked modules under ``core/``, and the ONE write-layer module each
#: is ranked so to reach.
_WRITE_RANKED_CORE_MODULES: dict[str, frozenset[str]] = {
    "cratekit.core.tree_registry": frozenset(),
    "cratekit.core.restore": frozenset(),
    "cratekit.core.restore_perform": frozenset(),
    "cratekit.core.restore_recovery": frozenset(),
    "cratekit.core.restore_retention": frozenset(),
}


def test_a_write_ranked_core_module_imports_no_write_layer_module():
    """A write-ranked core module imports no ``cratekit.write`` module, though its rank allows it.

    Ranking ``core.restore`` as write lets it read the tree registry, and also
    licenses the whole write layer; spending that licence must be a decision in
    this file.
    """
    offenders: dict[str, list[str]] = {}
    for module, source in _package_modules():
        allowed = _WRITE_RANKED_CORE_MODULES.get(module)
        if allowed is None:
            continue
        found = sorted(
            {
                name
                for name in _imported_cratekit_modules(source)
                if name.startswith("cratekit.write") and name not in allowed
            }
        )
        if found:
            offenders[module] = found
    assert not offenders, (
        f"a core module ranked write is using the whole layer its rank grants "
        f"rather than the one dependency the exception was taken for: {offenders}. "
        f"Either narrow the import or widen the entry above with the reason."
    )


def _imported_cratekit_modules(source: str) -> set[str]:
    """Every ``cratekit`` module path this source imports, lazy ones included."""
    found: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            found.add(node.module)
            found.update(f"{node.module}.{alias.name}" for alias in node.names)
    return {name for name in found if name.startswith("cratekit")}
