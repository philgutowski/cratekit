#!/usr/bin/env python3
"""The one measure of U290's refactor: lines, copied blocks, and seams (U296).

Every card under the refactor epic and its final audit read their numbers here,
so they are all measured the same way, and the two battery checks
(``tests/test_duplication.py`` and ``tests/test_import_rules.py``) call these
same functions, so the suite and the audit can never read two different things.

Six commands, listed by ``--help``. Five are readings that write nothing:
``lines``, ``duplicates``, ``imports``, ``outside`` and ``table``. ``prune``
lowers the allowance files of the packages it is given, and can add no line.

THE DEFINITIONS, each fixed here and nowhere else.

A LINE is a physical line of a Python file git tracks, outside ``_vendor``. It
is blank, or a comment when it holds only a comment, or a docstring line when
it lies in the string that opens a module, class or function, or code, read in
that order, so a blank line inside a docstring is blank.

A LOGICAL LINE is one statement's tokens up to its NEWLINE token, joined by
single spaces, with comments, blank lines, statements that are one string and
import statements dropped. Indentation is not part of it. A BLOCK is six or
more consecutive logical lines that occur in two or more places.

A WINDOW is exactly six consecutive logical lines. The suite's allowance is
held in windows and not in whole blocks, because the edges of a whole block
move when somebody else removes a partner copy, and a package whose own lines
did not change must never fail for that. A window either still occurs twice or
it does not, so removing a place of a copy can only shrink what is found. An
edit that brings two stretches of lines together can form a window that was
never there, and that is a new copy, failing on the branch that made it.

A PACKAGE is the first directory under ``src/cratekit``, with ``modules`` read
one level deeper (``modules.outbound``), and ``root`` for the files beside
them.

An ALLOWANCE is a file of lines, one per place a package may still hold
something the rule forbids. Lines are only ever removed. A line whose finding
is gone never fails anything, so removing a copy or a crossing cannot fail
another card's package; ``prune`` removes such lines and can add none.

Standard library only, and it imports nothing of Cratekit: the verb registry
and the rules' own lists are read from source text. Every reading is of what
the source writes, so a module reached through ``importlib.import_module`` and
a name reached through ``getattr`` with a string are seen by no rule.
"""

from __future__ import annotations

import argparse
import ast
import collections
import hashlib
import io
import json
import keyword
import os
import subprocess
import sys
import tokenize
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from functools import cached_property
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The source the refactor measures, and the tree inside it that it never does.
SOURCE = "src/cratekit"
VENDOR = "_vendor"

#: The smallest block the duplication rule sees, in logical lines.
BLOCK_LINES = 6
#: A source file longer than this is named by ``lines`` (point 2 of U290).
LARGE_FILE = 1500

#: Packages that are not feature packages: the two lower layers, the shell,
#: and the files beside them.
ROOT_PACKAGE = "root"
LOWER_PACKAGES = frozenset({"core", "write", "cli", ROOT_PACKAGE})

#: An allowance, or what a rule found for one package: a multiset of lines.
Lines = collections.Counter[str]
#: The same per package.
Found = dict[str, Lines]

RATCHETS = "tests/ratchets"
DUPLICATION_ALLOWANCES = f"{RATCHETS}/duplication"
IMPORT_ALLOWANCES = f"{RATCHETS}/imports"
#: Where the import rules keep their lists, read here as literals.
IMPORT_RULES_TEST = "tests/test_import_rules.py"
REGISTRY = f"{SOURCE}/cli/registry.py"


# ── Files ───────────────────────────────────────────────────────────────────


def python_files(root: Path, scope: str) -> list[str]:
    """Repository relative paths of the Python files under ``scope``, sorted.

    Git's own list where there is one: the files it tracks, and the ones it
    would track, so a module written a minute ago is measured before it is
    committed and an ignored scratch file never is. A walk of the directory
    otherwise, so the readings still work on an unpacked archive. ``_vendor``
    and bytecode directories are never read.
    """
    target = root / scope
    if target.is_file():
        return [scope] if scope.endswith(".py") else []
    try:
        listed = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", scope],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.split("\0")
    except (OSError, subprocess.CalledProcessError):
        listed = [path.relative_to(root).as_posix() for path in target.rglob("*.py")]
    return sorted(
        path
        for path in listed
        if path.endswith(".py")
        and f"/{VENDOR}/" not in f"/{path}"
        and "/__pycache__/" not in f"/{path}"
        and (root / path).is_file()
    )


def read_sources(root: Path, scopes: Iterable[str]) -> dict[str, str]:
    """``{path: text}`` for every Python file under each scope."""
    out: dict[str, str] = {}
    for scope in scopes:
        for path in python_files(root, scope):
            out[path] = (root / path).read_text(encoding="utf-8")
    return out


def package_of_path(path: str) -> str:
    """The package a source file belongs to, by the definition above.

    A file outside ``src/cratekit`` is filed under its own top directory, so
    ``lines tests`` still prints one row.
    """
    prefix = SOURCE + "/"
    if not path.startswith(prefix):
        return path.split("/", 1)[0]
    parts = path[len(prefix) :].split("/")
    if len(parts) == 1:
        return ROOT_PACKAGE
    if parts[0] == "modules":
        return "modules" if len(parts) == 2 else f"modules.{parts[1]}"
    return parts[0]


def module_name(path: str) -> str:
    """``src/cratekit/core/config.py`` is ``cratekit.core.config``."""
    parts = path.removeprefix("src/").removesuffix(".py").split("/")
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


# ── Lines ───────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class LineCount:
    """One file's physical lines by kind. ``lines`` is their sum."""

    code: int = 0
    docstring: int = 0
    comment: int = 0
    blank: int = 0

    @property
    def lines(self) -> int:
        return self.code + self.docstring + self.comment + self.blank

    def __add__(self, other: LineCount) -> LineCount:
        return LineCount(*(mine + theirs for mine, theirs in zip(_kinds(self), _kinds(other))))


def count_lines(source: str) -> LineCount:
    """Classify every physical line of ``source``.

    Blank first, then a line that holds only a comment, then a line inside
    the string that opens a module, class or function, then code. The order
    is the survey's and reproduces its baseline to the line.
    """
    docstring: set[int] = set()
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        first = node.body[0] if node.body else None
        if (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        ):
            docstring.update(range(first.lineno, (first.end_lineno or first.lineno) + 1))
    comment = {
        token.start[0]
        for token in tokenize.generate_tokens(io.StringIO(source).readline)
        if token.type == tokenize.COMMENT and token.line.lstrip().startswith("#")
    }
    counts = collections.Counter()
    for number, line in enumerate(source.splitlines(), 1):
        if not line.strip():
            counts["blank"] += 1
        elif number in comment:
            counts["comment"] += 1
        elif number in docstring:
            counts["docstring"] += 1
        else:
            counts["code"] += 1
    return LineCount(counts["code"], counts["docstring"], counts["comment"], counts["blank"])


