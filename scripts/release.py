#!/usr/bin/env python3
"""Cut a Cratekit release on request: a semantic version tag with notes (U159).

    .venv/bin/python scripts/release.py plan
    .venv/bin/python scripts/release.py cut --bump minor

`plan` lists what reached `main` since the last `vX.Y.Z` tag (or the root
commit), reading every commit in the range rather than the first parent line
(U215), and proposes a bump with a reason for each landing. `--since` and
`--tip` rerun a past range, and `--notes` prints only its release body. It
writes nothing.

`cut` refuses unless the checkout is on `main`, clean, equal to `origin/main`,
and the battery is clean on that commit (the `cloud_battery.py compare`
verdict, or `--mac-battery` here). It then writes the version into both files,
commits `release: vX.Y.Z`, tags, pushes both atomically, and publishes a
GitHub release over REST, since GraphQL is refused on a cloud container.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = Path("pyproject.toml")
INIT = Path("src") / "cratekit" / "__init__.py"
VERDICT = Path(".cloud-battery") / "last-compare.txt"
DEFAULT_REPO = "philgutowski/cratekit"

BUMPS = ("patch", "minor", "major")

TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
PYPROJECT_VERSION_RE = re.compile(r'^version = "([^"]*)"$', re.MULTILINE)
INIT_VERSION_RE = re.compile(r'^__version__ = "([^"]*)"$', re.MULTILINE)

# A title's kind of change: `!` before the colon or BREAKING breaks, a residual or
# fix repairs, a unit is new behaviour, anything else the smallest claim.
BREAKING_RE = re.compile(r"\bBREAKING\b|^[A-Za-z0-9-]+(?:\([^)]*\))?!:")
UNIT_RE = re.compile(r"^(?:U\d+\b|merge\(u\d+[a-z0-9-]*\):)", re.IGNORECASE)
REPAIR_RE = re.compile(r"^(?:R-\d+\b|merge\(r-?\d+[a-z0-9-]*\):|fix\b|fix\()", re.IGNORECASE)

# A unit or residual landing merge subject, a landing on whatever line it sits.
LANDING_RE = re.compile(r"^merge\((?:u\d+|r-?\d+)[a-z0-9-]*\):", re.IGNORECASE)

# A merge of `main` into a local `main`, which carries landings and is never one.
MAIN_SYNC_RE = re.compile(
    r"^Merge (?:(?:remote-tracking )?branch '(?:[\w.-]+/)?main'(?: of \S+)?"
    r"|(?:[\w.-]+/)?main)(?: into main)?$"
)


Runner = Callable[[Sequence[str]], subprocess.CompletedProcess]


def run(argv: Sequence[str]) -> subprocess.CompletedProcess:
    return subprocess.run(list(argv), capture_output=True, text=True, check=False)


def git(runner: Runner, *argv: str) -> str:
    done = runner(["git", *argv])
    if done.returncode != 0:
        raise ReleaseError(f"git {' '.join(argv)} failed: {done.stderr.strip()}")
    return done.stdout.strip()


class ReleaseError(Exception):
    """A refusal a person can act on, printed as a sentence and exit 1."""


def parse_tag(name: str) -> tuple[int, int, int] | None:
    """A `vX.Y.Z` tag as a tuple, or None for any tag that is not one."""
    match = TAG_RE.match(name.strip())
    return tuple(int(part) for part in match.groups()) if match else None


def latest_tag(names: Iterable[str]) -> str | None:
    """The highest `vX.Y.Z` among ``names``; tags that are not versions are ignored."""
    versions = [(v, n) for n in names if (v := parse_tag(n)) is not None]
    return max(versions)[1] if versions else None


def bumped(version: tuple[int, int, int], bump: str) -> tuple[int, int, int]:
    major, minor, patch = version
    if bump == "major":
        return (major + 1, 0, 0)
    if bump == "minor":
        return (major, minor + 1, 0)
    if bump == "patch":
        return (major, minor, patch + 1)
    raise ReleaseError(f"no such bump {bump!r}; one of {', '.join(BUMPS)}")


def dotted(version: tuple[int, int, int]) -> str:
    return ".".join(str(part) for part in version)


def parse_dotted(text: str) -> tuple[int, int, int]:
    found = parse_tag(f"v{text}")
    if found is None:
        raise ReleaseError(f"the current version {text!r} is not X.Y.Z")
    return found


@dataclass(frozen=True)
class Landing:
    """One thing that reached `main`: a pull request, or a merge made without one."""

    title: str
    sha: str
    number: int | None = None
    url: str | None = None

    def line(self) -> str:
        if self.number is not None:
            return f"- #{self.number} {self.title}"
        return f"- {self.title} ({self.sha[:7]})"


def classify(title: str) -> tuple[str, str]:
    """The bump one landing asks for, and why, read from its title."""
    if BREAKING_RE.search(title):
        return "major", "marked as breaking existing libraries or configs"
    if REPAIR_RE.match(title):
        return "patch", "a fix or a residual repaired"
    if UNIT_RE.match(title):
        return "minor", "a unit, new verbs or behaviour"
    return "patch", "neither a unit nor marked breaking, so the smallest claim"


def propose(landings: Sequence[Landing]) -> tuple[str | None, list[str]]:
    """The largest bump any landing asks for, and one reason line per landing."""
    if not landings:
        return None, []
    reasons = []
    chosen = "patch"
    for landing in landings:
        kind, why = classify(landing.title)
        if BUMPS.index(kind) > BUMPS.index(chosen):
            chosen = kind
        reasons.append(f"{kind:5}  {landing.line()[2:]}: {why}")
    return chosen, reasons


def range_commits(
    runner: Runner, since: str | None, tip: str, *, first_parent: bool = False
) -> list[tuple[str, str, list[str]]]:
    """Each commit after ``since`` up to ``tip``, newest first: sha, subject, parents.

    The whole range, or only the first parent line with ``first_parent``.
    """
    span = f"{since}..{tip}" if since else tip
    argv = ["log", "--date-order", "--format=%H%x1f%P%x1f%s", span]
    if first_parent:
        argv.insert(1, "--first-parent")
    # The subject last, since `str.strip` would lose the root's empty parents field.
    out = git(runner, *argv)
    commits = []
    for line in out.splitlines():
        if not line.strip():
            continue
        sha, parents, subject = line.split("\x1f", 2)
        commits.append((sha, subject, parents.split()))
    return commits


def landings_since(
    runner: Runner, since: str | None, tip: str, pulls: Sequence[dict]
) -> tuple[list[Landing], list[Landing]]:
    """The pull requests merged in the range, and the merges made without one.

    The whole range is read, since a local pull puts landings on the second
    parent side (U215). A pull request lands at its merge commit if in range,
    else at the merge that took its head (landings first), else at its head (a
    fast forward); every landing merge that took the head is claimed with it. A
    head outside the range shipped before it. An unclaimed merge is a landing
    on the first parent line, or off it with a landing subject; a merge of
    `main` into `main` never is.
    """
    commits = range_commits(runner, since, tip)
    first_line = {sha for sha, _s, _p in range_commits(runner, since, tip, first_parent=True)}
    by_sha = {sha: (subject, parents) for sha, subject, parents in commits}
    order = {sha: i for i, (sha, _s, _p) in enumerate(reversed(commits))}
    taken_by: dict[str, list[str]] = {}
    for sha, (_subject, parents) in by_sha.items():
        for parent in parents[1:]:
            taken_by.setdefault(parent, []).append(sha)

    def lands(sha: str) -> bool:
        """Whether a merge is a landing when no pull request claims it."""
        subject = by_sha[sha][0]
        if MAIN_SYNC_RE.match(subject):
            return False
        return sha in first_line or bool(LANDING_RE.match(subject))

    prs: list[Landing] = []
    claimed: set[str] = set()
    for pull in pulls:
        if not pull.get("merged_at"):
            continue
        merge_sha = pull.get("merge_commit_sha") or ""
        head_sha = (pull.get("head") or {}).get("sha") or ""
        taking = (
            sorted(
                taken_by.get(head_sha, ()),
                key=lambda sha: (not lands(sha), order[sha]),
            )
            if head_sha in by_sha
            else []
        )
        if merge_sha in by_sha:
            landed_at = merge_sha
        elif taking:
            landed_at = taking[0]
        elif head_sha in by_sha:
            landed_at = head_sha
        else:
            continue
        claimed.add(landed_at)
        claimed.update(sha for sha in taking if lands(sha))
        title, number, url = pull.get("title", ""), pull.get("number"), pull.get("html_url")
        prs.append(Landing(title, landed_at, number, url))
    prs.sort(key=lambda landing: order[landing.sha])
    direct = [
        Landing(title=subject, sha=sha)
        for sha, subject, parents in reversed(commits)
        if len(parents) > 1 and sha not in claimed and lands(sha)
    ]
    return prs, direct


def merged_pulls(runner: Runner, repo: str) -> list[dict]:
    """Every closed pull request against `main`, page by page (`--paginate` needs GraphQL)."""
    pulls: list[dict] = []
    page = 1
    while True:
        done = runner(
            ["gh", "api", f"repos/{repo}/pulls?state=closed&base=main&per_page=100&page={page}"]
        )
        if done.returncode != 0:
            raise ReleaseError(f"could not read the pull requests: {done.stderr.strip()}")
        batch = json.loads(done.stdout or "[]")
        pulls += batch
        if len(batch) < 100:
            return pulls
        page += 1


def upgrade_command(repo: str, tag: str) -> str:
    return f'pipx install --force "cratekit @ git+https://github.com/{repo}@{tag}"'


def notes(tag: str, repo: str, prs: Sequence[Landing], direct: Sequence[Landing]) -> str:
    """The release body: what landed, then how to upgrade."""
    lines = [f"Cratekit {tag}.", "", "## Pull requests", ""]
    lines += [landing.line() for landing in prs] or ["None in this release."]
    if direct:
        lines += ["", "## Merged without a pull request", ""]
        lines += [landing.line() for landing in direct]
    lines += ["", "## Upgrade", "", "    " + upgrade_command(repo, tag), ""]
    lines += [
        "If you installed extras, name them in brackets after `cratekit`, for",
        '`"cratekit[analysis] @ git+..."`. `crate doctor` prints the command',
        "with the extras this copy carries.",
        "",
    ]
    return "\n".join(lines)


def read_versions(root: Path) -> tuple[str, str]:
    pyproject = PYPROJECT_VERSION_RE.findall((root / PYPROJECT).read_text())
    init = INIT_VERSION_RE.findall((root / INIT).read_text())
    if len(pyproject) != 1 or len(init) != 1:
        raise ReleaseError(
            "expected exactly one version line in each of pyproject.toml and "
            f"src/cratekit/__init__.py, found {len(pyproject)} and {len(init)}"
        )
    return pyproject[0], init[0]


def write_version(root: Path, version: str) -> None:
    """Write ``version`` into both files, then read both back and refuse if they differ."""
    for path, pattern, template in (
        (root / PYPROJECT, PYPROJECT_VERSION_RE, 'version = "{}"'),
        (root / INIT, INIT_VERSION_RE, '__version__ = "{}"'),
    ):
        text, count = pattern.subn(template.format(version), path.read_text(), count=1)
        if count != 1:
            raise ReleaseError(f"no version line to write in {path.relative_to(root)}")
        path.write_text(text)
    written = read_versions(root)
    if written != (version, version):
        raise ReleaseError(f"the version read back as {written}, not {version} in both")


def refusals(runner: Runner, root: Path, *, mac_battery: bool) -> list[str]:
    """Every reason this checkout may not be released, empty when it may."""
    problems = []
    branch = git(runner, "rev-parse", "--abbrev-ref", "HEAD")
    if branch != "main":
        problems.append(f"the checkout is on {branch!r}, not main")
    if git(runner, "status", "--porcelain"):
        problems.append("the working tree is not clean")
    head = git(runner, "rev-parse", "HEAD")
    remote = runner(["git", "rev-parse", "--verify", "--quiet", "origin/main"])
    if remote.returncode != 0:
        problems.append("there is no origin/main to compare against; fetch it")
    elif remote.stdout.strip() != head:
        problems.append("HEAD is not origin/main as last fetched; fetch and pull or push first")
    problem = mac_battery_problem(runner) if mac_battery else verdict_problem(root, head)
    if problem:
        problems.append(problem)
    return problems


def verdict_problem(root: Path, head: str) -> str | None:
    """Why the recorded `cloud_battery.py compare` verdict does not clear ``head``."""
    path = root / VERDICT
    if not path.is_file():
        return (
            "no battery verdict: run `cloud_battery.py compare` on this commit, "
            "or `--mac-battery` on a Mac"
        )
    fields = path.read_text().split()
    if len(fields) < 2 or fields[0] != head:
        return "the battery verdict is for another commit; run `cloud_battery.py compare` again"
    if fields[1] != "clean":
        return f"the battery is {fields[1]} on this commit"
    return None


def mac_battery_problem(runner: Runner) -> str | None:
    for cmd in (
        [".venv/bin/ruff", "check", "src", "tests", "scripts"],
        [".venv/bin/python", "-m", "pytest"],
        [".venv/bin/python", "scripts/scan_repo.py"],
    ):
        if runner(cmd).returncode != 0:
            return f"the battery is red: {' '.join(cmd)}"
    return None


def repo_slug(runner: Runner) -> str:
    """owner/name from the origin URL, whatever proxy or scheme it goes through."""
    done = runner(["git", "remote", "get-url", "origin"])
    match = re.search(r"([^/:]+)/([^/]+?)(?:\.git)?/?$", done.stdout.strip())
    if done.returncode != 0 or not match:
        return DEFAULT_REPO
    return f"{match.group(1)}/{match.group(2)}"


def sync_history(runner: Runner) -> None:
    """Refuse a shallow clone, and fetch origin's tags (refs only), before anything is read."""
    if git(runner, "rev-parse", "--is-shallow-repository") == "true":
        raise ReleaseError(
            "this clone is shallow, so the history since the last tag is incomplete; "
            "run `git fetch --unshallow --tags origin` first"
        )
    git(runner, "fetch", "--quiet", "--tags", "origin")


