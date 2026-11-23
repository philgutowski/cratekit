"""Source analysis shared by the guards that hold a LATER unit to what an earlier one settled.

``tests/test_review_queue.py``, ``tests/test_cli_contract.py``,
``tests/test_pool_sizing.py`` and the exit code guards ask these questions,
once, here; two copies of one walk once disagreed about an aliased import.

Every question is answered against the name the source actually BOUND the
module to, in any import shape, never by matching an attribute name: a
reviewer passed a hand edited CSV gate with one unrelated ``.offer(`` call.
And each accepts every import shape the repository allows, since a guard that
fires on correct code gets routed around (P7).
"""

from __future__ import annotations

import ast
import re

_AST = ast.AST


def _children(node: ast.AST) -> list[ast.AST]:
    """``list(ast.iter_child_nodes(node))``, in its order, in one frame (U326)."""
    found: list[ast.AST] = []
    for name in node._fields:
        value = getattr(node, name, None)
        if isinstance(value, _AST):
            found.append(value)
        elif isinstance(value, list):
            found.extend([item for item in value if isinstance(item, _AST)])
    return found


def _walk(node: ast.AST):
    """Every node under ``node``, itself first, in exactly ``ast.walk``'s order (U326).

    The module walked last is held by identity with its walk, since the
    questions a sweep asks of one file come one after another; holding one beat
    holding none or many when measured on 2026-11-22. Sound only while no tree
    is written between two questions about it: nothing here writes one, and a
    caller that edits its own tree must parse the edited text afresh.
    """
    if not isinstance(node, ast.Module):
        return _breadth_first(node)
    if not (_LAST_MODULE_WALK and _LAST_MODULE_WALK[0] is node):
        walked = _breadth_first(node)
        next(walked)
        _LAST_MODULE_WALK[:] = [node, list(walked)]
    return _module_then(node, _LAST_MODULE_WALK[1])


#: The module tree walked last and every node under it, in walk order, or empty.
_LAST_MODULE_WALK: list = []


def _module_then(module: ast.Module, below: list[ast.AST]):
    yield module
    yield from below


def _breadth_first(node: ast.AST):
    """``ast.walk`` over ``node``, its queue a list read by position."""
    todo = [node]
    index = 0
    while index < len(todo):
        node = todo[index]
        index += 1
        todo.extend(_children(node))
        yield node


#: The module every question here is asked about. Its package is DERIVED from
#: this, not a second constant; see the residual
#: "Two copies of one import walk still carry a relative-import defect".
REVIEW_MODULE = "cratekit.core.review"

#: The two constructors that produce a comma separated writer, named once.
CSV_WRITER_NAMES = frozenset({"writer", "DictWriter"})


def _dotted(node: ast.AST) -> str | None:
    """``a.b.c`` as text, or None when the expression is not a plain name chain."""
    parts: list[str] = []
    current: ast.AST = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return ".".join(reversed(parts))
    return None


def _dotted_tail_of(candidate: str, path: str) -> bool:
    """Whether ``candidate`` is a whole dotted tail of ``path``.

    Only the fallback when the caller gives no package: it fires on a file in an
    unrelated package writing ``from .pool import PoolPlan``. See :func:`package_of`.
    """
    if not candidate:
        return False
    wanted = candidate.split(".")
    return path.split(".")[-len(wanted):] == wanted


def _absolute_module(package: str | None, level: int, module: str) -> str | None:
    """The module a relative import names, resolved against the importing package.

    None when there is no package, or the dots climb past the top, which the
    interpreter refuses.
    """
    if level == 0:
        return module or None
    if package is None:
        return None
    parts = package.split(".")
    if level - 1 > len(parts):
        return None
    base = parts[: len(parts) - (level - 1)]
    if not base:
        return None
    return ".".join([*base, module]) if module else ".".join(base)


def package_of(path, source_root) -> str | None:
    """The dotted package a module sits in, or None when it is not inside one."""
    try:
        relative = path.resolve().relative_to(source_root.resolve())
    except ValueError:
        return None
    parts = relative.parts[:-1]
    return ".".join(parts) if parts else None


class ImportsOf:
    """How one source file reaches ONE named module, if it reaches it at all.

    The four shapes the repository's own modules use::

        import cratekit.core.review            # cratekit.core.review.offer(...)
        import cratekit.core.review as rv      # rv.offer(...)
        from cratekit.core import review       # review.offer(...)
        from cratekit.core.review import offer # offer(...)

    An ancestor package reaches the module too (``from cratekit import core``
    then ``core.pool.PoolPlan(...)``), and a relative import, including the bare
    ``from . import pool`` a sibling writes. Parameterized by module (U12 asks
    about ``cratekit.core.pool``) and by the importing file's package, which
    makes the relative half exact; without one it falls back to matching by
    dotted tail, so a caller walking real files should pass it.
    """

    def __init__(self, tree: ast.AST, module: str, package: str | None = None) -> None:
        self.module = module
        self.package = package
        parts = module.split(".")
        #: Every dotted prefix of the module, mapped to the path still to be walked
        #: from it, derived from the module's name. The module maps to the empty string.
        ancestors = {
            ".".join(parts[:size]): ".".join(parts[size:])
            for size in range(1, len(parts) + 1)
        }
        #: Local name -> the path still to be walked from it to reach the module.
        self.paths: dict[str, str] = {}
        #: Local name -> the module attribute it was imported as.
        self.symbols: dict[str, str] = {}

        def remainder(reached: str, *, by_tail: bool) -> str | None:
            """What is left to walk from an imported name, or None if it misses."""
            if reached in ancestors:
                return ancestors[reached]
            if not by_tail:
                return None
            # Longest first, so a tail of two ancestors is credited to the more specific
            # one. Redundant for today's modules; kept for the next module name.
            for path in sorted(ancestors, key=len, reverse=True):
                if _dotted_tail_of(reached, path):
                    return ancestors[path]
            return None

        for node in _walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in ancestors:
                        self.paths[alias.asname or alias.name] = ancestors[alias.name]
            elif isinstance(node, ast.ImportFrom):
                imported = node.module or ""
                by_tail = False
                if node.level:
                    if package is None:
                        # Nothing to resolve against, so fall back to the tail heuristic.
                        by_tail = True
                    else:
                        resolved = _absolute_module(package, node.level, imported)
                        if resolved is None:
                            continue
                        imported = resolved
                if imported == module or (by_tail and _dotted_tail_of(imported, module)):
                    for alias in node.names:
                        self.symbols[alias.asname or alias.name] = alias.name
                    continue
                for alias in node.names:
                    reached = f"{imported}.{alias.name}" if imported else alias.name
                    rest = remainder(reached, by_tail=by_tail)
                    if rest is not None:
                        self.paths[alias.asname or alias.name] = rest
        #: Local names that ARE the module.
        self.module_names: set[str] = {name for name, rest in self.paths.items() if not rest}

    @property
    def reaches(self) -> bool:
        """Whether this source imports the module at all, in any shape."""
        return bool(self.paths or self.symbols)

    def resolves(self, node: ast.AST, wanted: str) -> bool:
        """Whether ``node`` names the module's ``wanted`` attribute, which may itself be dotted."""
        dotted = _dotted(node)
        if dotted is None:
            return False
        for name, rest in self.paths.items():
            reached = f"{name}.{rest}" if rest else name
            if dotted == f"{reached}.{wanted}":
                return True
        head, _, tail = dotted.partition(".")
        symbol = self.symbols.get(head)
        if symbol is None:
            return False
        return (f"{symbol}.{tail}" if tail else symbol) == wanted


class ReviewImports(ImportsOf):
    """:class:`ImportsOf` fixed to the review module, which is what U11 declared.

    ``package`` is forwarded: dropping it raises nothing and makes the guard
    answer about the wrong file, which three tests in ``test_review_queue.py`` drive.
    """

    def __init__(self, tree: ast.AST, package: str | None = None) -> None:
        super().__init__(tree, REVIEW_MODULE, package)

    @property
    def reaches_review(self) -> bool:
        """Whether this source imports the review module at all, in any shape."""
        return self.reaches


def calls_attribute(source: str, module: str, wanted: str, *, package: str | None = None) -> bool:
    """Whether this source CALLS ``module``'s ``wanted`` function, in any import shape.

    ``package`` is the package the source sits in, so a relative import resolves exactly.
    """
    tree = ast.parse(source)
    imports = ImportsOf(tree, module, package)
    if not imports.reaches:
        return False
    return any(
        isinstance(node, ast.Call) and imports.resolves(node.func, wanted)
        for node in _walk(tree)
    )


