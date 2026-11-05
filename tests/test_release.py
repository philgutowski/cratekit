"""The release script, U159: plan a bump, refuse an unsafe cut, write and publish.

`scripts/release.py` is loaded by path, as `board.py` is, because a script is
not part of the package. Every git operation runs against a throwaway
repository with a bare one as its `origin`, and every `gh` call is answered by
a fake runner, so nothing here reaches GitHub.
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


def _release():
    path = ROOT / "scripts" / "release.py"
    spec = importlib.util.spec_from_file_location("release_under_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


release = _release()


# --------------------------------------------------------------------------
# versions and the bump


@pytest.mark.parametrize(
    ("title", "kind"),
    [
        ("U158: a unit reaches main through a pull request", "minor"),
        ("merge(u57): the converge verb", "minor"),
        ("merge(u99-b): label registry verbs", "minor"),
        ("R-12: the scan misses a path", "patch"),
        ("merge(r1031): the account mirror's plan", "patch"),
        ("fix(write): a soft delete defect", "patch"),
        ("feat(config)!: rename the library root key", "major"),
        ("U200: BREAKING the taxonomy schema moves to 5", "major"),
        ("docs: a typo", "patch"),
    ],
)
def test_the_bump_a_title_asks_for(title, kind):
    assert release.classify(title)[0] == kind


def test_the_proposal_is_the_largest_bump_with_a_reason_per_landing():
    landings = [
        release.Landing(title="R-1: a repair", sha="a" * 40, number=1),
        release.Landing(title="U2: a verb", sha="b" * 40, number=2),
        release.Landing(title="merge(r3): another repair", sha="c" * 40),
    ]
    bump, reasons = release.propose(landings)
    assert bump == "minor"
    assert len(reasons) == 3
    assert reasons[1].startswith("minor") and "#2 U2: a verb" in reasons[1]


def test_nothing_landed_proposes_nothing():
    assert release.propose([]) == (None, [])


def test_tags_that_are_not_versions_are_ignored():
    names = ["v0.1.0", "v0.10.0", "v0.9.3", "nightly", "v1.0", "v2.0.0-rc1", "0.11.0"]
    assert release.latest_tag(names) == "v0.10.0"
    assert release.latest_tag(["nightly", "latest"]) is None


@pytest.mark.parametrize(
    ("bump", "expected"),
    [("patch", (0, 1, 1)), ("minor", (0, 2, 0)), ("major", (1, 0, 0))],
)
def test_each_bump(bump, expected):
    assert release.bumped((0, 1, 0), bump) == expected


# --------------------------------------------------------------------------
# a repository to release from


def _git(cwd: Path, *argv: str) -> str:
    done = subprocess.run(["git", *argv], cwd=cwd, capture_output=True, text=True, check=False)
    assert done.returncode == 0, f"git {argv} failed: {done.stderr}"
    return done.stdout.strip()


def _commit(repo: Path, name: str, message: str) -> str:
    (repo / name).write_text(f"{name}\n")
    _git(repo, "add", name)
    _git(repo, "commit", "-q", "--no-verify", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


def _merge(repo: Path, branch: str, message: str) -> tuple[str, str]:
    """A branch with one commit merged with --no-ff: the head and the merge."""
    _git(repo, "checkout", "-q", "-b", branch)
    head = _commit(repo, f"{branch.replace('/', '-')}.txt", f"feat: {branch}")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "-q", "--no-ff", "--no-verify", "-m", message, branch)
    return head, _git(repo, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A checkout on main with both version files at 0.1.0 and a bare origin."""
    origin = tmp_path / "origin.git"
    _git(tmp_path, "init", "-q", "--bare", "-b", "main", str(origin))
    work = tmp_path / "work"
    work.mkdir()
    _git(work, "init", "-q", "-b", "main")
    _git(work, "config", "user.email", "fixture@example.invalid")
    _git(work, "config", "user.name", "Fixture")
    _git(work, "config", "commit.gpgsign", "false")
    _git(work, "config", "tag.gpgsign", "false")
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


def _clean_verdict(root: Path) -> None:
    (root / ".cloud-battery").mkdir(exist_ok=True)
    (root / ".cloud-battery" / "last-compare.txt").write_text(
        f"{_git(root, 'rev-parse', 'HEAD')} clean\n"
    )