def gather(runner: Runner, repo: str, *, since: str | None = None, tip: str = "HEAD"):
    """The range's start (the last `vX.Y.Z` tag by default), its pull requests and direct merges."""
    for ref in (ref for ref in (since, tip) if ref is not None):
        found = runner(["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"])
        if found.returncode != 0:
            raise ReleaseError(f"{ref!r} names no commit here; fetch it, or name another")
    if since is None:
        since = latest_tag(git(runner, "tag", "--list", "v*").splitlines())
    return since, *landings_since(runner, since, tip, merged_pulls(runner, repo))


def version_at(runner: Runner, ref: str) -> str:
    """The version `pyproject.toml` carried at ``ref``, where a past range starts."""
    found = runner(["git", "show", f"{ref}:{PYPROJECT.as_posix()}"])
    versions = PYPROJECT_VERSION_RE.findall(found.stdout) if found.returncode == 0 else []
    if len(versions) != 1:
        raise ReleaseError(f"no one version line in pyproject.toml at {ref!r}")
    parse_dotted(versions[0])
    return versions[0]


def refuse_a_crossed_tag(runner: Runner, since: str, tip: str) -> str | None:
    """Refuse a reversed range or one holding a version tag other than at its tip.

    Returns the highest version tag at the tip, which titles the notes, or None.
    """
    if runner(["git", "merge-base", "--is-ancestor", since, tip]).returncode != 0:
        raise ReleaseError(f"{since!r} is not behind {tip!r}, so the range holds nothing of it")
    tip_sha = git(runner, "rev-parse", f"{tip}^{{commit}}")
    inside = git(runner, "tag", "--list", "v*", "--merged", tip, "--no-merged", since)
    at_tip = []
    for name in sorted(inside.splitlines(), key=lambda n: parse_tag(n) or (0, 0, 0)):
        if not parse_tag(name):
            continue
        if git(runner, "rev-parse", f"{name}^{{commit}}") != tip_sha:
            raise ReleaseError(
                f"the range crosses {name}; start it there with --since {name}, "
                f"or end it there with --tip {name}"
            )
        at_tip.append(name)
    return at_tip[-1] if at_tip else None


