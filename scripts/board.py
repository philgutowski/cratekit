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
    closing         refuse a `Closes #n` trailer while a register still owes Un

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


def planned_units() -> dict[int, list[str]]:
    """Which units the VERB REGISTRY still says owe a module.

    The second register, and until now nothing read it. `planned_in` on a registry
    entry is the same promise `tests/_pending.py` makes, written in a different
    file: this verb's module does not exist and unit U-n will land it. Three
    closed unit issues carry live markers between them and the board has never
    said a word, because `contradictions()` read one register and there are two.

    Read by ast rather than imported, for the same reason `pending_units` is: an
    audit must never execute the code it audits. Keyed on the MODULE rather than
    the verb, because one module carries several verbs and the obligation is the
    file.
    """
    source = Path(__file__).resolve().parent.parent / "src" / "cratekit" / "cli" / "registry.py"
    if not source.exists():
        return {}
    constants: dict[str, str] = {}
    tree = ast.parse(source.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            for target in node.targets:
                if isinstance(target, ast.Name) and isinstance(node.value.value, str):
                    constants[target.id] = node.value.value

    def literal(value: ast.AST) -> str | None:
        """The string this argument evaluates to, through one named constant.

        `ROUTING_CLI_UNIT` is a module-level constant precisely so four entries
        move together, so a reader that only understood literals would go blind
        on the entries most likely to be re-pointed.
        """
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            return value.value
        if isinstance(value, ast.Name):
            return constants.get(value.id)
        return None

    owed: dict[int, set[str]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or getattr(node.func, "id", None) != "Entry":
            continue
        fields = {kw.arg: kw.value for kw in node.keywords if kw.arg}
        planned = literal(fields["planned_in"]) if "planned_in" in fields else None
        module = literal(fields["module"]) if "module" in fields else None
        if not planned or not module:
            continue
        match = re.match(r"U(\d+)$", planned)
        if match:
            owed.setdefault(int(match.group(1)), set()).add(module)
    return {uid: sorted(modules) for uid, modules in owed.items()}


def owed_by_unit() -> dict[int, list[str]]:
    """Every module either register still owes, per unit, merged.

    Two registers exist and each one alone is a hole. `tests/_pending.py` holds
    guards waiting for their module; the verb registry holds verbs waiting for
    theirs. A unit can close clean against one while the other still owes it
    seven verbs, which is the state three closed issues are in right now.
    """
    merged: dict[int, set[str]] = {}
    for source in (pending_units(), planned_units()):
        for uid, modules in source.items():
            merged.setdefault(uid, set()).update(modules)
    return {uid: sorted(modules) for uid, modules in merged.items()}


# --------------------------------------------------------------------------
# the closing check: a trailer is refused BEFORE it closes anything


#: Every keyword GitHub closes an issue on, not the one this repository's
#: contract happens to use.
#:
#: The distinction cost a whole check. The first version matched `^Closes #n$`
#: and nothing else, on the reasoning that the contract says to write that exact
#: trailer. GitHub does not read the contract, and nine keywords times four
#: reference forms all close the issue and cascade every unit waiting on it.
CLOSING_KEYWORDS = ("close", "closes", "closed", "fix", "fixes", "fixed",
                    "resolve", "resolves", "resolved")

#: GitHub's THREE documented reference forms, plus the bare one. An earlier
#: version of this file widened the keywords and left the reference form alone,
#: then claimed in a commit message to recognize "the eleven ways somebody
#: actually types it". It recognized nine keywords times ONE form. Widening the
#: rest is a few characters, so it is cheaper to be right than to write down the
#: limitation.
#:
#: Ordered longest-first. At a given position the alternation tries branches left
#: to right, so the bare `#n` must come last or `owner/repo#36` would never be
#: reached.
REFERENCE_FORMS = (
    r"https?://github\.com/[\w.-]+/[\w.-]+/issues/(\d+)",
    r"[\w.-]+/[\w.-]+#(\d+)",
    r"GH-(\d+)",
    r"#(\d+)",
)

#: Keyword, optional colon, then a reference.
#:
#: The lookbehind rejects a keyword that is a URL PATH SEGMENT, so
#: `https://example.com/notes/fixes#36` is a link with a fragment rather than a
#: closing reference. That was a verified false refusal, and the whole cost of a
#: false refusal is somebody deleting the check.
CLOSES_RE = re.compile(
    r"(?<![/\w])\b(?:" + "|".join(CLOSING_KEYWORDS) + r")\b\s*:?\s*"
    r"(?:" + "|".join(REFERENCE_FORMS) + r")",
    re.IGNORECASE,
)

#: A comma list continuing from a keyword-anchored issue: `Closes #36, #33`.
#:
#: `[^\S\n]` IS HORIZONTAL WHITESPACE ONLY, and the distinction is the whole
#: correctness of this pattern. With `\s*` the continuation crossed newlines, so
#: a trailer followed by a blank line and a sentence beginning "and #33 stays
#: open" was read as a two-issue list and BOTH were refused. GitHub closes only
#: the first. The docstring below promises that explaining in a commit body why a
#: unit is still open must stay possible, and that is the exact sentence it
#: refused, so the code contradicted its own stated contract.
CONTINUED_RE = re.compile(
    r"[^\S\n]*(?:,|and)[^\S\n]*(?:" + "|".join(REFERENCE_FORMS) + r")",
    re.IGNORECASE,
)

#: Lines git itself strips from a commit message. The commit-msg hook is handed
#: the RAW file, comments and the verbose diff included, so a template line
#: reading `# Closes #NN` would otherwise refuse every commit that never touched
#: it. Applied ONLY to that path; see `message_body`.
COMMENT_LINE_RE = re.compile(r"^\s*#")
#: GIT'S OWN scissors line, not a shape that resembles one. Git emits
#: `# ------------------------ >8 ------------------------` and cuts everything
#: below it. The previous pattern allowed leading whitespace and as few as one
#: dash, so a line a person typed in a body truncated the message and took any
#: real trailer below it with it. Under the editor default git removes that line
#: as a comment and KEEPS what follows, so the trailer reached history and closed
#: the issue while this check reported clean. Eight dashes a side makes an
#: accidental match essentially impossible and still matches git's twenty-four.
SCISSORS_RE = re.compile(r"^#\s?-{8,}\s?>8\s?-{8,}\s*$")


def message_body(text: str, *, raw: bool) -> str:
    """The part of a commit message git will keep, comments and diff removed.

    ``raw`` SAYS WHICH SIDE OF GIT'S CLEANUP THIS TEXT IS ON, and getting that
    wrong is not symmetric.

    A message file handed to the commit-msg hook is PRE-cleanup: it carries git's
    instructional comments, and on `commit --verbose` the entire diff below a
    scissors line. Matching over all of it would let a template line refuse a
    commit that closes nothing, so those are removed.

    `git log --format=%B` is POST-cleanup. Those messages are final. They contain
    no git comments and no scissors block, so stripping cannot prevent a single
    false refusal there and can only DELETE A REAL TRAILER: a body line beginning
    with `#`, which git keeps under the `whitespace` cleanup that `-m` and `-F`
    use, was being discarded. That is the CI path, the one this repository calls
    the load-bearing wiring, so the strip was doing its only possible harm in the
    place it mattered most.

    RESIDUAL, stated rather than hidden. On the hook path a commit made with
    `-m` or `-F` also gets `whitespace` cleanup, so a real trailer on a
    `#`-leading line is dropped here too. Detecting the cleanup mode from inside
    the hook is not possible without reading the same config git is about to
    apply, so the hook is best-effort against that one shape and CI is
    authoritative. Recorded in R-18.
    """
    if raw is False:
        return text
    kept = []
    for line in text.splitlines():
        if SCISSORS_RE.match(line):
            break
        if COMMENT_LINE_RE.match(line):
            continue
        kept.append(line)
    return "\n".join(kept)


def closing_references(text: str, *, raw: bool = True) -> list[int]:
    """Every issue number this message would close, by any spelling GitHub reads.

    THE SPELLING IS NOT OURS TO CHOOSE. This repository's contract says to write
    `Closes #n`, and a check that only recognized that was clean on `Fixes #36`,
    `Resolve #36`, `Closes: #36`, `Closes #36.` and `This closes #36.`, each of
    which closes the issue and cascades every unit waiting on it. What matters is
    what GitHub acts on, not what the contract asks for.

    Nine keywords times FOUR reference forms: the bare `#n`, `GH-n`,
    `owner/repo#n`, and the full issue URL. An earlier version widened the
    keywords, left the reference form alone, and claimed to cover "the eleven
    ways somebody actually types it".

    The comma continuation is caught DELIBERATELY OVER-INCLUSIVELY, and confined
    to ONE LINE. Whether GitHub closes the second issue in `Closes #36, #33` has
    moved with its parser, but somebody writing that line means to close both,
    and the costs are not comparable: a false refusal is one reworded line, a
    miss is a close that has already cascaded. Crossing a newline is a different
    thing entirely and was a defect: a trailer, a blank line, then a sentence
    beginning "and #33 stays open" is not a list.

    A bare `#36` with no keyword is left alone. Refusing a reference would make
    it impossible to explain in a commit body why a unit is still open, which is
    exactly the sentence this check is asking people to write.

    WHAT STAYS REFUSED ON PURPOSE, because in each case GitHub really would close
    the issue and this check has no way to be righter than GitHub:

    * A REVERT. `Revert "feat: converge (closes #36)"` closes 36, and the refusal
      is not merely correct, it is the point: a revert un-lands the module, so
      the register genuinely re-owes that unit at the moment it fires.
    * PROSE QUOTING A REAL TRAILER, and a fixture or diff inside a fenced block
      in a body. Both close the issue when pushed. Nothing distinguishes quoting
      from asserting, to this check or to GitHub. The remedy is a non-numeric
      placeholder, which is what this branch's own history rewrite used after
      this check refused it.
    """
    found: list[int] = []
    body = message_body(text, raw=raw)
    for match in CLOSES_RE.finditer(body):
        found.append(_referenced(match))
        position = match.end()
        while (carried := CONTINUED_RE.match(body, position)) is not None:
            found.append(_referenced(carried))
            position = carried.end()
    return found


def _referenced(match: re.Match) -> int:
    """The issue number out of whichever reference form matched.

    One capturing group per form and exactly one of them is ever set, so the
    first non-empty group is the answer. Reading `group(1)` would silently be
    wrong for every form but the last.
    """
    return int(next(value for value in match.groups() if value is not None))


def unresolved_closes(
    text: str, owed: dict[int, list[str]] | None = None, *, raw: bool = True
) -> list[str]:
    """Every issue this message closes whose unit a register still owes a module.

    PURE, and network-free, which is what lets this run where it is useful. The
    rest of the audit needs `gh`, so it cannot bite on a machine with no token
    and cannot be tested without one. This reads two files in the repository and
    one block of text.

    This is `contradictions()` moved to the other side of the event. That function
    compares the registers against issues that are ALREADY CLOSED, so it can only
    report a contradiction after the close has cascaded and moved dependent units
    to ready. By then `sync` deliberately will not repair it, so the repository is
    stuck with it. The trailer is the moment the close is decided, and it is the
    last moment refusing is cheap.
    """
    owed = owed_by_unit() if owed is None else owed
    found = []
    for uid in dict.fromkeys(closing_references(text, raw=raw)):
        modules = owed.get(uid)
        if modules:
            found.append(
                f"this message closes #{uid}, but U{uid} is still owed "
                f"{', '.join(modules)}. Either land them, or re-point them at "
                f"the unit that will."
            )
    return found


def cmd_closing(args) -> int:
    """Refuse a closing trailer while a register still owes that unit a module."""
    if args.message_file:
        path = Path(args.message_file)
        if not path.is_file():
            # A refusal a person can act on, not a traceback. This runs inside a
            # git hook, where an unhandled exception surfaces as a stack trace in
            # place of the commit message editor and reads as the tool being
            # broken rather than the invocation being wrong.
            print(f"board: no commit message at {args.message_file!r}", file=sys.stderr)
            return 1
        text = path.read_text()
    else:
        result = subprocess.run(
            ["git", "log", "--format=%B", f"{args.since}..HEAD"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            # No such ref, a shallow clone, or no repository. Nothing to judge
            # rather than a refusal, because a check that fails on a machine it
            # cannot read is a check somebody removes from the hook.
            print("board: no commit range to read; nothing checked")
            return 0
        text = result.stdout
        # POST-cleanup messages. Nothing to strip, and stripping could only lose
        # a real trailer.
        return _report(unresolved_closes(text, raw=False))
    return _report(unresolved_closes(text, raw=True))


def _report(problems: list[str]) -> int:
    if not problems:
        return 0
    print("CONTRADICTION: a unit cannot close while a register still owes it work.")
    for line in problems:
        print(f"  {line}")
    print()
    print("This is the same comparison `audit` makes, run BEFORE the close rather")
    print("than after it. Afterwards the close has already cascaded and `sync`")
    print("will not repair it.")
    return 2


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


def contradictions(graph: dict) -> list[str]:
    """What the repository and the board disagree about, that a sync cannot fix.

    Every value the board derives comes from issue closure state, so closure
    state is the one INPUT and nothing checks it. TWO registers assert, each in a
    file the suite enforces, that a named unit has not finished: `tests/_pending.py`
    for guards awaiting their module, and `planned_in` on a verb registry entry
    for a verb awaiting its own. A closed issue for such a unit is the board
    claiming work landed that the repository says did not, and it cascades: one
    wrong close moved four units to Ready.

    Reading only the first register is how three closed units kept live markers
    for seven verbs between them with nothing ever saying so.

    This is kept apart from drift on purpose. Drift is a derived value that fell
    out of date and `sync` repairs it. A contradiction is two sources of truth
    disagreeing, and repairing it automatically would mean picking one to
    overwrite, which is how the wrong one wins silently.
    """
    found = []
    for uid, modules in sorted(owed_by_unit().items()):
        node = graph.get(uid)
        if node and node["unit"] and node["closed"]:
            found.append(
                f"#{uid} {node['title'][:44]}\n"
                f"      closed, but a register still owes it {', '.join(modules)}"
            )
    return found


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
    closing = sub.add_parser(
        "closing", help="refuse a Closes trailer while a register still owes that unit"
    )
    closing.add_argument(
        "--message-file",
        help="a single commit message to judge; this is what the commit-msg hook passes",
    )
    closing.add_argument(
        "--since",
        default="main",
        help="judge every commit after this ref instead of one message file",
    )
    closing.set_defaults(func=cmd_closing)
    args = parser.parse_args()
    try:
        return args.func(args)
    except Fail as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
