"""Source analysis shared by the guards that hold a LATER unit to what an earlier one settled.

Three files ask these questions, ``tests/test_review_queue.py``,
``tests/test_cli_contract.py`` and ``tests/test_pool_sizing.py``, and the first
two used to ask them with two copies of the same walk. One copy learned to
recognize an aliased import and the other did not, which is the second opinion
that eventually disagrees. There is one implementation now, and every fixture
that proves it bites lives beside it.

WHY THESE WALK THE IMPORT GRAPH RATHER THAN MATCHING A NAME. A guard that looks
for an attribute called ``offer`` is satisfied by any object in the language that
happens to have a method of that name, so a module that never touches the review
queue at all can pass it. A reviewer demonstrated exactly that: a file that hand
edits a gate column in a comma separated file, plus one unrelated ``.offer(``
call and one dead assignment, satisfied all three assertions of the countdown
meant to forbid it. So every question here is answered against the name the
source actually bound ``cratekit.core.review`` to, in whichever import shape it
used, and a call on anything else is not an answer.

THE OTHER DIRECTION MATTERS JUST AS MUCH (P7). A guard that fires on correct code
gets routed around, so each function accepts every import shape this repository
allows: the module imported whole, the module imported under another name, and a
symbol imported from it directly. ``tests/test_review_queue.py`` runs each one
against a correct fixture in both shapes AND against the evasion, because P7 says
to run a guard against correct code before shipping it and that half was the half
that was skipped.
"""

from __future__ import annotations

import ast

#: The module every question here is asked about.
REVIEW_MODULE = "cratekit.core.review"

#: The two constructors that produce a comma separated writer. Named once so the
#: files that need this question cannot ask it two different ways.
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

    THE FALLBACK, AND ONLY THE FALLBACK. A relative import cannot be resolved to
    an absolute module without knowing which package the importing file sits in,
    so a caller that does not say gets its relative imports matched by tail
    instead. That is a heuristic and it is wrong in one direction: a file in an
    unrelated package writing ``from .pool import PoolPlan`` ends the same way as
    the real one and fires. Callers that walk real files pass ``package`` and get
    exact resolution instead. See :func:`package_of`.
    """
    if not candidate:
        return False
    wanted = candidate.split(".")
    return path.split(".")[-len(wanted):] == wanted


def _absolute_module(package: str | None, level: int, module: str) -> str | None:
    """The module a relative import names, resolved against the importing package.

    ``from . import pool`` inside ``cratekit.core`` names ``cratekit.core.pool``
    and the identical line inside ``somewhere.else`` names ``somewhere.else.pool``,
    which is a different module in a different distribution. One of them is the
    thing a guard is looking for and the other is not, and the only thing that
    tells them apart is where the importing file sits.

    None means the import reaches nothing this walk can name: either there is no
    package to resolve against, or the dots climb past the top of the package
    tree, which is an import the interpreter itself refuses.
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
    """The dotted package a module sits in, or None when it is not inside one.

    The one piece of information :class:`ImportsOf` needs and was never given.
    Every walk in this repository already holds the ``Path`` and threw it away at
    ``read_text()``, so the fix is to pass it on rather than to compute anything
    new.
    """
    try:
        relative = path.resolve().relative_to(source_root.resolve())
    except ValueError:
        return None
    parts = relative.parts[:-1]
    return ".".join(parts) if parts else None