def cmd_plan(args, runner: Runner = run) -> int:
    """List what landed and propose a bump; with ``--notes``, print the release body only.

    A past range's bump is read from the version written at ``--since``.
    """
    asked_since = getattr(args, "since", None)
    tip = getattr(args, "tip", None)
    if tip and not asked_since:
        raise ReleaseError("--tip needs --since, the tag the range starts after")
    tip = tip or "HEAD"
    sync_history(runner)
    repo = args.repo or repo_slug(runner)
    since, prs, direct = gather(runner, repo, since=asked_since, tip=tip)
    tip_tag = None
    if asked_since:
        tip_tag = refuse_a_crossed_tag(runner, asked_since, tip)
        current = version_at(runner, asked_since)
    else:
        current = read_versions(ROOT)[0]
    bump, reasons = propose([*prs, *direct])
    # Below 1.0.0 a break is minor; 1.0.0 is Phillip's to choose.
    capped = bump == "major" and parse_dotted(current)[0] == 0
    if capped:
        bump = "minor"
    nxt = dotted(bumped(parse_dotted(current), bump)) if bump else None
    if getattr(args, "notes", False):
        if bump is None:
            start = since or "the root commit"
            print(f"release: nothing landed after {start}; no notes to print", file=sys.stderr)
            return 1
        tag = tip_tag or f"v{nxt}"
        print(notes(tag, repo, prs, direct), end="")
        return 0
    print(f"current version {current}, last tag {since or 'none (from the root commit)'}")
    if bump is None:
        print("nothing landed since the last tag; no release to cut")
        return 0
    print(f"{len(prs)} pull request(s), {len(direct)} merge(s) without one")
    for line in reasons:
        print(f"  {line}")
    if capped:
        print("  a break below 1.0.0 is proposed as minor; 1.0.0 is Phillip's to choose")
    print(f"proposed bump: {bump}, v{current} to v{nxt}")
    return 0


