"""The Location primitives: the composition-form rule and the KTD27 emitter invariant.

Two properties are under test and they fail in opposite directions.

The COMPARISON rule fails by reporting a present file as absent, which is how 144
still-referenced accented files were deleted. Every test here that compares two
spellings of one name is guarding that.

The EMITTER rule (KTD27) fails by reporting an absent file as present, or rather
by making rekordbox create a second collection row instead of matching the
existing one. An emitted ``Location`` that differs from rekordbox's own output by
a single byte is enough. So the character-class table below is exhaustive rather
than illustrative: it pins every printable ASCII character as literal or encoded,
so that widening or narrowing the safe set fails loudly instead of producing
duplicate rows in somebody's library six months later.

ON FIXTURES. Nothing here is copied from a real library. The plan forbids
shipping a real export string or a real catalog identifier even in a test, and
the property under test is the encoding RULE rather than any particular string.
The synthetic names below are built to exercise exactly the character classes
that matter: a space, a literal exclamation mark, an ampersand, an apostrophe,
and an accented character in both composition forms.

The rule these fixtures stand in for WAS verified against real output. The
encoder reproduces all 10,070 ``Location`` values in a live rekordbox export
byte for byte, and that measurement is what corrected two defects in the ported
encoder: uppercase percent escapes where rekordbox writes lowercase, and ``#``
encoded where rekordbox writes it literally.
"""

from __future__ import annotations

import ast
import string
import unicodedata
from pathlib import Path

import pytest

