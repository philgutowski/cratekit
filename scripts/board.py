#!/usr/bin/env python3
"""The build board, as a tool.

The board at https://github.com/users/<owner>/projects/2 is this repository's
work queue; `--help` lists the commands. The dependency graph is parsed out of
each issue body's `**Depends on:** #18 (U18)` line, never stored, and `audit`
fails on a unit issue that does not parse. Readiness is derived from closure
state and the graph, so `sync` is safe at any time. A cloud session's proxy
refuses GraphQL: reads fall back to REST, and `cloud` is its command.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

PROJECT_NUMBER = "2"
ROOT = Path(__file__).resolve().parent.parent

# Status option ids are looked up, never pinned: a recreated option's new id.
STATUS_ORDER = ["Ready", "In Progress", "In review", "Blocked", "Attended", "Done"]

# Somebody holds the card: `start` and a lane's builder set In Progress, the
# relay runner sets In review. No graph derives either, so a sync keeps them.
UNDERWAY = ("In Progress", "In review")

DEPENDS_RE = re.compile(r"^\*\*Depends on:\*\*\s*(.+)$", re.MULTILINE)
CLOSES_WITH_RE = re.compile(r"^\*\*Closes with:\*\*\s*(.+)$", re.MULTILINE)
ISSUE_REF_RE = re.compile(r"#(\d+)")
UNIT_TITLE_RE = re.compile(r"^U(\d+):")


class Fail(Exception):
    pass


class Truncated(Fail):
    """A board read came back cut short, so it cannot be taken as the whole board."""


# The most rows one read asks `gh` for (U148); a read this long is refused as
# truncated, and each read is also checked against GitHub's own count.
READ_LIMIT = 5000

# Every issue, any state, no pull requests; `gh api` fills the placeholders.
ISSUE_COUNT_QUERY = (
    "query($owner: String!, $name: String!) "
    "{ repository(owner: $owner, name: $name) { issues { totalCount } } }"
)
RAISE_LIMIT = "Raise READ_LIMIT in scripts/board.py."


def whole(rows: list, what: str) -> list:
    """The rows of one read, refused if they fill the limit."""
    if len(rows) >= READ_LIMIT:
        raise Truncated(
            f"the {what} read returned {len(rows)} rows, the whole limit of "
            f"{READ_LIMIT}, so it is truncated and the board cannot be read from it. "
            f"{RAISE_LIMIT}"
        )
    return rows


def gh(*args: str, parse: bool = False):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise Fail(f"gh {' '.join(args)}\n{result.stderr.strip()}")
    out = result.stdout.strip()
    return json.loads(out) if parse and out else out


def git(*args: str, cwd=None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd)


def repo_slug() -> tuple[str, str]:
    """Owner and name from the git remote, never hardcoded."""
    try:
        data = gh("repo", "view", "--json", "owner,name", parse=True)
    except Fail:
        # A cloud session's proxy refuses GraphQL; the checkout names the remote.
        return remote_slug()
    return data["owner"]["login"], data["name"]


REMOTE_RE = re.compile(r"github\.com[:/]([^/\s]+)/([^/\s]+?)(?:\.git)?/?$")


def remote_slug() -> tuple[str, str]:
    """Owner and name parsed from the origin remote, for a session with no GraphQL."""
    url = git("remote", "get-url", "origin").stdout.strip()
    match = REMOTE_RE.search(url)
    if not match:
        raise Fail(f"the origin remote {url!r} does not name a GitHub repository")
    return match.group(1), match.group(2)


def rest_pages(path: str, what: str) -> list:
    """Every row of a REST listing, a hundred a page, ending on a short page.

    Not `gh api --paginate`: the cloud proxy rejects its numeric `Link` paths.
    """
    joiner = "&" if "?" in path else "?"
    rows: list = []
    for page in range(1, READ_LIMIT // 100 + 2):
        batch = gh("api", f"{path}{joiner}per_page=100&page={page}", parse=True) or []
        rows.extend(batch)
        if len(batch) < 100:
            return rows
    raise Truncated(f"the {what} read ran past {READ_LIMIT} rows, so it is truncated. "
                    f"{RAISE_LIMIT}")


def short_of_count(rows: list, total, what: str) -> None:
    """Refuse a read with fewer rows than GitHub says exist, or with no count."""
    if not isinstance(total, int):
        # No count means no check, and a read nobody could check is not whole.
        raise Truncated(
            f"the {what} read came with no count to check it against ({total!r}), "
            f"so it cannot be shown to be whole."
        )
    if len(rows) < total:
        raise Truncated(
            f"the {what} read returned {len(rows)} of the {total} GitHub holds, "
            f"so it is truncated and the board cannot be read from it."
        )


def load_issues() -> list[dict]:
    # Counted BEFORE the read, so an issue filed between the two is never refused.
    try:
        total = gh(
            "api", "graphql", "-F", "owner={owner}", "-F", "name={repo}",
            "-f", f"query={ISSUE_COUNT_QUERY}",
            "--jq", ".data.repository.issues.totalCount",
        )
    except Fail:
        # No GraphQL at all is a cloud session's proxy, not a short read.
        return load_issues_rest()
    issues = gh(
        "issue", "list", "--state",
        "all",
        "--limit",
        str(READ_LIMIT),
        "--json", "number,title,state,body,labels", parse=True,
    )
    whole(issues, "issue")
    short_of_count(issues, int(total) if total.isdigit() else total, "issue")
    return issues


def load_issues_rest() -> list[dict]:
    """Every issue over REST in `gh issue list --json`'s shape, pull requests dropped."""
    owner, name = repo_slug()
    rows = rest_pages(f"repos/{owner}/{name}/issues?state=all", "issue")
    issues = [
        {
            "number": row["number"],
            "title": row["title"],
            "state": str(row.get("state", "")).upper(),
            "body": row.get("body") or "",
            "labels": [{"name": label["name"]} for label in row.get("labels") or []],
        }
        for row in rows
        if "pull_request" not in row
    ]
    return whole(issues, "issue")


def parse_deps(body: str) -> list[int] | None:
    """Issue numbers this one depends on, [] for none, None for a body with no line."""
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

    for node in by_number.values():
        node["unblocks"] = []
    for node in by_number.values():
        for dep in node["deps"] or []:
            if dep in by_number:
                by_number[dep]["unblocks"].append(node["number"])

    # Transitive reach over what is still open, so a gateway unit ranks by its phase.
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
    """What the board should say: closure wins, then a hold, then the graph."""
    if node["closed"]:
        return "Done"
    if current in UNDERWAY:
        # Any held card stays held, so a sync never pulls it from its builder.
        return current
    if node["attended"]:
        return "Attended"
    return "Blocked" if node["open_deps"] else "Ready"


