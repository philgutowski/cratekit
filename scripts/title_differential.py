"""Run the title matcher of a base revision against the tree's and print every difference.

Every file name of a corpus is matched against every catalogue row by both
matchers (U280), and every pair one matches and the other does not is printed.
THE BASE is `searchers.py` at ``--base`` (by default the commit before U280),
or with ``--titles-base REV`` (U324) `titles.py` at that revision, which also
compares `named_versions`, `writes_version` and `question`; loaded from git, so
nothing of the base is copied into the tree. THE TREE is `cratekit.tagging.titles`.

THE CORPUS is every short string constant of the tagging tests, wrapped in the
name shapes below with each artist credit, plus seeded generated names; the
rows are the same strings and the artists' own names. An index of each side's
keys finds the candidates, and the matcher itself decides each.

Usage:

    .venv/bin/python scripts/title_differential.py [--base REV] [--out FILE]
        [--generated N] [--beatport N]

Writes every difference to ``--out``: ``lost`` or ``gained``, the shape, the
artist tag, the name, the row and the tree's outcome. Exit 0 always.
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import random
import subprocess
import sys
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable
from pathlib import Path
from types import ModuleType
from typing import NamedTuple

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from cratekit.tagging import titles  # noqa: E402

#: The commit before U280, whose matcher is the base by default.
DEFAULT_BASE = "7237b92c"

#: The tagging test files whose string constants are the corpus.
CORPUS_FILES = (
    "tests/test_title_matcher.py", "tests/test_catalogue_searcher.py",
    "tests/test_discogs_searcher.py", "tests/test_tagging_engine.py", "tests/test_tag_suggest.py",
    "tests/test_tag_workers.py", "tests/test_tag_guess.py", "tests/test_tag_rows.py",
    "tests/test_tag_remap.py", "tests/test_genre_retag.py", "tests/test_published_genre.py",
    "tests/test_tag_folder_copyright.py", "tests/test_catalogue_app.py", "tests/test_tags.py",
    "tests/test_discogs_version.py",
)

#: The artists a name is wrapped with: the tag, and the credit as the name
#: writes it, since the exact artist string alone measures a fixture (R-1636), a
#: letter NFKD leaves alone each way round (U324), and an initial that folds to two.
ARTISTS = (
    ("Bernard Badie", "Bernard Badie"), ("Bernard Badie", "Bernard Badie & Tide"),
    ("Bernard Badie", "B. Badie"), ("Bernard Badie & Tide", "Bernard Badie"),
    ("The Black Madonna", "Black Madonna"), ("Âme", "Ame"), ("Trentemøller", "Trentemoller"),
    ("Trentemoller", "Trentemøller"), ("Þórður Badie", "Þ. Badie"), ("Tide", "Tide"),
    ("", "Bernard Badie"),
)

#: The name shapes a file's title tag or its name takes, {a} the credit and {t} the title.
SHAPES = (
    "{t}", "08A - 124 - {t}", "{a} - {t}", "08A - 124 - {a} - {t}", "{t} - {a}",
    "{t} - {a} - Sun Path", "08A - 124 - {t} - {a} - Sun Path", "{a} - Sun Path - 02 {t}",
    "{a} - Sun Path - 02 - {t}", "{a} - Summer Mix - 01 {t}", "01 - {a} - {t}", "01 {a} - {t}",
    "[MP3] {a} - {t}", "08A - 124 - [MP3] {a} - {t}", "{a} feat. Tide - {t}",
    "{t} feat. Tide - {a}", "{a} - Tide - {t}", "{a} - {a} - {t}", "{t} - Original Mix",
    "08A - 124 - {t} - Vocal Mix", "{a} - {t} - Original Mix", "{t} - 08A - 124",
)

#: Rows every corpus carries: the artists' self titled rows and their versions.
EXTRA_ROWS = (
    "Bernard Badie", "Bernard Badie (Extended Mix)", "Bernard Badie - Vocal Mix", "Tide",
    "Black Madonna", "Ame", "Sun Path", "Summer Mix", "Original Mix", "Vocal", "Vocal Mix",
)

#: The words a generated name is built from.
GENERATED_WORDS = (
    "sunrise", "mood", "tide", "love", "dub", "club", "vocal", "mix", "original",
    "extended", "remix", "edit", "radio", "part", "2", "1999", "2014", "remaster",
    "909", "01", "02", "007", "08a", "124", "feat", "ft", "intro", "session",
    "bernard", "badie", "black", "madonna", "the", "&", "x", "vs", "and", "with",
)


def _load_from_git(revision: str, file: str, name: str) -> ModuleType:
    """``src/cratekit/tagging/<file>`` at ``revision``, loaded as a module of its own."""
    source = subprocess.run(
        ["git", "show", f"{revision}:src/cratekit/tagging/{file}"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    spec = importlib.util.spec_from_loader(name, loader=None)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(source, f"{revision}:{file}", "exec"), module.__dict__)
    return module


def load_base(revision: str) -> ModuleType:
    """The base's ``searchers`` module."""
    return _load_from_git(revision, "searchers.py", "cratekit.tagging._differential_base")


