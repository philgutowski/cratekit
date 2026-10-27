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
    closing         refuse a `Closes #n` trailer while a register still owes Un,
                    and a residual file the landing could not read
    residuals       the residual files waiting for a number; `--land` numbers
                    them on main
    cloud           the cloud lane's queue: every open unit or residual card, by
                    the state its comments give it, and the one to take

A Claude Code cloud session sits behind a proxy that refuses GraphQL, so the
reads fall back to REST there (`load_issues_rest`), `start`, `sync` and
`audit` without `--labels-only` are not for it, and `cloud` is.

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
STATUS_ORDER = ["Ready", "In Progress", "In review", "Blocked", "Attended", "Done"]

# Statuses that mean somebody holds the card right now. `start` and a lane's
# builder set In Progress; the relay runner sets In review, its manifest's
# `in_review_status`, as its first tracker write. Neither can be derived from
# the graph, so a recomputation keeps them rather than undoing the holder's write.
UNDERWAY = ("In Progress", "In review")

DEPENDS_RE = re.compile(r"^\*\*Depends on:\*\*\s*(.+)$", re.MULTILINE)
CLOSES_WITH_RE = re.compile(r"^\*\*Closes with:\*\*\s*(.+)$", re.MULTILINE)
ISSUE_REF_RE = re.compile(r"#(\d+)")
UNIT_TITLE_RE = re.compile(r"^U(\d+):")


class Fail(Exception):
    pass


class Truncated(Fail):
    """A board read came back cut short, so it cannot be taken as the whole board."""


# The most rows one read asks `gh` for. `gh` pages internally up to this, so a
# read returns everything below it. It used to be 300, and once the project
# passed 300 items every newer card read as "not on the board" and no sync could
# repair it (U148). A read that returns exactly this many cannot be told from a
# truncated one, so it is refused rather than taken as whole. Each read is also
# checked against the count GitHub gives for it, which trusts no limit at all.
READ_LIMIT = 5000

# Every issue in the repository, any state, pull requests not included, which is
# the population `gh issue list --state all` reads. The placeholders are filled
# by `gh api` from the remote, so nothing here names the repository.
ISSUE_COUNT_QUERY = (
    "query($owner: String!, $name: String!) "
    "{ repository(owner: $owner, name: $name) { issues { totalCount } } }"
)


def whole(rows: list, what: str) -> list:
    """The rows of one read, refused if they fill the limit."""
    if len(rows) >= READ_LIMIT:
        raise Truncated(
            f"the {what} read returned {len(rows)} rows, the whole limit of "
            f"{READ_LIMIT}, so it is truncated and the board cannot be read from it. "
            f"Raise READ_LIMIT in scripts/board.py."
        )
    return rows


def gh(*args: str, parse: bool = False):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise Fail(f"gh {' '.join(args)}\n{result.stderr.strip()}")
    out = result.stdout.strip()
    return json.loads(out) if parse and out else out


def repo_slug() -> tuple[str, str]:
    """Owner and name from the git remote, never hardcoded."""
    try:
        data = gh("repo", "view", "--json", "owner,name", parse=True)
    except Fail:
        # `gh repo view` is a GraphQL call, which the proxy in front of a Claude
        # Code cloud session refuses outright. The checkout already names the
        # remote, so read it from there rather than fail before the first read.
        return remote_slug()
    return data["owner"]["login"], data["name"]


REMOTE_RE = re.compile(r"github\.com[:/]([^/\s]+)/([^/\s]+?)(?:\.git)?/?$")


def remote_slug() -> tuple[str, str]:
    """Owner and name parsed from the origin remote, for a session with no GraphQL."""
    url = subprocess.run(
        ["git", "remote", "get-url", "origin"], capture_output=True, text=True
    ).stdout.strip()
    match = REMOTE_RE.search(url)
    if not match:
        raise Fail(f"the origin remote {url!r} does not name a GitHub repository")
    return match.group(1), match.group(2)


