"""KTD23 layering and R19 stable identifiers, enforced as tests rather than as review.

Two guards live here because they fail the same way: quietly, at a distance, on
somebody else's machine.

**Import direction (KTD23).** Layers depend downward only. Lowest first:
foundation, domain, infrastructure, write, modules, CLI. A module may import its
own layer or anything below it, never anything above.

The source system violates this twice, and both violations are hidden behind a
LAZY import, which is why the check below walks the whole syntax tree rather than
just the module header:

* The shared router reaches up into an analysis module to load a calibration
  threshold. The analysis module is an optional extra that a slim install does
  not have. So on a slim install the router raises ImportError the first time a
  track needs vocal routing, and the traceback names an import inside a function,
  not the packaging decision that caused it.
* A sweep helper in the shared layer imports a feature module. That is a genuine
  cycle, since the feature module already depends on the shared layer. It works
  today only because the import is deferred until call time, which is to say the
  cycle is real and the laziness is what hides it.

Neither is ported. Both are fixed by construction: the guard is here first, so
the shape cannot arrive.

**No persisted display name (R19).** A taxonomy entry has a stable identifier and
a display name, and they are different things. Persisted records key on the
identifier. The reason is concrete: in the source system a playlist name is
simultaneously code, config, a persisted state key, XML bytes, a genre lookup
row, and a folder in the user's rekordbox. Renaming one genre touches all six,
and any state keyed on the old display name is orphaned the moment the rename
lands. The guard makes a display name unusable as a key.

Both checkers are pure functions over source text, in the same shape as the
skills lint: fixture tests prove each rule bites against synthetic sources, then
a final test runs the checker over the real package. That matters here more than
usual, because the real package is nearly empty in this unit. The fixture tests
are what prove the guard works BEFORE there is anything to guard.
"""

from __future__ import annotations

import ast
import importlib.util
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

# ---------------------------------------------------------------------------
# The layer ladder. Index is rank: lower index means lower layer.
# ---------------------------------------------------------------------------
LAYERS = ("foundation", "domain", "infrastructure", "write", "modules", "cli")
RANK = {name: index for index, name in enumerate(LAYERS)}

# Module-to-layer assignment, first match wins. Explicit overrides come first so
# that a module's DIRECTORY never silently overrules its role. Two of those
# overrides matter:
#
#   * the output envelope and the exit-code vocabulary live under cli/ for
#     packaging reasons but are foundation concepts, reserved globally before any
#     verb ships (KTD25). Ranking them as CLI would forbid every layer from using
#     the one output contract they are all required to use.
#   * the tree registry lives under core/ but is a WRITE concern.
_LAYER_RULES: tuple[tuple[str, str], ...] = (
    (r"^cratekit\.cli\.(output|exit_codes|envelope)$", "foundation"),
    # ``cause`` joins the foundation list for the same reason ``exit_codes``
    # does: KTD25 reserves the failure vocabulary globally, before any verb
    # ships, and every layer from the adapter upwards has to be able to build one.
    # Ranking it as infrastructure would forbid the output envelope, which is
    # foundation, from naming the type it carries.
    (
        r"^cratekit\.core\."
        r"(config|secrets|types|locations|naming|profiles|output|exit_codes|cause)$",
        "foundation",
    ),
    (r"^cratekit\.core\.(taxonomy|routing|match|identity|tombstone)$", "domain"),
    #     * the convergence record joins it for the same reason and by the same
    #       argument the registry's own docstring makes: it is a WRITE concern
    #       living under core/ so that the assertion every database tree writer
    #       is required to make ships below the writers that make it. A check
    #       that lived with each writer would be several implementations of one
    #       rule, which is how they come to disagree.
    (r"^cratekit\.core\.(tree_registry|convergence)$", "write"),
    # The restore takes the SAME exception, for the same reason and with the same
    # cost. It lives under core/ because the pending register and the state
    # inventory both name it there, and it is a WRITE concern: it reads the tree
    # registry to decide which trees a pre-cutover restore leaves unconverged, and
    # a module ranked below the registry cannot ask it. Nothing beneath the write
    # layer imports it, which is what keeps the exception free: the session
    # boundary underneath reaches ``core.reconcile``, which is infrastructure and
    # deliberately does not touch the registry at all.
    (r"^cratekit\.core\.restore$", "write"),
    (r"^cratekit\.core\.", "infrastructure"),
    (r"^cratekit\.write\.", "write"),
    (r"^cratekit\.cli\.", "cli"),
    # The package __init__ files themselves, ranked at the TOP of the layers they
    # contain, because a package initializer legitimately re-exports its own
    # members. The root package is the exception: it is ranked at the bottom, so
    # `import cratekit` stays free of everything and `crate --help` cannot become
    # expensive by accident.
    (r"^cratekit\.core$", "infrastructure"),
    (r"^cratekit\.write$", "write"),
    (r"^cratekit\.cli$", "cli"),
    (r"^cratekit\.[a-z_]+\.", "modules"),
    (r"^cratekit\.[a-z_]+$", "modules"),
    (r"^cratekit$", "foundation"),
)

