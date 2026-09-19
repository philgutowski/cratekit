"""The companion a credited tombstone gains, on the RECORDING side (R-431).

A library row that kept a featured credit is recorded under a title no provider
with a version field can compose, so the deletion pass writes a second record
with the credit groups taken out, under a kind of its own. The consulting half
is driven in ``tests/test_match_states.py`` and end to end in
``tests/test_intake_missing.py``. This file is what the recorder owes:

* a row with no credit gains nothing, which is what keeps a deletion of the
  plain record from ever withholding the credited one;
* the companion never lands on a lookup under the tombstone's own kind;
* REVOCABLE stays true of a deletion that is now two records.

Every identity asserted here is a literal, because an expected value built by
the code under test reduces the assertion to X equals X.
"""

from __future__ import annotations

import pytest

from cratekit.core import config, tombstone
from cratekit.deletion import run, stores
from cratekit.deletion.library import VERSION_IS_AN_ARTIST, RemovedRow
from tests.test_config import valid_data

ARTIST = "Aurora Bloom"


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return config.from_dict(valid_data(root))


def row(title: str, *, content_id: str = "9001", version: str = "", kind: str | None = None):
    extra = {"version_kind": kind} if kind else {}
    return RemovedRow(
        content_id=content_id, recorded=f"/Music/{content_id}.flac", sequence=1, size=None,
        artist=ARTIST, title=title, version=version, **extra,
    )


def live(cfg) -> list[tuple[str, str]]:
    """Every suppressing record as (kind, identity title), in a stable order."""
    return sorted(
        (record.kind, str((record.identity or {}).get("title")))
        for record in stores.list_tombstones(cfg)
    )


# ═══════════════════════════════════════════════════════════════════════════
# What strips, and what does not
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "title,expected",
    [
        ("Sun Path (feat. Mira) (Nightwave Remix)", "Sun Path (Nightwave Remix)"),
        ("Sun Path (Nightwave Remix) (feat. Mira)", "Sun Path (Nightwave Remix)"),
        ("Sun Path [ft. Mira] [Nightwave Remix]", "Sun Path [Nightwave Remix]"),
        ("Sun Path (with Mira)", "Sun Path"),
        ("Sun Path (Featuring Mira) (feat. Zed) (Live)", "Sun Path (Live)"),
        # No credit, so no companion. A mix name that merely CONTAINS a marker
        # is a mix name, which is ``_is_a_credit``'s first word rule.
        ("Sun Path (Nightwave Remix)", ""),
        ("Sun Path (Live with Strings)", ""),
        ("Sun Path", ""),
        # An unbracketed credit is left alone: taking it out means guessing
        # where it ends, and a wrong guess removes a word of the title.
        ("Sun Path feat. Mira (Nightwave Remix)", ""),
        # Nothing but a credit strips to nothing, and an empty title would
        # collapse every such row by one artist onto one record.
        ("(feat. Mira)", ""),
    ],
)
def test_only_a_bracketed_credit_group_comes_out_of_a_title(title, expected):
    assert tombstone.uncredited_title(title) == expected


def test_the_companion_identity_is_the_verbatim_one_with_the_credit_out():
    assert stores.uncredited_version_of(row("Sun Path (feat. Mira) (Nightwave Remix)")) == {
        "artist": "aurora bloom",
        "title": "sun path (nightwave remix)",
    }
    assert stores.uncredited_version_of(row("Sun Path (Nightwave Remix)")) is None


def test_the_companion_is_built_from_the_composed_title_not_the_title_column():
    """The version column is composed in FIRST, the way the tombstone's own
    identity is, so a row whose mix name sits beside the title strips to the
    string a provider composes for it."""
    assert stores.uncredited_version_of(
        row("Sun Path (feat. Mira)", version="Nightwave Remix")
    ) == {"artist": "aurora bloom", "title": "sun path (nightwave remix)"}
    assert stores.uncredited_version_of(
        row("Sun Path (feat. Mira)", version="Nightwave", kind=VERSION_IS_AN_ARTIST)
    ) == {"artist": "aurora bloom", "title": "sun path (nightwave remix)"}


