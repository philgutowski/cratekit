"""The Location primitives: the composition-form rule and the KTD27 emitter invariant.

The COMPARISON rule fails by reporting a present file as absent, which is how 144
still-referenced accented files were deleted. The EMITTER rule (KTD27) fails by
making rekordbox create a second collection row: an emitted ``Location`` one byte
off its own output is enough, so the character table pins every printable ASCII
character as literal or encoded.

Nothing here is copied from a real library; the synthetic names exercise the
classes that matter. The rule WAS verified against all 10,070 ``Location``
values of a live export byte for byte, which corrected lowercase escapes and a
literal ``#`` in the ported encoder.
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
from tests.test_config import parsed

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

# Vendored third-party source (KTD4), excluded from the one-decoder guard only.
_VENDOR_ROOT = SRC_ROOT / "cratekit" / "_vendor"

# One synthetic filename spelled two ways: U+00E9, and U+0065 then U+0301.
NFC_STEM = "Caf\u00e9 Session"
NFD_STEM = "Cafe\u0301 Session"

# Space, apostrophe, ampersand, literal exclamation mark and accent, in one name.
GOLDEN_STEM = "It's Set 01 - Caf\u00e9 & Friends!"
GOLDEN_ROOT = "/Volumes/Library/Music"
GOLDEN_LOCATION = (
    "file://localhost/Volumes/Library/Music/"
    "It%27s%20Set%2001%20-%20Caf%c3%a9%20%26%20Friends!.flac"
)


# The composition-form rule.


def test_the_two_spellings_are_not_equal_without_normalization():
    """The premise, asserted because the two strings PRINT identically."""
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
    """Stated as the set membership the orphan sweep actually used."""
    on_disk = f"{GOLDEN_ROOT}/{NFD_STEM}.flac"
    from_export = f"{GOLDEN_ROOT}/{NFC_STEM}.flac"
    assert norm_for_compare(on_disk) == norm_for_compare(from_export)
    assert norm_for_compare(on_disk) in {norm_for_compare(from_export)}


def test_a_path_differing_by_content_does_not_compare_equal():
    """A normalizer making everything equal would pass the test above."""
    one = norm_for_compare(f"{GOLDEN_ROOT}/{NFC_STEM}.flac")
    other = norm_for_compare(f"{GOLDEN_ROOT}/{NFC_STEM} (Remix).flac")
    assert one != other


def test_case_only_differences_are_not_normalized_away():
    """A documented NON-property: the device-and-inode proof covers case."""
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
    """The ported encoder wrote ``Cafe%cc%81`` where rekordbox writes ``Caf%c3%a9``."""
    nfd = location_url(Path(f"{GOLDEN_ROOT}/{NFD_STEM}.flac"))
    nfc = location_url(Path(f"{GOLDEN_ROOT}/{NFC_STEM}.flac"))
    assert nfd == nfc
    assert "%cc%81" not in nfd, "a combining accent leaked into the emitted Location"
    assert "%c3%a9" in nfd


# KTD27: the emitted Location is byte-identical to rekordbox's own.


def test_the_character_class_golden_round_trips_byte_for_byte():
    """Space, apostrophe, ampersand, literal ``!``, and an accent, in one name."""
    path = f"{GOLDEN_ROOT}/{GOLDEN_STEM}.flac"
    assert location_url(Path(path)) == GOLDEN_LOCATION
    assert location_to_path(GOLDEN_LOCATION) == path


def test_an_emitted_location_is_pure_ascii():
    """Raw multibyte text is valid XML and silently matches no rekordbox row."""
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
    """An edit to the safe set fails HERE. Space encodes and ``!`` does not (KTD27);
    the hex is lowercase, which alone failed 711 of 10,070 real rows."""
    assert location_url("/" + character) == "file://localhost/" + expected


def test_the_printable_ascii_table_is_exhaustive():
    """A character with no row above is a character nobody decided about."""
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
    """rekordbox writes ``#`` raw; ``%23`` failed nineteen real rows."""
    assert location_url("/x/Untitled #2.flac") == "file://localhost/x/Untitled%20#2.flac"


def test_a_literal_percent_in_a_filename_survives_the_round_trip():
    """The escape-lowercasing pass must not reach into ordinary filename text."""
    path = "/x/100%C3 Mix.flac"
    assert location_to_path(location_url(path)) == path


# Decoding: the shapes rekordbox has actually written.


@pytest.mark.parametrize(
    "location,expected",
    [
        # rekordbox has shipped both URL spellings.
        ("file://localhost/x/a%20b.flac", "/x/a b.flac"),
        ("file:///x/a%20b.flac", "/x/a b.flac"),
        # A real filename; decoding it would report a present file as missing.
        ("/x/50%20off.flac", "/x/50%20off.flac"),
        # Not every Location is a path: a collection holds streamed rows too.
        ("/v4/catalog/tracks/17477108/", "/v4/catalog/tracks/17477108/"),
    ],
    ids=["localhost-url", "empty-authority-url", "plain-path-with-percent-twenty-untouched",
         "streaming-pseudo-location-untouched"],
)
def test_location_to_path(location, expected):
    assert location_to_path(location) == expected


