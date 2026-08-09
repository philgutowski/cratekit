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

#: The module every question here is asked about. The package it lives in, which
#: is what ``from cratekit.core import review`` names, is DERIVED from this
#: rather than written out a second time. It was a second constant until the
#: residual "Two copies of one import walk still carry a relative-import defect",
#: and two spellings of one fact is how a pair drifts.
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


class ReviewImports:
    """How one source file reaches the review module, if it reaches it at all.

    Three shapes are recognized, and they are the three this repository's own
    modules use between them::

        import cratekit.core.review            # cratekit.core.review.offer(...)
        import cratekit.core.review as rv      # rv.offer(...)
        from cratekit.core import review       # review.offer(...)
        from cratekit.core.review import offer # offer(...)

    A relative import is recognized too, and until the residual
    "Two copies of one import walk still carry a relative-import defect" was fixed only ONE of
    the three relative spellings was. The rule read ``node.level > 0`` beside a
    two-element suffix match on ``node.module``, and ``node.module`` holds only
    the TAIL: ``from .review import offer`` records ``review`` and ``from .
    import review`` records nothing at all, so the two spellings a file sitting
    BESIDE the review module would actually use were the two that matched
    nothing. Every question in this file returns early when the source does not
    reach the module, so those sources were answered no rather than answered
    wrong, which is the silence a green suite cannot show you.

    ``_import_targets`` answers it now, resolving ``node.level`` against the
    importing file's package the way CPython's ``_resolve_name`` does when the
    caller knows that package, and reading the tail when it does not. No caller
    of this class knows it today, so the fallback is the live path here and the
    resolved one is driven by U38's suite; the exit-code walk lower down passes
    a real package on every file it scans.

    THE FIX SHIPPED WITH NOTHING WATCHING IT for one round. Reverting these four
    lines to the suffix match killed no test at all, because no fixture anywhere
    in ``tests/`` contained ``from .review import`` or ``from . import review``:
    the whole exit-code half of the same unification was driven and the review
    half was not, in the file whose thesis is that a guard answering "no"
    instead of "wrong" is the defect. ``test_review_queue.py`` now drives every
    relative spelling against both a resolving package and a non-resolving one.
    """

    def __init__(self, tree: ast.AST, package: str | None = None) -> None:
        #: Local names that ARE the module.
        self.module_names: set[str] = set()
        #: Local name -> the module attribute it was imported as.
        self.symbols: dict[str, str] = {}
        # DERIVED HERE RATHER THAN SPELLED AGAIN, and derived at USE rather than
        # at import. That residual deleted the second spelling of the package
        # and left the
        # LEAF written out as ``"review"`` one line below the resolver, so moving
        # ``REVIEW_MODULE`` moved the resolver and left the binding behind: the
        # same one fact in two spellings, which is the drift it says it closed.
        # Reading it inside the walk is what lets a test move the constant and
        # watch BOTH halves follow.
        leaf = REVIEW_MODULE.rpartition(".")[2]
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == REVIEW_MODULE:
                        self.module_names.add(alias.asname or REVIEW_MODULE)
            elif isinstance(node, ast.ImportFrom):
                names_the_module, names_the_package = _import_targets(
                    node, REVIEW_MODULE, package
                )
                if names_the_module:
                    for alias in node.names:
                        self.symbols[alias.asname or alias.name] = alias.name
                elif names_the_package:
                    for alias in node.names:
                        if alias.name == leaf:
                            self.module_names.add(alias.asname or leaf)

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


def calls_review(source: str, wanted: str, package: str | None = None) -> bool:
    """Whether this source CALLS the review module's ``wanted`` function.

    ``package`` is the dotted package the source sits in, which is what lets a
    relative import be RESOLVED rather than pattern matched. A caller holding
    only a source string does not know it; ``ReviewImports`` says what it falls
    back to.
    """
    tree = ast.parse(source)
    imports = ReviewImports(tree, package)
    if not imports.reaches_review:
        return False
    return any(
        isinstance(node, ast.Call) and imports.resolves(node.func, wanted)
        for node in ast.walk(tree)
    )


def offers_into(source: str, queue: str, package: str | None = None) -> bool:
    """Whether a review ``offer`` call is given the review queue named by ``queue``.

    The queue has to reach the CALL. An assignment naming the queue and going
    nowhere is what a module writes when somebody wanted the countdown to pass,
    and it is indistinguishable from a comment. One hop of indirection is
    accepted, because ``QUEUE = review.Queue.VERSION_MATCH`` at module level and
    ``queue=QUEUE`` at the call is ordinary correct code.
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


def constructs_review(source: str, wanted: str, package: str | None = None) -> bool:
    """Whether this source CONSTRUCTS the review module's ``wanted`` class."""
    return calls_review(source, wanted, package)


