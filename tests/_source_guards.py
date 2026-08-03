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
#: hyphens.
#:
#: NOT a key rule on its own, and it was one for exactly one round. Any kebab
#: string mapped to an integer inside the reserved range counted, which is a
#: logging level, a column width, a timeout, a retention in days, a retry budget,
#: a loudness target, a schema version, or any two-element tuple of a label and a
#: number. None of those is a reservation and every one of them would have fired.
#: The shape is now one half of a test whose other half is a DECLARATION: the
#: string has to be a cause somebody declares, either in the registry, in the
#: package-wide derivation the caller passes in, or as an enum member in this very
#: file. See ``ReservedCodeTable``.
CAUSE_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")


def _relative_module(node: ast.ImportFrom, package: str) -> str | None:
    """The absolute module a RELATIVE import names, resolved against its package.

    ``node.module`` is only the TAIL of a relative import, and the round before
    this matched that tail against a two-element suffix. That answered for
    ``from ..core.exit_codes import ExitCode`` and for no other relative
    spelling: a SIBLING records ``exit_codes`` and nothing else, and ``from .
    import exit_codes`` records nothing at all, so the two shapes most natural
    for a module sitting beside ``core/exit_codes.py`` were the two the guard
    could not see. Recognizing one relative form and not another is a bug in the
    resolution rather than a decision about scope.

    One dot is the file's own package, and one level up from
    ``cratekit.core.session`` is ``cratekit.core`` whether the file is a module
    or that package's ``__init__``, which is why the caller passes the dotted
    directory in both cases. None means the level walks off the top of the
    package, which Python refuses to import at all, so it names no module here
    either.
    """
    parts = package.split(".")
    if node.level - 1 >= len(parts):
        return None
    base = parts[: len(parts) - (node.level - 1)]
    return ".".join(base + ([node.module] if node.module else []))


class ExitCodeImports:
    """How one source file reaches ``ExitCode``, in every import shape.

    U12 COORDINATION, and it is now a THREE way duplication rather than a two.
    This is the same walk ``ReviewImports`` does, asked about a different module.
    U12 is generalizing that one into a module-parameterized ``ImportsOf``, and
    the conformance branch has a third copy of it as ``SoftDeleteNames``. All
    three merge textually clean in any order, so nothing will flag it. When they
    land together, this class collapses into ``ImportsOf(tree,
    EXIT_CODE_MODULE)`` with one narrowing, because this one records only the
    ``ExitCode`` symbol where ``ImportsOf`` records every symbol a source
    imported, and ``SoftDeleteNames`` collapses the same way. THE COLLAPSE HAS TO
    TAKE THE RELATIVE HANDLING BELOW WITH IT. The other two copies still carry
    the suffix match this one replaced, and a collapse onto either of them would
    reinstate the defect in one place instead of three. R-15 records that.

    Seven shapes are recognized, and they are every shape this repository's own
    modules use between them::

        import cratekit.core.exit_codes             # ...exit_codes.ExitCode.OK
        import cratekit.core.exit_codes as ec       # ec.ExitCode.OK
        from cratekit.core import exit_codes        # exit_codes.ExitCode.OK
        from cratekit.core.exit_codes import ExitCode        # ExitCode.OK
        from cratekit.core.exit_codes import ExitCode as EC  # EC.OK
        from .exit_codes import ExitCode            # a sibling of the module
        from . import exit_codes                    # the same, module bound

    ``from cratekit.cli import exit_codes`` is deliberately NOT one of them, and
    neither is the relative spelling of it from inside ``cli``. That name binds
    the reservation table, and reading the table is the sanctioned path rather
    than the shape being hunted. Resolving the level is what makes the relative
    spelling answer the same way the absolute one does rather than by accident.
    """

    def __init__(self, tree: ast.AST, package: str | None = None) -> None:
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
                names_the_module, names_the_package = self._targets(node, package)
                if names_the_module:
                    for alias in node.names:
                        if alias.name == "ExitCode":
                            self.class_names.add(alias.asname or "ExitCode")
                elif names_the_package:
                    for alias in node.names:
                        if alias.name == "exit_codes":
                            self.module_names.add(alias.asname or "exit_codes")

    @staticmethod
    def _targets(node: ast.ImportFrom, package: str | None) -> tuple[bool, bool]:
        """Whether this import names the vocabulary MODULE, or the package it sits in.

        Resolved against the importer's package when the caller knows it, which
        is the whole tree scan, so ``from . import exit_codes`` inside ``cli``
        resolves to the reservation table and stays out exactly as its absolute
        spelling does.

        The fallback, for a source with no path, matches the TAIL and accepts a
        bare sibling. A fixture is a file that could be anywhere, so the only
        honest reading of ``from .exit_codes import ExitCode`` there is that it
        names a module called ``exit_codes``.
        """
        if not node.level:
            module = node.module or ""
            return module == EXIT_CODE_MODULE, module == EXIT_CODE_PACKAGE
        if package is not None:
            absolute = _relative_module(node, package)
            return absolute == EXIT_CODE_MODULE, absolute == EXIT_CODE_PACKAGE
        tail = (node.module or "").split(".")
        names_the_module = tail[-2:] == ["core", "exit_codes"] or tail == ["exit_codes"]
        names_the_package = tail[-1:] == ["core"] or node.module is None
        return names_the_module, names_the_package

    def names_the_class(self, node: ast.AST) -> bool:
        """Whether ``node`` names the ``ExitCode`` CLASS this source imported."""
        dotted = _dotted(node)
        if dotted is None:
            return False
        if dotted in self.class_names:
            return True
        # The module-qualified spelling, ``exit_codes.ExitCode(30)``. Reachable
        # only through ``status``'s conversion branch, and no fixture in the tree
        # writes a conversion that way today, so a reader should take this as
        # defence in depth rather than as a live path. See R-16.
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