def _assignments(tree: ast.AST) -> list[tuple[str, ast.AST]]:
    """Every ``name = value`` and ``self.name = value``, as (dotted target, value)."""
    found: list[tuple[str, ast.AST]] = []
    for node in _walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                name = _dotted(target)
                if name is not None:
                    found.append((name, node.value))
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            name = _dotted(node.target)
            if name is not None:
                found.append((name, node.value))
    return found


def calls_review(source: str, wanted: str, package: str | None = None) -> bool:
    """Whether this source CALLS the review module's ``wanted`` function."""
    tree = ast.parse(source)
    imports = ReviewImports(tree, package)
    if not imports.reaches_review:
        return False
    return any(
        isinstance(node, ast.Call) and imports.resolves(node.func, wanted)
        for node in _walk(tree)
    )


def offers_into(source: str, queue: str, package: str | None = None) -> bool:
    """Whether a review ``offer`` call is given the review queue named by ``queue``.

    The queue has to reach the CALL. One hop of indirection is accepted:
    ``QUEUE = review.Queue.VERSION_MATCH`` then ``queue=QUEUE``.
    """
    tree = ast.parse(source)
    imports = ReviewImports(tree, package)
    if not imports.reaches_review:
        return False
    aliases = {
        name
        for name, value in _assignments(tree)
        if imports.resolves(value, queue)
    }
    for node in _walk(tree):
        if not isinstance(node, ast.Call) or not imports.resolves(node.func, "offer"):
            continue
        for keyword in node.keywords:
            if keyword.arg != "queue":
                continue
            if imports.resolves(keyword.value, queue):
                return True
            if _dotted(keyword.value) in aliases:
                return True
    return False


def constructs_review(source: str, wanted: str, package: str | None = None) -> bool:
    """Whether this source CONSTRUCTS the review module's ``wanted`` class."""
    return calls_review(source, wanted, package)


def methods_on_review_construction(
    source: str, wanted: str, package: str | None = None
) -> set[str]:
    """Method names called on something this source built from review's ``wanted``.

    The receiver is traced through a local, a field and a small returning
    helper, so an unrelated class's method of the same name never answers.
    """
    tree = ast.parse(source)
    imports = ReviewImports(tree, package)
    if not imports.reaches_review:
        return set()

    def is_construction(node: ast.AST) -> bool:
        return isinstance(node, ast.Call) and imports.resolves(node.func, wanted)

    factories = {
        function.name
        for function in _walk(tree)
        if isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef))
        for statement in _walk(function)
        if isinstance(statement, ast.Return)
        and statement.value is not None
        and is_construction(statement.value)
    }
    traced = {
        name
        for name, value in _assignments(tree)
        if is_construction(value)
        or (
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Name)
            and value.func.id in factories
        )
    }
    found: set[str] = set()
    for node in _walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        receiver = node.func.value
        if is_construction(receiver) or _dotted(receiver) in traced:
            found.add(node.func.attr)
    return found


def constructs_a_csv_writer(source: str) -> list[str]:
    """Every place this source builds a comma separated WRITER, in any import shape.

    Three narrowings, so the guard cannot fire on correct code (P7): writing
    only, since R12 names a file the product wrote for hand editing and pasted
    intake is legitimate; the module named, not just the attribute; and the name
    the source bound, so ``import csv as spreadsheet`` is caught.
    """
    tree = ast.parse(source)
    module_names = {
        alias.asname or "csv"
        for node in _walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
        if alias.name == "csv"
    }
    imported = {
        alias.asname or alias.name
        for node in _walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "csv"
        for alias in node.names
        if alias.name in CSV_WRITER_NAMES
    }
    found: list[str] = []
    for node in _walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr in CSV_WRITER_NAMES:
            if isinstance(func.value, ast.Name) and func.value.id in module_names:
                found.append(f"line {node.lineno}: {ast.unparse(func)}")
        elif isinstance(func, ast.Name) and func.id in imported:
            found.append(f"line {node.lineno}: {func.id}")
    return found


def package_modules(package_root) -> list[tuple[str, str]]:
    """Every module under one package directory, as (relative name, source), walked (P3)."""
    return [
        (path.name, path.read_text())
        for path in sorted(package_root.rglob("*.py"))
    ]


# ---------------------------------------------------------------------------
# U38: the two shapes that bypass the reserved exit-code table.
#
# Appended, so units landing at once conflict visibly rather than merging
# silently. Answered against the name the source BOUND, never the text
# ``ExitCode``, which anyone's class or one ``as`` would defeat.
# ---------------------------------------------------------------------------

#: The module that owns the status vocabulary. Its package and leaf are derived
#: at use, so a test can move the constant and watch every question follow.
EXIT_CODE_MODULE = "cratekit.core.exit_codes"

#: The class inside that module that IS the vocabulary.
EXIT_CODE_CLASS = "ExitCode"

#: A cause slug as this repository spells one: lowercase words joined by single
#: hyphens. Not a key rule on its own: the string must also be a declared
#: cause, from the registry, the caller's derivation, or an enum member in the
#: same source. See ``ReservedCodeTable``.
CAUSE_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")


def _relative_module(node: ast.ImportFrom, package: str) -> str | None:
    """The absolute module a RELATIVE import names, resolved against its package.

    One dot is the file's own package, for a module and for that package's
    ``__init__`` alike. None when the level walks off the top: Python's slice
    would otherwise quietly hand back a shorter package and report an import the
    interpreter refuses (driven by
    ``test_a_relative_import_that_walks_off_the_top_names_nothing``).
    """
    parts = package.split(".")
    if node.level - 1 >= len(parts):
        return None
    base = parts[: len(parts) - (node.level - 1)]
    return ".".join(base + ([node.module] if node.module else []))


def _import_targets(
    node: ast.ImportFrom, module: str, package: str | None
) -> tuple[bool, bool]:
    """Whether one ``from ... import`` names MODULE, or the package MODULE sits in.

    One implementation for both walks here; see the residual
    "Two copies of one import walk still carry a relative-import defect".
    Resolved against the importer's package when known, so ``from . import
    exit_codes`` in ``cli`` is the table. Without one the TAIL is matched and a
    bare sibling accepted, and ``from . import X`` (module None) names the package.
    """
    owner, _, leaf = module.rpartition(".")
    if not node.level:
        named = node.module or ""
        return named == module, named == owner
    if package is not None:
        absolute = _relative_module(node, package)
        return absolute == module, absolute == owner
    tail = (node.module or "").split(".")
    parent = owner.rsplit(".", 1)[-1]
    names_the_module = tail[-2:] == [parent, leaf] or tail == [leaf]
    names_the_package = node.module is None or tail[-1:] == [parent]
    return names_the_module, names_the_package


class ExitCodeImports:
    """How one source file reaches ``ExitCode``, in every import shape.

    Collapse outstanding: this is the walk :class:`ImportsOf` does, with its own
    relative resolver through ``_import_targets``. Collapse it into
    ``ImportsOf(tree, EXIT_CODE_MODULE, package)`` narrowed to the ``ExitCode``
    symbol, threading the package at every call site. The two resolvers agreed
    on 140 cases at the U12 merge, so it is deduplication, not a fix, and the
    residuals record the plan.

    Seven shapes are recognized::

        import cratekit.core.exit_codes             # ...exit_codes.ExitCode.OK
        import cratekit.core.exit_codes as ec       # ec.ExitCode.OK
        from cratekit.core import exit_codes        # exit_codes.ExitCode.OK
        from cratekit.core.exit_codes import ExitCode        # ExitCode.OK
        from cratekit.core.exit_codes import ExitCode as EC  # EC.OK
        from .exit_codes import ExitCode            # a sibling of the module
        from . import exit_codes                    # the same, module bound

    ``from cratekit.cli import exit_codes`` is deliberately not one: it binds the
    reservation table, and reading it is the sanctioned path.
    """

    def __init__(self, tree: ast.AST, package: str | None = None) -> None:
        #: Local names that ARE the vocabulary module.
        self.module_names: set[str] = set()
        #: Local names that ARE the ``ExitCode`` class itself.
        self.class_names: set[str] = set()
        leaf = EXIT_CODE_MODULE.rpartition(".")[2]
        for node in _walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == EXIT_CODE_MODULE:
                        self.module_names.add(alias.asname or EXIT_CODE_MODULE)
            elif isinstance(node, ast.ImportFrom):
                names_the_module, names_the_package = _import_targets(
                    node, EXIT_CODE_MODULE, package
                )
                if names_the_module:
                    for alias in node.names:
                        if alias.name == EXIT_CODE_CLASS:
                            self.class_names.add(alias.asname or EXIT_CODE_CLASS)
                elif names_the_package:
                    for alias in node.names:
                        if alias.name == leaf:
                            self.module_names.add(alias.asname or leaf)

    def names_the_class(self, node: ast.AST) -> bool:
        """Whether ``node`` names the ``ExitCode`` CLASS this source imported."""
        dotted = _dotted(node)
        if dotted is None:
            return False
        if dotted in self.class_names:
            return True
        # The module-qualified spelling, ``exit_codes.ExitCode(30)``, ordinary Python
        # once called unreachable; see the residual "One check in this unit is unreachable".
        parts = dotted.split(".")
        return (
            len(parts) >= 2
            and ".".join(parts[:-1]) in self.module_names
            and parts[-1] == EXIT_CODE_CLASS
        )

    def names_a_code(self, node: ast.AST) -> bool:
        """Whether ``node`` is a member of the ``ExitCode`` this source imported."""
        dotted = _dotted(node)
        if dotted is None:
            return False
        parts = dotted.split(".")
        if len(parts) >= 2 and ".".join(parts[:-1]) in self.class_names:
            return True
        return (
            len(parts) >= 3
            and ".".join(parts[:-2]) in self.module_names
            and parts[-2] == EXIT_CODE_CLASS
        )