def _fake_gh(pulls=(), *, release_ok=True):
    """The real runner for git, and canned answers for gh, recording each call."""
    calls: list[list[str]] = []

    def runner(argv):
        argv = list(argv)
        if argv[0] != "gh":
            return release.run(argv)
        calls.append(argv)
        if "/pulls?" in argv[2]:
            page = int(argv[2].rsplit("page=", 1)[1])
            batch = list(pulls) if page == 1 else []
            return subprocess.CompletedProcess(argv, 0, json.dumps(batch), "")
        if "/releases" in " ".join(argv):
            if not release_ok:
                return subprocess.CompletedProcess(argv, 1, "", "HTTP 403")
            body = Path(argv[argv.index("-F") + 1].removeprefix("body=@")).read_text()
            calls[-1].append(body)
            return subprocess.CompletedProcess(argv, 0, "https://example.invalid/r\n", "")
        raise AssertionError(f"unexpected gh call {argv}")

    return runner, calls


# --------------------------------------------------------------------------
# what landed since the last tag


def test_the_notes_list_exactly_the_pull_requests_since_the_last_tag(repo):
    _old_head, old_merge = _merge(repo, "cloud/1-old", "merge(u1): before the tag")
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    _head_a, merge_a = _merge(repo, "cloud/2-a", "merge(u2): through the API")
    head_b, _merge_b = _merge(repo, "cloud/3-b", "merge(u3): merged locally")
    _head_c, _merge_c = _merge(repo, "unit/u4-c", "merge(u4): no pull request")
    _commit(repo, "residuals.txt", "docs(residuals): number what landed")
    pulls = [
        {"number": 10, "title": "U1: old", "merged_at": "x", "merge_commit_sha": old_merge,
         "head": {"sha": _old_head}},
        {"number": 11, "title": "U2: a", "merged_at": "x", "merge_commit_sha": merge_a,
         "head": {"sha": "f" * 40}},
        {"number": 12, "title": "U3: b", "merged_at": "x", "merge_commit_sha": "e" * 40,
         "head": {"sha": head_b}},
        {"number": 13, "title": "U9: closed unmerged", "merged_at": None,
         "merge_commit_sha": "d" * 40, "head": {"sha": "d" * 40}},
    ]
    runner, _calls = _fake_gh(pulls)
    since, prs, direct = release.gather(runner, "o/r")
    assert since == "v0.1.0"
    assert [p.number for p in prs] == [11, 12], (
        "the notes must list the pull requests merged after the tag, merged "
        "through the API or by a local merge, and nothing before it or unmerged"
    )
    assert [d.title for d in direct] == ["merge(u4): no pull request"]
    body = release.notes("v0.2.0", "o/r", prs, direct)
    assert "- #11 U2: a" in body and "- #12 U3: b" in body
    assert "#10" not in body and "#13" not in body
    assert 'pipx install --force "cratekit @ git+https://github.com/o/r@v0.2.0"' in body


def test_with_no_tag_the_range_starts_at_the_root_commit(repo):
    _merge(repo, "cloud/2-a", "merge(u2): the first")
    runner, _calls = _fake_gh()
    since, prs, direct = release.gather(runner, "o/r")
    assert since is None
    assert prs == []
    assert [d.title for d in direct] == ["merge(u2): the first"]


# --------------------------------------------------------------------------
# the refusals


def test_a_clean_current_main_with_a_clean_verdict_is_not_refused(repo):
    _clean_verdict(repo)
    assert release.refusals(release.run, repo, mac_battery=False) == []


def test_cut_refuses_off_main(repo):
    _git(repo, "checkout", "-q", "-b", "cloud/9-x")
    _clean_verdict(repo)
    problems = release.refusals(release.run, repo, mac_battery=False)
    assert any("not main" in p for p in problems)


def test_cut_refuses_on_a_dirty_tree(repo):
    _clean_verdict(repo)
    (repo / "stray.txt").write_text("stray\n")
    problems = release.refusals(release.run, repo, mac_battery=False)
    assert any("not clean" in p for p in problems)


def test_cut_refuses_behind_origin_main(repo, tmp_path):
    other = tmp_path / "other"
    _git(tmp_path, "clone", "-q", str(tmp_path / "origin.git"), str(other))
    _git(other, "config", "user.email", "fixture@example.invalid")
    _git(other, "config", "user.name", "Fixture")
    _commit(other, "ahead.txt", "feat: someone else")
    _git(other, "push", "-q", "origin", "main")
    _git(repo, "fetch", "-q", "origin")
    _clean_verdict(repo)
    problems = release.refusals(release.run, repo, mac_battery=False)
    assert any("origin/main" in p for p in problems)


