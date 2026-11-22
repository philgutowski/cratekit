"""The release script, U159: plan a bump, refuse an unsafe cut, write and publish.

`scripts/release.py` is loaded by path. Every git operation runs against a
throwaway repository with a bare one as its `origin`, and every `gh` call is
answered by a fake runner, so nothing here reaches GitHub.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parent.parent


_SPEC = importlib.util.spec_from_file_location("release_under_test", ROOT / "scripts/release.py")
release = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = release
_SPEC.loader.exec_module(release)


@pytest.mark.parametrize(
    ("title", "kind"),
    [
        ("U158: a unit reaches main through a pull request", "minor"),
        ("merge(u57): the converge verb", "minor"),
        ("merge(u99-b): label registry verbs", "minor"),
        ("R-12: the scan misses a path", "patch"),
        ("merge(r1031): the account mirror's plan", "patch"),
        ("merge(r-4): a repair behind the pull", "patch"),
        ("fix(write): a soft delete defect", "patch"),
        ("feat(config)!: rename the library root key", "major"),
        ("U200: BREAKING the taxonomy schema moves to 5", "major"),
        ("docs: a typo", "patch"),
    ],
)
def test_the_bump_a_title_asks_for(title, kind):
    assert release.classify(title)[0] == kind


def test_the_proposal_is_the_largest_bump_and_versions_are_read_and_bumped():
    bump, reasons = release.propose([
        release.Landing("R-1: a repair", "a" * 40, 1), release.Landing("U2: a verb", "b" * 40, 2),
        release.Landing("merge(r3): another repair", "c" * 40),
    ])
    assert bump == "minor"
    assert len(reasons) == 3
    assert reasons[1].startswith("minor") and "#2 U2: a verb" in reasons[1]
    assert release.propose([]) == (None, [])
    names = ["v0.1.0", "v0.10.0", "v0.9.3", "nightly", "v1.0", "v2.0.0-rc1", "0.11.0"]
    assert release.latest_tag(names) == "v0.10.0"
    assert release.latest_tag(["nightly", "latest"]) is None
    expected = {"patch": (0, 1, 1), "minor": (0, 2, 0), "major": (1, 0, 0)}
    assert {bump: release.bumped((0, 1, 0), bump) for bump in expected} == expected


def _git(cwd: Path, *argv: str) -> str:
    done = subprocess.run(["git", *argv], cwd=cwd, capture_output=True, text=True, check=False)
    assert done.returncode == 0, f"git {argv} failed: {done.stderr}"
    return done.stdout.strip()


def _commit(repo: Path, name: str, message: str) -> str:
    (repo / name).write_text(f"{name}\n")
    _git(repo, "add", name)
    _git(repo, "commit", "-q", "--no-verify", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


def _nff(repo: Path, message: str, ref: str) -> str:
    """Merge ``ref`` into the checked out branch with --no-ff; the merge."""
    _git(repo, "merge", "-q", "--no-ff", "--no-verify", "-m", message, ref)
    return _git(repo, "rev-parse", "HEAD")


def _merge(repo: Path, branch: str, message: str, onto: str = "main") -> tuple[str, str]:
    """A branch with one commit off ``onto``, merged into it with --no-ff: head and merge."""
    _git(repo, "checkout", "-q", onto)
    _git(repo, "checkout", "-q", "-b", branch)
    head = _commit(repo, f"{branch.replace('/', '-')}.txt", f"feat: {branch}")
    _git(repo, "checkout", "-q", onto)
    return head, _nff(repo, message, branch)


def _pr(number: int, title: str, merge: str | None, head: str, merged="x") -> dict:
    pull = dict(number=number, title=title, merged_at=merged, merge_commit_sha=merge)
    return {**pull, "head": {"sha": head}}


def _tag(repo: Path, name: str = "v0.1.0") -> None:
    _git(repo, "tag", "-a", name, "-m", name)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A checkout on main with both version files at 0.1.0 and a bare origin."""
    origin = tmp_path / "origin.git"
    _git(tmp_path, "init", "-q", "--bare", "-b", "main", str(origin))
    work = tmp_path / "work"
    work.mkdir()
    _git(work, "init", "-q", "-b", "main")
    for key, value in (("user.email", "fixture@example.invalid"), ("user.name", "Fixture"),
                       ("commit.gpgsign", "false"), ("tag.gpgsign", "false")):
        _git(work, "config", key, value)
    (work / "src" / "cratekit").mkdir(parents=True)
    (work / "pyproject.toml").write_text(
        '[project]\nname = "cratekit"\nversion = "0.1.0"\n\n[tool.ruff]\ntarget-version = "py312"\n'
    )
    (work / "src" / "cratekit" / "__init__.py").write_text(
        '"""Doc."""\n\n__version__ = "0.1.0"\n\n__all__ = ["__version__"]\n'
    )
    (work / ".gitignore").write_text(".cloud-battery/\n")
    _git(work, "add", ".")
    _git(work, "commit", "-q", "--no-verify", "-m", "chore: seed")
    _git(work, "remote", "add", "origin", str(origin))
    _git(work, "push", "-q", "origin", "main")
    monkeypatch.chdir(work)
    return work


