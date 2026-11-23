"""R36: what a tombstone identifies, and the revocability both stores must have.

The deletion pass records and an acquisition pass consults without importing each
other, so both build the identity from ``cratekit.core.tombstone``. AE17 matters most,
a deleted version is suppressed while a DIFFERENT REMIX is still acquired."""

from __future__ import annotations

import unicodedata

import pytest

from cratekit.core import config, review, tombstone
from cratekit.core.cause import CratekitError
from cratekit.deletion import library, stores
from tests.test_config import valid_data

ARTIST = "A Synthesized Artist"
ORIGINAL = "A Synthesized Title"
REMIX = "A Synthesized Title (Someone Else Remix)"


@pytest.fixture
def library_root(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


@pytest.fixture
def cfg(library_root):
    return config.from_dict(valid_data(library_root))


def _row(content_id="1", *, artist=ARTIST, title=ORIGINAL, recorded="/music/x.flac"):
    return library.RemovedRow(
        content_id=content_id,
        recorded=recorded,
        sequence=10,
        size=11,
        artist=artist,
        title=title,
    )


# The identity


def test_a_remix_and_its_original_are_two_identities(cfg):
    """AE17: version identity, not recording identity, as the library is remix heavy (KTD16)."""
    assert tombstone.version_identity(artist=ARTIST, title=ORIGINAL) != (
        tombstone.version_identity(artist=ARTIST, title=REMIX)
    )


@pytest.mark.parametrize(
    "artist, title",
    [
        (ARTIST.upper(), ORIGINAL.lower()),
        (f"  {ARTIST} ", f"{ORIGINAL}  "),
        (ARTIST, ORIGINAL.replace(" ", "  ")),
    ],
)
def test_case_spacing_and_padding_are_folded(artist, title):
    """Routine differences between a row and a search result are not a different version."""
    assert tombstone.version_identity(artist=artist, title=title) == (
        tombstone.version_identity(artist=ARTIST, title=ORIGINAL)
    )


def test_composition_form_is_folded():
    """Composition form folds, as macOS and providers hand back different forms."""
    accented = "Café Track"
    assert tombstone.version_identity(artist=ARTIST, title=accented) == (
        tombstone.version_identity(
            artist=ARTIST, title=unicodedata.normalize("NFD", accented)
        )
    )


def test_punctuation_is_not_folded():
    """Conservative, since an over-eager fold silently withholds music the user wants."""
    assert tombstone.version_identity(artist=ARTIST, title="Track (Live)") != (
        tombstone.version_identity(artist=ARTIST, title="Track [Live]")
    )


def test_an_identity_with_neither_field_refuses():
    """An empty identity hashes to one value, so one deletion would suppress all."""
    with pytest.raises(CratekitError) as excinfo:
        tombstone.version_identity(artist="", title="   ")
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_the_field_set_never_varies_with_the_input():
    """An omitted empty field would hash differently and never match."""
    assert set(tombstone.version_identity(artist=ARTIST, title="")) == {"artist", "title"}
    assert set(tombstone.version_identity(artist="", title=ORIGINAL)) == {"artist", "title"}


def test_the_isrc_is_carried_in_the_payload_and_never_in_the_identity(cfg):
    """A code in the identity would miss the same version from a source without one."""
    row = library.RemovedRow(
        content_id="1",
        recorded="/music/x.flac",
        sequence=10,
        size=11,
        artist=ARTIST,
        title=ORIGINAL,
        isrc="AA6Q72000047",
    )
    record = stores.record_tombstone(cfg, row, actor="cli")
    assert "isrc" not in (record.identity or {})
    assert record.payload["isrc"] == "AA6Q72000047"
    assert stores.suppressed_version(cfg, artist=ARTIST, title=ORIGINAL)


# The stores


def test_a_tombstoned_version_is_suppressed_and_a_different_remix_is_not(cfg):
    """AE17, end to end through the store an acquisition pass actually reads."""
    stores.record_tombstone(cfg, _row(title=ORIGINAL), actor="cli")
    assert stores.suppressed_version(cfg, artist=ARTIST, title=ORIGINAL)
    assert not stores.suppressed_version(cfg, artist=ARTIST, title=REMIX)


def test_revoking_a_tombstone_makes_the_version_acquirable_again(cfg):
    record = stores.record_tombstone(cfg, _row(), actor="cli")
    assert stores.suppressed_version(cfg, artist=ARTIST, title=ORIGINAL)
    stores.revoke_tombstone(cfg, record.suppression_id, actor="cli")
    assert not stores.suppressed_version(cfg, artist=ARTIST, title=ORIGINAL)


def test_a_revoked_tombstone_stays_listable_so_the_two_cases_can_be_told_apart(cfg):
    """R36: LISTABLE and revocable, so "never suppressed" and "lifted" can be told apart."""
    record = stores.record_tombstone(cfg, _row(), actor="cli")
    stores.revoke_tombstone(cfg, record.suppression_id, actor="cli")
    assert stores.list_tombstones(cfg) == ()
    listed = stores.list_tombstones(cfg, include_revoked=True)
    assert [held.suppression_id for held in listed] == [record.suppression_id]
    assert listed[0].revoked and listed[0].revoked_by == "cli"

    # The projection a listing renders carries the revoked flag.
    row = stores.summarize(listed[0])
    assert row["revoked"] is True
    assert row["title"] == ORIGINAL and row["identity"] == f"{ARTIST.lower()} - {ORIGINAL.lower()}"


def test_recording_the_same_version_twice_changes_nothing(cfg):
    first = stores.record_tombstone(cfg, _row(), actor="cli")
    second = stores.record_tombstone(cfg, _row(content_id="2"), actor="someone-else")
    assert first == second, "a re-record moved the timestamp or the actor"


def test_a_decline_and_a_tombstone_are_separate_records_in_separate_stores(cfg):
    """A decline is about one row, a tombstone about a recording, so neither revokes the other."""
    row = _row()
    decline = stores.record_decline(cfg, row, actor="cli")
    stones = stores.record_tombstone(cfg, row, actor="cli")
    assert decline.suppression_id != stones.suppression_id

    stores.revoke_decline(cfg, decline.suppression_id, actor="cli")
    assert stores.suppressed_version(cfg, artist=ARTIST, title=ORIGINAL), (
        "revoking a decline lifted a tombstone"
    )


def test_a_decline_survives_a_row_being_re_pointed_at_a_different_file(cfg):
    """A decline says "leave THAT file alone", and never moves with the row."""
    original = _row(recorded="/music/one.flac")
    stores.record_decline(cfg, original, actor="cli")
    declined = stores.decline_predicate(cfg)
    assert declined(original)
    assert not declined(_row(recorded="/music/two.flac"))


def test_an_unreadable_store_refuses_rather_than_reporting_nothing_suppressed(cfg):
    """An empty read would silently un-suppress everything (U11)."""
    stores.record_tombstone(cfg, _row(), actor="cli")
    path = config.state_path(tombstone.STORE_KEY, cfg)
    config.atomic_write_bytes(b'{"version": 1, "store": "tombstones"}\n', path)
    with pytest.raises(CratekitError) as excinfo:
        stores.suppressed_version(cfg, artist=ARTIST, title=ORIGINAL)
    assert excinfo.value.cause.reason == "review-file-unusable"


def test_both_stores_are_declared_state_and_roll_back_with_the_database():
    """R30: a restore must not leave a tombstone over a track it brought back."""
    for key in (tombstone.STORE_KEY, tombstone.DECLINE_STORE_KEY):
        entry = config.state_file(key)
        assert entry.decision_store
        assert entry.snapshot is config.SnapshotRole.COUPLED
        assert key in review.DECISION_STORE_KEYS


def test_the_two_kinds_never_collide_even_on_one_identity(cfg):
    """One identity mapping, two kinds, two identifiers. The kind is part of the key."""
    same = {"content_id": "1", "recorded": "/music/x.flac"}
    assert review.suppression_id_for(
        tombstone.DECLINE_STORE_KEY, tombstone.KIND_REMOVED_FILE, same
    ) != review.suppression_id_for(tombstone.STORE_KEY, tombstone.KIND_REMOVED_FILE, same)


# fold_code: the folding for a STRUCTURED IDENTIFIER, which fold is not

#: The ISO 3901 example code, raw and in its punctuated display form.
_RAW_CODE = "GBAYA1500001"
_DISPLAY_CODE = "GB-AYA-15-00001"


@pytest.mark.parametrize(
    "spelling",
    [
        pytest.param(_DISPLAY_CODE, id="display-form"),
        pytest.param(_RAW_CODE.lower(), id="lowered"),
        pytest.param(_DISPLAY_CODE.lower(), id="lowered-display-form"),
        pytest.param("GB AYA 15 00001", id="spaces"),
        pytest.param("GB\u00a0AYA\u00a015\u00a000001", id="non-breaking-spaces"),
        pytest.param("GB.AYA.15.00001", id="dots"),
        pytest.param("GB_AYA_15_00001", id="underscores"),
        pytest.param(
            "\uff27\uff22\uff21\uff39\uff21\uff11\uff15\uff10\uff10\uff10\uff10\uff11",
            id="fullwidth",
        ),
    ],
)
def test_every_spelling_of_one_code_folds_to_one_value(spelling):
    """Each spelling a real column carries is ONE recording's code, not two."""
    assert tombstone.fold_code(spelling) == tombstone.fold_code(_RAW_CODE)


def test_fold_is_not_fold_code_and_that_is_the_whole_finding():
    """Stated as an inequality, since the two foldings have opposite correct answers."""
    assert tombstone.fold(_DISPLAY_CODE) != tombstone.fold(_RAW_CODE)
    assert tombstone.fold_code(_DISPLAY_CODE) == tombstone.fold_code(_RAW_CODE)


def test_two_genuinely_different_codes_stay_different():
    """Removing punctuation never merges two well-formed codes."""
    assert tombstone.fold_code("USRC17607839") != tombstone.fold_code(_RAW_CODE)


def test_a_non_ascii_alphanumeric_is_not_transliterated():
    """No transliteration, which could merge genuinely different codes and over-suppress."""
    cyrillic = "А" + _RAW_CODE[1:]
    assert tombstone.fold_code(cyrillic) != tombstone.fold_code(_RAW_CODE)
    assert tombstone.fold_code(cyrillic) == cyrillic.casefold()


@pytest.mark.parametrize("empty", ["", "   ", "-", "--", "\u00a0", "()", "_", "- - -"])
def test_a_value_carrying_no_code_folds_to_nothing(empty):
    """Punctuation only is an ABSENT code, so a placeholder dash never disagrees with a real one."""
    assert tombstone.fold_code(empty) == ""