# ``_bound_module_names`` and ``_bound_symbol_names`` were deleted once
# ``ProcessExits`` bound by module identity: dead code claiming a repair misleads.


def _module_level_literals(tree: ast.AST) -> dict[str, ast.AST]:
    """Every ``NAME = <expression>`` at module level, for resolution by name.

    ``PRECONDITION = 30`` beside a table is the careful spelling, and is read.
    """
    found: dict[str, ast.AST] = {}
    for node in getattr(tree, "body", []):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    found[target.id] = node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            if isinstance(node.target, ast.Name):
                found[node.target.id] = node.value
    return found


def _class_level_literals(tree: ast.AST) -> dict[str, dict[str, ast.AST]]:
    """Every ``CLASS.MEMBER = <expression>``, one level deep, by class name."""
    found: dict[str, dict[str, ast.AST]] = {}
    for node in _walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        members: dict[str, ast.AST] = {}
        for statement in node.body:
            if isinstance(statement, ast.Assign):
                for target in statement.targets:
                    if isinstance(target, ast.Name):
                        members[target.id] = statement.value
            elif isinstance(statement, ast.AnnAssign) and statement.value is not None:
                if isinstance(statement.target, ast.Name):
                    members[statement.target.id] = statement.value
        if members:
            found[node.name] = members
    return found


#: The names the ``enum`` module binds that a vocabulary is built on, read only
#: where a base was imported under another name. ``Flag`` and ``IntFlag`` are
#: out: their members are bit values. Only ``StrEnum`` is aliased in the suite.
ENUM_BASES = frozenset({"Enum", "StrEnum", "IntEnum"})


def _enum_bases(tree: ast.AST) -> set[str]:
    """Every local name in this source that IS a base out of the ``enum`` module.

    Bound through the import graph, so ``from enum import StrEnum as Vocabulary``
    is read. Only the symbol import: ``e.StrEnum`` is answered by the spelling
    clause in ``_declared_enum_values``.
    """
    found: set[str] = set()
    for node in _walk(tree):
        if not isinstance(node, ast.ImportFrom) or node.level or node.module != "enum":
            continue
        for alias in node.names:
            if alias.name in ENUM_BASES:
                found.add(alias.asname or alias.name)
    return found


def _declared_enum_values(tree: ast.AST) -> set[str]:
    """Every cause-shaped string this source declares as an enum member value.

    The DECLARATION half of the key test: a string declared in the file's own
    enum is a cause before anybody reserved it. Matched on the base, never on the
    class or variable name, by two clauses each with its own fixture: a base
    bound from ``enum`` under another name, and a base spelled ending in
    ``Enum``, which covers our own bases in other modules.

    Not read: a base from another module whose name is neither, such as
    ``class Cause(Vocabulary)``; that needs the other file.
    ``test_no_module_declares_a_vocabulary_on_a_base_this_cannot_read`` measures
    the tree for it.
    """
    bound = _enum_bases(tree)
    found: set[str] = set()
    for node in _walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        bases = [_dotted(base) or "" for base in node.bases]
        if not any(
            base in bound or base.split(".")[-1].endswith("Enum") for base in bases
        ):
            continue
        for statement in node.body:
            values = []
            if isinstance(statement, ast.Assign):
                values = [statement.value]
            elif isinstance(statement, ast.AnnAssign) and statement.value is not None:
                values = [statement.value]
            for value in values:
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    if CAUSE_SLUG.match(value.value):
                        found.add(value.value)
    return found


#: How far a code is chased through names, members and arithmetic. Bounded so a
#: mutually recursive pair of constants cannot hang the suite.
#:
#: THREE, the depth of the deepest spelling this guard promises to read:
#: ``BASE = 30``, ``OFFSET = BASE``, ``OFFSET + 1``. It is a coverage dial, not
#: a correctness constant: at three it reads at most two aliases before the
#: literal, so this is reported::
#:
#:     A0 = 30
#:     A1 = A0
#:     CODES = {"config-unusable": A1}
#:
#: and a chain of three aliases is SILENT, the cost of the number. Measured: the
#: three alias chain is silent at 2 and 3 and reported from 4.
#: ``test_the_hop_bound_is_a_coverage_dial_and_this_is_what_it_gives_up`` and
#: ``test_the_hop_bound_is_the_depth_of_the_deepest_spelling`` pin both edges; see
#: the residual "One check in this unit is unreachable".
MAX_HOPS = 3


def resolve_int(
    node: ast.AST | None,
    names: dict[str, ast.AST],
    members: dict[str, dict[str, ast.AST]],
    hops: int = 0,
) -> int | None:
    """The integer an expression evaluates to, through names, members and arithmetic.

    Shared by both guards, since a code held in a constant is the careful
    spelling. ``True`` is not an integer here, and a name that resolves to
    nothing resolves to nothing rather than a guess.
    """
    if node is None or hops > MAX_HOPS:
        return None
    if isinstance(node, ast.Constant):
        # THE BOOL EXCLUSION RUNS: ``CORRECT_A_RETRY_FLAG_PER_CAUSE`` reaches it. It
        # changes no outcome today only because the range starts at 10.
        if isinstance(node.value, bool) or not isinstance(node.value, int):
            return None
        return node.value
    if isinstance(node, ast.Name):
        return resolve_int(names.get(node.id), names, members, hops + 1)
    if isinstance(node, ast.Attribute):
        owner = _dotted(node.value) or ""
        return resolve_int(members.get(owner, {}).get(node.attr), names, members, hops + 1)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        # THE ONLY THING THAT READS A NEGATIVE. Without it ``sys.exit(-1)``, which
        # reaches the shell as 255 and the job engine as a signal death, is silent. See
        # the residual
        # "A negative process status is reserved against in prose and was covered by nothing".
        inner = resolve_int(node.operand, names, members, hops + 1)
        return None if inner is None else -inner
    if isinstance(node, ast.BinOp):
        left = resolve_int(node.left, names, members, hops + 1)
        right = resolve_int(node.right, names, members, hops + 1)
        if left is None or right is None:
            return None
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        # ``//`` and ``%`` complete the set. Division by zero is a source that does
        # not run, so it resolves to nothing rather than raising inside a test.
        if isinstance(node.op, (ast.FloorDiv, ast.Mod)) and right != 0:
            return left // right if isinstance(node.op, ast.FloorDiv) else left % right
        return None
    # ``int(30)`` around a plain integer, a live path: ``sys.exit(int(code))``
    # arrives here, and without it the bare status guard goes quiet on a real
    # bypass. The builtin is matched by the text of its name, as five other rules
    # here do; the residual
    # "Six of this unit's own rules recognize a builtin by the text of its name"
    # carries that with the measurement that no package module aliases one.
    if isinstance(node, ast.Call) and _dotted(node.func) == "int" and len(node.args) == 1:
        return resolve_int(node.args[0], names, members, hops + 1)
    return None


def _within_scope(body: list[ast.stmt]):
    """Every node inside a block of statements, without entering a nested scope.

    The rule ``_walk_scope`` applies to one node, shared rather than written twice.
    """
    for statement in body:
        if isinstance(
            statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)
        ):
            continue
        yield statement
        yield from _walk_scope(statement)


#: THERE IS NO PER-LINE OFF SWITCH. The old ``# not-a-reservation: <reason>``
#: silenced a one line ``def`` body, two statements on one line, and all of
#: ``core/cause.py``'s registry from one comment, and was never used: the tree
#: has zero offenders outside the two table owners, even with every kebab
#: literal in the package added to the key set.
#:
#: Ordinary data keyed on a cause slug with an in-range integer is still
#: REPORTED. The answer is a review: the value belongs in the table, or the file
#: joins ``TABLE_OWNERS`` with a reason and the membership assertion updated.
#: ``test_a_comment_cannot_silence_a_reservation`` fails if any escape returns.