def count_test_functions(source: str) -> int:
    """Functions named ``test_...`` at module level or in a class."""
    found = 0
    for node in ast.parse(source).body:
        for member in node.body if isinstance(node, ast.ClassDef) else [node]:
            if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found += member.name.startswith("test_")
    return found


# ── Copied blocks ───────────────────────────────────────────────────────────


#: One logical line: the physical lines it starts and ends on, and its tokens.
Logical = collections.namedtuple("Logical", "start end text")

_STRING_TOKENS = frozenset(
    getattr(tokenize, name, -1)
    for name in ("STRING", "FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END")
)
_SKIPPED_TOKENS = frozenset(
    getattr(tokenize, name)
    for name in ("COMMENT", "NL", "ENCODING", "ENDMARKER", "INDENT", "DEDENT")
)


def logical_lines(source: str, *, renamed: bool = False) -> list[Logical]:
    """The logical lines of ``source``, by the definition in this file's docstring.

    ``renamed`` replaces every identifier by ``N``, every number by ``0`` and
    every string by ``S`` before the tokens are joined, so a copy with its
    names changed still matches. That reading also matches tables, which is
    why it is information and never a rule.
    """
    out: list[Logical] = []
    written: list[str] = []
    first: tokenize.TokenInfo | None = None
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        kind = token.type
        if kind in _SKIPPED_TOKENS:
            continue
        if kind == tokenize.NEWLINE:
            if first is not None:
                one_string = len(written) == 1 and first.type == tokenize.STRING
                an_import = first.type == tokenize.NAME and first.string in ("import", "from")
                if not one_string and not an_import:
                    out.append(Logical(first.start[0], token.end[0], " ".join(written)))
            written, first = [], None
            continue
        if first is None:
            first = token
        if not renamed:
            written.append(token.string)
        elif kind == tokenize.NAME and not keyword.iskeyword(token.string):
            written.append("N")
        elif kind == tokenize.NUMBER:
            written.append("0")
        elif kind in _STRING_TOKENS:
            written.append("S")
        else:
            written.append(token.string)
    return out


#: One place a window stands: its file, and its first logical line's index.
Place = collections.namedtuple("Place", "path index")
#: A maximal run of copied logical lines in one file: the survey's "block".
Run = collections.namedtuple("Run", "path first_line last_line logical")


class Copies:
    """Every repeated window of ``size`` logical lines across ``sources``.

    ``repeated`` maps a window's digest to its places, and holds only windows
    that stand in two or more places. Two windows that overlap in one file
    are two places, as in the survey's instrument.
    """

    def __init__(
        self, sources: Mapping[str, str], *, size: int = BLOCK_LINES, renamed: bool = False
    ) -> None:
        if size < 1:
            raise ValueError("a block is at least one logical line")
        self.size = size
        self.lines = {
            path: logical_lines(text, renamed=renamed) for path, text in sources.items()
        }
        index: dict[bytes, list[Place]] = collections.defaultdict(list)
        for path, lines in self.lines.items():
            hashed = [hashlib.sha256(line.text.encode("utf-8")).digest() for line in lines]
            for start in range(len(lines) - size + 1):
                key = hashlib.sha256(b"".join(hashed[start : start + size])).digest()
                index[key].append(Place(path, start))
        self.repeated: dict[str, list[Place]] = {
            key.hex()[:16]: places for key, places in index.items() if len(places) > 1
        }

    @property
    def logical_total(self) -> int:
        return sum(len(lines) for lines in self.lines.values())

    @cached_property
    def runs(self) -> list[Run]:
        """Maximal runs of covered lines per file, longest first."""
        covered: dict[str, set[int]] = collections.defaultdict(set)
        for places in self.repeated.values():
            for place in places:
                covered[place.path].update(range(place.index, place.index + self.size))
        runs: list[Run] = []
        for path, indexes in covered.items():
            lines = self.lines[path]
            ordered = sorted(indexes)
            start = previous = ordered[0]
            for index in [*ordered[1:], None]:
                if index is None or index != previous + 1:
                    runs.append(
                        Run(path, lines[start].start, lines[previous].end, previous - start + 1)
                    )
                    if index is not None:
                        start = index
                if index is not None:
                    previous = index
        return sorted(runs, key=lambda run: (-run.logical, run.path, run.first_line))

    def held(self) -> Found:
        """Per package, each repeated window's digest and how many places hold it."""
        out: Found = collections.defaultdict(collections.Counter)
        for digest, places in self.repeated.items():
            for place in places:
                out[package_of_path(place.path)][digest] += 1
        return dict(out)

    def describe(self, digest: str) -> str:
        """Where one window stands, as ``path:first-last`` for each place."""
        spans = []
        for place in self.repeated.get(digest, ()):
            lines = self.lines[place.path]
            last = lines[place.index + self.size - 1]
            spans.append(f"{place.path}:{lines[place.index].start}-{last.end}")
        return ", ".join(spans)


# ── Allowances ──────────────────────────────────────────────────────────────


def parse_allowance(text: str) -> Lines:
    """An allowance file's lines as a multiset. ``#`` opens a comment line."""
    return collections.Counter(
        " ".join(line.split())
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )


def read_allowances(root: Path, directory: str) -> Found:
    """``{package: allowance}`` for every ``<package>.txt`` in ``directory``."""
    out: Found = {}
    for path in sorted((root / directory).glob("*.txt")):
        out[path.stem] = parse_allowance(path.read_text(encoding="utf-8"))
    return out


def over_allowance(found: Mapping[str, Lines], allowed: Mapping[str, Lines]) -> Found:
    """What each package holds beyond its allowance. Empty means the rule holds.

    Only an excess is reported. An allowance line with nothing found against
    it is never a failure: the finding went away, which is the point.
    """
    out: Found = {}
    for package, counts in found.items():
        excess = counts - allowed.get(package, collections.Counter())
        if excess:
            out[package] = excess
    return out


def pruned(found: Lines, allowed: Lines) -> Lines:
    """The allowance lowered to what is still found. It can never gain a line."""
    return found & allowed


def render_allowance(header: Sequence[str], lines: Lines) -> str:
    body = sorted(lines.elements())
    return "".join(f"{line}\n" for line in [*(f"# {text}".rstrip() for text in header), *body])


def allowance_header(text: str) -> list[str]:
    """The comment lines a file opens with, without their ``# ``."""
    header: list[str] = []
    for line in text.splitlines():
        if not line.startswith("#"):
            break
        header.append(line[1:].removeprefix(" "))
    return header


# ── The source tree, for the import rules ───────────────────────────────────


