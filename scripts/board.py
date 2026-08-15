#!/usr/bin/env python3
"""The build board, as a tool.

The board at https://github.com/users/<owner>/projects/2 is the work queue for
this repository. This script is how a session reads that queue and how the board
is kept true to the repository.

The dependency graph is NOT stored here. It is parsed out of the issue bodies,
which carry a `**Depends on:** #18 (U18), #31 (U31)` line. That is deliberate:
a committed copy of the graph is a second representation of one fact, and two
representations of one fact are how they come to disagree. The cost is that a
body which loses its line becomes invisible to the graph, so `audit` fails when
a unit issue does not parse rather than quietly treating it as dependency-free.

Subcommands:

    next            the ready queue, ranked by how much each unit releases
    show N          one issue's brief
    start N         branch, mark In Progress, print the closing trailer
    sync            make the board match the repository, idempotent
    audit           report drift, exit 1 if the board is lying

`sync` is safe to run at any time and is the one that matters. Everything the
board says about readiness is derived from issue closure state and the graph, so
`sync` can always rebuild it from scratch and never needs to be trusted to have
run before.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from collections import deque
from pathlib import Path

PROJECT_NUMBER = "2"

# Status option ids on the project's single-select Status field. Looked up once
# at startup rather than pinned, because an option id changes if the option is
# recreated and a pinned id fails silently by writing nothing.
STATUS_ORDER = ["Ready", "In Progress", "Blocked", "Attended", "Done"]

DEPENDS_RE = re.compile(r"^\*\*Depends on:\*\*\s*(.+)$", re.MULTILINE)
CLOSES_WITH_RE = re.compile(r"^\*\*Closes with:\*\*\s*(.+)$", re.MULTILINE)
ISSUE_REF_RE = re.compile(r"#(\d+)")
UNIT_TITLE_RE = re.compile(r"^U(\d+):")


class Fail(Exception):
    pass


def gh(*args: str, parse: bool = False):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise Fail(f"gh {' '.join(args)}\n{result.stderr.strip()}")
    out = result.stdout.strip()
    return json.loads(out) if parse and out else out


def repo_slug() -> tuple[str, str]:
    """Owner and name from the git remote, never hardcoded."""
    data = gh("repo", "view", "--json", "owner,name", parse=True)
    return data["owner"]["login"], data["name"]


# --------------------------------------------------------------------------
# reading the board


def load_issues() -> list[dict]:
    return gh(
        "issue",
        "list",
        "--state",
        "all",
        "--limit",
        "300",
        "--json",
        "number,title,state,body,labels",
        parse=True,
    )


def parse_deps(body: str) -> list[int] | None:
    """Issue numbers this one depends on, or None if the body declares nothing.

    None and [] mean different things. [] is a unit with no dependencies, which
    U1 genuinely is. None is a body that lost its line, which is a defect the
    audit has to see rather than treat as "depends on nothing".
    """
    match = DEPENDS_RE.search(body or "")
    if not match:
        return None
    return [int(n) for n in ISSUE_REF_RE.findall(match.group(1))]


def closes_with(body: str) -> list[int]:
    """A residual finding waits on whichever unit closes it, if one does."""
    match = CLOSES_WITH_RE.search(body or "")
    return [int(n) for n in ISSUE_REF_RE.findall(match.group(1))] if match else []


def build_graph(issues: list[dict]) -> dict:
    """Every issue, keyed by number, with its parsed edges and derived state."""
    by_number = {}
    for issue in issues:
        labels = {label["name"] for label in issue["labels"]}
        is_unit = "unit" in labels
        by_number[issue["number"]] = {
            "number": issue["number"],
            "title": issue["title"],
            "closed": issue["state"] == "CLOSED",
            "labels": labels,
            "unit": is_unit,
            "attended": "attended" in labels,
            "deps": parse_deps(issue["body"]) if is_unit else closes_with(issue["body"]),
            "body": issue["body"],
        }

    # reverse edges
    for node in by_number.values():
        node["unblocks"] = []
    for node in by_number.values():
        for dep in node["deps"] or []:
            if dep in by_number:
                by_number[dep]["unblocks"].append(node["number"])

    # transitive reach: how much of the remaining build this one releases,
    # counting only what is still open. Direct count under-ranks a unit whose
    # single dependent is itself the gateway to a whole phase.
    for node in by_number.values():
        seen: set[int] = set()
        queue = deque(node["unblocks"])
        while queue:
            nxt = queue.popleft()
            if nxt in seen or nxt not in by_number:
                continue
            seen.add(nxt)
            queue.extend(by_number[nxt]["unblocks"])
        node["reach"] = len({n for n in seen if not by_number[n]["closed"]})

    for node in by_number.values():
        node["open_deps"] = [
            d for d in (node["deps"] or []) if d in by_number and not by_number[d]["closed"]
        ]
    return by_number


def derive_status(node: dict, current: str | None) -> str:
    """What the board should say, from closure state and the graph alone."""
    if node["closed"]:
        return "Done"
    if node["attended"]:
        return "Attended"
    if not node["unit"]:
        # A residual finding waits on whichever unit closes it, and is Ready when
        # nothing does, because then it is somebody's to pick up directly.
        return "Blocked" if node["open_deps"] else "Ready"
    if current == "In Progress":
        # A unit on a branch stays on a branch. Recomputing it back to Ready
        # is how a session loses track of work already underway.
        return "In Progress"
    return "Blocked" if node["open_deps"] else "Ready"


def pending_units() -> dict[int, list[str]]:
    """Which units the pending register still says owe a module.

    `tests/_pending.py` is the countdown for guards written before the code they
    govern. An entry there is the repository asserting, in a file the suite
    enforces, that a unit has not landed. Read by ast rather than imported, so an
    audit never executes test-tree code.
    """
    source = Path(__file__).resolve().parent.parent / "tests" / "_pending.py"
    if not source.exists():
        return {}
    tree = ast.parse(source.read_text())
    owed: dict[int, list[str]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.AnnAssign) and not isinstance(node, ast.Assign):
            continue
        targets = [node.target] if isinstance(node, ast.AnnAssign) else node.targets
        if not any(isinstance(t, ast.Name) and t.id == "PENDING" for t in targets):
            continue
        if not isinstance(node.value, ast.Dict):
            continue
        for key, value in zip(node.value.keys, node.value.values):
            if not isinstance(value, ast.Tuple) or not value.elts:
                continue
            unit = value.elts[0]
            name = key.value if isinstance(key, ast.Constant) else "?"
            if isinstance(unit, ast.Constant) and isinstance(unit.value, str):
                match = re.match(r"U(\d+)$", unit.value)
                if match:
                    owed.setdefault(int(match.group(1)), []).append(str(name))
    return owed


# --------------------------------------------------------------------------
# writing the board


def project_context(owner: str) -> dict:
    fields = gh(
        "project", "field-list", PROJECT_NUMBER, "--owner", owner, "--format", "json", parse=True
    )
    status = next(f for f in fields["fields"] if f["name"] == "Status")
    unblocks = next((f for f in fields["fields"] if f["name"] == "Unblocks"), None)
    project = gh(
        "project", "view", PROJECT_NUMBER, "--owner", owner, "--format", "json", parse=True
    )
    return {
        "id": project["id"],
        "url": project["url"],
        "status_field": status["id"],
        "options": {o["name"]: o["id"] for o in status["options"]},
        "unblocks_field": unblocks["id"] if unblocks else None,
    }


def project_items(owner: str) -> dict:
    data = gh(
        "project",
        "item-list",
        PROJECT_NUMBER,
        "--owner",
        owner,
        "--limit",
        "300",
        "--format",
        "json",
        parse=True,
    )
    items = {}
    for item in data["items"]:
        content = item.get("content") or {}
        number = content.get("number")
        if number is not None:
            items[number] = {"id": item["id"], "status": item.get("status")}
    return items


# --------------------------------------------------------------------------
# commands


def cmd_next(args) -> int:
    owner, _ = repo_slug()
    graph = build_graph(load_issues())
    try:
        items = project_items(owner)
    except Fail:
        # A repository-scoped token cannot read a user-owned project. The queue
        # itself comes from the issues and is unaffected; the only thing lost is
        # knowing what is already on a branch, so say so rather than imply the
        # list is complete.
        items = {}
        print("(cannot read the project board with this token, so work already")
        print(" in progress is not shown below)")
        print()

    ready = [
        n
        for n in graph.values()
        if n["unit"] and not n["closed"] and not n["open_deps"]
    ]
    in_progress = [
        n for n in graph.values() if items.get(n["number"], {}).get("status") == "In Progress"
    ]
    busy = {n["number"] for n in in_progress}
    ready = [n for n in ready if n["number"] not in busy]
    ready.sort(key=lambda n: (-n["reach"], -len(n["unblocks"]), n["number"]))

    if in_progress:
        print("Already in progress, finish this before starting anything:")
        for node in in_progress:
            print(f"  #{node['number']:<3} {node['title']}")
        print()

    if not ready:
        print("Nothing is ready. Every open unit is waiting on another one.")
        return 0

    print(f"Ready now, ranked by how much of the build each one releases ({len(ready)} units):")
    print()
    for rank, node in enumerate(ready, 1):
        marker = "->" if rank == 1 else "  "
        print(f"{marker} #{node['number']:<3} {node['title']}")
        print(
            f"      releases {node['reach']} open unit(s), "
            f"{len(node['unblocks'])} of them directly"
        )
    print()
    top = ready[0]
    print(f"Take #{top['number']}. Start it with:")
    print(f"    .venv/bin/python scripts/board.py start {top['number']}")
    return 0


def cmd_show(args) -> int:
    graph = build_graph(load_issues())
    node = graph.get(args.number)
    if not node:
        raise Fail(f"no issue #{args.number}")
    print(f"#{node['number']} {node['title']}")
    print(f"state: {'closed' if node['closed'] else 'open'}")
    if node["open_deps"]:
        print(f"blocked by: {', '.join('#' + str(d) for d in node['open_deps'])}")
    print()
    print(node["body"])
    return 0


def slugify(title: str) -> str:
    body = title.split(":", 1)[-1].strip().lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", body)).strip("-")[:40]


def cmd_start(args) -> int:
    owner, _ = repo_slug()
    graph = build_graph(load_issues())
    node = graph.get(args.number)
    if not node:
        raise Fail(f"no issue #{args.number}")
    if node["closed"]:
        raise Fail(f"#{args.number} is already closed")
    if node["open_deps"]:
        blockers = ", ".join(f"#{d} ({graph[d]['title'].split(':')[0]})" for d in node["open_deps"])
        raise Fail(f"#{args.number} is blocked by {blockers}. Pick something ready.")

    match = UNIT_TITLE_RE.match(node["title"])
    prefix = f"u{match.group(1)}" if match else f"issue{node['number']}"
    branch = f"unit/{prefix}-{slugify(node['title'])}"

    current = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    if current != "main":
        raise Fail(f"on branch {current}, not main. Land or park that work first.")
    dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout
    if dirty.strip():
        raise Fail("the working tree is dirty. Commit or stash before starting a unit.")

    subprocess.run(["git", "checkout", "-b", branch], check=True)

    ctx = project_context(owner)
    items = project_items(owner)
    item = items.get(node["number"])
    if item:
        gh(
            "project",
            "item-edit",
            "--id",
            item["id"],
            "--project-id",
            ctx["id"],
            "--field-id",
            ctx["status_field"],
            "--single-select-option-id",
            ctx["options"]["In Progress"],
        )
    print()
    print(f"Branch {branch} is checked out and #{node['number']} is In Progress.")
    print()
    print("Read the brief:")
    print(f"    .venv/bin/python scripts/board.py show {node['number']}")
    print()
    print("The battery, before you merge anything:")
    print("    .venv/bin/ruff check src tests scripts")
    print("    .venv/bin/python -m pytest")
    print("    .venv/bin/python scripts/scan_repo.py")
    print()
    print("End the merge commit message with this line and nothing will need doing by hand:")
    print()
    print(f"    Closes #{node['number']}")
    print()
    print("Pushing main then closes the issue, and the board cascade flips every unit")
    print("this one unblocks from Blocked to Ready on its own.")
    return 0


def residual_titles() -> dict[int, str]:
    """Every ``## R-N.`` heading in the residual file, by number.

    Read as text rather than parsed as a document, because the only structure
    this needs is the heading line and the file is append only by rule.
    """
    source = Path(__file__).resolve().parent.parent / "docs" / "residual-findings.md"
    if not source.exists():
        return {}
    found: dict[int, str] = {}
    for line in source.read_text().splitlines():
        match = re.match(r"^## R-(\d+)\.\s*(.+?)\s*$", line)
        if match:
            found[int(match.group(1))] = match.group(2)
    return found


def repointed_residuals(graph: dict) -> list[str]:
    """Residual issues whose title no longer matches the finding they number.

    A RESIDUAL'S NUMBER LIVES IN ITS ISSUE TITLE, which is a surface the
    repository cannot see. Residual numbers are append only for exactly this
    reason, and METHOD records that the sweep certifying the last renumber
    checked `src`, `tests` and `scripts` and missed this one: a renumber
    silently repoints every issue title at a different finding, and nothing in
    the tree can observe it.

    So the check is not that a residual has an issue. Most do not, and should
    not: the board is the build and the residual file is the ledger. The check
    is that an issue which DOES exist still names what its number now points at.
    """
    file_titles = residual_titles()
    found = []
    for node in sorted(graph.values(), key=lambda n: n["number"]):
        match = re.match(r"^R-(\d+):\s*(.+?)\s*$", node["title"])
        if not match:
            continue
        number, issue_title = int(match.group(1)), match.group(2)
        if number not in file_titles:
            found.append(
                f"#{node['number']} R-{number}\n"
                f"      the issue names it, docs/residual-findings.md has no such finding"
            )
        elif file_titles[number] != issue_title:
            found.append(
                f"#{node['number']} R-{number} names a different finding than the file does\n"
                f"      issue: {issue_title[:72]}\n"
                f"      file : {file_titles[number][:72]}"
            )
    return found


def contradictions(graph: dict) -> list[str]:
    """What the repository and the board disagree about, that a sync cannot fix.

    Every value the board derives comes from issue closure state, so closure
    state is the one INPUT and nothing checks it. `tests/_pending.py` is the
    repository asserting, in a file the suite enforces, that a named unit has not
    finished. A closed issue for such a unit is the board claiming work landed
    that the repository says did not, and it cascades: one wrong close moved four
    units to Ready.

    This is kept apart from drift on purpose. Drift is a derived value that fell
    out of date and `sync` repairs it. A contradiction is two sources of truth
    disagreeing, and repairing it automatically would mean picking one to
    overwrite, which is how the wrong one wins silently.
    """
    found = []
    for uid, modules in sorted(pending_units().items()):
        node = graph.get(uid)
        if node and node["unit"] and node["closed"]:
            found.append(
                f"#{uid} {node['title'][:44]}\n"
                f"      closed, but tests/_pending.py still owes it {', '.join(modules)}"
            )
    return found + repointed_residuals(graph)


def reconcile(owner: str, apply: bool, labels_only: bool = False) -> list[str]:
    """Compare the board against the repository. Returns the drift found.

    `labels_only` drops every project-board call. A repository-scoped token
    cannot reach a user-owned project, so CI running as GITHUB_TOKEN can still
    keep the ready/blocked labels true even though it cannot move a card. The
    labels are the half that has to be right, because they are what the queue
    is derived from; the card is the view of it.
    """
    graph = build_graph(load_issues())
    ctx = None if labels_only else project_context(owner)
    items = {} if labels_only else project_items(owner)
    name = repo_slug()[1]
    drift: list[str] = []

    # The one thing the board cannot derive from itself. Every other value here
    # is computed from closure state, so closure state is the input and nothing
    # checks it. A closed issue whose unit still owes a module in the pending
    # register is the board claiming work landed that the repository says did
    # not, and it cascades: four units went Ready off one such close.

    for number, node in sorted(graph.items()):
        item = items.get(number)
        if not item and not labels_only:
            drift.append(f"#{number} {node['title'][:50]} is not on the board")
            if apply:
                url = f"https://github.com/{owner}/{name}/issues/{number}"
                added = gh(
                    "project", "item-add", PROJECT_NUMBER, "--owner", owner,
                    "--url", url, "--format", "json", parse=True,
                )
                items[number] = {"id": added["id"], "status": None}
                item = items[number]
            else:
                continue

        want = derive_status(node, item["status"]) if item else None
        if item and item["status"] != want:
            drift.append(f"#{number} status is {item['status']}, should be {want}")
            if apply:
                gh(
                    "project", "item-edit", "--id", item["id"],
                    "--project-id", ctx["id"], "--field-id", ctx["status_field"],
                    "--single-select-option-id", ctx["options"][want],
                )

        if node["unit"]:
            if node["deps"] is None:
                drift.append(
                    f"#{number} has no 'Depends on' line, so it is invisible to the graph"
                )
            want_labels = set()
            if not node["closed"]:
                want_labels = {"blocked"} if node["open_deps"] else {"ready"}
            has = node["labels"] & {"ready", "blocked"}
            if has != want_labels:
                drift.append(
                    f"#{number} labels are {sorted(has) or 'none'}, "
                    f"should be {sorted(want_labels) or 'none'}"
                )
                if apply:
                    for label in has - want_labels:
                        gh("issue", "edit", str(number), "--remove-label", label)
                    for label in want_labels - has:
                        gh("issue", "edit", str(number), "--add-label", label)

        if item and ctx and ctx["unblocks_field"] and apply:
            gh(
                "project", "item-edit", "--id", item["id"],
                "--project-id", ctx["id"], "--field-id", ctx["unblocks_field"],
                "--number", str(len(node["unblocks"])),
            )
    return drift


def cmd_sync(args) -> int:
    owner, _ = repo_slug()
    drift = reconcile(owner, apply=True, labels_only=args.labels_only)
    if not drift:
        print("The board already matched the repository. Nothing changed.")
        return 0
    print(f"Corrected {len(drift)} item(s):")
    for line in drift:
        print(f"  {line}")
    return 0


def cmd_audit(args) -> int:
    owner, _ = repo_slug()
    drift = reconcile(owner, apply=False, labels_only=args.labels_only)
    graph = build_graph(load_issues())
    units = [n for n in graph.values() if n["unit"]]
    done = sum(1 for n in units if n["closed"])
    ready = sum(1 for n in units if not n["closed"] and not n["open_deps"])
    print(f"{len(units)} units: {done} done, {ready} ready, {len(units) - done - ready} blocked")
    clashes = contradictions(graph)

    if drift:
        print()
        print(f"DRIFT, {len(drift)} item(s). Derived values that fell out of date:")
        for line in drift:
            print(f"  {line}")
        print()
        print("Fix it with: .venv/bin/python scripts/board.py sync")

    if clashes:
        print()
        print(f"CONTRADICTION, {len(clashes)} item(s). A sync cannot fix these:")
        for line in clashes:
            print(f"  {line}")
        print()
        print("Each one is a decision, not a repair. Either reopen the issue because")
        print("the unit is not finished, or clear its tests/_pending.py entry because")
        print("it is. Overwriting one from the other would let the wrong one win.")

    if not drift and not clashes:
        print("The board matches the repository.")
        return 0
    return 2 if clashes else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("next", help="the ready queue, ranked by leverage").set_defaults(func=cmd_next)
    show = sub.add_parser("show", help="print one issue's brief")
    show.add_argument("number", type=int)
    show.set_defaults(func=cmd_show)
    start = sub.add_parser("start", help="branch and mark In Progress")
    start.add_argument("number", type=int)
    start.set_defaults(func=cmd_start)
    sync = sub.add_parser("sync", help="make the board match the repository")
    sync.add_argument(
        "--labels-only",
        action="store_true",
        help="skip the project board, for a token that cannot reach it",
    )
    sync.set_defaults(func=cmd_sync)
    audit = sub.add_parser("audit", help="report drift, exit 1 if the board is lying")
    audit.add_argument("--labels-only", action="store_true", help="skip the project board")
    audit.set_defaults(func=cmd_audit)
    args = parser.parse_args()
    try:
        return args.func(args)
    except Fail as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