class ReservedCodeTable:
    """Reads one source for a second opinion about what a refusal cause exits with.

    ONE KEY SET AND ONE VALUE RULE. Every string anybody in this repository has
    declared to be a refusal cause is a key, and any of them beside a status is
    a reservation: an ``ExitCode`` member in any import spelling, a conversion
    round one, a code held in a name or a class attribute, a module's own
    ``IntEnum`` member, a small piece of arithmetic, or a bare integer inside the
    reserved range. The tiered key set before it was silent on fourteen of the
    sixteen shapes in ``REGISTRY_SLUG_SECOND_TABLES``.

    The trade runs on error costs: a false alarm costs one look and a recorded
    decision, a miss is a module quietly disagreeing with the registry. A bare
    integer is ambiguous, so only one inside the reserved range counts, taken
    from the live table; ``True`` and ``False`` are never a status. An
    ``ExitCode`` member or a conversion round the vocabulary is a code at any
    value. Not narrowed to the integers the enum uses, since a new module
    inventing 33 for an unreserved cause is the case this exists for.

    The key is resolved through names too, as the value is, and every construct
    holding keys in a subtree asks ``cause_keys_within``, so one widening reaches
    all of them.

    THE RESIDUAL LIMIT: a poll interval or a width keyed by a cause slug reads as
    a reservation, and is reported, since matching on variable names is a guard
    a rename defeats. Shapes still silent are recorded in the residual
    "The tiers were bought with a number that does not exist".
    """

    def __init__(
        self,
        tree: ast.AST,
        causes: frozenset[str],
        code_range: tuple[int, int],
        package: str | None = None,
    ) -> None:
        self.tree = tree
        self.low, self.high = code_range
        self.codes = ExitCodeImports(tree, package)
        self.constants = _module_level_literals(tree)
        self.members = _class_level_literals(tree)
        #: Every string somebody declared a refusal cause, plus what THIS source
        #: declares in an enum of its own.
        self.causes = set(causes) | _declared_enum_values(tree)

    def cause_key(self, node: ast.AST | None) -> str | None:
        """The cause slug a key names, or None when nobody declared it a cause.

        Through names, as the value side reads a code::

            CONFIG_UNUSABLE = "config-unusable"
            CODES = {CONFIG_UNUSABLE: 30}

            class Slug:
                CONFIG_UNUSABLE = "config-unusable"
            CODES = {Slug.CONFIG_UNUSABLE: 30}

        A name not resolving to a declared cause answers None, as an undeclared
        literal does, so this widens what is READ, not what is a cause.
        """
        held = self._resolved(node)
        if not (isinstance(held, ast.Constant) and isinstance(held.value, str)):
            return None
        return held.value if held.value in self.causes else None

    def cause_keys_within(self, node: ast.AST) -> list[ast.AST]:
        """Every expression anywhere inside ``node`` that names a declared cause.

        One filter for every construct holding its keys in a subtree, so ``case
        Slug.X``, ``if cause == Slug.X`` and a comprehension over named slugs all read
        a key the same way; with separate filters the ``if`` arm and the
        comprehension once stayed silent where ``match`` reported.
        """
        return [element for element in _walk(node) if self.cause_key(element)]

    def _resolved(self, node: ast.AST | None) -> ast.AST | None:
        """A key expression reduced to what it holds: a name or a class attribute.

        Shares ``_through_names``'s bound, so the chase has one depth for both halves.
        """
        if node is None:
            return None
        if isinstance(node, ast.Attribute):
            owner = _dotted(node.value) or ""
            member = self.members.get(owner, {}).get(node.attr)
            return node if member is None else self._through_names(member)
        return self._through_names(node)

    def _through_names(
        self, node: ast.AST, extra: dict[str, ast.AST] | None = None
    ) -> ast.AST:
        """The expression a NAME ultimately holds, bounded like ``resolve_int``.

        Chasing to an expression, then asking the import walk, reads an imported
        ``ExitCode`` member behind a constant, which ``resolve_int`` alone cannot.
        """
        names = dict(self.constants)
        names.update(extra or {})
        seen = 0
        while isinstance(node, ast.Name) and node.id in names and seen < MAX_HOPS:
            node = names[node.id]
            seen += 1
        return node

    def _as_int(
        self, node: ast.AST | None, extra: dict[str, ast.AST] | None = None
    ) -> int | None:
        """This source's constants, plus whatever locals the caller is inside."""
        names = dict(self.constants)
        names.update(extra or {})
        return resolve_int(node, names, self.members)

    def status(self, node: ast.AST | None, extra: dict[str, ast.AST] | None = None) -> str | None:
        """What this expression reserves as a process status, or None."""
        if node is None:
            return None
        spelled = ast.unparse(node)
        # THROUGH NAMES FIRST: ``CODE = ExitCode.PRECONDITION`` beside
        # ``{"rclone-missing": CODE}``. The reported text keeps both spellings, since
        # which name held it is what a reader chasing the hit needs.
        held = self._through_names(node, extra)
        as_written = spelled if held is node else f"{ast.unparse(held)} as {spelled}"
        if self.codes.names_a_code(held):
            return as_written
        # One argument only: ``ExitCode(30, "the note")`` is a constructor taking a
        # code and a sentence, not a conversion (P7).
        if isinstance(held, ast.Call) and len(held.args) == 1:
            # ``ExitCode(0)``: the constructor spelling of a member, not gated by the
            # range, as ``ExitCode.SUCCESS`` is not. Narrowed to an argument that RESOLVES
            # to an integer, so ``ExitCode(result.code)`` reads a runtime value.
            if self.codes.names_the_class(held.func):
                if self._as_int(held.args[0], extra) is not None:
                    return as_written
            # ``int(ExitCode.X)``: a conversion is a code only when what it wraps is one.
            if _dotted(held.func) == "int" and self.status(held.args[0], extra) is not None:
                return as_written
        # ``getattr(ExitCode, "PRECONDITION")``, the vocabulary reached by a string, as
        # the bare-status guard reads ``getattr(sys, "exit")``. Narrowed to a constant
        # name on the class this source imported.
        if (
            isinstance(held, ast.Call)
            and _dotted(held.func) == "getattr"
            and len(held.args) == 2
            and self.codes.names_the_class(held.args[0])
            and isinstance(held.args[1], ast.Constant)
            and isinstance(held.args[1].value, str)
        ):
            return as_written
        value = self._as_int(node, extra)
        if value is None or not self.low <= value < self.high:
            return None
        spelled = ast.unparse(node)
        return f"status {value}" if spelled == str(value) else f"status {value} as {spelled}"

    def _sequence(self, node: ast.AST) -> list[ast.AST] | None:
        """A literal sequence, through at most one module-level name."""
        if isinstance(node, ast.Name):
            node = self.constants.get(node.id, node)
        if isinstance(node, (ast.Tuple, ast.List)):
            return list(node.elts)
        return None

    def _crossed(self, elements: list[ast.AST]) -> list[tuple[ast.AST, ast.AST, None]]:
        """Cause keys paired with statuses sitting in the SAME construct.

        Reads ``("tagger-art-rejected", 41, "the note")`` and its constructor form,
        U38's own idiom of a tuple of dataclasses. Split rather than multiplied out,
        so a long tuple costs one pass and a mapping of causes to sentences adds nothing.
        """
        keys = [element for element in elements if self.cause_key(element)]
        values = [element for element in elements if self.status(element)]
        return [(key, value, None) for key in keys for value in values]

    def pairs(self) -> list[tuple[ast.AST, ast.AST, str | None]]:
        """Every place a key and a value are bound together, in any shape.

        Each shape below was written as an evasion first.
        """
        found: list[tuple[ast.AST, ast.AST, str | None]] = []
        for node in _walk(self.tree):
            if isinstance(node, ast.Dict):
                # A mapping literal, including inside ``dict(**{...})``,
                # ``MappingProxyType({...})`` and ``CODES.update({...})``. Keys stay bound to
                # THEIR value.
                for key, value in zip(node.keys, node.values):
                    if key is not None:
                        found.append((key, value, None))
                # A RECORD written as a mapping::
                #
                #     [{"cause": "config-unusable", "code": 30}, ...]
                #
                # The slug and code sit in the VALUES, never the keys, which are field names.
                found.extend(self._crossed(list(node.values)))
            elif isinstance(node, (ast.Tuple, ast.List)):
                found.extend(self._crossed(list(node.elts)))
            elif isinstance(node, ast.DictComp):
                # ``{slug: 30 for slug in (...)}``: every slug in the iterables is a key the
                # code is given to, read through ``cause_keys_within``.
                for generator in node.generators:
                    for element in self.cause_keys_within(generator.iter):
                        found.append((element, node.value, None))
            elif isinstance(node, ast.Assign):
                # ``CODES[slug] = 30`` after ``CODES = {}``, a table built a line at a time.
                for target in node.targets:
                    if isinstance(target, ast.Subscript):
                        found.append((target.slice, node.value, None))
            elif isinstance(node, ast.Call):
                function = node.func
                if (
                    isinstance(function, ast.Attribute)
                    and function.attr == "setdefault"
                    and len(node.args) == 2
                ):
                    # Redundant with the catch-all below, but binds the key to ITS value by
                    # position, so a three-argument call cannot pair the wrong two. See the
                    # residual "One check in this unit is unreachable".
                    found.append((node.args[0], node.args[1], None))
                elif _dotted(function) in {"dict", "OrderedDict"} and len(node.args) == 1:
                    found.extend(self._zipped(node.args[0]))
                else:
                    # Any other call: a reservation built by a constructor is one. Argument order
                    # is not assumed.
                    arguments = list(node.args) + [keyword.value for keyword in node.keywords]
                    found.extend(self._crossed(arguments))
        found.extend(self._branches())
        return found

    def _zipped(self, argument: ast.AST) -> list[tuple[ast.AST, ast.AST, None]]:
        """``dict(zip(slugs, codes))``, with either sequence named once."""
        if not (isinstance(argument, ast.Call) and _dotted(argument.func) == "zip"):
            return []
        if len(argument.args) != 2:
            return []
        keys = self._sequence(argument.args[0])
        values = self._sequence(argument.args[1])
        if keys is None or values is None:
            return []
        return [(key, value, None) for key, value in zip(keys, values)]

    def _branches(self) -> list[tuple[ast.AST, ast.AST, str | None]]:
        """A table written as control flow: a match statement or an if chain.

        Narrowed to what the branch RETURNS, resolved through the branch's own
        locals, so ``code = 41`` then ``return code`` reads as ``return 41``. Both
        arms ask ``cause_keys_within``.
        """
        found: list[tuple[ast.AST, ast.AST, str | None]] = []
        for node in _walk(self.tree):
            if isinstance(node, ast.Match):
                for case in node.cases:
                    found.extend(
                        self._returned(self.cause_keys_within(case.pattern), case.body)
                    )
            elif isinstance(node, ast.If):
                found.extend(
                    self._returned(self.cause_keys_within(node.test), node.body)
                )
        return found

    def _returned(
        self, keys: list[ast.AST], body: list[ast.stmt]
    ) -> list[tuple[ast.AST, ast.AST, str | None]]:
        """What a branch returns at ANY depth, not entering a nested def, class or lambda."""
        within = list(_within_scope(body))
        locals_here: dict[str, ast.AST] = {}
        for node in within:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        locals_here[target.id] = node.value
        returned = [
            (node.value, self.status(node.value, locals_here))
            for node in within
            if isinstance(node, ast.Return) and node.value is not None
        ]
        return [
            (key, value, label)
            for key in keys
            for value, label in returned
            if label is not None
        ]