@dataclass(frozen=True, slots=True)
class Use:
    """One place a module uses another module of the package, or a name in it.

    ``name`` is None for an import of the module itself. ``kind`` is
    ``import`` for a name written in an import statement and ``attribute`` for
    one reached through a module the file imported. ``lazy`` is an import
    inside a function, ``typing_only`` one under ``if TYPE_CHECKING``.
    ``rest`` is what is read off the name, kept so a name that is a module
    can be followed into it, and ``local`` what an import binds.
    """

    path: str
    target: str
    name: str | None
    line: int
    kind: str
    lazy: bool = False
    typing_only: bool = False
    rest: tuple[str, ...] = ()
    local: str | None = None

    @property
    def dotted(self) -> str:
        return self.target if self.name is None else f"{self.target}.{self.name}"


def is_private(name: str) -> bool:
    """A leading underscore that is not a dunder."""
    return name.startswith("_") and not (name.startswith("__") and name.endswith("__"))


def _is_type_checking(test: ast.expr) -> bool:
    return (isinstance(test, ast.Name) and test.id == "TYPE_CHECKING") or (
        isinstance(test, ast.Attribute) and test.attr == "TYPE_CHECKING"
    )


@dataclass(frozen=True, slots=True)
class _FileReading:
    """What one parse of one file yields. ``defined`` is None when it cannot be listed."""

    uses: list[Use]
    functions: dict[str, tuple[int, int]]
    aliases: dict[str, str]
    defined: frozenset[str] | None
    #: ``(local name, attributes, line)`` read off a name imported from a module.
    chains: tuple[tuple[str, tuple[str, ...], int], ...] = ()


def _defined_names(tree: ast.Module) -> frozenset[str] | None:
    """The names a module binds at its top level, branches of ``if`` and ``try`` included.

    None when the module can answer for any name, by a ``__getattr__`` of its
    own or a star import, so that nothing is ruled out on a list that is not
    the whole of it.
    """
    names: set[str] = set()
    pending: list[ast.AST] = list(tree.body)
    while pending:
        node = pending.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            names.update((alias.asname or alias.name).split(".")[0] for alias in node.names)
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                names.update(n.id for n in ast.walk(target) if isinstance(n, ast.Name))
        else:
            pending.extend(
                child for child in ast.iter_child_nodes(node) if isinstance(child, ast.stmt)
            )
            pending.extend(
                inner for handler in getattr(node, "handlers", ()) for inner in handler.body
            )
    return None if names & {"__getattr__", "*"} else frozenset(names)