def pending_units() -> dict[int, list[str]]:
    """Units `tests/_pending.py` still says owe a module, read by ast, never imported."""
    source = ROOT / "tests" / "_pending.py"
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
    """Units the verb registry's `planned_in` markers still say owe a module, by ast."""
    source = ROOT / "src" / "cratekit" / "cli" / "registry.py"
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
        """The string this argument evaluates to, through one named constant."""
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
    """Every module either register still owes, per unit, merged."""
    merged: dict[int, set[str]] = {}
    for source in (pending_units(), planned_units()):
        for uid, modules in source.items():
            merged.setdefault(uid, set()).update(modules)
    return {uid: sorted(modules) for uid, modules in merged.items()}


# The closing check: a trailer is refused BEFORE it closes anything.

#: Every keyword GitHub closes an issue on, not only the one the contract uses.
CLOSING_KEYWORDS = ("close", "closes", "closed", "fix", "fixes", "fixed",
                    "resolve", "resolves", "resolved")

#: The reference forms that close an issue IN THIS REPOSITORY, longest first.
#: `owner/repo#n` and an issue URL close one elsewhere, so they are left out.
REFERENCE_FORMS = (r"GH-(\d+)", r"#(\d+)")

#: Keyword, optional colon, then a reference. The lookbehind rejects a keyword
#: that is a URL path segment, `https://example.com/notes/fixes#36`.
CLOSES_RE = re.compile(
    r"(?<![/\w])\b(?:" + "|".join(CLOSING_KEYWORDS) + r")\b\s*:?\s*"
    r"(?:" + "|".join(REFERENCE_FORMS) + r")",
    re.IGNORECASE,
)

#: A comma list continuing from a keyword-anchored issue: `Closes #36, #33`.
#: `[^\S\n]` is horizontal whitespace only, so a later line opening "and #33
#: stays open" is never read as part of the list.
CONTINUED_RE = re.compile(
    r"[^\S\n]*(?:,|and)[^\S\n]*(?:" + "|".join(REFERENCE_FORMS) + r")",
    re.IGNORECASE,
)

#: Lines git itself strips from a commit message, applied only to the raw file
#: the commit-msg hook is handed; see `message_body`.
COMMENT_LINE_RE = re.compile(r"^\s*#")
#: Git's own scissors line, eight dashes a side at least, so a line a person
#: typed in a body never truncates the message.
SCISSORS_RE = re.compile(r"^#\s?-{8,}\s?>8\s?-{8,}\s*$")


