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
from pathlib import Path

import pytest

from cratekit import cli
from cratekit.core import config, naming, tags
from cratekit.core.exit_codes import ExitCode
from cratekit.write.naming_cli import _template
from tests._containers import synth_container
from tests.test_config import valid_data


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def configured(library, monkeypatch):
    """A machine set up far enough that the verb reaches its own logic."""
    resolved = config.from_dict(valid_data(library))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: resolved)
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


def _moves(plan: dict) -> list[tuple[str, str]]:
    return [(item["from"], item["to"]) for item in plan["items"]]


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