class Tree:
    """The package's modules as source text, and what each one reaches for.

    Built from ``{path: text}`` so the fixture tests hand it synthetic
    sources and the real reading hands it the tree. Only absolute and
    relative imports of the package itself are read. Each file is parsed
    once, read, and its syntax tree dropped: holding every tree of this
    package at once is hundreds of megabytes (``tests/_parse_memo.py``).

    A name reached through an imported module, ``config.load``, is a use only
    when that module defines the name at its top level. A module's alias is
    followed anywhere in the file, and a local variable named as
    an imported module is would otherwise read as a use of it: ``source.name`` beside
    ``from cratekit.modules.outbound import source`` is the tree's own case.

    A name that is itself a module of the package is followed into it (U331):
    ``tags.art.read`` and ``from cratekit.core.tags import art`` are uses of
    ``cratekit.core.art``, whichever module handed it over, so a module cannot
    be reached under one counted name of another.
    """

    def __init__(self, sources: Mapping[str, str], *, root_package: str = "cratekit") -> None:
        self.root_package = root_package
        self.sources = dict(sources)
        self.modules: dict[str, str] = {module_name(path): path for path in self.sources}

    def owns(self, dotted: str) -> bool:
        return dotted == self.root_package or dotted.startswith(self.root_package + ".")

    def resolve(self, dotted: str) -> tuple[str, list[str]]:
        """Split ``dotted`` into its longest known module and the names after it."""
        parts = dotted.split(".")
        for cut in range(len(parts), 0, -1):
            candidate = ".".join(parts[:cut])
            if candidate in self.modules:
                return candidate, parts[cut:]
        return dotted, []

    def package(self, module: str) -> str:
        """The package of a module, by its file where the tree holds it."""
        known, _ = self.resolve(module)
        if known in self.modules:
            return package_of_path(self.modules[known])
        return package_of_path("src/" + module.replace(".", "/") + ".py")

    @cached_property
    def _read(self) -> dict[str, _FileReading]:
        return {path: self._read_file(path) for path in self.sources}

    @cached_property
    def uses(self) -> dict[str, list[Use]]:
        """``{path: every use in that file}``, imports first."""
        defined = {module_name(path): read.defined for path, read in self._read.items()}
        return {
            path: [
                use
                for use in self._followed(read)
                if use.kind == "import"
                or use.name is None
                or defined[use.target] is None
                or use.name in defined[use.target]
            ]
            for path, read in self._read.items()
        }

    def _handed(self, module: str, name: str | None) -> str | None:
        """The module of the package that ``module`` binds ``name`` to, if it binds one."""
        path = self.modules.get(module)
        bound = self._read[path].aliases.get(name) if path is not None and name else None
        return bound if bound in self.modules else None

    def _reached(self, module: str, rest: Sequence[str]) -> tuple[str, str | None]:
        """Where ``module`` and what is read off it lead: a module, and a name in it or None."""
        while rest:
            module, more = self.resolve(".".join([module, *rest]))
            handed = self._handed(module, more[0]) if more else None
            if handed is None:
                return module, more[0] if more else None
            module, rest = handed, more[1:]
        return module, None

    def _followed(self, read: _FileReading) -> list[Use]:
        """One file's uses, each name that is a module read as a use of that module."""
        out: list[Use] = []
        for use in read.uses:
            module = self._handed(use.target, use.name)
            if module is None:
                out.append(use)
            elif use.kind == "import":
                out.append(replace(use, target=module, name=None))
                for local, chain, line in read.chains:
                    if local == use.local:
                        target, name = self._reached(module, chain)
                        out.append(Use(use.path, target, name, line, "attribute"))
            else:
                target, name = self._reached(module, use.rest)
                out.append(replace(use, target=target, name=name, rest=()))
        return out

    def aliases(self, path: str) -> dict[str, str]:
        """``{local name: module}`` for the modules one file imports under a name."""
        return self._read[path].aliases

    def _base_of(self, path: str, level: int) -> str | None:
        """The package a relative import of ``level`` dots starts from."""
        parts = module_name(path).split(".")
        if not path.endswith("/__init__.py"):
            parts = parts[:-1]
        cut = len(parts) - (level - 1)
        return ".".join(parts[:cut]) if cut >= 1 else None

    def _read_file(self, path: str) -> _FileReading:
        """One file's uses, top level functions, module aliases and defined names.

        An import is lazy when it stands on a line inside any function, and
        typing only when it stands inside the body of ``if TYPE_CHECKING``,
        both read from line spans so the tree is walked once.
        """
        tree = ast.parse(self.sources[path])
        imports: list[ast.Import | ast.ImportFrom] = []
        attributes: list[ast.Attribute] = []
        functions: list[tuple[int, int]] = []
        typing_blocks: list[tuple[int, int]] = []
        for node in ast.walk(tree):
            kind = node.__class__
            if kind is ast.Attribute:
                attributes.append(node)
            elif kind is ast.Import or kind is ast.ImportFrom:
                imports.append(node)
            elif kind is ast.FunctionDef or kind is ast.AsyncFunctionDef:
                functions.append((node.lineno, node.end_lineno or node.lineno))
            elif kind is ast.If and _is_type_checking(node.test):
                last = node.body[-1]
                typing_blocks.append((node.body[0].lineno, last.end_lineno or last.lineno))

        def inside(line: int, spans: list[tuple[int, int]]) -> bool:
            return any(first <= line <= last for first, last in spans)

        found: list[Use] = []
        aliases: dict[str, str] = {}
        named: set[str] = set()
        for node in sorted(imports, key=lambda node: (node.lineno, node.col_offset)):
            lazy = inside(node.lineno, functions)
            typing_only = inside(node.lineno, typing_blocks)
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if not self.owns(alias.name):
                        continue
                    found.append(
                        Use(path, alias.name, None, node.lineno, "import", lazy, typing_only)
                    )
                    top = alias.name.split(".")[0]
                    aliases[alias.asname or top] = alias.name if alias.asname else top
                continue
            base = node.module or ""
            if node.level:
                start = self._base_of(path, node.level)
                if start is None:
                    continue
                base = f"{start}.{base}" if base else start
            if not self.owns(base):
                continue
            for alias in node.names:
                whole = f"{base}.{alias.name}"
                if whole in self.modules:
                    found.append(Use(path, whole, None, node.lineno, "import", lazy, typing_only))
                    aliases[alias.asname or alias.name] = whole
                else:
                    local = alias.asname or alias.name
                    named.add(local)
                    found.append(Use(
                        path, base, alias.name, node.lineno, "import", lazy, typing_only,
                        local=local,
                    ))

        chains: list[tuple[str, tuple[str, ...], int]] = []
        for node in attributes:
            chain: list[str] = []
            current: ast.expr = node
            while isinstance(current, ast.Attribute):
                chain.append(current.attr)
                current = current.value
            if not isinstance(current, ast.Name):
                continue
            chain.reverse()
            if current.id in named and current.id not in aliases:
                chains.append((current.id, tuple(chain), node.lineno))
            if current.id not in aliases:
                continue
            target, rest = self.resolve(".".join([aliases[current.id], *chain]))
            if rest and target in self.modules:
                found.append(
                    Use(path, target, rest[0], node.lineno, "attribute", rest=tuple(rest[1:]))
                )

        top_level = {
            node.name: (node.lineno, node.end_lineno or node.lineno)
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        return _FileReading(found, top_level, aliases, _defined_names(tree), tuple(chains))

    # The import graph at import time, for rule four.

    @cached_property
    def loads(self) -> dict[str, frozenset[str]]:
        """``{module: the modules its own import names}``, as written.

        Top level statements only, and nothing under ``TYPE_CHECKING``: what
        runs when the module is imported. A class body runs then too.
        """
        out: dict[str, set[str]] = {module: set() for module in self.modules}
        for path, uses in self.uses.items():
            for use in uses:
                if use.kind == "import" and not use.lazy and not use.typing_only:
                    out[module_name(path)].add(use.target)
        return {module: frozenset(targets) for module, targets in out.items()}

    def function_loads(self, module: str, function: str) -> frozenset[str]:
        """The modules named by imports written in one top level function's body."""
        path = self.modules.get(module)
        span = self._read[path].functions.get(function) if path is not None else None
        if span is None:
            return frozenset()
        return frozenset(
            use.target
            for use in self.uses[path]
            if use.kind == "import"
            and use.lazy
            and not use.typing_only
            and span[0] <= use.line <= span[1]
        )

    def loaded_from(self, starts: Iterable[str], blocked: Sequence[str] = ()) -> frozenset[str]:
        """Every module importing ``starts`` runs, never passing a blocked one.

        Importing ``a.b.c`` imports ``a`` and ``a.b`` first, so each module's
        packages are loaded with it. A module under a ``blocked`` prefix is
        where an import stops, so nothing is followed through it.
        """
        seen: set[str] = set()
        queue = list(starts)
        while queue:
            parts = queue.pop().split(".")
            for cut in range(1, len(parts) + 1):
                module = ".".join(parts[:cut])
                if module in seen or within(module, blocked):
                    continue
                seen.add(module)
                queue.extend(self.loads.get(module, ()))
        return frozenset(seen)


def within(module: str, prefixes: Sequence[str]) -> bool:
    """True when ``module`` is one of ``prefixes`` or lies under one."""
    return any(module == prefix or module.startswith(prefix + ".") for prefix in prefixes)


# ── The import rules. Each returns {importing package: Counter of allowance lines}. ───


def private_crossings(tree: Tree) -> Found:
    """Rule one: no private name crosses a package.

    A use is a crossing when the name, or any part of the module path after
    the root, is private, and the module that defines it is in another
    package. ``_vendor`` is the vendored downloader's own seam and is exempt
    by name. One line per package and name, however many files use it, so a
    module that is split adds none.
    """
    out: Found = collections.defaultdict(collections.Counter)
    for path, uses in tree.uses.items():
        importer = package_of_path(path)
        for use in uses:
            parts = use.target.split(".")[1:]
            if VENDOR in parts:
                continue
            private = any(is_private(part) for part in parts) or (
                use.name is not None and is_private(use.name)
            )
            if private and tree.package(use.target) != importer:
                out[importer][f"private {use.dotted}"] = 1
    return dict(out)


def core_modules_reached(tree: Tree) -> dict[str, set[str]]:
    """``{core module: feature packages that reach it}``, by any import."""
    out: dict[str, set[str]] = collections.defaultdict(set)
    core = f"{tree.root_package}.core"
    for path, uses in tree.uses.items():
        importer = package_of_path(path)
        if importer in LOWER_PACKAGES:
            continue
        for use in uses:
            if use.target.startswith(core + "."):
                out[use.target.split(".")[2]].add(importer)
    return dict(out)


def off_interface(tree: Tree, interface: Iterable[str]) -> Found:
    """Rule two: a feature package imports from core only the named interface."""
    named = frozenset(interface)
    out: Found = collections.defaultdict(collections.Counter)
    for module, packages in core_modules_reached(tree).items():
        if module in named:
            continue
        for package in packages:
            out[package][f"off-interface {tree.root_package}.core.{module}"] = 1
    return dict(out)


def toggleable_packages(tree: Tree, homes: Mapping[str, Sequence[str]]) -> frozenset[str]:
    """The packages that hold a toggle's home."""
    return frozenset(tree.package(home) for owned in homes.values() for home in owned)


def top_level_toggleable(
    tree: Tree, homes: Mapping[str, Sequence[str]], *, lazy: bool = False
) -> Found:
    """Rule three: an always on package never imports a toggleable one at top level.

    Counted per imported name, as the survey counted its 54, and held on the
    allowance as one line per package and name. ``lazy=True`` reads the
    imports inside functions instead, which the rule allows.
    """
    toggleable = toggleable_packages(tree, homes)
    out: Found = collections.defaultdict(collections.Counter)
    for path, uses in tree.uses.items():
        importer = package_of_path(path)
        if importer in toggleable:
            continue
        for use in uses:
            if use.kind != "import" or use.typing_only or use.lazy != lazy:
                continue
            if tree.package(use.target) in toggleable:
                out[importer][f"top-level {use.dotted}"] += 1
    return dict(out)


@dataclass(frozen=True, slots=True)
class Verb:
    """A landed verb as the registry declares it: what rule four needs."""

    name: str
    module: str
    builder: str
    toggle: str | None


#: The importer rule four names when the registry itself loads a module in a
#: toggle's home for a verb that toggle does not gate.
REGISTRY_LOADS = "(registry)"


@dataclass(frozen=True, slots=True)
class Dangling:
    """What one toggle leaves dangling when its homes cannot be imported.

    ``verbs`` are the remaining verbs that no longer build. ``edges`` are the
    imports that cause it, each ``(importing module, module in a home)``: the
    importing module is outside the toggle's homes and is loaded for at least
    one remaining verb.
    """

    toggle: str
    verbs: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]


