#!/usr/bin/env python3
"""U337: the survey's kill set, read against every replay under U290, and the rows it still owes.

The survey of U290 counted 7,093 live killed rows at `ff8e5ec` (`killset.py
--repo-root <a checkout of ff8e5ec> list`). Each card under the epic replayed
the rows of the files it owned, so a row whose file no card owned was never
measured after. This script reads, for every survey row, every replay table
under `docs/mutation/` (at the top level and in this directory) that names it
by its source table and id, or failing that by its file and text, and says
where it stands.

    survey.py --survey-root <ff8e5ec checkout> owed
    survey.py --survey-root <ff8e5ec checkout> rows --out-dir DIR
    survey.py --survey-root <ff8e5ec checkout> join --out-dir DIR

`owed` prints each survey row that has no killed measurement after, and no
mapping: the newest replay of it on an after side read it not killed, or no
replay after names it. `rows` writes the replay row files for those of them
that are live on this checkout, in batches: the rows whose tests need the
analysis extra, any row of `r926.json` (its mutant can leave a folder outside
the test roots) alone, and the rest in groups by file. `join` writes the two
tables `killset.py check` reads for the whole survey: `survey-before.json`,
every survey row owed a kill as its own table recorded it, and
`survey-after.json`, the newest measurement of each after U290's cards and
this card's batches, with every mapping they made. A survey row not owed a
kill is left out of the before table and named in its `excluded` list with
the reason, so the count `check` prints and that list add up to 7,093.

Nothing here runs a test or writes a source file; it only reads tables and
the two trees, and writes row files and tables.
"""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
import tomllib
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import killset as K  # noqa: E402

TABLES = REPO_ROOT / "docs" / "mutation"

#: The batch of rows naming a test file that skips whole without the analysis
#: extra (`pytest.importorskip` of numpy or librosa at module level).
ANALYSIS_EXTRA = "analysis"


def side_of(name: str) -> str:
    if "before" in name:
        return "before"
    return "after"


def replay_tables() -> list[tuple[Path, dict]]:
    found = []
    for path in sorted([*TABLES.glob("*.json"), *TABLES.glob("*/*.json")]):
        table = K.load_table(path)
        if table is None or table.get("pass_kind") != K.REPLAY:
            continue
        if path.parent == HERE and path.name.startswith("survey-"):
            continue
        if path.name == "u337-replay.json":
            continue  # the batches it joins are read from this directory
        found.append((path, table))
    return found


class Measurements:
    """Every replay row, by the source it came from and by its text."""

    def __init__(self) -> None:
        self.by_source: dict[tuple[str, str], list[tuple]] = defaultdict(list)
        self.by_text: dict[tuple, list[tuple]] = defaultdict(list)
        self.mapped: dict[tuple[str, str], list[tuple[Path, dict, dict]]] = defaultdict(list)
        for path, table in replay_tables():
            when = str(table.get("when") or "")
            side = side_of(path.name)
            for row in table["rows"]:
                if not isinstance(row, dict):
                    continue
                entry = (when, str(path.relative_to(REPO_ROOT)), side, row, table)
                source = K.source_of(row)
                if source is not None:
                    self.by_source[source].append(entry)
                self.by_text[(row.get("file"), row.get("old"), row.get("new"))].append(entry)
            for mapping in table.get("mapped") or []:
                source = K.source_of(mapping) if isinstance(mapping, dict) else None
                if source is not None:
                    self.mapped[source].append((path, table, mapping))

    def of(self, row: K.Recorded) -> tuple[list[tuple], str]:
        found = self.by_source.get(row.source)
        if found:
            return sorted(found, key=lambda one: (one[0], one[1])), "source"
        found = self.by_text.get(row.anchor.key)
        if found:
            return sorted(found, key=lambda one: (one[0], one[1])), "text"
        return [], ""


def survey_rows(survey_root: Path) -> list[K.Recorded]:
    return [row for row in K.read_kill_set(survey_root).rows if row.state == K.LIVE]


def standing(row: K.Recorded, seen: Measurements) -> dict:
    measured, how = seen.of(row)
    after = [one for one in measured if one[2] == "after"]
    newest = after[-1] if after else None
    return {
        "measured": measured,
        "how": how,
        "after": after,
        "newest": newest,
        "held": bool(newest and K.killed(newest[3])) or bool(seen.mapped.get(row.source)),
    }


def owed(survey: list[K.Recorded], seen: Measurements) -> list[K.Recorded]:
    return [row for row in survey if not standing(row, seen)["held"]]