def reserved_code_tables(
    source: str,
    causes: frozenset[str],
    code_range: tuple[int, int],
    package: str | None = None,
) -> list[str]:
    """Every place this source gives a refusal cause its own exit code.

    Not restricted to dict literals or two-element pairs: the protected file
    declares its own table as a tuple of three-field dataclasses. ``package``
    lets a relative import resolve exactly; without it ``ExitCodeImports`` falls
    back. There is no second key set parameter, because a defaulted parameter
    that weakens the guard when omitted makes the absence-asserting scans greener.
    """
    tree = ast.parse(source)
    table = ReservedCodeTable(tree, causes, code_range, package)
    return _reservations(table)


def reserved_code_tables_in(
    tree: ast.AST,
    causes: frozenset[str],
    code_range: tuple[int, int],
    package: str | None = None,
) -> list[str]:
    """:func:`reserved_code_tables` asked of a tree already parsed (U258), read and never written.

    It lets a test share one tree among its questions, since the text must reach
    nothing here but ``ast.parse``.
    """
    return _reservations(ReservedCodeTable(tree, causes, code_range, package))


def _reservations(table: ReservedCodeTable) -> list[str]:
    """Every reservation one table reads, one line per (line, slug, status)."""
    found: list[str] = []
    # ONE HIT PER (LINE, SLUG, STATUS): a duplicate key reaches the walk as two
    # identical pairs, and a doubled hit would make the failure's count wrong.
    seen: set[tuple[int, str, str]] = set()
    for key, value, label in table.pairs():
        slug = table.cause_key(key)
        if slug is None:
            continue
        # A branch return carries its label already; its locals are out of scope here.
        status = label if label is not None else table.status(value)
        if status is None:
            continue
        entry = (key.lineno, slug, status)
        if entry in seen:
            continue
        seen.add(entry)
        found.append(f"line {key.lineno}: {slug!r} -> {status}")
    return sorted(found)


# ---------------------------------------------------------------------------
# Ending the process with a bare integer.
# ---------------------------------------------------------------------------

#: The standard-library modules that can end a process, and the attribute of
#: each that does it, held by module IDENTITY.
EXIT_ATTRIBUTES = {"sys": "exit", "os": "_exit"}

#: Modules recognized by identity for any purpose here.
TRACKED_MODULES = frozenset({"sys", "os", "builtins", "importlib"})


def _walk_scope(node: ast.AST):
    """Every node in ONE lexical scope, not entering a nested def, class or lambda.

    A module-level ``stop = sys.exit`` is an exit in functions that inherit it,
    not in one with a parameter of the same name.
    """
    stack = list(_children(node))
    while stack:
        current = stack.pop()
        yield current
        if isinstance(
            current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)
        ):
            continue
        stack.extend(_children(current))


def _parameter_names(node: ast.AST) -> set[str]:
    arguments = getattr(node, "args", None)
    if not isinstance(arguments, ast.arguments):
        return set()
    every = (
        list(arguments.posonlyargs)
        + list(arguments.args)
        + list(arguments.kwonlyargs)
        + [argument for argument in (arguments.vararg, arguments.kwarg) if argument]
    )
    return {argument.arg for argument in every}