from cratekit.core.locations import (
    REKORDBOX_SAFE_CHARS,
    LocationDecodeError,
    PrefixRule,
    Resolution,
    leading_prefix,
    location_to_path,
    location_url,
    looks_like_location,
    norm_for_compare,
    resolve_recorded_path,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

# Third-party source, vendored because its upstream was deleted (KTD4). Excluded
# from the one-decoder guard below and from nothing else. See the comment at the
# exclusion for why that asymmetry is deliberate rather than convenient.
_VENDOR_ROOT = SRC_ROOT / "cratekit" / "_vendor"

# One synthetic filename spelled two ways.
#   composed:   LATIN SMALL LETTER E WITH ACUTE, U+00E9
#   decomposed: LATIN SMALL LETTER E, U+0065, then COMBINING ACUTE ACCENT, U+0301
# Same name to a human, same file on disk, different codepoint sequences to ==.
NFC_STEM = "Caf\u00e9 Session"
NFD_STEM = "Cafe\u0301 Session"

# The character-class golden. Every class that has ever mattered, in one name:
# a space, an apostrophe, an ampersand, a literal exclamation mark, an accent.
GOLDEN_STEM = "It's Set 01 - Caf\u00e9 & Friends!"
GOLDEN_ROOT = "/Volumes/Library/Music"
GOLDEN_LOCATION = (
    "file://localhost/Volumes/Library/Music/"
    "It%27s%20Set%2001%20-%20Caf%c3%a9%20%26%20Friends!.flac"
)


# ═══════════════════════════════════════════════════════════════════════════
# The composition-form rule
# ═══════════════════════════════════════════════════════════════════════════


def test_the_two_spellings_are_not_equal_without_normalization():
    """The premise. If this ever passes, nothing else in this file is needed.

    Asserted explicitly because the bug is invisible in a terminal: the two
    strings PRINT identically. Somebody debugging the orphan sweep looked at
    both, saw the same name twice, and concluded the comparison was fine.
    """
    assert NFD_STEM != NFC_STEM
    assert len(NFD_STEM) == len(NFC_STEM) + 1


def test_nfd_and_nfc_converge():
    assert norm_for_compare(NFD_STEM) == norm_for_compare(NFC_STEM)
    assert norm_for_compare(NFD_STEM) == NFC_STEM


def test_ascii_is_untouched():
    plain = "/Volumes/Library/Music/Set 01 - Track.flac"
    assert norm_for_compare(plain) == plain


def test_normalization_is_idempotent():
    once = norm_for_compare(NFD_STEM)
    assert norm_for_compare(once) == once


def test_a_path_differing_only_by_composition_form_compares_equal():
    """The plan's test scenario, stated as the set-membership operation that failed.

    A set is what the orphan sweep actually used. Equality is the same question
    with a friendlier failure mode.
    """
    on_disk = f"{GOLDEN_ROOT}/{NFD_STEM}.flac"
    from_export = f"{GOLDEN_ROOT}/{NFC_STEM}.flac"
    assert norm_for_compare(on_disk) == norm_for_compare(from_export)
    assert norm_for_compare(on_disk) in {norm_for_compare(from_export)}


def test_a_path_differing_by_content_does_not_compare_equal():
    """The other half, and the half that makes the guard worth having.

    A normalizer that made everything equal would also pass the test above. This
    is what stops somebody "fixing" a future failure by loosening the rule until
    two genuinely different files match, which would move the damage from
    deleting a present file to deleting the wrong one.
    """
    one = norm_for_compare(f"{GOLDEN_ROOT}/{NFC_STEM}.flac")
    other = norm_for_compare(f"{GOLDEN_ROOT}/{NFC_STEM} (Remix).flac")
    assert one != other


def test_case_only_differences_are_not_normalized_away():
    """A documented NON-property, asserted so nobody assumes it.

    Two names differing only in case are a real collision on a case-insensitive
    volume, and this function will not report them equal. That case is covered
    by the device-and-inode proof that gates a deletion. An implementer who
    assumes the normalizer handles it ships a guard that silently passes.
    """
    assert norm_for_compare("Track.flac") != norm_for_compare("track.flac")


def test_a_decoded_location_is_always_composed():
    decoded = location_to_path(f"file://localhost{GOLDEN_ROOT}/{NFD_STEM}.flac")
    assert unicodedata.is_normalized("NFC", decoded)
    assert NFC_STEM in decoded


def test_encode_then_decode_converges_across_forms():
    """Both spellings of one filename decode to the same path. That IS the fix."""
    from_nfd = location_to_path(location_url(Path(f"{GOLDEN_ROOT}/{NFD_STEM}.flac")))
    from_nfc = location_to_path(location_url(Path(f"{GOLDEN_ROOT}/{NFC_STEM}.flac")))
    assert from_nfd == from_nfc == f"{GOLDEN_ROOT}/{NFC_STEM}.flac"


def test_the_encoder_emits_one_location_for_both_composition_forms():
    """The KTD27 defect the ported encoder carried, made executable.

    The source encoder percent-encoded whatever form it was handed, so a
    decomposed on-disk name produced ``Cafe%cc%81`` while rekordbox's own export
    of that same file said ``Caf%c3%a9``. One file, two Location strings, and by
    KTD27 a byte mismatch is what makes rekordbox create a duplicate row instead
    of matching the existing one.
    """
    nfd = location_url(Path(f"{GOLDEN_ROOT}/{NFD_STEM}.flac"))
    nfc = location_url(Path(f"{GOLDEN_ROOT}/{NFC_STEM}.flac"))
    assert nfd == nfc
    assert "%cc%81" not in nfd, "a combining accent leaked into the emitted Location"
    assert "%c3%a9" in nfd


# ═══════════════════════════════════════════════════════════════════════════
# KTD27: the emitted Location is byte-identical to rekordbox's own
# ═══════════════════════════════════════════════════════════════════════════


def test_the_character_class_golden_round_trips_byte_for_byte():
    """Space, apostrophe, ampersand, literal ``!``, and an accent, in one name."""
    path = f"{GOLDEN_ROOT}/{GOLDEN_STEM}.flac"
    assert location_url(Path(path)) == GOLDEN_LOCATION
    assert location_to_path(GOLDEN_LOCATION) == path


def test_an_emitted_location_is_pure_ascii():
    """Non-ASCII must arrive as percent-encoded UTF-8 bytes, never raw.

    A raw multibyte character in the attribute would still be valid XML, so
    nothing downstream would complain. It would simply not match the row
    rekordbox wrote, which is the failure this whole section exists to prevent.
    """
    emitted = location_url(Path(f"{GOLDEN_ROOT}/{NFD_STEM}.flac"))
    assert emitted.isascii()
    emitted.encode("ascii")  # raises rather than asserting, if the above regresses


@pytest.mark.parametrize(
    "character, expected",
    [(c, c) for c in string.ascii_letters + string.digits + REKORDBOX_SAFE_CHARS]
    + [
        (" ", "%20"),
        ('"', "%22"),
        ("%", "%25"),
        ("&", "%26"),
        ("'", "%27"),
        ("<", "%3c"),
        (">", "%3e"),
        ("?", "%3f"),
        ("[", "%5b"),
        ("\\", "%5c"),
        ("]", "%5d"),
        ("^", "%5e"),
        ("`", "%60"),
        ("{", "%7b"),
        ("|", "%7c"),
        ("}", "%7d"),
    ],
)
def test_every_printable_ascii_character_is_pinned_literal_or_encoded(character, expected):
    """The exhaustive table. An edit to the safe set fails HERE, not in a library.

    Two entries carry most of the weight. The space must encode and the ``!``
    must not, which is the pair KTD27 names and the pair that separates
    rekordbox's rule from every off-the-shelf URL quoter. The lowercase hex is
    the second: rekordbox writes ``%3c``, Python's ``quote`` writes ``%3C``, and
    that difference alone failed 711 of 10,070 real rows.
    """
    assert location_url("/" + character) == "file://localhost/" + expected


def test_the_printable_ascii_table_is_exhaustive():
    """A character with no row above is a character nobody decided about.

    Without this, adding a character to the safe set and forgetting to add its
    row leaves it silently unpinned, which is the same as not having the table.
    """
    covered = set(string.ascii_letters + string.digits + REKORDBOX_SAFE_CHARS)
    covered |= set(" \"%&'<>?[\\]^`{|}")
    printable = set(string.printable) - set("\t\n\r\x0b\x0c")
    assert printable == covered, f"unpinned printable ASCII: {sorted(printable - covered)}"


def test_percent_escapes_are_lowercase():
    """Measured, not assumed: all 144,350 escapes in a live export are lowercase."""
    emitted = location_url(Path(f"{GOLDEN_ROOT}/{NFC_STEM} & More.flac"))
    assert "%C3" not in emitted and "%c3" in emitted
    assert "%26" in emitted


def test_the_hash_character_stays_literal():
    """rekordbox writes ``#`` raw. The ported encoder wrote ``%23`` and was wrong.

    Nineteen real rows failed on this alone, all of them tracks whose title
    carries a numbering like ``Untitled #2``.
    """
    assert location_url("/x/Untitled #2.flac") == "file://localhost/x/Untitled%20#2.flac"


def test_a_literal_percent_in_a_filename_survives_the_round_trip():
    """The escape-lowercasing pass must not reach into ordinary filename text.

    A name containing the text ``%C3`` encodes its ``%`` to ``%25`` and leaves
    ``C3`` as ordinary characters. Lowercasing those would rename the file.
    """
    path = "/x/100%C3 Mix.flac"
    assert location_to_path(location_url(path)) == path


# ═══════════════════════════════════════════════════════════════════════════
# Decoding: the shapes rekordbox has actually written
# ═══════════════════════════════════════════════════════════════════════════


def test_both_url_spellings_decode():
    """rekordbox has shipped both. A decoder that knows one silently drops the other."""
    assert location_to_path("file://localhost/x/a%20b.flac") == "/x/a b.flac"
    assert location_to_path("file:///x/a%20b.flac") == "/x/a b.flac"


def test_a_plain_path_containing_percent_twenty_is_not_decoded():
    """The trap in the ported decoder's fallback branch.

    ``/x/50%20off.flac`` is a real filename a real person has. Percent-decoding
    it produces ``/x/50 off.flac``, a path that does not exist, and the caller
    reports a present file as missing. The source system patched this in ONE
    caller; here it lives in the primitive, because the caller that forgets is
    the one that causes the incident.
    """
    assert location_to_path("/x/50%20off.flac") == "/x/50%20off.flac"


def test_a_streaming_pseudo_location_passes_through_untouched():
    """Not every Location is a path. A collection holds streamed rows too."""
    assert location_to_path("/v4/catalog/tracks/17477108/") == "/v4/catalog/tracks/17477108/"


def test_a_non_localhost_authority_is_refused_rather_than_mangled():
    """Refusing beats guessing.

    The ported decoder fell through and returned ``file://host/x.flac`` as if it
    were a filesystem path. The caller then failed an existence check and
    reported a missing FILE, so the cause and the symptom had nothing to do with
    each other and the real cause was invisible.
    """
    with pytest.raises(LocationDecodeError, match="not this machine"):
        location_to_path("file://otherhost/x/a%20b.flac")


def test_looks_like_location_separates_a_url_from_a_path():
    assert looks_like_location("file://localhost/x.flac")
    assert not looks_like_location("/x/50%20off.flac")


# ═══════════════════════════════════════════════════════════════════════════
# The Windows seam (R1)
# ═══════════════════════════════════════════════════════════════════════════


def test_a_backslash_on_posix_is_a_filename_character_and_is_encoded():
    """The two platforms disagree about what a backslash MEANS, so it is a seam.

    On POSIX a backslash is an ordinary character in a filename and must survive
    as ``%5c``. Silently converting it to a separator would rewrite the path.
    """
    assert location_url("/x/a\\b.flac", separator="/") == "file://localhost/x/a%5cb.flac"


def test_the_windows_separator_becomes_a_url_separator():
    """The other half of the same seam, exercised from a POSIX machine.

    Adding Windows should be a new argument to this function, not a rewrite of
    the encoder. Passing the separator explicitly is what proves that, before
    anybody actually runs this on Windows.
    """
    emitted = location_url("C:\\Music\\Set 01.flac", separator="\\")
    assert emitted == "file://localhost/C:/Music/Set%2001.flac"


# ═══════════════════════════════════════════════════════════════════════════
# The volume prefix map
# ═══════════════════════════════════════════════════════════════════════════

CURRENT_ROOT = "/Volumes/Library"
LEGACY_ROOT = "/Volumes/MyLibrary"


def test_a_path_already_under_the_root_resolves_as_itself():
    result = resolve_recorded_path(f"{CURRENT_ROOT}/Music/t.flac", root=CURRENT_ROOT)
    assert result.resolution is Resolution.UNDER_ROOT
    assert result.path == f"{CURRENT_ROOT}/Music/t.flac"


def test_a_configured_prefix_resolves_a_legacy_volume_path():
    """The plan's scenario. Without the map, most of a real library resolves to nothing."""
    rules = [PrefixRule(LEGACY_ROOT, CURRENT_ROOT)]
    result = resolve_recorded_path(f"{LEGACY_ROOT}/Music/t.flac", root=CURRENT_ROOT,
                                   prefix_map=rules)
    assert result.resolution is Resolution.REMAPPED
    assert result.path == f"{CURRENT_ROOT}/Music/t.flac"
    assert result.rule_index == 0


def test_an_unmapped_prefix_is_reported_and_never_guessed():
    """The other half of the plan's scenario, and the half with teeth.

    No path comes back at all, so a caller cannot accidentally treat an
    unresolved row as a resolved one. The prefix DOES come back, because the
    doctor check groups rows by it and shows the user "these rows record this
    prefix" instead of one failure per row.
    """
    result = resolve_recorded_path("/Volumes/MusicLibrary/x/t.flac", root=CURRENT_ROOT)
    assert result.resolution is Resolution.UNMAPPED
    assert result.path is None
    assert result.prefix == "/Volumes/MusicLibrary"


def test_the_rewrite_is_anchored_and_not_a_substring_replace():
    """The ported implementation used ``str.replace``, which is neither.

    ``str.replace`` rewrites EVERY occurrence anywhere in the string, so a path
    holding the old volume name deeper down comes back corrupted while reporting
    success. Corrupted-but-confident is worse than unresolved.
    """
    rules = [PrefixRule(LEGACY_ROOT, CURRENT_ROOT)]
    nested = f"{CURRENT_ROOT}/Music/Archive{LEGACY_ROOT}/t.flac"
    result = resolve_recorded_path(nested, root=CURRENT_ROOT, prefix_map=rules)
    assert result.resolution is Resolution.UNDER_ROOT
    assert result.path == nested


def test_a_sibling_sharing_a_string_prefix_does_not_match():
    """A rule for one volume must not swallow another whose name extends it.

    A drive and a drive whose name is that name plus a suffix are two different
    volumes that happen to share leading characters. Rewriting the second on the
    first's rule produces a path pointing at nothing while reporting success.
    """
    rules = [PrefixRule(LEGACY_ROOT, CURRENT_ROOT)]
    result = resolve_recorded_path(f"{LEGACY_ROOT}Archive/t.flac", root=CURRENT_ROOT,
                                   prefix_map=rules)
    assert result.resolution is Resolution.UNMAPPED


def test_the_map_is_ordered_and_the_first_match_wins():
    """Order is load-bearing because one prefix can be another's prefix.

    An unordered mapping resolves this pair differently depending on iteration
    order, which is a bug that appears and disappears between runs.
    """
    rules = [
        PrefixRule(f"{LEGACY_ROOT}/Music", f"{CURRENT_ROOT}/Audio"),
        PrefixRule(LEGACY_ROOT, CURRENT_ROOT),
    ]
    result = resolve_recorded_path(f"{LEGACY_ROOT}/Music/t.flac", root=CURRENT_ROOT,
                                   prefix_map=rules)
    assert result.rule_index == 0
    assert result.path == f"{CURRENT_ROOT}/Audio/t.flac"


def test_a_rule_matches_a_prefix_written_in_either_composition_form():
    """A volume named with an accent is ordinary, and the user types one form.

    Normalizing both the rule and the path removes the question of whether the
    rewrite happens before or after normalization: the answer stops mattering.
    """
    legacy_nfd = "/Volumes/" + NFD_STEM
    legacy_nfc = "/Volumes/" + NFC_STEM
    rules = [PrefixRule(legacy_nfd, CURRENT_ROOT)]
    result = resolve_recorded_path(f"{legacy_nfc}/t.flac", root=CURRENT_ROOT,
                                   prefix_map=rules)
    assert result.resolution is Resolution.REMAPPED
    assert result.path == f"{CURRENT_ROOT}/t.flac"


def test_resolution_does_not_check_existence():
    """Kept apart on purpose, because deletion needs the two categories separate.

    The ported resolver returned None for BOTH "no rule maps this prefix" and
    "the file is gone". One is a configuration error and one may be a file the
    user is about to be asked to move to the Trash.
    """
    result = resolve_recorded_path(f"{CURRENT_ROOT}/nothing/here.flac", root=CURRENT_ROOT)
    assert result.resolution is Resolution.UNDER_ROOT
    assert result.path == f"{CURRENT_ROOT}/nothing/here.flac"


def test_a_non_absolute_recorded_path_is_its_own_category():
    """Device-relative and streaming rows are not failures and are not paths."""
    result = resolve_recorded_path("contents/x.flac", root=CURRENT_ROOT)
    assert result.resolution is Resolution.NOT_A_PATH
    assert result.path is None


def test_leading_prefix_names_no_platform_mount_root():
    """Reporting counts components rather than naming a platform's mount root."""
    assert leading_prefix("/media/library/x/t.flac") == "/media/library"
    assert leading_prefix("/Volumes/Library/x/t.flac") == "/Volumes/Library"
    assert leading_prefix("relative/x.flac") is None


# ═══════════════════════════════════════════════════════════════════════════
# The drift guard: exactly one decoder in the package
# ═══════════════════════════════════════════════════════════════════════════

#: The four call names that encode or decode a Location, by name alone.
_LOCATION_CODEC_CALLS = frozenset({"unquote", "unquote_plus", "quote", "quote_plus"})

#: The one call in our own tree that wears this shape and is not this shape,
#: as (module, function). Narrow on BOTH axes on purpose, so the day
#: ``searchers.py`` decodes something it is still reported.
#:
#: U56's catalogue searcher builds a SEARCH QUERY STRING for three public
#: record catalogues, ``?q=artist+title``. It is the same distinction this
#: guard's vendored-tree paragraph below already draws, now arriving in code
#: we wrote: that module never sees a rekordbox Location, has no concept of
#: one, and cannot reach the code that does. What makes the exemption safe to
#: state this narrowly rather than merely plausible is the function itself.
#: ``quote_plus`` encodes a space as ``+``, which is a query-string
#: convention and is WRONG for a path: a Location encoder written with it
#: would corrupt every file whose name has a space, which is most of a music
#: library. So this call cannot be the seventh copy of the decoder even by
#: accident. The four-name scan cannot see that, and widening it to reason
#: about intent would make it a thing nobody trusts.
#:
#: The alternative, spelling the same encoding as ``urlencode`` so the scan
#: does not match the name, is what P7 calls training people to route around
#: a guard. Stating the exemption where it can be read is the honest form.
_PERMITTED_CODEC_CALLS = frozenset({("cratekit/tagging/searchers.py", "quote_plus")})


def _location_codec_offenders(root: Path) -> list[str]:
    """Every call outside the one decoder that encodes or decodes a Location.

    One line per offending call, ``<path relative to root> calls <name>()``,
    in sorted file order and walk order within a file. ``root`` is ``SRC_ROOT``
    for the guard and a planted tree for the tests that prove it still bites.

    The path relative to ``root`` is computed once per file, before the walk
    over its nodes (U253). Computed once per node, as it was, the guard spent
    forty seconds of a suite run in ``pathlib`` producing the same string
    hundreds of thousands of times.
    """
    vendor_root = root / "cratekit" / "_vendor"
    offenders: list[str] = []
    for path in sorted(root.rglob("*.py")):
        if path.name == "locations.py":
            continue
        # The vendored tree is out of scope for this guard, and only for this
        # guard. It is third-party source we did not author and do not restyle,
        # and the rule here is about OUR architectural discipline: one decoder,
        # so a seventh copy cannot drift away from the composition-form
        # handling. The vendored downloader does call unquote, twice, but on an
        # HTTP download URL to derive a filename. It never sees a rekordbox
        # Location, has no concept of one, and cannot reach the code that does.
        #
        # This distinction is the point, so it is worth stating plainly: a
        # guard about how WE choose to organize code stops at code we wrote,
        # while a guard about SAFETY or about what ships must cover everything,
        # vendored trees included. The beatgrid guard, the secret scan, and the
        # personal-literal scan all deliberately reach in here, and the vendored
        # downloader is exactly why: it arrived writing a tempo tag in three
        # containers and carrying live third-party credentials. Adding this
        # exclusion to one of those would undo the reason they exist.
        if vendor_root in path.parents:
            continue
        relative = path.relative_to(root).as_posix()
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            called = None
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    called = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    called = node.func.attr
            if called in _LOCATION_CODEC_CALLS and (relative, called) not in _PERMITTED_CODEC_CALLS:
                offenders.append(f"{relative} calls {called}()")
    return offenders


def test_no_module_outside_this_one_decodes_a_location_itself():
    """Six copies of this decoder drifted apart once. This is what stops a seventh.

    The consolidation in the source system was real but incomplete: two hand
    rolled decoders survived it, and one of them omitted the composition-form
    normalization entirely, which is the exact shape that cost 144 files. A
    reviewer will not catch the eighth copy. A test will.
    """
    offenders = _location_codec_offenders(SRC_ROOT)
    assert not offenders, (
        "Location encoding and decoding live in cratekit.core.locations and "
        "nowhere else:\n" + "\n".join(offenders)
    )


def _plant(root: Path, relative: str, source: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source)


def test_the_sweep_still_reports_a_planted_decoder_by_its_relative_path(tmp_path):
    """The guard bites: a module that decodes for itself is named, path and call."""
    _plant(
        tmp_path,
        "cratekit/library/planted.py",
        "from urllib.parse import unquote_plus\n\n"
        "def decode(value):\n    return unquote_plus(value)\n",
    )
    _plant(tmp_path, "cratekit/library/clean.py", "def nothing():\n    return 1\n")

    assert _location_codec_offenders(tmp_path) == [
        "cratekit/library/planted.py calls unquote_plus()"
    ]


def test_the_sweep_reports_every_name_in_both_call_shapes_and_every_call(tmp_path):
    """Each of the four names, called bare or as an attribute, once per call."""
    _plant(
        tmp_path,
        "cratekit/a.py",
        "import urllib.parse as parse\n"
        "from urllib.parse import quote, unquote\n\n"
        "def f(v):\n"
        "    unquote(v)\n"
        "    unquote(v)\n"
        "    parse.quote_plus(v)\n"
        "    return quote(v)\n",
    )
    _plant(
        tmp_path,
        "cratekit/b/c.py",
        "import shlex\n\ndef g(v):\n    return shlex.quote(v)\n",
    )

    offenders = _location_codec_offenders(tmp_path)

    assert sorted(offenders) == sorted(
        [
            "cratekit/a.py calls unquote()",
            "cratekit/a.py calls unquote()",
            "cratekit/a.py calls quote_plus()",
            "cratekit/a.py calls quote()",
            "cratekit/b/c.py calls quote()",
        ]
    )


def test_the_permitted_quote_plus_is_excused_and_nothing_else_is(tmp_path):
    """The exemption covers one call name in one module, on both axes."""
    _plant(
        tmp_path,
        "cratekit/tagging/searchers.py",
        "from urllib.parse import quote_plus, unquote\n\n"
        "def q(v):\n    return quote_plus(v), unquote(v)\n",
    )
    _plant(
        tmp_path,
        "cratekit/tagging/other.py",
        "from urllib.parse import quote_plus\n\ndef q(v):\n    return quote_plus(v)\n",
    )
    _plant(
        tmp_path,
        "searchers.py",
        "from urllib.parse import quote_plus\n\ndef q(v):\n    return quote_plus(v)\n",
    )

    assert sorted(_location_codec_offenders(tmp_path)) == [
        "cratekit/tagging/other.py calls quote_plus()",
        "cratekit/tagging/searchers.py calls unquote()",
        "searchers.py calls quote_plus()",
    ]


def test_the_sweep_skips_the_decoder_and_the_vendored_tree_and_nothing_beside_them(
    tmp_path,
):
    """locations.py and the vendored tree are excluded, their lookalikes are not."""
    call = "from urllib.parse import unquote\n\ndef f(v):\n    return unquote(v)\n"
    _plant(tmp_path, "cratekit/core/locations.py", call)
    _plant(tmp_path, "cratekit/_vendor/downloader/fetch.py", call)
    _plant(tmp_path, "cratekit/_vendor/top.py", call)
    _plant(tmp_path, "cratekit/_vendored/fetch.py", call)
    _plant(tmp_path, "cratekit/core/_vendor/fetch.py", call)
    _plant(tmp_path, "cratekit/core/locations_extra.py", call)

    assert _location_codec_offenders(tmp_path) == [
        "cratekit/_vendored/fetch.py calls unquote()",
        "cratekit/core/_vendor/fetch.py calls unquote()",
        "cratekit/core/locations_extra.py calls unquote()",
    ]


def test_the_sweep_computes_each_relative_path_once_per_file(tmp_path, monkeypatch):
    """U253's proof is a count: one ``relative_to`` per file swept, not per node.

    Computed per node, the guard made 834,825 calls for 311 files and took
    forty seconds of every suite run. The files planted here have hundreds of
    nodes each, so a per node computation is read as hundreds of calls.
    """
    body = "".join(f"x{n} = [{n}, {n} + 1, ({n},)]\n" for n in range(100))
    for name in ("one", "two", "three"):
        _plant(tmp_path, f"cratekit/{name}.py", body)
    _plant(tmp_path, "cratekit/core/locations.py", body)
    _plant(tmp_path, "cratekit/_vendor/skip.py", body)

    swept: list[Path] = []
    real = Path.relative_to

    def counting(self, *other, **kwargs):
        if other == (tmp_path,):
            swept.append(self)
        return real(self, *other, **kwargs)

    monkeypatch.setattr(Path, "relative_to", counting)

    assert _location_codec_offenders(tmp_path) == []
    assert sorted(swept) == sorted(
        tmp_path / "cratekit" / f"{name}.py" for name in ("one", "two", "three")
    )


def test_the_one_permitted_call_is_still_there_and_is_still_a_query_string():
    """An exemption for a call nobody makes is an exemption nobody maintains.

    The guard above names one permitted pair. If the searcher stops calling
    ``quote_plus``, or the file moves, the exemption silently starts covering
    nothing while still reading as a live carve-out, and the next author who
    needs one adds a second beside it. So the pair is asserted to still match
    something, and the call is asserted to still be what the exemption says it
    is: a query string, built against a URL that names a public catalogue, and
    never a path under the library.
    """
    source = (SRC_ROOT / "cratekit" / "tagging" / "searchers.py").read_text()
    calls = [
        node
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "quote_plus"
    ]
    assert calls, (
        "the permitted quote_plus call is gone, so the exemption in the guard "
        "above covers nothing and should be deleted with it"
    )
    assert "from urllib.parse import quote_plus" in source
    assert "https://" in source and "file://" not in source, (
        "the exempted module encodes for a catalogue URL; a file scheme here "
        "would mean it had started building a location after all"
    )


def test_the_vendor_exclusion_is_not_copied_into_the_safety_guards():
    """The guard above skips the vendored tree. The safety guards must not.

    This exists because the exclusion above is the tempting thing to copy. It
    looks like boilerplate, it silences a failure, and applying it to the
    beatgrid guard or the secret scan would silence those too, in the one place
    where they have already earned their keep.

    Concretely, on the day it was vendored, that tree wrote a tempo tag in
    three containers and carried live third-party credentials in two files. The
    beatgrid rule is not a style preference and the credential rule is not
    ours to waive on someone else's code, so both must reach in there.

    Asserted by construction rather than by reading: the beatgrid guard is
    handed a real vendored module path and must still enumerate it.
    """
    from tests.test_no_beatgrid_ever import _package_modules

    assert _VENDOR_ROOT.is_dir(), "vendored tree missing; this guard has nothing to prove"

    scanned = {module for module, _source in _package_modules()}
    vendored = {m for m in scanned if "._vendor." in m or m.endswith("._vendor")}
    assert vendored, (
        "the beatgrid guard no longer enumerates the vendored tree. If an "
        "exclusion was added there to quiet a failure, remove it and fix the "
        "vendored source instead: that tree arrived writing tempo tags in three "
        "containers, and this guard is what caught them."
    )