def methods_on_review_construction(
    source: str, wanted: str, package: str | None = None
) -> set[str]:
    """Method names called on something this source built from review's ``wanted``.

    The receiver is traced rather than assumed, through the three shapes a real
    module uses: a local variable, a field on an object, and a small helper that
    returns one. A method called on anything else is not counted, which is what
    stops an unrelated class with a method of the same name from answering for
    the store.
    """
    tree = ast.parse(source)
    imports = ReviewImports(tree, package)
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

#: The module that owns the status vocabulary. As with ``REVIEW_MODULE``, the
#: package it sits in AND its leaf are derived from this rather than spelled a
#: second time, and both are derived at use so a test can move the constant and
#: watch every question here follow it.
EXIT_CODE_MODULE = "cratekit.core.exit_codes"

#: The class inside that module that IS the vocabulary. A separate fact from the
#: module, so it gets its own name rather than four string literals scattered
#: through two methods and a constructor.
EXIT_CODE_CLASS = "ExitCode"

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

    THE OFF THE TOP CLAUSE IS NOT DEFENSIVE PADDING. Python's slicing is
    forgiving where an import is not: with a package of ``cratekit.core.sub``
    and five dots, ``len(parts) - (node.level - 1)`` is ``-1``, and ``parts[:-1]``
    quietly hands back ``cratekit.core``, so the walk would resolve an import
    the interpreter refuses outright onto the very module it is hunting and
    REPORT an offender that cannot exist.
    ``test_a_relative_import_that_walks_off_the_top_names_nothing`` drives that
    case. The assertion that used to claim it, two dots from ``cratekit``,
    proved nothing: the short base it leaves behind matches nothing either way.
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

    ONE implementation for both walks in this file, and the residual
    "Two copies of one import walk still carry a relative-import defect" is why. The same
    question was answered twice here and the two answers disagreed about
    relative imports: one resolved the level and the other matched a two-element
    suffix that ``from .review import offer`` does not have and ``from . import
    review`` does not have either. Two answers to "does this source reach that
    module" is exactly the drift these guards exist to report in other people's
    code.

    Resolved against the importer's package when the caller knows it, which is
    the whole tree scan, so ``from . import exit_codes`` inside ``cli`` resolves
    to the reservation table and stays out exactly as its absolute spelling
    does.

    The fallback, for a source with no path, matches the TAIL and accepts a bare
    sibling. A fixture is a file that could be anywhere, so the only honest
    reading of ``from .exit_codes import ExitCode`` there is that it names a
    module called ``exit_codes``. ``node.module`` is None for ``from . import
    X``, which names the package and nothing else, and reading that None as an
    empty string is how the shape went missing.
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

    U12 COORDINATION. This is the same walk ``ReviewImports`` does, asked about
    a different module, and the relative half of it is now literally shared:
    both call ``_import_targets``. U12 is generalizing ``ReviewImports`` into a
    module-parameterized ``ImportsOf`` on its own branch, and the conformance
    branch has a third copy as ``SoftDeleteNames``. All three merge textually
    clean in any order, so nothing will flag it. When they land together, this
    class collapses into ``ImportsOf(tree, EXIT_CODE_MODULE)`` with one
    narrowing, because this one records only the ``ExitCode`` symbol where
    ``ImportsOf`` records every symbol a source imported, and ``SoftDeleteNames``
    collapses the same way. THE COLLAPSE HAS TO TAKE ``_import_targets`` WITH IT.
    The two copies on the other branches still carry the suffix match this file
    has now replaced in both of its own, and a collapse onto either of them
    would reinstate the defect in one place instead of two. The residual
    "Two copies of one import walk still carry a relative-import defect" records that.

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
        leaf = EXIT_CODE_MODULE.rpartition(".")[2]
        for node in ast.walk(tree):
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
        # The module-qualified spelling, ``exit_codes.ExitCode(30)``. Round three
        # called this unreachable; it is ordinary Python that no fixture happened
        # to write, which is a different thing and the difference is the whole
        # point of the residual "One check in this unit is unreachable".
        # ``EVASION_A_CONVERSION_THROUGH_THE_MODULE_NAME`` writes
        # it now: without this branch the call is not a conversion, the guard
        # falls through to resolving a ``Call`` as an integer, gets nothing, and
        # says nothing about a module that reserved 30 for a reserved cause.
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