def rest_pages(path: str, what: str) -> list:
    """Every row of a REST listing, a page of a hundred at a time, or refused.

    `gh api --paginate` cannot be used here: the proxy a cloud session sits
    behind rejects the numeric `repositories/<id>/` paths GitHub writes into
    its `Link` headers, so the second page fails by name. Page numbers are
    asked for explicitly instead, and the read ends on the first short page,
    which is whole by construction: a page shorter than a hundred is the last
    one. The read is still refused past READ_LIMIT, like every other read here.
    """
    joiner = "&" if "?" in path else "?"
    rows: list = []
    for page in range(1, READ_LIMIT // 100 + 2):
        batch = gh("api", f"{path}{joiner}per_page=100&page={page}", parse=True) or []
        rows.extend(batch)
        if len(batch) < 100:
            return rows
    raise Truncated(
        f"the {what} read ran past {READ_LIMIT} rows, so it is truncated. "
        f"Raise READ_LIMIT in scripts/board.py."
    )


# --------------------------------------------------------------------------
# reading the board


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
    # Counted BEFORE the read, so an issue filed between the two makes the read
    # longer than the count rather than shorter, and is never refused.
    try:
        total = gh(
            "api", "graphql", "-F", "owner={owner}", "-F", "name={repo}",
            "-f", f"query={ISSUE_COUNT_QUERY}",
            "--jq", ".data.repository.issues.totalCount",
        )
    except Fail:
        # No GraphQL at all is a cloud session's proxy, not a short read, and
        # the same issues are there over REST.
        return load_issues_rest()
    issues = gh(
        "issue",
        "list",
        "--state",
        "all",
        "--limit",
        str(READ_LIMIT),
        "--json",
        "number,title,state,body,labels",
        parse=True,
    )
    whole(issues, "issue")
    short_of_count(issues, int(total) if total.isdigit() else total, "issue")
    return issues


def load_issues_rest() -> list[dict]:
    """Every issue over REST, in the shape `gh issue list --json` gives.

    This is the read a Claude Code cloud session gets, where the GitHub proxy
    refuses every GraphQL call and allows the repository's own REST paths. REST
    lists pull requests among the issues, so those are dropped, and it writes
    states in lower case, so they are raised to the GraphQL spelling the graph
    reads. There is no separate count to check the read against; the page
    loop in `rest_pages` ends on a short page, which is the whole listing.
    """
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
    """What the board should say, from closure state, the graph, and a hold.

    Closure state wins. Otherwise a card somebody holds (UNDERWAY) keeps the
    status it holds, because no graph can derive who is building what; every
    other card is derived from the graph alone.
    """
    if node["closed"]:
        return "Done"
    if current in UNDERWAY:
        # A card on a branch stays on a branch, unit, residual or attended, since
        # a lane builds residual cards too and an attended unit is still built.
        # Recomputing it back is how a session loses track of work already
        # underway, and how a sync pulls a card out from under the runner.
        return current
    if node["attended"]:
        return "Attended"
    # A residual finding waits on whichever unit closes it, and is Ready when
    # nothing does, because then it is somebody's to pick up directly. A unit
    # waits on its dependencies the same way.
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

#: The reference forms that close an issue IN THIS REPOSITORY. Two of them, and
#: the two that are missing are missing on purpose.
#:
#: GitHub documents four. The two cross-repository forms, `owner/repo#n` and the
#: full issue URL, close an issue in the NAMED repository and nothing here. A
#: previous version matched both and read the number out of them, so
#: `fixes numpy/numpy#36` and a link to an upstream pyrekordbox issue each
#: refused a commit over a unit they have no relationship to. That is not
#: hypothetical: this repository VENDORS pyrekordbox, the owed unit numbers run
#: from 8 to 38, and upstream issue numbers collide with them constantly, so a
#: vendor bump citing an upstream issue is the realistic trigger.
#:
#: Reading them correctly would mean knowing this repository's own slug, and
#: `repo_slug()` needs `gh`, which would end this function's purity and with it
#: its place in a hook and in the dependency-free CI job. Dropping them costs
#: nothing, because a commit closing a unit here writes `#n` or `GH-n`.
#:
#: Ordered longest-first: at a given position the alternation tries branches left
#: to right, so the bare `#n` must come last.
REFERENCE_FORMS = (
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
    authoritative. Recorded in R-320.
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

    Nine keywords times the two reference forms that close an issue HERE, the
    bare `#n` and `GH-n`. GitHub documents two more, `owner/repo#n` and the full
    issue URL, and both are deliberately not matched: they close an issue in the
    named repository, so matching them refused commits over units they had no
    relationship to. See :data:`REFERENCE_FORMS`.

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
    text: str,
    owed: dict[int, list[str]] | None = None,
    *,
    raw: bool = True,
    units: dict[int, int] | None = None,
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

    ``units`` MAPS AN ISSUE NUMBER TO A UNIT NUMBER, and it is optional because
    of a limit rather than a preference. A trailer names an ISSUE. Both registers
    name a UNIT. Those coincide for most units here and not for all: U38 is issue
    #51, and U39 through U61 are issues #57 through #79. The mapping lives in the
    issue TITLES, which is to say on GitHub, and this function's whole value is
    that it needs no token, so it cannot go and get it.

    So the caller supplies it when it has it, and `audit` does through
    `units_by_issue_number`. When it does not, an issue number is read as a unit
    number, WHICH IS A GUESS, and the two ways it is wrong are not equally
    priced. Against a mismatched unit it MISSES, and a miss is a close that has
    already cascaded. Against a number that is some other unit's issue it refuses
    wrongly, and the refusal says which assumption it made so the reader can see
    the guess rather than trust the sentence. Recorded as a residual with its
    measured reach: twenty four units were mismatched on 2026-09-10 and none of
    them was owed a module, so the miss was real and unreachable that day.
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
    """For each owed module that is absent, what its package DOES contain.

    THE DIAGNOSIS, moved to where the refusal is read. A register key can name a
    module nobody will ever build, and the loudest symptom is a permanent exit 2
    with no hint why. `cratekit.write.rebuild` absent while
    `cratekit.write.tree_rebuild` exists is a one-word spelling difference that
    is invisible in a message saying only that a module is owed.

    This replaces a rule that would have ASSERTED the mismatch. That rule was
    rejected on measurement: `cratekit.core.restore` is U32's live key today and
    a substring heuristic would false-positive on it against a unit that did
    nothing wrong. Telling the reader what is in the package costs no false
    positives at all, and the failure was never silent to begin with, because a
    register entry keeps its unit owed for as long as it sits in the file.
    """
    root = Path(__file__).resolve().parent.parent / "src"
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
            # A refusal a person can act on, not a traceback. This runs inside a
            # git hook, where an unhandled exception surfaces as a stack trace in
            # place of the commit message editor and reads as the tool being
            # broken rather than the invocation being wrong.
            print(f"board: no commit message at {args.message_file!r}", file=sys.stderr)
            return 1
        text = path.read_text()
    else:
        # ONE MESSAGE PER RECORD, NOT ONE CONCATENATED BLOB, and the separator is
        # what makes that true. `--format=%B` alone runs the messages together
        # with a blank line between them, and the keyword-to-reference gap in
        # CLOSES_RE spans newlines, so a commit whose subject ends with the word
        # "closes" followed by a commit whose body opens with `#36` produced a
        # closing reference NEITHER commit contains. Measured on 2026-09-10.
        # A false refusal manufactured by the reader is worse than one a person
        # wrote, because there is no line to reword: the commits are already
        # history and the only way past the check is to delete it.
        #
        # A NUL is the separator because it is the one byte a commit message
        # cannot contain. Any printable sentinel is a string somebody can type.
        result = subprocess.run(
            ["git", "log", "--format=%B%x00", f"{args.since}..HEAD"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            # No such ref, a shallow clone, or no repository. Nothing to judge
            # rather than a refusal, because a check that fails on a machine it
            # cannot read is a check somebody removes from the hook.
            print("board: no commit range to read; no trailer checked")
            return _report([])
        problems: list[str] = []
        for message in result.stdout.split("\0"):
            if message.strip():
                # POST-cleanup messages. Nothing to strip, and stripping could
                # only lose a real trailer.
                problems += unresolved_closes(message, raw=False)
        return _report(problems)
    return _report(unresolved_closes(text, raw=True))


def _report(problems: list[str]) -> int:
    # A RESIDUAL FILE THE LANDING CANNOT READ is refused here, on every path,
    # because this is the check that runs before a landing: in the commit-msg
    # hook and in CI over the pushed range. A file with no title or no Found
    # line would reach main and stop `residuals --land` there, after the
    # branch that wrote it is gone.
    malformed = residual_file_problems()
    if not problems and not malformed:
        return 0
    if problems:
        print("CONTRADICTION: a unit cannot close while a register still owes it work.")
        for line in problems:
            print(f"  {line}")
        print()
        print("This is the same comparison `audit` makes, run BEFORE the close rather")
        print("than after it. Afterwards the close has already cascaded and `sync`")
        print("will not repair it.")
    if malformed:
        if problems:
            print()
        print("A RESIDUAL FILE CANNOT LAND as it stands:")
        for line in malformed:
            print(f"  {line}")
        print()
        print("docs/residuals/README.md is the form: a title and a Found line in the")
        print("frontmatter, then the body.")
    return 2


# --------------------------------------------------------------------------
# writing the board


# The project and its fields, asked of the owner by number. One query, one
# point, where `gh project field-list` and `gh project view` were a listing each
# (U151). The owner is a user or an organization and GraphQL asks each by its
# own field, so the user is asked first and the organization second.
CONTEXT_QUERY = (
    "query($login: String!, $number: Int!) { %s(login: $login) { "
    "projectV2(number: $number) { id url fields(first: 100) { totalCount nodes { "
    "... on ProjectV2SingleSelectField { id name options { id name } } "
    "... on ProjectV2Field { id name } } } } } }"
)

# Each issue's own cards, a page of a hundred issues at a time. GitHub meters
# GraphQL by the node, 5,000 points an hour for the whole account, and this
# costs one point a page, where `gh project item-list` cost about 101 a page of
# a hundred cards (measured 2026-10-14). Archived cards are left out, as the
# item listing left them out: an archived card reads as not on the board and
# `sync` adds it again, which is what it did before U151, and archiving Done
# cards is a decision of its own.
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
    """Every issue's card on the project, read from the issues, never the project.

    A card is an issue's membership of project `PROJECT_NUMBER` owned by
    `owner`; a membership of any other project, or of another owner's project
    with the same number, is not this board's. Refused as `Truncated`, like the
    issue read, when the pages come back short of the repository's own issue
    count or an issue's memberships come back short of their count.
    """
    items: dict = {}
    seen: list[int] = []
    total = None
    after = None
    # A page per hundred issues, so this bound is READ_LIMIT issues, and a
    # cursor that never ends is refused rather than followed for ever.
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
            f"truncated. Raise READ_LIMIT in scripts/board.py."
        )
    short_of_count(seen, total, "project membership")
    return items


# --------------------------------------------------------------------------
# commands


def cmd_next(args) -> int:
    owner, _ = repo_slug()
    graph = build_graph(load_issues())
    try:
        # The context first: a token that cannot see the project still reads the
        # issues' memberships, as none at all, and an empty read is not a board
        # with nothing underway.
        project_context(owner)
        items = project_items(owner)
    except Truncated:
        # A cut short read is not a token that cannot see the board, and the
        # queue below would offer a held card the read missed.
        raise
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
        n for n in graph.values() if items.get(n["number"], {}).get("status") in UNDERWAY
    ]
    busy = {n["number"] for n in in_progress}
    ready = [n for n in ready if n["number"] not in busy]
    ready.sort(key=lambda n: (-n["reach"], -len(n["unblocks"]), n["number"]))

    if in_progress:
        # In review is the relay runner's hold and In Progress a session's or a
        # lane's, so name which, rather than tell a reader to finish a card a
        # background run owns.
        print("Already underway, never start one of these again:")
        for node in in_progress:
            status = items[node["number"]]["status"]
            print(f"  #{node['number']:<3} {status:<11} {node['title']}")
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

    # The board is read BEFORE the branch exists, so a read that refuses leaves
    # the checkout on main with nothing to undo.
    ctx = project_context(owner)
    items = project_items(owner)
    item = items.get(node["number"])

    subprocess.run(["git", "checkout", "-b", branch], check=True)

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
    else:
        print()
        print(f"Branch {branch} is checked out, but #{node['number']} is NOT on the")
        print("project board, so nothing there shows it is taken and `next` will")
        print("still offer it. Run `board.py sync` to add it, then set it In Progress.")
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


#: The ledger, append only, and the folder a residual waits in for its number.
#: Module level so a test can point both at a fixture.
LEDGER = Path(__file__).resolve().parent.parent / "docs" / "residual-findings.md"
RESIDUALS_DIR = Path(__file__).resolve().parent.parent / "docs" / "residuals"

#: The frontmatter a residual file carries, which is exactly what a ledger
#: entry opens with: the heading's title and the Found line. ``issue`` says the
#: finding meets METHOD's board bar, so whoever numbers it files the issue.
RESIDUAL_REQUIRED = ("title", "found")
RESIDUAL_OPTIONAL = {"issue": ("yes", "no")}


def residual_titles(ledger: Path | None = None) -> dict[int, str]:
    """Every ``## R-N.`` heading in the residual file, by number.

    Read as text rather than parsed as a document, because the only structure
    this needs is the heading line and the file is append only by rule.
    """
    source = LEDGER if ledger is None else ledger
    if not source.exists():
        return {}
    found: dict[int, str] = {}
    for line in source.read_text().splitlines():
        match = re.match(r"^## R-(\d+)\.\s*(.+?)\s*$", line)
        if match:
            found[int(match.group(1))] = match.group(2)
    return found


def residual_files(folder: Path | None = None) -> list[Path]:
    """The residuals waiting for a number, in the order they will take one.

    Name order, so a landing that numbers two files at once numbers them the
    same way on every machine. The README describes the form and is not one.
    """
    folder = RESIDUALS_DIR if folder is None else folder
    if not folder.is_dir():
        return []
    paths = sorted(p for p in folder.glob("*.md") if p.name != "README.md")
    # ONLY WHAT GIT KNOWS, staged or committed. An untracked draft is not
    # filed yet: judging it refused every unrelated commit through the hook,
    # and landing it numbered a finding nobody had committed. A folder git
    # cannot read, a fixture outside any repository, is taken whole.
    listed = subprocess.run(
        ["git", "ls-files", "-z", "--", "."],
        cwd=folder,
        capture_output=True,
        text=True,
    )
    if listed.returncode != 0:
        return paths
    known = {name for name in listed.stdout.split("\0") if name}
    return [p for p in paths if p.name in known]


def read_residual_file(path: Path) -> tuple[dict[str, str], str]:
    """The frontmatter and the body of one residual file.

    Raises ValueError naming what is wrong. Parsed by hand rather than as YAML
    because this script imports only the standard library, and the form is
    one ``key: value`` per line between two ``---`` lines.
    """
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
    # "R-12. A title" is a filer numbering its own finding. "R-204 is
    # discharged by half" is a title citing another residual, which the
    # ledger already holds several of, so only the heading's own shape is
    # refused.
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

    THE NUMBER IS TAKEN BY WHOEVER LANDS FIRST, never by whoever files first,
    which is the whole point: two branches cut from one base each file a
    residual without a number, merge in either order, and the landing gives
    each the next number past the ledger's highest at that moment. A number
    once given is the finding's for life, so this only appends.

    Validates every file before writing anything, so a malformed one leaves
    the ledger and the folder exactly as they were. Returns ``(number, title,
    meets the board bar)`` per file landed.
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
    # A FILE THAT LANDED ONCE CAN COME BACK. Landing deletes it, and a branch
    # that edited it afterwards brings it back through a modify and delete
    # conflict resolved the wrong way. Its heading is then already in the
    # ledger, and numbering it again would file one finding twice.
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
        # The separator the ledger's recent entries carry between them.
        text = text.rstrip("\n") + "\n\n---\n\n"
        text += f"## R-{number}. {meta['title']}\n\n**Found:** {meta['found']}\n\n{body}\n"
        landed.append((number, meta["title"], meta.get("issue") == "yes"))
    ledger.write_text(text)
    for path, _, _ in parsed:
        path.unlink()
    return landed


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


def units_by_issue_number(graph: dict) -> dict[int, int]:
    """Unit number to issue number, read off the titles, because nothing else has it.

    THE MAPPING LIVES ON GITHUB AND NOWHERE IN THIS REPOSITORY, which is the
    whole reason it is derived here rather than looked up. `CLAUDE.md` states the
    fact plainly, "an issue number usually matches its unit number and it is not
    guaranteed", and the title is where the unit number is written down.

    A title claiming a unit number some other issue already claimed is dropped
    rather than allowed to overwrite, because a duplicate is a board editing
    mistake and picking the later one silently answers with the wrong issue.
    """
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

    A UNIT NUMBER IS NOT AN ISSUE NUMBER, and this used to index the graph with
    one as though it were the other. The registers name UNITS, `U25`, and the
    graph is keyed by ISSUE. They coincide for most units here and not for all:
    U38 is issue #51, and U39 through U61 are issues #57 through #79. So a
    register owing U51 looked up issue #51, which is U38's, and answered about
    the wrong unit in both directions, silently reporting a contradiction over a
    unit nothing owed and missing the one that was owed. Measured 2026-09-10:
    twenty four units are mismatched, and none of them was owed a module that
    day, which is why nothing had ever surfaced it. Resolved through the title,
    which is the only place the mapping exists, and the graph already carries it.

    ``owed`` IS SUPPLIED BY A CALLER THAT HAS ONE, exactly as `unresolved_closes`
    takes it, and defaults to the live registers. R-322 is the finding that
    nothing drove this function at all, and the register is half of why: keyed to
    whatever `main` happens to owe today, a test passes for a reason that has
    nothing to do with the code and goes red the day somebody discharges a
    marker. The graph is the other half, and that one is answered at the caller,
    since `build_graph` is what a test drives instead of `gh`.
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
                items[number] = {"id": added["id"], "status": None, "unblocks": None}
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

        # Written only when the stored number differs, so a sync over a board
        # with no drift writes nothing. It used to rewrite every card on every
        # sync, about 300 mutations a run (U151).
        unblocks = len(node["unblocks"])
        if item and ctx and ctx["unblocks_field"] and apply and item.get("unblocks") != unblocks:
            gh(
                "project", "item-edit", "--id", item["id"],
                "--project-id", ctx["id"], "--field-id", ctx["unblocks_field"],
                "--number", str(unblocks),
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
        print("the unit is not finished, or clear the register entry because it is.")
        print("TWO REGISTERS CAN OWE, so read the module named above to know which")
        print("file to open: a dotted module in tests/_pending.py PENDING, or a")
        print("planned_in marker on a src/cratekit/cli/registry.py entry. Naming")
        print("only the first sent people to a file the entry was never in.")
        print("Overwriting one from the other would let the wrong one win.")

    malformed = residual_file_problems()
    if malformed:
        print()
        print(f"RESIDUAL FILES THAT CANNOT LAND, {len(malformed)}. A sync cannot fix these:")
        for line in malformed:
            print(f"  {line}")
        clashes = clashes + malformed

    waiting = residual_files()
    if waiting:
        print()
        print(f"{len(waiting)} residual file(s) in docs/residuals wait for a number.")
        print("On main, after the merge that carried them:")
        print("    .venv/bin/python scripts/board.py residuals --land")

    if not drift and not clashes:
        print("The board matches the repository.")
        return 0
    return 2 if clashes else 1


def cmd_residuals(args) -> int:
    """List the residuals waiting for a number, or number them on main."""
    malformed = residual_file_problems()
    if malformed:
        print("A RESIDUAL FILE CANNOT LAND as it stands:")
        for line in malformed:
            print(f"  {line}")
        return 2
    waiting = residual_files()
    if not args.land:
        highest = max(residual_titles(), default=0)
        print(f"The ledger's highest is R-{highest}. {len(waiting)} file(s) wait:")
        for path in waiting:
            print(f"  docs/residuals/{path.name}")
        return 0
    # ON MAIN AND NOWHERE ELSE. A number given on a branch is a number given
    # by whoever FILED, which is the race this folder exists to remove: two
    # branches would each take the ledger's highest plus one.
    branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        cwd=LEDGER.parent,
    ).stdout.strip()
    if branch != "main":
        print(
            f"board: residuals are numbered on main, after the merge that carried "
            f"them, and this checkout is on {branch or 'no branch'}",
            file=sys.stderr,
        )
        return 1
    # BEHIND THE REMOTE, the ledger's highest is stale, and a number given
    # here may already be taken there. Read against the last fetch, since a
    # check that needs the network is a check that fails offline.
    behind = subprocess.run(
        ["git", "rev-list", "--count", "main..origin/main"],
        capture_output=True,
        text=True,
        cwd=LEDGER.parent,
    )
    if behind.returncode == 0 and behind.stdout.strip() not in ("", "0"):
        print(
            f"board: main is {behind.stdout.strip()} commit(s) behind origin/main as "
            f"last fetched; pull first, or a number given here may be taken there",
            file=sys.stderr,
        )
        return 1
    try:
        landed = land_residuals()
    except ValueError as exc:
        print(f"board: nothing numbered, {exc}", file=sys.stderr)
        return 2
    if not landed:
        print("No residual file waits for a number.")
        return 0
    for number, title, board_bar in landed:
        print(f"R-{number}. {title}")
        if board_bar:
            print(f"    meets the board bar: file the issue titled R-{number}: {title}")
    print()
    print("Commit the ledger and the deleted files together:")
    print("    git add docs/residual-findings.md docs/residuals")
    print('    git commit -m "docs(residuals): number what landed"')
    return 0


# --------------------------------------------------------------------------
# the cloud lane

# The label a residual's card carries. Held in a constant so the word is never
# followed by a quoted string, which the citation rule in test_reserved_causes
# reads as a residual title.
FINDING_LABEL = "residual"

# A comment the cloud session wrote carries this footer, which the person's
# own comments never do. It is how an answer is told from a question when every
# comment on the card is posted by the same login.
SESSION_MARK = "Generated by [Claude Code]"

# The headings a cloud session writes, as this reader reads them. The spelling
# is fixed because the reader reads headings and nothing else.
HEAD_STARTED = "started"
HEAD_RESUMED = "resumed"
HEAD_PLAN = "plan"
HEAD_PROGRESS = "progress"
HEAD_BRAINSTORM = "brainstorm"
HEAD_QUESTION = "question for phillip"
HEAD_MACHINE = "needs the machine"
HEAD_LANDED = "landed"

# A hold older than this with nothing landed after it is read as a session
# that died, and the next session resumes the card from whatever it pushed.
STALE_HOURS = 8

# What the cloud takes, in the order it takes them. A card that is held, or
# waiting on a person, or set aside for the machine, is never offered.
CLOUD_TAKE = ("answered", "resume", "ready")
CLOUD_SKIP = ("underway", "waiting-on-phillip", "set-aside", "landed-open", "blocked", "attended")


def comment_heading(body: str) -> str:
    """The first line of a comment, as a heading: markdown and emphasis stripped,
    anything after a colon or comma dropped, lower case."""
    for line in (body or "").splitlines():
        text = line.strip().lstrip("#").strip().strip("*_").strip()
        if text:
            return re.split(r"[:,]", text, maxsplit=1)[0].strip().strip("*_").lower()
    return ""


def _when(comment: dict) -> str:
    return comment.get("created_at") or ""


def cloud_state(node: dict, comments: list[dict]) -> tuple[str, str]:
    """What the cloud lane owes a card, read from the card's comments alone.

    The cloud session never writes a label or a status, so its hold on a card
    is its own last comment, by heading, and the person's reply is any comment
    without the session footer written after it. Returns a state and a line
    saying why.
    """
    if node["attended"]:
        return "attended", "needs Phillip at the machine"
    if node["open_deps"]:
        return "blocked", "waits on " + ", ".join(f"#{d}" for d in node["open_deps"])

    ordered = sorted(comments, key=_when)
    mine = [c for c in ordered if SESSION_MARK in (c.get("body") or "")]
    if not mine:
        return "ready", "no cloud session has taken it"
    # The state is the session's last comment that is not a progress note,
    # and every comment it writes, progress included, refreshes the hold, so
    # a build that reports as it goes is never read as a session that died.
    stated = [c for c in mine if comment_heading(c.get("body") or "") not in (HEAD_PLAN, HEAD_PROGRESS)]
    last = stated[-1] if stated else mine[-1]
    last_mine = (comment_heading(last.get("body") or ""), _when(last))
    freshest = _when(mine[-1])

    heading, since = last_mine
    after = [
        c for c in ordered
        if _when(c) > since and SESSION_MARK not in (c.get("body") or "")
    ]
    if heading == HEAD_MACHINE:
        return "set-aside", f"needs the machine, set aside {since[:10]}"
    if heading == HEAD_LANDED:
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
    from datetime import datetime, timezone

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


def cmd_cloud(args) -> int:
    """The cloud lane's queue: every open unit or residual card, by state."""
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
    take.sort(
        key=lambda n: (
            CLOUD_TAKE.index(states[n["number"]][0]),
            -n["reach"],
            -len(n["unblocks"]),
            n["number"],
        )
    )
    skipped = [n for n in cards if states[n["number"]][0] in CLOUD_SKIP]
    if skipped:
        print("Not the cloud's to take right now:")
        for node in sorted(skipped, key=lambda n: n["number"]):
            state, why = states[node["number"]]
            print(f"  #{node['number']:<4} {state:<19} {why}")
            print(f"        {node['title'][:72]}")
        print()
    if held:
        # One builder at a time. Two sessions on two cards would each merge
        # main under the other, which is the halt the feeder called
        # remote_advanced, so a held card holds the whole lane.
        print(f"The lane is held by #{held[0]['number']}. Nothing to take until it lands.")
        return 0
    if not take:
        print("Nothing for the cloud to take. Every open card is waiting, set aside, blocked or attended.")
        return 0
    print(f"The cloud may take ({len(take)}):")
    for node in take:
        state, why = states[node["number"]]
        print(f"  #{node['number']:<4} {state:<12} {why}")
        print(f"        {node['title'][:72]}")
    print()
    top = take[0]
    state, _ = states[top["number"]]
    print(f"Take #{top['number']} ({state}). Branch: {cloud_branch(top)}, from origin/main.")
    return 0


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
    residuals = sub.add_parser(
        "residuals",
        help="list the residual files waiting for a number, or number them",
    )
    residuals.add_argument(
        "--land",
        action="store_true",
        help="on main, give each file the next R number and append it to the ledger",
    )
    residuals.set_defaults(func=cmd_residuals)
    cloud = sub.add_parser(
        "cloud", help="the cloud lane's queue, read from the cards' comments over REST"
    )
    cloud.set_defaults(func=cmd_cloud)
    args = parser.parse_args()
    try:
        return args.func(args)
    except Fail as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