class ImportsOf:
    """How one source file reaches ONE named module, if it reaches it at all.

    Four shapes were recognized first, and they are the four this repository's
    own modules use between them::

        import cratekit.core.review            # cratekit.core.review.offer(...)
        import cratekit.core.review as rv      # rv.offer(...)
        from cratekit.core import review       # review.offer(...)
        from cratekit.core.review import offer # offer(...)

    AN ANCESTOR PACKAGE REACHES THE MODULE TOO, which is five more shapes, and
    the hole was live rather than theoretical. ``from cratekit import core``
    followed by ``core.pool.PoolPlan(...)`` builds the very object the provenance
    guard exists to forbid, and ``import cratekit.core`` does the same thing one
    import shorter. Neither names the module, so a walk keyed on the module's own
    dotted path saw nothing at all and the guard returned an empty list. That is
    the same shape the pool construction guard in ``tests/test_pool_sizing.py``
    had already closed for its own question, by deriving the import shapes rather
    than listing them, and the two walks sat in one wave giving two different
    answers to one question.

    A relative import is recognized too, INCLUDING THE BARE ``from . import
    pool`` that a sibling inside the module's own package writes, which is the
    package the sizing module lives in. That one was invisible in BOTH
    directions, which is the more expensive half: the countdown could not see a
    fabricated plan built that way, and it could not see a correct ``plan_pool``
    call built that way either, so a correctly sized package would have been
    reported as having no planner in it at all.

    PARAMETERIZED BY MODULE, because the review queue is no longer the only
    obligation a countdown holds a later unit to. U12 asks the same question
    about ``cratekit.core.pool``, and asking it with a second copy of this walk
    is exactly the drift this file was created to end: the copy that learned to
    recognize an aliased import and the copy that did not.

    AND PARAMETERIZED BY THE IMPORTING FILE'S PACKAGE, which is what makes the
    relative half exact rather than approximate. Given the package, a relative
    import is RESOLVED: the dots are counted against the package's own parts and
    the result is compared like any absolute name. Without one, it falls back to
    matching by dotted tail, which fires on a file in an unrelated package
    writing ``from .pool import PoolPlan``, ``from . import pool``,
    ``from . import core``, ``from .core.pool import PoolPlan`` or
    ``from .. import cratekit``. All five are silent once the package is passed,
    and all five are demonstrated in ``tests/test_pool_sizing.py``. Any caller
    walking real files has the package for free and should pass it.
    """

    def __init__(self, tree: ast.AST, module: str, package: str | None = None) -> None:
        self.module = module
        self.package = package
        parts = module.split(".")
        #: Every dotted prefix of the module, mapped to the path still to be
        #: walked from it. The module itself maps to the empty string. Derived
        #: from the module's own name rather than listed, because a listed set of
        #: shapes is a set somebody has to remember to extend.
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
            # Longest first, so a name that is a tail of two ancestors is
            # credited to the more specific one. REDUNDANT for the three modules
            # this file is asked about, since no two ancestors of any of them
            # share a dotted tail, so reversing the order kills nothing today.
            # Kept because the ambiguity is a property of the module NAME rather
            # than of this code, and the next module asked about may have it.
            for path in sorted(ancestors, key=len, reverse=True):
                if _dotted_tail_of(reached, path):
                    return ancestors[path]
            return None

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in ancestors:
                        self.paths[alias.asname or alias.name] = ancestors[alias.name]
            elif isinstance(node, ast.ImportFrom):
                imported = node.module or ""
                by_tail = False
                if node.level:
                    if package is None:
                        # Nothing to resolve against, so fall back to the tail
                        # heuristic and accept its one false direction.
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
        #: Local names that ARE the module, kept as its own set because that is
        #: the question most of this file asks.
        self.module_names: set[str] = {name for name, rest in self.paths.items() if not rest}

    @property
    def reaches(self) -> bool:
        """Whether this source imports the module at all, in any shape."""
        return bool(self.paths or self.symbols)

    def resolves(self, node: ast.AST, wanted: str) -> bool:
        """Whether ``node`` names the module's ``wanted`` attribute.

        ``wanted`` may itself be dotted, so ``Queue.VERSION_MATCH`` is one
        question rather than two, and it is answered the same way whether the
        source spelled the module, an alias for it, an ancestor package of it, or
        imported ``Queue`` on its own.
        """
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

    Kept as its own name because the review questions below read better for it
    and because the file's callers already spell it, but it is the general walk
    with one argument filled in rather than a second implementation.
    """

    def __init__(self, tree: ast.AST) -> None:
        super().__init__(tree, REVIEW_MODULE)

    @property
    def reaches_review(self) -> bool:
        """Whether this source imports the review module at all, in any shape."""
        return self.reaches


def calls_attribute(source: str, module: str, wanted: str, *, package: str | None = None) -> bool:
    """Whether this source CALLS ``module``'s ``wanted`` function, in any import shape.

    The general form of :func:`calls_review`. A call on something that merely has
    a function of the same name is not an answer, which is the whole reason this
    binds through the import graph. ``package`` is the package the source sits
    in, and passing it is what makes a relative import resolve exactly.
    """
    tree = ast.parse(source)
    imports = ImportsOf(tree, module, package)
    if not imports.reaches:
        return False
    return any(
        isinstance(node, ast.Call) and imports.resolves(node.func, wanted)
        for node in ast.walk(tree)
    )


def _assignments(tree: ast.AST) -> list[tuple[str, ast.AST]]:
    """Every ``name = value`` and ``self.name = value``, as (dotted target, value).

    Attribute targets are included because the ordinary way to hold a store is a
    field on an object, and a guard that only understood local variables would
    fail on the shape most likely to be correct.
    """
    found: list[tuple[str, ast.AST]] = []
    for node in ast.walk(tree):
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


def calls_review(source: str, wanted: str) -> bool:
    """Whether this source CALLS the review module's ``wanted`` function."""
    return calls_attribute(source, REVIEW_MODULE, wanted)


