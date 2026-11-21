"""U173: the rekordbox visit skill says what the code it drives says.

The skill is the procedure an attended session follows for the one step
Cratekit may not do itself: open rekordbox, analyse INBOX / Analyze, wait,
quit, check, clear. It is text, so nothing breaks when it rots. Every value it
spells (the playlist, the mark the second run is for, the process names it
waits on, the gate it answers, the exit codes it branches on, the JSON fields
it reads, the settings it sets) is a value some module owns, and a skill that
spells last month's value sends a session to click the wrong playlist or to
read a verdict backwards. So each one is read here from the module that owns
it and compared with the text, and the skill is put through the shipped
skills lint, whose rule (g) parses every ``crate`` line with the real parser.

The settings table is pinned against the brief as well as against the step
``crate sync land`` prints, because the two are the same standard written
twice and either can move alone.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import pytest

from cratekit.analysis import check_cli
from cratekit.analysis import rekordbox_check as rc
from cratekit.cli import doctor, registry, sync_land
from cratekit.core import analysis_store, cause, processes
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import analyzed_cli, native
from tests.test_skills_lint import _real_scripts, lint_skills

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".claude" / "skills" / "rekordbox-visit"
SKILL = SKILL_DIR / "SKILL.md"

#: Phillip's standard, as the brief gives it (U173, filed 2026-10-27).
STANDARD = {
    "Analysis Mode": "Normal",
    "High precision": "off",
    "BPM / Grid": "on",
    "Phrase": "on",
    "KEY": "on",
    "Vocal": "off",
    "CUE": "off",
}

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


def _settings(text: str) -> dict[str, str]:
    """The field and value table under step 3, read row by row."""
    section = text.split("## 3.", 1)[1].split("\n## ", 1)[0]
    rows = re.findall(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", section, re.M)
    return {field: value for field, value in rows if field != "Field" and not set(field) <= {"-"}}


def _normal(field: str) -> str:
    return re.sub(r"\s+", "", field).lower()


def test_the_skill_passes_the_shipped_skills_lint(tmp_path):
    """Frontmatter, every crate line parsed by the real parser, no personal literal."""
    shutil.copytree(SKILL_DIR, tmp_path / SKILL_DIR.name)
    assert lint_skills(tmp_path, _real_scripts()) == []


def test_the_lint_reads_the_skills_commands_at_all(text):
    """Anti vacuity: a lint over a skill with no crate line proves nothing."""
    verbs = [line for line in _commands(text) if line.startswith("crate ")]
    for verb in ("job list", "analyze check", "inbox analyzed", "run decide"):
        assert any(verb in line for line in verbs), verb


def test_the_settings_are_the_brief_s_standard(text):
    assert _settings(text) == STANDARD


def test_the_settings_agree_with_the_step_crate_sync_land_prints(text):
    """The sync stop's settings clause is the table's, rendered the way it words it.

    Rendered whole rather than read field by field, so a step that turns one
    field the other way (KEY off against a table saying KEY on) fails here
    whichever side moved.
    """
    table = _settings(text)
    assert table["BPM / Grid"] == table["Phrase"] == table["KEY"]
    clause = (
        f"Analysis Mode {table['Analysis Mode']}, high precision "
        f"{table['High precision']}, BPM/Grid, Phrase and KEY {table['KEY']}"
    )
    assert clause in sync_land.REKORDBOX_STEPS[0]


def test_the_mode_list_needs_a_held_press(flat):
    assert "opens only while the mouse is held down on it" in flat
    assert "Press and hold on the control" in flat


def test_it_selects_the_playlist_every_landing_fills(flat):
    assert sync_land.ANALYZE_PLAYLIST == f"INBOX / {native.ANALYZE}"
    assert sync_land.ANALYZE_PLAYLIST in flat
    assert f"`{native.ANALYZE}` directly under it" in flat


def test_the_second_run_is_for_the_mark_the_check_reads(flat):
    assert f"My Tag value named `{rc.DYN_VALUE}`" in flat
    assert f"My Tag `{rc.DYN_VALUE}`" in flat
    assert "**Dynamic**" in flat


def test_it_waits_on_the_processes_the_product_watches(text):
    for name in processes.REKORDBOX_PROCESSES:
        assert f"pgrep -x {name}\n" in text, name


def test_the_doctor_checks_it_reads_exist(flat):
    keys = {check.key for check in doctor.CHECKS}
    named = set(re.findall(r"`((?:backup|rekordbox)\.[a-z.]+)`", flat))
    assert named == {"backup.age.files", "backup.age.database", "rekordbox.closed"}
    assert named <= keys


def test_the_store_it_counts_is_the_analysis_store(flat):
    assert f"`{analysis_store.SHARE_DIRNAME}/PIONEER/USBANLZ` beside the configured database" in flat
    assert "-name ANLZ0000.DAT -newer \"$marker\"" in flat
    assert "marker=$(mktemp -t rekordbox-visit.XXXXXX)" in flat, "BSD and GNU both take this form"


def test_the_background_wait_is_handed_the_marker(text):
    """A background job is its own shell, so its fill in line names all three values."""
    loop = next(block for block in _FENCED.findall(text) + [text] if "while :; do" in block)
    head = loop.split("while :; do", 1)[0].strip().splitlines()[-2]
    for name in ("store=", "expected=", "marker="):
        assert name in head, (name, head)


def test_the_exit_codes_it_branches_on_are_the_check_s(flat):
    """0 done, 12 waiting, 27 suspect, each read off what the verb raises."""
    assert f"**{int(ExitCode.OK)}, {rc.DONE}.**" in flat
    assert f"**{int(ExitCode.PENDING_HUMAN)}, {rc.WAITING}.**" in flat
    assert f"**{int(cause.REASONS['analysis-suspect'])}, {rc.SUSPECT}.**" in flat
    assert f"It must exit {int(ExitCode.PENDING_HUMAN)} with" in flat
    suspect = int(cause.REASONS["analysis-suspect"])
    assert f"or {suspect} with a `data.summary.grids` count above zero" in flat


def test_the_json_fields_it_reads_are_the_check_s(flat):
    """Driven: the payload the verb emits carries every field the skill reads."""
    row = rc.Row(content_id="1", title="t", state=rc.NOT_ANALYSED, dyn=True)
    found = rc.Check(
        scope=rc.Scope(kind=rc.SCOPE_ANALYZE, name=sync_land.ANALYZE_PLAYLIST, content_ids=("1",)),
        rows=(row,),
    )
    summary = check_cli.payload(found)["summary"]
    assert summary["scope"] == rc.SCOPE_ANALYZE
    assert summary["rows"] == 1 and summary["not_analysed"] == 1
    assert summary["items"][0]["dyn"] is True
    assert f"Read `data.summary.scope` first. It must read `{rc.SCOPE_ANALYZE}`" in flat
    assert f"`data.summary.scope` must still read `{rc.SCOPE_ANALYZE}`" in flat, "the post check too"
    assert summary["analysed"] == 0 and summary["grids"][rc.VARIABLE] == 0
    assert f"count above zero under `{rc.VARIABLE}`" in flat
    assert "`data.summary.analysed` plus `data.summary.not_analysed`" in flat
    assert "gone" in summary and "`data.summary.gone`" in flat
    for state in (rc.VARIABLE, rc.ABSENT, rc.MISSING, rc.UNREADABLE):
        assert state in summary["grids"] and f"`{state}`" in flat, state
    for name in ("rows", "not_analysed", "items"):
        assert f"`data.summary.{name}`" in flat, name
    assert "whose `dyn` is true" in flat


def test_the_clear_s_gate_is_answered_by_its_own_name_and_option(text):
    spec = next(
        gate
        for entry in registry.ENTRIES
        for gate in entry.gates
        if gate.name == analyzed_cli.APPROVE_GATE
    )
    decide = [line for line in _commands(text) if line.startswith("crate run decide")]
    assert len(decide) == 1
    words = decide[0].split()
    assert words[-2] == analyzed_cli.APPROVE_GATE
    assert words[-1] in spec.options and words[-1] != "abort"
    assert "--actor session" in decide[0]


def test_every_repository_file_it_cites_exists(flat):
    cited = set(re.findall(r"`((?:docs|src|scripts|tests)/[^`\s]+\.(?:md|py))`", flat))
    assert cited, "the skill cites the learnings it rests on"
    for path in sorted(cited):
        assert (REPO_ROOT / path).exists(), path


def test_the_contract_points_an_attended_session_at_it():
    """A procedure nothing names is a procedure nobody follows."""
    assert "`rekordbox-visit` skill" in (REPO_ROOT / "CLAUDE.md").read_text()


def test_the_acknowledgment_it_mints_is_the_sessions_one_command(flat):
    """U184: minted as the session in one command, a flag the verb takes."""
    from cratekit.cli import build_parser
    from cratekit.core import session as core_session

    named = re.search(r"`crate session ack --as ([a-z]+)`", flat)
    assert named and named.group(1) == core_session.SESSION_ACTOR
    args = build_parser().parse_args(["session", "ack", "--as", named.group(1)])
    assert args.as_actor == core_session.SESSION_ACTOR


# ---------------------------------------------------------------------------
# U319: the Auto Analysis path, first, and the Analyze Tracks path behind it
# ---------------------------------------------------------------------------


def _step(text: str, number: int) -> str:
    """The text of one numbered step, from its heading to the next step's."""
    return text.split(f"\n## {number}.", 1)[1].split("\n## ", 1)[0]