# ``_bound_module_names`` and ``_bound_symbol_names`` stood here. They were round
# one's answer to ``from sys import exit`` and round two replaced them with
# ``ProcessExits``, which binds by module IDENTITY and covers every shape they
# did. Nothing called either of them afterwards, while one of the two carried a
# docstring naming itself the fix for the defect. Dead code that claims a repair
# is worse than no code: a reader checking whether the shape is handled finds a
# function that says yes and never runs. Deleted rather than left as evidence.


def _module_level_literals(tree: ast.AST) -> dict[str, ast.AST]:
    """Every ``NAME = <expression>`` at module level, for resolution by name.

    ``PRECONDITION = 30`` beside ``CODES = {"tagger-art-rejected": PRECONDITION}``
    is how a real module writes a table, because a bare 30 in a mapping tells a
    reader nothing about which band it belongs to. A guard that read only the
    inlined integer was defeated by the more careful spelling, which is the wrong
    way round.
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
    """Every ``CLASS.MEMBER = <expression>``, one level deep, by class name.

    Covers a module holding its codes on a class or in an ``IntEnum`` of its own,
    which is the same table written with a namespace round it.
    """
    found: dict[str, dict[str, ast.AST]] = {}
    for node in ast.walk(tree):
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


def _declared_enum_values(tree: ast.AST) -> set[str]:
    """Every cause-shaped string this source declares as an enum member value.

    This is the DECLARATION half of the key test. A module that writes
    ``ART_REJECTED = "tagger-art-rejected"`` inside an enum has declared that
    string to be one of its causes, in its own file, before anybody reserved it.
    Mapping that same string to a status somewhere else in the same file is a
    reservation whoever wrote it, and no registry has to have heard of it.

    Matched on the BASE being an enum, which is how Python spells an enum, not on
    what the class or the variable holding it was called. A rename of either
    changes nothing.
    """
    found: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        bases = [_dotted(base) or "" for base in node.bases]
        if not any(base.split(".")[-1].endswith("Enum") for base in bases):
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
#: LOAD BEARING IN BOTH DIRECTIONS, and only the downward half used to be
#: covered. Lowering it stops the guard resolving the careful spellings and kills
#: seven tests. Raising it past the interpreter's own recursion limit turns
#: ``A = B`` beside ``B = A`` from a silent None into a ``RecursionError`` that
#: takes the suite with it, which is the hang this constant exists to prevent, so
#: ``test_a_mutually_recursive_pair_of_constants_resolves_to_nothing`` drives
#: that pair.
MAX_HOPS = 6


def resolve_int(
    node: ast.AST | None,
    names: dict[str, ast.AST],
    members: dict[str, dict[str, ast.AST]],
    hops: int = 0,
) -> int | None:
    """The integer an expression evaluates to, through names, members and arithmetic.

    Shared by both guards on purpose. A code held in a constant is the CAREFUL
    spelling, because a bare 30 in a mapping or an exit call tells a reader
    nothing about which band it belongs to, and for one round the guards read
    only the careless one. That is a guard rewarding the wrong habit.

    ``True`` is not an integer here even though the language says it is, and a
    name that resolves to nothing resolves to nothing rather than to a guess.
    """
    if node is None or hops > MAX_HOPS:
        return None
    if isinstance(node, ast.Constant):
        # The bool exclusion is unobservable today: nothing in the tree or the
        # fixtures maps a cause to True, and the reserved range would reject
        # ``1`` anyway. Kept because the FIRST version of this guard reported
        # ``'rekordbox-running' -> bare status False``, which is the false
        # positive that got it suppressed. See R-16.
        if isinstance(node.value, bool) or not isinstance(node.value, int):
            return None
        return node.value
    if isinstance(node, ast.Name):
        return resolve_int(names.get(node.id), names, members, hops + 1)
    if isinstance(node, ast.Attribute):
        owner = _dotted(node.value) or ""
        return resolve_int(members.get(owner, {}).get(node.attr), names, members, hops + 1)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
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
        return None
    # ``int(30)`` around a plain integer. Unobservable: the only ``int(...)`` a
    # fixture writes is ``int(ExitCode.PRECONDITION)``, which ``status`` answers
    # through its own conversion branch before this is reached. Defence in depth
    # for the careful spelling, not a live path. See R-16.
    if isinstance(node, ast.Call) and _dotted(node.func) == "int" and len(node.args) == 1:
        return resolve_int(node.args[0], names, members, hops + 1)
    return None


def _within_scope(body: list[ast.stmt]):
    """Every node inside a block of statements, without entering a nested scope.

    The same rule ``_walk_scope`` below applies to one node, applied to a list of
    them. Shared rather than written twice, because "what counts as still being
    in this scope" is exactly the kind of question two copies eventually answer
    differently.
    """
    for statement in body:
        if isinstance(
            statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)
        ):
            continue
        yield statement
        yield from _walk_scope(statement)


class ReservedCodeTable:
    """Reads one source for a second opinion about what a refusal cause exits with.

    TWO SIDES HAVE TO BE RIGHT AT ONCE, and the first two versions of this guard
    got each of them wrong in a different direction.

    WHAT COUNTS AS A KEY: a string somebody DECLARED to be a cause. Three
    declarations count, and the union of them is what the caller passes in plus
    what this file says about itself:

    * a cause in the reservation table;
    * a cause the package-wide derivation found, so a module's table for its own
      brand new causes is seen the moment the module declares them;
    * a cause-shaped string this very source declares as an enum member value,
      which is what catches a module whose exception has not been written yet.

    The middle rule is why this and the completeness check now share one answer to
    "what is a cause" rather than each having its own. Keying on the RESERVED set
    alone was blind to the whole case the table exists for. Keying on the SHAPE
    alone, which is what the round before this did, fired on any kebab string
    mapped to a number in range: a logging level, a column width, a timeout, a
    retention in days, a retry budget, a schema version, or any two-element tuple
    of a label and a size. The tree holds 66 kebab-keyed pairs today and not one
    of them is a reservation.

    WHAT COUNTS AS A CODE, and this is where a guard that fires on correct code
    gets itself switched off (P7). An ``ExitCode`` member is unambiguous. So is a
    code reached through a NAME, a class attribute, a module's own ``IntEnum``
    member, or a small piece of arithmetic, all of which resolve here, because
    naming a constant is what a careful author does and the careless spelling was
    the only one the guard could read. A bare integer is ambiguous, so only the
    ones inside the RESERVED RANGE count, and the range comes from the live table
    rather than being repeated here. ``True`` and ``False`` are integers to
    ``isinstance`` and are never a status.

    THE RESIDUAL LIMIT, pinned by a fixture rather than left to be discovered: a
    backoff of 30 seconds keyed by a slug that IS a declared cause is
    indistinguishable from a reservation of 30 by shape alone, and this reports
    it. That direction was chosen deliberately, because the alternative is
    matching on the variable's name, and a guard a rename defeats is not a guard.
    The narrowing above is what makes that residual small: it can only happen for
    a string somebody already declared to be a refusal cause.
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
        self.causes = set(causes) | _declared_enum_values(tree)

    def cause_key(self, node: ast.AST | None) -> str | None:
        """The cause slug a key names, or None when nobody declared it a cause."""
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            return None
        return node.value if node.value in self.causes else None

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
        if self.codes.names_a_code(node):
            return ast.unparse(node)
        # The one-argument narrowing is unobservable: no fixture writes
        # ``int(ExitCode.X, base)`` or any other two-argument spelling, so
        # widening it kills nothing. It stays because ``ExitCode(30, "note")``
        # is not a conversion and reading its first argument as one would be a
        # false positive on somebody else's constructor. See R-16.
        if isinstance(node, ast.Call) and len(node.args) == 1:
            # ``int(ExitCode.X)`` and ``ExitCode(30)``: a code with a conversion
            # wrapped round it is still a code, and both spellings read as
            # ordinary Python rather than as an evasion.
            wraps_a_code = _dotted(node.func) == "int" or self.codes.names_the_class(node.func)
            if wraps_a_code and self.status(node.args[0], extra) is not None:
                return ast.unparse(node)
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

        This is what reads ``("tagger-art-rejected", 41, "the note")`` and
        ``Entry("tagger-art-rejected", 41, "the note")``, which is U38's own
        idiom: the reservation table in ``cli/exit_codes.py`` is a tuple of
        dataclasses, so the second module to copy the house style was the one
        shape a two-element rule could not see.

        Split rather than multiplied out, so a long tuple costs one pass rather
        than a square, and so a mapping of causes to SENTENCES contributes
        nothing on either side.
        """
        keys = [element for element in elements if self.cause_key(element)]
        values = [element for element in elements if self.status(element)]
        return [(key, value, None) for key in keys for value in values]

    def pairs(self) -> list[tuple[ast.AST, ast.AST, str | None]]:
        """Every place a key and a value are bound together, in any shape.

        Every shape below was written as an evasion first and only then as a
        rule, which is why the list is this specific.
        """
        found: list[tuple[ast.AST, ast.AST, str | None]] = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Dict):
                # A mapping literal, including the one inside ``dict(**{...})``,
                # ``MappingProxyType({...})`` and ``CODES.update({...})``. Keys
                # stay bound to THEIR value: crossing a mapping would pair a
                # cause whose value is a sentence with an unrelated number.
                for key, value in zip(node.keys, node.values):
                    if key is not None:
                        found.append((key, value, None))
            elif isinstance(node, (ast.Tuple, ast.List)):
                found.extend(self._crossed(list(node.elts)))
            elif isinstance(node, ast.DictComp):
                # ``{slug: 30 for slug in (...)}``: the value is the code and
                # every slug in the iterables is a key it is given to.
                for generator in node.generators:
                    for element in ast.walk(generator.iter):
                        if isinstance(element, ast.Constant):
                            found.append((element, node.value, None))
            elif isinstance(node, ast.Assign):
                # ``CODES[slug] = 30`` after ``CODES = {}``, which is a table
                # built a line at a time and is a table all the same.
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
                    # Redundant since the catch-all below started crossing every
                    # call's arguments, which reaches ``setdefault`` too.
                    # Deleting it kills nothing. Kept because it binds the key to
                    # ITS value by position rather than crossing them, so a
                    # three-argument call cannot pair the wrong two. See R-16.
                    found.append((node.args[0], node.args[1], None))
                elif _dotted(function) in {"dict", "OrderedDict"} and len(node.args) == 1:
                    found.extend(self._zipped(node.args[0]))
                else:
                    # Any other call, because a reservation built by a
                    # constructor is a reservation. Argument order is not assumed.
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

        Narrowed to what the branch RETURNS. A module that waits 30 seconds
        inside a branch and does not return it is doing something ordinary, and a
        guard that reported it would be the false positive that gets the whole
        check suppressed.

        The returned expression is resolved through the branch's OWN locals, so
        ``code = 41`` then ``return code`` reads the same as ``return 41``.
        Without that, the two sides of this guard swapped on a spelling that has
        nothing to do with what the code means.
        """
        found: list[tuple[ast.AST, ast.AST, str | None]] = []
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

    def _returned(
        self, keys: list[ast.AST], body: list[ast.stmt]
    ) -> list[tuple[ast.AST, ast.AST, str | None]]:
        """What a branch returns, at ANY depth inside it.

        Reading the body's top level alone was one indent from silence, and no
        evasion was needed to reach it: a branch that checks something else
        before returning is the ordinary way to write the second case of a table,
        and ``if c == "rclone-missing": if ready: return 30`` reported nothing
        while the flat spelling reported it. A guard that a plain ``if`` defeats
        is a guard that is off.

        A nested def, class or lambda is NOT entered, because a function declared
        inside the branch has its own scope and its own returns, and attributing
        them to the branch's key would be the false positive that gets this
        suppressed.
        """
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

    A second table is how two answers to one question appear, and the repository
    has already paid for that shape once in its taxonomy resolvers. The class
    above carries the reasoning for what counts as a key and what counts as a
    code; this function is the walk over every shape a table can be written in.

    Deliberately NOT restricted to dict literals, which is what the first version
    was while its docstring claimed otherwise, and not to two-element pairs,
    which is what the second was while the file it protects declares its own
    table as a tuple of three-field dataclasses.

    ``package`` is the dotted package the source sits in, and it is what lets a
    relative import be resolved rather than pattern matched. A caller scanning
    real files knows it and passes it; a caller holding a source string does not,
    and ``ExitCodeImports`` says what it falls back to.
    """
    table = ReservedCodeTable(ast.parse(source), causes, code_range, package)
    found: list[str] = []
    seen: set[tuple[int, str, str]] = set()
    for key, value, label in table.pairs():
        slug = table.cause_key(key)
        if slug is None:
            continue
        # A branch return carries its label already, because proving it needed
        # that branch's own locals and they are out of scope here.
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

#: The standard-library modules that can end a process, and the attribute of each
#: that does it. Held by module IDENTITY rather than by the name a source bound,
#: so ``import sys as system``, ``system = sys`` and ``os.sys`` are one question.
EXIT_ATTRIBUTES = {"sys": "exit", "os": "_exit"}

#: Modules recognized by identity for any purpose here.
TRACKED_MODULES = frozenset({"sys", "os", "builtins", "importlib"})


def _walk_scope(node: ast.AST):
    """Every node in ONE lexical scope, not entering a nested def, class or lambda.

    Scope matters because a binding is not a property of a file. A module-level
    ``stop = sys.exit`` makes ``stop`` an exit inside the functions that inherit
    it and NOT inside a function that takes a parameter of the same name, and a
    guard that walked the whole module fired on the second.
    """
    stack = list(ast.iter_child_nodes(node))
    while stack:
        current = stack.pop()
        yield current
        if isinstance(
            current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)
        ):
            continue
        stack.extend(ast.iter_child_nodes(current))


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

    Bound by module IDENTITY, never by the text of a name, because every shape
    below is ordinary Python that somebody would write without meaning to evade
    anything::

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

    The ``getattr`` shape is the one that matters most, because it disarms the
    guard on its own and reads as perfectly innocent. Resolution runs to a fixed
    point, so mutual and multi-hop aliases both settle whatever order they are
    written in.
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
            if identity in EXIT_ATTRIBUTES and node.attr == EXIT_ATTRIBUTES[identity]:
                return True
            return (_dotted(node) or "") in self.exits
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
            if self.module_identity(node.value) == "builtins" and node.attr == "SystemExit":
                return True
            return (_dotted(node) or "") in self.statuses
        if isinstance(node, ast.Call):
            identity, attribute = self._fetched(node)
            return identity == "builtins" and attribute == "SystemExit"
        return False

    def ends_the_process(self, node: ast.AST) -> bool:
        return self._is_exit(node) or self._is_status(node)


def process_status_literals(source: str) -> list[str]:
    """Every place this source turns a bare integer into a process status.

    ``sys.exit(21)`` bypasses the whole vocabulary: nothing imports, nothing
    looks anything up, and the integer arrives at the shell meaning whatever the
    author believed that day. Every name is bound through the import graph and
    resolved by module identity, so every spelling ``ProcessExits`` lists is
    caught and ``runner.exit(21)`` on somebody's own object is not.

    THE STATUS IS RESOLVED, not just read. ``PRECONDITION = 30`` then
    ``sys.exit(PRECONDITION)`` is the same bare integer reaching the same shell,
    spelled the way a careful author spells it, and reading only the inlined
    literal meant the guard rewarded the careless spelling. Names resolve through
    the scope they are read in, so a parameter shadowing a module constant
    resolves to nothing, which is what it is.

    Zero is excluded. ``sys.exit(0)`` is success spelled plainly and is not a
    refusal, and reporting it would be the false positive that gets the whole
    guard suppressed. ``True`` is excluded for the same reason and a stronger
    one: it is an integer only by accident of the language. A status this cannot
    evaluate stays silent: ``sys.exit(int(code_for(cause)))`` is the sanctioned
    path and reports nothing.
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