def cmd_owed(args) -> int:
    seen = Measurements()
    survey = survey_rows(args.survey_root)
    now = {row.source: row for row in K.read_kill_set(REPO_ROOT).rows}
    rows = owed(survey, seen)
    print(f"{len(survey)} survey rows, {len(rows)} with no killed measurement after and no mapping")
    for row in rows:
        here = now.get(row.source)
        print(f"{here.state if here else 'absent':<9} {row.anchor.file}  {row.table}  {row.id}")
    return 0


def needs_extra(tests: tuple[str, ...]) -> bool:
    """Whether any of a row's test files skips whole without the analysis extra.

    Such a row is measured where the extra is installed, so every test it
    names runs; a container without it would run only the rest.
    """
    for name in {one.split("::", 1)[0] for one in tests}:
        path = REPO_ROOT / name
        head = (
            "\n".join(path.read_text(encoding="utf-8").splitlines()[:60]) if path.exists() else ""
        )
        if 'importorskip("librosa")' in head or 'importorskip("numpy")' in head:
            return True
    return False


def recorded_text(source: tuple[str, str]) -> tuple:
    table = K.load_table(TABLES / source[0]) or {"rows": []}
    for row in table["rows"]:
        if isinstance(row, dict) and str(row.get("id")) == source[1]:
            return (row.get("file"), row.get("old"), row.get("new"))
    return (None, None, None)


def moved_reason(row: K.Recorded, seen: Measurements) -> str:
    """The `moved` reason the replay that anchored a row where it now is wrote, or none
    when the row stands at the text its own table recorded."""
    if row.anchor.key == recorded_text(row.source):
        return ""
    for entry in reversed(
        sorted(seen.by_source.get(row.source, []), key=lambda one: (one[0], one[1]))
    ):
        replayed = entry[3]
        if (replayed.get("file"), replayed.get("old"), replayed.get("new")) == row.anchor.key:
            reason = str(replayed.get("moved") or "").strip()
            if reason:
                return reason
    raise SystemExit(f"{row.table} {row.id}: anchored away from its text with no moved reason")


