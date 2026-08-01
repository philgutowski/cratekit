"""R17, the one rule with no configuration flag: nothing here writes a beat grid.

Beat grids belong to rekordbox and to nobody else. This is not a preference, it
is not tunable, and there is no profile in which it relaxes. The reason is not
squeamishness about touching the database, it is that a wrong grid is worse than
no grid: the detector octave-folds, so a "helpful" BPM seeds a grid at half or
double time, and every cue point and every loop the user has ever set against
that track moves. Import gridless and rekordbox derives BPM and grid from the
audio alone, which it is good at and which is reversible.

R17 has four surfaces, and this file guards all four:

1. **A ``<TEMPO>`` element in COLLECTION XML.** The element rekordbox reads as a
   grid. No emitter may produce one.
2. **A real ``AverageBpm`` in COLLECTION XML.** Tracks import with
   ``AverageBpm="0.00"`` so rekordbox analyses from scratch. An interpolated
   value there is the same mistake wearing a different attribute name.
3. **A ``bpm`` or ``TBPM`` file tag.** rekordbox reads file tags on import, so a
   tag write reaches the same place by a longer route.
4. **The analysis columns of the database.** That surface is the guarded writer's
   additive whitelist, asserted in tests/test_rb_writer_guard.py.

The distinction that makes all of this workable: rekordbox-AUTHORED grid data
must round-trip verbatim. A tool that subsets an export the user already analysed
must hand back every ``<TEMPO>`` it was given, byte for byte. Never create one,
never destroy one. Both halves are asserted below.

If any test here goes red, do not loosen the assertion. The rule is the product.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tests._pending import requires
from tests.xml_fixtures import _ml_track, _no_bare_lf, _xml_doc

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

# Tokens that only ever appear in grid-bearing XML. Any one of them in emitted
# output means a grid was written.
FORBIDDEN_TOKENS = ("<TEMPO", "Battito", "Metro=", "Inizio=")

# File tag keys that carry tempo. Writing any of these reaches rekordbox on
# import just as surely as an XML element does.
FORBIDDEN_TAG_KEYS = frozenset({"bpm", "BPM", "TBPM", "beatgrid", "beat_grid"})

# The one value AverageBpm may carry in anything we emit. It is a string, not a
# number, because the XML attribute is compared as bytes.
GRIDLESS_AVERAGE_BPM = '0.00'


# ═══════════════════════════════════════════════════════════════════════════
# Half one: no module in the package can emit a grid. Runs today.
# ═══════════════════════════════════════════════════════════════════════════


def beatgrid_emission_violations(source: str, module: str) -> list[str]:
    """Return one message per grid-writing construct in ``source``.

    A source scan rather than an output check, because it holds for code that
    has not been written yet, and because it catches the emitter that would only
    fire on some rare branch nobody thought to test.

    Three constructs are violations:

    * a string literal containing a grid token;
    * a string literal ending in ``AverageBpm="``, which means the value that
      follows is interpolated and therefore is not the gridless constant;
    * an assignment into a tag mapping under a tempo key.
    """
    problems: list[str] = []
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            for token in FORBIDDEN_TOKENS:
                if token in node.value:
                    problems.append(
                        f"{module}: emits the grid token {token!r}; beat grids are "
                        f"rekordbox-only and are never written by this package (R17)"
                    )
            if node.value.rstrip().endswith('AverageBpm="'):
                problems.append(
                    f"{module}: interpolates a value into AverageBpm; tracks import "
                    f'with AverageBpm="{GRIDLESS_AVERAGE_BPM}" so rekordbox derives '
                    f"the grid from the audio alone (R17)"
                )

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Subscript)
                    and isinstance(target.slice, ast.Constant)
                    and target.slice.value in FORBIDDEN_TAG_KEYS
                ):
                    problems.append(
                        f"{module}: writes the file tag {target.slice.value!r}; "
                        f"rekordbox reads file tags on import, so a tempo tag is a "
                        f"grid by another route (R17)"
                    )
    return problems


def _package_modules() -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
        relative = path.relative_to(SRC_ROOT).with_suffix("")
        parts = list(relative.parts)
        if parts[-1] == "__init__":
            parts.pop()
        out.append((".".join(parts), path.read_text()))
    return out


def test_no_module_in_the_package_emits_a_grid():
    """The live half of the guard. Green today, and green is the point.

    U6 lands this before any emitter exists precisely so that the first emitter
    to try cannot land quietly.
    """
    problems: list[str] = []
    for module, source in _package_modules():
        problems += beatgrid_emission_violations(source, module)
    assert not problems, "R17 violations:\n" + "\n".join(problems)


@pytest.mark.parametrize(
    "source, expect",
    [
        ('X = \'      <TEMPO Inizio="0.5" Bpm="124.00" Metro="4/4" Battito="1"/>\'\n',
         "grid token"),
        ('X = "Battito=1"\n', "grid token"),
        ('X = f\'<TRACK AverageBpm="{bpm}"\'\n', "interpolates a value into AverageBpm"),
        ('tags["bpm"] = "124"\n', "writes the file tag"),
        ('tags["TBPM"] = value\n', "writes the file tag"),
    ],
)
def test_the_source_scan_catches_each_way_of_writing_a_grid(source, expect):
    problems = beatgrid_emission_violations(source, "cratekit.intake.collection_xml")
    assert any(expect in p for p in problems), f"{expect!r} not caught; got {problems}"


def test_the_gridless_constant_is_not_a_violation():
    """What correct emission looks like. Asserted so the guard cannot forbid it."""
    source = 'LINE = \'           TotalTime="300" Year="0" AverageBpm="0.00"\'\n'
    assert beatgrid_emission_violations(source, "cratekit.intake.collection_xml") == []


def test_reading_a_bpm_tag_is_not_a_violation():
    """Analysis legitimately READS tempo. The rule is about writing it.

    A guard that forbade reading would make key detection impossible and would
    be worked around within a week, which is worse than no guard.
    """
    source = "value = tags.get('bpm')\nexisting = tags['TBPM']\n"
    assert beatgrid_emission_violations(source, "cratekit.analysis.detect") == []


# ═══════════════════════════════════════════════════════════════════════════
# Half two: rekordbox-authored grids round-trip verbatim. Runs today.
# ═══════════════════════════════════════════════════════════════════════════


def test_a_rekordbox_authored_grid_survives_verbatim():
    """Never create a grid, and never destroy one either.

    A user who has analysed their library has grid data worth more than the
    tracks. Any tool that subsets or rewrites an export must hand every
    ``<TEMPO>`` back byte for byte. This asserts the fixture actually carries one,
    so the ported round-trip tests in later units have something real to prove.
    """
    analysed = _xml_doc(
        collection=['  <COLLECTION Entries="1">', *_ml_track(101, "01A - 124 - One",
                                                             analyzed=True),
                    "  </COLLECTION>"],
        root_children=['      <NODE Name="INBOX" Type="0" Count="0">', "      </NODE>"],
    )
    assert b"<TEMPO " in analysed, "the analysed fixture must carry a real grid"
    assert b'AverageBpm="124.00"' in analysed
    assert _no_bare_lf(analysed)


def test_our_own_track_shape_is_gridless():
    """The same builder, without the analysed flag, is what our emitters imitate."""
    ours = _xml_doc(
        collection=['  <COLLECTION Entries="1">', *_ml_track(102, "02A - 120 - Two"),
                    "  </COLLECTION>"],
        root_children=['      <NODE Name="INBOX" Type="0" Count="0">', "      </NODE>"],
    )
    for token in FORBIDDEN_TOKENS:
        assert token.encode() not in ours, f"grid token {token!r} in a gridless track"
    assert f'AverageBpm="{GRIDLESS_AVERAGE_BPM}"'.encode() in ours


# ═══════════════════════════════════════════════════════════════════════════
# Half three: the ported emitter guards. Armed when U37 lands the emitter.
# ═══════════════════════════════════════════════════════════════════════════


def _meta(**over):
    """The metadata shape the COLLECTION TRACK emitter consumes.

    ``inizio`` is populated ON PURPOSE. A first-beat anchor is a legitimate
    dormant file tag; what it must never become is a ``<TEMPO>``. Carrying it in
    the default fixture means every test below is the adversarial case.
    """
    meta = dict(
        bpm=124.0,
        energy=7,
        name="04A - 124 - Test Title",
        artist="Test Artist",
        album="Test Album",
        genre="Deep House",
        size_bytes=12345678,
        duration_s=321,
        bitrate_kbps=1000,
        sample_rate=44100,
        location="file://localhost/x.flac",
        tonality="4A",
        inizio=0.512,
    )
    meta.update(over)
    return meta


@requires("cratekit.intake.collection_xml")
def test_track_xml_has_no_beatgrid():
    from cratekit.intake.collection_xml import build_track_xml

    xml = build_track_xml(42, _meta(), "2026-01-01")
    for token in FORBIDDEN_TOKENS:
        assert token not in xml, (
            f"beat-grid token {token!r} leaked into TRACK XML; external grids are "
            f"forbidden (R17)"
        )


@requires("cratekit.intake.collection_xml")
def test_track_xml_has_no_grid_even_with_inizio_and_no_energy():
    """The adversarial case: an anchor present and no energy.

    This exact combination, a populated ``inizio`` with a null rating, is the
    shape the source system's removed ``<TEMPO>`` code fired on. It must still
    produce zero grid, and it must still produce a real TRACK entry, so the guard
    cannot pass by emitting nothing at all.
    """
    from cratekit.intake.collection_xml import build_track_xml

    xml = build_track_xml(7, _meta(energy=None, inizio=3.25), "2026-01-01")
    assert "<TEMPO" not in xml
    assert '<TRACK TrackID="7"' in xml and "</TRACK>" in xml