# Dotted paths that are PACKAGES rather than modules. Needed to read an import
# correctly: in `from cratekit.core import taxonomy` the dependency is on
# cratekit.core.taxonomy, while in `from cratekit.core.config import load` it is
# on cratekit.core.config and `load` is a symbol, not a module. Treating a symbol
# as a module makes the checker report imports that do not exist.
_PACKAGE_DEPTH = 2  # "cratekit" and "cratekit.<subpackage>"

# Toggleable feature-module package names. A lower layer must not name one, even
# as a string, because a string is all a dynamic import needs.
MODULE_PACKAGES = frozenset(
    {
        "acquire", "intake", "analysis", "vocals", "label", "favorites",
        "setbuilder", "reports", "backup", "web", "desktop", "sync",
        "maintenance", "tagging", "master", "deletion", "export", "outbound",
        # U23. Library adoption is a Module row that stays available in every
        # profile (R5), which makes it MORE likely to be reached for from below
        # rather than less: "it is always there" is exactly the reasoning that
        # produces a dynamic import in a core module.
        "adopt",
    }
)

# Taxonomy DISPLAY names. R19: these live in the shipped template and in the
# user's config, never in code below the modules layer. Routing, sorting,
# auditing, and sync operate on the declared taxonomy.
TAXONOMY_LITERALS = frozenset(
    {
        "BY GENRE + ENERGY", "BY GENRE", "INBOX", "Record Labels",
        "with vox", "High Energy", "Low Energy", "Med Energy",
        "Deep House", "Melodic House", "Progressive House", "Organic House",
        "Drum & Bass", "Electronica", "Downtempo", "Techno",
    }
)

# Operation names that identify a higher-layer verb. Curated and compound on
# purpose: single common words like "review" or "delete" name infrastructure
# concepts too, and a guard that fires on those gets muted rather than obeyed.
# Once the CLI registry lands (U5) this is read from it instead, and the fallback
# below stops being the source of truth.
_FALLBACK_VERBS = frozenset(
    {
        "label-sweep", "set-builder", "vocal-restamp", "vocal-calibrate",
        "fetch-others", "playlist-labels", "label-import", "sort-inbox",
        "sort-unplaced", "audit-genre-playlists", "retag-electronica",
    }
)


def verb_names() -> frozenset[str]:
    """The authoritative verb list, from the CLI registry once it exists.

    Reading the registry rather than a hand-kept copy is the same lesson the CI
    dependency list taught: a hand-mirrored list is a list that drifts, and the
    drift shows up as a guard that stopped guarding.
    """
    try:
        if importlib.util.find_spec("cratekit.cli.registry") is not None:
            import cratekit.cli.registry as registry  # noqa: PLC0415

            names = getattr(registry, "VERB_NAMES", None)
            if names:
                return frozenset(names)
    except (ImportError, ModuleNotFoundError):
        pass
    return _FALLBACK_VERBS


# The text a user types, in the two shapes that actually turned up below the CLI:
# a package-manager install line and an invocation of Cratekit's own entry point.
# D2 says remediation carries a structured token and only the CLI renders it into
# a command, because the command depends on the platform, the package manager the
# user actually has, and the interface they are sitting in front of. A string
# baked in below the CLI has already decided all three.
#
# Matched anywhere in the constant rather than at its start, because a docstring
# is one constant and a command buried in its middle is the same defect.
_SHELL_COMMAND = re.compile(
    r"\b(?:brew|apt|apt-get|pipx|pip|sudo|port|winget|choco|dnf|yum|npm)\s+install\b"
)

