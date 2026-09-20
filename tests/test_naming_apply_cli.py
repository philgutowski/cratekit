"""U39: ``name.apply`` carries an existing head through instead of destroying it.

WHY THIS FILE EXISTS. The conformance suite drives every verb over an EMPTY
library, so ``name.apply``'s loop body shipped in U37 without a single driven
rename. Driving it on 2026-08-24 showed the shipped verb renaming
``01A - 124 - Cola.flac`` to ``Cola.flac``: the spec was built from the title
tag and the initialkey tag with no tempo, the default head is all or nothing,
so the head rendered empty and the pass destroyed the convention it exists to
apply. Every test here drives the real dispatcher over real audio files.

THE TEMPO IS TEXT. The recovered head values come from the head parser over
the filename and the title, which is string parsing over names the library
already holds. Nothing here reads or writes any analysis surface, and the
tempo lands in the filename and the title convention only, never in a tag
field, which ``core.tags.FIELDS`` having no tempo key guarantees structurally.
"""

from __future__ import annotations

import io
import json
import unicodedata
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.core import config, locations, naming, rb_writer, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.write import naming_cli
from cratekit.write.naming_cli import _template
from tests._containers import synth_container
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION, _build_disposable_database, _row


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def configured(library, monkeypatch):
    """A machine set up far enough that the verb reaches its own logic.

    The collection is stubbed as READ AND EMPTY, which is a real state and not a
    missing database: these tests are about the rename, and the collection guard
    is driven against a disposable database further down.
    """
    resolved = config.from_dict(valid_data(library))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    monkeypatch.setattr(naming_cli, "_recorded", lambda cfg: ())
    return resolved