#: The names the standard library's ``enum`` module binds that a vocabulary is
#: built on. ``Flag`` and ``IntFlag`` are in it and neither ends in ``Enum``,
#: which is the whole reason this set exists beside the spelling rule below.
ENUM_BASES = frozenset(
    {"Enum", "StrEnum", "IntEnum", "IntFlag", "Flag", "ReprEnum"}
)


def _enum_bases(tree: ast.AST) -> set[str]:
    """Every local name in this source that IS a base out of the ``enum`` module.

    Bound through the import graph, which is the rule every other question in
    this file already follows: ``from enum import StrEnum as Vocabulary`` binds
    the base to ``Vocabulary``, and a classification that read only the text of
    the base would be defeated by that one ``as`` keyword. That is the exact
    failure this file reports in other people's code, so it is not one this file
    may keep.

    ``import enum as e`` binds every base as ``e.<name>``, which is why the
    module spelling is expanded here rather than special-cased at the use.
    """
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "enum":
                    module = alias.asname or "enum"
                    found.update(f"{module}.{base}" for base in ENUM_BASES)
        elif isinstance(node, ast.ImportFrom):
            if node.level or node.module != "enum":
                continue
            for alias in node.names:
                if alias.name in ENUM_BASES:
                    found.add(alias.asname or alias.name)
    return found