def test_cut_refuses_ahead_of_origin_main(repo):
    _commit(repo, "local.txt", "feat: not pushed")
    _clean_verdict(repo)
    problems = release.refusals(release.run, repo, mac_battery=False)
    assert any("origin/main" in p for p in problems)


@pytest.mark.parametrize("verdict", ["red", "dirty"])
def test_cut_refuses_on_a_red_battery(repo, verdict):
    (repo / ".cloud-battery").mkdir()
    (repo / ".cloud-battery" / "last-compare.txt").write_text(
        f"{_git(repo, 'rev-parse', 'HEAD')} {verdict}\n"
    )
    problems = release.refusals(release.run, repo, mac_battery=False)
    assert any(f"battery is {verdict}" in p for p in problems)


def test_cut_refuses_without_a_verdict_or_with_another_commit_s(repo):
    problems = release.refusals(release.run, repo, mac_battery=False)
    assert any("no battery verdict" in p for p in problems)
    (repo / ".cloud-battery").mkdir()
    (repo / ".cloud-battery" / "last-compare.txt").write_text(f"{'a' * 40} clean\n")
    problems = release.refusals(release.run, repo, mac_battery=False)
    assert any("another commit" in p for p in problems)


def test_the_mac_battery_refuses_on_any_red_command(repo):
    def runner(argv):
        argv = list(argv)
        if argv[0] == "git":
            return release.run(argv)
        code = 1 if "pytest" in argv else 0
        return subprocess.CompletedProcess(argv, code, "", "")

    problems = release.refusals(runner, repo, mac_battery=True)
    assert any("battery is red" in p and "pytest" in p for p in problems)


# --------------------------------------------------------------------------
# the cut


def test_the_version_is_written_to_both_files_and_read_back_equal(repo):
    release.write_version(repo, "0.2.0")
    assert release.read_versions(repo) == ("0.2.0", "0.2.0")
    assert 'target-version = "py312"' in (repo / "pyproject.toml").read_text()


def test_a_missing_version_line_is_refused(repo):
    (repo / "src" / "cratekit" / "__init__.py").write_text('"""Doc."""\n')
    with pytest.raises(release.ReleaseError):
        release.read_versions(repo)


def test_cut_writes_commits_tags_pushes_and_publishes(repo, tmp_path):
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    _git(repo, "push", "-q", "origin", "v0.1.0")
    _head, merge = _merge(repo, "cloud/2-a", "merge(u2): a verb")
    _git(repo, "push", "-q", "origin", "main")
    _clean_verdict(repo)
    pulls = [{"number": 7, "title": "U2: a verb", "merged_at": "x",
              "merge_commit_sha": merge, "head": {"sha": "f" * 40}}]
    runner, calls = _fake_gh(pulls)
    args = SimpleNamespace(bump="minor", mac_battery=False, repo="o/r")
    assert release.cmd_cut(args, runner=runner, root=repo) == 0
    assert release.read_versions(repo) == ("0.2.0", "0.2.0")
    assert _git(repo, "log", "-1", "--format=%s") == "release: v0.2.0"
    origin = tmp_path / "origin.git"
    assert _git(origin, "rev-parse", "main") == _git(repo, "rev-parse", "HEAD")
    assert _git(origin, "cat-file", "-t", "v0.2.0") == "tag", "the tag must be annotated"
    published = [c for c in calls if "repos/o/r/releases" in c]
    assert len(published) == 1
    assert "tag_name=v0.2.0" in published[0]
    assert "- #7 U2: a verb" in published[0][-1]


def test_cut_refuses_when_nothing_landed(repo):
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    _clean_verdict(repo)
    runner, calls = _fake_gh()
    args = SimpleNamespace(bump="patch", mac_battery=False, repo="o/r")
    assert release.cmd_cut(args, runner=runner, root=repo) == 1
    assert release.read_versions(repo) == ("0.1.0", "0.1.0")
    assert not [c for c in calls if "releases" in " ".join(c)]


def test_a_refused_release_says_the_tag_is_already_pushed(repo, capsys):
    _merge(repo, "cloud/2-a", "merge(u2): a verb")
    _git(repo, "push", "-q", "origin", "main")
    _clean_verdict(repo)
    runner, _calls = _fake_gh(release_ok=False)
    args = SimpleNamespace(bump="minor", mac_battery=False, repo="o/r")
    assert release.cmd_cut(args, runner=runner, root=repo) == 1
    assert "tagged and pushed" in capsys.readouterr().out


