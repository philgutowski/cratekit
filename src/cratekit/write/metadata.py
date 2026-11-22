"""Per-field metadata maintenance, database-direct and convergent (U21).

The structural whitelist in ``core.rb_writer`` answers whether a table may be
touched at all. This module answers whether THIS operation may set THIS field
on a curated row, which names feature operations and so cannot live in core.
It is the only place operation names appear.

An operation REGISTERS the fields it declares, so the writable column set is
the union of what is enabled; enable nothing and nothing is writable (R14).

**Fill-if-empty is the default and ownership is the exception**, so a value a
person set by hand, a rating above all, survives every sweep.

**Some fields refuse at registration** (:data:`UNWRITABLE_FIELDS`), rather
than relying on absence from the policy table, which one plausible entry in a
later unit would undo.

**The key field is never authored.** ``djmdKey`` is structurally writable on
the A4 verdict, but that is a ceiling: padded Camelot belongs in the title,
and the key field stays blank so rekordbox's answer stays independent. There
is no resolve-then-create helper for keys.

LAYER: write. It writes through the guarded writer and names no verb (D2).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from cratekit.core import naming, rb_writer, taxonomy
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy

logger = logging.getLogger(__name__)


# The operations, named once.

#: Kebab-case, as ``rb_writer.TRACK_COLOR_POLICY``'s owner is, so a policy table
#: keyed on owner names cannot half-match.
PAD_CAMELOT = "pad-camelot"
RETAG_GENRE = "retag-genre"
RATING_BACKFILL = "rating-backfill"

#: Every operation this module can enable, walked wherever a count or coverage
#: claim is made (P3), so a new one is covered the moment it is added.
OPERATIONS: Mapping[str, rb_writer.FieldPolicy] = MappingProxyType(
    {
        #: Owned: it rewrites the key's own span in the head and no other byte.
        PAD_CAMELOT: rb_writer.FieldPolicy(
            owner=PAD_CAMELOT,
            fields=MappingProxyType({"Title": rb_writer.Ownership.OWNED}),
        ),
        #: Owned, because its one caller lists every row at an explicit gate and
        #: lets a row be held out by name. It links a lookup row, never mints one.
        RETAG_GENRE: rb_writer.FieldPolicy(
            owner=RETAG_GENRE,
            fields=MappingProxyType({"GenreID": rb_writer.Ownership.OWNED}),
        ),
        #: Fill-if-empty, never to be widened: a rating is what a person most
        #: often sets by hand, and overwriting it erases their disagreement.
        RATING_BACKFILL: rb_writer.FieldPolicy(
            owner=RATING_BACKFILL,
            fields=MappingProxyType({"Rating": rb_writer.Ownership.FILL_IF_EMPTY}),
        ),
    }
)


#: The fields no operation here may declare, refused at registration with the
#: reason for each, since "no policy entry exists" is one entry from undone.
UNWRITABLE_FIELDS: Mapping[str, str] = MappingProxyType(
    {
        "KeyID": (
            "the writer never authors a key value. Padded Camelot is a sorting "
            "artifact and belongs in the title; the key field stays blank so "
            "rekordbox's answer stays an independent second opinion (A4 rescope)"
        ),
        "ColorID": (
            "the track colour is the favourites operation's, registered in the "
            "core writer under its own owner. A metadata operation declaring it "
            "would give one column two owners with different policies"
        ),
        "Commnt": (
            "the comment field is the user's own free text. Nothing this product "
            "computes belongs in it, and it has no formatting an operation could "
            "claim to own"
        ),
    }
)


class PolicyRefused(Exception):
    """An operation declared a field it may never declare.

    A plain exception: this is a programming error at registration, not a
    condition a user can reach or remediate.
    """


def _assert_declarable(policy: rb_writer.FieldPolicy) -> None:
    """Refuse a policy naming an unwritable field, before it can reach the registry."""
    for field_name in policy.fields:
        why = UNWRITABLE_FIELDS.get(field_name)
        if why is not None:
            raise PolicyRefused(
                f"operation {policy.owner!r} declares {field_name!r}, which no "
                f"metadata operation may write: {why}"
            )


def enable(owners: Iterable[str] = ()) -> frozenset[str]:
    """Register the named operations, or every operation when none are named.

    Returns the content columns writable afterwards, derived from the core
    registry rather than from the argument, so the answer is what the guard will
    actually enforce rather than what this function intended (P2).
    """
    wanted = tuple(owners) or tuple(OPERATIONS)
    for owner in wanted:
        policy = OPERATIONS.get(owner)
        if policy is None:
            raise PolicyRefused(f"no metadata operation named {owner!r}")
        _assert_declarable(policy)
        rb_writer.register_field_policy(policy)
    return rb_writer.content_writable_columns()


# Lookup rows: resolve, never create.

#: A row that could not answer, distinct from every value the soft-delete column
#: can hold, since a plain default would be the permissive answer.
_MARKER_ABSENT = object()


def resolve_genre_id(db: Any, genre_name: str) -> Any | None:
    """The identifier of an existing, active genre row, or None.

    Never creates: the taxonomy is the user's, so a miss is skipped and surfaced.
    There is deliberately no sibling for keys. The first ACTIVE row wins, since a
    soft-deleted namesake can sort first. A row that cannot report its marker
    refuses (:func:`first_active_id`) rather than defaulting to active, and is not
    folded into None, which means "no active genre by that name" and becomes a
    per-row skip that would blame the user's taxonomy for a binding regression.
    """
    if not genre_name:
        return None
    return first_active_id(db.get_genre(Name=genre_name), table="djmdGenre", name=genre_name)


#: The key a lookup word is named under in a refusal's detail, by table.
_WORD_KEYS = MappingProxyType({"djmdGenre": "genre", "djmdArtist": "artist", "djmdAlbum": "album"})


def first_active_id(rows: Iterable[Any], *, table: str, name: str) -> Any | None:
    """The identifier of the first active lookup row among ``rows``, or None.

    :func:`resolve_genre_id`'s rule for any lookup table (U163): a tombstone is
    skipped, and a row that cannot report its marker refuses. ``rows`` are the
    table's rows by exact name, in the binding's order.
    """
    for row in rows:
        marker = getattr(row, rb_writer.SOFT_DELETE_COLUMN, _MARKER_ABSENT)
        if marker is _MARKER_ABSENT or marker is None:
            word = _WORD_KEYS.get(table, "word")
            raise refuse(
                "soft-delete-marker-unreadable",
                f"the {word} row {getattr(row, 'ID', '?')!r} cannot say whether "
                f"it is a tombstone, and treating that as 'not deleted' would "
                f"point a track's {word} at a row rekordbox has already retired",
                remedy=Remedy.RUN_DOCTOR,
                scope=Scope.RUN,
                origin=("write", "metadata"),
                detail={
                    "table": table,
                    "row_id": str(getattr(row, "ID", "")),
                    "column": rb_writer.SOFT_DELETE_COLUMN,
                    word: name,
                },
            )
        if not marker:
            return row.ID
    return None


# The plan: one shape, serving the preview and the apply.


@dataclass(frozen=True, slots=True)
class Change:
    """One proposed field write on one row, before anything is applied."""

    content_id: str
    owner: str
    field_name: str
    current: Any
    new: Any

    def decide(self, *, policies: Mapping[str, rb_writer.FieldPolicy] | None = None):
        """What the per-field policy says about this change. Pure."""
        return rb_writer.metadata_decision(
            self.owner, self.field_name, self.current, self.new, policies=policies
        )


@dataclass(frozen=True, slots=True)
class Skipped:
    """A row the plan could not propose a change for, and why; surfaced, not raised."""

    content_id: str
    reason: str
    detail: str = ""


@dataclass(frozen=True, slots=True)
class Plan:
    """Every proposed change and every skip, for one operation over one row set.

    The same object serves the dry run and the apply, so the preview cannot
    disagree with what is written.
    """

    owner: str
    changes: tuple[Change, ...] = ()
    skipped: tuple[Skipped, ...] = ()

    def decisions(
        self, *, policies: Mapping[str, rb_writer.FieldPolicy] | None = None
    ) -> tuple[tuple[Change, rb_writer.Decision], ...]:
        """Each change paired with what the policy says, without touching a row."""
        return tuple((c, c.decide(policies=policies)) for c in self.changes)

    @property
    def content_ids(self) -> tuple[str, ...]:
        return tuple(c.content_id for c in self.changes)


@dataclass(frozen=True, slots=True)
class Report:
    """What an apply did, counted from the decisions the writer returned."""

    owner: str
    applied: tuple[tuple[str, rb_writer.Decision], ...] = ()
    skipped: tuple[Skipped, ...] = ()

    @property
    def totals(self) -> Mapping[str, int]:
        counts: dict[str, int] = {d.value: 0 for d in rb_writer.Decision}
        for _, decision in self.applied:
            counts[decision.value] += 1
        return MappingProxyType(counts)

    @property
    def written(self) -> tuple[str, ...]:
        return tuple(cid for cid, d in self.applied if d is rb_writer.Decision.WRITE)


# Planning each operation. Pure, and none of them opens a session.


def _content_id(row: Any) -> str:
    return str(getattr(row, "ID", "") or "")


def plan_title_padding(rows: Iterable[Any], *, template: naming.NameTemplate) -> Plan:
    """Zero-pad the Camelot head on each title that carries an unpadded one.

    Idempotent by selection: an already padded head is no change.
    :func:`naming.pad_head` splices the key's own span and leaves every other byte.
    """
    changes: list[Change] = []
    skipped: list[Skipped] = []
    for row in rows:
        content_id = _content_id(row)
        current = getattr(row, "Title", None)
        if not current:
            skipped.append(Skipped(content_id, "no-title"))
            continue
        padded = naming.pad_head(str(current), template=template)
        if padded == str(current):
            continue
        changes.append(Change(content_id, PAD_CAMELOT, "Title", current, padded))
    return Plan(PAD_CAMELOT, tuple(changes), tuple(skipped))


def plan_genre_retag(rows: Iterable[Any], genres: Mapping[str, str], *, db: Any) -> Plan:
    """Link each row to the existing lookup row for its reviewed genre name.

    A name with no lookup row is skipped and surfaced; ``djmdGenre`` is also
    absent from ``rb_writer.PERMITTED_ROW_TABLES``. Each distinct name is resolved
    once per plan.
    """
    changes: list[Change] = []
    skipped: list[Skipped] = []
    resolved: dict[str, Any | None] = {}
    for row in rows:
        content_id = _content_id(row)
        wanted = genres.get(content_id)
        if not wanted:
            continue
        if wanted not in resolved:
            resolved[wanted] = resolve_genre_id(db, wanted)
        genre_id = resolved[wanted]
        if genre_id is None:
            skipped.append(Skipped(content_id, "genre-unknown", wanted))
            continue
        changes.append(
            Change(content_id, RETAG_GENRE, "GenreID", getattr(row, "GenreID", None), genre_id)
        )
    return Plan(RETAG_GENRE, tuple(changes), tuple(skipped))


def rating_for(level: int, cuts: Sequence[taxonomy.RatingCut]) -> int | None:
    """The star value for an energy level, read off the taxonomy's own curve."""
    for cut in sorted(cuts, key=lambda c: c.max):
        if level <= cut.max:
            return cut.rating
    return None


