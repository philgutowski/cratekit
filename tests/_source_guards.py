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
import re

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


# ---------------------------------------------------------------------------
# U38: the two shapes that bypass the reserved exit-code table.
#
# APPENDED rather than filed beside its relatives, for the reason the verb
# registry and the reason registry both give: several units land against this
# file at once, and two additions inserted into the middle auto-merge while two
# appends conflict textually, which is a conflict somebody reads.
#
# These ask a different question of a different module than ``ReviewImports``
# does, so they are a sibling rather than a duplicate, and they answer it the
# same way: against the name the source actually BOUND, never against a bare
# attribute name. A guard that matched the text ``ExitCode`` would be satisfied
# by anybody's class of that name and defeated by one ``as`` keyword, which is
# the exact pair of failures the armed review guards already shipped once.
# ---------------------------------------------------------------------------

#: The module that owns the status vocabulary, and the package it sits in.
EXIT_CODE_MODULE = "cratekit.core.exit_codes"
EXIT_CODE_PACKAGE = "cratekit.core"

#: A cause slug as this repository spells one: lowercase words joined by single
#: hyphens. The reserved set is passed in as well, so a slug that does not match
#: this shape is still recognized once it is reserved. The shape is what lets the
#: guard see a table for causes NOBODY has reserved yet, which is the case the
#: table exists to prevent and the case a reserved-keys-only guard cannot see.
CAUSE_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")


class ExitCodeImports:
    """How one source file reaches ``ExitCode``, in every import shape.

    U12 COORDINATION. This is the same walk ``ReviewImports`` does, asked about a
    different module, and U12 is concurrently generalizing that one into a
    module-parameterized ``ImportsOf``. When both land, this class collapses into
    ``ImportsOf(tree, EXIT_CODE_MODULE)`` with one narrowing, because this one
    records only the ``ExitCode`` symbol where ``ImportsOf`` records every symbol
    a source imported. The two merge textually clean in either order, so nothing
    will flag the duplication; it is written down here instead.

    Five shapes are recognized, and they are every shape this repository's own
    modules use between them::

        import cratekit.core.exit_codes             # ...exit_codes.ExitCode.OK
        import cratekit.core.exit_codes as ec       # ec.ExitCode.OK
        from cratekit.core import exit_codes        # exit_codes.ExitCode.OK
        from cratekit.core.exit_codes import ExitCode        # ExitCode.OK
        from cratekit.core.exit_codes import ExitCode as EC  # EC.OK

    ``from cratekit.cli import exit_codes`` is deliberately NOT one of them. That
    name binds the reservation table, and reading the table is the sanctioned
    path rather than the shape being hunted.
    """

    def __init__(self, tree: ast.AST) -> None:
        #: Local names that ARE the vocabulary module.
        self.module_names: set[str] = set()
        #: Local names that ARE the ``ExitCode`` class itself.
        self.class_names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == EXIT_CODE_MODULE:
                        self.module_names.add(alias.asname or EXIT_CODE_MODULE)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names_the_module = module == EXIT_CODE_MODULE or (
                    node.level > 0 and module.split(".")[-2:] == ["core", "exit_codes"]
                )
                names_the_package = module == EXIT_CODE_PACKAGE or (
                    node.level > 0 and module.split(".")[-1:] == ["core"]
                )
                if names_the_module:
                    for alias in node.names:
                        if alias.name == "ExitCode":
                            self.class_names.add(alias.asname or "ExitCode")
                elif names_the_package:
                    for alias in node.names:
                        if alias.name == "exit_codes":
                            self.module_names.add(alias.asname or "exit_codes")

    def names_the_class(self, node: ast.AST) -> bool:
        """Whether ``node`` names the ``ExitCode`` CLASS this source imported."""
        dotted = _dotted(node)
        if dotted is None:
            return False
        if dotted in self.class_names:
            return True
        parts = dotted.split(".")
        return len(parts) >= 2 and ".".join(parts[:-1]) in self.module_names and parts[-1] == "ExitCode"

    def names_a_code(self, node: ast.AST) -> bool:
        """Whether ``node`` is a member of the ``ExitCode`` this source imported."""
        dotted = _dotted(node)
        if dotted is None:
            return False
        parts = dotted.split(".")
        if len(parts) >= 2 and ".".join(parts[:-1]) in self.class_names:
            return True
        return len(parts) >= 3 and ".".join(parts[:-2]) in self.module_names and parts[-2] == "ExitCode"