def _declared_enum_values(tree: ast.AST) -> set[str]:
    """Every cause-shaped string this source declares as an enum member value.

    This is the DECLARATION half of the key test. A module that writes
    ``ART_REJECTED = "tagger-art-rejected"`` inside an enum has declared that
    string to be one of its causes, in its own file, before anybody reserved it.
    Mapping that same string to a status somewhere else in the same file is a
    reservation whoever wrote it, and no registry has to have heard of it.

    MATCHED ON THE BASE AND NEVER ON THE CLASS OR THE VARIABLE, so renaming
    either changes nothing, and ``test_an_enum_is_read_by_its_base_and_not_by
    _its_name`` drives both renames rather than asserting them.

    THE BASE IS MATCHED TWO WAYS AND THE RECORD SAID ONE, which is the correction
    this round makes. The rule was a SPELLING, ``endswith("Enum")``, described as
    "how Python spells an enum" and set against a rename-defeatable rule while
    being one: ``from enum import StrEnum as Vocabulary`` defeated it outright,
    and ``Flag`` and ``IntFlag`` are enum bases whose spelling it never matched.
    Worse, the spelling could not be TOLD APART from an exact list of the three
    base names the suite happened to use: narrowing it to
    ``{"Enum", "StrEnum", "IntEnum"}`` killed zero of 3379.

    So there are two clauses now and each has a fixture that only it answers:

    * a name this source BOUND from the ``enum`` module, in any spelling, which
      is the clause an aliased import needs and the clause ``Flag`` needs;
    * a base whose spelling ends in ``Enum``, which is the clause a base defined
      in ANOTHER of our modules needs, since no import of ``enum`` appears in the
      subclassing file at all.

    WHAT IS STILL NOT READ, said rather than left to be found: a base from
    another module whose name neither ends in ``Enum`` nor is one the ``enum``
    module exports, ``class Cause(Vocabulary)`` against our own
    ``class Vocabulary(StrEnum)`` next door. Reading that needs the base's OTHER
    file, which no question in this file opens. The package holds no such base
    today and ``test_no_module_declares_a_vocabulary_on_a_base_this_cannot_read``
    measures that against the tree rather than assuming it.
    """
    bound = _enum_bases(tree)
    found: set[str] = set()
    for node in ast.walk(tree):
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
#: THREE, and three is the depth of the deepest spelling this guard promises to
#: read: ``BASE = 30`` then ``OFFSET = BASE`` then ``OFFSET + 1``, which costs a
#: hop for each name and one for the arithmetic. It was six, with a docstring
#: claiming that "lowering it kills seven tests". Measured across the whole
#: suite, a full sweep of every lower value: 0 kills nine, 1 kills two, and 2, 3,
#: 4 and 5 each kill NOTHING. No lowering killed seven and the constant was over
#: provisioned by four, so the claim was checkable and wrong at every value,
#: which is the class of claim the residual
#: "One check in this unit is unreachable" exists to delete.
#:
#: LOAD BEARING IN BOTH DIRECTIONS, and now driven at the value rather than
#: argued about. ``test_the_hop_bound_is_the_depth_of_the_deepest_spelling``
#: asserts the deepest fixture resolves AT this number and goes silent one below
#: it, so changing the constant alone fails. Raising it past the interpreter's
#: own recursion limit turns ``A = B`` beside ``B = A`` from a silent None into a
#: ``RecursionError`` that takes the suite with it, which is the hang this
#: constant exists to prevent, so
#: ``test_a_mutually_recursive_pair_of_constants_resolves_to_nothing`` drives
#: that pair.
#:
#: WHAT THREE GIVES UP, said rather than implied, because the reduction from six
#: was justified with "nothing in the suite needed more than two hops" and that
#: is absence read as evidence of absence applied to a COVERAGE DIAL. This is not
#: a correctness constant. Any finite value below the recursion limit stops the
#: hang; the value decides how long a chain of aliases the guard can read. At
#: three it reads at most TWO aliases before the literal, so this is reported::
#:
#:     A0 = 30
#:     A1 = A0
#:     CODES = {"config-unusable": A1}
#:
#: and this is SILENT, which is the cost of the number and not a property of the
#: guard::
#:
#:     A0 = 30
#:     A1 = A0
#:     A2 = A1
#:     A3 = A2
#:     CODES = {"config-unusable": A3}
#:
#: MEASURED AT EVERY VALUE, so the boundary is a number rather than a guess. The
#: two alias chain is reported at 2, 3, 4, 5 and 6. The three alias chain is
#: SILENT at 2 and 3 and reported at 4, 5 and 6, so the boundary this constant
#: sets sits exactly between 3 and 4.
#: ``test_the_hop_bound_is_a_coverage_dial_and_this_is_what_it_gives_up`` pins
#: both, so the silence is a fixture somebody has to look at rather than a hole
#: nobody has met, and raising the constant to reach further fails that test and
#: demands the new boundary be written down the same way.
MAX_HOPS = 3


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
        # THE BOOL EXCLUSION RUNS, and round three's comment here said it did
        # not. ``CORRECT_A_RETRY_FLAG_PER_CAUSE`` maps a cause to ``True`` and
        # another to ``False``, and instrumenting this line counted 464 booleans
        # arriving in one suite run. What is true is that it changes no OUTCOME
        # today, because ``True`` is 1 and ``False`` is 0 and the reserved range
        # starts at 10, which is a fact about the range rather than about this
        # line. ``test_a_boolean_is_not_an_integer_here`` asserts the answer
        # directly, so the line is covered rather than merely reasoned about.
        if isinstance(node.value, bool) or not isinstance(node.value, int):
            return None
        return node.value
    if isinstance(node, ast.Name):
        return resolve_int(names.get(node.id), names, members, hops + 1)
    if isinstance(node, ast.Attribute):
        owner = _dotted(node.value) or ""
        return resolve_int(members.get(owner, {}).get(node.attr), names, members, hops + 1)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        # THE ONLY THING THAT READS A NEGATIVE, and for six rounds nothing drove
        # it. Deleting this branch leaves ``sys.exit(-1)`` resolving to nothing,
        # which is silence on the one bare status that reaches the shell as 255
        # and reaches the job engine's ``returncode`` as a signal death. It
        # changes no answer on the reservation side, where a negative is outside
        # the reserved range either way, so the bare-status guard is the whole of
        # what this branch is for. See the residual
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
        # ``//`` and ``%`` complete the set rather than extending it. A guard
        # that reads ``BASE + 3`` and ``BASE * 2`` and goes silent on
        # ``BASE // 2`` is answering the same question two ways, which is the
        # defect this whole file reports in other people's code. Division by zero
        # is a source that does not run, so it resolves to nothing rather than
        # raising inside a test.
        if isinstance(node.op, (ast.FloorDiv, ast.Mod)) and right != 0:
            return left // right if isinstance(node.op, ast.FloorDiv) else left % right
        return None
    # ``int(30)`` around a plain integer, and this is a LIVE path that round
    # three called unreachable. The builtin is matched by the TEXT of its name
    # here and in five other rules in this file, which is the shape this file
    # forbids elsewhere; the residual
    # "Six of this unit's own rules recognize a builtin by the text of its name"
    # carries it with the measurement that no package module aliases one. ``process_status_literals`` resolves the
    # argument of every single-argument call it walks, so ``sys.exit(int(code))``
    # arrives here rather than at ``status``'s conversion branch, and
    # instrumenting the line counted 25 arrivals in one suite run. Without it a
    # module ending the process with ``sys.exit(int(PRECONDITION))`` resolves to
    # nothing and the bare status guard goes quiet on a real bypass, which is
    # what ``EVASION_A_STATUS_WITH_A_CONVERSION_ROUND_IT`` now drives.
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