def _verdict(root: Path, line: str = "{head} clean") -> None:
    (root / ".cloud-battery").mkdir(exist_ok=True)
    head = _git(root, "rev-parse", "HEAD")
    (root / ".cloud-battery" / "last-compare.txt").write_text(line.format(head=head) + "\n")


def _fake_gh(pulls=(), *, release_ok=True):
    """The real runner for git, and canned answers for gh, recording each call."""
    calls: list[list[str]] = []

    def runner(argv):
        argv = list(argv)
        if argv[0] != "gh":
            return release.run(argv)
        calls.append(argv)
        if "/pulls?" in argv[2]:
            batch = list(pulls) if argv[2].endswith("&page=1") else []
            return subprocess.CompletedProcess(argv, 0, json.dumps(batch), "")
        assert "/releases" in " ".join(argv), f"unexpected gh call {argv}"
        if not release_ok:
            return subprocess.CompletedProcess(argv, 1, "", "HTTP 403")
        calls[-1].append(Path(argv[argv.index("-F") + 1].removeprefix("body=@")).read_text())
        return subprocess.CompletedProcess(argv, 0, "https://example.invalid/r\n", "")

    return runner, calls


def _gather(pulls=()):
    return release.gather(_fake_gh(pulls)[0], "o/r")


def _cut(repo, bump="minor", **gh):
    runner, calls = _fake_gh(**gh)
    args = SimpleNamespace(bump=bump, mac_battery=False, repo="o/r")
    return release.cmd_cut(args, runner=runner, root=repo), calls


def _published(calls):
    return [c for c in calls if "releases" in " ".join(c)]


def test_the_notes_list_exactly_the_pull_requests_since_the_last_tag(repo):
    old_head, old_merge = _merge(repo, "cloud/1-old", "merge(u1): before the tag")
    _tag(repo)
    _head_a, merge_a = _merge(repo, "cloud/2-a", "merge(u2): through the API")
    head_b, _merge_b = _merge(repo, "cloud/3-b", "merge(u3): merged locally")
    _merge(repo, "unit/u4-c", "merge(u4): no pull request")
    _commit(repo, "residuals.txt", "docs(residuals): number what landed")
    since, prs, direct = _gather([
        _pr(10, "U1: old", old_merge, old_head),
        _pr(11, "U2: a", merge_a, "f" * 40),
        _pr(12, "U3: b", "e" * 40, head_b),
        _pr(13, "U9: closed unmerged", "d" * 40, "d" * 40, merged=None),
    ])
    assert since == "v0.1.0"
    # Merged after the tag, through the API or by a local merge; nothing before it or unmerged.
    assert [p.number for p in prs] == [11, 12]
    assert [d.title for d in direct] == ["merge(u4): no pull request"]
    body = release.notes("v0.2.0", "o/r", prs, direct)
    assert "- #11 U2: a" in body and "- #12 U3: b" in body
    assert "#10" not in body and "#13" not in body
    assert 'pipx install --force "cratekit @ git+https://github.com/o/r@v0.2.0"' in body