def test_adding_the_companion_did_not_move_the_identity_stamp():
    """``uncredited_version_of`` sits ON TOP of ``version_of``. Were it called
    from inside, the stamp would walk it, move, and send every tombstone this
    build ever wrote to the row lookup. ``tests/test_deletion.py`` pins the
    literal stamp, and this pins the reason it held."""
    reached = stores._composition_rules()
    assert not any("uncredited" in name for name in reached)


# ═══════════════════════════════════════════════════════════════════════════
# What one deletion records
# ═══════════════════════════════════════════════════════════════════════════


def test_a_credited_deletion_is_two_records_and_a_plain_one_is_one(cfg):
    written = stores.record_tombstone(
        cfg, row("Sun Path (feat. Mira) (Nightwave Remix)"), actor="deletion"
    )
    assert written.kind == tombstone.KIND_VERSION
    assert live(cfg) == [
        ("version", "sun path (feat. mira) (nightwave remix)"),
        ("version-uncredited", "sun path (nightwave remix)"),
    ]
    companion = next(
        one for one in stores.list_tombstones(cfg)
        if one.kind == tombstone.KIND_VERSION_UNCREDITED
    )
    assert companion.payload[stores.CREDITED_ID_FIELD] == written.suppression_id

    stores.record_tombstone(cfg, row("Salt Road", content_id="9002"), actor="deletion")
    assert [kind for kind, _title in live(cfg)].count("version-uncredited") == 1


def test_recording_the_same_deletion_twice_is_still_two_records(cfg):
    for _ in range(2):
        stores.record_tombstone(
            cfg, row("Sun Path (feat. Mira) (Nightwave Remix)"), actor="deletion"
        )
    assert len(live(cfg)) == 2


def test_a_companion_is_never_the_answer_to_a_verbatim_lookup(cfg):
    """THE REASON IT HAS A KIND OF ITS OWN. ``suppressed_version`` and the label
    sweep ask under the tombstone's kind, and neither narrowed its question to
    a listing that spelled no credit. Under one kind they would both land on
    the stripped title."""
    stores.record_tombstone(
        cfg, row("Sun Path (feat. Mira) (Nightwave Remix)"), actor="deletion"
    )
    assert stores.suppressed_version(
        cfg, artist=ARTIST, title="Sun Path (feat. Mira) (Nightwave Remix)"
    )
    assert not stores.suppressed_version(cfg, artist=ARTIST, title="Sun Path (Nightwave Remix)")


def test_a_companion_never_says_a_run_recorded_a_different_rows_deletion(cfg):
    """``tombstone_predicate`` retires a confirmed removal without moving
    anything, so a companion answering for the plain row would throw away a
    deletion somebody confirmed."""
    stores.record_tombstone(
        cfg, row("Sun Path (feat. Mira) (Nightwave Remix)"), actor="deletion"
    )
    recorded = stores.tombstone_predicate(cfg)
    assert recorded(row("Sun Path (feat. Mira) (Nightwave Remix)"))
    assert not recorded(row("Sun Path (Nightwave Remix)", content_id="9002"))


# ═══════════════════════════════════════════════════════════════════════════
# Revocable, which is now a statement about two records
# ═══════════════════════════════════════════════════════════════════════════


def test_lifting_a_credited_tombstone_lifts_its_companion(cfg):
    written = stores.record_tombstone(
        cfg, row("Sun Path (feat. Mira) (Nightwave Remix)"), actor="deletion"
    )
    lifted = run.revoke(cfg, written.suppression_id, actor="a-person")

    assert lifted.suppression_id == written.suppression_id and lifted.revoked
    assert live(cfg) == []
    assert sorted(
        (one.kind, one.revoked, one.revoked_by)
        for one in stores.list_tombstones(cfg, include_revoked=True)
    ) == [("version", True, "a-person"), ("version-uncredited", True, "a-person")]


def test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second(cfg):
    """Two rows crediting two guests strip to ONE identity, and the companion
    names only whichever arrived first. Lifting it with the first would
    re-acquire the second, which nobody lifted. Leaving it after the second
    would be a suppression nothing can lift, since its pointer names a record
    that is already revoked."""
    first = stores.record_tombstone(
        cfg, row("Sun Path (feat. Mira) (Nightwave Remix)"), actor="deletion"
    )
    second = stores.record_tombstone(
        cfg, row("Sun Path (feat. Zed) (Nightwave Remix)", content_id="9002"), actor="deletion"
    )
    assert [kind for kind, _title in live(cfg)] == ["version", "version", "version-uncredited"]

    run.revoke(cfg, first.suppression_id, actor="a-person")
    assert live(cfg) == [
        ("version", "sun path (feat. zed) (nightwave remix)"),
        ("version-uncredited", "sun path (nightwave remix)"),
    ]

    run.revoke(cfg, second.suppression_id, actor="a-person")
    assert live(cfg) == []


