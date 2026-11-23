"""Combine U325's replay batches into one table for `scripts/killset.py check`.

U325 (#930) measured U298's kill set replay in batches packed by subset, each
sized to finish inside a two hour job, beside the rows #855 measured before
the split. `killset.py check` reads one table a side, so this joins the
batches' tables into one. It refuses anything that would make the joined
table say more than its parts: two heads, a batch the driver found invalid,
a batch it did not finish (only the partial sidecars #855 left, named with
`--partial`, may be unfinished, and only their measured rows are carried),
or two rows from one source. It runs no test and writes nothing but OUT.

    python docs/mutation/u325-replay/combine.py OUT NAME TABLE ...
        [--partial TABLE ...] [--again TABLE ...] [--superseded ID ...]

Tables after `--again` hold rows measured a second time for a reason the
record gives: a row #855 read as killed only by an inode bound test under no
scratch copy, or a row read killed only by the eight tests a directory left
at the filesystem root fails, measured again on a container that never had
it. Each id named by `--superseded` must stand in exactly one `--again`
table; its row in every other table is left out, the `--again` row stands,
and the header lists each row left out with its table and status, so nothing
is replaced silently. A superseded id no `--again` table holds is refused.

What it does not see: a table left off the command line, a table's own
`dropped` list, and a measurement that never finished (U325's first
`u325-after-l-24`, kept beside the batches as a partial). The record names
each table that went in and each that did not.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

FLAGS = ("--partial", "--again", "--superseded")


def main(argv: list[str]) -> int:
    out, name, *rest = argv
    groups: dict[str, list[str]] = {"": [], **{flag: [] for flag in FLAGS}}
    into = ""
    for item in rest:
        if item in FLAGS:
            into = item
            continue
        groups[into].append(item)
    full = [Path(p) for p in groups[""]]
    partial = [Path(p) for p in groups["--partial"]]
    again = [Path(p) for p in groups["--again"]]
    superseded = set(groups["--superseded"])

    batches, rows, mapped, dropped, seen, heads = [], [], [], [], set(), set()
    measured_again: dict[str, str] = {}
    for path in [*partial, *full, *again]:
        table = json.loads(path.read_text(encoding="utf-8"))
        reason = table.get("invalid_reason") or ""
        if table.get("valid") is not True:
            raise SystemExit(f"{path}: the driver found the batch invalid: {reason}")
        if reason and not (path in partial and reason == "in progress"):
            raise SystemExit(f"{path}: not a finished batch: {reason}")
        heads.add(table.get("head"))
        for row in table.get("rows", []):
            row_id = row.get("id")
            if row_id in superseded and path not in again:
                dropped.append(
                    {"id": row_id, "from": table.get("name"), "status": row.get("status")}
                )
                continue
            if path in again:
                if row_id in measured_again:
                    raise SystemExit(f"{row_id} is measured again in two tables")
                measured_again[row_id] = str(table.get("name"))
            source = row.get("source") or {}
            key = (source.get("table"), source.get("id"))
            if key in seen:
                raise SystemExit(f"{path}: a second row for {key}")
            seen.add(key)
            rows.append(row)
        mapped += table.get("mapped") or []
        control = table.get("control") or {}
        batches.append(
            {
                "name": table.get("name"),
                "finished": path not in partial,
                "measured_again": path in again,
                "rows": len(table.get("rows", [])),
                "control": control.get("status"),
                "control_deaths": control.get("deaths"),
                "baseline_source": table.get("baseline_source"),
                "subset_baselines": table.get("subset_baselines"),
                "known_source": table.get("known_source"),
                "when": table.get("when"),
            }
        )
    missing = sorted(one for one in superseded if one not in measured_again)
    if missing:
        raise SystemExit(f"superseded but measured again in no --again table: {missing}")
    if len(heads) != 1:
        raise SystemExit(f"the batches were measured on more than one commit: {sorted(heads)}")
    combined = {
        "name": name,
        "pass_kind": "replay",
        "head": heads.pop(),
        # The latest batch's time, which `killset.py list` dates a replay by.
        "when": max((str(b["when"] or "") for b in batches), default=""),
        "valid": True,
        "invalid_reason": "",
        "combined_from": batches,
        "superseded": dropped,
        "rows": rows,
        "mapped": mapped,
    }
    Path(out).write_text(json.dumps(combined, indent=1) + "\n", encoding="utf-8")
    print(
        f"{len(rows)} rows from {len(batches)} batches written to {out}; "
        f"{len(dropped)} rows left out for a measurement taken again"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