#: THERE IS NO PER-LINE OFF SWITCH, and its absence is a decision this round
#: measured rather than a gap. The round before shipped
#: ``# not-a-reservation: <reason>`` and claimed three things about it: that it
#: silenced one statement, that it was never a ``def`` body, and that its blast
#: radius was visible from where it was written. Measured, all three were false.
#: ``def build(): return {"config-unusable": 30}  # not-a-reservation: honest``
#: silenced the body, because the mark and the body are one physical line and
#: ``pyproject.toml`` selects ``E9``, ``F`` and ``I`` only, so ``ruff`` never
#: fails a one line ``def``. ``A = {...}; B = {...}`` on one line silenced BOTH
#: statements on one reason. And one comment appended to the opening line of
#: ``core/cause.py``'s registry silenced all SIXTY ONE of its reservations, with
#: the furthest silenced line 214 below the mark, while the failure message
#: reported only the line and the reason and never how many went quiet.
#:
#: WHAT REPLACES IT IS THE MEASUREMENT THAT MADE IT UNNECESSARY. The hatch was
#: sold as the thing that makes a false alarm cheap, and it was never used once.
#: The package has ZERO offenders outside the two table owners, and it still has
#: zero when every kebab shaped string literal in the package is added to the key
#: set: 189 distinct literals, 108 of them not keys today. The wide rule has no
#: headroom problem in this tree, so the hatch bought nothing and could switch the
#: guard off for a whole registry with one comment.
#:
#: The residual is still real and still REPORTED: ordinary data keyed on a cause
#: slug with an in-range integer reads as a reservation by shape alone. The answer
#: to it is a REVIEW rather than a comment anybody can write. If a module ever
#: meets it, either the value is a reservation and belongs in the table, or the
#: file joins ``TABLE_OWNERS`` with a reason beside it and the exact-membership
#: assertion updated, which is the review a silenced guard never gets otherwise.
#: ``test_a_comment_cannot_silence_a_reservation`` drives the ABSENCE against the
#: whole residual fixture, so reinstating any per-line escape fails rather than
#: passing quietly.