class ProcessExits:
    """Every way one lexical scope can reach the call that ends the process.

    Bound by module IDENTITY, never by the text of a name::

        import sys; sys.exit(30)
        import sys as system; system.exit(30)
        system = sys; system.exit(30)          # rebound, not imported
        from sys import exit; exit(30)
        from os import _exit; _exit(30)
        stop = sys.exit; stop(30)
        getattr(sys, "exit")(30)               # inline or held in a name
        importlib.import_module("sys").exit(30)
        os.sys.exit(30)
        raise SystemExit(30)
        raise builtins.SystemExit(30)
        Stop = SystemExit; raise Stop(30)
        class Refused(SystemExit): ...; raise Refused(30)

    ``getattr`` matters most: it disarms a name-based guard on its own. Resolved
    to a fixed point, so aliases settle in any order.
    """

    def __init__(
        self,
        node: ast.AST,
        *,
        inherited: ProcessExits | None = None,
        shadowed: set[str] | None = None,
    ) -> None:
        if inherited is None:
            self.modules: dict[str, str] = {}
            self.exits: set[str] = set()
            self.statuses: set[str] = {"SystemExit"}
            self.importers: set[str] = {"__import__"}
        else:
            self.modules = dict(inherited.modules)
            self.exits = set(inherited.exits)
            self.statuses = set(inherited.statuses)
            self.importers = set(inherited.importers)
        for name in shadowed or ():
            self.modules.pop(name, None)
            self.exits.discard(name)
            self.statuses.discard(name)
            self.importers.discard(name)
        self._bind(node)

    def extended(self, node: ast.AST) -> ProcessExits:
        """This scope's bindings, plus the ones a nested scope makes for itself."""
        return ProcessExits(node, inherited=self, shadowed=_parameter_names(node))

    # ── Binding: what this scope's imports and assignments name ─────────

    def _bind(self, node: ast.AST) -> None:
        classes: list[ast.ClassDef] = []
        assignments: list[tuple[str, ast.AST]] = []
        for child in _walk_scope(node):
            if isinstance(child, ast.Import):
                for alias in child.names:
                    if alias.name in TRACKED_MODULES:
                        self.modules[alias.asname or alias.name] = alias.name
            elif isinstance(child, ast.ImportFrom) and not child.level:
                self._bind_symbols(child)
            elif isinstance(child, ast.ClassDef):
                classes.append(child)
            elif isinstance(child, ast.Assign):
                for target in child.targets:
                    if isinstance(target, ast.Name):
                        assignments.append((target.id, child.value))
            elif isinstance(child, ast.AnnAssign) and child.value is not None:
                if isinstance(child.target, ast.Name):
                    assignments.append((child.target.id, child.value))
        changed = True
        while changed:
            changed = False
            for name, value in assignments:
                if self._is_exit(value) and name not in self.exits:
                    self.exits.add(name)
                    changed = True
                elif self._is_status(value) and name not in self.statuses:
                    self.statuses.add(name)
                    changed = True
                else:
                    identity = self.module_identity(value)
                    if identity and self.modules.get(name) != identity:
                        self.modules[name] = identity
                        changed = True
                    elif (
                        isinstance(value, ast.Attribute)
                        and value.attr == "import_module"
                        and self.module_identity(value.value) == "importlib"
                        and name not in self.importers
                    ):
                        self.importers.add(name)
                        changed = True
            for definition in classes:
                if definition.name in self.statuses:
                    continue
                if any(self._is_status(base) for base in definition.bases):
                    self.statuses.add(definition.name)
                    changed = True

    def _bind_symbols(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        for alias in node.names:
            bound = alias.asname or alias.name
            if module in EXIT_ATTRIBUTES and alias.name == EXIT_ATTRIBUTES[module]:
                self.exits.add(bound)
            elif module == "builtins" and alias.name == "SystemExit":
                self.statuses.add(bound)
            elif module == "builtins" and alias.name == "__import__":
                self.importers.add(bound)
            elif module == "importlib" and alias.name == "import_module":
                self.importers.add(bound)
            elif module in TRACKED_MODULES and alias.name in TRACKED_MODULES:
                self.modules[bound] = alias.name

    # ── Resolution: what an expression IS, whatever it was called ───────

    def module_identity(self, node: ast.AST | None) -> str | None:
        """Which tracked module this expression IS, whatever it was called."""
        if isinstance(node, ast.Name):
            return self.modules.get(node.id)
        if isinstance(node, ast.Attribute):
            # ``os.sys`` is the one attribute chain that names another module.
            if self.module_identity(node.value) == "os" and node.attr == "sys":
                return "sys"
            return None
        if isinstance(node, ast.Call):
            return self._imported_module(node)
        return None

    def _imported_module(self, node: ast.Call) -> str | None:
        if not node.args:
            return None
        named = node.args[0]
        if not (isinstance(named, ast.Constant) and isinstance(named.value, str)):
            return None
        function = node.func
        imports_by_name = (
            isinstance(function, ast.Name) and function.id in self.importers
        ) or (
            isinstance(function, ast.Attribute)
            and function.attr == "import_module"
            and self.module_identity(function.value) == "importlib"
        )
        if imports_by_name and named.value in TRACKED_MODULES:
            return named.value
        return None

    def _fetched(self, node: ast.Call) -> tuple[str | None, str | None]:
        """``getattr(<module>, "name")`` as (module identity, attribute)."""
        if not (isinstance(node.func, ast.Name) and node.func.id == "getattr"):
            return None, None
        if len(node.args) < 2:
            return None, None
        attribute = node.args[1]
        if not (isinstance(attribute, ast.Constant) and isinstance(attribute.value, str)):
            return None, None
        return self.module_identity(node.args[0]), attribute.value

    def _is_exit(self, node: ast.AST) -> bool:
        """Whether this expression IS the callable that ends the process."""
        if isinstance(node, ast.Name):
            return node.id in self.exits
        if isinstance(node, ast.Attribute):
            identity = self.module_identity(node.value)
            return bool(
                identity in EXIT_ATTRIBUTES and node.attr == EXIT_ATTRIBUTES[identity]
            )
            # A dotted lookup here was dead code: every name in ``self.exits`` is bare.
            # ``self.stop = sys.exit`` then ``self.stop(30)`` is NOT handled, since binding
            # across methods leaks across scopes; no package module holds an exit on an
            # attribute.
        if isinstance(node, ast.Call):
            identity, attribute = self._fetched(node)
            return bool(
                identity in EXIT_ATTRIBUTES and attribute == EXIT_ATTRIBUTES[identity]
            )
        return False

    def _is_status(self, node: ast.AST) -> bool:
        """Whether this expression IS the exception whose argument is a status."""
        if isinstance(node, ast.Name):
            return node.id in self.statuses
        if isinstance(node, ast.Attribute):
            # No dotted lookup: nothing puts a dotted name in ``self.statuses``.
            return (
                self.module_identity(node.value) == "builtins"
                and node.attr == "SystemExit"
            )
        if isinstance(node, ast.Call):
            identity, attribute = self._fetched(node)
            return identity == "builtins" and attribute == "SystemExit"
        return False

    def ends_the_process(self, node: ast.AST) -> bool:
        return self._is_exit(node) or self._is_status(node)


def process_status_literals(source: str) -> list[str]:
    """Every place this source turns a bare integer into a process status.

    ``sys.exit(21)`` bypasses the vocabulary. Every name is bound through the
    import graph by module identity, so ``runner.exit(21)`` on someone's own
    object is not caught. The status is RESOLVED, through the scope it is read
    in, so ``sys.exit(PRECONDITION)`` is caught and a shadowing parameter
    resolves to nothing. Zero and ``True`` are excluded; a status this cannot
    evaluate, like ``sys.exit(int(code_for(cause)))``, stays silent.

    A NEGATIVE STATUS IS REPORTED: the shell reads ``exit(-1)`` as 255 and the
    job engine's ``returncode`` as a signal death.
    ``test_a_negative_status_is_a_bare_status_too`` drives it.
    """
    tree = ast.parse(source)
    found: list[str] = []
    _scan_for_exits(
        tree,
        ProcessExits(tree),
        _module_level_literals(tree),
        _class_level_literals(tree),
        found,
    )
    return sorted(found, key=lambda entry: (int(entry.split()[1].rstrip(":")), entry))


def _scope_literals(node: ast.AST, inherited: dict[str, ast.AST]) -> dict[str, ast.AST]:
    """The constants readable inside one scope: what it inherits, minus what it shadows."""
    names = dict(inherited)
    for parameter in _parameter_names(node):
        names.pop(parameter, None)
    for child in _walk_scope(node):
        if isinstance(child, ast.Assign):
            for target in child.targets:
                if isinstance(target, ast.Name):
                    names[target.id] = child.value
        elif isinstance(child, ast.AnnAssign) and child.value is not None:
            if isinstance(child.target, ast.Name):
                names[child.target.id] = child.value
    return names


def _scan_for_exits(
    node: ast.AST,
    exits: ProcessExits,
    names: dict[str, ast.AST],
    members: dict[str, dict[str, ast.AST]],
    found: list[str],
) -> None:
    nested: list[ast.AST] = []
    for child in _walk_scope(node):
        if isinstance(
            child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)
        ):
            nested.append(child)
            continue
        if not isinstance(child, ast.Call) or len(child.args) != 1:
            continue
        status = resolve_int(child.args[0], names, members)
        if status is None or status == 0:
            continue
        if exits.ends_the_process(child.func):
            spelled = ast.unparse(child)
            suffix = "" if str(status) in spelled else f" (status {status})"
            found.append(f"line {child.lineno}: {spelled}{suffix}")
    for scope in nested:
        _scan_for_exits(
            scope, exits.extended(scope), _scope_literals(scope, names), members, found
        )
# ═══════════════════════════════════════════════════════════════════════════
# The soft-delete marker: read it, never default it (appended, per this file)
# ═══════════════════════════════════════════════════════════════════════════

#: The module that owns the binding's vocabulary, and its constant naming the
#: soft-delete column, resolved through the import graph, so
#: ``rb_writer.SOFT_DELETE_COLUMN`` names the column without the literal.
RB_WRITER_MODULE = "cratekit.core.rb_writer"
RB_WRITER_PACKAGE = "cratekit.core"
SOFT_DELETE_CONSTANT = "SOFT_DELETE_COLUMN"

#: The column itself: the literal is still legal and is what the defect looked like.
SOFT_DELETE_COLUMN_LITERAL = "rb_local_deleted"