#: The export byte rekordbox spells for each star count, one to five.
_EXPORT_BYTE_STARS = MappingProxyType({51: 1, 102: 2, 153: 3, 204: 4, 255: 5})
_DATABASE_STARS = frozenset(_EXPORT_BYTE_STARS.values())


def _scale_unknown(message: str, detail: Mapping[str, Any]) -> CratekitError:
    return refuse(
        "rating-scale-unknown",
        message,
        remedy=Remedy.FIX_CONFIG_VALUES,
        scope=Scope.RUN,
        origin=("write", "metadata"),
        detail=dict(detail),
    )


def database_stars(value: int) -> int:
    """The star count the database stores for a taxonomy rating value (R-414).

    The taxonomy's cuts are on the xml export scale (255 is five stars), and the
    database stores 0 to 5, so a cut crosses into the database here and nowhere
    else. A star count passes through, zero is unrated on both scales, and
    anything else is refused rather than written into a field whose largest value
    is 5.
    """
    if value == 0 or value in _DATABASE_STARS:
        return value
    stars = _EXPORT_BYTE_STARS.get(value)
    if stars is None:
        raise _scale_unknown(
            f"the taxonomy's [energy.rating] curve holds {value}, which is neither "
            f"an export byte (51, 102, 153, 204, 255) nor a star count (1 to 5), "
            f"so there is no star rating to write for it",
            {"rating": value},
        )
    return stars


