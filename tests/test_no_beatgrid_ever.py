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
#
# The set is per-container, because a tempo tag is spelled differently in each
# and a guard that knows only one spelling protects only one container. Vorbis
# and Ogg use BPM, ID3 uses the TBPM frame, and MP4 and M4A use the four-letter
# atom `tmpo`, which resembles nothing else on this list and is the reason a
# key set assembled by intuition misses it.
FORBIDDEN_TAG_KEYS = frozenset(
    {
        "bpm", "BPM", "Bpm",            # Vorbis comments, and loose callers
        "TBPM",                          # ID3v2 tempo frame, by name
        "tmpo", "TMPO",                  # MP4 and M4A tempo atom
        "beatgrid", "beat_grid",         # anything storing a grid wholesale
        "AverageBpm", "averagebpm",      # the rekordbox field, by any route
    }
)

# ID3 frame constructors that carry tempo. These never appear as a subscript
# key, so the subscript rule below cannot see them: mutagen writes a frame by
# CONSTRUCTING it and handing it to `tags.add(...)`, which is an expression,
# not an assignment.
#
# This gap was not hypothetical. The downloader vendored in U13 wrote the
# provider's tempo into every file it saved, at three sites in one module, and
# the original guard caught exactly one of them: the Vorbis subscript. The ID3
# site was `tags.add(TBPM(...))` and the MP4 site keyed on `tmpo`. Both would
# have shipped, and every downloaded track would have reached rekordbox
# carrying a grid seed, which is the one outcome R17 exists to prevent.
FORBIDDEN_FRAME_CONSTRUCTORS = frozenset({"TBPM"})

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

        # Constructing a tempo frame at all. There is no legitimate reason to
        # build one: this package never writes tempo, so the constructor call
        # is the violation, wherever its result ends up. Matching the
        # construction rather than the `.add(...)` that consumes it means an
        # intermediate variable, a list comprehension, or a helper that returns
        # the frame is caught just the same.
        if isinstance(node, ast.Call):
            func = node.func
            name = (
                func.id
                if isinstance(func, ast.Name)
                else func.attr
                if isinstance(func, ast.Attribute)
                else None
            )
            if name in FORBIDDEN_FRAME_CONSTRUCTORS:
                problems.append(
                    f"{module}: constructs the {name} tempo frame; this package "
                    f"never writes tempo, so building the frame is the violation "
                    f"regardless of where it is handed off (R17)"
                )

        # A tempo key inside a dict literal, which reaches a tag store through
        # `update(...)` or a keyword-expanded call without ever being a
        # subscript assignment.
        if isinstance(node, ast.Dict):
            for key in node.keys:
                if isinstance(key, ast.Constant) and key.value in FORBIDDEN_TAG_KEYS:
                    problems.append(
                        f"{module}: builds a mapping carrying the tempo key "
                        f"{key.value!r}; a dict handed to a tag writer writes just "
                        f"as surely as a subscript does (R17)"
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
        # The three shapes a real downloader used. Only the first was caught
        # before U13; see FORBIDDEN_FRAME_CONSTRUCTORS for what that cost.
        ('self.m.tags["BPM"] = str(self.bpm)\n', "writes the file tag"),
        ("self.m.tags.add(TBPM(encoding=3, text=str(self.bpm)))\n", "TBPM tempo frame"),
        ('self.m.tags["tmpo"] = [self.bpm]\n', "writes the file tag"),
        # The same frame reached by an indirection the .add form would miss.
        ("frame = TBPM(encoding=3, text='124')\n", "TBPM tempo frame"),
        ("frames = [TBPM(text=str(b)) for b in values]\n", "TBPM tempo frame"),
        ("tags.update({'bpm': 124})\n", "mapping carrying the tempo key"),
    ],
)
def test_the_source_scan_catches_each_way_of_writing_a_grid(source, expect):
    problems = beatgrid_emission_violations(source, "cratekit.intake.collection_xml")
    assert any(expect in p for p in problems), f"{expect!r} not caught; got {problems}"


@pytest.mark.parametrize("container_key", ["BPM", "TBPM", "tmpo"])
def test_every_container_spelling_of_tempo_is_covered(container_key):
    """One spelling per container, and the guard must know all of them.

    Asserted separately from the table above because the failure this prevents
    is not "somebody wrote a tempo tag", it is "somebody wrote a tempo tag in
    the one container whose spelling the guard had never heard of". That is
    what happened: the MP4 atom is four lowercase letters resembling nothing
    else on the list, so a key set assembled by intuition omits it.
    """
    problems = beatgrid_emission_violations(
        f'tags[{container_key!r}] = value\n', "cratekit.intake.collection_xml"
    )
    assert problems, f"{container_key!r} is a tempo tag in some container and is not caught"


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