def drive(argv: list[str]) -> tuple[int, str, str]:
    """Run the real dispatcher and return (status, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def _track(
    folder: Path, name: str, *, title: str | None = None, key: str | None = None
) -> Path:
    """A real audio file under ``folder`` with the given name and tags."""
    made = synth_container(folder, ".flac")
    target = folder / name
    made.rename(target)
    fields: dict[str, object] = {}
    if title is not None:
        fields["title"] = title
    if key is not None:
        fields["initialkey"] = key
    if fields:
        tags.write_tags(target, fields)
    return target


def _folder(cfg) -> Path:
    folder = Path(cfg.library.root) / "Music" / "wave"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _drive(folder: Path, option: str) -> dict:
    code, out, _ = drive([
        "--output", "json", "-d", f"name.apply.confirm={option}",
        "name", "apply", "--root", str(folder),
    ])
    assert code == int(ExitCode.OK), out
    return json.loads(out)["data"]


def _plan(folder: Path) -> dict:
    """Read the plan without touching anything, through the abort option."""
    return _drive(folder, "abort")


def _apply(folder: Path) -> dict:
    return _drive(folder, "apply")


def _answer(folder: Path) -> tuple[int, dict]:
    """Status and whole envelope from one apply, whatever it exits with.

    ``_apply`` asserts a zero exit, which is right for a sweep that carried out
    every rename it promised. R-172's whole content is that an apply which could
    not is a non-success answer carrying its plan, so these tests read both
    halves rather than the payload alone.
    """
    code, out, _ = drive([
        "--output", "json", "-d", "name.apply.confirm=apply",
        "name", "apply", "--root", str(folder),
    ])
    return code, json.loads(out)


def _moves(plan: dict) -> list[tuple[str, str]]:
    return [(item["from"], item["to"]) for item in plan["items"]]


def _actions(plan: dict) -> dict[str, str]:
    return {item["from"]: item["action"] for item in plan["items"]}


def test_a_folder_already_in_convention_proposes_no_rename(configured):
    """The pass is idempotent over the convention it establishes."""
    folder = _folder(configured)
    _track(folder, "01A - 124 - Cola.flac", title="01A - 124 - Cola", key="01A")
    assert _plan(folder)["items"] == []


def test_an_unpadded_head_is_carried_and_padded_with_the_tempo_intact(configured):
    folder = _folder(configured)
    path = _track(folder, "1A - 124 - Cola.flac", title="1A - 124 - Cola", key="1A")
    assert _moves(_plan(folder)) == [
        ("1A - 124 - Cola.flac", "01A - 124 - Cola.flac")
    ]
    _apply(folder)
    renamed = folder / "01A - 124 - Cola.flac"
    assert renamed.is_file() and not path.exists()
    assert tags.read_tag(renamed, "title") == "01A - 124 - Cola"
    assert _plan(folder)["items"] == []


def test_the_head_is_recovered_from_the_title_when_the_filename_lost_it(configured):
    """The tag then rename crash window leaves the head in the title and not
    in the filename. The pass heals that file rather than stripping it."""
    folder = _folder(configured)
    _track(folder, "Cola.flac", title="01A - 124 - Cola", key="01A")
    _apply(folder)
    healed = folder / "01A - 124 - Cola.flac"
    assert healed.is_file()
    assert tags.read_tag(healed, "title") == "01A - 124 - Cola"


def test_the_plan_and_the_apply_agree_on_a_marked_file(configured):
    """The plan used to build its spec without the lossy flag, so it promised
    a marked file a rename the apply pass was never going to perform."""
    folder = _folder(configured)
    marker = configured.naming.lossy_marker
    _track(folder, f"{marker} Cola.flac", title=f"{marker} Cola")
    assert _plan(folder)["items"] == []


def test_a_name_with_no_parseable_head_is_left_as_it_arrives(configured):
    """13A is off the wheel, so the whole name is the body and stays put.
    Driven and pinned rather than assumed."""
    folder = _folder(configured)
    _track(folder, "13A - 124 - Cola.flac", title="13A - 124 - Cola")
    assert _plan(folder)["items"] == []


def test_a_key_tag_that_is_not_camelot_does_not_poison_the_pass(configured):
    """The head's own key still carries the rename; the junk tag is ignored
    rather than crashing the render or overruling the head."""
    folder = _folder(configured)
    _track(folder, "1A - 124 - Cola.flac", title="1A - 124 - Cola", key="Amaj")
    assert _moves(_plan(folder)) == [
        ("1A - 124 - Cola.flac", "01A - 124 - Cola.flac")
    ]


def test_the_tag_key_wins_over_a_stale_head_and_the_pass_converges(configured):
    """Renaming from metadata is the verb's job. The head fills silence; it
    does not overrule a tag somebody corrected, and one apply converges."""
    folder = _folder(configured)
    _track(folder, "01A - 124 - Cola.flac", title="01A - 124 - Cola", key="2A")
    assert _moves(_plan(folder)) == [
        ("01A - 124 - Cola.flac", "02A - 124 - Cola.flac")
    ]
    _apply(folder)
    assert (folder / "02A - 124 - Cola.flac").is_file()
    assert _plan(folder)["items"] == []


def test_the_filename_head_alone_is_enough_when_the_title_tag_lacks_it(configured):
    """Acquired files often carry a clean title tag while the filename still
    holds the head. The filename is the surface being renamed, so it is the
    first head source, and the title fallback must not be the only one."""
    folder = _folder(configured)
    _track(folder, "1A - 124 - Cola.flac", title="Cola")
    assert _moves(_plan(folder)) == [
        ("1A - 124 - Cola.flac", "01A - 124 - Cola.flac")
    ]
    _apply(folder)
    renamed = folder / "01A - 124 - Cola.flac"
    assert renamed.is_file()
    assert tags.read_tag(renamed, "title") == "01A - 124 - Cola"


def test_the_filename_head_wins_when_both_heads_parse_and_disagree(configured):
    """Precedence, pinned where it is observable. Every other test that gives
    both surfaces a parseable head gives them the SAME values, so none of them
    can tell "the filename wins" from "either wins, it did not matter here".
    The filename is the convention's ground truth and the title is a recovery
    fallback for the crash window, not a correction channel, so a stale title
    head must not drag a correct filename backwards."""
    folder = _folder(configured)
    _track(folder, "1A - 124 - Cola.flac", title="5B - 95 - Cola")
    assert _moves(_plan(folder)) == [
        ("1A - 124 - Cola.flac", "01A - 124 - Cola.flac")
    ]


#: U41 answered the question the removed test had guessed at. The head is the
#: verb's to derive; the BODY of each surface is carried through untouched. The
#: filename keeps the filename's body and the title tag keeps the title tag's,
#: which is what `NameSpec` always meant by holding `stem` and `title`
#: separately. Measured over the library on 2026-08-25, read only: 53 percent of
#: names are `Title - Artist - Album`, 25 percent are `Artist - Title`, and one
#: percent have a body equal to the title tag, so no single recomposition rule
#: fits and none is attempted.


def test_the_filename_body_is_carried_through_a_padding_rename(configured):
    """R-168. The library keeps the artist in the filename and the title alone
    in the tag, so composing the name from the tag drops the artist off almost
    every file. The head is padded and the body is whatever the file already
    had."""
    folder = _folder(configured)
    _track(
        folder,
        "1A - 124 - Artist Name - Song Title.flac",
        title="1A - 124 - Song Title",
        key="1A",
    )
    assert _moves(_plan(folder)) == [
        (
            "1A - 124 - Artist Name - Song Title.flac",
            "01A - 124 - Artist Name - Song Title.flac",
        )
    ]


def test_the_title_tag_is_not_given_the_filename_body(configured):
    """The other half of the same decision, and the one a rename could corrupt
    silently. The apply pass rewrites the title tag, so a spec that fed the
    filename's body into both surfaces would stuff the artist and the album
    into every title tag in the library. Each surface keeps its own body."""
    folder = _folder(configured)
    _track(
        folder,
        "1A - 124 - Artist Name - Song Title.flac",
        title="1A - 124 - Song Title",
        key="1A",
    )
    _apply(folder)
    renamed = folder / "01A - 124 - Artist Name - Song Title.flac"
    assert renamed.is_file()
    assert tags.read_tag(renamed, "title") == "01A - 124 - Song Title"


def test_both_library_grammars_survive_a_rename(configured):
    """Measured on the real library: `Artist - Title` and
    `Title - Artist - Album` both occur, in that order of rarity, and no rule
    distinguishes them. Preserving the body serves both without knowing which
    is which."""
    folder = _folder(configured)
    _track(folder, "2A - 120 - Artist - Song.flac", title="2A - 120 - Song")
    _track(
        folder,
        "3A - 121 - Song Two - Artist Two - Some Album.flac",
        title="3A - 121 - Song Two",
    )
    assert sorted(_moves(_plan(folder))) == sorted(
        [
            ("2A - 120 - Artist - Song.flac", "02A - 120 - Artist - Song.flac"),
            (
                "3A - 121 - Song Two - Artist Two - Some Album.flac",
                "03A - 121 - Song Two - Artist Two - Some Album.flac",
            ),
        ]
    )


def test_a_rename_never_replaces_the_body_with_the_title_tag(configured):
    """The structural form of R-168, stated as what it actually forbids.

    "A rename never shortens the body" is the wrong rule and was tried first.
    Two shorteners are legitimate and predate this unit: ``dedupe_stem`` drops a
    trailing segment that merely repeats the lead, and ``fit_to_budget``
    truncates a name over the path ceiling. Driven over sixty real library files
    they account for every remaining body change and nothing else does. What
    must never happen is the body being REPLACED by the title tag's body, which
    is the defect, and that is the first assertion.

    THESE THREE FIXTURES DELIBERATELY TRIGGER NEITHER SHORTENER, which is why
    the second assertion may demand exact equality here. That is a property of
    the inputs and not a general rule, so do not read it as one and do not
    "fix" a future failure by widening it. The shorteners are pinned in
    ``test_a_trailing_segment_repeating_the_lead_is_still_deduped``,
    ``test_a_trailing_segment_that_only_starts_with_the_lead_survives`` and
    ``test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt``. Two
    reviewers caught this docstring promising a weaker rule than the assertion
    enforced, which is the same shape as the defect this unit fixes."""
    folder = _folder(configured)
    names = [
        "1A - 124 - Artist Name - Song Title.flac",
        "2A - 120 - Song - Artist - Album.flac",
        "4A - 90 - Just A Body.flac",
    ]
    for name in names:
        _track(folder, name, title="Song")
    template = _template(configured)
    moves = _moves(_plan(folder))
    # Without this the whole guard is a loop with no assertion outside it, so an
    # implementation that proposes NO rename satisfies it vacuously. Driven by
    # the independent pass, which passed this test against a plan pass stubbed
    # to return nothing. All three fixtures are unpadded, so all three move.
    assert len(moves) == 3, f"expected three renames, got {moves!r}"
    for frm, to in moves:
        before = naming.strip_head(Path(frm).stem, template=template)
        after = naming.strip_head(Path(to).stem, template=template)
        assert after != "Song", (
            f"{frm} was rebuilt from the title tag: {before!r} became {after!r}"
        )
        assert after == before, f"{frm} lost body text: {before!r} became {after!r}"


def test_a_trailing_segment_repeating_the_lead_is_still_deduped(configured):
    """``dedupe_stem`` has always run inside ``build`` and never had anything to
    work on, because the body it received was a single segment off the title
    tag. Feeding it the filename's real body is what switches it on, so its
    behaviour is pinned here rather than discovered later as a surprise. Nine of
    sixty real files take this path."""
    folder = _folder(configured)
    _track(
        folder,
        "5A - 122 - Golden Boy - Alphadog - Golden Boy.flac",
        title="5A - 122 - Golden Boy",
    )
    assert _moves(_plan(folder)) == [
        (
            "5A - 122 - Golden Boy - Alphadog - Golden Boy.flac",
            "05A - 122 - Golden Boy - Alphadog.flac",
        )
    ]


def test_a_marker_in_the_title_alone_is_still_recovered(configured):
    """The marker is read from either surface, and the only other test of that
    ``or`` puts it in BOTH at once, so it cannot say which operand carries the
    case. This is the marker's own crash window: a run that wrote the marked
    title and died before the rename leaves the marker in the title alone, and
    the pass has to carry it onto the file rather than drop it."""
    folder = _folder(configured)
    marker = configured.naming.lossy_marker
    _track(folder, "Cola.flac", title=f"{marker} Cola")
    assert _moves(_plan(folder)) == [("Cola.flac", f"{marker} Cola.flac")]


def test_a_marker_in_the_filename_alone_is_not_stripped_off(configured):
    """The other operand of the same ``or``, and the direction that loses data.
    An acquired file is marked in its name while its title tag arrives clean
    from the source. If only the title were consulted the render would drop
    the marker, and the pass would propose renaming the marked file to its
    unmarked form, which is how a lossy copy and its lossless twin stop being
    distinguishable. It proposes nothing instead."""
    folder = _folder(configured)
    marker = configured.naming.lossy_marker
    _track(folder, f"{marker} Cola.flac", title="Cola")
    assert _plan(folder)["items"] == []


def test_a_trailing_segment_that_only_starts_with_the_lead_survives(configured):
    """The negative half of dedupe, and the rule that makes it safe to run
    unconditionally. ``dedupe_stem``'s docstring calls it "ambiguity means
    identity": anything not matching exactly passes through byte identical, so
    a trailing segment that merely BEGINS with the lead is not a repeat and is
    kept. Only the positive case was pinned, which is how a widened rule would
    have shipped looking correct."""
    folder = _folder(configured)
    _track(
        folder,
        "6A - 118 - Track - Artist - Track (Deluxe Edition).flac",
        title="6A - 118 - Track",
    )
    assert _moves(_plan(folder)) == [
        (
            "6A - 118 - Track - Artist - Track (Deluxe Edition).flac",
            "06A - 118 - Track - Artist - Track (Deluxe Edition).flac",
        )
    ]


def test_a_deduping_rename_converges_on_one_pass(configured):
    """``dedupe_stem`` applies its rule once rather than to a fixed point, and
    this unit is what gave it real input, so convergence is pinned at the
    surface rather than assumed. Apply, then re-plan and require silence."""
    folder = _folder(configured)
    _track(
        folder,
        "5A - 122 - Golden Boy - Alphadog - Golden Boy.flac",
        title="5A - 122 - Golden Boy",
    )
    _apply(folder)
    assert (folder / "05A - 122 - Golden Boy - Alphadog.flac").is_file()
    assert _plan(folder)["items"] == []


def test_a_file_with_no_title_tag_takes_its_body_from_the_filename(configured):
    """The only surface left when the tag is absent is the name itself, so the
    body comes from there and the tag is populated from it. This fills an empty
    tag rather than losing anything, and it is what the pre-U41 code did too.
    Driven by hand during review and pinned here because a hand drive that
    leaves no test is a measurement nobody can repeat."""
    folder = _folder(configured)
    _track(folder, "1A - 124 - Artist Name - Song Title.flac", key="1A")
    _apply(folder)
    renamed = folder / "01A - 124 - Artist Name - Song Title.flac"
    assert renamed.is_file()
    assert tags.read_tag(renamed, "title") == "01A - 124 - Artist Name - Song Title"


def test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt(configured):
    """Truncation went from unreachable to live in this unit, and nothing drove
    it. While the body came off the title tag it was short by construction, so
    the ceiling was never approached; carrying the real body means some names
    now cross it. Four of thirty six renames in a sixty file real library
    sample took this path.

    Truncating is not the defect. Losing the body to the tag is. This asserts
    the shape rather than an exact string, because the fixture's temporary
    parent directory varies in length between runs and moves the cut."""
    folder = _folder(configured)
    body = "Artist Name - " + ("Extremely Long Song Title Part " * 6).strip()
    name = f"1A - 124 - {body}.flac"
    _track(folder, name, title="1A - 124 - Short")
    moves = _moves(_plan(folder))
    assert len(moves) == 1
    template = _template(configured)
    before = naming.strip_head(Path(moves[0][0]).stem, template=template)
    after = naming.strip_head(Path(moves[0][1]).stem, template=template)
    assert after != "Short", "the body was rebuilt from the title tag"
    assert after.startswith("Artist Name - "), "the leading artist was lost"
    assert "~" in after, "an over ceiling name should carry the truncation hash"
    assert len(after) < len(before), "nothing was truncated"


# ---------------------------------------------------------------------------
# U67: a file the collection references is never renamed or retagged.
#
# Driven against a DISPOSABLE database in the temporary library, never the
# configured one, through the same seams ``tests/test_adopt_collection.py``
# neutralises. The open is a read, so none of those seams weakens the guard
# under test.
# ---------------------------------------------------------------------------


@pytest.fixture
def prefix_map() -> list[dict[str, str]]:
    """No volume rewrites, unless a test parametrizes this name."""
    return []


@pytest.fixture
def collected(library, monkeypatch, prefix_map):
    """A configured machine whose collection is a real, readable database.

    The rows are added per test through :func:`_record`.
    """
    from pyrekordbox.db6 import database as binding

    data = valid_data(
        library,
        rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
    )
    if prefix_map:
        data["library"]["location_prefix_map"] = prefix_map
    resolved = config.from_dict(data)
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )
    _build_disposable_database(Path(resolved.library.db_path), with_tag_category=False)
    return resolved


def _record(cfg, recorded: str, *, identifier: str, deleted: int = 0) -> None:
    """Add one collection row recording ``recorded`` as its path."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(f"sqlite:///{cfg.library.db_path}")
    with Session(engine) as db_session:
        db_session.add(
            _row(
                tables.DjmdContent,
                ID=identifier,
                Title=Path(recorded).name,
                rb_local_deleted=deleted,
                FolderPath=recorded,
            )
        )
        db_session.commit()
    engine.dispose()