def dangling(
    tree: Tree, verbs: Iterable[Verb], homes: Mapping[str, Sequence[str]]
) -> list[Dangling]:
    """Rule four, read from source: toggle by toggle, which verbs stop building.

    A verb builds by importing its module and running its builder, so what it
    loads is everything its module's import runs plus the imports written in
    its builder. With a toggle off, its homes cannot be imported, and a
    remaining verb dangles when what it loads names a module in one of them.
    Imports made by functions the builder calls are not followed;
    ``imports --drive`` drives the same question in a fresh interpreter and
    prints any difference.
    """
    listed = list(verbs)
    out: list[Dangling] = []
    for toggle, owned in homes.items():
        broken: list[str] = []
        edges: set[tuple[str, str]] = set()
        for verb in listed if owned else ():
            if verb.toggle == toggle:
                continue
            if within(verb.module, owned):
                broken.append(verb.name)
                edges.add((REGISTRY_LOADS, verb.module))
                continue
            built = tree.function_loads(verb.module, verb.builder)
            crossing = {(verb.module, target) for target in built if within(target, owned)}
            for module in tree.loaded_from([verb.module, *built], owned):
                crossing.update(
                    (module, target)
                    for target in tree.loads.get(module, ())
                    if within(target, owned)
                )
            if crossing:
                broken.append(verb.name)
                edges.update(crossing)
        out.append(Dangling(toggle, tuple(sorted(broken)), tuple(sorted(edges))))
    return out


def dangling_lines(tree: Tree, found: Iterable[Dangling]) -> Found:
    """Rule four's allowance lines, filed under the package holding the import.

    A verb the registry loads from inside a home it is not gated by is filed
    under that module's own package.
    """
    out: Found = collections.defaultdict(collections.Counter)
    for item in found:
        for importer, loaded in item.edges:
            package = tree.package(loaded if importer == REGISTRY_LOADS else importer)
            out[package][f"dangling {item.toggle} {loaded}"] = 1
    return dict(out)


def core_names(tree: Tree) -> dict[str, set[str]]:
    """``{feature package: the core names it uses}``, each as a dotted name."""
    core = f"{tree.root_package}.core"
    out: dict[str, set[str]] = collections.defaultdict(set)
    for path, uses in tree.uses.items():
        importer = package_of_path(path)
        if importer in LOWER_PACKAGES:
            continue
        for use in uses:
            if use.name is not None and (use.target == core or use.target.startswith(core + ".")):
                out[importer].add(use.dotted)
    return dict(out)


def import_findings(tree: Tree, rules: Rules, verbs: Iterable[Verb]) -> Found:
    """Every allowance line the four rules find, per importing package."""
    out: Found = collections.defaultdict(collections.Counter)
    for found in (
        private_crossings(tree),
        off_interface(tree, rules.interface),
        {
            package: collections.Counter(dict.fromkeys(lines, 1))
            for package, lines in top_level_toggleable(tree, rules.homes).items()
        },
        dangling_lines(tree, dangling(tree, verbs, rules.homes)),
    ):
        for package, lines in found.items():
            out[package].update(lines)
    return dict(out)


# ── The rules' lists, the verbs and the toggles, read from source text ──────


@dataclass(frozen=True, slots=True)
class Rules:
    """The lists the import rules test declares, read as literals."""

    interface: tuple[str, ...]
    homes: dict[str, tuple[str, ...]]
    names_ceiling: int


def _literal_assignments(source: str) -> dict[str, object]:
    """Every module level ``NAME = literal`` or ``NAME: T = literal``."""
    out: dict[str, object] = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target, value = node.targets[0], node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            target, value = node.target, node.value
        else:
            continue
        if not isinstance(target, ast.Name):
            continue
        try:
            out[target.id] = ast.literal_eval(value)
        except (ValueError, TypeError, SyntaxError):
            continue
    return out


def rules_from(test_source: str) -> Rules:
    """The interface list, the toggle homes and the names ceiling, from the test.

    They live in ``tests/test_import_rules.py``, where the layer ladder's own
    lists live, and are read here as literals so there is one copy.
    """
    found = _literal_assignments(test_source)
    return Rules(
        interface=tuple(found["CORE_INTERFACE"]),
        homes={toggle: tuple(owned) for toggle, owned in found["TOGGLE_HOMES"].items()},
        names_ceiling=int(found["CORE_NAMES_CEILING"]),
    )


def verbs_from(registry_source: str) -> list[Verb]:
    """Every landed verb, read from the registry's ``ENTRIES`` as written.

    The registry cannot be imported with the standard library alone, so its
    table is read as text: each ``Entry(...)`` call's keywords, a bare name
    resolved through the module's own string constants. An argument this
    cannot read raises, and ``tests/test_import_rules.py`` holds the reading
    equal to the live registry.
    """
    tree = ast.parse(registry_source)
    constants = _literal_assignments(registry_source)

    def value(given: Mapping[str, ast.expr], field: str, verb: str) -> object:
        node = given.get(field)
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name) and node.id in constants:
            return constants[node.id]
        state = "does not give" if node is None else "gives"
        raise ValueError(f"the registry entry {verb!r} {state} {field} in a form this can read")

    entries: ast.expr | None = None
    for node in tree.body:
        target = node.target if isinstance(node, ast.AnnAssign) else None
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
        if isinstance(target, ast.Name) and target.id == "ENTRIES":
            entries = node.value
    if not isinstance(entries, ast.Tuple):
        raise ValueError("the registry holds no ENTRIES tuple")
    out: list[Verb] = []
    for call in entries.elts:
        if not isinstance(call, ast.Call) or call.args:
            raise ValueError("an ENTRIES member is not an Entry(...) call of keywords")
        given = {keyword_.arg: keyword_.value for keyword_ in call.keywords}
        name = str(value(given, "name", "?"))
        if "planned_in" in given and value(given, "planned_in", name) is not None:
            continue
        toggle = value(given, "module_id", name) if "module_id" in given else None
        module, builder = value(given, "module", name), value(given, "builder", name)
        out.append(Verb(name, str(module), str(builder), None if toggle is None else str(toggle)))
    return out


