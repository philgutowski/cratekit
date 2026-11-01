"""U174: the crate-sync skill says what the code it drives says.

The skill is the one command sync an attended session runs: preflight, ``crate
sync land``, the rehearsed landing answered as the session, the rekordbox
visit by its own skill, the account's marks and filing, and one report. It is
text, so nothing breaks when it rots. Every value it spells (the gates it
answers and their options, the JSON fields it branches on, the organize kinds
it runs and the one it must never run, the doctor checks it reads) is a value
some module owns, so each is read here from that module and compared with the
text, and the skill is put through the shipped skills lint, whose rule (g)
parses every ``crate`` line with the real parser.

The step that answers the landing is DRIVEN, not read: the live plan stopped
at its gate, the rehearsal, the same run planned again naming the rehearsal as
equal, and one ``run decide --continue`` as the session landing the rows. That
the re-plan on the stopped run shows the rehearsal is the claim the skill's
step 3 rests on, and nothing else in the suite drives it in that order.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import pytest

from cratekit.cli import build_parser, doctor, registry, sync_land, tail
from cratekit.cli.verbs import runs
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import land_cli
from cratekit.organize import account as account_area
from cratekit.organize import cli as organize_cli
from cratekit.sync import mark_cli
from tests.cli_drive import drive
from tests.test_intake_land_native import _land, _landed_rows, _stage
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414
from tests.test_intake_land_native import silence as silence  # noqa: PLC0414
from tests.test_skills_lint import _real_scripts, lint_skills

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".claude" / "skills" / "crate-sync"
SKILL = SKILL_DIR / "SKILL.md"

_FENCED = re.compile(r"(?:```|~~~)[^\n]*\n(.*?)(?:```|~~~)", re.DOTALL)
_INDENTED = re.compile(r"^ {4,}(\S.*)$", re.M)


@pytest.fixture(scope="module")
def text() -> str:
    return SKILL.read_text()


@pytest.fixture(scope="module")
def flat(text) -> str:
    """The text with every run of white space one space, for phrases a line wraps."""
    return re.sub(r"\s+", " ", text)


def _commands(text: str) -> list[str]:
    """Every line the skill shows as something to run, fenced or indented."""
    lines = [line for block in _FENCED.findall(text) for line in block.splitlines()]
    return [line.strip() for line in lines + _INDENTED.findall(text)]


def _gate(name: str):
    return next(
        gate for entry in registry.ENTRIES for gate in entry.gates if gate.name == name
    )


def test_the_skill_passes_the_shipped_skills_lint(tmp_path):
    """Frontmatter, every crate line parsed by the real parser, no personal literal."""
    shutil.copytree(SKILL_DIR, tmp_path / SKILL_DIR.name)
    assert lint_skills(tmp_path, _real_scripts()) == []


def test_the_lint_reads_the_skills_commands_at_all(text):
    """Anti vacuity: a lint over a skill with no crate line proves nothing."""
    verbs = [line for line in _commands(text) if line.startswith("crate ")]
    for verb in ("job list", "sync land", "intake land", "run decide", "organize --only"):
        assert any(verb in line for line in verbs), verb


def test_it_runs_the_steps_the_brief_names_in_order(flat):
    """Preflight, the pass, the rehearsal and gate, the visit, the account, the report."""
    order = [
        "crate job list --state running",
        "crate --output json sync land",
        "--rehearse",
        "intake.land.native apply --actor session --continue",
        "`rekordbox-visit` skill",
        "organize --only marks",
        "organize --only file",
        "One closing report",
    ]
    places = [flat.index(phrase) for phrase in order]
    assert places == sorted(places), dict(zip(order, places, strict=True))


def test_every_gate_it_answers_is_answered_by_its_own_name_and_option(text):
    decides = [line for line in _commands(text) if line.startswith("crate run decide")]
    # TWO SINCE U184: the backup acknowledgment is minted in one command with no
    # gate (``test_the_acknowledgment_is_minted_in_one_command_as_the_session``).
    assert len(decides) == 2, decides
    for line in decides:
        words = line.split()
        gate, option = words[4], words[5]
        spec = _gate(gate)
        assert option in spec.options and option != "abort", line
        assert "--actor session" in line and "--continue" in line, line
    assert {line.split()[4] for line in decides} == {
        tail.LAND_GATE,
        organize_cli.ACCOUNT_GATE,
    }
    assert tail.LAND_OPTION == "apply" and organize_cli.APPLY == "apply"


def test_the_acknowledgment_is_minted_in_one_command_as_the_session(text):
    """U184. The one command, parsed by the real parser into the session's road."""
    acks = [line for line in _commands(text) if line.startswith("crate session ack")]
    assert acks == ["crate session ack --as session"], acks
    args = build_parser().parse_args(acks[0].split()[1:])
    assert args.as_actor == runs.SESSION_ACTOR


def test_the_actor_it_answers_as_is_the_one_the_decide_verb_reads_as_the_session():
    assert runs.SESSION_ACTOR == tail.SESSION_ACTOR == "session"


def test_continue_is_a_flag_the_decide_verb_takes():
    parser = build_parser()
    args = parser.parse_args(
        ["run", "decide", "R", tail.LAND_GATE, tail.LAND_OPTION, "--actor", "session", "--continue"]
    )
    assert args.continue_run is True


def test_the_stops_it_branches_on_are_the_ones_sync_land_makes(flat):
    assert f"It stopped at `{tail.LAND_GATE}`" in flat
    assert f"It stopped at `{tail.ACK_STOP}`" in flat
    assert "crate session ack --as session" in flat