# The entry point followed by a SUBCOMMAND, IN A COMMAND CONTEXT. Three things
# are excluded, and each exclusion has a reason.
#
# Bare flags: ``crate --help`` is the entry point's own identity, and a lower
# layer explaining that it must stay cheap to run is describing itself, not
# prescribing a fix. A remediation always names a subcommand, which is the half
# that belongs to U5's vocabulary and not to any layer below it.
#
# The word "crate" as an ORDINARY NOUN. The rule used to be "crate followed by a
# lowercase word", which matches "the crate registry", "each crate module", and
# "crate state is per install" - correct prose in a correct module. A guard that
# can fail correct code gets worked around rather than obeyed, and being worked
# around is the exact failure D2 itself exists to prevent, so the guard must not
# model that behaviour.
#
# What actually distinguishes the two is CONTEXT, not the following word. A
# command appears quoted as code, after a shell prompt, or after an imperative
# telling the reader to run it. A noun phrase appears after an article, a
# preposition, or nothing at all. So the prefix is required, and it is the
# narrow half of the pair: a lower layer that spells a bare command with no
# context at all is a shape nobody has written, while prose about crates is a
# shape this repository writes constantly.
_CLI_INVOCATION = re.compile(
    r"(?:[`$]\s*|\b(?:run|runs|running|type|typing|invoke|invoking|execute|executing)\s+)"
    r"crate\s+(?!-)[a-z][a-z0-9]*(?:-[a-z0-9]+)*\b"
)


def layer_of(module: str) -> str:
    """Return the layer name for a dotted module path."""
    for pattern, layer in _LAYER_RULES:
        if re.match(pattern, module):
            return layer
    raise AssertionError(
        f"{module!r} matches no layer rule. Every module must be placed in the "
        f"KTD23 ladder explicitly; an unplaced module is an unguarded one."
    )


# ---------------------------------------------------------------------------
# Rule 1: imports point downward only
# ---------------------------------------------------------------------------


def import_direction_violations(source: str, module: str) -> list[str]:
    """Return one message per upward import in ``source``.

    The whole tree is walked, not just the top-level body. That is the entire
    point: both live violations in the source system are function-body imports.
    A header-only check would report the package as clean.
    """
    problems: list[str] = []
    own_rank = RANK[layer_of(module)]
    tree = ast.parse(source)

    for node in ast.walk(tree):
        targets: list[str] = []
        if isinstance(node, ast.Import):
            targets = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                # A relative import cannot cross a layer boundary upward without
                # also being expressible absolutely; resolving it needs package
                # context this pure checker deliberately does not have. The real
                # tree scan below reports absolute paths, so relative imports are
                # covered there by the same rule.
                continue
            if node.module:
                # Expand the imported names into module paths ONLY when the
                # source is a package. In `from cratekit.core import taxonomy`
                # the dependency is on cratekit.core.taxonomy; in
                # `from cratekit.core.config import load` it is on
                # cratekit.core.config, and `load` is a symbol. Treating a symbol
                # as a module makes the checker report imports that do not exist.
                if len(node.module.split(".")) <= _PACKAGE_DEPTH:
                    # Even from a package, an imported name may be a symbol
                    # rather than a submodule. Dunders and CapWords are symbols
                    # by convention, and treating them as modules would place
                    # `from cratekit import __version__` in the wrong layer.
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
    """True when ``node`` sits inside a function or class body.

    Used only to sharpen the message. A lazy import is the shape that hides a
    layering break, so saying so in the failure saves the reader a search.
    """
    for parent in ast.walk(tree):
        if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for child in ast.walk(parent):
                if child is node:
                    return True
    return False


# ---------------------------------------------------------------------------
# Rule 2: a lower layer never NAMES a higher-layer concept
# ---------------------------------------------------------------------------


def higher_concept_violations(source: str, module: str) -> list[str]:
    """Return one message per higher-layer name appearing as a string literal.

    Rule 1 stops an upward import statement. This stops the same thing written as
    data: ``importlib.import_module("cratekit.analysis.vocal")`` is an upward
    dependency that no import checker sees. It also enforces R19's half of the
    rule, that a taxonomy display name is never written into code below the
    modules layer.
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


# ---------------------------------------------------------------------------
# Rule 3: no persisted record is keyed by a display name (R19)
# ---------------------------------------------------------------------------

# Mapping operations whose FIRST argument is a key. A display name reaching any
# of these is a display name being used as an identifier.
_KEY_METHODS = frozenset({"get", "setdefault", "pop", "__getitem__", "__contains__"})


def _names_a_display_name(node: ast.AST) -> bool:
    """True when the expression ends in a display-name attribute access."""
    return isinstance(node, ast.Attribute) and node.attr in {"display_name", "displayName"}


def persisted_display_name_violations(source: str, module: str) -> list[str]:
    """Return one message per record keyed by a display name.

    The detection is structural rather than semantic, and deliberately so. A
    display name is fine to READ, fine to PRINT, and fine to put in a message.
    What it must never be is a KEY. So the rule is exactly: a display name, or a
    known taxonomy display literal, may not appear in a key position. Key
    positions are a dict literal key, a subscript slice, and the first argument
    of a mapping lookup.
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