def cmd_cut(args, runner: Runner = run, root: Path = ROOT) -> int:
    sync_history(runner)
    problems = refusals(runner, root, mac_battery=args.mac_battery)
    if problems:
        print("release: refused")
        for line in problems:
            print(f"  {line}")
        return 1
    repo = args.repo or repo_slug(runner)
    since, prs, direct = gather(runner, repo)
    if not prs and not direct:
        print("release: refused, nothing landed since the last tag")
        return 1
    current = read_versions(root)[0]
    version = dotted(bumped(parse_dotted(current), args.bump))
    tag = f"v{version}"
    if tag in git(runner, "tag", "--list", tag).splitlines():
        print(f"release: refused, {tag} already exists")
        return 1
    body = notes(tag, repo, prs, direct)
    write_version(root, version)
    git(runner, "add", str(PYPROJECT), str(INIT))
    git(runner, "commit", "-m", f"release: {tag}")
    git(runner, "tag", "-a", tag, "-m", f"Cratekit {tag}")
    # One atomic push, so `main` never carries a release commit no tag names.
    git(runner, "push", "--atomic", "origin", "main", tag)
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as handle:
        handle.write(body)
    done = runner(
        [
            "gh", "api", "-X", "POST", f"repos/{repo}/releases",
            "-f", f"tag_name={tag}", "-f", f"name=Cratekit {tag}",
            "-F", f"body=@{handle.name}", "--jq", ".html_url",
        ]
    )
    if done.returncode != 0:
        # The tag is out, so the notes are kept and their publish command printed.
        print(f"release: {tag} is tagged and pushed, but the GitHub release was refused:")
        print(f"  {done.stderr.strip()}")
        print("publish it with:")
        print(
            f"  gh api -X POST repos/{repo}/releases -f tag_name={tag} "
            f"-f 'name=Cratekit {tag}' -F body=@{handle.name}"
        )
        return 1
    Path(handle.name).unlink(missing_ok=True)
    print(f"released {tag}: {done.stdout.strip()}")
    print()
    print(body)
    return 0


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--repo", help="owner/name; read from the origin URL by default")
    sub = parser.add_subparsers(dest="cmd", required=True)
    plan = sub.add_parser("plan", help="list what landed since the last tag and propose a bump")
    since_help = "the tag or commit the range starts after; the last tag by default"
    plan.add_argument("--since", help=since_help)
    tip_help = "the tag or commit the range ends at, with --since; HEAD by default"
    plan.add_argument("--tip", help=tip_help)
    notes_help = "print only the release body for the range, titled by --tip when it is a version"
    plan.add_argument("--notes", action="store_true", help=notes_help)
    cut = sub.add_parser("cut", help="write the version, tag, push and publish the release")
    cut.add_argument("--bump", choices=BUMPS, required=True)
    cut.add_argument(
        "--mac-battery",
        action="store_true",
        help="run the full battery here instead of reading cloud_battery's verdict",
    )
    args = parser.parse_args(argv)
    os.chdir(ROOT)
    try:
        return cmd_plan(args) if args.cmd == "plan" else cmd_cut(args)
    except ReleaseError as exc:
        print(f"release: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