class ReservedCodeTable:
    """Reads one source for a second opinion about what a refusal cause exits with.

    ONE KEY SET AND ONE VALUE RULE. Every string anybody in this repository has
    declared to be a refusal cause is a key, all eighty two of them, and any of
    them beside a status is a reservation: an ``ExitCode`` member in any import
    spelling, a conversion round one, a code held in a name, a class attribute,
    a module's own ``IntEnum`` member, a small piece of arithmetic, or a bare
    integer inside the reserved range.

    THE ROUND BEFORE THIS SPLIT THE KEYS INTO TWO TIERS AND THE SPLIT WAS BOUGHT
    WITH A NUMBER THAT DOES NOT EXIST. The justification was that the wide rule
    reported "twenty seven of twenty eight ordinary constructs". That count came
    from a hand written fixture, not from this repository. Measured over the 51
    files ``package_sources`` returns, 43 modules and 8 package ``__init__.py``,
    under the wide rule: ZERO offenders outside the two files that own a table.
    The over fire the tiers were built to stop does not occur here, and it does
    not appear when the key set is widened either: adding every kebab shaped
    string literal in the package, 189 distinct with 108 that are not keys today,
    still measures ZERO offenders outside the two owners.

    WHAT THE TIERS COST, MEASURED AGAINST THE FIXTURE TUPLE THIS FILE SHIPS. Of
    the sixteen realistic second-reservation shapes keyed on registry-only slugs
    in ``REGISTRY_SLUG_SECOND_TABLES``, round four's tiers report TWO and are
    silent on FOURTEEN. The two they report are a named code and a conversion.
    They are blind to a module declaring its own ``IntEnum`` of statuses, to
    ``ExitCode(30)`` and its module-qualified spelling, to a named constant, to
    arithmetic, and to every table shape this file already proves for the other
    twenty two keys, for sixty of the eighty two keys.

    SO THE TRADE RUNS THE OTHER WAY, and it runs on the error costs rather than
    on a preference. A false alarm costs one developer one look and a decision
    that is recorded: either the value is a reservation and belongs in the table,
    or the file joins ``TABLE_OWNERS`` with a reason and an updated membership
    assertion. A miss is a module quietly disagreeing with the registry about
    what a refusal exits with, which is the defect this guard is the only thing
    watching for. For a guard of this shape the loud direction is the correct
    one. The round before bought the loud direction with a per-line comment that
    could switch off sixty one reservations at once; the comment is gone and the
    measurement above is why nothing had to replace it.

    WHAT COUNTS AS A CODE, and this is where a guard that fires on correct code
    gets itself switched off (P7). An ``ExitCode`` member is unambiguous, in any
    spelling, through a bounded chain of names, and through ``getattr`` on the
    class: ``CODE = ExitCode.PRECONDITION`` beside ``{"rclone-missing": CODE}``
    is what a careful author writes, and both tiers of the round before were
    blind to it while this class's own docstring claimed it resolved. A bare
    integer is ambiguous, so only the ones inside the RESERVED RANGE count, and
    the range comes from the live table rather than being repeated here. ``True``
    and ``False`` are integers to ``isinstance`` and are never a status.

    THE KEY IS RESOLVED THROUGH NAMES TOO, and for one round it was not. The
    value side chased a code through module constants and class attributes on the
    argument that "a bare 30 in a mapping tells a reader nothing", which is a
    reason to read the careful spelling. The identical argument holds for the
    key: ``CONFIG_UNUSABLE = "config-unusable"`` beside ``{CONFIG_UNUSABLE: 30}``
    is the same table, and ``{Slug.CONFIG_UNUSABLE: 30}`` is the same table with a
    namespace round it. The package already carries 37 class attributes whose
    value is a declared cause, so this is the spelling in the tree rather than an
    invented one, and both were SILENT.

    ONE MACHINERY ANSWERS BOTH SIDES, and saying so was premature by one round.
    The widening reached four constructs and missed two: ``cause_keys_within``
    exists because ``case Slug.CONFIG_UNUSABLE`` was reported while its direct
    twin ``if cause == Slug.CONFIG_UNUSABLE`` was silent, and a dict
    comprehension over named slugs was silent while the same comprehension over
    inlined slugs was reported. Every construct that finds its keys in a subtree
    asks one method now, so the claim is a structure rather than a sentence.

    WHAT THE RANGE GATES AND WHAT IT DOES NOT, because the record had this wrong
    in three of four clauses. An ``ExitCode`` member and a conversion wrapped
    round the vocabulary are the vocabulary at ANY value, in range or out. A bare
    integer, a named constant holding one and arithmetic producing one are all
    the same thing to this guard, an INTEGER, and all three are reported only
    inside the reserved range. Arithmetic can produce nothing but an integer, so
    "arithmetic reaching an out of range value is still reported" was
    unconditionally false and is not claimed.

    NOT NARROWED TO THE EIGHTEEN INTEGERS THE ENUM ACTUALLY USES, which was the
    other candidate. The case this table exists for is a new module deciding its
    OWN codes, and a module inventing 33 for a cause nobody reserved is precisely
    that case. That rejection is honest now: under the tiers,
    ``{"tree-registry-unusable": 33}`` was NOT reported either, so the shipped
    scheme was rejecting an alternative for a hole it had itself.

    THE RESIDUAL LIMIT, pinned by fixtures rather than left to be discovered: a
    poll interval, a column width or a schema version keyed by a cause slug is
    indistinguishable from a reservation by shape alone, and this reports it.
    That direction was chosen deliberately, because the alternative is matching
    on the variable's name, and a guard a rename defeats is not a guard. The
    answer to it is a decision recorded in the suite, not a comment: see the note
    above ``ReservedCodeTable`` for why the per-line escape was deleted.

    WHAT IS STILL SILENT IS WRITTEN DOWN RATHER THAN LEFT TO BE FOUND. Seventeen
    realistic shapes have been measured against this guard and every one was
    silent when it was found; NINE are closed here and the residual
    "The tiers were bought with a number that does not exist" carries the other
    eight with the reason each is recorded rather than closed. The enumeration
    grew from fourteen to seventeen the round after it was written down as
    complete, which is the argument for writing it down: a gap nobody wrote down
    is a gap nobody reviews.
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
        #: Every string somebody declared a refusal cause, plus whatever THIS
        #: source declares in an enum of its own.
        self.causes = set(causes) | _declared_enum_values(tree)

    def cause_key(self, node: ast.AST | None) -> str | None:
        """The cause slug a key names, or None when nobody declared it a cause.

        THROUGH NAMES, the same way the VALUE side reads a code. Requiring an
        ``ast.Constant`` here was the largest hole this guard had: the value rule
        chases a code through module constants, class attributes and a module's
        own enum on the argument that a bare integer "tells a reader nothing",
        and the identical argument holds for the key. Measured, both of these
        gave zero hits while their inlined spelling gave one::

            CONFIG_UNUSABLE = "config-unusable"
            CODES = {CONFIG_UNUSABLE: 30}

            class Slug:
                CONFIG_UNUSABLE = "config-unusable"
            CODES = {Slug.CONFIG_UNUSABLE: 30}

        A name that does not resolve to a declared cause answers None exactly as
        an undeclared literal does, so this widens what the guard can READ and
        not what it treats as a cause.
        """
        held = self._resolved(node)
        if not (isinstance(held, ast.Constant) and isinstance(held.value, str)):
            return None
        return held.value if held.value in self.causes else None

    def cause_keys_within(self, node: ast.AST) -> list[ast.AST]:
        """Every expression anywhere inside ``node`` that names a declared cause.

        ONE FILTER FOR EVERY CONSTRUCT THAT HOLDS ITS KEYS IN A SUBTREE, and
        having three was how one question got two answers inside one method. The
        round before widened ``cause_key`` to read a name, and three callers
        reached it through a subtree: the ``match`` arm passed ``pattern.value``
        straight in and INHERITED the widening, while the ``if`` arm and the
        dict comprehension's iterable each pre-filtered the subtree to
        ``ast.Constant`` and did not. Measured on the shipped tree before this
        method existed::

            match cause:
                case Slug.CONFIG_UNUSABLE: return 30      # REPORTED
            if cause == Slug.CONFIG_UNUSABLE: return 30   # SILENT
            if cause == CONFIG_UNUSABLE:      return 30   # SILENT
            if cause == "config-unusable":    return 30   # REPORTED
            {slug: 30 for slug in (CONFIG_UNUSABLE, SMOKE)}   # SILENT
            {slug: 30 for slug in ("config-unusable", ...)}   # REPORTED

        The first pair is the same table written two ways, and the guard read one
        of them. Every construct that finds its keys in a subtree now asks this,
        so widening what a key can be widens all of them at once or none of them.

        A node that is not a cause answers nothing, exactly as an undeclared
        literal does, so this reads more spellings rather than treating more
        strings as causes.
        """
        return [element for element in ast.walk(node) if self.cause_key(element)]

    def _resolved(self, node: ast.AST | None) -> ast.AST | None:
        """A key expression reduced to what it holds: a name or a class attribute.

        Shares ``_through_names``'s bound rather than carrying a second one, so
        "how far does this guard chase a name" has one answer for both halves of
        a pair. ``Slug.CONFIG_UNUSABLE`` reads ``_class_level_literals``, which is
        the same table the value side reads for a module's own ``IntEnum``.
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

        ``resolve_int`` chases names to an INTEGER, which is why an imported
        ``ExitCode`` member behind a constant fell through both halves of the
        round before: its attribute branch reads ``_class_level_literals``, which
        only records classes defined in THIS source, so a member of an imported
        enum resolved to nothing and the pair went unreported. That is not an
        evasion anybody has to intend. It is the spelling a careful author
        reaches for, and the class docstring claimed it resolved.

        Chasing to an EXPRESSION first, and asking the import walk about what
        comes back, answers the named constant and the ``code = ExitCode.X`` then
        ``return code`` shape with the same three lines.
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
        # THROUGH NAMES FIRST. ``CODE = ExitCode.PRECONDITION`` beside
        # ``{"rclone-missing": CODE}`` is the careful spelling of the
        # unambiguous one, and it resolved to nothing for three rounds while the
        # docstring above said it resolved. The reported text keeps BOTH
        # spellings, because "which name held it" is the first thing a reader
        # chasing the hit needs.
        held = self._through_names(node, extra)
        as_written = spelled if held is node else f"{ast.unparse(held)} as {spelled}"
        if self.codes.names_a_code(held):
            return as_written
        # THE ONE-ARGUMENT NARROWING IS WHAT KEEPS THIS OFF SOMEBODY ELSE'S
        # CONSTRUCTOR. A two-argument call is not a conversion, so its first
        # argument is not a status: ``ExitCode(30, "the note")`` is a
        # constructor taking a code and a sentence, and reading the 30 out of it
        # would report a module that reserved nothing. Round three's comment
        # here claimed the narrowing was unreachable and that widening it killed
        # nothing; both halves were wrong in the useful direction, and
        # ``test_a_two_argument_call_is_not_a_conversion`` now drives it.
        if isinstance(held, ast.Call) and len(held.args) == 1:
            # ``ExitCode(0)``: a one-argument call on the vocabulary CLASS is the
            # constructor spelling of a member, so the RESERVED RANGE does not
            # gate it, exactly as ``ExitCode.SUCCESS`` is not gated. It was gated
            # for a round, because this branch only returned when the inner
            # expression was already a status, and an out-of-range integer is
            # not one. Measured on the shipped tree,
            # ``{"config-unusable": ExitCode.SUCCESS}`` was reported and
            # ``{"config-unusable": ExitCode(0)}`` was silent, which is one
            # vocabulary read two ways on the spelling alone. Narrowed to an
            # argument that RESOLVES to an integer, so ``ExitCode(result.code)``
            # is somebody reading a runtime value and is not a reservation.
            if self.codes.names_the_class(held.func):
                if self._as_int(held.args[0], extra) is not None:
                    return as_written
            # ``int(ExitCode.X)``: a conversion is a code only when what it wraps
            # is one. ``int(5)`` is the bare-integer rule's business, not this
            # branch's.
            if _dotted(held.func) == "int" and self.status(held.args[0], extra) is not None:
                return as_written
        # ``getattr(ExitCode, "PRECONDITION")``, which is the vocabulary reached
        # by a string rather than by an attribute. The bare-status guard below
        # has recognized ``getattr(sys, "exit")`` since round two and called it
        # "the one that matters most, because it disarms the guard on its own";
        # this half of the same file did not recognize the same shape, which is
        # the two-answers-to-one-question defect inside one module. Narrowed to a
        # constant attribute name on the class this source imported, so
        # ``getattr(somebody_else, "PRECONDITION")`` is not a code.
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
                # A RECORD written as a mapping, which is the house style with a
                # dict instead of a dataclass::
                #
                #     [{"cause": "config-unusable", "code": 30}, ...]
                #
                # ``_crossed`` already reads the tuple and the dataclass forms of
                # exactly this, and this file's own reservation table is the
                # dataclass one. The dict spelling was silent, so the third way
                # to write one record was the one way to write it unseen. The
                # slug and the code sit in the VALUES here, never in the keys,
                # which are field names.
                found.extend(self._crossed(list(node.values)))
            elif isinstance(node, (ast.Tuple, ast.List)):
                found.extend(self._crossed(list(node.elts)))
            elif isinstance(node, ast.DictComp):
                # ``{slug: 30 for slug in (...)}``: the value is the code and
                # every slug in the iterables is a key it is given to. Through
                # ``cause_keys_within``, so a comprehension over NAMED slugs
                # reads the same as one over inlined slugs; it pre-filtered the
                # iterable to ``ast.Constant`` for one round and did not.
                for generator in node.generators:
                    for element in self.cause_keys_within(generator.iter):
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
                    # three-argument call cannot pair the wrong two. See the
                    # residual "One check in this unit is unreachable".
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

        BOTH ARMS ASK ``cause_keys_within``, which they did not for one round.
        ``case Slug.CONFIG_UNUSABLE`` was reported and its direct twin
        ``if cause == Slug.CONFIG_UNUSABLE`` was silent, because the ``match``
        arm passed its pattern value in unfiltered and the ``if`` arm filtered
        the test to ``ast.Constant`` first. One method answered one question two
        ways; it asks once now.
        """
        found: list[tuple[ast.AST, ast.AST, str | None]] = []
        for node in ast.walk(self.tree):
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

    THERE IS NO SECOND KEY SET PARAMETER, and its absence is the fix rather than
    an omission. The round before carried ``named_only_causes`` with a default of
    empty and a docstring saying a caller that forgets it "loses coverage
    loudly". It did not: deleting the argument from both live call sites killed
    ZERO tests, because the tree-wide scan asserts that nothing is found, so
    dropping a tier makes it quieter and greener. A defaulted parameter that
    weakens a guard when omitted cannot be the shape of this, so there is nothing
    to omit.
    """
    tree = ast.parse(source)
    table = ReservedCodeTable(tree, causes, code_range, package)
    found: list[str] = []
    # ONE HIT PER (LINE, SLUG, STATUS), and this is not decoration. A duplicate
    # key in a mapping literal, which is the very first defect this unit's suite
    # hunts, reaches the walk as two pairs carrying the identical line, slug and
    # status, and so does a record whose code column repeats. Reporting the same
    # reservation twice makes the count in a failure message wrong, which is the
    # number the reader uses to decide how big the problem is.
    # ``test_a_duplicate_key_in_a_second_table_is_reported_once`` drives it.
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

    A NEGATIVE STATUS IS REPORTED, and until this round nothing in the suite
    could see whether it was. ``sys.exit(-1)`` is the worst bare status a module
    can write here rather than an odd one: the interpreter truncates it to 255 at
    the shell, which ``cli/exit_codes.py`` reserves against by name as "what a
    status above a byte truncates to", and the OTHER reader of these statuses is
    the job engine, which reads ``subprocess.returncode`` where a negative
    integer means KILLED BY THAT SIGNAL. So one module's ``exit(-1)`` arrives at
    one reader as the shell's own territory and at the other as a signal death,
    and neither reading is the refusal that was meant.

    It was uncovered in both directions at once, which is why it is written down
    here. Dropping ``resolve_int``'s unary-minus branch makes every negative
    resolve to nothing, and widening the zero test to ``status <= 0`` makes every
    negative a success; both were silent, and so was both together, because no
    fixture anywhere wrote a negative status.
    ``test_a_negative_status_is_a_bare_status_too`` writes three of them.
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