def _behind(repo: Path) -> None:
    other, config = repo.parent / "other", ["-c", "user.email=f@example.invalid"]
    _git(repo.parent, "clone", "-q", *config, "-c", "user.name=F", "origin.git", str(other))
    _commit(other, "ahead.txt", "feat: someone else")
    _git(other, "push", "-q", "origin", "main")
    _git(repo, "fetch", "-q", "origin")


@pytest.mark.parametrize(
    ("setup", "verdict", "words"),
    [
        (lambda repo: _git(repo, "checkout", "-q", "-b", "cloud/9-x"), "{head} clean", "not main"),
        (lambda repo: (repo / "stray.txt").write_text("stray\n"), "{head} clean", "not clean"),
        (_behind, "{head} clean", "origin/main"),
        (lambda repo: _commit(repo, "local.txt", "feat: unpushed"), "{head} clean", "origin/main"),
        (None, "{head} red", "battery is red"),
        (None, "{head} dirty", "battery is dirty"),
        (None, None, "no battery verdict"),
        (None, f"{'a' * 40} clean", "another commit"),
    ],
)
def test_cut_refuses_an_unsafe_checkout(repo, setup, verdict, words):
    if setup:
        setup(repo)
    if verdict:
        _verdict(repo, verdict)
    problems = release.refusals(release.run, repo, mac_battery=False)
    assert any(words in p for p in problems), problems


def test_a_clean_main_is_not_refused_and_the_mac_battery_refuses_on_any_red_command(repo):
    _verdict(repo)
    assert release.refusals(release.run, repo, mac_battery=False) == []

    def runner(argv):
        argv = list(argv)
        if argv[0] == "git":
            return release.run(argv)
        return subprocess.CompletedProcess(argv, 1 if "pytest" in argv else 0, "", "")

    problems = release.refusals(runner, repo, mac_battery=True)
    assert any("battery is red" in p and "pytest" in p for p in problems)


def test_cut_writes_commits_tags_pushes_and_publishes(repo, tmp_path):
    _tag(repo)
    _git(repo, "push", "-q", "origin", "v0.1.0")
    _head, merge = _merge(repo, "cloud/2-a", "merge(u2): a verb")
    _git(repo, "push", "-q", "origin", "main")
    _verdict(repo)
    code, calls = _cut(repo, pulls=[_pr(7, "U2: a verb", merge, "f" * 40)])
    assert code == 0
    assert release.read_versions(repo) == ("0.2.0", "0.2.0")
    assert _git(repo, "log", "-1", "--format=%s") == "release: v0.2.0"
    origin = tmp_path / "origin.git"
    assert _git(origin, "rev-parse", "main") == _git(repo, "rev-parse", "HEAD")
    assert _git(origin, "cat-file", "-t", "v0.2.0") == "tag", "the tag must be annotated"
    published = [c for c in calls if "repos/o/r/releases" in c]
    assert len(published) == 1
    assert "tag_name=v0.2.0" in published[0]
    assert "- #7 U2: a verb" in published[0][-1]
    assert 'target-version = "py312"' in (repo / "pyproject.toml").read_text()
    (repo / "src" / "cratekit" / "__init__.py").write_text('"""Doc."""\n')
    with pytest.raises(release.ReleaseError, match="exactly one version line"):
        release.read_versions(repo)


def test_cut_refuses_before_writing_anything_on_a_refusal_or_with_nothing_landed(repo):
    _merge(repo, "cloud/2-a", "merge(u2): a verb")
    assert _cut(repo) == (1, [])
    assert release.read_versions(repo) == ("0.1.0", "0.1.0")
    _tag(repo)
    _git(repo, "push", "-q", "origin", "main")
    _verdict(repo)
    code, calls = _cut(repo, "patch")
    assert code == 1 and not _published(calls)
    assert release.read_versions(repo) == ("0.1.0", "0.1.0")