def test_the_summary_fields_it_reads_are_the_ones_sync_land_writes(flat):
    """Read off the pass's own record, and off the chain's stop, by name."""
    report = sync_land._report(None)
    written = set(report.summary)
    # The stop for a person and the pass's own steps add these as they go.
    source = Path(sync_land.__file__).read_text() + Path(tail.__file__).read_text()
    for name in ("stopped_at", "gate_run", "pass_run", "staging", "land_name",
                 "download_refused", "open_passes"):
        assert f"`data.summary.{name}`" in flat, name
        assert name in written or f'summary["{name}"]' in source, name


def test_the_rehearsal_lines_it_reads_are_the_landings_own(flat):
    """The gate screen's two keys and the phrase that means equal, from the verb."""
    source = Path(land_cli.__file__).read_text()
    assert '"rehearsal": (' in source
    assert '"equal to this plan\'s"' in source or "equal to this plan's" in source
    assert 'facts["differs from the rehearsal"]' in source
    assert "`cause.detail.shown.rehearsal`" in flat
    assert "ends \"equal to this plan's\"" in flat
    assert '`cause.detail.shown["differs from the rehearsal"]`' in flat


def test_the_rehearsal_command_is_the_flag_intake_land_takes():
    parser = build_parser()
    args = parser.parse_args(["intake", "land", "STAGING", "--pass", "PASS", "--rehearse"])
    assert args.rehearse is True


def test_the_organize_kinds_it_runs_exist_and_root_is_never_run(text, flat):
    assert {account_area.MARKS, account_area.FILE} <= set(organize_cli.KINDS)
    runs_of = [line for line in _commands(text) if " organize " in f" {line} " and "decide" not in line]
    kinds = {line.split("--only", 1)[1].split()[0] for line in runs_of}
    assert kinds == {account_area.MARKS, account_area.FILE}
    assert f"**Never `crate organize --only {account_area.ROOT}`**" in flat


def test_the_account_steps_it_reads_are_where_organize_puts_them(flat):
    assert f"`data.summary.areas.{account_area.AREA}.steps`" in flat


def test_the_one_playlist_mark_it_names_is_the_flag_sync_mark_takes(flat):
    parser = build_parser()
    args = parser.parse_args(["sync", "mark", "--pass", "P", "--playlist", "ID"])
    assert args.playlist == ["ID"]
    assert "`crate sync mark --pass PASS --playlist ID`" in flat
    assert mark_cli.ONLY_SAID


def test_the_doctor_checks_it_reads_exist(flat):
    keys = {check.key for check in doctor.CHECKS}
    named = set(re.findall(r"`((?:backup|rekordbox|install)\.[a-z.]+)`", flat))
    assert named == {
        "backup.age.files",
        "backup.age.database",
        "rekordbox.closed",
        "install.release",
    }
    assert named <= keys


def test_the_visit_is_the_visit_skill_and_not_a_copy_of_it(flat):
    """Delegated: none of the visit's own settings or waits is spelled here."""
    assert "Follow the project's `rekordbox-visit` skill step by step" in flat
    visit = REPO_ROOT / ".claude" / "skills" / "rekordbox-visit" / "SKILL.md"
    assert visit.is_file()
    for owned in ("Analysis Mode", "ANLZ0000.DAT", "High precision"):
        assert owned not in flat, owned


def test_it_links_the_shipped_sync_skill_rather_than_repeating_it(flat):
    shipped = "src/cratekit/skills/assets/sync-and-publish/SKILL.md"
    assert f"`{shipped}`" in flat
    assert (REPO_ROOT / shipped).is_file()


def test_every_repository_file_it_cites_exists(flat):
    cited = set(re.findall(r"`((?:docs|src|scripts|tests)/[^`\s]+\.(?:md|py))`", flat))
    assert cited, "the skill cites the plan it carries out"
    for path in sorted(cited):
        assert (REPO_ROOT / path).exists(), path


def test_the_contract_points_an_attended_session_at_it():
    """A procedure nothing names is a procedure nobody follows."""
    assert "`crate-sync` skill" in (REPO_ROOT / "CLAUDE.md").read_text()


def test_questions_wait_for_the_report(flat):
    assert "never stops mid run to ask" in flat
    assert "The questions no rule answers" in flat


# ---------------------------------------------------------------------------
# Step 3, driven: the stopped landing, the rehearsal, the same run re-planned,
# and one decide as the session that lands it
# ---------------------------------------------------------------------------


def test_step_three_re_planned_on_its_stopped_run_names_the_rehearsal_and_lands(
    native_library, silence
):
    cfg, _root = native_library
    _stage(cfg, silence, "One.flac")
    _stage(cfg, silence, "Two.flac")

    # The live plan stops at its gate, as crate sync land leaves it.
    code, stopped = drive(_land())
    assert code == int(ExitCode.DECISION_REQUIRED), stopped
    assert stopped["cause"]["detail"]["gate"] == tail.LAND_GATE
    assert "rehearsal" not in stopped["cause"]["detail"]["shown"]
    gate_run = stopped["run_id"]

    code, rehearsed = drive(_land("--rehearse"))
    assert code == int(ExitCode.OK), rehearsed

    # The same run, planned again, now names the rehearsal and says equal.
    code, again = drive(["--run", gate_run, *_land()])
    assert code == int(ExitCode.DECISION_REQUIRED), again
    assert again["run_id"] == gate_run
    shown = again["cause"]["detail"]["shown"]
    assert shown["rehearsal"].endswith("equal to this plan's"), shown["rehearsal"]
    assert rehearsed["run_id"] in shown["rehearsal"]
    assert _landed_rows(cfg) == []

    code, landed = drive(
        ["run", "decide", gate_run, tail.LAND_GATE, tail.LAND_OPTION,
         "--actor", "session", "--continue"]
    )
    assert code == int(ExitCode.OK), landed
    assert len(_landed_rows(cfg)) == 2
