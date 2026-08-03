"""Source analysis shared by the guards that hold a LATER unit to what U11 settled.

Two files ask these questions, ``tests/test_review_queue.py`` and
``tests/test_cli_contract.py``, and they used to ask them with two copies of the
same walk. One copy learned to recognize an aliased import and the other did not,
which is the second opinion that eventually disagrees. There is one
implementation now, and every fixture that proves it bites lives beside it.

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

#: The package it lives in, for the ``from cratekit.core import review`` shape.
REVIEW_PACKAGE = "cratekit.core"

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


class ReviewImports:
    """How one source file reaches the review module, if it reaches it at all.

    Three shapes are recognized, and they are the three this repository's own
    modules use between them::

        import cratekit.core.review            # cratekit.core.review.offer(...)
        import cratekit.core.review as rv      # rv.offer(...)
        from cratekit.core import review       # review.offer(...)
        from cratekit.core.review import offer # offer(...)

    A relative import is recognized too. Nothing in the package uses one today,
    and a guard that failed the first module to do so would be a guard somebody
    routes around rather than a defect anybody fixes.
    """

    def __init__(self, tree: ast.AST) -> None:
        #: Local names that ARE the module.
        self.module_names: set[str] = set()
        #: Local name -> the module attribute it was imported as.
        self.symbols: dict[str, str] = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == REVIEW_MODULE:
                        self.module_names.add(alias.asname or REVIEW_MODULE)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names_the_module = module == REVIEW_MODULE or (
                    node.level > 0 and module.split(".")[-2:] == ["core", "review"]
                )
                names_the_package = module == REVIEW_PACKAGE or (
                    node.level > 0 and module.split(".")[-1:] == ["core"]
                )
                if names_the_module:
                    for alias in node.names:
                        self.symbols[alias.asname or alias.name] = alias.name
                elif names_the_package:
                    for alias in node.names:
                        if alias.name == "review":
                            self.module_names.add(alias.asname or "review")

    @property
    def reaches_review(self) -> bool:
        """Whether this source imports the review module at all, in any shape."""
        return bool(self.module_names or self.symbols)

    def resolves(self, node: ast.AST, wanted: str) -> bool:
        """Whether ``node`` names the review module's ``wanted`` attribute.

        ``wanted`` may itself be dotted, so ``Queue.VERSION_MATCH`` is one
        question rather than two, and it is answered the same way whether the
        source spelled the module, an alias for it, or imported ``Queue`` on its
        own.
        """
        dotted = _dotted(node)
        if dotted is None:
            return False
        for module_name in self.module_names:
            if dotted == f"{module_name}.{wanted}":
                return True
        head, _, rest = dotted.partition(".")
        symbol = self.symbols.get(head)
        if symbol is None:
            return False
        return (f"{symbol}.{rest}" if rest else symbol) == wanted


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
    tree = ast.parse(source)
    imports = ReviewImports(tree)
    if not imports.reaches_review:
        return False
    return any(
        isinstance(node, ast.Call) and imports.resolves(node.func, wanted)
        for node in ast.walk(tree)
    )


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


# ═══════════════════════════════════════════════════════════════════════════
# The soft-delete marker: read it, never default it
#
# APPENDED, per this file's convention. Two units edit this file in the same
# wave, and an addition in the middle auto-merges with theirs while an addition
# at the end conflicts textually, which is a conflict somebody reads.
# ═══════════════════════════════════════════════════════════════════════════

#: The module that owns the binding's vocabulary, and the constant on it that
#: names the soft-delete column. The guard below resolves a reader through the
#: import graph to THIS symbol, so a module that says
#: ``rb_writer.SOFT_DELETE_COLUMN`` is recognized as naming the column even
#: though the text ``rb_local_deleted`` never appears in it.
RB_WRITER_MODULE = "cratekit.core.rb_writer"
RB_WRITER_PACKAGE = "cratekit.core"
SOFT_DELETE_CONSTANT = "SOFT_DELETE_COLUMN"

#: The column itself. Kept here as well as resolved through the import graph
#: because the literal is still legal to write and is what the defect looked
#: like, and a guard that recognized only the indirection would miss the shape it
#: exists to catch.
SOFT_DELETE_COLUMN_LITERAL = "rb_local_deleted"


class SoftDeleteNames:
    """Every expression in one source file that NAMES the soft-delete column.

    Four shapes, and the reason each is here rather than left out:

    * the literal ``"rb_local_deleted"``, which is what the defect looked like
      at ``write/metadata.py:195`` and at ``write/routing_pass.py``;
    * ``rb_writer.SOFT_DELETE_COLUMN`` through any import shape, which is what
      correct code SHOULD say and what a guard bound to the literal alone would
      be blind to;
    * a local constant assigned either of those, one hop, because
      ``COLUMN = rb_writer.SOFT_DELETE_COLUMN`` at module level and
      ``getattr(row, COLUMN, 0)`` at the call is the obvious way around a guard
      that only reads the argument;
    * a local constant assigned a FALSEY constant, which is the same evasion
      pointed at the default rather than at the column.

    One hop is where this stops, deliberately, and it is the same depth
    :func:`offers_into` accepts. Chasing arbitrary indirection means writing a
    small interpreter, and the shape a person actually reaches for when a guard
    is in their way is exactly one name.
    """

    def __init__(self, tree: ast.AST) -> None:
        #: Local names that ARE the rb_writer module.
        self.module_names: set[str] = set()
        #: Local names bound directly to the constant.
        self.constant_names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == RB_WRITER_MODULE:
                        self.module_names.add(alias.asname or RB_WRITER_MODULE)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names_the_module = module == RB_WRITER_MODULE or (
                    node.level > 0 and module.split(".")[-2:] == ["core", "rb_writer"]
                )
                names_the_package = module == RB_WRITER_PACKAGE or (
                    node.level > 0 and module.split(".")[-1:] == ["core"]
                )
                if names_the_module:
                    for alias in node.names:
                        if alias.name == SOFT_DELETE_CONSTANT:
                            self.constant_names.add(alias.asname or alias.name)
                elif names_the_package:
                    for alias in node.names:
                        if alias.name == "rb_writer":
                            self.module_names.add(alias.asname or "rb_writer")

        # The one hop. Resolved after the imports so an alias assigned from an
        # imported constant is seen, and iterated to a fixed point over the
        # module's own assignments so ordering in the file does not decide it.
        #: Local names bound to something FALSEY, which is what a permissive
        #: default looks like once it has been given a name.
        self.falsey_names: set[str] = set()
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
            if not grew:
                break

    def _is_column(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Constant) and node.value == SOFT_DELETE_COLUMN_LITERAL:
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
        if isinstance(node, ast.Constant):
            return not node.value
        dotted = _dotted(node)
        return dotted is not None and dotted in self.falsey_names

    def names_the_column(self, node: ast.AST) -> bool:
        """Whether ``node`` evaluates to the soft-delete column's name."""
        return self._is_column(node)

    def is_permissive(self, node: ast.AST) -> bool:
        """Whether ``node`` is a default that reads as 'this row is active'.

        Falsey is the whole test, because the marker is consumed as a truth
        value: ``0``, ``False``, ``None`` and ``""`` all mean active, and
        ``bool(None)`` is not a third state however much a reader wants it to be.
        A sentinel object is truthy and is therefore NOT flagged, which is
        correct: a sentinel forces the caller to compare against it, and a
        sentinel that is never compared reports every row as DELETED, which is
        the safe direction and fails loudly rather than quietly.
        """
        return self._is_falsey(node)


