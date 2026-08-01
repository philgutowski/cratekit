"""R17, the one rule with no configuration flag: nothing here writes a beat grid.

Beat grids belong to rekordbox and to nobody else. This is not a preference, it
is not tunable, and there is no profile in which it relaxes. The reason is not
squeamishness about touching the database, it is that a wrong grid is worse than
no grid: the detector octave-folds, so a "helpful" BPM seeds a grid at half or
double time, and every cue point and every loop the user has ever set against
that track moves. Import gridless and rekordbox derives BPM and grid from the
audio alone, which it is good at and which is reversible.

R17 has five surfaces, and this file guards all five:

1. **A ``<TEMPO>`` element in COLLECTION XML.** The element rekordbox reads as a
   grid. No emitter may produce one.
2. **A real ``AverageBpm`` in COLLECTION XML.** Tracks import with
   ``AverageBpm="0.00"`` so rekordbox analyses from scratch. An interpolated
   value there is the same mistake wearing a different attribute name.
3. **A ``bpm`` or ``TBPM`` file tag.** rekordbox reads file tags on import, so a
   tag write reaches the same place by a longer route.
4. **The analysis columns of the database.** That surface is the guarded writer's
   additive whitelist, asserted in tests/test_rb_writer_guard.py.
5. **The ANLZ analysis files on disk.** Once rekordbox has analysed a track, its
   grid lives in four files beside the row: ``.DAT``, ``.EXT``, ``.2EX``, ``.3EX``.
   Those are ordinary files, so surface 4's whitelist, which governs database
   ROWS, is blind to a write here by construction. Worse, the route does not
   look like a write: pyrekordbox's ``update_content_path`` reads every ANLZ
   file for a track, mutates a tag, saves each one back, and then commits the
   database directly, bypassing the guarded writer, so a caller who meant to
   rename a file rewrites its analysis. Guarded below by name, at the source
   level, because a filesystem write leaves no row to whitelist.

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

# Symbols that serialise an ANLZ file, or that call one that does. Naming any of
# them anywhere under src/ is the violation.
#
# The reason this is a separate rule rather than another tempo key: after
# analysis, a track's grid lives in four files beside the audio, and those are
# ordinary files. The guarded writer's additive whitelist governs database ROWS,
# so it is blind to a filesystem write by construction, and no amount of
# tightening it would help.
#
# `AnlzFile` is the serialiser itself: `build()` renders the struct to bytes and
# `save(path)` opens that path "wb" and writes them, so an instance under any
# name is a write primitive in hand.
#
# The other two are the reachable route, and they are worse than the primitive
# because they do not look like writes. In pyrekordbox 0.4.4,
# `pyrekordbox/db6/database.py`'s `update_content_path` reads every ANLZ file
# for a track, calls `set_path` on each, saves each one back to disk, and then
# calls `self.commit()` DIRECTLY, bypassing the guarded commit entirely.
# `update_content_filename` just below it delegates to that same method. So a
# caller who only meant to rename a file writes four analysis files and commits
# the database outside the whitelist, and nothing in the row guard can see it.
FORBIDDEN_ANLZ_SYMBOLS = frozenset(
    {
        "AnlzFile",                  # the serialiser: build() then save(path)
        "update_content_path",       # saves every ANLZ file, then commits unguarded
        "update_content_filename",   # delegates to update_content_path
        # THE GRID SETTERS THEMSELVES, which close a hole the first three left.
        # ``read_anlz_files`` is legal and returns LIVE AnlzFile objects, so a
        # caller could take one, reach its PQTZ tag, rewrite the beat grid, and
        # save it without naming any of the three names above. Forbidding the
        # setters closes that path without forbidding reading, which is the line
        # this file draws everywhere else. Derived from the binding: these are
        # every ``set*`` method on every ANLZ tag class in pyrekordbox 0.4.4, and
        # a test asserts that derivation still holds, so a binding that adds a
        # fifth setter fails here rather than opening the hole again.
        "set_bpms",
        "set_beats",
        "set_times",
    }
)

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


# ═══════════════════════════════════════════════════════════════════════════
# Surface five: no module in the package writes an ANLZ file. Runs today.
# ═══════════════════════════════════════════════════════════════════════════


def anlz_write_violations(source: str, module: str) -> list[str]:
    """Return one message per ANLZ-writing symbol named in ``source``.

    Kept separate from ``beatgrid_emission_violations`` on purpose. The two
    rules fail differently and are fixed differently: a tempo tag is a value
    somebody chose to write, while an ANLZ write is usually a side effect of
    calling something that sounded like a rename. Merging them would produce
    one scanner whose failure message could not tell you which rule you broke.

    Three node kinds carry a name, and all three are checked:

    * ``ast.Name``, the bare symbol, which covers ``AnlzFile.parse_file(p)`` and
      any call to a module-level ``update_content_path``;
    * ``ast.Attribute``, which covers ``db.update_content_path(...)`` and the
      same method reached through an intermediate variable, because the
      attribute access itself is the node, not the call around it;
    * ``ast.ImportFrom``, because ``from pyrekordbox.anlz import AnlzFile``
      binds the name through an ``alias`` node that is neither of the above.

    What this deliberately does NOT match is a string. Every message, docstring
    and comment naming these symbols, including this one, is an ``ast.Constant``
    or is not in the tree at all, so prose explaining the rule can never trip
    it. A guard that fired on the sentence describing it would be suppressed
    within a week, and a suppressed guard protects nothing.

    Reading stays legal, exactly as it does for a BPM tag. ``get_anlz_paths``,
    ``get_anlz_path``, ``read_anlz_file``, ``read_anlz_files`` and
    ``is_anlz_file`` are absent from the forbidden set by decision, not by
    oversight: R17 is about writing a tempo, and a package that may not even
    look at an analysis file cannot tell whether a track has been analysed.
    """
    problems: list[str] = []
    tree = ast.parse(source)

    def flag(symbol: str) -> None:
        problems.append(
            f"{module}: names {symbol!r}, which writes an ANLZ file to disk; the "
            f"beat grid lives in those files, they are rekordbox-authored, and "
            f"the database whitelist governs rows so it cannot see this (R17)"
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in FORBIDDEN_ANLZ_SYMBOLS:
            flag(node.id)
        elif isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_ANLZ_SYMBOLS:
            flag(node.attr)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name in FORBIDDEN_ANLZ_SYMBOLS:
                    flag(alias.name)

    return problems


def test_no_module_in_the_package_writes_an_anlz_file():
    """The live half of surface five. Green today, and green is the point.

    Walks the same derived module set as the tempo scan rather than a list of
    modules to check, so the next module added to the package is covered on the
    day it is added and nobody has to remember to add it here.
    """
    problems: list[str] = []
    for module, source in _package_modules():
        problems += anlz_write_violations(source, module)
    assert not problems, "R17 ANLZ violations:\n" + "\n".join(problems)


@pytest.mark.parametrize(
    "source, expect",
    [
        # The serialiser reached directly. `parse_file` remembers the path it
        # read, so the bare `save()` with no argument overwrites that file.
        ("AnlzFile.parse_file(p).save()\n", "AnlzFile"),
        # The import that binds the name, which no Name or Attribute node sees.
        ("from pyrekordbox.anlz import AnlzFile\n", "AnlzFile"),
        # An alias does not launder it.
        ("from pyrekordbox.anlz import AnlzFile as _AF\n", "AnlzFile"),
        # The route that does not look like a write at all: this saves every
        # ANLZ file for the track and then commits the database unguarded.
        ("db.update_content_path(cid, p)\n", "update_content_path"),
        ("db.update_content_filename(cid, name)\n", "update_content_filename"),
        # Reached through an intermediate variable. The attribute access is the
        # violation, so deferring the call changes nothing.
        ("rename = db.update_content_path\nrename(cid, p)\n", "update_content_path"),
        # And the same indirection for the serialiser itself.
        ("cls = AnlzFile\nf = cls.parse_file(p)\nf.save(q)\n", "AnlzFile"),
    ],
)
def test_the_anlz_scan_catches_each_way_of_writing_one(source, expect):
    problems = anlz_write_violations(source, "cratekit.core.rb_writer")
    assert any(expect in p for p in problems), f"{expect!r} not caught; got {problems}"


def test_prose_naming_the_forbidden_symbols_is_not_a_violation():
    """A docstring explaining the rule must not break the rule.

    This is the failure mode that retired an earlier layering pattern: it
    matched ordinary English containing a common word, so it got suppressed,
    and a suppressed guard protects nothing. Pinned as a test because the
    obvious "improvement" to the scanner, also matching string constants, would
    reintroduce it, and this goes red when it does.
    """
    source = (
        '"""Never call update_content_path: it saves every AnlzFile and then\n'
        'commits outside the guarded writer. update_content_filename too."""\n'
        "# AnlzFile.save is the primitive we refuse to name in code.\n"
        "NOTE = 'update_content_path is forbidden here'\n"
    )
    assert anlz_write_violations(source, "cratekit.core.rb_writer") == []