def cmd_rows(args) -> int:
    seen = Measurements()
    survey = survey_rows(args.survey_root)
    wanted = {row.source for row in owed(survey, seen)}
    now = [
        row
        for row in K.read_kill_set(REPO_ROOT).rows
        if row.source in wanted and row.state == K.LIVE
    ]
    groups: dict[str, list[K.Recorded]] = defaultdict(list)
    plain: list[K.Recorded] = []
    for row in sorted(now, key=lambda one: (one.anchor.file, one.table, one.id)):
        if row.table == "r926.json":
            groups["r926"].append(row)
        elif needs_extra(row.anchor.tests):
            groups[ANALYSIS_EXTRA].append(row)
        else:
            plain.append(row)
    by_file: dict[str, list[K.Recorded]] = defaultdict(list)
    for row in plain:
        by_file[row.anchor.file].append(row)
    size = -(-len(plain) // args.batches)
    batch, count = 1, 0
    for name in sorted(by_file):
        if count >= size and batch < args.batches:
            batch, count = batch + 1, 0
        groups[str(batch)] += by_file[name]
        count += len(by_file[name])
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for group, rows in sorted(groups.items()):
        name = f"u337-{group}"
        body: list[str] = []
        for row in rows:
            body += K.render_row(
                row.source, row.description, row.surface, row.anchor, moved_reason(row, seen)
            )
        K.write_rows(args.out_dir / f"{name}-rows.toml", name, body)
        print(f"{name}: {len(rows)} rows in {len({row.anchor.file for row in rows})} files")
    return 0


# ---------------------------------------------------------------------------
# join: the two tables `killset.py check` reads for the whole survey
# ---------------------------------------------------------------------------

#: Survey rows not owed a kill, each with the reason, kept beside this script.
EXCLUDED = HERE / "excluded.toml"


def read_excluded() -> dict[tuple[str, str], str]:
    data = tomllib.loads(EXCLUDED.read_text(encoding="utf-8")) if EXCLUDED.exists() else {}
    found: dict[tuple[str, str], str] = {}
    for entry in data.get("excluded", []):
        key = (entry["table"], entry["id"])
        if key in found:
            raise SystemExit(f"{EXCLUDED.name} names {key} twice")
        reason = str(entry.get("reason") or "").strip()
        if not reason:
            raise SystemExit(f"{EXCLUDED.name}: {key} gives no reason")
        found[key] = reason
    return found


#: Survey rows held by a killed row of a unit's own table rather than a replay,
#: each with the row that holds it and why, kept beside this script.
MAPPED = HERE / "mapped.toml"


def read_mapped() -> dict[tuple[str, str], dict]:
    data = tomllib.loads(MAPPED.read_text(encoding="utf-8")) if MAPPED.exists() else {}
    return {(one["table"], one["id"]): one for one in data.get("mapped", [])}


def text_of(row: dict) -> tuple:
    return (row.get("file"), row.get("old"), row.get("new"))


def vouched_reason(row: K.Recorded, measured: list[tuple], pick: dict) -> str:
    """A reason for a row measured at another text than its survey text, from the
    chain of replays that carried it there, or none when the chain breaks.

    The chain starts at the survey's text and the tests that killed it there.
    Each killed replay at a text already in the chain adds its killers, since
    one exact text occurring once is one guard however its tests were renamed.
    A replay at a new text joins the chain only on the rule `check` holds a move
    to: a test the chain already holds killed it there, or a person wrote its
    `moved` reason. The reason names each move and the test or reason that
    carried it.
    """
    texts = {(row.anchor.file, row.anchor.old, row.anchor.new)}
    killers = set(row.killers)
    steps: list[str] = []
    for when, table, _side, replayed, _ in measured:
        if not K.killed(replayed):
            continue
        text = text_of(replayed)
        mine = K.killer_names(replayed)
        if text not in texts:
            own = str(replayed.get("moved") or "").strip()
            shared = sorted(killers & mine)
            if shared:
                steps.append(f"{table} ({when}) at {text[0]}, killed by {shared[0]}")
            elif own and not own.startswith(K.AUTOMATIC_MOVE):
                steps.append(f"{table} ({when}) at {text[0]}, whose reason is: {own}")
            else:
                continue
            texts.add(text)
        killers |= mine
    if text_of(pick) not in texts:
        return ""
    return (
        "The survey's guard, carried by its replays, each move by a test that had killed "
        "it at the text before or by a reason a person wrote: " + "; ".join(steps) + "."
    )


def git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "--short=8", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def table_head(name: str, note: str) -> dict:
    return {
        "name": name,
        "pass_kind": K.REPLAY,
        "head": git_head(),
        "when": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "valid": True,
        "invalid_reason": "",
        "note": note,
    }


def recorded_row(source: tuple[str, str]) -> dict:
    table = K.load_table(TABLES / source[0]) or {"rows": []}
    for row in table["rows"]:
        if isinstance(row, dict) and str(row.get("id")) == source[1]:
            return row
    raise SystemExit(f"{source[0]} holds no row {source[1]}")


def cmd_join(args) -> int:
    seen = Measurements()
    survey = survey_rows(args.survey_root)
    excluded = read_excluded()
    by_hand = read_mapped()
    known = {row.source for row in survey}
    stray = sorted(set(excluded) - known)
    if stray:
        raise SystemExit(f"{EXCLUDED.name} names rows the survey does not hold: {stray}")
    before_rows, after_rows, mapped, left_out, unheld = [], {}, [], [], []
    for row in survey:
        if row.source in excluded:
            left_out.append(
                {
                    "source": {"table": row.table, "id": row.id},
                    "id": K.row_id(row.source),
                    "file": row.anchor.file,
                    "reason": excluded[row.source],
                }
            )
            continue
        was = copy.deepcopy(recorded_row(row.source))
        was["id"] = K.row_id(row.source)
        was["source"] = {"table": row.table, "id": row.id}
        before_rows.append(was)
        measured, how = seen.of(row)
        after = [one for one in measured if one[2] == "after"]
        if after:
            pick = copy.deepcopy(after[-1][3])
            pick["id"] = K.row_id(row.source)
            pick["source"] = {"table": row.table, "id": row.id}
            pick["measured_in"] = after[-1][1]
            if how == "text":
                pick["matched_by"] = "its file and text, as U315 matched it"
            if text_of(pick) != text_of(was) and K.unvouched_move(row.killers, pick):
                reason = vouched_reason(row, measured, pick)
                if reason:
                    pick["moved"] = reason
            after_rows[row.source] = pick
        curated = by_hand.get(row.source)
        if curated is not None and not (after and K.killed(after[-1][3])):
            target = copy.deepcopy(recorded_row((curated["to_table"], curated["to_id"])))
            target["id"] = K.row_id((curated["to_table"], curated["to_id"]))
            target["measured_in"] = f"docs/mutation/{curated['to_table']}"
            after_rows[("", target["id"])] = target
            mapped.append(
                {
                    "source": {"table": row.table, "id": row.id},
                    "to": target["id"],
                    "reason": curated["reason"],
                }
            )
            continue
        held_by_map = seen.mapped.get(row.source)
        if held_by_map and not (after and K.killed(after[-1][3])):
            path, table, entry = held_by_map[-1]
            mapped.append(copy.deepcopy(entry))
            target = next(
                (
                    one
                    for one in table["rows"]
                    if isinstance(one, dict) and one.get("id") == entry.get("to")
                ),
                None,
            )
            if target is not None:
                key = K.source_of(target) or ("", str(target.get("id")))
                if key not in after_rows:
                    kept = copy.deepcopy(target)
                    kept["measured_in"] = str(path.relative_to(REPO_ROOT))
                    after_rows[key] = kept
        if not after and not held_by_map:
            unheld.append(row)
    if unheld and args.draft:
        drop = {row.source for row in unheld}
        before_rows = [one for one in before_rows if K.source_of(one) not in drop]
    elif unheld:
        for row in unheld:
            print(f"NO MEASUREMENT {row.anchor.file}  {row.table}  {row.id}")
        raise SystemExit(f"{len(unheld)} survey rows owed a kill have no measurement after")
    note = (
        f"The survey of U290 at ff8e5ec: {len(survey)} live killed rows, "
        f"{len(before_rows)} owed a kill and {len(left_out)} left out, each named under "
        "excluded with its reason. Each row as its own table recorded it."
    )
    before = table_head("survey-before", note)
    before["rows"] = before_rows
    before["excluded"] = left_out
    after_table = table_head(
        "survey-after",
        "The newest after measurement of each survey row owed a kill, from every replay "
        "table under docs/mutation (U290's cards and this card's batches), each naming "
        "the table it was measured in, with every mapping those tables made.",
    )
    after_table["rows"] = list(after_rows.values())
    after_table["mapped"] = mapped
    for name, table in (("survey-before.json", before), ("survey-after.json", after_table)):
        (args.out_dir / name).write_text(json.dumps(table, indent=1) + "\n", encoding="utf-8")
    print(
        f"{len(before_rows)} owed, {len(left_out)} left out, {len(after_rows)} after rows, {len(mapped)} mapped"
    )
    return 0


# ---------------------------------------------------------------------------
# combine: this card's batches as one replay table `killset.py` reads
# ---------------------------------------------------------------------------

#: The batches of this card, in the order they are joined.
BATCHES = (
    "u337-1",
    "u337-2",
    "u337-3",
    "u337-r926",
    "u337-analysis",
    "u337-librosa-1-0-0",
    "u337-moved",
)

#: A row measured again in a later batch, and the batch whose reading stands.
SUPERSEDED = {
    ("u264.json", "M1_fast_path_never"): "u337-librosa-1-0-0",
    ("u264.json", "M8_finite_check"): "u337-librosa-1-0-0",
}


def cmd_combine(args) -> int:
    """Join this card's batch tables into ``docs/mutation/u337-replay.json``.

    `killset.py` reads only the tables at the top of `docs/mutation/`, so a row
    this card anchored again is found there by the next `list` or `rows` only
    through this table. It refuses a batch that is missing, unfinished or
    invalid, and two rows from one source unless `SUPERSEDED` names the batch
    whose reading stands.
    """
    rows: dict[tuple[str, str], tuple[str, dict]] = {}
    heads, controls = [], []
    for name in BATCHES:
        path = HERE / f"{name}.json"
        table = K.read_measured(path)
        heads.append(f"{name} at {table.get('head')}")
        control = table.get("control") or {}
        controls.append(f"{name} {control.get('status')} ({control.get('deaths')} deaths)")
        for row in table["rows"]:
            key = K.source_of(row)
            if key is None:
                raise SystemExit(f"{name}: row {row.get('id')} names no source")
            if key in rows and SUPERSEDED.get(key) != name:
                if SUPERSEDED.get(key) == rows[key][0]:
                    continue
                raise SystemExit(f"{name}: {key} was measured in {rows[key][0]} too")
            kept = copy.deepcopy(row)
            kept["batch"] = name
            rows[key] = (name, kept)
    combined = table_head(
        "u337-replay",
        "U337's batches joined: "
        + "; ".join(heads)
        + ". Null controls: "
        + "; ".join(controls)
        + ". Each row names its batch under docs/mutation/u337-replay/.",
    )
    combined["rows"] = [row for _, row in rows.values()]
    out = TABLES / "u337-replay.json"
    out.write_text(json.dumps(combined, indent=1) + "\n", encoding="utf-8")
    print(f"{len(combined['rows'])} rows from {len(BATCHES)} batches written to {out.name}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--survey-root", type=Path, required=True)
    verbs = parser.add_subparsers(dest="verb", required=True)
    verbs.add_parser("owed").set_defaults(run=cmd_owed)
    rows = verbs.add_parser("rows")
    rows.add_argument("--out-dir", type=Path, default=HERE)
    rows.add_argument("--batches", type=int, default=3)
    rows.set_defaults(run=cmd_rows)
    verbs.add_parser("combine").set_defaults(run=cmd_combine)
    joined = verbs.add_parser("join")
    joined.add_argument("--out-dir", type=Path, default=HERE)
    joined.add_argument(
        "--draft", action="store_true", help="leave out rows with no measurement, to read the rest"
    )
    joined.set_defaults(run=cmd_join)
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv[1:])
    return args.run(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