def test_a_non_localhost_authority_is_refused_rather_than_mangled():
    """The ported decoder returned it as a path, so a caller reported a missing FILE."""
    with pytest.raises(LocationDecodeError, match="not this machine"):
        location_to_path("file://otherhost/x/a%20b.flac")


def test_looks_like_location_separates_a_url_from_a_path():
    assert looks_like_location("file://localhost/x.flac")
    assert not looks_like_location("/x/50%20off.flac")


# The Windows seam (R1).


def test_a_backslash_on_posix_is_a_filename_character_and_is_encoded():
    """On POSIX a backslash is a filename character and must survive as ``%5c``."""
    assert location_url("/x/a\\b.flac", separator="/") == "file://localhost/x/a%5cb.flac"


def test_the_windows_separator_becomes_a_url_separator():
    """The other half of the seam: Windows is an argument, not a rewrite."""
    emitted = location_url("C:\\Music\\Set 01.flac", separator="\\")
    assert emitted == "file://localhost/C:/Music/Set%2001.flac"


# The volume prefix map.

CURRENT_ROOT = "/Volumes/Library"
LEGACY_ROOT = "/Volumes/MyLibrary"


def test_a_path_already_under_the_root_resolves_as_itself():
    result = resolve_recorded_path(f"{CURRENT_ROOT}/Music/t.flac", root=CURRENT_ROOT)
    assert result.resolution is Resolution.UNDER_ROOT
    assert result.path == f"{CURRENT_ROOT}/Music/t.flac"


def test_a_configured_prefix_resolves_a_legacy_volume_path():
    """Without the map, most of a real library resolves to nothing."""
    rules = [PrefixRule(LEGACY_ROOT, CURRENT_ROOT)]
    result = resolve_recorded_path(f"{LEGACY_ROOT}/Music/t.flac", root=CURRENT_ROOT,
                                   prefix_map=rules)
    assert result.resolution is Resolution.REMAPPED
    assert result.path == f"{CURRENT_ROOT}/Music/t.flac"
    assert result.rule_index == 0


def test_an_unmapped_prefix_is_reported_and_never_guessed():
    """No path comes back; the prefix does, for doctor to group rows by."""
    result = resolve_recorded_path("/Volumes/MusicLibrary/x/t.flac", root=CURRENT_ROOT)
    assert result.resolution is Resolution.UNMAPPED
    assert result.path is None
    assert result.prefix == "/Volumes/MusicLibrary"


def test_the_rewrite_is_anchored_and_not_a_substring_replace():
    """``str.replace`` rewrote every occurrence, corrupting a path while reporting success."""
    rules = [PrefixRule(LEGACY_ROOT, CURRENT_ROOT)]
    nested = f"{CURRENT_ROOT}/Music/Archive{LEGACY_ROOT}/t.flac"
    result = resolve_recorded_path(nested, root=CURRENT_ROOT, prefix_map=rules)
    assert result.resolution is Resolution.UNDER_ROOT
    assert result.path == nested


def test_a_sibling_sharing_a_string_prefix_does_not_match():
    """A rule for one volume must not swallow another whose name extends it."""
    rules = [PrefixRule(LEGACY_ROOT, CURRENT_ROOT)]
    result = resolve_recorded_path(f"{LEGACY_ROOT}Archive/t.flac", root=CURRENT_ROOT,
                                   prefix_map=rules)
    assert result.resolution is Resolution.UNMAPPED


def test_the_map_is_ordered_and_the_first_match_wins():
    """Order is load-bearing because one prefix can be another's prefix."""
    rules = [
        PrefixRule(f"{LEGACY_ROOT}/Music", f"{CURRENT_ROOT}/Audio"),
        PrefixRule(LEGACY_ROOT, CURRENT_ROOT),
    ]
    result = resolve_recorded_path(f"{LEGACY_ROOT}/Music/t.flac", root=CURRENT_ROOT,
                                   prefix_map=rules)
    assert result.rule_index == 0
    assert result.path == f"{CURRENT_ROOT}/Audio/t.flac"


def test_a_rule_matches_a_prefix_written_in_either_composition_form():
    """A volume named with an accent is ordinary, and the user types one form."""
    legacy_nfd = "/Volumes/" + NFD_STEM
    legacy_nfc = "/Volumes/" + NFC_STEM
    rules = [PrefixRule(legacy_nfd, CURRENT_ROOT)]
    result = resolve_recorded_path(f"{legacy_nfc}/t.flac", root=CURRENT_ROOT,
                                   prefix_map=rules)
    assert result.resolution is Resolution.REMAPPED
    assert result.path == f"{CURRENT_ROOT}/t.flac"


def test_resolution_does_not_check_existence():
    """An unmapped prefix and a gone file are separate categories for deletion."""
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


# The drift guard: exactly one decoder in the package.

#: The four call names that encode or decode a Location, by name alone.
_LOCATION_CODEC_CALLS = frozenset({"unquote", "unquote_plus", "quote", "quote_plus"})