def test_the_shared_companion_is_also_found_in_the_other_order(cfg):
    """The second deletion's companion is found by stripping, not by pointer,
    so lifting the SECOND first keeps it and lifting the first then takes it."""
    first = stores.record_tombstone(
        cfg, row("Sun Path (feat. Mira) (Nightwave Remix)"), actor="deletion"
    )
    second = stores.record_tombstone(
        cfg, row("Sun Path (feat. Zed) (Nightwave Remix)", content_id="9002"), actor="deletion"
    )
    run.revoke(cfg, second.suppression_id, actor="a-person")
    assert ("version-uncredited", "sun path (nightwave remix)") in live(cfg)
    run.revoke(cfg, first.suppression_id, actor="a-person")
    assert live(cfg) == []


def test_a_companion_is_found_by_its_pointer_when_the_stripping_rule_has_moved(cfg, monkeypatch):
    """THE LOOKUP HALF, removed from the recomputation half. A later build whose
    stripping rule differs composes a different companion identifier, and a
    revocation that only recomputed would leave this one standing for ever."""
    written = stores.record_tombstone(
        cfg, row("Sun Path (feat. Mira) (Nightwave Remix)"), actor="deletion"
    )
    monkeypatch.setattr(tombstone, "uncredited_title", lambda _title: "")
    run.revoke(cfg, written.suppression_id, actor="a-person")
    assert live(cfg) == []


def test_lifting_the_companion_alone_leaves_the_tombstone_standing(cfg):
    written = stores.record_tombstone(
        cfg, row("Sun Path (feat. Mira) (Nightwave Remix)"), actor="deletion"
    )
    companion = next(
        one for one in stores.list_tombstones(cfg)
        if one.kind == tombstone.KIND_VERSION_UNCREDITED
    )
    run.revoke(cfg, companion.suppression_id, actor="a-person")
    assert live(cfg) == [("version", "sun path (feat. mira) (nightwave remix)")]
    assert written.suppression_id in {one.suppression_id for one in stores.list_tombstones(cfg)}


def test_lifting_a_plain_tombstone_touches_no_companion_it_does_not_own(cfg):
    """A plain ``Sun Path (Nightwave Remix)`` deletion strips to nothing, so
    lifting it must leave the credited deletion's companion where it is, even
    though the two titles are the same string."""
    stores.record_tombstone(
        cfg, row("Sun Path (feat. Mira) (Nightwave Remix)"), actor="deletion"
    )
    plain = stores.record_tombstone(
        cfg, row("Sun Path (Nightwave Remix)", content_id="9002"), actor="deletion"
    )
    run.revoke(cfg, plain.suppression_id, actor="a-person")
    assert live(cfg) == [
        ("version", "sun path (feat. mira) (nightwave remix)"),
        ("version-uncredited", "sun path (nightwave remix)"),
    ]


def test_an_unknown_identifier_still_refuses_in_the_stores_own_words(cfg):
    from cratekit.core.cause import CratekitError

    with pytest.raises(CratekitError) as refused:
        stores.revoke_tombstone(cfg, "dc_nope", actor="a-person")
    assert refused.value.cause.reason == "review-item-unknown"


def test_the_listing_projects_a_companion_without_inventing_fields(cfg):
    stores.record_tombstone(
        cfg, row("Sun Path (feat. Mira) (Nightwave Remix)"), actor="deletion"
    )
    companion = next(
        one for one in stores.list_tombstones(cfg)
        if one.kind == tombstone.KIND_VERSION_UNCREDITED
    )
    shown = stores.summarize(companion)
    assert shown["kind"] == "version-uncredited"
    assert shown["identity"] == "aurora bloom - sun path (nightwave remix)"
    assert shown["title"] == "Sun Path (feat. Mira) (Nightwave Remix)"
    assert shown["revoked"] is False