def test_cut_refuses_before_writing_anything_on_a_refusal(repo):
    _merge(repo, "cloud/2-a", "merge(u2): a verb")
    runner, calls = _fake_gh()
    args = SimpleNamespace(bump="minor", mac_battery=False, repo="o/r")
    assert release.cmd_cut(args, runner=runner, root=repo) == 1
    assert release.read_versions(repo) == ("0.1.0", "0.1.0")
    assert calls == []


@pytest.mark.parametrize(
    ("url", "slug"),
    [
        ("https://github.com/philgutowski/cratekit.git", "philgutowski/cratekit"),
        ("ssh://github.com/philgutowski/cratekit.git", "philgutowski/cratekit"),
        ("http://proxy@127.0.0.1:1234/git/philgutowski/cratekit", "philgutowski/cratekit"),
    ],
)
def test_the_repository_is_read_off_the_origin_url(url, slug):
    def runner(argv):
        return subprocess.CompletedProcess(list(argv), 0, url + "\n", "")

    assert release.repo_slug(runner) == slug


# --------------------------------------------------------------------------
# the review's round: a shallow clone, origin's tags, the atomic push


def test_a_shallow_clone_is_refused_before_anything_is_read(repo, tmp_path, monkeypatch):
    for n in range(3):
        _commit(repo, f"c{n}.txt", f"feat: {n}")
    _git(repo, "push", "-q", "origin", "main")
    shallow = tmp_path / "shallow"
    _git(tmp_path, "clone", "-q", "--depth", "1", f"file://{tmp_path / 'origin.git'}", str(shallow))
    monkeypatch.chdir(shallow)
    with pytest.raises(release.ReleaseError, match="shallow"):
        release.sync_history(release.run)
    args = SimpleNamespace(bump="minor", mac_battery=False, repo="o/r")
    with pytest.raises(release.ReleaseError, match="shallow"):
        release.cmd_cut(args, runner=_fake_gh()[0], root=shallow)
    assert release.read_versions(shallow) == ("0.1.0", "0.1.0")


def test_a_tag_only_origin_carries_is_where_the_range_starts(repo, tmp_path, monkeypatch):
    _merge(repo, "cloud/1-old", "merge(u1): shipped in v0.1.0")
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    _git(repo, "push", "-q", "origin", "main", "v0.1.0")
    _merge(repo, "cloud/2-new", "merge(u2): after the tag")
    _git(repo, "push", "-q", "origin", "main")
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
    _clean_verdict(repo)
    runner, calls = _fake_gh()
    args = SimpleNamespace(bump="minor", mac_battery=False, repo="o/r")
    with pytest.raises(release.ReleaseError):
        release.cmd_cut(args, runner=runner, root=repo)
    assert _git(tmp_path / "origin.git", "rev-parse", "main") == before, (
        "main carries a release commit that no tag names"
    )
    assert not [c for c in calls if "releases" in " ".join(c)]


def test_a_refused_release_prints_the_command_that_publishes_the_kept_notes(repo, capsys):
    _merge(repo, "cloud/2-a", "merge(u2): a verb")
    _git(repo, "push", "-q", "origin", "main")
    _clean_verdict(repo)
    runner, _calls = _fake_gh(release_ok=False)
    args = SimpleNamespace(bump="minor", mac_battery=False, repo="o/r")
    assert release.cmd_cut(args, runner=runner, root=repo) == 1
    out = capsys.readouterr().out
    line = next(x for x in out.splitlines() if "gh api -X POST repos/o/r/releases" in x)
    notes_file = Path(line.rsplit("body=@", 1)[1])
    assert "merge(u2): a verb" in notes_file.read_text()
    notes_file.unlink()


def test_plan_caps_a_break_below_1_0_0_at_minor(repo, capsys, monkeypatch):
    _merge(repo, "cloud/2-a", "feat(config)!: rename a key")
    monkeypatch.setattr(release, "ROOT", repo)
    runner, _calls = _fake_gh()
    assert release.cmd_plan(SimpleNamespace(repo="o/r"), runner=runner) == 0
    out = capsys.readouterr().out
    assert "proposed bump: minor, v0.1.0 to v0.2.0" in out
    assert "Phillip's to choose" in out