# ── Names used from outside a set of files ──────────────────────────────────


@dataclass(frozen=True, slots=True)
class OutsideUse:
    """One name of an owned module that a file outside the set uses."""

    target: str
    name: str
    user: str
    line: int
    kind: str


_SETTERS = frozenset({"setattr", "getattr", "delattr", "hasattr", "object"})


def outside_uses(sources: Mapping[str, str], owned: Iterable[str]) -> list[OutsideUse]:
    """Every name of the ``owned`` files that another file reaches for.

    Three forms are read: a name in an import statement, a name reached
    through an imported module, and a name written as text, either a dotted
    string (``"cratekit.core.config.load"``) or the second argument of
    ``setattr``, ``getattr``, ``monkeypatch.setattr`` and ``patch.object`` on
    an imported module, which is how the suite replaces a name. A name built
    at run time is not seen.
    """
    owned_paths = frozenset(owned)
    tree = Tree(sources)
    owned_modules = {module_name(path) for path in owned_paths if path in sources}
    found: list[OutsideUse] = []
    for path in sources:
        if path in owned_paths:
            continue
        for use in tree.uses[path]:
            if use.name is not None and use.target in owned_modules:
                found.append(OutsideUse(use.target, use.name, path, use.line, use.kind))
        aliases = tree.aliases(path)
        for node in ast.walk(ast.parse(tree.sources[path])):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                text = node.value
                if tree.owns(text) and text.replace(".", "").replace("_", "").isalnum():
                    target, rest = tree.resolve(text)
                    if rest and target in owned_modules:
                        found.append(OutsideUse(target, rest[0], path, node.lineno, "string"))
            elif isinstance(node, ast.Call) and len(node.args) >= 2:
                called = getattr(node.func, "attr", None) or getattr(node.func, "id", "")
                first, second = node.args[0], node.args[1]
                if called not in _SETTERS or not isinstance(second, ast.Constant):
                    continue
                if not isinstance(second.value, str):
                    continue
                target = _aliased_module(tree, aliases, first)
                if target in owned_modules:
                    found.append(OutsideUse(target, second.value, path, node.lineno, "string"))
    return found


def _aliased_module(tree: Tree, aliases: Mapping[str, str], node: ast.expr) -> str | None:
    chain: list[str] = []
    while isinstance(node, ast.Attribute):
        chain.append(node.attr)
        node = node.value
    if not isinstance(node, ast.Name) or node.id not in aliases:
        return None
    target, rest = tree.resolve(".".join([aliases[node.id], *reversed(chain)]))
    return target if not rest else None


# ── Printing ────────────────────────────────────────────────────────────────


def _print_table(header: Sequence[str], rows: Sequence[Sequence[object]], out) -> None:
    """Left align the first column and right align the rest."""
    table = [header, *rows]
    widths = [max(len(str(row[column])) for row in table) for column in range(len(header))]
    for row in table:
        cells = [f"{row[0]!s:<{widths[0]}}"]
        cells += [f"{cell!s:>{width}}" for cell, width in zip(row[1:], widths[1:])]
        print("  ".join(cells), file=out)


def _total(counters: Mapping[str, Lines]) -> int:
    return sum(sum(lines.values()) for lines in counters.values())


def lines_report(sources: Mapping[str, str], *, files: bool, out) -> None:
    per_file = {path: count_lines(text) for path, text in sources.items()}
    packages: dict[str, list[LineCount]] = collections.defaultdict(list)
    for path, count in per_file.items():
        packages[package_of_path(path)].append(count)

    def row(name: str, counts: Sequence[LineCount]) -> tuple[object, ...]:
        total = sum(counts, LineCount())
        large = sum(count.lines > LARGE_FILE for count in counts)
        return (name, len(counts), total.lines, *_kinds(total), large)

    rows = [row(name, counts) for name, counts in packages.items()]
    rows.sort(key=lambda cells: (-cells[2], cells[0]))
    header = ("package", "files", "lines", "code", "docstring", "comment", "blank")
    _print_table(
        (*header, f"over {LARGE_FILE}"), [*rows, row("all", list(per_file.values()))], out
    )
    over = sorted(
        ((count.lines, path) for path, count in per_file.items() if count.lines > LARGE_FILE),
        reverse=True,
    )
    print(f"\nfiles over {LARGE_FILE} lines: {len(over)}", file=out)
    for lines, path in over:
        print(f"  {lines:6d}  {path}", file=out)
    if files:
        print("\nevery file:", file=out)
        listing = sorted(per_file.items(), key=lambda item: (-item[1].lines, item[0]))
        _print_table(
            ("file", *header[2:]),
            [(path, count.lines, *_kinds(count)) for path, count in listing],
            out,
        )


def _kinds(count: LineCount) -> tuple[int, int, int, int]:
    return count.code, count.docstring, count.comment, count.blank


def duplicates_line(copies: Copies) -> str:
    """Blocks, the logical lines in them, the files holding one, and window places."""
    runs = copies.runs
    logical = sum(run.logical for run in runs)
    share = 100 * logical / copies.logical_total if copies.logical_total else 0.0
    return (
        f"{len(runs)} blocks over {logical} logical lines in "
        f"{len({run.path for run in runs})} files ({share:.1f}% of "
        f"{copies.logical_total} logical lines in {len(copies.lines)} files); "
        f"{sum(map(len, copies.repeated.values()))} places of a repeated window of {copies.size}"
    )


def duplicates_report(
    sources: Mapping[str, str], *, size: int, renamed: bool, listed: int, out
) -> None:
    copies = Copies(sources, size=size, renamed=renamed)
    reading = "renamed (identifiers, numbers and strings normalised)" if renamed else "exact"
    print(
        f"{reading}, blocks of {size} logical lines or more: {duplicates_line(copies)}", file=out
    )
    blocks: Lines = collections.Counter()
    logical: Lines = collections.Counter()
    for run in copies.runs:
        blocks[package_of_path(run.path)] += 1
        logical[package_of_path(run.path)] += run.logical
    held = copies.held()
    _print_table(
        ("package", "blocks", "logical lines", "window places"),
        [
            (name, blocks[name], lines, sum(held.get(name, {}).values()))
            for name, lines in logical.most_common()
        ],
        out,
    )
    for run in copies.runs[:listed]:
        print(
            f"  {run.logical:4d} logical  {run.path}:{run.first_line}-{run.last_line}", file=out
        )