#: The one call that wears this shape and is not it, as (module, function),
#: narrow on both axes. U56's searcher builds a ``?q=artist+title`` query string
#: for public catalogues and never sees a Location; ``quote_plus`` encodes a space
#: as ``+``, which is wrong for a path, so it cannot be a seventh decoder even by
#: accident. Spelling it as ``urlencode`` to dodge the scan is what P7 calls
#: routing around a guard; stating the exemption is the honest form.
_PERMITTED_CODEC_CALLS = frozenset({("cratekit/tagging/searchers.py", "quote_plus")})


def _location_codec_offenders(root: Path) -> list[str]:
    """Every call outside the one decoder that encodes or decodes a Location.

    One line per call, ``<path relative to root> calls <name>()``, in sorted
    file order and walk order. The relative path is computed once per file
    (U253): once per node it cost about forty seconds of a suite run.

    A file whose text, read as Python reads identifiers (NFKC), never spells
    ``quote`` cannot call any of the four names, so it is not parsed. That
    skips most of the tree and finds exactly what a full parse would.
    """
    vendor_root = root / "cratekit" / "_vendor"
    offenders: list[str] = []
    for path in sorted(root.rglob("*.py")):
        if path.name == "locations.py":
            continue
        # The vendored tree is out of scope for this guard alone: it is about
        # how WE organize code, and the vendored downloader's two unquote calls
        # derive a filename from an HTTP URL. A SAFETY guard (beatgrid, secret
        # scan, personal literals) must reach in here; that tree arrived writing
        # tempo tags and carrying live credentials.
        if vendor_root in path.parents:
            continue
        relative = path.relative_to(root).as_posix()
        text = path.read_text()
        if "quote" not in unicodedata.normalize("NFKC", text):
            continue
        for node in ast.walk(parsed(text)):
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
    """Six copies of this decoder drifted apart once, one without the
    composition-form step that cost 144 files. This stops a seventh."""
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


def test_the_guard_itself_fails_naming_a_decoder_planted_under_its_root(tmp_path, monkeypatch):
    """The guard, not only its sweep, fails on a planted root and names the module."""
    _plant(
        tmp_path,
        "cratekit/library/planted.py",
        "from urllib.parse import unquote\n\ndef decode(value):\n    return unquote(value)\n",
    )
    monkeypatch.setitem(globals(), "SRC_ROOT", tmp_path)

    with pytest.raises(AssertionError) as raised:
        test_no_module_outside_this_one_decodes_a_location_itself()

    message = str(raised.value)
    assert message.startswith(
        "Location encoding and decoding live in cratekit.core.locations and nowhere else:\n"
    )
    assert "cratekit/library/planted.py calls unquote()" in message


@pytest.mark.parametrize("shape", ["bare", "attribute"])
@pytest.mark.parametrize("name", ["unquote", "unquote_plus", "quote", "quote_plus"])
def test_the_sweep_reports_each_name_called_bare_or_as_an_attribute(tmp_path, name, shape):
    """A literal list, not ``_LOCATION_CODEC_CALLS``, so a dropped name fails here."""
    if shape == "bare":
        source = f"from urllib.parse import {name}\n\n{name}('a%20b')\n"
    else:
        source = f"import urllib.parse\n\nurllib.parse.{name}('a%20b')\n"
    _plant(tmp_path, "cratekit/library/planted.py", source)

    assert _location_codec_offenders(tmp_path) == [f"cratekit/library/planted.py calls {name}()"]


def test_the_sweep_reports_every_call_and_reads_the_name_alone(tmp_path):
    """One line per call, two calls in one file are two lines, and the name is
    read without its owner, so ``shlex.quote`` is reported as ``quote`` is."""
    _plant(
        tmp_path,
        "cratekit/a.py",
        "from urllib.parse import unquote\n\ndef f(v):\n    unquote(v)\n    return unquote(v)\n",
    )
    _plant(
        tmp_path,
        "cratekit/b/c.py",
        "import shlex\n\ndef g(v):\n    return shlex.quote(v)\n",
    )

    assert _location_codec_offenders(tmp_path) == [
        "cratekit/a.py calls unquote()",
        "cratekit/a.py calls unquote()",
        "cratekit/b/c.py calls quote()",
    ]


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


def test_the_sweep_skips_the_decoder_and_the_vendored_tree(tmp_path):
    """Only ``cratekit/_vendor`` under the root and files named ``locations.py``
    are skipped; lookalikes are swept."""
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
    """U253's proof is a count: one ``relative_to`` per file swept, not per node
    (834,825 calls for 311 files at ``a7fcc9f4``)."""
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
    """An exemption for a call nobody makes is an exemption nobody maintains, so
    the pair still matches a call, and it still builds a catalogue query string."""
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
    """The guard above skips the vendored tree; the safety guards must not, since
    that tree arrived writing tempo tags and carrying live credentials. Asserted
    by construction: the beatgrid guard must still enumerate a vendored module."""
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