def offers_into(source: str, queue: str) -> bool:
    """Whether a review ``offer`` call is given the review queue named by ``queue``.

    The queue has to reach the CALL. An assignment naming the queue and going
    nowhere is what a module writes when somebody wanted the countdown to pass,
    and it is indistinguishable from a comment. One hop of indirection is
    accepted, because ``QUEUE = review.Queue.VERSION_MATCH`` at module level and
    ``queue=QUEUE`` at the call is ordinary correct code.
    """
    tree = ast.parse(source)
    imports = ReviewImports(tree)
    if not imports.reaches_review:
        return False
    aliases = {
        name
        for name, value in _assignments(tree)
        if imports.resolves(value, queue)
    }
    for node in ast.walk(tree):
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


def constructs_review(source: str, wanted: str) -> bool:
    """Whether this source CONSTRUCTS the review module's ``wanted`` class."""
    return calls_review(source, wanted)


def methods_on_review_construction(source: str, wanted: str) -> set[str]:
    """Method names called on something this source built from review's ``wanted``.

    The receiver is traced rather than assumed, through the three shapes a real
    module uses: a local variable, a field on an object, and a small helper that
    returns one. A method called on anything else is not counted, which is what
    stops an unrelated class with a method of the same name from answering for
    the store.
    """
    tree = ast.parse(source)
    imports = ReviewImports(tree)
    if not imports.reaches_review:
        return set()

    def is_construction(node: ast.AST) -> bool:
        return isinstance(node, ast.Call) and imports.resolves(node.func, wanted)

    factories = {
        function.name
        for function in ast.walk(tree)
        if isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef))
        for statement in ast.walk(function)
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
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        receiver = node.func.value
        if is_construction(receiver) or _dotted(receiver) in traced:
            found.add(node.func.attr)
    return found


def constructs_a_csv_writer(source: str) -> list[str]:
    """Every place this source builds a comma separated WRITER, in any import shape.

    Three narrowings, and each one is there so the guard cannot fire on correct
    code, which is how a guard gets routed around (P7).

    WRITING ONLY. Reading stays legal. The anti-pattern R12 names is "a file the
    user must hand edit", which is a file this product WROTE for them to edit. A
    tracklist somebody pastes in from elsewhere is legitimate intake, and a guard
    that refused it would be refusing the feature.

    THE MODULE IS NAMED, not just the attribute. ``xml.writer`` and
    ``something.DictWriter`` are perfectly ordinary names for things that are not
    this.

    THE NAME IS THE ONE THE SOURCE BOUND. ``import csv as spreadsheet`` binds the
    module to ``spreadsheet``, and a guard that only recognized the literal
    ``csv`` was one keyword away from being switched off. That gap was live in
    the armed copy of this question.
    """
    tree = ast.parse(source)
    module_names = {
        alias.asname or "csv"
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
        if alias.name == "csv"
    }
    imported = {
        alias.asname or alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "csv"
        for alias in node.names
        if alias.name in CSV_WRITER_NAMES
    }
    found: list[str] = []
    for node in ast.walk(tree):
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
    """Every module under one package directory, as (relative name, source).

    A countdown that named one file inside a package would be satisfied by that
    file and blind to the rest of the unit. Walking is the same rule the state
    audit follows (P3).
    """
    return [
        (path.name, path.read_text())
        for path in sorted(package_root.rglob("*.py"))
    ]