def message_body(text: str, *, raw: bool) -> str:
    """The part of a commit message git will keep, comments and diff removed.

    ``raw`` is the hook's pre-cleanup file; `git log --format=%B` is already
    clean, where stripping could only delete a real `#` leading trailer (R-320).
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

    A comma list is caught over inclusively on one line; a bare `#36` with no
    keyword is left alone, so a body can say why a unit is still open.
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
    """The issue number out of whichever reference form matched."""
    return int(next(value for value in match.groups() if value is not None))


def unresolved_closes(
    text: str,
    owed: dict[int, list[str]] | None = None,
    *,
    raw: bool = True,
    units: dict[int, int] | None = None,
) -> list[str]:
    """Every issue this message closes whose unit a register still owes a module.

    Network free, so it runs in a hook. ``units`` maps issue to unit number (U38
    is issue #51); without it an issue number is read as a unit, a named guess.
    """
    owed = owed_by_unit() if owed is None else owed
    found = []
    for reference in dict.fromkeys(closing_references(text, raw=raw)):
        uid = reference if units is None else units.get(reference)
        modules = owed.get(uid) if uid is not None else None
        if not modules:
            continue
        lines = [
            f"this message closes #{reference}, but U{uid} is still owed "
            f"{', '.join(modules)}. Either land them, or re-point them at "
            f"the unit that will."
        ]
        if units is None and reference == uid:
            lines.append(
                f"      read #{reference} as U{uid} without consulting the board, "
                f"which is right for most units here and not for all. Run "
                f"`board.py audit` to have the mapping resolved."
            )
        lines += [f"      {note}" for note in _near_misses(modules)]
        found.append("\n".join(lines))
    return found


def _near_misses(modules: list[str]) -> list[str]:
    """For each owed module that is absent, the near names its package does hold."""
    root = ROOT / "src"
    notes: list[str] = []
    for module in modules:
        if module.startswith("path:"):
            continue
        parts = module.split(".")
        package = root.joinpath(*parts[:-1])
        target = package / f"{parts[-1]}.py"
        if not package.is_dir() or target.exists() or (package / parts[-1]).is_dir():
            continue
        siblings = sorted(
            child.stem
            for child in package.glob("*.py")
            if child.stem != "__init__" and parts[-1] in child.stem
        )
        if siblings:
            notes.append(
                f"note: {module} is absent and {package.name} already contains "
                f"{', '.join(siblings)}. If that is the same module under "
                f"another name, the register key is what needs correcting."
            )
    return notes


def cmd_closing(args) -> int:
    """Refuse a closing trailer while a register still owes that unit a module."""
    if args.message_file:
        path = Path(args.message_file)
        if not path.is_file():
            # Inside a git hook a traceback reads as the tool being broken.
            print(f"board: no commit message at {args.message_file!r}", file=sys.stderr)
            return 1
        text = path.read_text()
    else:
        # One message per record, split on NUL: run together, two messages can
        # make a closing reference neither commit contains.
        result = subprocess.run(
            ["git", "log", "--format=%B%x00", f"{args.since}..HEAD"],
            capture_output=True,
            text=True,
        )
        problems: list[str] = []
        card = pull_request_card(getattr(args, "pull_request_head", None))
        if card is not None:
            # The trailer its merge will write is in no commit yet (U158).
            problems += unresolved_closes(f"Closes #{card}", raw=False)
        if result.returncode != 0:
            print("board: no commit range to read; no trailer checked")
            return _report(problems)
        for message in result.stdout.split("\0"):
            if message.strip():
                problems += unresolved_closes(message, raw=False)
        return _report(problems)
    return _report(unresolved_closes(text, raw=True))


#: A cloud worker's branch, the only head a closing merge comes from (U158).
CLOUD_BRANCH_RE = re.compile(r"^cloud/(\d+)-")


def pull_request_card(head_ref: str | None) -> int | None:
    """The card a pull request's head branch will close at its merge, if any."""
    match = CLOUD_BRANCH_RE.match(head_ref or "")
    return int(match.group(1)) if match else None


def _print_all(lines) -> None:
    for line in lines:
        print(f"  {line}")


def _report(problems: list[str]) -> int:
    # This runs before a landing, so a residual file it cannot read is refused.
    malformed = residual_file_problems()
    if not problems and not malformed:
        return 0
    if problems:
        print("CONTRADICTION: a unit cannot close while a register still owes it work.")
        _print_all(problems)
        print("\nThis is the same comparison `audit` makes, run BEFORE the close rather")
        print("than after it. Afterwards the close has already cascaded and `sync`")
        print("will not repair it.")
    if malformed:
        if problems:
            print()
        print("A RESIDUAL FILE CANNOT LAND as it stands:")
        _print_all(malformed)
        print("\ndocs/residuals/README.md is the form: a title and a Found line in the")
        print("frontmatter, then the body.")
    return 2


# Writing the board.

# The project and its fields in one query (U151), asked of a user, then an org.
CONTEXT_QUERY = (
    "query($login: String!, $number: Int!) { %s(login: $login) { "
    "projectV2(number: $number) { id url fields(first: 100) { totalCount nodes { "
    "... on ProjectV2SingleSelectField { id name options { id name } } "
    "... on ProjectV2Field { id name } } } } } }"
)

# Each issue's own cards, a hundred issues at one point a page; archived left out.
MEMBERSHIP_QUERY = (
    "query($owner: String!, $name: String!, $after: String) { "
    "repository(owner: $owner, name: $name) { "
    "issues(first: 100, after: $after) { totalCount pageInfo { hasNextPage endCursor } "
    "nodes { number projectItems(first: 20, includeArchived: false) { totalCount nodes { "
    "id project { number owner { ... on User { login } ... on Organization { login } } } "
    'status: fieldValueByName(name: "Status") { '
    "... on ProjectV2ItemFieldSingleSelectValue { name } } "
    'unblocks: fieldValueByName(name: "Unblocks") { '
    "... on ProjectV2ItemFieldNumberValue { number } } } } } } } }"
)


def project_context(owner: str) -> dict:
    project = None
    refusals = []
    for kind in ("user", "organization"):
        try:
            data = gh(
                "api", "graphql", "-F", f"login={owner}", "-F", f"number={PROJECT_NUMBER}",
                "-f", f"query={CONTEXT_QUERY % kind}", parse=True,
            )
        except Fail as refused:
            refusals.append(str(refused))
            continue
        project = ((data.get("data") or {}).get(kind) or {}).get("projectV2")
        if project:
            break
    if not project:
        raise Fail(
            f"project {PROJECT_NUMBER} of {owner} cannot be read with this token\n"
            + "\n".join(refusals)
        )
    fields = project["fields"]
    whole_fields = [f for f in fields["nodes"] if f]
    short_of_count(fields["nodes"], fields.get("totalCount"), "project field")
    status = next((f for f in whole_fields if f.get("name") == "Status"), None)
    if not status or "options" not in status:
        raise Fail(f"project {PROJECT_NUMBER} of {owner} has no single select Status field")
    unblocks = next((f for f in whole_fields if f.get("name") == "Unblocks"), None)
    return {
        "id": project["id"],
        "url": project["url"],
        "status_field": status["id"],
        "options": {o["name"]: o["id"] for o in status["options"]},
        "unblocks_field": unblocks["id"] if unblocks else None,
    }


def project_items(owner: str) -> dict:
    """Every issue's card on project `PROJECT_NUMBER` of `owner`, read from the issues."""
    items: dict = {}
    seen: list[int] = []
    total = None
    after = None
    for _ in range(READ_LIMIT // 100 + 1):
        args = [
            "api", "graphql", "-F", "owner={owner}", "-F", "name={repo}",
            "-f", f"query={MEMBERSHIP_QUERY}",
        ]
        if after:
            # `-f`, never `-F`: a cursor is text and `-F` would type it.
            args += ["-f", f"after={after}"]
        page = gh(*args, parse=True)["data"]["repository"]["issues"]
        if total is None:
            total = page.get("totalCount")
        for issue in page["nodes"]:
            seen.append(issue["number"])
            memberships = issue["projectItems"]
            short_of_count(
                memberships["nodes"], memberships.get("totalCount"),
                f"#{issue['number']} project membership",
            )
            for item in memberships["nodes"]:
                project = item.get("project") or {}
                login = (project.get("owner") or {}).get("login") or ""
                if str(project.get("number")) != PROJECT_NUMBER:
                    continue
                if login.lower() != owner.lower():
                    continue
                items[issue["number"]] = {
                    "id": item["id"],
                    "status": (item.get("status") or {}).get("name"),
                    "unblocks": (item.get("unblocks") or {}).get("number"),
                }
        info = page["pageInfo"]
        if not info["hasNextPage"]:
            break
        after = info.get("endCursor")
        if not after:
            raise Truncated("the project membership read said there was more and gave no cursor")
    else:
        raise Truncated(
            f"the project membership read ran past {READ_LIMIT} issues, so it is "
            f"truncated. {RAISE_LIMIT}"
        )
    short_of_count(seen, total, "project membership")
    return items


# Commands.


def cmd_next(args) -> int:
    owner, _ = repo_slug()
    graph = build_graph(load_issues())
    try:
        # The context first: a token blind to the project reads no memberships.
        project_context(owner)
        items = project_items(owner)
    except Truncated:
        # A cut short read is not a token that cannot see the board, and the
        # queue below would offer a held card the read missed.
        raise
    except Fail:
        # A repository scoped token cannot read a user owned project.
        items = {}
        print("(cannot read the project board with this token, so work already")
        print(" in progress is not shown below)")
        print()

    ready = [n for n in graph.values() if n["unit"] and not n["closed"] and not n["open_deps"]]
    in_progress = [
        n for n in graph.values() if items.get(n["number"], {}).get("status") in UNDERWAY
    ]
    busy = {n["number"] for n in in_progress}
    ready = [n for n in ready if n["number"] not in busy]
    ready.sort(key=lambda n: (-n["reach"], -len(n["unblocks"]), n["number"]))

    if in_progress:
        print("Already underway, never start one of these again:")
        for node in in_progress:
            status = items[node["number"]]["status"]
            print(f"  #{node['number']:<3} {status:<11} {node['title']}")
        print()

    if not ready:
        print("Nothing is ready. Every open unit is waiting on another one.")
        return 0

    print(f"Ready now, ranked by how much of the build each one releases ({len(ready)} units):\n")
    for rank, node in enumerate(ready, 1):
        marker = "->" if rank == 1 else "  "
        print(f"{marker} #{node['number']:<3} {node['title']}")
        directly = len(node["unblocks"])
        print(f"      releases {node['reach']} open unit(s), {directly} of them directly")
    top = ready[0]
    print(f"\nTake #{top['number']}. Start it with:")
    print(f"    .venv/bin/python scripts/board.py start {top['number']}")
    return 0


def _issue(graph: dict, number: int) -> dict:
    node = graph.get(number)
    if not node:
        raise Fail(f"no issue #{number}")
    return node


def cmd_show(args) -> int:
    node = _issue(build_graph(load_issues()), args.number)
    print(f"#{node['number']} {node['title']}")
    print(f"state: {'closed' if node['closed'] else 'open'}")
    if node["open_deps"]:
        print(f"blocked by: {', '.join('#' + str(d) for d in node['open_deps'])}")
    print(f"\n{node['body']}")
    return 0


def slugify(title: str) -> str:
    body = title.split(":", 1)[-1].strip().lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", body)).strip("-")[:40]


def _set_field(item: dict, ctx: dict, field: str, *value: str) -> None:
    gh(
        "project", "item-edit", "--id", item["id"],
        "--project-id", ctx["id"], "--field-id", field, *value,
    )


def cmd_start(args) -> int:
    owner, _ = repo_slug()
    graph = build_graph(load_issues())
    node = _issue(graph, args.number)
    if node["closed"]:
        raise Fail(f"#{args.number} is already closed")
    if node["open_deps"]:
        blockers = ", ".join(f"#{d} ({graph[d]['title'].split(':')[0]})" for d in node["open_deps"])
        raise Fail(f"#{args.number} is blocked by {blockers}. Pick something ready.")

    match = UNIT_TITLE_RE.match(node["title"])
    prefix = f"u{match.group(1)}" if match else f"issue{node['number']}"
    branch = f"unit/{prefix}-{slugify(node['title'])}"

    current = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if current != "main":
        raise Fail(f"on branch {current}, not main. Land or park that work first.")
    if git("status", "--porcelain").stdout.strip():
        raise Fail("the working tree is dirty. Commit or stash before starting a unit.")

    # Read BEFORE the branch exists, so a refused read leaves main.
    ctx = project_context(owner)
    items = project_items(owner)
    item = items.get(node["number"])

    subprocess.run(["git", "checkout", "-b", branch], check=True)

    if item:
        opt = ctx["options"]["In Progress"]
        _set_field(item, ctx, ctx["status_field"], "--single-select-option-id", opt)
        print()
        print(f"Branch {branch} is checked out and #{node['number']} is In Progress.")
    else:
        print()
        print(f"Branch {branch} is checked out, but #{node['number']} is NOT on the")
        print("project board, so nothing there shows it is taken and `next` will")
        print("still offer it. Run `board.py sync` to add it, then set it In Progress.")
    print("\nRead the brief:")
    print(f"    .venv/bin/python scripts/board.py show {node['number']}")
    print("\nThe battery, before you merge anything:")
    print("    .venv/bin/ruff check src tests scripts")
    print("    .venv/bin/python -m pytest")
    print("    .venv/bin/python scripts/scan_repo.py")
    print("\nEnd the merge commit message with this line and nothing will need doing by hand:\n")
    print(f"    Closes #{node['number']}\n")
    print("Pushing main then closes the issue, and the board cascade flips every unit")
    print("this one unblocks from Blocked to Ready on its own.")
    return 0


#: The ledger, append only, its older entries archived by number range in the
#: sibling `ledger/` folder with no file over the limit (U314), and the folder a
#: residual waits in for its number.
LEDGER = ROOT / "docs" / "residual-findings.md"
RESIDUALS_DIR = ROOT / "docs" / "residuals"
LEDGER_LIMIT = 5000
_HEADING = re.compile(r"^## R-(\d+)\.\s*(.+?)\s*$")
ARCHIVE_NOTE = [
    "The older findings are archived by number range in `docs/ledger/`, every entry",
    "byte for byte as filed, and `board.py residuals --search WORDS` searches them",
    "all. An amendment to an archived entry is made in its archive file.",
]

#: A residual file's frontmatter; ``issue`` says it meets METHOD's board bar.
RESIDUAL_REQUIRED = ("title", "found")
RESIDUAL_OPTIONAL = {"issue": ("yes", "no")}


def _archive_name(first: int, last: int) -> str:
    return f"R-{first:04d}-R-{last:04d}.md"


def ledger_files(ledger: Path | None = None) -> list[Path]:
    """The ledger's archives in number order, then its working file."""
    ledger = LEDGER if ledger is None else ledger

    def first(path: Path) -> tuple[int, str]:
        match = re.fullmatch(r"R-(\d+)-R-\d+\.md", path.name)
        return (int(match[1]) if match else -1, path.name)

    return sorted((ledger.parent / "ledger").glob("*.md"), key=first) + [ledger]


def _headings(ledger: Path | None = None) -> list[tuple[int, str, Path]]:
    return [
        (int(match[1]), match[2], path)
        for path in ledger_files(ledger)
        if path.exists()
        for match in map(_HEADING.match, path.read_text().splitlines())
        if match
    ]


def residual_titles(ledger: Path | None = None) -> dict[int, str]:
    """Every ``## R-N.`` heading in every ledger file, by number, read as text."""
    return {number: title for number, title, _ in _headings(ledger)}


def _entries(lines: list[str]) -> list[tuple[int, int, int]]:
    """(number, where its separator starts, its heading line) per entry."""
    found = []
    for head, line in enumerate(lines):
        match = _HEADING.match(line)
        if match:
            start = head
            while start and lines[start - 1] in ("", "---"):
                start -= 1
            found.append((int(match[1]), start, head))
    return found


def ledger_entries(text: str) -> list[tuple[int, str]]:
    """Each entry's text, its heading to the next entry's separator."""
    lines = text.split("\n")
    found = _entries(lines)
    ends = [start for _, start, _ in found[1:]] + [len(lines)]
    return [
        (number, "\n".join(lines[head:end]).rstrip("\n"))
        for (number, _, head), end in zip(found, ends)
    ]


#: How many headings a ledger search prints before it counts the rest.
SEARCH_CAP = 25


def search_residuals(
    words: list[str], ledger: Path | None = None, cap: int = SEARCH_CAP
) -> tuple[list[tuple[int, str, Path]], int]:
    """The headings in every ledger file carrying every word, newest first (U196)."""
    source = LEDGER if ledger is None else ledger
    if not source.is_file():
        # A missing ledger is not an empty one: "nothing matches" over a file
        # never read is how a duplicate card gets filed.
        raise FileNotFoundError(f"no residual ledger at {source}")
    wanted = [word.casefold() for word in words]
    hits = [hit for hit in _headings(source) if all(w in hit[1].casefold() for w in wanted)]
    hits.sort(key=lambda hit: hit[0], reverse=True)
    return hits[:cap], max(0, len(hits) - cap)


def residual_files(folder: Path | None = None) -> list[Path]:
    """The residuals waiting for a number, in name order, the order they take one."""
    folder = RESIDUALS_DIR if folder is None else folder
    if not folder.is_dir():
        return []
    paths = sorted(p for p in folder.glob("*.md") if p.name != "README.md")
    # Only what git knows: an untracked draft is not filed yet. A folder outside
    # any repository is taken whole.
    listed = git("ls-files", "-z", "--", ".", cwd=folder)
    if listed.returncode != 0:
        return paths
    known = {name for name in listed.stdout.split("\0") if name}
    return [p for p in paths if p.name in known]


def read_residual_file(path: Path) -> tuple[dict[str, str], str]:
    """The frontmatter and the body of one residual file, or ValueError saying why."""
    text = path.read_text()
    lines = text.split("\n")
    if not lines or lines[0] != "---":
        raise ValueError("does not open with a frontmatter fence")
    try:
        close = lines.index("---", 1)
    except ValueError:
        raise ValueError("its frontmatter fence is never closed") from None
    meta: dict[str, str] = {}
    for line in lines[1:close]:
        key, sep, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if not sep or not key:
            raise ValueError(f"frontmatter line {line!r} is not key: value")
        if key in meta:
            raise ValueError(f"frontmatter names {key} twice")
        if key not in RESIDUAL_REQUIRED and key not in RESIDUAL_OPTIONAL:
            raise ValueError(f"frontmatter key {key} is not one a ledger entry carries")
        meta[key] = value
    for key in RESIDUAL_REQUIRED:
        if not meta.get(key):
            raise ValueError(f"frontmatter has no {key}")
    for key, allowed in RESIDUAL_OPTIONAL.items():
        if key in meta and meta[key] not in allowed:
            raise ValueError(f"frontmatter {key} is {meta[key]!r}, not one of {allowed}")
    # Only the heading's own shape is refused: "R-204 is discharged" cites another.
    if re.match(r"R-\d+\.", meta["title"]):
        raise ValueError("its title carries a number; the number is given at landing")
    body = "\n".join(lines[close + 1 :]).strip("\n")
    if not body.strip():
        raise ValueError("has frontmatter and no body")
    return meta, body


def residual_file_problems(folder: Path | None = None) -> list[str]:
    """One line per residual file that could not be landed as it stands."""
    problems = []
    for path in residual_files(folder):
        try:
            read_residual_file(path)
        except ValueError as exc:
            problems.append(f"docs/residuals/{path.name} {exc}")
    return problems


def land_residuals(
    ledger: Path | None = None, folder: Path | None = None
) -> list[tuple[int, str, bool]]:
    """Number every waiting residual, append it to the ledger, delete its file.

    Whoever lands first takes the next number past the highest in any ledger
    file; every file is validated first, and the working file is archived if the
    landing put it over the limit. Returns ``(number, title, meets the board bar)``.
    """
    ledger = LEDGER if ledger is None else ledger
    paths = residual_files(folder)
    parsed = []
    problems = []
    for path in paths:
        try:
            parsed.append((path, *read_residual_file(path)))
        except ValueError as exc:
            problems.append(f"{path.name} {exc}")
    if problems:
        raise ValueError("; ".join(problems))
    if not parsed:
        return []
    text = ledger.read_text()
    titles = residual_titles(ledger)
    # A landed file can come back through a conflict; never number it twice.
    held = {title: number for number, title in titles.items()}
    again = [
        f"{path.name} is R-{held[meta['title']]} already"
        for path, meta, _ in parsed
        if meta["title"] in held
    ]
    if again:
        raise ValueError("; ".join(again))
    number = max(titles, default=0)
    landed = []
    for path, meta, body in parsed:
        number += 1
        text = text.rstrip("\n") + "\n\n---\n\n"
        text += f"## R-{number}. {meta['title']}\n\n**Found:** {meta['found']}\n\n{body}\n"
        landed.append((number, meta["title"], meta.get("issue") == "yes"))
    ledger.write_text(text)
    archive_ledger(ledger)
    for path, _, _ in parsed:
        path.unlink()
    return landed


def archive_ledger(ledger: Path | None = None) -> list[Path]:
    """While the working file is over the limit, move its oldest entries to new archives."""
    ledger = LEDGER if ledger is None else ledger
    lines = ledger.read_text().rstrip("\n").split("\n")
    entries = _entries(lines)
    if not entries:
        return []
    head = lines[: entries[0][1]]
    if ARCHIVE_NOTE[0] not in head:
        head += ["", *ARCHIVE_NOTE]
    starts = [start for _, start, _ in entries] + [len(lines)]

    def body(first: int, last: int) -> list[str]:
        part = lines[starts[first] : starts[last]]
        while part and not part[0]:
            part = part[1:]
        return part

    written, first, count = [], 0, len(entries)
    while first < count - 1 and len(head) + 1 + len(body(first, count)) > LEDGER_LIMIT:
        last = first + 1
        while last < count - 1 and 4 + len(body(first, last + 1)) <= LEDGER_LIMIT:
            last += 1
        low, high = entries[first][0], entries[last - 1][0]
        path = ledger.parent / "ledger" / _archive_name(low, high)
        path.parent.mkdir(exist_ok=True)
        path.write_text("\n".join([
            f"# Residual findings, R-{low} to R-{high}", "",
            "Archived from `docs/residual-findings.md` by `board.py residuals --archive` "
            "(U314), every entry byte for byte as filed.", "",
            *body(first, last),
        ]) + "\n")
        written.append(path)
        first = last
    if written:
        ledger.write_text("\n".join([*head, "", *body(first, count)]) + "\n")
    return written


def _ledger_at(rev: str, ledger: Path) -> list[str] | None:
    """Every ledger file's text at a revision, the single file layout included."""
    listed = git("ls-tree", "--name-only", rev, "--", "ledger/", cwd=ledger.parent)
    if listed.returncode != 0:
        return None
    texts = []
    for name in [*(n for n in listed.stdout.split() if n.endswith(".md")), ledger.name]:
        shown = git("show", f"{rev}:./{name}", cwd=ledger.parent)
        if shown.returncode != 0:
            return None
        texts.append(shown.stdout)
    return texts


def ledger_problems(
    ledger: Path | None = None, against: str | None = None, unchanged: bool = False
) -> list[str]:
    """METHOD's merge checks over the archived ledger, and the move's byte comparison."""
    ledger = LEDGER if ledger is None else ledger
    problems: list[str] = []
    now: dict[int, str] = {}
    where: dict[int, Path] = {}
    last = 0
    for path in ledger_files(ledger):
        name = path.relative_to(ledger.parent.parent)
        text = path.read_text() if path.exists() else ""
        if text.count("\n") > LEDGER_LIMIT:
            problems.append(f"{name} is {text.count(chr(10))} lines, over {LEDGER_LIMIT}")
        entries = ledger_entries(text)
        numbers = [number for number, _ in entries]
        for number, entry in entries:
            if number in where:
                problems.append(f"R-{number} is a heading in {where[number]} and in {name}")
            where.setdefault(number, name)
            now.setdefault(number, entry)
        if path != ledger and (not numbers or path.name != _archive_name(numbers[0], numbers[-1])):
            held = f"R-{numbers[0]} to R-{numbers[-1]}" if numbers else "no heading"
            problems.append(f"{name} is not named by what it holds, {held}")
        if numbers and (numbers != sorted(numbers) or numbers[0] <= last):
            problems.append(f"{name} is out of number order or overlaps the file before it")
        last = max([last, *numbers])
    if against is None:
        return problems
    texts = _ledger_at(against, ledger)
    if texts is None:
        return [*problems, f"cannot read the ledger at {against}"]
    before: dict[int, str] = {}
    for text in texts:
        for number, entry in ledger_entries(text):
            before.setdefault(number, entry)
    missing = [f"R-{n}" for n in sorted(set(before) - set(now))]
    if missing:
        problems.append(f"headings at {against} are gone now: {', '.join(missing)}")
    retitled = [f"R-{n}" for n in sorted(before) if n in now
                and now[n].split("\n", 1)[0] != before[n].split("\n", 1)[0]]
    if retitled:
        problems.append(f"headings at {against} are retitled now: {', '.join(retitled)}")
    changed = [f"R-{n}" for n in sorted(before) if n in now and now[n] != before[n]]
    if unchanged and changed:
        problems.append(f"entries that differ from {against}: {', '.join(changed)}")
    return problems


def repointed_residuals(graph: dict) -> list[str]:
    """Residual issues whose title no longer matches the finding they number."""
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
                f"      the issue names it, the residual ledger has no such finding"
            )
        elif file_titles[number] != issue_title:
            found.append(
                f"#{node['number']} R-{number} names a different finding than the ledger does\n"
                f"      issue: {issue_title[:72]}\n"
                f"      file : {file_titles[number][:72]}"
            )
    return found


def units_by_issue_number(graph: dict) -> dict[int, int]:
    """Unit number to issue number, off the titles; a unit two issues claim is dropped."""
    seen: dict[int, int] = {}
    duplicated: set[int] = set()
    for number, node in graph.items():
        if not node["unit"]:
            continue
        match = re.match(r"U(\d+)\b", node["title"])
        if not match:
            continue
        unit = int(match.group(1))
        if unit in seen and seen[unit] != number:
            duplicated.add(unit)
        seen[unit] = number
    return {unit: number for unit, number in seen.items() if unit not in duplicated}


def contradictions(graph: dict, owed: dict[int, list[str]] | None = None) -> list[str]:
    """Closed unit issues a register still owes a module, and repointed residuals.

    Not drift: a sync would have to pick a source to overwrite. ``owed`` defaults
    to the live registers (R-322).
    """
    found = []
    owed = owed_by_unit() if owed is None else owed
    issues_by_unit = units_by_issue_number(graph)
    for uid, modules in sorted(owed.items()):
        number = issues_by_unit.get(uid)
        node = graph.get(number) if number is not None else None
        if node and node["unit"] and node["closed"]:
            found.append(
                f"#{node['number']} {node['title'][:44]}\n"
                f"      closed, but a register still owes it {', '.join(modules)}"
            )
    return found + repointed_residuals(graph)


def reconcile(owner: str, apply: bool, labels_only: bool = False) -> list[str]:
    """The drift between board and repository; `labels_only` skips the project."""
    graph = build_graph(load_issues())
    ctx = None if labels_only else project_context(owner)
    items = {} if labels_only else project_items(owner)
    name = repo_slug()[1]
    drift: list[str] = []

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
                items[number] = {"id": added["id"], "status": None, "unblocks": None}
                item = items[number]
            else:
                continue

        want = derive_status(node, item["status"]) if item else None
        if item and item["status"] != want:
            drift.append(f"#{number} status is {item['status']}, should be {want}")
            if apply:
                opt = ctx["options"][want]
                _set_field(item, ctx, ctx["status_field"], "--single-select-option-id", opt)

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

        # Written only when it differs, so a sync with no drift writes nothing.
        unblocks = len(node["unblocks"])
        if item and ctx and ctx["unblocks_field"] and apply and item.get("unblocks") != unblocks:
            _set_field(item, ctx, ctx["unblocks_field"], "--number", str(unblocks))
    return drift


def cmd_sync(args) -> int:
    owner, _ = repo_slug()
    drift = reconcile(owner, apply=True, labels_only=args.labels_only)
    if not drift:
        print("The board already matched the repository. Nothing changed.")
        return 0
    print(f"Corrected {len(drift)} item(s):")
    _print_all(drift)
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
        print(f"\nDRIFT, {len(drift)} item(s). Derived values that fell out of date:")
        _print_all(drift)
        print("\nFix it with: .venv/bin/python scripts/board.py sync")

    if clashes:
        print(f"\nCONTRADICTION, {len(clashes)} item(s). A sync cannot fix these:")
        _print_all(clashes)
        print("\nEach one is a decision, not a repair. Either reopen the issue because")
        print("the unit is not finished, or clear the register entry because it is.")
        print("TWO REGISTERS CAN OWE, so read the module named above to know which")
        print("file to open: a dotted module in tests/_pending.py PENDING, or a")
        print("planned_in marker on a src/cratekit/cli/registry.py entry. Naming")
        print("only the first sent people to a file the entry was never in.")
        print("Overwriting one from the other would let the wrong one win.")

    malformed = residual_file_problems()
    if malformed:
        print(f"\nRESIDUAL FILES THAT CANNOT LAND, {len(malformed)}. A sync cannot fix these:")
        _print_all(malformed)
        clashes = clashes + malformed

    waiting = residual_files()
    if waiting:
        print(f"\n{len(waiting)} residual file(s) in docs/residuals wait for a number.")
        print("On main, after the merge that carried them:")
        print("    .venv/bin/python scripts/board.py residuals --land")

    if not drift and not clashes:
        print("The board matches the repository.")
        return 0
    return 2 if clashes else 1


def _refuse(message: str, code: int) -> int:
    print(f"board: {message}", file=sys.stderr)
    return code


def cmd_residuals(args) -> int:
    """List the residuals waiting for a number, number them on main, or search."""
    if getattr(args, "archive", False):
        written = archive_ledger()
        for path in written:
            print(f"wrote {path.relative_to(LEDGER.parent.parent)}")
        print(f"The working file is within {LEDGER_LIMIT} lines; {len(written)} archive(s) written.")
        return 0
    if getattr(args, "check", False):
        if args.unchanged and not args.against:
            return _refuse("--unchanged compares with a revision, so it needs --against", 2)
        problems = ledger_problems(against=args.against, unchanged=args.unchanged)
        print("The ledger " + ("FAILS its checks:" if problems else "passes its checks."))
        _print_all(problems)
        return 1 if problems else 0
    words = getattr(args, "search", None)
    if words is not None:
        if args.land or not words:
            return _refuse("--search takes one word or more, and not with --land", 2)
        try:
            hits, more = search_residuals(words)
        except FileNotFoundError as exc:
            return _refuse(f"cannot search, {exc}", 2)
        for number, title, path in hits:
            print(f"R-{number}. {title}  ({path.relative_to(LEDGER.parent.parent)})")
        if more:
            print(f"... and {more} more; add a word to narrow it")
        if not hits:
            print(f"No ledger heading carries every one of: {' '.join(words)}")
        return 0
    malformed = residual_file_problems()
    if malformed:
        print("A RESIDUAL FILE CANNOT LAND as it stands:")
        _print_all(malformed)
        return 2
    waiting = residual_files()
    if not args.land:
        highest = max(residual_titles(), default=0)
        print(f"The ledger's highest is R-{highest}. {len(waiting)} file(s) wait:")
        for path in waiting:
            print(f"  docs/residuals/{path.name}")
        return 0
    # On main only: a number given on a branch races every other branch.
    branch = git("rev-parse", "--abbrev-ref", "HEAD", cwd=LEDGER.parent).stdout.strip()
    if branch != "main":
        print(
            f"board: residuals are numbered on main, after the merge that carried "
            f"them, and this checkout is on {branch or 'no branch'}",
            file=sys.stderr,
        )
        return 1
    # Behind the remote as last fetched, a number given here may be taken there.
    behind = git("rev-list", "--count", "main..origin/main", cwd=LEDGER.parent)
    if behind.returncode == 0 and behind.stdout.strip() not in ("", "0"):
        return _refuse(
            f"main is {behind.stdout.strip()} commit(s) behind origin/main as "
            f"last fetched; pull first, or a number given here may be taken there",
            1,
        )
    try:
        landed = land_residuals()
    except ValueError as exc:
        return _refuse(f"nothing numbered, {exc}", 2)
    if not landed:
        print("No residual file waits for a number.")
        return 0
    for number, title, board_bar in landed:
        print(f"R-{number}. {title}")
        if board_bar:
            print(f"    meets the board bar: file the issue titled R-{number}: {title}")
    print("\nCommit the ledger and the deleted files together:")
    print("    git add docs/residual-findings.md docs/ledger docs/residuals")
    print('    git commit -m "docs(residuals): number what landed"')
    return 0


# The cloud lane.

# The label a residual's card carries, held in a constant so the word is never
# followed by a quoted string, which test_reserved_causes reads as a title.
FINDING_LABEL = "residual"

# A cloud session's footer, which tells its comments from the person's.
SESSION_MARK = "Generated by [Claude Code]"

# The headings a cloud session writes; the reader reads headings and nothing else.
HEAD_STARTED = "started"
HEAD_RESUMED = "resumed"
HEAD_PLAN = "plan"
HEAD_PROGRESS = "progress"
HEAD_BRAINSTORM = "brainstorm"
HEAD_QUESTION = "question for phillip"
HEAD_MACHINE = "needs the machine"
HEAD_LANDED = "landed"
HEAD_WITHDRAWN = "withdrawn"
# The relay thread posts Phillip's answer under this heading: a reply, not a hold.
HEAD_ANSWER = "answer from phillip"

# A hold older than this is a session that died, and the card is resumed.
STALE_HOURS = 8

# What the cloud takes, in the order it takes them; the rest is never offered.
CLOUD_TAKE = ("answered", "resume", "ready")
CLOUD_SKIP = ("underway", "waiting-on-phillip", "set-aside", "landed-open", "blocked", "attended")


# An opening emphasised span heads the line, `**Brainstorm.** One question
# waits`; its closer must repeat the opener and be followed by the line's end,
# whitespace or punctuation, so `**Brainstorm**s` is no span.
_OPENING_EMPHASIS = re.compile(r"([*_]+)(.+?)\1(?=$|[\s.,:;?!\u2026])")
# A heading ends at a colon, a comma, or a sentence end followed by whitespace,
# so `**Started: cloud/1-a**` reads `started` and `v0.6.0` is never cut.
_HEADING_END = re.compile(r"[:,]|[.?!;\u2026](?=\s)")
# What may trail a heading, stripped with emphasis until neither is left.
_TRAILING = ".?!;\u2026# \t"


def comment_heading(body: str) -> str:
    """The first line of a comment as a lower case heading, punctuation dropped (U203)."""
    for line in (body or "").splitlines():
        text = line.strip().lstrip("#").strip()
        if not text.strip("*_").strip():
            continue
        span = _OPENING_EMPHASIS.match(text)
        text = span.group(2) if span else text.strip("*_")
        text = _HEADING_END.split(text, maxsplit=1)[0]
        settled = None
        while text != settled:
            settled = text
            text = text.strip().strip("*_").rstrip(_TRAILING)
        return text.lower()
    return ""


def _relayed_answer(comment: dict) -> bool:
    return comment_heading(comment.get("body") or "") == HEAD_ANSWER


def _when(comment: dict) -> str:
    return comment.get("created_at") or ""


def cloud_state(node: dict, comments: list[dict]) -> tuple[str, str]:
    """A card's cloud state and why, from its comments: the session's last heading
    is its hold, and a later comment without the footer is the person's reply."""
    if node["attended"]:
        return "attended", "needs Phillip at the machine"
    if node["open_deps"]:
        return "blocked", "waits on " + ", ".join(f"#{d}" for d in node["open_deps"])

    ordered = sorted(comments, key=_when)
    mine = [c for c in ordered if SESSION_MARK in (c.get("body") or "") and not _relayed_answer(c)]
    if not mine:
        return "ready", "no cloud session has taken it"
    # Progress notes do not set the state, but they do refresh the hold.
    notes = (HEAD_PLAN, HEAD_PROGRESS)
    stated = [c for c in mine if comment_heading(c.get("body") or "") not in notes]
    last = stated[-1] if stated else mine[-1]
    heading, since = comment_heading(last.get("body") or ""), _when(last)
    freshest = _when(mine[-1])

    after = [
        c for c in ordered
        if _when(c) > since and (SESSION_MARK not in (c.get("body") or "") or _relayed_answer(c))
    ]
    if heading == HEAD_WITHDRAWN:
        return "ready", f"withdrawn {since[:16]}, no session holds it"
    if heading == HEAD_MACHINE:
        return "set-aside", f"needs the machine, set aside {since[:10]}"
    if heading == HEAD_LANDED or heading.startswith(HEAD_LANDED + " "):
        # By its first word, so "Landed on main as abc" is a landing too.
        return "landed-open", f"landed {since[:16]} and the card is still open; close it by hand"
    if heading in (HEAD_BRAINSTORM, HEAD_QUESTION):
        if after:
            return "answered", f"Phillip replied {_when(after[-1])[:16]} to the {heading}"
        return "waiting-on-phillip", f"{heading} posted {since[:16]}, no reply yet"
    # Started, Resumed, or any heading this reader does not know, is a hold.
    age = _hours_since(freshest)
    if age is not None and age > STALE_HOURS:
        return "resume", f"held since {since[:16]}, {age:.0f} hours, the session is gone"
    return "underway", f"{heading or 'held'} {since[:16]}"


def _hours_since(stamp: str) -> float | None:
    try:
        then = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (datetime.now(timezone.utc) - then).total_seconds() / 3600


def load_comments(number: int) -> list[dict]:
    owner, name = repo_slug()
    return rest_pages(f"repos/{owner}/{name}/issues/{number}/comments", f"#{number} comment")


def cloud_branch(node: dict) -> str:
    return f"cloud/{node['number']}-{slugify(node['title'])[:32].rstrip('-')}"


# How many cards the cloud builds at once, Phillip's cap of 2026-11-21 (U291).
CLOUD_LANES = 10


def _card_lines(cards: list, states: dict, width: int) -> None:
    for node in cards:
        state, why = states[node["number"]]
        print(f"  #{node['number']:<4} {state:<{width}} {why}")
        print(f"        {node['title'][:72]}")


def cmd_cloud(args) -> int:
    """The cloud lane's queue: every open unit or residual card, by state."""
    lanes = max(1, getattr(args, "lanes", None) or CLOUD_LANES)
    graph = build_graph(load_issues())
    cards = [
        n for n in graph.values()
        if not n["closed"] and (n["unit"] or FINDING_LABEL in n["labels"])
    ]
    if not cards:
        print("No open unit or residual card. Nothing is the cloud's.")
        return 0
    states = {n["number"]: cloud_state(n, load_comments(n["number"])) for n in cards}
    held = [n for n in cards if states[n["number"]][0] == "underway"]
    take = [n for n in cards if states[n["number"]][0] in CLOUD_TAKE]
    take.sort(key=lambda n: (
        CLOUD_TAKE.index(states[n["number"]][0]), -n["reach"], -len(n["unblocks"]), n["number"]
    ))
    skipped = [n for n in cards if states[n["number"]][0] in CLOUD_SKIP]
    if skipped:
        print("Not the cloud's to take right now:")
        _card_lines(sorted(skipped, key=lambda n: n["number"]), states, 19)
        print()
    # Times come from the states' own lines, which end in the hold's timestamp.
    held.sort(key=lambda n: states[n["number"]][1].rsplit(" ", 1)[-1])
    if len(held) > lanes:
        # The earliest holds keep their lanes and every later one withdraws.
        keep = held[:lanes]
        print(f"MORE CARDS ARE HELD THAN THERE ARE LANES ({len(held)} for {lanes}): "
              + ", ".join(f"#{n['number']}" for n in held))
        for node in held:
            print(f"  #{node['number']:<4} {states[node['number']][1]}")
        print(f"{', '.join('#' + str(n['number']) for n in keep)} held first and keep "
              f"{'its lane' if lanes == 1 else 'their lanes'}. Every later holder")
        print("posts Withdrawn on its own card and stops. Nothing is offered.")
        return 1
    if held:
        print(f"Held, {len(held)} of {lanes} lane(s): "
              + ", ".join(f"#{n['number']}" for n in held))
    if len(held) >= lanes:
        print("Every lane is held. Nothing to take until one of them lands.")
        return 0
    if not take:
        print("Nothing for the cloud to take. Every open card is waiting, set aside, "
              "blocked or attended.")
        return 0
    print(f"The cloud may take ({len(take)}):")
    _card_lines(take, states, 12)
    print()
    top = take[0]
    state, _ = states[top["number"]]
    print(f"Take #{top['number']} ({state}). Branch: {cloud_branch(top)}, from origin/main.")
    return 0


def cmd_local(args) -> int:
    """The work only Phillip's Mac can do: every open card labelled attended."""
    graph = build_graph(load_issues())
    cards = sorted((n for n in graph.values() if n["attended"] and not n["closed"]),
                   key=lambda n: n["number"])
    if not cards:
        print("Nothing waits on your Mac.")
        return 0
    ready, waiting = [], []
    for node in cards:
        deps = parse_deps(node["body"]) or []
        still = [d for d in deps if d in graph and not graph[d]["closed"]]
        (waiting if still else ready).append((node, still))
    if ready:
        print(f"Ready at your Mac ({len(ready)}):")
        for node, _ in ready:
            print(f"  #{node['number']:<4} {node['title'][:76]}")
    if waiting:
        print(f"Waiting on the cloud ({len(waiting)}):")
        for node, still in waiting:
            on = ", ".join(f"#{d}" for d in still)
            print(f"  #{node['number']:<4} {node['title'][:60]}  (after {on})")
    print("Read one with: .venv/bin/python scripts/board.py show N")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    def command(name: str, help: str, func, number: bool = False):
        parser = sub.add_parser(name, help=help)
        if number:
            parser.add_argument("number", type=int)
        parser.set_defaults(func=func)
        return parser.add_argument

    command("next", "the ready queue, ranked by leverage", cmd_next)
    command("show", "print one issue's brief", cmd_show, number=True)
    command("start", "branch and mark In Progress", cmd_start, number=True)
    command("sync", "make the board match the repository", cmd_sync)(
        "--labels-only", action="store_true",
        help="skip the project board, for a token that cannot reach it",
    )
    command("audit", "report drift, exit 1 if the board is lying", cmd_audit)(
        "--labels-only", action="store_true", help="skip the project board"
    )
    closing = command(
        "closing", "refuse a Closes trailer while a register still owes that unit", cmd_closing
    )
    closing(
        "--message-file",
        help="a single commit message to judge; this is what the commit-msg hook passes",
    )
    closing(
        "--since", default="main",
        help="judge every commit after this ref instead of one message file",
    )
    closing(
        "--pull-request-head",
        help=(
            "a pull request's head branch; a `cloud/N-slug` head is judged as "
            "closing card N, the trailer its merge will write"
        ),
    )
    residuals = command(
        "residuals",
        "list the residual files waiting for a number, or number them",
        cmd_residuals,
    )
    residuals(
        "--land", action="store_true",
        help="on main, give each file the next R number and append it to the ledger",
    )
    residuals(
        "--search", nargs="+", metavar="WORD",
        help="print the ledger headings carrying every word, case insensitive, newest first",
    )
    residuals(
        "--archive", action="store_true",
        help=f"move the working file's oldest entries to docs/ledger while over {LEDGER_LIMIT} lines",
    )
    residuals(
        "--check", action="store_true",
        help="refuse a duplicated heading, a misnamed or overlapping archive, or a file over the limit",
    )
    residuals("--against", metavar="REV", help="with --check, refuse a heading REV has and now lacks")
    residuals("--unchanged", action="store_true", help="with --against, refuse a changed entry")
    command(
        "cloud", "the cloud lane's queue, read from the cards' comments over REST", cmd_cloud
    )(
        "--lanes", type=int, default=None,
        help=f"how many cards the cloud builds at once (default {CLOUD_LANES})",
    )
    command("local", "the attended cards only Phillip's Mac can do", cmd_local)
    args = parser.parse_args()
    try:
        return args.func(args)
    except Fail as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