def test_reading_anlz_paths_is_not_a_violation():
    """Locating and parsing ANLZ files is legal. Serialising one is not.

    The same distinction the tempo scanner draws between reading a BPM tag and
    writing one. A tool that wants to know whether a track has been analysed,
    or where its analysis lives, has to look, and a guard that forbade looking
    would be routed around within a week, which is worse than no guard.
    """
    source = (
        "paths = db.get_anlz_paths(content)\n"
        "files = db.read_anlz_files(cid)\n"
        "one = db.read_anlz_file(cid, 'DAT')\n"
        "where = db.get_anlz_path(content, 'EXT')\n"
        "if is_anlz_file(candidate):\n"
        "    pass\n"
    )
    assert anlz_write_violations(source, "cratekit.core.analysis_state") == []


def test_the_forbidden_setters_are_every_setter_the_binding_offers():
    """P4. A derived set must be derived completely, or it is a list in disguise.

    The three setter names are a claim about pyrekordbox's ANLZ tag API. Checked
    against the binding at run time, so a version that adds a fourth way to write
    a grid fails here rather than quietly leaving the hole open. Nothing about
    this asserts the AnlzFile names, which are a different claim.
    """
    import inspect as _inspect

    from pyrekordbox.anlz import tags as anlz_tags

    offered = {
        method
        for name in dir(anlz_tags)
        if _inspect.isclass(getattr(anlz_tags, name)) and "Tag" in name
        for method in dir(getattr(anlz_tags, name))
        if method.startswith("set_")
    }
    assert offered, "found no setters on the binding's tag classes; the walk is broken"

    missing = sorted(offered - FORBIDDEN_ANLZ_SYMBOLS)
    assert not missing, (
        f"pyrekordbox offers {missing} to write ANLZ tag data and the scan does not "
        "forbid them, so a grid could be rewritten through a handle the binding returns"
    )


def test_the_grid_setter_route_is_caught(tmp_path):
    """The exact path the first three names left open.

    Read the files, which is legal, then rewrite the grid through the tag and
    save. It names no forbidden AnlzFile symbol, so only the setters catch it.
    """
    source = (
        "def repoint(db, cid, bpms):\n"
        "    files = db.read_anlz_files(cid)\n"
        "    for path, f in files.items():\n"
        "        f.get_tag('PQTZ').set_bpms(bpms)\n"
        "        f.save(path)\n"
    )
    assert anlz_write_violations(source, "cratekit.probe")


def test_reading_and_saving_nothing_is_still_allowed():
    """P7 again, on the widened set. Reading stays legal, all the way through."""
    source = (
        "def report(db, cid):\n"
        "    files = db.read_anlz_files(cid)\n"
        "    return {p: f.get_tag('PQTZ') for p, f in files.items()}\n"
    )
    assert anlz_write_violations(source, "cratekit.probe") == []
