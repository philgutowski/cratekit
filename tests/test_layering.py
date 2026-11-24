"""KTD23 layering and R19 stable identifiers, enforced as tests rather than as review.

Layers depend downward only, the whole syntax tree walked, since both of the source system's
violations hid behind a LAZY import. Records key on a taxonomy entry's stable identifier, never
its display name, since renaming one genre once orphaned state keyed on the old name. Each
checker is a pure function over source text, proved to bite before it reads the package.
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

# A module placed BY NAME is looked up first, so a directory never overrules a role; one
# sorted line each (U296). The envelope and exit codes are foundation under cli/ (KTD25).
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
    # The convergence record is a WRITE concern under core/, shipped below the writers.
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
    # A package initializer re-exports its members, so it ranks at the TOP of its layer;
    # the root ranks at the bottom, so ``import cratekit`` and ``crate --help`` stay cheap.
    (r"^cratekit\.core$", "infrastructure"),
    (r"^cratekit\.write$", "write"),
    (r"^cratekit\.cli$", "cli"),
    (r"^cratekit\.[a-z_]+\.", "modules"),
    (r"^cratekit\.[a-z_]+$", "modules"),
    (r"^cratekit$", "foundation"),
)

# Dotted paths this deep are PACKAGES, so a name imported from one is read as a module.
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


# An install line a user types: only the CLI renders a remediation token into a command (D2).
# Matched anywhere in a constant, since a docstring is one.
_SHELL_COMMAND = re.compile(
    r"\b(?:brew|apt|apt-get|pipx|pip|sudo|port|winget|choco|dnf|yum|npm)\s+install\b"
)

# The entry point and a SUBCOMMAND in a command context: quoted, after a prompt or an
# imperative. Bare flags and "crate" as an ordinary noun are correct prose and pass.
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
                # Needs package context this checker lacks; the tree scan covers it.
                continue
            if node.module:
                # Names become module paths ONLY from a package, so a symbol stays a symbol.
                if len(node.module.split(".")) <= _PACKAGE_DEPTH:
                    # Even from a package, dunders and CapWords are symbols.
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
    """One message per higher-layer name, verb, display name or command in a string literal."""
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
    """One message per display name in a key position: dict key, subscript, lookup, membership."""
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


IMPORTS, NAMES, KEYS = (
    import_direction_violations, higher_concept_violations, persisted_display_name_violations,
)

#: (rule, planted source, the module it sits in, words its one problem names). Each is the
#: exact shape of a mistake: deferred, written as data or prose, or a display name as a key.
PLANTED_VIOLATIONS = (
    pytest.param(
        IMPORTS, "from cratekit.analysis.vocal_calibrate import load_threshold\n",
        "cratekit.core.routing", ("domain", "modules"), id="upward-import-from-a-lower-layer",
    ),
    pytest.param(
        IMPORTS,
        "def clears_vocal_cut(level):\n"
        "    from cratekit.analysis.vocal_calibrate import load_threshold\n"
        "    return level >= load_threshold()\n",
        "cratekit.core.routing", ("lazy import inside a function",),
        id="a-lazy-upward-import-is-still-a-violation",
    ),
    pytest.param(
        IMPORTS,
        "def prepare(playlist):\n"
        "    from cratekit.intake import collection_xml\n"
        "    return collection_xml.prepare(playlist)\n",
        "cratekit.core.sweep_prep", ("infrastructure",),
        id="a-cycle-masked-by-a-lazy-import-is-a-violation",
    ),
    pytest.param(
        NAMES, 'MODULE = "cratekit.analysis.vocal_calibrate"\n', "cratekit.core.routing",
        ("as a string",), id="a-core-module-naming-a-feature-operation",
    ),
    pytest.param(
        NAMES, 'ROOT_FOLDER = "BY GENRE + ENERGY"\n', "cratekit.core.routing",
        ("taxonomy display name",), id="a-core-module-hardcoding-a-taxonomy-literal",
    ),
    pytest.param(
        NAMES, 'HINTS = {"ffmpeg": "brew install ffmpeg"}\n', "cratekit.core.binaries",
        ("brew install",), id="a-foundation-module-spelling-an-install-command",
    ),
    pytest.param(
        NAMES, 'MESSAGE = "no configuration found; run crate setup to create it"\n',
        "cratekit.core.config", ("invocation of a CLI subcommand",),
        id="a-foundation-module-spelling-a-cli-invocation",
    ),
    *(
        pytest.param(
            NAMES, source, "cratekit.core.config", ("invocation of a CLI subcommand",),
            id=f"an-invocation-in-a-command-context-{context}",
        )
        for context, source in (
            ("after-an-imperative", 'MESSAGE = "run crate setup first"\n'),
            ("quoted-as-code", 'DOC = "Fix it with `crate doctor --repair`."\n'),
            ("after-a-prompt", 'HELP = "$ crate label-sweep"\n'),
        )
    ),
    pytest.param(
        NAMES, '"""Resolve binaries.\n\n    Missing ones need pipx install yt-dlp first.\n'
        '    """\n', "cratekit.core.binaries", ("pipx install",),
        id="a-command-buried-in-a-docstring",
    ),
    pytest.param(
        KEYS, "def save(entry, state):\n    state[entry.display_name] = {'done': True}\n",
        "cratekit.core.session", ("subscript key",), id="a-state-record-keyed-by-a-display-name",
    ),
    pytest.param(
        KEYS, "record = {entry.display_name: entry.count}\n", "cratekit.write.trees",
        ("dict key",), id="a-dict-literal-keyed-by-a-display-name",
    ),
    pytest.param(
        KEYS, "seen = state.get(entry.display_name)\n", "cratekit.core.session", (".get()",),
        id="a-lookup-keyed-by-a-display-name",
    ),
    pytest.param(
        KEYS, "if entry.display_name in watermarks:\n    pass\n", "cratekit.core.session",
        ("membership key",), id="a-membership-test-on-a-display-name",
    ),
    pytest.param(
        KEYS, 'state["Deep House"] = {"last_synced": 0}\n', "cratekit.core.session",
        ("taxonomy display literal",), id="a-taxonomy-display-literal-as-a-state-key",
    ),
)