def test_a_refused_release_says_the_tag_is_pushed_and_prints_the_publish_command(repo, capsys):
    _merge(repo, "cloud/2-a", "merge(u2): a verb")
    _git(repo, "push", "-q", "origin", "main")
    _verdict(repo)
    assert _cut(repo, release_ok=False)[0] == 1
    out = capsys.readouterr().out
    assert "tagged and pushed" in out
    line = next(x for x in out.splitlines() if "gh api -X POST repos/o/r/releases" in x)
    notes_file = Path(line.rsplit("body=@", 1)[1])
    assert "merge(u2): a verb" in notes_file.read_text()
    notes_file.unlink()


@pytest.mark.parametrize("url", [
    "https://github.com/philgutowski/cratekit.git", "ssh://github.com/philgutowski/cratekit.git",
    "http://proxy@127.0.0.1:1234/git/philgutowski/cratekit",
])
def test_the_repository_is_read_off_the_origin_url(url):
    def runner(argv):
        return subprocess.CompletedProcess(list(argv), 0, url + "\n", "")

    assert release.repo_slug(runner) == "philgutowski/cratekit"


def test_a_shallow_clone_is_refused_and_a_tag_only_origin_carries_starts_the_range(
    repo, tmp_path, monkeypatch
):
    _merge(repo, "cloud/1-old", "merge(u1): shipped in v0.1.0")
    _tag(repo)
    _git(repo, "push", "-q", "origin", "main", "v0.1.0")
    _merge(repo, "cloud/2-new", "merge(u2): after the tag")
    _git(repo, "push", "-q", "origin", "main")
    shallow = tmp_path / "shallow"
    _git(tmp_path, "clone", "-q", "--depth", "1", f"file://{tmp_path / 'origin.git'}", str(shallow))
    monkeypatch.chdir(shallow)
    with pytest.raises(release.ReleaseError, match="shallow"):
        release.sync_history(release.run)
    with pytest.raises(release.ReleaseError, match="shallow"):
        _cut(shallow)
    assert release.read_versions(shallow) == ("0.1.0", "0.1.0")
    fresh = tmp_path / "fresh"
    _git(tmp_path, "clone", "-q", "--no-tags", str(tmp_path / "origin.git"), str(fresh))
    monkeypatch.chdir(fresh)
    runner, _calls = _fake_gh()
    release.sync_history(runner)
    since, _prs, direct = release.gather(runner, "o/r")
    assert since == "v0.1.0", "a clone without tags planned from the root commit"
    assert [d.title for d in direct] == ["merge(u2): after the tag"]


def test_a_refused_tag_push_leaves_main_without_the_release_commit(repo, tmp_path):
    hook = tmp_path / "origin.git" / "hooks" / "pre-receive"
    hook.write_text(
        "#!/bin/sh\nwhile read old new ref; do\n"
        '  case "$ref" in refs/tags/*) echo refused >&2; exit 1;; esac\ndone\n'
    )
    hook.chmod(0o755)
    _merge(repo, "cloud/2-a", "merge(u2): a verb")
    _git(repo, "push", "-q", "origin", "main")
    before = _git(tmp_path / "origin.git", "rev-parse", "main")
    _verdict(repo)
    runner, calls = _fake_gh()
    with pytest.raises(release.ReleaseError):
        release.cmd_cut(SimpleNamespace(bump="minor", mac_battery=False, repo="o/r"),
                        runner=runner, root=repo)
    assert _git(tmp_path / "origin.git", "rev-parse", "main") == before, "an untagged release"
    assert not _published(calls)


def _pull_upstream(repo: Path, message: str = "Merge branch 'main' of https://github.com/o/r"):
    """A local commit on main, then main merged with `upstream`, playing `origin/main` (U215)."""
    _git(repo, "checkout", "-q", "main")
    _commit(repo, "sitting.txt", "docs(cutover): a sitting recorded on the Mac")
    return _nff(repo, message, "upstream")


def _upstream(repo: Path) -> None:
    _tag(repo)
    _git(repo, "branch", "upstream", "main")


def _titles(landings) -> list[str]:
    return [landing.title for landing in landings]