def test_the_auto_analysis_path_comes_before_the_analyze_tracks_path(text):
    """The brief's first path is step 2's first part, and today's path follows it."""
    two = _step(text, 2)
    assert two.startswith(" Open rekordbox: the Auto Analysis path first\n")
    auto, tracks = two.split("\n### The Analyze Tracks path\n", 1)
    assert "Auto Analysis is starting." in re.sub(r"\s+", " ", auto)
    assert "Analyze Track" not in auto.replace("Analyze Tracks path", ""), "no selection on it"
    assert "Command A" in tracks and "Analyze Track)" in tracks
    head = text.split("\n## 1.", 1)[0]
    assert "**Two paths, the short one first** (U319)" in head
    description = next(line for line in text.split("---", 2)[1].splitlines() if line.startswith("description:"))
    assert "Auto Analysis dialog" in description.split("Analyze Tracks", 1)[0]


def test_its_numbered_steps_read_in_order(text):
    """Each part's steps numbered from one with none skipped, so none is missed."""
    auto, tracks = _step(text, 2).split("\n### The Analyze Tracks path\n", 1)
    for part, count in ((auto, 5), (tracks, 3)):
        numbers = [int(n) for n in re.findall(r"^(\d+)\. ", part, re.M)]
        assert numbers == list(range(1, count + 1)), numbers