def _load(root: Path) -> tuple[dict[str, str], Tree, Rules, list[Verb]]:
    sources = read_sources(root, [SOURCE])
    rules = rules_from((root / IMPORT_RULES_TEST).read_text(encoding="utf-8"))
    verbs = verbs_from((root / REGISTRY).read_text(encoding="utf-8"))
    return sources, Tree(sources), rules, verbs


def seam_counts(tree: Tree, rules: Rules, verbs: Sequence[Verb]) -> dict[str, int]:
    """The numbers the import rules hold, one per name, for ``imports`` and ``table``."""
    private = private_crossings(tree)
    found = dangling(tree, verbs, rules.homes)
    names = core_names(tree)
    return {
        "private names crossing a package": len(
            {line for lines in private.values() for line in lines}
        ),
        "packages and private names": _total(private),
        "core modules": sum(package_of_path(path) == "core" for path in tree.sources),
        "core modules feature packages reach": len(core_modules_reached(tree)),
        "core modules on the interface list": len(rules.interface),
        "reaches off the interface list": _total(off_interface(tree, rules.interface)),
        "top level imports of a toggleable package": _total(
            top_level_toggleable(tree, rules.homes)
        ),
        "lazy imports of a toggleable package": _total(
            top_level_toggleable(tree, rules.homes, lazy=True)
        ),
        "verbs left dangling, summed over the toggles": sum(len(item.verbs) for item in found),
        "allowance lines for the imports that leave them dangling": _total(
            dangling_lines(tree, found)
        ),
        "distinct core names feature packages use": len(
            {name for used in names.values() for name in used}
        ),
        "the ceiling on distinct core names": rules.names_ceiling,
    }


def imports_report(root: Path, *, names: bool, drive: bool, out) -> int:
    _, tree, rules, verbs = _load(root)
    for label, count in seam_counts(tree, rules, verbs).items():
        print(f"{count:6d}  {label}", file=out)

    private = private_crossings(tree)
    print("\ncore modules reached, by how many feature packages:", file=out)
    reached = core_modules_reached(tree)
    for module, packages in sorted(reached.items(), key=lambda item: (-len(item[1]), item[0])):
        mark = "" if module in rules.interface else "  off the list: " + ", ".join(sorted(packages))
        print(f"  {len(packages):3d}  {module}{mark}", file=out)

    print("\nprivate names crossing a package:", file=out)
    crossing: dict[str, list[str]] = collections.defaultdict(list)
    for package, lines in private.items():
        for line in lines:
            crossing[line.split(" ", 1)[1]].append(package)
    for name, packages in sorted(crossing.items()):
        print(f"  {name}  from {', '.join(sorted(packages))}", file=out)

    print("\nwith a toggle off and its homes unimportable:", file=out)
    found = dangling(tree, verbs, rules.homes)
    for item in found:
        print(
            f"  {item.toggle:<11} {len(item.verbs):3d} verbs dangle, by {len(item.edges):3d} imports",
            file=out,
        )

    if names:
        print("\nevery core name a feature package uses:", file=out)
        for name in sorted({name for group in core_names(tree).values() for name in group}):
            print(f"  {name}", file=out)
    return _drive_report(root, rules, found, out) if drive else 0


#: Run in a fresh interpreter by ``imports --drive``. It blocks each toggle's
#: homes in turn, imports every remaining verb's module, runs its builder and
#: formats its help, and prints which verbs failed, as JSON.
_DRIVE = r"""
import argparse, importlib, importlib.abc, json, sys

homes = json.loads(sys.argv[1])

class Block(importlib.abc.MetaPathFinder):
    prefixes = ()
    def find_spec(self, name, path, target=None):
        for prefix in self.prefixes:
            if name == prefix or name.startswith(prefix + "."):
                raise ModuleNotFoundError("switched off: " + name, name=name)
        return None

block = Block()
sys.meta_path.insert(0, block)
out = {}
for toggle, owned in homes.items():
    for name in [name for name in sys.modules if name.split(".")[0] == "cratekit"]:
        del sys.modules[name]
    block.prefixes = tuple(owned)
    from cratekit.cli import registry
    broken = []
    for entry in registry.landed_entries():
        if entry.module_id == toggle:
            continue
        try:
            module = importlib.import_module(entry.module)
            parser = argparse.ArgumentParser()
            getattr(module, entry.builder)(parser, entry)
            parser.format_help()
        except Exception:
            broken.append(entry.name)
    out[toggle] = sorted(broken)
print(json.dumps(out))
"""


def _drive_report(root: Path, rules: Rules, found: Sequence[Dangling], out) -> int:
    """Drive rule four for real and set it beside the static reading."""
    finished = subprocess.run(
        [sys.executable, "-c", _DRIVE, json.dumps(rules.homes)],
        cwd=root,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(root / "src")},
    )
    if finished.returncode != 0:
        print(
            "\nthe driven reading could not run; it imports Cratekit, so it needs the "
            "environment the suite runs in:\n" + finished.stderr.strip()[-600:],
            file=out,
        )
        return 1
    driven = json.loads(finished.stdout.strip().splitlines()[-1])
    print("\ndriven in a fresh interpreter, against the static reading:", file=out)
    differing = 0
    for item in found:
        static, real = set(item.verbs), set(driven.get(item.toggle, ()))
        differing += static != real
        said = "the same" if static == real else (
            f"{len(static)} static; driven only: {sorted(real - static)}; "
            f"static only: {sorted(static - real)}"
        )
        print(f"  {item.toggle:<11} {len(real):3d} verbs driven, {said}", file=out)
    return 1 if differing else 0


def outside_report(root: Path, owned: Sequence[str], *, where: bool, out) -> int:
    sources = read_sources(root, [SOURCE, "tests", "scripts"])
    missing = [path for path in owned if path not in sources]
    if missing:
        print("not a tracked Python file under src/cratekit, tests or scripts:", file=out)
        for path in missing:
            print(f"  {path}", file=out)
        return 2
    grouped: dict[tuple[str, str], list[OutsideUse]] = collections.defaultdict(list)
    for use in outside_uses(sources, owned):
        grouped[(use.target, use.name)].append(use)
    print(
        f"{len(grouped)} names of {len(owned)} files are used outside them, "
        f"{sum(is_private(name) for _, name in grouped)} of them private (marked _)",
        file=out,
    )
    for (target, name), uses in sorted(grouped.items()):
        users = sorted({use.user for use in uses})
        source = sum(user.startswith(SOURCE) for user in users)
        print(
            f"{'_' if is_private(name) else ' '} {target}.{name}  {len(users)} files "
            f"({source} source, {len(users) - source} tests and scripts)",
            file=out,
        )
        for user in users if where else ():
            lines = sorted({use.line for use in uses if use.user == user})
            print(f"      {user}:{','.join(map(str, lines))}", file=out)
    return 0