def test_unit_and_residual_merges_behind_a_local_merge_of_main_are_all_listed(repo):
    _upstream(repo)
    _merge(repo, "cloud/2-a", "merge(u2): the first behind the pull", "upstream")
    _merge(repo, "cloud/3-b", "merge(u3): the second behind the pull", "upstream")
    _merge(repo, "cloud/4-r", "merge(r-4): a repair behind the pull", "upstream")
    _pull_upstream(repo)
    _merge(repo, "cloud/5-r", "merge(r-5): a repair on the first parent line")
    since, prs, direct = _gather()
    assert (since, prs) == ("v0.1.0", [])
    assert _titles(direct) == [
        "merge(u2): the first behind the pull",
        "merge(u3): the second behind the pull",
        "merge(r-4): a repair behind the pull",
        "merge(r-5): a repair on the first parent line",
    ], "a landing on the second parent side of a local merge of main went unlisted"
    assert release.propose(direct)[0] == "minor"


@pytest.mark.parametrize(
    "subject",
    [
        "Merge branch 'main' of https://github.com/philgutowski/cratekit",
        "Merge branch 'main' of github.com:philgutowski/cratekit",
        "Merge remote-tracking branch 'origin/main'",
        "Merge origin/main",
    ],
)
def test_a_local_merge_of_main_is_never_a_landing(repo, subject):
    _upstream(repo)
    _commit(repo, "upstream-only.txt", "docs: nothing merged upstream")
    _git(repo, "checkout", "-q", "upstream")
    _commit(repo, "upstream.txt", "docs(residuals): number what landed")
    _pull_upstream(repo, subject)
    _since, prs, direct = _gather()
    assert prs == [] and direct == [], f"{subject!r} was read as a landing"


def test_a_unit_reachable_through_its_head_and_its_merge_is_listed_once(repo):
    _upstream(repo)
    head_a, merge_a = _merge(repo, "cloud/2-a", "merge(u2): merged locally", "upstream")
    # Another branch took U2's head before U2 landed, under a sync subject.
    _git(repo, "checkout", "-q", "-b", "cloud/3-b", "upstream~1")
    _commit(repo, "b.txt", "feat: b")
    _nff(repo, "Merge remote-tracking branch 'origin/cloud/2-a' into cloud/3-b", head_a)
    _git(repo, "checkout", "-q", "upstream")
    _nff(repo, "merge(u3): after U2", "cloud/3-b")
    _pull_upstream(repo)
    # GitHub's merge commit for a pull request merged by a local push is not
    # always the commit on main; the head is what finds it.
    _since, prs, direct = _gather([_pr(31, "U2: a", "e" * 40, head_a)])
    # It lands at the branch sync that took its head, and is listed once; no sync is listed.
    assert [(p.number, p.sha) for p in prs] == [(31, merge_a)]
    assert _titles(direct) == ["merge(u3): after U2"]


def test_a_range_with_no_local_merge_lists_what_the_first_parent_line_lists(repo):
    _tag(repo)
    head_a, merge_a = _merge(repo, "cloud/2-a", "merge(u2): through the API")
    # A branch that catches up with main, then lands without a pull request.
    _git(repo, "checkout", "-q", "-b", "unit/u3-b", "main~1")
    _commit(repo, "b.txt", "feat: b")
    _nff(repo, "merge: main into the U3 branch", "main")
    _git(repo, "checkout", "-q", "main")
    _nff(repo, "Merge relay task 3 from relay/3", "unit/u3-b")
    _merge(repo, "cloud/4-c", "feat(config)!: a break")
    _commit(repo, "residuals.txt", "docs(residuals): number what landed")
    _since, prs, direct = _gather([_pr(41, "U2: a", merge_a, head_a)])
    log = _git(repo, "log", "--first-parent", "--merges", "--reverse", "--format=%H %s",
               "v0.1.0..HEAD")
    first_parent = [x.split(" ", 1)[1] for x in log.splitlines() if not x.startswith(merge_a)]
    assert [p.number for p in prs] == [41]
    assert _titles(direct) == first_parent
    assert first_parent == ["Merge relay task 3 from relay/3", "feat(config)!: a break"]