def _bound_module_names(tree: ast.AST, module: str) -> set[str]:
    """Local names bound to a standard-library MODULE, aliases included.

    Module binding only. ``from sys import exit`` binds a callable rather than a
    module and is answered by ``_bound_symbol_names`` below, which is the half
    that was missing: a guard that walked ``ast.Import`` alone let the one import
    shape that needs no attribute access through untouched.
    """
    return {
        alias.asname or alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
        if alias.name == module
    }


def _bound_symbol_names(tree: ast.AST, module: str, symbol: str) -> set[str]:
    """Local names bound to one SYMBOL of a standard-library module."""
    return {
        alias.asname or alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == module and node.level == 0
        for alias in node.names
        if alias.name == symbol
    }


def _module_level_literals(tree: ast.AST) -> dict[str, ast.AST]:
    """Every ``NAME = <expression>`` at module level, for one hop of resolution.

    One hop only, and deliberately. ``CAUSES = (...)`` beside
    ``dict(zip(CAUSES, CODES))`` is how a real module spells a table, and a guard
    that only understood the inlined spelling would be one refactor away from
    seeing nothing. Chasing further than one hop needs dataflow, which is the
    line this file does not cross.
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


class ReservedCodeTable:
    """Reads one source for a second opinion about what a refusal cause exits with.

    TWO SIDES HAVE TO BE RIGHT AT ONCE, and the first version of this guard got
    each of them wrong in a different direction.

    WHAT COUNTS AS A KEY. Not "a cause already reserved". A module that maps its
    OWN new causes to its own codes is the whole defect the table exists to
    prevent, and a guard keyed on the existing registry is blind to exactly that
    module. So a key counts when it is a reserved cause OR when it is spelled the
    way this repository spells a cause slug (``CAUSE_SLUG``). One word with no
    hyphen is not, which is what keeps a module's own data keyed on its own
    vocabulary out of it: ``{"files": ..., "settings": ...}`` is a portion table.

    WHAT COUNTS AS A CODE, and this is where a guard that fires on correct code
    gets itself switched off (P7). An ``ExitCode`` member is unambiguous. A bare
    integer is not: a cause slug mapped to 3 is an attempt budget, mapped to 1 is
    a display order, mapped to 5 is a backoff in seconds, and six of the reserved
    keys are also remediation tokens, so every one of those maps is ordinary
    correct code keyed on a slug. The only integers that can be a second
    reservation are the ones inside the RESERVED RANGE, which the caller passes
    in from the live table rather than repeating here. ``True`` and ``False`` are
    integers to ``isinstance`` and are never a status, so they are excluded
    before the range is even consulted.

    THE RESIDUAL LIMIT, stated rather than hidden: a backoff of 30 seconds keyed
    by a cause slug is indistinguishable from a reservation of 30 by shape alone,
    and this reports it. That direction was chosen deliberately, because the
    alternative is matching on the variable's NAME, and a guard a rename defeats
    is not a guard.
    """

    def __init__(self, tree: ast.AST, causes: frozenset[str], code_range: tuple[int, int]) -> None:
        self.tree = tree
        self.causes = causes
        self.low, self.high = code_range
        self.codes = ExitCodeImports(tree)
        self.literals = _module_level_literals(tree)

    def cause_key(self, node: ast.AST | None) -> str | None:
        """The cause slug a key names, whether or not anyone has reserved it."""
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            return None
        if node.value in self.causes or CAUSE_SLUG.match(node.value):
            return node.value
        return None

    def status(self, node: ast.AST | None) -> str | None:
        """What this expression reserves as a process status, or None."""
        if node is None:
            return None
        if self.codes.names_a_code(node):
            return ast.unparse(node)
        if isinstance(node, ast.Call) and len(node.args) == 1:
            # ``int(ExitCode.X)`` and ``ExitCode(30)``: a code with a conversion
            # wrapped round it is still a code, and both spellings read as
            # ordinary Python rather than as an evasion.
            wraps_a_code = _dotted(node.func) == "int" or self.codes.names_the_class(node.func)
            if wraps_a_code and self.status(node.args[0]) is not None:
                return ast.unparse(node)
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            if isinstance(node.value, bool):
                return None
            if self.low <= node.value < self.high:
                return f"bare status {node.value}"
        return None

    def _sequence(self, node: ast.AST) -> list[ast.AST] | None:
        """A literal sequence, through at most one module-level name."""
        if isinstance(node, ast.Name):
            node = self.literals.get(node.id, node)
        if isinstance(node, (ast.Tuple, ast.List)):
            return list(node.elts)
        return None

    def pairs(self) -> list[tuple[ast.AST, ast.AST]]:
        """Every place a key and a value are bound together, in any shape.

        Every shape below was written as an evasion first and only then as a
        rule, which is why the list is this specific.
        """
        found: list[tuple[ast.AST, ast.AST]] = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Dict):
                # A mapping literal, including the one inside ``dict(**{...})``,
                # ``MappingProxyType({...})`` and ``CODES.update({...})``.
                for key, value in zip(node.keys, node.values):
                    if key is not None:
                        found.append((key, value))
            elif isinstance(node, (ast.Tuple, ast.List)) and len(node.elts) == 2:
                # One pair, wherever it sits: a tuple of pairs, the argument to
                # ``dict([...])`` or ``OrderedDict([...])``, or the iterable a
                # dict comprehension unpacks.
                found.append((node.elts[0], node.elts[1]))
            elif isinstance(node, ast.DictComp):
                # ``{slug: 30 for slug in (...)}``: the value is the code and
                # every slug in the iterables is a key it is given to.
                for generator in node.generators:
                    for element in ast.walk(generator.iter):
                        if isinstance(element, ast.Constant):
                            found.append((element, node.value))
            elif isinstance(node, ast.Assign):
                # ``CODES[slug] = 30`` after ``CODES = {}``, which is a table
                # built a line at a time and is a table all the same.
                for target in node.targets:
                    if isinstance(target, ast.Subscript):
                        found.append((target.slice, node.value))
            elif isinstance(node, ast.Call):
                function = node.func
                if (
                    isinstance(function, ast.Attribute)
                    and function.attr == "setdefault"
                    and len(node.args) == 2
                ):
                    found.append((node.args[0], node.args[1]))
                elif _dotted(function) in {"dict", "OrderedDict"} and len(node.args) == 1:
                    found.extend(self._zipped(node.args[0]))
        found.extend(self._branches())
        return found

    def _zipped(self, argument: ast.AST) -> list[tuple[ast.AST, ast.AST]]:
        """``dict(zip(slugs, codes))``, with either sequence named once."""
        if not (isinstance(argument, ast.Call) and _dotted(argument.func) == "zip"):
            return []
        if len(argument.args) != 2:
            return []
        keys = self._sequence(argument.args[0])
        values = self._sequence(argument.args[1])
        if keys is None or values is None:
            return []
        return list(zip(keys, values))

    def _branches(self) -> list[tuple[ast.AST, ast.AST]]:
        """A table written as control flow: a match statement or an if chain.

        Narrowed to what the branch RETURNS. A module that waits 30 seconds
        inside a branch keyed on a cause is doing something ordinary, and a guard
        that reported it would be the false positive that gets the whole check
        suppressed. A module that RETURNS 30 from that branch is answering the
        question this table answers.
        """
        found: list[tuple[ast.AST, ast.AST]] = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Match):
                for case in node.cases:
                    keys = [
                        pattern.value
                        for pattern in ast.walk(case.pattern)
                        if isinstance(pattern, ast.MatchValue)
                    ]
                    found.extend(self._returned(keys, case.body))
            elif isinstance(node, ast.If):
                keys = [
                    element
                    for element in ast.walk(node.test)
                    if isinstance(element, ast.Constant)
                ]
                found.extend(self._returned(keys, node.body))
        return found

    @staticmethod
    def _returned(keys: list[ast.AST], body: list[ast.stmt]) -> list[tuple[ast.AST, ast.AST]]:
        returned = [
            statement.value
            for statement in body
            if isinstance(statement, ast.Return) and statement.value is not None
        ]
        return [(key, value) for key in keys for value in returned]


def reserved_code_tables(
    source: str, causes: frozenset[str], code_range: tuple[int, int]
) -> list[str]:
    """Every place this source gives a refusal cause its own exit code.

    A second table is how two answers to one question appear, and the repository
    has already paid for that shape once in its taxonomy resolvers. The class
    above carries the reasoning for what counts as a key and what counts as a
    code; this function is the walk over every shape a table can be written in.

    Deliberately NOT restricted to dict literals, which is what the first version
    was while its docstring claimed otherwise. A tuple of pairs, a comprehension,
    ``dict(zip(...))``, a mapping filled a key at a time, ``setdefault``, a match
    statement and an if chain are all a table, and a guard that only understood
    the punctuation of one of them is a guard the next module walks past without
    meaning to.
    """
    table = ReservedCodeTable(ast.parse(source), causes, code_range)
    found: list[str] = []
    seen: set[tuple[int, str, str]] = set()
    for key, value in table.pairs():
        slug = table.cause_key(key)
        if slug is None:
            continue
        status = table.status(value)
        if status is None:
            continue
        entry = (key.lineno, slug, status)
        if entry in seen:
            continue
        seen.add(entry)
        found.append(f"line {key.lineno}: {slug!r} -> {status}")
    return sorted(found)


class ProcessExits:
    """Every local name in one source that ends the process with a status.

    Four bindings reach a process status, and the first version of this guard
    recognized one and a half of them::

        import sys; sys.exit(30)            # recognized
        import sys as system; system.exit(30)   # recognized
        from sys import exit; exit(30)      # NOT, and it needs no attribute
        from os import _exit; _exit(30)     # NOT
        e = sys.exit; e(30)                 # NOT
        SE = SystemExit; raise SE(30)       # NOT
        class Refused(SystemExit): ...      # NOT, and it reads as good design

    The two ``from`` shapes are the ones that matter, because they are ordinary
    Python that anybody might write without meaning to evade anything, and
    because both sibling classes in this file already handle ``ast.ImportFrom``.
    The aliases are cheaper to close than to argue about, so they are closed.

    Resolution runs to a fixed point, so ``a = sys.exit`` then ``b = a`` binds
    both, and a class deriving from a class deriving from ``SystemExit`` is one.
    """

    def __init__(self, tree: ast.AST) -> None:
        #: Names that, CALLED, end the process.
        self.exits: set[str] = {
            f"{name}.exit" for name in _bound_module_names(tree, "sys")
        } | {f"{name}._exit" for name in _bound_module_names(tree, "os")}
        self.exits |= _bound_symbol_names(tree, "sys", "exit")
        self.exits |= _bound_symbol_names(tree, "os", "_exit")
        #: Names that ARE the exception whose argument is a process status.
        self.statuses: set[str] = {"SystemExit"}
        assignments = _assignments(tree)
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        changed = True
        while changed:
            changed = False
            for name, value in assignments:
                dotted = _dotted(value)
                if dotted in self.exits and name not in self.exits:
                    self.exits.add(name)
                    changed = True
                if dotted in self.statuses and name not in self.statuses:
                    self.statuses.add(name)
                    changed = True
            for node in classes:
                if node.name in self.statuses:
                    continue
                if any(_dotted(base) in self.statuses for base in node.bases):
                    self.statuses.add(node.name)
                    changed = True

    def ends_the_process(self, node: ast.AST) -> bool:
        target = _dotted(node)
        return target is not None and (target in self.exits or target in self.statuses)


def process_status_literals(source: str) -> list[str]:
    """Every place this source turns a bare integer into a process status.

    ``sys.exit(21)`` bypasses the whole vocabulary: nothing imports, nothing
    looks anything up, and the integer arrives at the shell meaning whatever the
    author believed that day. Every name is bound through the import graph, so
    ``import sys as system`` and ``from sys import exit`` are both caught and
    ``runner.exit(21)`` on somebody's own object is not.

    Zero is excluded. ``sys.exit(0)`` is success spelled plainly and is not a
    refusal, and reporting it would be the false positive that gets the whole
    guard suppressed. ``True`` is excluded for the same reason and a stronger
    one: it is an integer only by accident of the language.
    """
    tree = ast.parse(source)
    exits = ProcessExits(tree)
    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or len(node.args) != 1:
            continue
        argument = node.args[0]
        if not (isinstance(argument, ast.Constant) and isinstance(argument.value, int)):
            continue
        if argument.value == 0 or isinstance(argument.value, bool):
            continue
        if exits.ends_the_process(node.func):
            found.append(f"line {node.lineno}: {ast.unparse(node)}")
    return found
