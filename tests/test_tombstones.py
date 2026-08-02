"""R36: what a tombstone identifies, and the revocability both stores must have.

TWO PARTIES WHO NEVER MEET have to agree here, and that is the whole subject of
this file. The deletion pass RECORDS a suppression from a row rekordbox
soft-deleted. An acquisition pass CONSULTS it from a candidate a provider
returned. Neither imports the other, and on a slim install with deletion switched
off the recorder is not even present, so the only thing making them agree is that
both build the identity from ``cratekit.core.tombstone``.

AE17 IS THE ASSERTION THAT MATTERS. A deleted version of a track that a favourite
label later re-releases must be reported as suppressed, while a DIFFERENT REMIX
of the same recording is still acquired. Get the identity one notch too coarse
and deleting one mix silently withholds every other; one notch too fine and the
tombstone never matches anything and the whole feature is decorative.
"""

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


# ═══════════════════════════════════════════════════════════════════════════
# The identity
# ═══════════════════════════════════════════════════════════════════════════


def test_a_remix_and_its_original_are_two_identities(cfg):
    """AE17, at the level where it is decided.

    KTD16 chose version identity over recording identity because the library is
    remix-heavy, and fuzzy identity is the exact defect the three-state match
    exists to prevent.
    """
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
    """The four things that differ routinely between a row and a search result.

    None of them is a different version, and an identity that treated them as one
    would make the suppression miss the sweeps it exists to stop.
    """
    assert tombstone.version_identity(artist=artist, title=title) == (
        tombstone.version_identity(artist=ARTIST, title=ORIGINAL)
    )


def test_composition_form_is_folded():
    """The 144-file lesson, one layer up from the filesystem.

    macOS hands a name back in whatever form it was created with and a provider
    returns the composed form, so an identity that compared codepoints would miss
    every accented title and only accented titles.
    """
    accented = "Café Track"
    assert tombstone.version_identity(artist=ARTIST, title=accented) == (
        tombstone.version_identity(
            artist=ARTIST, title=unicodedata.normalize("NFD", accented)
        )
    )


def test_punctuation_is_not_folded():
    """Deliberately conservative, and the asymmetry of the costs is the reason.

    A missed suppression re-acquires something and REPORTS it. An over-eager one
    silently withholds music the user wants, and nothing tells them.
    """
    assert tombstone.version_identity(artist=ARTIST, title="Track (Live)") != (
        tombstone.version_identity(artist=ARTIST, title="Track [Live]")
    )


def test_an_identity_with_neither_field_refuses():
    """An empty identity hashes to one value, so one deletion would suppress all."""
    with pytest.raises(CratekitError) as excinfo:
        tombstone.version_identity(artist="", title="   ")
    assert excinfo.value.cause.reason == "review-selection-invalid"


def test_the_field_set_never_varies_with_the_input():
    """A producer that omitted an empty field would hash differently from one that
    supplied it, and the two would never match each other."""
    assert set(tombstone.version_identity(artist=ARTIST, title="")) == {"artist", "title"}
    assert set(tombstone.version_identity(artist="", title=ORIGINAL)) == {"artist", "title"}


def test_the_isrc_is_carried_in_the_payload_and_never_in_the_identity(cfg):
    """The obvious suggestion, and the reason it is wrong.

    A database row often carries a code and a provider candidate often does not.
    In the identity, a tombstone written from a row that had one would fail to
    suppress the same version arriving from a source that had none, silently.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# The stores
# ═══════════════════════════════════════════════════════════════════════════


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
    """R36 says LISTABLE and revocable, and the two halves need each other.

    A revoked record that vanished would leave a person unable to tell "never
    suppressed" from "suppressed and then lifted".
    """
    record = stores.record_tombstone(cfg, _row(), actor="cli")
    stores.revoke_tombstone(cfg, record.suppression_id, actor="cli")
    assert stores.list_tombstones(cfg) == ()
    listed = stores.list_tombstones(cfg, include_revoked=True)
    assert [held.suppression_id for held in listed] == [record.suppression_id]
    assert listed[0].revoked and listed[0].revoked_by == "cli"

    # The projection a listing renders. It carries the revoked flag, so a person
    # reading the list can tell the two cases apart rather than being shown a
    # record that looks live.
    row = stores.summarize(listed[0])
    assert row["revoked"] is True
    assert row["title"] == ORIGINAL and row["identity"] == f"{ARTIST.lower()} - {ORIGINAL.lower()}"


def test_recording_the_same_version_twice_changes_nothing(cfg):
    first = stores.record_tombstone(cfg, _row(), actor="cli")
    second = stores.record_tombstone(cfg, _row(content_id="2"), actor="someone-else")
    assert first == second, "a re-record moved the timestamp or the actor"


def test_a_decline_and_a_tombstone_are_separate_records_in_separate_stores(cfg):
    """Revoking a decline must not un-suppress an acquisition.

    A decline is about one library ROW and one file on this disk. A tombstone is
    about a RECORDING that outlives the row, the file, and the library. Folding
    them into one store would make "keep this file" mean "acquire this again".
    """
    row = _row()
    decline = stores.record_decline(cfg, row, actor="cli")
    stones = stores.record_tombstone(cfg, row, actor="cli")
    assert decline.suppression_id != stones.suppression_id

    stores.revoke_decline(cfg, decline.suppression_id, actor="cli")
    assert stores.suppressed_version(cfg, artist=ARTIST, title=ORIGINAL), (
        "revoking a decline lifted a tombstone"
    )


def test_a_decline_survives_a_row_being_re_pointed_at_a_different_file(cfg):
    """A decline says "leave THAT file alone", and inheriting it onto whatever the
    row points at next would be a decision nobody made."""
    original = _row(recorded="/music/one.flac")
    stores.record_decline(cfg, original, actor="cli")
    declined = stores.decline_predicate(cfg)
    assert declined(original)
    assert not declined(_row(recorded="/music/two.flac"))


def test_an_unreadable_store_refuses_rather_than_reporting_nothing_suppressed(cfg):
    """The U11 defect, asserted from this unit's side of the seam.

    A suppression list read as empty un-suppresses everything in it silently, and
    the next acquisition pass re-acquires exactly what somebody deleted on
    purpose.
    """
    stores.record_tombstone(cfg, _row(), actor="cli")
    path = config.state_path(tombstone.STORE_KEY, cfg)
    config.atomic_write_bytes(b'{"version": 1, "store": "tombstones"}\n', path)
    with pytest.raises(CratekitError) as excinfo:
        stores.suppressed_version(cfg, artist=ARTIST, title=ORIGINAL)
    assert excinfo.value.cause.reason == "review-file-unusable"


def test_both_stores_are_declared_state_and_roll_back_with_the_database():
    """R30 names them by name, and the coupling is what stops a restore leaving a
    tombstone standing over a track the restore just brought back."""
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
