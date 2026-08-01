"""R1: nothing that ships names a person, a machine, a path, a volume, or an account.

The source system had a guard for this. It ran in CI as a single grep and it had
three holes, all of which are closed here and each of which is proved closed by a
fixture test below:

* it looked only at package Python, so tests, docs, shipped skills, shell
  scripts, templates, and workflow files were invisible to it;
* it excluded by filename SUBSTRING, so any future file whose path happened to
  contain the excluded fragment inherited the exemption silently;
* its literal set was two hardcoded strings, so a second volume, a second
  account, or the same volume named without its path prefix all passed.

Two live violations sit in the source repository right now, both in the widened
coverage area: a shipped skill instructing the reader to work in the author's
home directory, and another naming the author's volume by bare name. Neither is
visible to the old guard. Both are caught by this one.

The scan is also a SECRET scan over every tracked path, vendored trees included,
because the vendored artifact in the source system sits in the same directory as
a live OAuth session cache, a credentials env file, and a service token. The same
machinery answers the same question about a different literal: does this tracked
file contain something that belongs to one person rather than to the project.

A NOTE ON THE FIXTURES BELOW. Every bad literal in this file is ASSEMBLED FROM
FRAGMENTS at runtime rather than written out. That is not decoration. If a test
for the portability guard contained a real hardcoded home directory, the guard
would flag its own test file, and the usual fix for that is an exemption, and an
exemption is the hole this rewrite exists to close. Assembling the strings keeps
the file genuinely clean, so no exemption is needed anywhere.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_scanner():
    """Load ``scripts/scan_repo.py`` by path.

    It lives in ``scripts/`` rather than in the package because it also runs as a
    pre-commit hook and as a standalone CI step, where importing the package
    would be a circular requirement: the scan has to pass before an install is
    trustworthy. Loading it by path keeps it out of the package namespace while
    still letting the tests drive its pure checkers directly.
    """
    spec = importlib.util.spec_from_file_location(
        "cratekit_scan_repo", REPO_ROOT / "scripts" / "scan_repo.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scan = _load_scanner()


# ---------------------------------------------------------------------------
# Assembled bad literals. See the module docstring for why these are built
# rather than written.
# ---------------------------------------------------------------------------

_A_HOME = "/" + "Users" + "/" + "jdoe" + "/Documents/project"
_A_VOLUME = "/" + "Volumes" + "/" + "BigAudioDrive" + "/Music"
_A_LINUX_HOME = "/" + "home" + "/" + "jdoe" + "/.config"
_AN_EMAIL = "jane.doe" + "@" + "somecompany" + ".com"


def _violations(text: str) -> list[str]:
    """Shape patterns only. The runtime-derived identity tier is off so these
    assertions mean the same thing on every machine."""
    return scan.portability_violations(text, identity_tokens=set())


# ── the literal set: shapes, not two fixed strings ───────────────────────────


def test_any_home_directory_is_caught_not_just_one():
    """The old guard knew one home directory. This one knows the shape.

    Both platforms are asserted because a contributor on Linux writing their own
    path is the same failure as the author writing theirs.
    """
    assert _violations(_A_HOME), "a macOS home directory must be a violation"
    assert _violations(_A_LINUX_HOME), "a Linux home directory must be a violation"


def test_any_volume_is_caught_not_just_one():
    problems = _violations(_A_VOLUME)
    assert problems and "volume path" in problems[0]


def test_account_identifier_is_caught():
    problems = _violations(f"contact {_AN_EMAIL} for access")
    assert problems and "account identifier" in problems[0]


def test_placeholder_paths_are_allowed():
    """Documentation must still be able to show the SHAPE of a path.

    A guard that forbids writing a path at all pushes docs into vagueness, and
    vague install docs are how a friend ends up guessing. The rule is that a path
    must not be one particular person's path.
    """
    for good in (
        "/Users/<your-username>/Music",
        "/Users/{user}/Music",
        "/Volumes/<library-volume>/Music",
        "/home/$USER/.config/cratekit",
        "/Volumes/{library_volume}/Music/Processed",
    ):
        assert _violations(good) == [], f"placeholder path wrongly flagged: {good}"


def test_illustrative_email_domains_are_allowed():
    assert _violations("mail contributors@example.com") == []


def test_runtime_derived_identity_catches_a_bare_name():
    """The tier that closes the "same volume, no path prefix" hole.

    A volume named WITHOUT its mount prefix is invisible to any path-shaped
    pattern. That is the exact shape of one of the two live violations in the
    source repository: a shipped skill says the volume "must be mounted" and
    names it, with no leading path. Deriving identifiers from the running machine
    is what catches that, and it does so without this file, or the scanner,
    naming anybody.
    """
    problems = scan.portability_violations(
        "the SomeSpecificDrive volume must be mounted",
        identity_tokens={"SomeSpecificDrive"},
    )
    assert problems and "personal identifier" in problems[0]

    # Substring hits do not count. A guard that fires on fragments gets muted.
    assert (
        scan.portability_violations(
            "SomeSpecificDriveExtended", identity_tokens={"SomeSpecificDrive"}
        )
        == []
    )


def test_identity_can_be_declared_rather_than_only_detected(tmp_path):
    """The detected tier alone would make the guard depend on what is plugged in.

    Reading mounted volume names catches a bare drive name only while the drive
    is connected. Unplug it and the same document passes, which is a guard that
    works by coincidence. The declared file makes it deterministic, and it is
    gitignored because it is the one file that names a specific person's things.
    """
    (tmp_path / scan.IDENTITY_FILE).write_text(
        "# a comment\nMyBigAudioDrive\n\n  my-laptop  # trailing comment\n"
    )
    declared = scan.identity_file_tokens(tmp_path)
    assert declared == {"MyBigAudioDrive", "my-laptop"}
    assert scan.machine_identity_tokens(tmp_path) >= declared


def test_declared_identity_is_gitignored():
    """If it were committed it would be the leak it exists to prevent."""
    ignored = (REPO_ROOT / ".gitignore").read_text()
    assert scan.IDENTITY_FILE in ignored
    assert (REPO_ROOT / f"{scan.IDENTITY_FILE}.example").exists(), (
        "the format must be documented, or nobody will use the mechanism"
    )


# ── coverage: tests, docs, and skills, not just package source ───────────────


def _tree_with_planted(tmp_path: Path, relative: str, body: str) -> Path:
    target = tmp_path / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body)
    return tmp_path


@pytest.mark.parametrize(
    "relative, body",
    [
        # The three blind spots the source guard had, one case each.
        ("tests/test_something.py", f'PATH = "{_A_HOME}"\n'),
        ("docs/install.md", f"Put the library at {_A_VOLUME}\n"),
        ("skills/crate-sync/SKILL.md", f"Work in {_A_HOME} when running this.\n"),
        # Non-Python files were invisible too.
        ("scripts/backup.sh", f'VOLUME={_A_VOLUME}\n'),
        (".github/workflows/other.yml", f"    run: ls {_A_HOME}\n"),
        ("src/cratekit/core/config.py", f'ROOT = "{_A_VOLUME}"\n'),
    ],
)
def test_guard_covers_every_shipped_surface(tmp_path, relative, body):
    """The planted literal is found wherever it is planted.

    Parametrized rather than written six times because the point being made is
    that the LOCATION does not matter, and six near-identical test bodies would
    obscure that.
    """
    root = _tree_with_planted(tmp_path, relative, body)
    findings = scan.scan_tree(root, check_identity=False)
    assert any(f.startswith(f"{relative}:") for f in findings), (
        f"a planted literal in {relative} was not caught; findings were {findings}"
    )


def test_exclusions_are_exact_paths_not_substrings():
    """The exemption mechanism cannot be inherited by accident.

    The source guard excluded with ``grep -v "DJ_common/config.py"``, which
    exempts every path CONTAINING that text. Here the exclusion set holds exact
    repo-relative paths, so a new file can only be exempt if somebody exempted
    that exact file.
    """
    assert isinstance(scan.ALLOWED_EXACT, frozenset)
    for entry in scan.ALLOWED_EXACT:
        assert not entry.startswith("*") and "*" not in entry, (
            f"{entry!r} is a glob; exclusions must be exact repo-relative paths"
        )


# ── the secret scan ──────────────────────────────────────────────────────────

_A_TOKEN = "a" + "B3xQ" + "7zK9" + "mN2pR4tV6wY8" + "cE1gJ5"


@pytest.mark.parametrize(
    "body, label",
    [
        (f'{{"access_token": "{_A_TOKEN}"}}', "OAuth token field"),
        (f'{{"refresh_token": "{_A_TOKEN}"}}', "OAuth token field"),
        (f"Authorization: Bearer {_A_TOKEN}{_A_TOKEN}", "bearer token"),
        ("AKIA" + "ABCDEFGHIJKLMNOP", "AWS access key id"),
        ("ghp_" + "abcdefghij0123456789klmn", "GitHub token"),
        ("xox" + "b-" + "1234567890-abcdefg", "Slack token"),
        (f'api_key = "{_A_TOKEN}"', "credential assignment"),
        ("-----BEGIN RSA PRIVATE" + " KEY-----", "private key block"),
    ],
)
def test_credential_shapes_are_caught(body, label):
    problems = scan.secret_violations(body)
    assert any(p.startswith(label) for p in problems), (
        f"{label} not caught in {body!r}; got {problems}"
    )


@pytest.mark.parametrize(
    "key",
    [
        "client_secret", "clientSecret", "client-secret", "CLIENTSECRET",
        "client_id", "clientId",
        "access_token", "accessToken",
        "refresh_token", "refreshToken",
        "api_key", "apiKey", "apikey",
    ],
)
def test_a_credential_key_is_caught_in_every_casing_and_separator(key):
    """Naming conventions are not a security boundary.

    This is not a hypothetical hardening pass. A real vendored source file held
    five live third-party credential pairs written as ``"clientSecret"``, and
    this scan walked straight past every one of them while catching the
    snake_case spelling in a neighbouring file. Two separate causes, both fixed
    here and both asserted by this test:

    1. The keyword list was written in one casing, so a camelCase key matched
       nothing.
    2. The rule that should have caught it anyway, on the bare word ``secret``,
       required whitespace between the keyword and the colon. In a JSON-shaped
       literal a closing quote sits there instead, and that is the form almost
       every credential in a real file takes.

    Parametrized over spellings rather than asserted once, because the failure
    was specifically that one spelling was covered and the others were not.
    """
    body = f'{{"{key}": "{_A_TOKEN}"}}'
    assert scan.secret_violations(body), f"{key!r} carrying a live value was not caught"


@pytest.mark.parametrize(
    "body",
    [
        '{"clientSecret": "YOUR_CLIENT_SECRET_HERE"}',
        '{"clientId": "abc"}',
        "The client id is supplied during setup and stored in the keychain.",
        '{"apiKey": "EXAMPLE_VALUE_GOES_HERE"}',
    ],
)
def test_the_widened_credential_rules_stay_quiet_on_correct_content(body):
    """A guard that fires on correct code gets suppressed, and then it guards nothing.

    Widening a pattern is the moment false positives arrive, so the quiet cases
    are asserted alongside the loud ones: a documented placeholder, a value too
    short to be a credential, ordinary prose naming the concept, and an
    illustrative example.
    """
    assert scan.secret_violations(body) == [], f"wrongly flagged: {body!r}"


def test_findings_never_print_the_secret():
    """A guard that echoes what it found has copied it into the CI log.

    The finding must carry enough to locate the line and not enough to use it.
    """
    body = f'{{"access_token": "{_A_TOKEN}"}}'
    problems = scan.secret_violations(body)
    assert problems
    assert _A_TOKEN not in problems[0], "the scanner leaked the credential it found"
    assert "elided" in problems[0]


def test_documented_placeholder_credentials_are_allowed():
    for good in (
        'access_token = "<your-token-here>"',
        'api_key = "YOUR_API_KEY_HERE"',
        'password = "xxxxxxxxxxxxxxxx"',
        'client_secret = "${CRATEKIT_CLIENT_SECRET}"',
    ):
        assert scan.secret_violations(good) == [], f"placeholder wrongly flagged: {good}"


@pytest.mark.parametrize(
    "name",
    [
        "vendor/tidal_session.json",
        "vendor/.env",
        "src/cratekit/secrets.env",
        "docs/credentials.json",
        "keys/id_rsa",
        "certs/client.pem",
        "vendor/web_token",
    ],
)
def test_a_credential_filename_is_a_violation_whatever_is_inside(name):
    """The content scan cannot see inside an archive. A name is always visible.

    This rule exists for a concrete adjacency: in the source system the artifact
    that gets vendored sits in the same directory as a live OAuth session cache,
    a credentials env file, and a service token. Vendoring that directory
    wholesale is the mistake this catches, and it catches it even if the payload
    is compressed.
    """
    assert scan.credential_filename_violations(name)


def test_template_credential_files_are_allowed():
    """Shipping ``secrets.env.example`` is how a user learns what to fill in."""
    assert scan.credential_filename_violations("docs/secrets.env.example") == []
    assert scan.credential_filename_violations("vendor/example.env") == []


def test_the_scan_reaches_vendored_trees(tmp_path):
    """``vendor/`` is not exempt. It is the highest-risk directory in the tree.

    A vendored dependency is code somebody else wrote, copied wholesale, and
    reviewed less carefully than authored code. Bounding the scan to package
    source is what would let a credential ride in with it.
    """
    (tmp_path / "vendor" / "downloader").mkdir(parents=True)
    (tmp_path / "vendor" / "downloader" / "cfg.json").write_text(
        f'{{"refresh_token": "{_A_TOKEN}"}}\n'
    )
    findings = scan.scan_tree(tmp_path, check_identity=False)
    assert any("vendor/downloader/cfg.json" in f for f in findings)


# ── the real tree ────────────────────────────────────────────────────────────


def test_the_repository_itself_is_clean():
    """The whole point. Everything above proves the guard bites; this runs it.

    Identity checking is ON here, so on a contributor's own machine this also
    catches their account name, their hostname, and the names of their mounted
    volumes, none of which this repository has any business containing.
    """
    findings = scan.scan_tree(REPO_ROOT)
    assert not findings, "repository scan violations:\n" + "\n".join(findings)


# ── a symlink has no content, so every content rule skips it ─────────────────


def test_a_symlink_to_an_absolute_path_is_caught(tmp_path):
    """The hole this closes, in the exact shape that got through.

    Every other rule here reads a file's CONTENT. A symlink has none: following
    one to a directory raises, the reader returns None, and the entry is skipped
    before any rule sees it. A ``.venv`` symlink pointing at an absolute home
    directory was committed on a tree where this scan exited 0.
    """
    link = tmp_path / "dot-venv"
    link.symlink_to("/Users/someone/elsewhere/.venv")

    findings = scan.scan_tree(tmp_path, [link], check_identity=False)

    assert findings, "an absolute symlink target was not caught"
    assert "absolute path" in findings[0]


def test_a_symlink_escaping_the_repository_is_caught(tmp_path):
    """A relative target that leaves the tree resolves to whatever sits beside it."""
    link = tmp_path / "outward"
    link.symlink_to("../not-in-the-clone")

    findings = scan.scan_tree(tmp_path, [link], check_identity=False)

    assert findings, "a symlink escaping the tree was not caught"
    assert "escaping the repository" in findings[0]


def test_a_relative_symlink_inside_the_repository_is_allowed(tmp_path):
    """P7. A guard that fires on correct code is one people route around.

    A relative link within the tree is portable and common. It must stay quiet.
    """
    (tmp_path / "real.txt").write_text("fine\n", encoding="utf-8")
    link = tmp_path / "alias.txt"
    link.symlink_to("real.txt")

    assert scan.scan_tree(tmp_path, [link], check_identity=False) == []


def test_the_scanner_does_not_resolve_away_the_link_it_is_asked_about(tmp_path):
    """``resolve()`` follows a symlink and hands the checkers the TARGET.

    That disarms the rule precisely where it matters, because pre-commit passes
    filenames, so the explicit-path branch is the one the hook uses. Pinned here
    because the first version of this rule had exactly that defect and reported
    clean against a planted link.
    """
    import subprocess
    import sys

    (tmp_path / "real.txt").write_text("fine\n", encoding="utf-8")
    link = tmp_path / "dot-venv"
    link.symlink_to("/Users/someone/elsewhere/.venv")

    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "scan_repo.py"), str(link)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "absolute path" in result.stderr