def test_a_unit_shipped_in_the_last_tag_is_not_listed_again_through_a_sibling_sync(repo):
    # cloud/3-b took cloud/2-a's final head before either landed; U2 shipped
    # in v0.2.0, and U3 lands after it carrying that sync.
    _git(repo, "checkout", "-q", "-b", "cloud/2-a")
    head_a = _commit(repo, "a.txt", "feat: a")
    _git(repo, "checkout", "-q", "-b", "cloud/3-b", "main")
    _commit(repo, "b.txt", "feat: b")
    _nff(repo, "Merge remote-tracking branch 'origin/cloud/2-a' into cloud/3-b", head_a)
    _git(repo, "checkout", "-q", "main")
    merge_a = _nff(repo, "merge(u2): a", "cloud/2-a")
    _tag(repo, "v0.2.0")
    merge_b = _nff(repo, "merge(u3): b", "cloud/3-b")
    pulls = [_pr(2, "U2: a", merge_a, head_a), _pr(3, "R-3: b", merge_b, "f" * 40)]
    since, prs, direct = _gather(pulls)
    assert since == "v0.2.0"
    assert [p.number for p in prs] == [3], "a unit the last tag shipped was listed again"
    assert direct == []
    assert release.propose([*prs, *direct])[0] == "patch"


@pytest.mark.parametrize(
    "local_subject",
    [
        None,  # merged through the API only, off the first parent line
        # A local session had merged the same branch the cloud merged through the API.
        "merge(u2): merged locally",
        # GitHub's default subject, which is no landing subject but is on the line.
        "Merge pull request #2 from o/cloud/2-a",
    ],
)
def test_a_pull_request_merged_through_the_api_behind_a_local_merge_is_listed_once(
    repo, local_subject
):
    _upstream(repo)
    head_a, merge_api = _merge(repo, "cloud/2-a", "merge(u2): through the API", "upstream")
    if local_subject:
        _git(repo, "checkout", "-q", "main")
        _nff(repo, local_subject, head_a)
    _pull_upstream(repo)
    _since, prs, direct = _gather([_pr(2, "U2: a", merge_api, head_a)])
    assert [(p.number, p.sha) for p in prs] == [(2, merge_api)]
    assert direct == [], "a listed pull request's merge was listed again"


def test_a_pull_request_fast_forwarded_onto_main_lands_at_its_head(repo):
    _tag(repo)
    _git(repo, "checkout", "-q", "-b", "cloud/2-a")
    head_a = _commit(repo, "a.txt", "feat: a")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "-q", "--ff-only", "cloud/2-a")
    _since, prs, direct = _gather([_pr(2, "U2: a", "e" * 40, head_a)])
    assert [(p.number, p.sha) for p in prs] == [(2, head_a)]
    assert direct == []


def _plan(repo, monkeypatch, **flags):
    monkeypatch.setattr(release, "ROOT", repo)
    args = SimpleNamespace(**{"repo": "o/r", "since": None, "tip": None, "notes": False, **flags})
    return release.cmd_plan(args, runner=_fake_gh()[0])


def _set_version(repo: Path, version: str) -> None:
    for path, key in ((repo / "pyproject.toml", "version"),
                      (repo / "src" / "cratekit" / "__init__.py", "__version__")):
        rows = path.read_text().splitlines()
        path.write_text("\n".join(
            f'{key} = "{version}"' if row.startswith(f"{key} = ") else row for row in rows
        ) + "\n")
    _git(repo, "commit", "-q", "--no-verify", "-am", f"release: v{version}")
    _tag(repo, f"v{version}")


def test_plan_from_the_root_commit_caps_a_break_below_1_0_0(repo, capsys, monkeypatch):
    _merge(repo, "cloud/2-a", "feat(config)!: rename a key")
    assert _plan(repo, monkeypatch) == 0
    out = capsys.readouterr().out
    assert out.startswith("current version 0.1.0, last tag none (from the root commit)\n")
    assert "0 pull request(s), 1 merge(s) without one" in out
    assert "major  feat(config)!: rename a key (" in out
    assert "proposed bump: minor, v0.1.0 to v0.2.0" in out
    assert "Phillip's to choose" in out


