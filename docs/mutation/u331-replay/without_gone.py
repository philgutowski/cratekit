"""Write a before table without the rows a unit merged from main removed, for `killset.py check`.

U331 (#980) measured its kill set replay before on `main` at b8d6d1d8 and after
on its branch, which merged `main` at e0573a66. Between the two, U343 removed
twelve guards with their tests (the key floor, the key stage, two rename
discards and the head in the title). Those kills are U343's to account for,
not this card's, so `check` reads a before table without them, and this
script writes it. It refuses unless every row it leaves out is:

* named under `[[dropped]]` in the after row file with a reason that opens
  `gone at the head, removed by`, a reason a person wrote;
* killed in the before table, so nothing already lost is hidden;
* gone from `main` itself: its `old` text occurs nowhere in its file at MAIN
  (read with `git show`, which is only read), so `main` without this card has
  lost it too, and no move by this card could be the cause.

A row whose line still stands but whose mutant reads a name `main` removed
is named in GONE-ON-MAIN, a TOML file of `[[gone]]` entries with `id`,
`absent` and `reason`. It is left out only when it was killed before, its
`new` text holds `absent`, its file at the before table's head holds
`absent`, and its file at MAIN does not: the guard has nothing left to
hold on `main`, so a kill after is the name's absence and not the guard.

It runs no test and writes nothing but OUT, whose header lists each row left
out with its reason.

    python docs/mutation/u331-replay/without_gone.py BEFORE.json AFTER-ROWS.toml MAIN OUT [GONE-ON-MAIN]
"""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path

GONE = "gone at the head, removed by"


def _show(rev: str, path: str) -> str:
    shown = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=False)
    return shown.stdout if shown.returncode == 0 else ""


def _rid(row: dict) -> str:
    source = row.get("source")
    return f"{Path(source['table']).stem}.{source['id']}" if isinstance(source, dict) else row["id"]


def main(argv: list[str]) -> int:
    before_path, rows_path, main_rev, out, *extra = argv
    before = json.loads(Path(before_path).read_text(encoding="utf-8"))
    spec = tomllib.loads(Path(rows_path).read_text(encoding="utf-8"))
    gone = {d["id"]: d["reason"] for d in spec.get("dropped", []) if d["reason"].startswith(GONE)}
    if len(gone) != len(spec.get("dropped", [])):
        raise SystemExit(f"{rows_path}: a dropped row has no reason opening {GONE!r}")
    absent: dict[str, dict] = {}
    for path in extra:
        for entry in tomllib.loads(Path(path).read_text(encoding="utf-8")).get("gone", []):
            absent[entry["id"]] = entry
    kept, left_out = [], []
    for row in before["rows"]:
        rid = _rid(row)
        named = absent.get(rid) or absent.get(row["id"])
        if named is not None:
            text = named["absent"]
            if row.get("status") not in ("killed", "collect-error") or not row.get("deaths"):
                raise SystemExit(f"{row['id']}: not killed before, so leaving it out is refused")
            then = _show(before["head"], row["file"])
            now = _show(main_rev, row["file"])
            if text not in row["new"] or text not in then or text in now:
                raise SystemExit(
                    f"{row['id']}: {text!r} must be in its new text and its file at "
                    f"{before['head']}, and gone from it at {main_rev}"
                )
            left_out.append({"id": row["id"], "file": row["file"], "reason": named["reason"]})
            continue
        if rid not in gone and row["id"] not in gone:
            kept.append(row)
            continue
        if row.get("status") not in ("killed", "collect-error") or not row.get("deaths"):
            raise SystemExit(f"{row['id']}: not killed before, so leaving it out would hide nothing and is refused")
        shown = subprocess.run(
            ["git", "show", f"{main_rev}:{row['file']}"], capture_output=True, text=True, check=False
        )
        if shown.returncode == 0 and row["old"] in shown.stdout:
            raise SystemExit(f"{row['id']}: its text still stands in {row['file']} at {main_rev}")
        left_out.append({"id": row["id"], "file": row["file"], "reason": gone.get(rid) or gone[row["id"]]})
    if len(left_out) != len(gone) + sum(
        1 for row in before["rows"] if row["id"] in absent or _rid(row) in absent
    ):
        raise SystemExit(f"{len(gone)} gone rows named, {len(left_out)} found in {before_path}")
    before["rows"] = kept
    before["left_out_as_gone_on_main"] = left_out
    before["left_out_note"] = (
        f"written by without_gone.py from {Path(before_path).name}: {len(left_out)} killed rows left out, "
        f"each named gone in {Path(rows_path).name} with its text absent from its file at {main_rev}, "
        f"or named in {', '.join(Path(p).name for p in extra) or 'no other file'} with a name its "
        f"mutant reads absent from its file at {main_rev}"
    )
    Path(out).write_text(json.dumps(before, indent=2) + "\n", encoding="utf-8")
    print(f"{len(kept)} rows kept, {len(left_out)} left out as gone on {main_rev}: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