def _soft_delete_reads(tree: ast.AST, names: SoftDeleteNames) -> list[tuple[ast.AST, ast.AST | None]]:
    """Every read of the marker, paired with the default it supplied, if any.

    Three access shapes, because a rekordbox row reaches this package as an
    object from the binding AND as a mapping from a raw query, and a guard that
    understood only one of them would be answered by rewriting the other.
    """
    found: list[tuple[ast.AST, ast.AST | None]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr == SOFT_DELETE_COLUMN_LITERAL:
            # ``row.rb_local_deleted``. No default is possible, so it cannot be
            # permissive; it is recorded because the READER pin below counts it.
            found.append((node, None))
            continue
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id == "getattr" and len(node.args) >= 2:
            if names.names_the_column(node.args[1]):
                found.append((node, node.args[2] if len(node.args) > 2 else None))
        elif isinstance(func, ast.Attribute) and func.attr == "get" and node.args:
            if names.names_the_column(node.args[0]):
                # A one-argument ``.get`` defaults to None ALL BY ITSELF, which
                # is the permissive answer arrived at by omission rather than by
                # decision. It is reported as a read whose default is a synthetic
                # None so it lands on the same side of the line.
                default = node.args[1] if len(node.args) > 1 else ast.Constant(value=None)
                found.append((node, default))
    return found


def permissive_soft_delete_reads(source: str) -> list[str]:
    """Every place this source reads the soft-delete marker PERMISSIVELY.

    This is the shape U18 removed, U19 shipped again as a blocking defect, and
    U21 shipped a third time at ``write/metadata.py:195`` on the genre lookup.
    Three times on one column is not three people being careless, it is a rule
    that lived in a docstring, so it lives here instead.

    WHAT IS FORBIDDEN is a read that supplies a FALSEY fallback, however the
    column and the fallback are spelled. ``rb_local_deleted`` is a bookkeeping
    column, so it is exactly the column a binding change can stop exposing, and
    the fallback is then applied to every row at once. Falsey means active, so
    the fallback silently promotes every tombstone in the library to a live row
    and nothing anywhere reports it.

    WHAT IS LEFT ALONE, so the guard cannot fire on correct code (P7): a read
    with a sentinel default that the caller then compares against, a read with no
    default at all, a plain attribute access, and the constant's own definition.
    All four fail loudly or not at all, and none of them can answer "active" for
    a row that never said so.
    """
    tree = ast.parse(source)
    names = SoftDeleteNames(tree)
    return [
        f"line {node.lineno}: {ast.unparse(node)}"
        for node, default in _soft_delete_reads(tree, names)
        if default is not None and names.is_permissive(default)
    ]


def reads_soft_delete_marker(source: str) -> bool:
    """Whether this source reads the soft-delete marker at all, permissively or not.

    Separate from the question above because the two guard different things. The
    one above is a defect check and must fire on nobody today. This one feeds an
    exact-membership PIN over the modules that read the column, which is the only
    shape that catches a WIDENING (R-15): a fourth reader is a two-line diff that
    passes every other assertion in this suite.

    It is what will force the reconciliation with U24's ``trees.soft_delete_marker``
    instead of leaving it to be remembered. That unit lands a single sanctioned
    implementation; the moment it merges, this pin has more readers than it
    declares and goes red until they are collapsed into one.

    Defining the column is not reading it, so ``core/rb_writer.py`` is not a
    reader and the pin does not have to carve out an exception for the module
    that owns the name.
    """
    tree = ast.parse(source)
    return bool(_soft_delete_reads(tree, SoftDeleteNames(tree)))