def _database_curve(cuts: Sequence[taxonomy.RatingCut]) -> dict[int, int]:
    """Every cut value folded to its star count, or a refusal naming the curve.

    A curve is on ONE scale; a mix of bytes and stars is a template typo, refused
    rather than resolved either way. Zero belongs to both scales.
    """
    folded = {cut.rating: database_stars(cut.rating) for cut in cuts}
    bytes_ = sorted(v for v in folded if v in _EXPORT_BYTE_STARS)
    stars = sorted(v for v in folded if v in _DATABASE_STARS)
    if bytes_ and stars:
        raise _scale_unknown(
            f"the taxonomy's [energy.rating] curve mixes export bytes {bytes_} "
            f"with star counts {stars}, so it does not say which scale it is on",
            {"ratings": sorted(folded)},
        )
    return folded


def plan_rating_backfill(
    rows: Iterable[Any], levels: Mapping[str, int], *, cuts: Sequence[taxonomy.RatingCut]
) -> Plan:
    """Fill a database star rating from an energy level, on rows with no rating.

    The whole curve is folded BEFORE any row is planned, so a bad value refuses
    the plan rather than the rows in its cut. A cut of zero leaves its band
    unrated, skipped as ``level-unrated``. Fill-if-empty is the policy's, through
    :func:`rb_writer.metadata_decision`, not a check here (P2).
    """
    curve = _database_curve(cuts)
    changes: list[Change] = []
    skipped: list[Skipped] = []
    for row in rows:
        content_id = _content_id(row)
        level = levels.get(content_id)
        if level is None:
            continue
        rating = rating_for(level, cuts)
        if rating is None:
            skipped.append(Skipped(content_id, "level-uncut", str(level)))
            continue
        stars = curve[rating]
        if stars == 0:
            skipped.append(Skipped(content_id, "level-unrated", str(level)))
            continue
        changes.append(
            Change(content_id, RATING_BACKFILL, "Rating", getattr(row, "Rating", None), stars)
        )
    return Plan(RATING_BACKFILL, tuple(changes), tuple(skipped))