def _pair(folder: Path) -> tuple[Path, Path]:
    """Two unpadded files, each of which the pass would rename."""
    held = _track(folder, "1A - 124 - Held.flac", title="1A - 124 - Held", key="1A")
    free = _track(folder, "2A - 124 - Free.flac", title="2A - 124 - Free", key="2A")
    return held, free


def _refusal(folder: Path) -> tuple[int, dict]:
    return _answer(folder)


def test_a_referenced_file_is_untouched_and_its_sibling_is_renamed(collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, str(held), identifier="10")
    before = held.read_bytes()
    plan = _plan(folder)
    assert {item["from"]: item["action"] for item in plan["items"]} == {
        held.name: "referenced",
        free.name: "rename",
    }
    assert plan["totals"] == {"count": 1, "referenced": 1, "collides": 0}
    _apply(folder)
    assert held.is_file() and held.read_bytes() == before
    assert not free.exists() and (folder / "02A - 124 - Free.flac").is_file()


def test_a_row_recorded_as_a_location_url_protects_its_file(collected):
    folder = _folder(collected)
    held, _free = _pair(folder)
    _record(collected, locations.location_url(held), identifier="10")
    _apply(folder)
    assert held.is_file()


@pytest.mark.parametrize(
    "prefix_map", [[{"from": "/mnt/volume", "to": "{library.root}"}]]
)
def test_a_row_under_a_remapped_volume_still_protects_its_file(collected):
    folder = _folder(collected)
    held, _free = _pair(folder)
    relative = held.relative_to(collected.library.root)
    _record(collected, f"/mnt/volume/{relative}", identifier="10")
    assert _plan(folder)["totals"]["referenced"] == 1
    _apply(folder)
    assert held.is_file()