# --------------------------------------------------------------------------
# a local merge of main, U215
#
# A local session commits on `main` and then pulls, so each landing pushed to
# `origin/main` meanwhile sits on the second parent side of a merge of `main`
# into the local `main`. Here the branch `upstream` plays `origin/main`.


def _merge_into(repo: Path, target: str, branch: str, message: str) -> tuple[str, str]:
    """A branch with one commit off ``target``, merged into it with --no-ff."""
    _git(repo, "checkout", "-q", target)
    _git(repo, "checkout", "-q", "-b", branch)
    head = _commit(repo, f"{branch.replace('/', '-')}.txt", f"feat: {branch}")
    _git(repo, "checkout", "-q", target)
    _git(repo, "merge", "-q", "--no-ff", "--no-verify", "-m", message, branch)
    return head, _git(repo, "rev-parse", "HEAD")


def _pull_upstream(repo: Path, message: str = "Merge branch 'main' of https://github.com/o/r"):
    """A local commit on main, then main merged with what landed upstream."""
    _git(repo, "checkout", "-q", "main")
    _commit(repo, "sitting.txt", "docs(cutover): a sitting recorded on the Mac")
    _git(repo, "merge", "-q", "--no-ff", "--no-verify", "-m", message, "upstream")
    return _git(repo, "rev-parse", "HEAD")


def _tag_and_branch_upstream(repo: Path) -> None:
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    _git(repo, "branch", "upstream", "main")


def test_two_unit_merges_behind_a_local_merge_of_main_are_both_listed(repo):
    _tag_and_branch_upstream(repo)
    _merge_into(repo, "upstream", "cloud/2-a", "merge(u2): the first behind the pull")
    _merge_into(repo, "upstream", "cloud/3-b", "merge(u3): the second behind the pull")
    _pull_upstream(repo)
    since, prs, direct = release.gather(_fake_gh()[0], "o/r")
    assert since == "v0.1.0"
    assert prs == []
    assert [d.title for d in direct] == [
        "merge(u2): the first behind the pull",
        "merge(u3): the second behind the pull",
    ], "a unit merge on the second parent side of a local merge of main went unlisted"


def test_a_pull_request_merged_through_the_api_off_the_first_parent_line_is_listed(repo):
    _tag_and_branch_upstream(repo)
    head_a, merge_a = _merge_into(repo, "upstream", "cloud/2-a", "merge(u2): through the API")
    head_b, merge_b = _merge_into(repo, "upstream", "cloud/3-b", "merge(u3): also the API")
    _pull_upstream(repo)
    pulls = [
        {"number": 21, "title": "U2: a", "merged_at": "x", "merge_commit_sha": merge_a,
         "head": {"sha": head_a}},
        {"number": 22, "title": "U3: b", "merged_at": "x", "merge_commit_sha": merge_b,
         "head": {"sha": head_b}},
    ]
    _since, prs, direct = release.gather(_fake_gh(pulls)[0], "o/r")
    assert [p.number for p in prs] == [21, 22]
    assert [p.sha for p in prs] == [merge_a, merge_b]
    assert direct == [], "a pull request's own merge commit was listed a second time"


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
    _tag_and_branch_upstream(repo)
    _commit(repo, "upstream-only.txt", "docs: nothing merged upstream")
    _git(repo, "checkout", "-q", "upstream")
    _commit(repo, "upstream.txt", "docs(residuals): number what landed")
    _pull_upstream(repo, subject)
    _since, prs, direct = release.gather(_fake_gh()[0], "o/r")
    assert prs == [] and direct == [], f"{subject!r} was read as a landing"


def test_a_unit_reachable_through_its_head_and_its_merge_is_listed_once(repo):
    _tag_and_branch_upstream(repo)
    head_a, merge_a = _merge_into(repo, "upstream", "cloud/2-a", "merge(u2): merged locally")
    # Another branch took U2's head before U2 landed, under a sync subject.
    _git(repo, "checkout", "-q", "upstream")
    _git(repo, "checkout", "-q", "-b", "cloud/3-b", "upstream~1")
    _commit(repo, "b.txt", "feat: b")
    _git(repo, "merge", "-q", "--no-ff", "--no-verify", "-m",
         "Merge remote-tracking branch 'origin/cloud/2-a' into cloud/3-b", head_a)
    _git(repo, "checkout", "-q", "upstream")
    _git(repo, "merge", "-q", "--no-ff", "--no-verify", "-m", "merge(u3): after U2", "cloud/3-b")
    _pull_upstream(repo)
    pulls = [
        # GitHub's merge commit for a pull request merged by a local push is
        # not always the commit on main; the head is what finds it.
        {"number": 31, "title": "U2: a", "merged_at": "x", "merge_commit_sha": "e" * 40,
         "head": {"sha": head_a}},
    ]
    _since, prs, direct = release.gather(_fake_gh(pulls)[0], "o/r")
    assert [(p.number, p.sha) for p in prs] == [(31, merge_a)], (
        "the pull request landed at the branch sync that took its head, not at its own merge"
    )
    assert [d.title for d in direct] == ["merge(u3): after U2"], (
        "a unit reachable through its head and its merge was listed twice, or a sync was listed"
    )