# Applying a plan.


def write_plan(
    plan: Plan,
    rows_by_id: Mapping[str, Any],
    *,
    policies: Mapping[str, rb_writer.FieldPolicy] | None = None,
) -> Report:
    """Apply every change in a plan and report what each one decided.

    Does not commit: the caller batches and calls
    :func:`rb_writer.commit_guarded`, the structural backstop. A change naming a
    row the caller did not supply is surfaced as a skip.
    """
    applied: list[tuple[str, rb_writer.Decision]] = []
    skipped = list(plan.skipped)
    for change in plan.changes:
        row = rows_by_id.get(change.content_id)
        if row is None:
            skipped.append(Skipped(change.content_id, "row-absent"))
            continue
        decision = rb_writer.write_metadata_field(
            row, change.owner, change.field_name, change.new, policies=policies
        )
        applied.append((change.content_id, decision))
    return Report(plan.owner, tuple(applied), tuple(skipped))


def assert_within_policy(plan: Plan) -> None:
    """Refuse a plan proposing a field its operation does not own.

    Applying one is harmless (``SKIP_UNOWNED``), but a sweep that silently writes
    nothing looks like a sweep with nothing to do.
    """
    offenders = [
        f"{c.owner} -> {c.field_name}"
        for c, d in plan.decisions()
        if d is rb_writer.Decision.SKIP_UNOWNED
    ]
    if offenders:
        raise refuse(
            "refused-by-policy",
            "this operation does not own every field its plan would write: "
            + ", ".join(sorted(set(offenders))),
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.RUN,
            origin=("write", "metadata"),
            detail={"owner": plan.owner, "fields": sorted(set(offenders))},
        )


__all__ = [
    "OPERATIONS",
    "PAD_CAMELOT",
    "RATING_BACKFILL",
    "RETAG_GENRE",
    "UNWRITABLE_FIELDS",
    "Change",
    "Plan",
    "PolicyRefused",
    "Report",
    "Skipped",
    "write_plan",
    "assert_within_policy",
    "database_stars",
    "enable",
    "first_active_id",
    "plan_genre_retag",
    "plan_rating_backfill",
    "plan_title_padding",
    "rating_for",
    "resolve_genre_id",
]