# ---------------------------------------------------------------------------
# R-500: a row whose recorded prefix matches no rule refuses the whole verb.
#
# Such a row is keyed only by a spelling no file on this machine carries, so it
# matches no candidate and the file it names is planned as an ordinary rename.
# The deletion pass refuses on the same condition, and the two writers now agree
# about what an unmapped row means.
# ---------------------------------------------------------------------------


def test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing(collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    relative = held.relative_to(collected.library.root)
    _record(collected, f"/mnt/volume/{relative}", identifier="10")
    code, envelope = _refusal(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "collection-row-unmapped"
    assert cause["remediation"]["remedy"] == "fix-config-values"
    assert "location_prefix_map" in cause["remediation"]["steps"][0]
    assert cause["message"].startswith("1 collection row records")
    assert f"/mnt/volume/{relative}" in cause["message"]
    assert cause["detail"]["unmapped"] == 1
    assert cause["detail"]["unmapped_locations"] == [f"/mnt/volume/{relative}"]
    assert cause["detail"]["unmapped_prefixes"] == ["/mnt/volume"]
    assert held.is_file() and free.is_file()


def test_an_unmapped_row_refuses_the_plan_too(collected):
    """The abort option reads the plan, and a plan over a collection with a hole
    in it would show a rename the apply was never going to be allowed."""
    folder = _folder(collected)
    _pair(folder)
    _record(collected, "/mnt/volume/Music/elsewhere.flac", identifier="10")
    code, out, _ = drive([
        "--output", "json", "-d", "name.apply.confirm=abort",
        "name", "apply", "--root", str(folder),
    ])
    assert code == int(ExitCode.PRECONDITION), out
    assert json.loads(out)["cause"]["reason"] == "collection-row-unmapped"


def test_every_unmapped_row_is_counted_and_the_first_is_named(collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, "/mnt/volume/Music/b.flac", identifier="10")
    _record(collected, "/mnt/library/Music/a.flac", identifier="11", deleted=1)
    _record(collected, str(held), identifier="12")
    code, envelope = _refusal(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["message"].startswith("2 collection rows record")
    assert "/mnt/volume/Music/b.flac" in cause["message"]
    assert "/mnt/library/Music/a.flac" not in cause["message"]
    assert cause["detail"]["unmapped"] == 2
    assert cause["detail"]["unmapped_prefixes"] == ["/mnt/library", "/mnt/volume"]
    assert held.is_file() and free.is_file()


@pytest.mark.parametrize(
    "prefix_map", [[{"from": "/mnt/VOLUME", "to": "{library.root}"}]]
)
def test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses(collected):
    """PINNED TO THE REFUSAL. The shared resolver compares a prefix exactly, so
    this row is unmapped to every writer, and matching it here alone would make
    this verb a second locate that disagrees with the first. The message names
    the recorded spelling, which is what shows a person the difference."""
    folder = _folder(collected)
    held, free = _pair(folder)
    relative = held.relative_to(collected.library.root)
    _record(collected, f"/mnt/volume/{relative}", identifier="10")
    code, envelope = _refusal(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "collection-row-unmapped"
    assert "/mnt/volume/" in envelope["cause"]["message"]
    assert held.is_file() and free.is_file()


def test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename(
    collected, monkeypatch
):
    """The re-read before the rename, on its own. The plan is built over a
    collection every row of which resolves, and the apply pass reads one that
    gained a row under a volume no rule names."""
    folder = _folder(collected)
    held, free = _pair(folder)
    reads = iter([(), ("/mnt/volume/Music/late.flac",)])
    monkeypatch.setattr(naming_cli, "_recorded", lambda cfg: next(reads))
    code, envelope = _refusal(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "collection-row-unmapped"
    assert held.is_file() and free.is_file()


def test_the_refusal_names_the_decoded_location_a_rule_is_matched_against(collected):
    """A row recorded as a location URL is quoted DECODED, because a rule is
    compared with the decoded path and the encoded spelling would never match."""
    folder = _folder(collected)
    _pair(folder)
    _record(collected, "file://localhost/mnt/volume/My%20Music/x.flac", identifier="10")
    _code, envelope = _refusal(folder)
    cause = envelope["cause"]
    assert "/mnt/volume/My Music/x.flac" in cause["message"]
    assert "%20" not in cause["message"]
    assert cause["detail"]["unmapped_locations"] == ["/mnt/volume/My Music/x.flac"]


def test_an_unmapped_row_whose_file_is_gone_refuses_even_outside_a_volume(
    collected, tmp_path
):
    """The other half of the existence rule. The folder is on this machine and
    the recorded file is not, so nothing says which file the row names."""
    folder = tmp_path / "laptop" / "Downloads"
    folder.mkdir(parents=True)
    held, free = _pair(folder)
    _record(collected, str(folder / "moved away.flac"), identifier="10")
    code, envelope = _refusal(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["detail"]["unmapped_locations"] == [
        str(folder / "moved away.flac")
    ]
    assert held.is_file() and free.is_file()


def test_the_refusal_counts_every_row_and_lists_no_more_than_twenty(collected):
    """A fresh setup was measured at 9937 unmapped rows, which uncapped is 9937
    strings in one envelope. The count is never capped, only the two lists."""
    recorded = tuple(f"/absent-{index:02d}/music/track.flac" for index in range(25))
    with pytest.raises(naming_cli.CratekitError) as refused:
        naming_cli._referenced(recorded, cfg=collected)
    detail = refused.value.cause.detail
    assert detail["unmapped"] == 25
    assert detail["unmapped_locations"] == list(recorded[:20])
    assert detail["unmapped_prefixes"] == [f"/absent-{index:02d}/music" for index in range(20)]
    assert refused.value.cause.message.startswith("25 collection rows record")


def test_a_row_recording_a_link_to_nothing_is_dark(collected, tmp_path):
    """The name is on this machine and the file behind it is not, so the row has
    not answered. Existence is asked of what the path reaches, never of the
    link itself."""
    folder = _folder(collected)
    held, free = _pair(folder)
    dangling = tmp_path / "elsewhere" / "gone.flac"
    dangling.parent.mkdir()
    dangling.symlink_to(tmp_path / "elsewhere" / "never there.flac")
    _record(collected, str(dangling), identifier="10")
    code, envelope = _refusal(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert held.is_file() and free.is_file()


def test_a_row_that_is_not_a_path_neither_blocks_nor_protects(collected):
    """A streaming pseudo-location references no file, so it is not a hole in
    the collection, and a library that ever streamed anything still renames."""
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, "tidal:tracks:12345", identifier="10")
    _apply(folder)
    assert not held.exists() and not free.exists()


def test_an_unmapped_row_over_an_empty_folder_refuses_nothing(collected):
    """With no rename candidate the collection is not read at all, so a hole in
    it cannot change the outcome and the empty plan is still readable."""
    folder = _folder(collected)
    _record(collected, "/mnt/volume/Music/elsewhere.flac", identifier="10")
    assert _plan(folder)["items"] == []


@pytest.mark.parametrize("form", ["NFD", "NFC"])
def test_a_composition_variant_of_the_name_still_protects_its_file(collected, form):
    folder = _folder(collected)
    other = "NFC" if form == "NFD" else "NFD"
    name = unicodedata.normalize(form, "1A - 124 - Café.flac")
    held = _track(folder, name, key="1A")
    recorded = str(folder / unicodedata.normalize(other, "1A - 124 - Café.flac"))
    assert recorded != str(held)
    _record(collected, recorded, identifier="10")
    _apply(folder)
    assert held.is_file()


def test_a_case_variant_of_the_name_still_protects_its_file(collected):
    folder = _folder(collected)
    held, _free = _pair(folder)
    _record(collected, str(held).replace("Held", "HELD"), identifier="10")
    _apply(folder)
    assert held.is_file()


def test_a_tombstoned_row_still_protects_its_file(collected):
    folder = _folder(collected)
    held, _free = _pair(folder)
    _record(collected, str(held), identifier="10", deleted=1)
    _apply(folder)
    assert held.is_file()


def test_a_root_outside_the_library_is_still_checked(collected, tmp_path):
    """The row sits under no rule and its recorded file is on this machine, so
    it has answered (R-500): the recorded key protects the file and nothing
    refuses. A downloads folder is the ordinary case."""
    folder = tmp_path / "laptop" / "Downloads"
    folder.mkdir(parents=True)
    held, free = _pair(folder)
    _record(collected, str(held), identifier="10")
    _apply(folder)
    assert held.is_file()
    assert not free.exists()


def test_a_database_with_no_matching_row_proceeds(collected):
    """Zero referencing rows from a database that OPENED is a fact, not a
    failure, so the pass renames. The disposable database holds two rows with
    no path at all."""
    folder = _folder(collected)
    held, free = _pair(folder)
    _apply(folder)
    assert not held.exists() and not free.exists()


def test_the_digest_changes_when_a_row_starts_referencing_a_file(collected):
    folder = _folder(collected)
    held, _free = _pair(folder)
    before = _plan(folder)["digest"]
    _record(collected, str(held), identifier="10")
    assert _plan(folder)["digest"] != before


def test_a_missing_database_refuses_and_renames_nothing(collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    Path(collected.library.db_path).unlink()
    code, envelope = _refusal(folder)
    assert code == int(ExitCode.LIBRARY_UNREADABLE), envelope
    assert envelope["cause"]["reason"] == "collection-unreadable"
    assert envelope["cause"]["remediation"]["remedy"] != "restore-from-snapshot"
    assert held.is_file() and free.is_file()


def test_an_unopenable_database_refuses_and_renames_nothing(collected):
    folder = _folder(collected)
    held, free = _pair(folder)
    Path(collected.library.db_path).write_bytes(b"not a database at all")
    code, envelope = _refusal(folder)
    assert code == int(ExitCode.LIBRARY_UNREADABLE), envelope
    assert envelope["cause"]["reason"] == "collection-unreadable"
    assert held.is_file() and free.is_file()


def test_an_empty_folder_needs_no_database(collected):
    """With nothing to rename the collection cannot change the outcome, so a
    machine with no database can still read an empty plan."""
    folder = _folder(collected)
    Path(collected.library.db_path).unlink()
    assert _plan(folder)["items"] == []


def test_a_row_that_appears_after_the_gate_still_protects_its_file(collected, monkeypatch):
    """The re-check before the rename, on its own. The plan is built over an
    empty collection and the apply pass reads one that references the file,
    which is rekordbox importing while the gate waits on a person.

    R-172 added the second half: the file is still protected AND the run says
    the rename a person approved did not happen. The protection is not a reason
    to report success over a plan that was carried out in part, and the next run
    shows the same file as referenced and exits 0.
    """
    folder = _folder(collected)
    held, free = _pair(folder)
    reads = iter([(), (str(held),)])
    monkeypatch.setattr(naming_cli, "_recorded", lambda cfg: next(reads))
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    incomplete = envelope["cause"]["detail"]["incomplete"]
    assert [item["from"] for item in incomplete] == [held.name]
    assert "began referencing it" in incomplete[0]["why"]
    assert held.is_file()
    assert not free.exists()


def test_a_library_with_cloud_sync_on_refuses_and_names_the_real_cause(collected, monkeypatch):
    """The read open still runs the canary, which refuses a library whose cloud
    sync is ON. That is kept as a refusal, the same one every other collection
    reader makes, and the person is told the real cause and its remedy rather
    than only that the collection could not be read."""
    folder = _folder(collected)
    held, free = _pair(folder)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 1},
    )
    code, envelope = _refusal(folder)
    assert code == int(ExitCode.LIBRARY_UNREADABLE), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "collection-unreadable"
    assert cause["remediation"]["remedy"] == "disable-cloud-sync"
    assert "Cloud Library Sync" in cause["message"]
    assert held.is_file() and free.is_file()


def test_a_file_recorded_by_its_real_path_is_protected_through_a_linked_root(
    collected, tmp_path
):
    """The root is given through a link and the row records the real path, so
    only the RESOLVED spelling of the candidate matches."""
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, str(held), identifier="10")
    link = tmp_path / "linked"
    link.symlink_to(folder, target_is_directory=True)
    _apply(link)
    assert held.is_file()
    assert not free.exists()


def test_a_file_recorded_through_a_link_is_protected_through_that_link(
    collected, tmp_path
):
    """The row records the path through a link and the root is given the same
    way, so only the ABSOLUTE spelling of the candidate matches."""
    folder = _folder(collected)
    held, free = _pair(folder)
    link = tmp_path / "linked"
    link.symlink_to(folder, target_is_directory=True)
    _record(collected, str(link / held.name), identifier="10")
    _apply(link)
    assert held.is_file()
    assert not free.exists()


def test_a_row_naming_another_host_neither_blocks_nor_protects(collected):
    """A remote location has no local path, so it protects no local file, and
    one such row in a library must not stop the verb for every other file."""
    folder = _folder(collected)
    held, free = _pair(folder)
    _record(collected, f"file://elsewhere.invalid{held}", identifier="10")
    _apply(folder)
    assert not held.exists() and not free.exists()


def test_a_read_that_fails_after_the_open_refuses_and_renames_nothing(
    collected, monkeypatch
):
    """The open succeeds and the query does not, which is a failure no open
    side check classifies. It still refuses rather than reading as empty."""
    folder = _folder(collected)
    held, free = _pair(folder)

    class _Broken:
        def get_content(self):
            raise RuntimeError("the query failed")

    monkeypatch.setattr(rb_writer, "open_db", lambda *args, **kwargs: _Broken())
    monkeypatch.setattr(rb_writer, "close_db", lambda handle: None)
    code, envelope = _refusal(folder)
    assert code == int(ExitCode.LIBRARY_UNREADABLE), envelope
    assert envelope["cause"]["reason"] == "collection-unreadable"
    assert envelope["cause"]["remediation"]["remedy"] == "report-defect"
    assert held.is_file() and free.is_file()


def test_a_rename_onto_a_name_another_file_holds_overwrites_nothing(configured):
    """Two files that render to one name. The padded one is already in
    convention, and the unpadded one would be renamed onto it, which on this
    platform replaces the file silently. The claim on the target is what
    stops that, and nothing drove it until the U67 mutation table asked.

    R-172 added the second half: the file that stays put is NAMED. The target
    is a file on disk that nothing is moving, so the collision is known while
    the plan is built and the rename is never promised.
    """
    folder = _folder(configured)
    kept = _track(folder, "01A - 124 - Cola.flac", title="01A - 124 - Cola", key="01A")
    other = _track(folder, "1A - 124 - Cola.flac", title="1A - 124 - Cola", key="1A")
    tags.write_tags(kept, {"artist": "the one already in place"})
    assert _actions(_plan(folder)) == {other.name: "collides"}
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "rename-incomplete"
    assert other.name in envelope["cause"]["message"]
    assert other.is_file()
    assert tags.read_tag(kept, "artist") == "the one already in place"


# ---------------------------------------------------------------------------
# R-172: a rename the plan promised is never skipped in silence
# ---------------------------------------------------------------------------
#
# The recorded cost: "An operator sweeping the library is told a rename happened
# when it did not, with nothing in the report naming which file stayed put."
# Every test below drives the real dispatcher over real audio files.


def _colliding_pair(folder: Path) -> tuple[Path, Path]:
    """Two files that render to one name, each of which needs a rename.

    The dedupe rule drops a trailing body segment repeating the lead, so these
    two differ on disk and render identically. This is the ledger's own driven
    case, with the dedupe standing in for its 05A song.
    """
    first = _track(
        folder, "5A - 120 - Song - Artist - Song.flac", title="5A - 120 - Song", key="5A"
    )
    second = _track(folder, "5A - 120 - Song - Artist.flac", title="5A - 120 - Song", key="5A")
    return first, second


def test_two_files_rendering_to_one_name_are_not_promised_two_renames(configured):
    """The plan pass owns the collision, which is where the ledger put it.

    Before this, the plan promised both renames, the apply performed one, the
    other file was skipped at the claim and the envelope still answered ok.
    Neither is promised now, both are named, and ``totals.count`` is the number
    of renames that can actually happen.
    """
    folder = _folder(configured)
    first, second = _colliding_pair(folder)
    plan = _plan(folder)
    assert _actions(plan) == {first.name: "collides", second.name: "collides"}
    assert plan["totals"] == {"count": 0, "referenced": 0, "collides": 2}
    assert first.is_file() and second.is_file()


def test_a_collision_answers_with_the_files_that_stayed_put(configured):
    """The apply over that plan renames nothing and says so.

    Answering ok here is the whole finding: every later sweep detects the same
    collision, so a library that can never converge would report success for
    ever. The cause names both files and the remediation says what to do.
    """
    folder = _folder(configured)
    first, second = _colliding_pair(folder)
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "rename-incomplete"
    assert sorted(cause["detail"]["incomplete"], key=lambda item: item["from"]) == [
        {
            "from": first.name,
            "path": str(first),
            "why": f"{second.name} renders to the same name, and neither is renamed",
        },
        {
            "from": second.name,
            "path": str(second),
            "why": f"{first.name} renders to the same name, and neither is renamed",
        },
    ]
    assert envelope["data"]["totals"] == {
        "count": 0,
        "referenced": 0,
        "collides": 2,
        "renamed": 0,
        "incomplete": 2,
    }
    assert first.is_file() and second.is_file()


def test_a_sweep_that_carried_out_every_rename_still_answers_ok(configured):
    """The other half of the outcome, so the new answer cannot swallow the old
    one. Two files with nothing in each other's way both land and the envelope
    is ok at exit 0, which is what every earlier test in this file drives."""
    folder = _folder(configured)
    _track(folder, "1A - 124 - Alpha.flac", title="1A - 124 - Alpha", key="1A")
    _track(folder, "2A - 124 - Beta.flac", title="2A - 124 - Beta", key="2A")
    code, envelope = _answer(folder)
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "ok"
    assert envelope["cause"] is None
    assert envelope["data"]["totals"] == {
        "count": 2,
        "referenced": 0,
        "collides": 0,
        "renamed": 2,
        "incomplete": 0,
    }
    assert (folder / "01A - 124 - Alpha.flac").is_file()
    assert (folder / "02A - 124 - Beta.flac").is_file()


def test_a_target_another_mover_still_holds_is_promised_and_then_reported(configured):
    """The collision the plan CANNOT rule out, driven with nothing faked.

    ``lead`` dedupes onto the name ``marked`` currently holds, and ``marked`` is
    itself moving because its title carries the lossy marker. Sort order decides
    whether the chain resolves: a hyphen sorts before a dot, so ``lead`` is
    attempted first and its target is still occupied. Holding it back in the
    plan would lose a rename that succeeds whenever the order runs the other
    way, so it stays promised and the apply reports what happened.
    """
    folder = _folder(configured)
    marker = configured.naming.lossy_marker
    lead = _track(
        folder,
        "01A - 120 - Alpha - Artist - Alpha.flac",
        title="01A - 120 - Alpha",
        key="01A",
    )
    marked = _track(
        folder,
        "01A - 120 - Alpha - Artist.flac",
        title=f"01A - 120 - Alpha {marker}",
        key="01A",
    )
    assert _actions(_plan(folder)) == {lead.name: "rename", marked.name: "rename"}
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    incomplete = envelope["cause"]["detail"]["incomplete"]
    assert [item["from"] for item in incomplete] == [lead.name]
    assert "already taken" in incomplete[0]["why"]
    assert envelope["data"]["totals"]["renamed"] == 1
    assert lead.is_file()
    assert not marked.exists()


def test_a_file_gone_after_the_plan_is_named_rather_than_skipped(configured, monkeypatch):
    """A file moved or deleted while the gate waits on a person. The plan
    promised its rename, and a report that shows the promise with no mark on it
    is the cost R-172 names."""
    folder = _folder(configured)
    vanishing = _track(folder, "1A - 124 - Gone.flac", title="1A - 124 - Gone", key="1A")
    staying = _track(folder, "2A - 124 - Here.flac", title="2A - 124 - Here", key="2A")
    real = naming_cli._plan_for

    def _plan_then_delete(root, *, cfg):
        plan = real(root, cfg=cfg)
        vanishing.unlink()
        return plan

    monkeypatch.setattr(naming_cli, "_plan_for", _plan_then_delete)
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    incomplete = envelope["cause"]["detail"]["incomplete"]
    assert [item["from"] for item in incomplete] == [vanishing.name]
    assert "no longer there" in incomplete[0]["why"]
    assert not staying.exists() and (folder / "02A - 124 - Here.flac").is_file()


def test_a_rename_the_filesystem_refuses_is_named_and_leaves_no_claim(configured, monkeypatch):
    """The ``OSError`` branch. The claim it created is removed, which was
    already true, and the file it could not rename is now named as well."""
    folder = _folder(configured)
    track = _track(folder, "1A - 124 - Alpha.flac", title="1A - 124 - Alpha", key="1A")
    original = Path.rename

    def _refuse_rename(self, target):
        if self.name == track.name:
            raise OSError(28, "no space left on device")
        return original(self, target)

    monkeypatch.setattr(Path, "rename", _refuse_rename)
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    incomplete = envelope["cause"]["detail"]["incomplete"]
    assert [item["from"] for item in incomplete] == [track.name]
    assert "no space left on device" in incomplete[0]["why"]
    assert track.is_file()
    assert not (folder / "01A - 124 - Alpha.flac").exists()


def test_a_title_tag_that_could_not_be_written_is_named(configured, monkeypatch):
    """The same shape one file over, which METHOD's fifth pattern asks for.

    ``write_tags`` returns False on any failure rather than raising, and nothing
    read the answer, so a file whose title never got the head was reported as a
    rename that happened in full. The rename itself stands and is counted.
    """
    folder = _folder(configured)
    track = _track(folder, "1A - 124 - Alpha.flac", title="1A - 124 - Alpha", key="1A")
    monkeypatch.setattr(naming_cli.tags, "write_tags", lambda path, fields: False)
    code, envelope = _answer(folder)
    assert code == int(ExitCode.PRECONDITION), envelope
    incomplete = envelope["cause"]["detail"]["incomplete"]
    assert [item["from"] for item in incomplete] == [track.name]
    assert "title tag" in incomplete[0]["why"]
    assert envelope["data"]["totals"]["renamed"] == 1
    assert (folder / "01A - 124 - Alpha.flac").is_file()