def test_a_range_with_no_local_merge_lists_what_the_first_parent_line_lists(repo):
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    head_a, merge_a = _merge_into(repo, "main", "cloud/2-a", "merge(u2): through the API")
    # A branch that catches up with main, then lands without a pull request.
    _git(repo, "checkout", "-q", "-b", "unit/u3-b", "main~1")
    _commit(repo, "b.txt", "feat: b")
    _git(repo, "merge", "-q", "--no-ff", "--no-verify", "-m", "merge: main into the U3 branch", "main")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "-q", "--no-ff", "--no-verify", "-m", "Merge relay task 3 from relay/3",
         "unit/u3-b")
    _merge_into(repo, "main", "cloud/4-c", "feat(config)!: a break")
    _commit(repo, "residuals.txt", "docs(residuals): number what landed")
    pulls = [{"number": 41, "title": "U2: a", "merged_at": "x", "merge_commit_sha": merge_a,
              "head": {"sha": head_a}}]
    _since, prs, direct = release.gather(_fake_gh(pulls)[0], "o/r")
    first_parent_merges = [
        line.split(" ", 1)[1]
        for line in _git(repo, "log", "--first-parent", "--merges", "--reverse",
                         "--format=%H %s", "v0.1.0..HEAD").splitlines()
        if not line.startswith(merge_a)
    ]
    assert [p.number for p in prs] == [41]
    assert [d.title for d in direct] == first_parent_merges == [
        "Merge relay task 3 from relay/3",
        "feat(config)!: a break",
    ]


def test_the_bump_over_a_minor_unit_behind_a_local_merge_is_minor(repo):
    _tag_and_branch_upstream(repo)
    _merge_into(repo, "upstream", "cloud/2-a", "merge(u2): the only unit")
    _pull_upstream(repo)
    _merge_into(repo, "main", "cloud/3-r", "merge(r-3): a repair on the first parent line")
    _since, prs, direct = release.gather(_fake_gh()[0], "o/r")
    assert release.propose([*prs, *direct])[0] == "minor"


def _plan(repo, monkeypatch, **flags):
    monkeypatch.setattr(release, "ROOT", repo)
    args = SimpleNamespace(repo="o/r", since=None, tip=None, notes=False)
    for key, value in flags.items():
        setattr(args, key, value)
    return release.cmd_plan(args, runner=_fake_gh()[0])


def test_plan_reruns_a_past_range_and_prints_its_notes(repo, capsys, monkeypatch):
    _tag_and_branch_upstream(repo)
    _merge_into(repo, "upstream", "cloud/2-a", "merge(u2): behind the pull")
    _pull_upstream(repo)
    _merge_into(repo, "main", "cloud/3-b", "merge(u3): on the line")
    _git(repo, "tag", "-a", "v0.2.0", "-m", "v0.2.0")
    _merge_into(repo, "main", "cloud/4-c", "merge(u4): after the range")
    _git(repo, "tag", "-a", "v0.3.0", "-m", "v0.3.0")
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


def test_plan_refuses_a_tip_without_a_start_and_a_ref_that_names_nothing(repo, monkeypatch):
    _merge_into(repo, "main", "cloud/2-a", "merge(u2): a verb")
    with pytest.raises(release.ReleaseError, match="--tip needs --since"):
        _plan(repo, monkeypatch, tip="HEAD")
    with pytest.raises(release.ReleaseError, match="names no commit"):
        _plan(repo, monkeypatch, since="v9.9.9")


def test_plan_notes_over_an_empty_range_print_nothing_and_fail(repo, capsys, monkeypatch):
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    assert _plan(repo, monkeypatch, notes=True) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "nothing landed" in captured.err
