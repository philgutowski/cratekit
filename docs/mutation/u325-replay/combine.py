"""Combine U325's replay batches into one table for `scripts/killset.py check`.

U325 (#930) measured U298's kill set replay in batches packed by subset, each
sized to finish inside a two hour job, beside the rows #855 measured before
the split. `killset.py check` reads one table a side, so this joins the
batches' tables into one. It refuses anything that would make the joined
table say more than its parts: two heads, a batch the driver found invalid,
a batch it did not finish (only the partial sidecars #855 left, named with
`--partial`, may be unfinished, and only their measured rows are carried),
or two rows from one source. It runs no test and writes nothing but OUT.

    python docs/mutation/u325-replay/combine.py OUT NAME TABLE ... [--partial TABLE ...]
        [--superseded ID ...]

A row named by `--superseded` is one a partial table holds that a finished
batch measured again, for a reason the record gives (#855's README asks for
a row killed only by an inode bound test, under no scratch copy, to be
measured again against one). The partial table's row is left out, the
finished batch's row stands, and the header lists each, so nothing is
replaced silently. A superseded id that no finished batch measured again is
refused.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    out, name, *rest = argv
    full, partial, superseded, into = [], [], [], None
    for item in rest:
        if item in ("--partial", "--superseded"):
            into = partial if item == "--partial" else superseded
            continue
        (into if into is not None else full).append(item if into is superseded else Path(item))
    dropped = []
    batches, rows, mapped, seen, heads = [], [], [], set(), set()
    for path in [*partial, *full]:
        table = json.loads(path.read_text(encoding="utf-8"))
        reason = table.get("invalid_reason") or ""
        if table.get("valid") is not True:
            raise SystemExit(f"{path}: the driver found the batch invalid: {reason}")
        if reason and not (path in partial and reason == "in progress"):
            raise SystemExit(f"{path}: not a finished batch: {reason}")
        heads.add(table.get("head"))
        for row in table.get("rows", []):
            if path in partial and row.get("id") in superseded:
                dropped.append({"id": row.get("id"), "from": table.get("name"), "status": row.get("status")})
                continue
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
                "finished": path in full,
                "rows": len(table.get("rows", [])),
                "control": control.get("status"),
                "control_deaths": control.get("deaths"),
                "baseline_source": table.get("baseline_source"),
                "subset_baselines": table.get("subset_baselines"),
                "known_source": table.get("known_source"),
                "when": table.get("when"),
            }
        )
    again = {row.get("id") for row in rows}
    missing = [one for one in superseded if one not in again or one not in {d["id"] for d in dropped}]
    if missing:
        raise SystemExit(f"superseded but not measured again, or not in a partial table: {missing}")
    if len(heads) != 1:
        raise SystemExit(f"the batches were measured on more than one commit: {sorted(heads)}")
    combined = {
        "name": name,
        "pass_kind": "replay",
        "head": heads.pop(),
        "valid": True,
        "invalid_reason": "",
        "combined_from": batches,
        "superseded": dropped,
        "rows": rows,
        "mapped": mapped,
    }
    Path(out).write_text(json.dumps(combined, indent=1) + "\n", encoding="utf-8")
    print(f"{len(rows)} rows from {len(batches)} batches written to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
