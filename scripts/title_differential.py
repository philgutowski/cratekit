"""Run the title matcher of a base revision against the tree's and print every difference.

U280 redesigned the record shop title matcher (`cratekit.tagging.titles`)
beside the one it replaced, and this is how the two were held to each other:
every file name of a corpus is matched against every catalogue row of it by
both matchers, and every pair one matches and the other does not is printed,
so each difference is read rather than sampled.

THE BASE is `src/cratekit/tagging/searchers.py` at ``--base`` (by default the
commit before U280's matcher, whose `_readings` and `_meet` it reads), loaded
from git into a module of its own, so nothing of the base is copied into the
tree. THE TREE is `cratekit.tagging.titles` as it stands.

THE CORPUS is every short string constant of the tagging tests (title
positions and every other string, unfiltered, as R-1631's and R-1646's own
differentials were), wrapped in the name shapes the naming verb and a
library write, each with the artist written each way a credit is, plus a
seeded set of generated adversarial names. The rows are the same strings,
read as a catalogue writes them, and the artists' own names.

EVERY PAIR IS DECIDED by an index: each side's names (word tuples) and
splits map to the rows that carry them, so a pair either matcher could
match is found without a quadratic scan, and each candidate is then decided
by the matcher itself.

Usage:

    .venv/bin/python scripts/title_differential.py [--base REV] [--out FILE]
        [--generated N] [--beatport N]

Prints a summary per shape and writes every difference, one per line, to
``--out``: ``lost`` (the base matched, the tree does not) or ``gained``, then
the artist tag, the file's name and the row. Exit 0 always: a difference is a
finding to read, not a failure.
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

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from cratekit.tagging import titles  # noqa: E402

#: The commit before U280, whose matcher is the base by default.
DEFAULT_BASE = "7237b92c"

#: The tagging test files whose string constants are the corpus.
CORPUS_FILES = (
    "tests/test_title_matcher.py",
    "tests/test_catalogue_searcher.py",
    "tests/test_discogs_searcher.py",
    "tests/test_tagging_engine.py",
    "tests/test_tag_suggest.py",
    "tests/test_tag_workers.py",
    "tests/test_tag_guess.py",
    "tests/test_tag_rows.py",
    "tests/test_tag_remap.py",
    "tests/test_genre_retag.py",
    "tests/test_published_genre.py",
    "tests/test_tag_folder_copyright.py",
    "tests/test_catalogue_app.py",
    "tests/test_tags.py",
)

#: The artists a name is wrapped with: the tag, and the credit as the name
#: writes it. A differential that wraps titles only in the exact artist string
#: measures a fixture (R-1636's solution).
ARTISTS = (
    ("Bernard Badie", "Bernard Badie"),
    ("Bernard Badie", "Bernard Badie & Tide"),
    ("Bernard Badie", "B. Badie"),
    ("Bernard Badie & Tide", "Bernard Badie"),
    ("The Black Madonna", "Black Madonna"),
    ("Âme", "Ame"),
    ("Tide", "Tide"),
    ("", "Bernard Badie"),
)

#: The name shapes a file's title tag or its name takes, {a} the credit and
#: {t} the title: the library's head, the naming verb's marker, an artist
#: before or after, an album, a track number alone or glued, a feature credit
#: on either side, a version part, a trailing head.
SHAPES = (
    "{t}",
    "08A - 124 - {t}",
    "{a} - {t}",
    "08A - 124 - {a} - {t}",
    "{t} - {a}",
    "{t} - {a} - Sun Path",
    "08A - 124 - {t} - {a} - Sun Path",
    "{a} - Sun Path - 02 {t}",
    "{a} - Sun Path - 02 - {t}",
    "{a} - Summer Mix - 01 {t}",
    "01 - {a} - {t}",
    "01 {a} - {t}",
    "[MP3] {a} - {t}",
    "08A - 124 - [MP3] {a} - {t}",
    "{a} feat. Tide - {t}",
    "{t} feat. Tide - {a}",
    "{a} - Tide - {t}",
    "{a} - {a} - {t}",
    "{t} - Original Mix",
    "08A - 124 - {t} - Vocal Mix",
    "{a} - {t} - Original Mix",
    "{t} - 08A - 124",
)

#: Rows every corpus carries beside its strings: the artists' self titled
#: rows, and their versions written each way a catalogue writes one.
EXTRA_ROWS = (
    "Bernard Badie",
    "Bernard Badie (Extended Mix)",
    "Bernard Badie - Vocal Mix",
    "Tide",
    "Black Madonna",
    "Ame",
    "Sun Path",
    "Summer Mix",
    "Original Mix",
    "Vocal",
    "Vocal Mix",
)

#: The words a generated name is built from.
GENERATED_WORDS = (
    "sunrise", "mood", "tide", "love", "dub", "club", "vocal", "mix", "original",
    "extended", "remix", "edit", "radio", "part", "2", "1999", "2014", "remaster",
    "909", "01", "02", "007", "08a", "124", "feat", "ft", "intro", "session",
    "bernard", "badie", "black", "madonna", "the", "&", "x", "vs", "and", "with",
)


def load_base(revision: str) -> ModuleType:
    """The base's ``searchers`` module, loaded from git as a module of its own."""
    source = subprocess.run(
        ["git", "show", f"{revision}:src/cratekit/tagging/searchers.py"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    name = "cratekit.tagging._differential_base"
    spec = importlib.util.spec_from_loader(name, loader=None)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(source, f"{revision}:searchers.py", "exec"), module.__dict__)
    return module


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


class Side:
    """One matcher: how it reads a file and a row, the keys a match needs one
    of, and the decision itself."""

    def __init__(self, read_file, read_row, file_keys, row_keys, decide) -> None:
        self.read_file = read_file
        self.read_row = read_row
        self.file_keys = file_keys
        self.row_keys = row_keys
        self.decide = decide


def base_side(base: ModuleType) -> Side:
    def file_keys(read) -> Iterable[object]:
        names, shed, splits = read
        return [*names, *shed, *(("split", split) for split in splits)]

    def row_keys(read) -> Iterable[object]:
        names, shed, splits = read
        return [*names, *shed, *(("split", split) for split in splits)]

    return Side(
        lambda name, artist: base._readings(name, searched=True, artist=artist),
        lambda row: base._readings(row, searched=False),
        file_keys,
        row_keys,
        base._meet,
    )


def tree_side() -> Side:
    def file_keys(read: titles.FileName) -> Iterable[object]:
        keys: list[object] = []
        for title in (*read.titles, *((read.whole,) if read.whole else ())):
            keys.extend(title.names)
            keys.extend(title.bare)
        keys.extend(("split", split) for split in read.splits)
        return keys

    def row_keys(read: titles.Row) -> Iterable[object]:
        keys: list[object] = []
        for title in read.titles:
            keys.extend(title.names)
            keys.extend(title.bare)
        keys.extend(("split", split) for split in read.splits)
        return keys

    return Side(titles.read_file, titles.read_row, file_keys, row_keys, titles.matches)


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--out", type=Path, default=Path("title-differential.tsv"))
    parser.add_argument("--generated", type=int, default=20000)
    parser.add_argument("--beatport", type=int, default=0)
    parser.add_argument("--shapes", default="", help="only shapes whose index is listed, comma separated")
    args = parser.parse_args(argv)

    base = load_base(args.base)
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

    old = matched(base_side(base), names, rows)
    new = matched(tree_side(), names, rows)
    per_shape: Counter = Counter()
    lines: list[str] = []
    for number, (shape, artist, name, _) in enumerate(names):
        for row in sorted(old[number] - new[number]):
            per_shape[(shape, "lost")] += 1
            lines.append(f"lost\t{shape}\t{artist}\t{name}\t{rows[row]}")
        for row in sorted(new[number] - old[number]):
            per_shape[(shape, "gained")] += 1
            lines.append(f"gained\t{shape}\t{artist}\t{name}\t{rows[row]}")
        per_shape[(shape, "both")] += len(old[number] & new[number])
    for shape in (*shapes, "generated"):
        print(
            f"{per_shape[(shape, 'both')]:>8} both {per_shape[(shape, 'lost')]:>7} lost "
            f"{per_shape[(shape, 'gained')]:>6} gained  {shape}"
        )
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