def load_titles_base(revision: str) -> ModuleType:
    """The base's ``titles`` module (U324)."""
    return _load_from_git(revision, "titles.py", "cratekit.tagging._differential_titles_base")


def corpus() -> list[str]:
    """Every short string constant of the tagging tests, whole and once."""
    found: dict[str, None] = {}
    for relative in CORPUS_FILES:
        path = REPO / relative
        if not path.exists():
            continue
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                value = node.value
                if 0 < len(value) <= 60 and "\n" not in value and "://" not in value:
                    found.setdefault(value)
    return list(found)


def generated(count: int, seed: int = 280) -> list[str]:
    """Adversarial names from a small grammar of the words that decide a match."""
    chance = random.Random(seed)
    names: list[str] = []
    for _ in range(count):
        parts = []
        for _ in range(chance.choice((1, 1, 2, 2, 3, 4))):
            part = " ".join(chance.choice(GENERATED_WORDS) for _ in range(chance.choice((1, 1, 2, 3))))
            if chance.random() < 0.2:
                part = f"{part} ({' '.join(chance.choice(GENERATED_WORDS) for _ in range(2))})"
            if chance.random() < 0.05:
                part = f"[{chance.choice(GENERATED_WORDS)}] {part}"
            parts.append(part)
        names.append(" - ".join(parts))
    return names


Keys = Callable[[str], Iterable[object]]


class Side(NamedTuple):
    """One matcher: how it reads a file and a row, the keys a match needs, the decision."""

    read_file: Callable
    read_row: Callable
    file_keys: Keys
    row_keys: Keys
    decide: Callable


def base_side(base: ModuleType) -> Side:
    def keys(read) -> Iterable[object]:
        names, shed, splits = read
        return [*names, *shed, *(("split", split) for split in splits)]

    return Side(
        lambda name, artist: base._readings(name, searched=True, artist=artist),
        lambda row: base._readings(row, searched=False),
        keys,
        keys,
        base._meet,
    )


def tree_side(module: ModuleType = titles) -> Side:
    """A side reading through a ``titles`` module, the tree's unless another is given."""

    def keys(read_titles, splits) -> list[object]:
        found: list[object] = []
        for title in read_titles:
            found.extend(title.names)
            found.extend(title.bare)
        found.extend(("split", split) for split in splits)
        return found

    def file_keys(read: titles.FileName) -> Iterable[object]:
        return keys((*read.titles, *((read.whole,) if read.whole else ())), read.splits)

    def row_keys(read: titles.Row) -> Iterable[object]:
        return keys(read.titles, read.splits)

    return Side(module.read_file, module.read_row, file_keys, row_keys, module.matches)


def matched(side: Side, names: list[tuple[str, str, str, str]], rows: list[str]) -> dict[int, set[int]]:
    """For each name, the rows the side matches, every candidate decided."""
    read_rows = [side.read_row(row) for row in rows]
    index: dict[object, set[int]] = defaultdict(set)
    for number, read in enumerate(read_rows):
        for key in side.row_keys(read):
            index[key].add(number)
    found: dict[int, set[int]] = {}
    for number, (_, artist, name, _) in enumerate(names):
        read = side.read_file(name, artist)
        candidates: set[int] = set()
        for key in side.file_keys(read):
            candidates |= index.get(key, set())
        found[number] = {row for row in candidates if side.decide(read, read_rows[row])}
    return found


def beatport(base: ModuleType, names: list[tuple[str, str, str, str]], rows: list[str], count: int) -> Counter:
    """Beatport's scorer over sampled single row pages, base against tree: half
    the rows the name's own title, written with a mix or not, half any row."""
    from cratekit.tagging import searchers

    chance = random.Random(1646)
    tally: Counter = Counter()
    mixes = ("", "Original Mix", "Extended Mix", "Vocal Mix", "Radio Edit")
    differences: list[str] = []
    for _ in range(count):
        _, artist, name, title = chance.choice(names)
        track = {
            "track_name": title if chance.random() < 0.5 else chance.choice(rows),
            "mix_name": chance.choice(mixes),
            "genre": [{"genre_name": "House"}],
            "artists": [{"artist_name": artist or "Bernard Badie"}],
        }
        old = base._beatport_best([track], artist, name) is not None
        new = searchers._beatport_best([track], artist, name) is not None
        tally[(old, new)] += 1
        if old != new:
            differences.append(
                f"beatport-{'lost' if old else 'gained'}\t{artist}\t{name}\t{track['track_name']}\t{track['mix_name']}"
            )
    tally["lines"] = differences  # type: ignore[assignment]
    return tally