def test_plan_reruns_a_past_range_and_prints_its_notes(repo, capsys, monkeypatch):
    _upstream(repo)
    _merge(repo, "cloud/2-a", "merge(u2): behind the pull", "upstream")
    _pull_upstream(repo)
    _merge(repo, "cloud/3-b", "merge(u3): on the line")
    _tag(repo, "v0.2.0")
    _merge(repo, "cloud/4-c", "merge(u4): after the range")
    _tag(repo, "v0.3.0")
    assert _plan(repo, monkeypatch, since="v0.1.0", tip="v0.2.0") == 0
    out = capsys.readouterr().out
    assert "merge(u2): behind the pull" in out and "merge(u3): on the line" in out
    assert "merge(u4)" not in out
    assert "proposed bump: minor, v0.1.0 to v0.2.0" in out, "the bump was not read from --since"
    assert _plan(repo, monkeypatch, since="v0.1.0", tip="v0.2.0", notes=True) == 0
    body = capsys.readouterr().out
    assert body.startswith("Cratekit v0.2.0.\n")
    assert "- merge(u2): behind the pull (" in body and "- merge(u3): on the line (" in body
    assert "merge(u4)" not in body and "proposed bump" not in body
    assert "cratekit @ git+https://github.com/o/r@v0.2.0" in body


def test_plan_reads_the_bump_from_the_version_the_range_starts_at(repo, capsys, monkeypatch):
    _set_version(repo, "0.2.0")
    _merge(repo, "cloud/3-r", "merge(r-3): a repair")
    _set_version(repo, "0.2.1")
    _merge(repo, "cloud/4-a", "merge(u4): a unit")
    _set_version(repo, "0.3.0")
    # The checkout reads 0.3.0; the range v0.2.0..v0.2.1 started at 0.2.0.
    assert _plan(repo, monkeypatch, since="v0.2.0", tip="v0.2.1") == 0
    out = capsys.readouterr().out
    assert "current version 0.2.0" in out
    assert "proposed bump: patch, v0.2.0 to v0.2.1" in out
    assert "merge(u4)" not in out
    # A range ending at a version tag is titled by that tag however the tip is
    # spelled: a repair alone proposes v0.3.1, and the release cut was v0.4.0.
    _merge(repo, "cloud/5-r", "merge(r-5): a repair")
    _set_version(repo, "0.4.0")
    _git(repo, "branch", "at-v0.4.0", "v0.4.0")
    for tip in ("v0.4.0", "at-v0.4.0"):
        assert _plan(repo, monkeypatch, since="v0.3.0", tip=tip, notes=True) == 0
        body = capsys.readouterr().out
        assert body.startswith("Cratekit v0.4.0.\n"), f"--tip {tip} titled the notes {body[:20]!r}"
        assert "@v0.4.0" in body and "v0.3.1" not in body


def test_plan_refuses_what_it_cannot_plan_or_print(repo, capsys, monkeypatch):
    _set_version(repo, "0.2.0")
    _merge(repo, "cloud/3-a", "merge(u3): in v0.3.0")
    _set_version(repo, "0.3.0")
    assert _plan(repo, monkeypatch, notes=True) == 1, "notes over an empty range"
    captured = capsys.readouterr()
    assert captured.out == "" and "nothing landed" in captured.err
    _merge(repo, "cloud/4-b", "merge(u4): after v0.3.0")
    with pytest.raises(release.ReleaseError, match="--tip needs --since"):
        _plan(repo, monkeypatch, tip="HEAD")
    with pytest.raises(release.ReleaseError, match="names no commit"):
        _plan(repo, monkeypatch, since="v9.9.9")
    with pytest.raises(release.ReleaseError, match="crosses v0.3.0"):
        _plan(repo, monkeypatch, since="v0.2.0", tip="HEAD", notes=True)
    assert capsys.readouterr().out == "", "notes were printed over a range two releases wide"
    with pytest.raises(release.ReleaseError, match="is not behind"):
        _plan(repo, monkeypatch, since="v0.3.0", tip="v0.2.0")
