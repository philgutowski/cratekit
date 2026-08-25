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
from cratekit.core import config, tags
from cratekit.core.exit_codes import ExitCode
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


def test_the_body_text_comes_from_the_title_and_not_the_filename(configured):
    """The stem is taken from the title tag with its head stripped, which is
    the whole point of renaming from metadata: somebody corrects a title and
    the file follows it. No other test makes the two bodies differ, so a
    version reading the filename's own stem instead would pass all of them."""
    folder = _folder(configured)
    _track(
        folder,
        "1A - 124 - Old Stale Body.flac",
        title="1A - 124 - Corrected Body",
    )
    assert _moves(_plan(folder)) == [
        ("1A - 124 - Old Stale Body.flac", "01A - 124 - Corrected Body.flac")
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