def test_the_visit_never_changes_the_setting(flat):
    """Auto Analysis is Phillip's: the visit reads it through the dialog and nothing else."""
    assert (
        "It never turns Auto Analysis on or off and never changes a field of "
        "rekordbox's Analysis preference; it reads them only through the dialog below."
    ) in flat
    assert "press Cancel, never OK, and touch no field of the dialog" in flat
    for verb in ("tick Auto Analysis", "turn Auto Analysis on", "untick"):
        assert verb not in flat, verb


def test_the_dialog_is_read_against_the_one_table_with_no_field_left_unread(text, flat):
    """Every field of step 3's table, and a field the dialog does not show stops it."""
    two = _step(text, 2)
    flat_two = re.sub(r"\s+", " ", two)
    assert "read back every field of the table in step 3 from the dialog's screenshot" in flat_two
    assert "A table field the dialog does not show is unread, and unread is not equal." in flat_two
    assert "The Auto Analysis dialog of step 2 is only read against it, never set." in flat
    # The table both paths read is still Phillip's standard, whole.
    assert _settings(text) == STANDARD


def test_ok_only_on_every_field_equal_and_a_waiting_check(flat):
    """A 27 has rows to analyse again, which Auto Analysis leaves alone."""
    waiting = int(ExitCode.PENDING_HUMAN)
    suspect = int(cause.REASONS["analysis-suspect"])
    assert f"**Every field equal, and the check in step 1.5 exited {waiting}**" in flat
    assert f"**Any field differs or is unread**, or the check exited {suspect}: press Cancel" in flat
    assert f"A check that exited {suspect} has rows to analyse again" in flat


def test_no_dialog_and_a_cancel_each_take_the_analyze_tracks_path(flat):
    assert "bring it to the front, and take a screenshot" in flat
    assert "**No dialog on either screenshot**" in flat
    assert "Take the Analyze Tracks path below." in flat
    assert "Zero: Cancel held; take the Analyze Tracks path below." in flat
    assert "then take the Analyze Tracks path below, whose run on the table's fields" in flat
    assert "**A dialog that appears after the Analyze Tracks path has begun** is answered Cancel" in flat


def test_the_auto_analysis_wait_counts_the_rows_not_analysed(flat):
    """Auto Analysis leaves an analysed row alone, so the batch would stall the wait."""
    row = rc.Row(content_id="1", title="t", state=rc.NOT_ANALYSED, dyn=False)
    done = rc.Row(content_id="2", title="u", state=rc.ANALYSED, dyn=False)
    found = rc.Check(
        scope=rc.Scope(kind=rc.SCOPE_ANALYZE, name=sync_land.ANALYZE_PLAYLIST, content_ids=("1", "2")),
        rows=(row, done),
    )
    summary = check_cli.payload(found)["summary"]
    assert summary["not_analysed"] == 1 and summary["analysed"] + summary["not_analysed"] == 2
    assert "with `expected` the `data.summary.not_analysed` count from step 1.5, not the batch" in flat
    assert "On the Auto Analysis path `expected` is `data.summary.not_analysed`" in flat
    assert "the count can pass `expected`; the quiet still ends the wait" in flat


def test_a_cancel_rekordbox_ignores_is_counted_from_before_the_launch(text, flat):
    """The launch marker is written before rekordbox opens, and the count reads it."""
    assert "opened=$(mktemp -t rekordbox-visit.XXXXXX)" in flat
    two = _step(text, 2)
    assert two.index("opened=$(mktemp") < two.index("Open rekordbox through desktop control")
    assert '-name ANLZ0000.DAT -newer "<the path step 2.1 printed>"' in flat
    assert "Wait as step 4 says with `marker` the path step 2.1 printed" in flat


def test_the_dynamic_run_follows_either_path(text):
    five = re.sub(r"\s+", " ", _step(text, 5))
    assert "On the Auto Analysis path nothing is open yet" in five
    assert "**Dynamic**" in five


def test_what_to_record_names_the_path_and_the_dialog(flat):
    assert "which path ran and why (no dialog, a dialog whose fields were equal, or one cancelled" in flat
    assert "whether rekordbox wrote after Cancel" in flat