@pytest.mark.parametrize(("rule", "source", "module", "named"), PLANTED_VIOLATIONS)
def test_a_planted_violation_is_one_problem_naming_what_it_is(rule, source, module, named):
    """Running each rule against the evasion is what proves it a guard."""
    problems = rule(source, module)
    assert len(problems) == 1
    assert all(word in problems[0] for word in named), problems[0]


#: (rule, correct source, the module it sits in). A guard that fails correct code is muted.
CORRECT_CODE = (
    pytest.param(
        IMPORTS, "from cratekit.core.config import load\nfrom cratekit.core.naming import build\n",
        "cratekit.core.routing", id="downward-and-same-layer-imports",
    ),
    *(
        pytest.param(NAMES, source, "cratekit.core.config", id=f"crate-as-an-ordinary-noun-{n}")
        for n, source in enumerate((
            '"""The crate registry lives here."""\n',
            '"""crate state is per install, and each crate module declares its own."""\n',
            'NOTE = "one crate directory per library, one crate lock beside it"\n',
        ))
    ),
    pytest.param(
        NAMES, '"""Cheap enough that crate --help runs before setup."""\n', "cratekit.core.config",
        id="a-foundation-module-may-name-the-entry-point-by-its-own-flags",
    ),
    pytest.param(
        NAMES,
        'PLATFORM = "provided by the operating system; there is nothing to install"\n'
        'REMEDY = "install-keychain-backend"\n',
        "cratekit.core.secrets", id="prose-about-installing-without-a-command",
    ),
    pytest.param(
        NAMES, 'HELP = "brew install ffmpeg"\n', "cratekit.cli.doctor",
        id="a-module-layer-file-may-spell-its-own-remediation",
    ),
    pytest.param(
        KEYS,
        "def save(entry, state):\n"
        "    state[entry.id] = {'display': entry.display_name, 'done': True}\n",
        "cratekit.core.session", id="keying-on-the-stable-identifier",
    ),
    pytest.param(
        KEYS, 'print(f"routed into {entry.display_name}")\nlabel = entry.display_name\n',
        "cratekit.write.trees", id="displaying-a-display-name",
    ),
)


@pytest.mark.parametrize(("rule", "source", "module"), CORRECT_CODE)
def test_correct_code_passes_every_rule_that_could_misread_it(rule, source, module):
    """Every rule is directional: the CLI may spell a command and a module its own verb."""
    assert rule(source, module) == []


def test_a_core_module_naming_a_verb_fails():
    """The planted verb name comes from the registry, so a rename cannot stale the fixture."""
    planted = sorted(verb_names())[0]
    source = f'WORKFLOW = "{planted}"\n'
    problems = higher_concept_violations(source, "cratekit.core.jobs")
    assert len(problems) == 1 and "names the verb" in problems[0]


def test_a_module_layer_file_may_name_its_own_concepts():
    """The rule is directional. A feature module naming its own verb is normal."""
    planted = sorted(verb_names())[0]
    source = f'WORKFLOW = "{planted}"\nFOLDER = "BY GENRE + ENERGY"\n'
    assert higher_concept_violations(source, "cratekit.label.sweep") == []


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


@pytest.mark.parametrize(
    ("rule", "named"),
    [
        pytest.param(IMPORTS, "KTD23 import-direction", id="the-package-imports-downward-only"),
        pytest.param(NAMES, "KTD23 naming", id="no-lower-layer-names-a-higher-layer-concept"),
        pytest.param(KEYS, "R19", id="no-persisted-record-is-keyed-by-a-display-name"),
    ],
)
def test_the_real_package_breaks_no_rule(rule, named):
    problems = [found for module, source in _package_modules() for found in rule(source, module)]
    assert not problems, f"{named} violations:\n" + "\n".join(problems)


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
    """Its rank licenses the whole write layer, so spending that is a decision made here."""
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