# ═══════════════════════════════════════════════════════════════════════════
# Fixture tests: each rule bites
# ═══════════════════════════════════════════════════════════════════════════


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
    """The ladder covers the package the plan describes, not just what exists.

    Placing modules before they are written is the point of porting the guards
    first: the layer a file belongs to is decided by the architecture, not by
    whichever directory it happens to land in when somebody is in a hurry.
    """
    assert layer_of(module) == layer


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
    """A deferred import is not a smaller dependency. It is a hidden one.

    This is how the source system's router ends up raising ImportError on a slim
    install: the import is real, it just does not run until a track needs vocal
    routing, so nothing at install time or import time can see it coming.
    """
    source = (
        "def clears_vocal_cut(level):\n"
        "    from cratekit.analysis.vocal_calibrate import load_threshold\n"
        "    return level >= load_threshold()\n"
    )
    problems = import_direction_violations(source, "cratekit.core.routing")
    assert len(problems) == 1
    assert "lazy import inside a function" in problems[0]


def test_a_cycle_masked_by_a_lazy_import_is_a_violation():
    """The second live violation: a shared helper importing a feature module.

    The feature module already depends on the shared layer, so this is a genuine
    cycle. It runs today only because the import is deferred to call time.
    """
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
    """The planted name is taken FROM the registry, now that one exists.

    Until U5 landed, this guard read a hand-kept fallback list and the fixture
    planted a name from it. Hardcoding a name here again would test the fallback
    rather than the rule, and would keep passing after the registry renamed the
    verb, which is the drift the guard was built to read the registry to avoid.
    """
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
    """The shape the guard could not see before: prose, not an import or a verb.

    A hint holding "brew install ffmpeg" is an upward dependency written as
    English. The CLI can no longer choose a platform-appropriate or
    interface-appropriate remediation, because the string was baked in below it.
    """
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
    """A guard that fails a correct module trains people to route around it.

    The rule is about the text a user TYPES at a shell. "crate" followed by a
    lowercase word is a noun phrase far more often than it is a command, and this
    repository writes that noun phrase constantly: a check that cannot tell them
    apart would be muted within a week, which is the same behaviour D2 exists to
    prevent people from having to invent.
    """
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
    """The narrowing must not cost the rule its bite.

    Every shape a remediation actually takes below the CLI is still caught: after
    an imperative, quoted as code, or after a shell prompt.
    """
    problems = higher_concept_violations(source, "cratekit.core.config")
    assert len(problems) == 1 and "invocation of a CLI subcommand" in problems[0]


def test_a_foundation_module_may_name_the_entry_point_by_its_own_flags():
    """The rule is about remediation, not about mentioning the program's name.

    A module explaining that it must stay importable so ``crate --help`` works on
    an unconfigured machine is describing itself. A remediation always names a
    subcommand, and that is the half U5 owns.
    """
    source = '"""Cheap enough that crate --help runs before setup."""\n'
    assert higher_concept_violations(source, "cratekit.core.config") == []


def test_a_command_buried_in_a_docstring_still_fails():
    """A docstring is one string constant, so a check on its first words is not a check."""
    source = '"""Resolve binaries.\n\n    Missing ones need pipx install yt-dlp first.\n    """\n'
    problems = higher_concept_violations(source, "cratekit.core.binaries")
    assert len(problems) == 1 and "pipx install" in problems[0]


def test_prose_about_installing_without_a_command_passes():
    """What correct code looks like, asserted so the guard cannot forbid it.

    The rule is about the text a user TYPES. Naming the fact that something must
    be installed, or that there is nothing to install, is this layer's own
    knowledge and stays.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# The real package
# ═══════════════════════════════════════════════════════════════════════════


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


#: The write-ranked modules that live under ``core/``, and the ONE write-layer
#: module each is ranked that way in order to reach. The exception buys a named
#: import, not a layer's worth of them.
_WRITE_RANKED_CORE_MODULES: dict[str, frozenset[str]] = {
    "cratekit.core.tree_registry": frozenset(),
    "cratekit.core.restore": frozenset(),
}


def test_a_write_ranked_core_module_imports_no_write_layer_module():
    """The exception is narrower than the rank that implements it, so say so here.

    Ranking ``core.restore`` as write is what lets it read the tree registry,
    which is itself a write-ranked module under ``core/``. The rank is a blunt
    instrument: it also grants permission to import every ``cratekit.write.*``
    module, which is a whole layer of licence for one named dependency, and the
    licence is the kind nobody notices being spent. Neither module uses any of it
    today, and this is what keeps that true: adding such an import is a decision
    that has to be made in this file, in a diff, rather than by an editor's
    autocomplete in a module that already compiles.
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