def _allowance_line(
    root: Path, directory: str, found: Mapping[str, Lines], out
) -> bool:
    """Print one allowance's state. True when something stands beyond it."""
    allowed = read_allowances(root, directory)
    still = sum(
        sum(pruned(found.get(package, collections.Counter()), lines).values())
        for package, lines in allowed.items()
    )
    beyond = _total(over_allowance(found, allowed))
    print(
        f"  allowance: {_total(allowed)} lines in {len(allowed)} files, {still} still found; "
        f"beyond the allowance: {beyond}",
        file=out,
    )
    return beyond > 0


def _lines_line(scope: str, texts: Mapping[str, str], out) -> None:
    total = sum((count_lines(text) for text in texts.values()), LineCount())
    code, docstring, comment, blank = _kinds(total)
    print(
        f"  {total.lines} lines in {len(texts)} files under {scope} (code {code}, "
        f"docstring {docstring}, comment {comment}, blank {blank})",
        file=out,
    )


def table_report(root: Path, out) -> int:
    """Points 2 to 5 of U290 in one print. Exit 1 when an allowance or the ceiling is exceeded."""
    source, tree, rules, verbs = _load(root)
    print("point 2, size", file=out)
    _lines_line(SOURCE, source, out)
    over = sum(len(text.splitlines()) > LARGE_FILE for text in source.values())
    print(f"  outside {VENDOR}; {over} files over {LARGE_FILE} lines", file=out)

    copies = Copies(source)
    print("point 3, duplication", file=out)
    print(
        f"  exact blocks of {BLOCK_LINES} logical lines or more: {duplicates_line(copies)}",
        file=out,
    )
    exceeded = _allowance_line(root, DUPLICATION_ALLOWANCES, copies.held(), out)

    print("point 4, seams", file=out)
    for label, count in seam_counts(tree, rules, verbs).items():
        print(f"  {count:6d}  {label}", file=out)
    found = import_findings(tree, rules, verbs)
    exceeded = _allowance_line(root, IMPORT_ALLOWANCES, found, out) or exceeded
    over = len({name for used in core_names(tree).values() for name in used})
    over = max(0, over - rules.names_ceiling)
    print(f"  core names over the ceiling: {over}", file=out)
    exceeded = exceeded or over > 0

    tests = read_sources(root, ["tests"])
    print("point 5, tests", file=out)
    _lines_line("tests", tests, out)
    print(
        f"  {sum(count_test_functions(text) for text in tests.values())} test functions; the "
        "suite's time is read from cloud_battery.py's own summary line and the kill set "
        "by the reader of U297, neither of them here",
        file=out,
    )
    return 1 if exceeded else 0


def prune_report(root: Path, packages: Sequence[str], out) -> int:
    """Lower the named packages' allowance files to what is still found."""
    source, tree, rules, verbs = _load(root)
    readings = (
        (DUPLICATION_ALLOWANCES, Copies(source).held()),
        (IMPORT_ALLOWANCES, import_findings(tree, rules, verbs)),
    )
    status = 0
    # A package is named by an allowance file's own stem, so one that left the
    # tree can still be pruned and a path to another directory's file cannot.
    known = {path.stem for directory, _ in readings for path in (root / directory).glob("*.txt")}
    for package in packages:
        paths = [(root / directory / f"{package}.txt", found) for directory, found in readings]
        if package not in known:
            print(f"{package}: no allowance file by that name", file=out)
            status = 2
            continue
        for path, found in paths:
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            allowed = parse_allowance(text)
            kept = pruned(found.get(package, collections.Counter()), allowed)
            removed = sum(allowed.values()) - sum(kept.values())
            if removed:
                path.write_text(render_allowance(allowance_header(text), kept), encoding="utf-8")
            print(
                f"{path.relative_to(root)}: {removed} lines removed, {sum(kept.values())} left",
                file=out,
            )
    return status


# ── The command line ────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="refactor_measure.py",
        description="The one measure of U290's refactor: lines, copied blocks and seams.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    lines = commands.add_parser("lines", help="lines by kind, per package and per file")
    lines.add_argument("paths", nargs="*", help=f"files or directories; default {SOURCE} and tests")
    lines.add_argument("--files", action="store_true", help="list every file, largest first")

    duplicates = commands.add_parser("duplicates", help="exact repeated blocks of logical lines")
    duplicates.add_argument("paths", nargs="*", help=f"files or directories; default {SOURCE}")
    duplicates.add_argument("--min", type=int, default=BLOCK_LINES, dest="size", metavar="N")
    duplicates.add_argument("--renamed", action="store_true", help="also print the renamed reading")
    duplicates.add_argument("--list", type=int, default=0, dest="listed", metavar="N")
    duplicates.add_argument("--where", metavar="DIGEST", help="say where one allowed window stands")

    imports = commands.add_parser("imports", help="the seam counts the import rules hold")
    imports.add_argument("--names", action="store_true", help="list every core name used")
    drive = "also drive rule four in a fresh interpreter; needs Cratekit importable"
    imports.add_argument("--drive", action="store_true", help=drive)

    outside = commands.add_parser("outside", help="names of these files used outside them")
    outside.add_argument("files", nargs="+")
    outside.add_argument("--where", action="store_true", help="list each using file and line")

    commands.add_parser("table", help="points 2 to 5 of U290 in one print")

    prune = commands.add_parser("prune", help="lower packages' allowance files to what is left")
    prune.add_argument("packages", nargs="+")
    return parser


def main(argv: Sequence[str] | None = None, *, root: Path = REPO_ROOT, out=None) -> int:
    out = out if out is not None else sys.stdout
    args = build_parser().parse_args(argv)
    empty = [scope for scope in getattr(args, "paths", ()) if not python_files(root, scope)]
    if empty:
        print("no Python file this reads is at or under: " + ", ".join(empty), file=out)
        return 2
    if args.command == "lines":
        scopes = args.paths or [SOURCE, "tests"]
        for position, scope in enumerate(scopes):
            if len(scopes) > 1:
                print(("\n" if position else "") + f"{scope}:", file=out)
            lines_report(read_sources(root, [scope]), files=args.files, out=out)
        return 0
    if args.command == "duplicates":
        sources = read_sources(root, args.paths or [SOURCE])
        if args.where:
            where = Copies(sources, size=args.size).describe(args.where)
            print(where or f"{args.where} is not a repeated window here", file=out)
            return 0 if where else 1
        for renamed in (False, True) if args.renamed else (False,):
            duplicates_report(sources, size=args.size, renamed=renamed, listed=args.listed, out=out)
        return 0
    if args.command == "imports":
        return imports_report(root, names=args.names, drive=args.drive, out=out)
    if args.command == "outside":
        return outside_report(root, args.files, where=args.where, out=out)
    if args.command == "table":
        return table_report(root, out)
    return prune_report(root, args.packages, out)


if __name__ == "__main__":
    raise SystemExit(main())