def _writer_imports(nodes) -> tuple[set[str], set[str]]:
    """The names these import nodes bind to the writer module, and to its constant.

    ``import cratekit.core.rb_writer [as w]``, ``from cratekit.core import
    rb_writer [as w]``, the relative ``from .core import rb_writer`` and ``from .
    import rb_writer`` (inside ``core``), and ``from ...rb_writer import
    SOFT_DELETE_COLUMN``.
    """
    module_names: set[str] = set()
    constant_names: set[str] = set()
    for node in nodes:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == RB_WRITER_MODULE:
                    module_names.add(alias.asname or RB_WRITER_MODULE)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names_the_module = module == RB_WRITER_MODULE or (
                node.level > 0 and module.split(".")[-2:] == ["core", "rb_writer"]
            )
            names_the_package = module == RB_WRITER_PACKAGE or (
                node.level > 0 and (module == "" or module.split(".")[-1:] == ["core"])
            )
            if names_the_module:
                for alias in node.names:
                    if alias.name == SOFT_DELETE_CONSTANT:
                        constant_names.add(alias.asname or alias.name)
            elif names_the_package:
                for alias in node.names:
                    if alias.name == "rb_writer":
                        module_names.add(alias.asname or "rb_writer")
    return module_names, constant_names


def _writer_accessors(tree: ast.AST) -> set[str]:
    """Functions that import the writer and return the name they bound it to.

    Keyed on what makes a function the writer: its imports bind it and a return
    hands back that name, plain or dotted, at any depth.
    """
    found: set[str] = set()
    for node in _walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        bound, _ = _writer_imports(_walk(node))
        if any(
            isinstance(inner, ast.Return)
            and inner.value is not None
            and _dotted(inner.value) in bound
            for inner in _walk(node)
        ):
            found.add(node.name)
    return found


class SoftDeleteNames:
    """Every expression in one source file that NAMES the soft-delete column.

    * the literal ``"rb_local_deleted"``, what the defect looked like;
    * ``rb_writer.SOFT_DELETE_COLUMN`` through any import shape;
    * ``_writer().SOFT_DELETE_COLUMN``, the accessor the U300 parts read through;
    * a local constant assigned any of those, one hop;
    * a local constant assigned a FALSEY constant.

    One hop, the depth :func:`offers_into` accepts: the shape a person reaches
    for around a guard is one name.
    """

    def __init__(self, tree: ast.AST) -> None:
        #: Local names that ARE the rb_writer module, and names bound to the constant.
        self.module_names, self.constant_names = _writer_imports(_walk(tree))
        #: Functions that import the writer and return it, the U300 parts' call time
        #: accessor, so ``_writer().SOFT_DELETE_COLUMN`` names the column.
        self.accessor_names: set[str] = _writer_accessors(tree)

        # The one hop, resolved after the imports and to a fixed point, so file order
        # does not decide it.
        # Local names bound to something FALSEY: a permissive default with a name.
        self.falsey_names: set[str] = set()
        # The one hop and the module alias chain, to a fixed point, so ``M = W`` where
        # ``W`` is itself an alias resolves.
        # Local names that ARE the rb_writer module.
        pairs = _assignments(tree)
        for _ in range(len(pairs) + 1):
            grew = False
            for name, value in pairs:
                if name not in self.constant_names and self._is_column(value):
                    self.constant_names.add(name)
                    grew = True
                if name not in self.falsey_names and self._is_falsey(value):
                    self.falsey_names.add(name)
                    grew = True
                dotted = _dotted(value)
                is_module = dotted in self.module_names or self._calls_accessor(value)
                if is_module and name not in self.module_names:
                    self.module_names.add(name)
                    grew = True
            if not grew:
                break

        #: Names bound at MODULE level: a ``.get`` on one is a lookup table, not a row,
        #: as ``COLUMN_TYPES.get(SOFT_DELETE_COLUMN)`` in the house style.
        self.lookup_tables: set[str] = set()
        for node in getattr(tree, "body", []):
            targets: list[ast.AST] = []
            value: ast.AST | None = None
            if isinstance(node, ast.Assign):
                targets, value = list(node.targets), node.value
            elif isinstance(node, ast.AnnAssign) and node.value is not None:
                targets, value = [node.target], node.value
            if value is None or not _is_container(value):
                continue
            for target in targets:
                name = _dotted(target)
                if name is not None:
                    self.lookup_tables.add(name)

        #: ``.get`` calls whose receiver is SHADOWED by a local of the same name, so a
        #: module-level ``row = {}`` cannot excuse a ``row`` parameter.
        self.shadowed_gets: set[ast.AST] = set()
        for scope in _scopes(tree):
            if scope is tree:
                continue
            local = _local_names(scope)
            if not local:
                continue
            for node in _own_nodes(scope):
                if not isinstance(node, ast.Call):
                    continue
                if not isinstance(node.func, ast.Attribute) or node.func.attr != "get":
                    continue
                receiver = _dotted(node.func.value)
                if receiver is not None and receiver.split(".")[0] in local:
                    self.shadowed_gets.add(node)

    def _calls_accessor(self, node: ast.AST) -> bool:
        """Whether ``node`` is ``_writer()``, a call of the writer's accessor."""
        return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in self.accessor_names
        )

    def _is_column(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Constant) and node.value == SOFT_DELETE_COLUMN_LITERAL:
            return True
        if (
            isinstance(node, ast.Attribute)
            and node.attr == SOFT_DELETE_CONSTANT
            and self._calls_accessor(node.value)
        ):
            return True
        dotted = _dotted(node)
        if dotted is None:
            return False
        if dotted in self.constant_names:
            return True
        return any(
            dotted == f"{module_name}.{SOFT_DELETE_CONSTANT}"
            for module_name in self.module_names
        )

    def _is_falsey(self, node: ast.AST) -> bool:
        """Whether this expression evaluates to something that reads as 'active'.

        Constant-folded, since ``int()``, ``1 - 1`` and ``""`` are zero too.
        """
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            # A zero-argument builtin constructor is that type's empty value, falsey.
            if not node.args and not node.keywords:
                if node.func.id in {"int", "bool", "float", "str", "list", "dict",
                                    "set", "tuple", "bytes", "frozenset"}:
                    return True
        if isinstance(node, ast.BinOp) and isinstance(
            node.op, (ast.Add, ast.Sub, ast.Mult)
        ):
            # ``literal_eval`` refuses ``1 - 1``, so arithmetic on two numbers is folded
            # here, shallowly.
            left, right = node.left, node.right
            if isinstance(left, ast.Constant) and isinstance(right, ast.Constant):
                if isinstance(left.value, (int, float)) and isinstance(
                    right.value, (int, float)
                ):
                    if isinstance(node.op, ast.Add):
                        return not (left.value + right.value)
                    if isinstance(node.op, ast.Sub):
                        return not (left.value - right.value)
                    return not (left.value * right.value)
        try:
            return not ast.literal_eval(node)
        except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
            pass
        dotted = _dotted(node)
        return dotted is not None and dotted in self.falsey_names

    def names_the_column(self, node: ast.AST) -> bool:
        """Whether ``node`` evaluates to the soft-delete column's name."""
        return self._is_column(node)

    def is_permissive(self, node: ast.AST) -> bool:
        """Whether ``node`` is a default that reads as 'this row is active'.

        Falsey is the whole test, since the marker is consumed as a truth value. A
        sentinel is truthy and not flagged: uncompared, it reports rows DELETED,
        which fails loudly.
        """
        return self._is_falsey(node)


def _soft_delete_reads(
    tree: ast.AST, names: SoftDeleteNames
) -> list[tuple[ast.AST, ast.AST | None]]:
    """Every read of the marker, paired with the default it supplied, if any.

    Three access shapes, since a row arrives as a binding object and as a raw
    query mapping. A ``.get`` on a receiver bound at module level TO A CONTAINER
    LITERAL is a per-column table and excluded; keyed on the name alone,
    ``row = fetch_one()`` would excuse every ``row.get(COL, 0)``.
    """
    found: list[tuple[ast.AST, ast.AST | None]] = []
    for node in _walk(tree):
        if isinstance(node, ast.Attribute) and node.attr == SOFT_DELETE_COLUMN_LITERAL:
            # ``row.rb_local_deleted``: no default, so never permissive, recorded for the
            # reader pin. LOAD context only: ``self.rb_local_deleted = deleted`` in a test
            # double defines the attribute, and counting it would make the pin fire on the
            # next fixture. A read is a Load by construction.
            if not isinstance(node.ctx, ast.Load):
                continue
            found.append((node, None))
            continue
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id == "hasattr":
            # A presence test supplies no default; recognized as the ternary route's
            # condition and as a module in this conversation.
            if len(node.args) >= 2 and names.names_the_column(node.args[1]):
                found.append((node, None))
            continue
        if isinstance(func, ast.Name) and func.id == "getattr":
            if len(node.args) >= 2 and names.names_the_column(node.args[1]):
                found.append((node, node.args[2] if len(node.args) > 2 else None))
                continue
            # ``getattr(row, *pair)``: the pair is resolved one hop.
            for argument in node.args:
                if not isinstance(argument, ast.Starred):
                    continue
                packed = _packed_pair(argument.value, tree)
                if packed is not None and names.names_the_column(packed[0]):
                    found.append((node, packed[1] if len(packed) > 1 else None))
        elif isinstance(func, ast.Attribute) and func.attr == "get" and node.args:
            if not names.names_the_column(node.args[0]):
                continue
            receiver = _dotted(func.value)
            if receiver is not None and receiver in names.lookup_tables:
                if node not in names.shadowed_gets:
                    continue
            # A one-argument ``.get`` defaults to None by omission, reported with a
            # synthetic None default.
            default = node.args[1] if len(node.args) > 1 else ast.Constant(value=None)
            found.append((node, default))
    return found