def folded_readers(
    base: ModuleType,
    names: list[tuple[str, str, str, str]],
    rows: list[str],
    old: dict[int, set[int]],
    new: dict[int, set[int]],
) -> Counter:
    """Every other reader of the name fold, base against tree (U324).

    Each difference is a line: ``question``, ``named``, ``writes`` or
    ``writes-alone``, then the artist, the name, the row and both answers.
    """
    tally: Counter = Counter()
    lines: list[str] = []
    for number, (_, artist, name, _) in enumerate(names):
        asked = (base.question(name, artist), titles.question(name, artist))
        if (asked[0].artist, asked[0].title, asked[0].read.value) != (
            asked[1].artist,
            asked[1].title,
            asked[1].read.value,
        ):
            tally["question"] += 1
            lines.append(f"question\t{artist}\t{name}\t\t{asked[0]}\t{asked[1]}")
        both = old[number] & new[number]
        if not both:
            continue
        named_base = base.named_versions(base.read_file(name, artist))
        named_tree = titles.named_versions(titles.read_file(name, artist))
        if named_base != named_tree:
            tally["named"] += 1
            lines.append(f"named\t{artist}\t{name}\t\t{sorted(named_base)}\t{sorted(named_tree)}")
        if not named_base and not named_tree:
            continue
        for row in sorted(both):
            tally["pairs"] += 1
            for kind, titled in (("writes", True), ("writes-alone", False)):
                was = base.writes_version(rows[row], named_base, titled=titled)
                now = titles.writes_version(rows[row], named_tree, titled=titled)
                if was != now:
                    tally[kind] += 1
                    lines.append(f"{kind}\t{artist}\t{name}\t{rows[row]}\t{was}\t{now}")
    tally["lines"] = lines  # type: ignore[assignment]
    return tally


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--out", type=Path, default=Path("title-differential.tsv"))
    parser.add_argument("--generated", type=int, default=20000)
    parser.add_argument("--beatport", type=int, default=0)
    parser.add_argument("--shapes", default="", help="only shapes whose index is listed, comma separated")
    parser.add_argument(
        "--titles-base",
        default="",
        help="hold the tree's titles module to its own source at this revision (U324)",
    )
    args = parser.parse_args(argv)

    if args.titles_base:
        base = load_base(args.titles_base)
        base_titles = load_titles_base(args.titles_base)
        # The base's searchers read its own titles: each function looks the
        # module up when it runs, so Beatport's scorer is held to it as well.
        base.titles = base_titles
        side = tree_side(base_titles)
    else:
        base = load_base(args.base)
        base_titles = None
        side = base_side(base)
    titles_found = corpus()
    rows = list(dict.fromkeys([*titles_found, *EXTRA_ROWS]))
    shapes = SHAPES
    if args.shapes:
        shapes = tuple(SHAPES[int(index)] for index in args.shapes.split(","))
    names: list[tuple[str, str, str, str]] = []
    for shape in shapes:
        for artist, credit in ARTISTS:
            for title in titles_found:
                names.append((shape, artist, shape.format(a=credit, t=title), title))
    chance = random.Random(791)
    for name in generated(args.generated):
        for artist, _ in ARTISTS[:2] + ARTISTS[-2:]:
            names.append(("generated", artist, name, chance.choice(rows)))
    print(f"corpus: {len(titles_found)} strings, {len(rows)} rows, {len(names)} names")

    old = matched(side, names, rows)
    new = matched(tree_side(), names, rows)
    per_shape: Counter = Counter()
    lines: list[str] = []
    for number, (shape, artist, name, _) in enumerate(names):
        if old[number] != new[number]:
            outcome = titles.read_file(name, artist).outcome.value
        for row in sorted(old[number] - new[number]):
            per_shape[(shape, "lost")] += 1
            lines.append(f"lost\t{shape}\t{artist}\t{name}\t{rows[row]}\t{outcome}")
        for row in sorted(new[number] - old[number]):
            per_shape[(shape, "gained")] += 1
            lines.append(f"gained\t{shape}\t{artist}\t{name}\t{rows[row]}\t{outcome}")
        per_shape[(shape, "both")] += len(old[number] & new[number])
    for shape in (*shapes, "generated"):
        print(
            f"{per_shape[(shape, 'both')]:>8} both {per_shape[(shape, 'lost')]:>7} lost "
            f"{per_shape[(shape, 'gained')]:>6} gained  {shape}"
        )
    if base_titles is not None:
        readers = folded_readers(base_titles, names, rows, old, new)
        lines.extend(readers.pop("lines"))
        print(f"readers: {dict(readers)}")
    if args.beatport:
        tally = beatport(base, names, rows, args.beatport)
        beat_lines = tally.pop("lines")
        lines.extend(beat_lines)
        print(f"beatport: {dict(tally)}")
    args.out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    print(f"{len(lines)} difference(s) written to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