def _local_names(scope: ast.AST) -> set[str]:
    """Names this scope binds itself: parameters, assignments, and walrus targets.

    Every binding form, walked rather than matched: with only bare ``Name``
    targets, this was silent (measured 2026-09-10)::

        TABLE = {}                       # a real per-column lookup table
        def read(rows):
            TABLE, meta = rows[0]        # ... shadowed by a real row
            return TABLE.get(COLUMN, 0)  # ... and the read was excused
    """

    def bind(target: ast.AST | None) -> None:
        """Every name a binding target introduces, through any nesting of it."""
        if target is None:
            return
        for node in _walk(target):
            if isinstance(node, ast.Name):
                found.add(node.id)

    found: set[str] = set()
    arguments = getattr(scope, "args", None)
    if arguments is not None:
        for group in ("posonlyargs", "args", "kwonlyargs"):
            found.update(item.arg for item in getattr(arguments, group, []) or [])
        for single in (getattr(arguments, "vararg", None), getattr(arguments, "kwarg", None)):
            if single is not None:
                found.add(single.arg)
    for node in _own_nodes(scope):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                bind(target)
        elif isinstance(node, (ast.AnnAssign, ast.NamedExpr)):
            bind(node.target)
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            bind(node.target)
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                bind(item.optional_vars)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            found.add(node.name)
        elif isinstance(node, (ast.comprehension,)):
            bind(node.target)
    return found


def _is_container(node: ast.AST) -> bool:
    """Whether this expression builds a mapping or a set: a per-column table.

    Narrow on purpose: any other call could return a row.
    """
    if isinstance(node, (ast.Dict, ast.Set, ast.DictComp, ast.SetComp)):
        return True
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        # ``MappingProxyType({...})`` is how this package freezes a table, always by
        # the bare imported name.
        return node.func.id in {"dict", "set", "frozenset", "MappingProxyType"}
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        return node.func.attr in {"MappingProxyType"}
    return False


def _packed_pair(node: ast.AST, tree: ast.AST) -> list[ast.AST] | None:
    """The elements of a tuple or list, directly or through one named binding."""
    if isinstance(node, (ast.Tuple, ast.List)):
        return list(node.elts)
    dotted = _dotted(node)
    if dotted is None:
        return None
    for name, value in _assignments(tree):
        if name == dotted and isinstance(value, (ast.Tuple, ast.List)):
            return list(value.elts)
    return None


#: Node types that OPEN A NEW SCOPE, where walking must stop.
_SCOPE_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)


def _own_nodes(scope: ast.AST):
    """Every node belonging to THIS scope, never descending into a nested one.

    ``ast.walk`` descends into every function, so "module scope" meant the whole
    file and an unrelated helper's ``marker`` counter fired the guard.
    """
    for child in _children(scope):
        if isinstance(child, _SCOPE_NODES):
            continue
        yield child
        yield from _own_nodes(child)


def _scopes(tree: ast.AST):
    """Each function body, plus the module's own top level, as separate scopes."""
    yield tree
    for node in _walk(tree):
        # ClassDef is here because ``_own_nodes`` stops at one; without it no scope
        # walks a class body.
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            yield node


def _laundered_reads(tree: ast.AST, names: SoftDeleteNames) -> list[ast.AST]:
    """Reads that are correct at the call and made permissive one line later.

    Three routes, one question to an analyzer::

        marker = getattr(row, COL, _ABSENT)     # correct so far
        if marker is _ABSENT:
            marker = 0                          # and now it is not

        try:                                    # the shape a person reaches for
            marker = row.rb_local_deleted
        except AttributeError:
            marker = 0

        marker = row.rb_local_deleted if hasattr(row, COL) else 0
    """
    found: list[ast.AST] = []
    for scope in _scopes(tree):
        holders: dict[str, ast.AST] = {}
        for statement in _own_nodes(scope):
            targets: list[ast.AST] = []
            value: ast.AST | None = None
            if isinstance(statement, ast.Assign):
                targets, value = list(statement.targets), statement.value
            elif isinstance(statement, ast.AnnAssign) and statement.value is not None:
                targets, value = [statement.target], statement.value
            if value is None:
                continue
            reads = _soft_delete_reads(value, names)
            # A PRESENCE TEST IS NOT A HOLDER: ``present = hasattr(row, COL)`` is a flag
            # about the column, so ``present = False`` later is not a launder.
            if all(_is_presence_test(node) for node, _ in reads):
                continue
            for target in targets:
                name = _dotted(target)
                if name is not None:
                    holders[name] = statement

        if not holders:
            continue
        for statement in _rebinding_statements(scope, holders):
            name = _dotted(statement.targets[0])
            if name in holders and names.is_permissive(statement.value):
                found.append(statement)

    for node in _walk(tree):
        if not isinstance(node, ast.IfExp):
            continue
        for kept, other in ((node.body, node.orelse), (node.orelse, node.body)):
            # THE KEPT BRANCH MUST BE THE READ, not merely contain it, so
            # ``row.rb_local_deleted if row else False`` is caught and a formatted string
            # quoting the value is not.
            if not any(read is kept for read, _ in _soft_delete_reads(kept, names)):
                continue
            if names.is_permissive(other):
                found.append(node)
                break
    return found


def _is_presence_test(node: ast.AST) -> bool:
    """Whether this read asks IF the column is there rather than what it says."""
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "hasattr"
    )


def _rebinding_statements(scope: ast.AST, holders: dict[str, ast.AST]):
    """Assignments that rebind a holder, including through ``nonlocal`` and ``global``.

    The walk follows the declaration rather than the indentation, as Python does.
    """
    for statement in _own_nodes(scope):
        if isinstance(statement, ast.Assign) and len(statement.targets) == 1:
            yield statement
    for node in _walk(scope):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        declared: set[str] = set()
        for inner in _walk(node):
            if isinstance(inner, (ast.Nonlocal, ast.Global)):
                declared.update(inner.names)
        if not declared & set(holders):
            continue
        for inner in _walk(node):
            if isinstance(inner, ast.Assign) and len(inner.targets) == 1:
                if _dotted(inner.targets[0]) in declared:
                    yield inner


def permissive_soft_delete_reads(source: str) -> list[str]:
    """Every place this source reads the soft-delete marker PERMISSIVELY.

    U18 removed this shape, U19 and U21 shipped it again, so the rule lives here.
    FORBIDDEN: a read supplying a FALSEY fallback, however spelled, or one
    laundered a line later (:func:`_laundered_reads`). ``rb_local_deleted`` is a
    bookkeeping column a binding change can stop exposing, and a falsey fallback
    then silently promotes every tombstone to a live row.

    LEFT ALONE (P7): a sentinel default the caller compares against, no default,
    a plain attribute read, the constant's definition, and a ``.get`` on a
    module-level table.

    KNOWN LIMITS: a row subclass with a falsey class default, the column from a
    function call other than a same-file writer accessor, a dictionary lookup,
    and a runtime attribute name. Recorded in the residual
    "What the soft-delete guard cannot see, and two gaps in the gate contract".
    """
    tree = ast.parse(source)
    names = SoftDeleteNames(tree)
    found = [
        f"line {node.lineno}: {ast.unparse(node)}"
        for node, default in _soft_delete_reads(tree, names)
        if default is not None and names.is_permissive(default)
    ]
    found += [
        f"line {node.lineno}: {ast.unparse(node)}"
        for node in _laundered_reads(tree, names)
    ]
    return sorted(set(found))


def reads_soft_delete_marker(source: str) -> bool:
    """Whether this source reads the soft-delete marker at all, permissively or not.

    Feeds an exact-membership pin over the modules that read the column, the only
    shape that catches a widening; see the residual
    "Guard whitelists assert what is forbidden, never what is permitted". It
    forces U24's ``trees.soft_delete_marker`` reconciliation. Defining the column
    is not reading it, so ``core/rb_writer.py`` is not a reader.
    """
    tree = ast.parse(source)
    return bool(_soft_delete_reads(tree, SoftDeleteNames(tree)))
