"""Per-field metadata maintenance, database-direct and convergent (U21).

WHAT THIS MODULE IS FOR. The structural whitelist in ``core.rb_writer`` answers
"may a row in this table be touched at all". It cannot answer "may THIS operation
set THIS field on a row a person has already curated", because that question names
feature operations and a core module that enumerates features inverts the layering
the build is organised around. This module is the answer to the second question,
and it is the only place operation names appear.

THE DIRECTION IS INVERTED, AND THAT IS THE WHOLE DESIGN. The source system kept
one static table of every field any operation might ever write, so a slim install
with no metadata features enabled still had four content columns structurally
writable for no reason at all. Here an operation REGISTERS the fields it declares,
and the writable column set is the union of what is actually enabled. Enable
nothing and nothing is writable. That is R14's "widened only as far as each
feature requires" implemented rather than described.

THREE PROPERTIES, EACH LEARNED FROM A DIFFERENT FAILURE.

**Fill-if-empty is the default and ownership is the exception.** An operation may
overwrite only a field whose formatting it owns outright. Everything else it may
only fill, so a value a person set by hand survives every sweep. A rating someone
placed on a track is the case that matters: automation that recomputes it from
energy and overwrites is indistinguishable, afterwards, from automation that was
right.

**Some fields are unwritable by refusal, not by omission.** Absence from the
policy table already yields ``SKIP_UNOWNED``, which is correct but fragile: it
takes one plausible-looking table entry in a later unit to undo, and the person
adding it will not know what they undid. The fields named in
:data:`UNWRITABLE_FIELDS` refuse at REGISTRATION time instead, so the mistake
cannot reach a write path and cannot be made quietly.

**The key metadata field is never authored, and no path to author one exists.**
``djmdKey`` sits in the structural whitelist on the A4 verdict, which found
rekordbox tolerates an externally authored lookup row untouched. That permission
is a ceiling, not a licence. Padded Camelot belongs in the track TITLE, where it
is a sorting artifact: ``1A`` sorts after ``10A`` alphabetically and ``01A`` does
not. The key field itself stays blank so rekordbox's analysis and this product's
answer remain independently comparable. It is the beat-grid rule one layer up: do
not feed your own answer into the thing whose independent answer you wanted. So
there is no resolve-then-create helper for keys here, and no caller can grow one
without deleting a test that says so.

LAYER: write. It reads library rows and writes them through the guarded writer,
calls the structural gate rather than restating it, and NAMES NO VERB (D2): the
CLI layer renders every command a user types.
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


# ---------------------------------------------------------------------------
# The operations, named once
# ---------------------------------------------------------------------------

#: Kebab-case, matching ``rb_writer.TRACK_COLOR_POLICY``'s owner rather than the
#: source system's snake_case. One convention, so a policy table keyed on owner
#: names cannot half-match.
PAD_CAMELOT = "pad-camelot"
RETAG_GENRE = "retag-genre"
RATING_BACKFILL = "rating-backfill"

#: Every operation this module can enable. Walked rather than enumerated wherever
#: a count or a coverage claim is made (P3), so an operation added below is
#: covered by the suite the moment it is added rather than the moment somebody
#: remembers to widen a list.
OPERATIONS: Mapping[str, rb_writer.FieldPolicy] = MappingProxyType(
    {
        #: The Camelot head is a formatting concern this operation owns outright:
        #: it rewrites the key's own span inside the head and leaves every other
        #: byte of the title alone.
        PAD_CAMELOT: rb_writer.FieldPolicy(
            owner=PAD_CAMELOT,
            fields=MappingProxyType({"Title": rb_writer.Ownership.OWNED}),
        ),
        #: A genre retag is owned because the operation only runs over rows a
        #: person reviewed, and its one caller, the row verb, is what makes that
        #: true: every row it would write is listed with the row's word and the
        #: file's at an explicit gate, and nothing is written without that
        #: answer. Owned still means a word a person set on the row by hand is
        #: replaced when they approve a plan that lists it, which is why that
        #: verb lets a row be held out by name. It links an existing lookup row
        #: and never mints one.
        RETAG_GENRE: rb_writer.FieldPolicy(
            owner=RETAG_GENRE,
            fields=MappingProxyType({"GenreID": rb_writer.Ownership.OWNED}),
        ),
        #: Fill-if-empty, and this is the one that must never be widened. A star
        #: rating is the most common thing in this schema for a person to have set
        #: deliberately, and an energy-derived rating that overwrites it destroys
        #: the only record that a human disagreed.
        RATING_BACKFILL: rb_writer.FieldPolicy(
            owner=RATING_BACKFILL,
            fields=MappingProxyType({"Rating": rb_writer.Ownership.FILL_IF_EMPTY}),
        ),
    }
)


# ---------------------------------------------------------------------------
# The fields no operation here may declare
# ---------------------------------------------------------------------------

#: Refused at registration, with the argument attached to each one. These are the
#: fields where "no policy entry exists" is true today and is not a strong enough
#: guarantee, because the repair for a future caller who wants one is to add an
#: entry, and nothing would stop them.
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

    A plain exception rather than a typed refusal: this fires at registration,
    which is a programming error inside this package, not a condition a user can
    reach or remediate. A ``Cause`` here would put a remediation token in front of
    somebody who cannot act on it.
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


# ---------------------------------------------------------------------------
# Lookup rows: resolve, never create
# ---------------------------------------------------------------------------


#: What "this row could not answer" looks like, distinct from every value the
#: soft-delete column can legitimately hold. A plain default would be the
#: permissive answer wearing a sentinel's clothes.
_MARKER_ABSENT = object()


def resolve_genre_id(db: Any, genre_name: str) -> Any | None:
    """The identifier of an existing, active genre row, or None.

    NEVER CREATES. A genre this library has never seen is a row this product has
    no business minting: the taxonomy is the user's, and a fabricated lookup row
    that nothing ends up referencing is garbage collected by rekordbox anyway.
    A miss is skipped and surfaced, which is a fact the user can act on.

    There is deliberately no sibling for keys. See the module docstring.

    The first ACTIVE row wins rather than the first row. A soft-deleted namesake
    sorts ahead of a live one often enough to matter, and taking the first row and
    then testing it reports "no such genre" for a genre the library plainly has.

    THE MARKER IS READ, NEVER DEFAULTED, AND A ROW THAT CANNOT REPORT IT REFUSES.
    ``rb_local_deleted`` is a bookkeeping column, so a binding that stops exposing
    it hands back rows that cannot say whether they are tombstones, and every
    default this function could supply for that is the answer "active". Supplying
    it made a soft-deleted genre resolve, and the write that followed pointed a
    track's ``GenreID`` at a row rekordbox has already retired.

    WHY REFUSING IS RIGHT HERE, AND WHY IT IS NOT THE SAME ARGUMENT AS A TRACK'S.
    A tombstoned content row is a track somebody removed, and acting on it acts on
    something that is gone. A tombstoned lookup row is not that. It is a
    perfectly ordinary thing to encounter, and the correct response to a marker
    that says "deleted" is to keep reading, because the next row may be the live
    namesake. So the deleted case is not an error here at all, and exhausting the
    rows is an honest None.

    That is exactly why the UNREADABLE case cannot be folded into it. This
    function's None already means one specific thing, "this library has no active
    genre by that name", and the plan turns it into a per-row ``genre-unknown``
    skip. Collapsing an unreadable marker into that None would report a binding
    regression as thousands of skips naming the user's taxonomy, sending them to
    fix a taxonomy that was never wrong. The failure is not per-row and it is not
    about genres, so it does not get a per-row genre-shaped answer. ``None`` is
    refused alongside a missing attribute because ``bool(None)`` is the same
    permissive answer.
    """
    if not genre_name:
        return None
    for row in db.get_genre(Name=genre_name):
        marker = getattr(row, rb_writer.SOFT_DELETE_COLUMN, _MARKER_ABSENT)
        if marker is _MARKER_ABSENT or marker is None:
            raise refuse(
                "soft-delete-marker-unreadable",
                f"the genre row {getattr(row, 'ID', '?')!r} cannot say whether "
                f"it is a tombstone, and treating that as 'not deleted' would "
                f"point a track's genre at a row rekordbox has already retired",
                remedy=Remedy.RUN_DOCTOR,
                scope=Scope.RUN,
                origin=("write", "metadata"),
                detail={
                    "table": "djmdGenre",
                    "row_id": str(getattr(row, "ID", "")),
                    "column": rb_writer.SOFT_DELETE_COLUMN,
                    "genre": genre_name,
                },
            )
        if not marker:
            return row.ID
    return None


# ---------------------------------------------------------------------------
# The plan: one shape, serving the preview and the apply
# ---------------------------------------------------------------------------


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
    """A row the plan could not propose a change for, and why.

    Surfaced rather than raised. One unresolvable genre is not a reason to abandon
    a sweep, and a silent skip is how a person comes to believe a sweep ran.
    """

    content_id: str
    reason: str
    detail: str = ""


@dataclass(frozen=True, slots=True)
class Plan:
    """Every proposed change and every skip, for one operation over one row set.

    THE SAME OBJECT SERVES THE DRY RUN AND THE APPLY. Two code paths that both
    describe the work are two code paths that can disagree, and the one that
    disagrees silently is the preview, because nobody checks a preview against
    anything afterwards.
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
    """What an apply actually did, counted by decision.

    Counts are derived from the decisions the writer returned, never accumulated
    alongside them, so the report cannot drift from the writes it describes.
    """

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
        return tuple(
            cid for cid, d in self.applied if d is rb_writer.Decision.WRITE
        )


# ---------------------------------------------------------------------------
# Planning each operation. Pure, and none of them opens a session.
# ---------------------------------------------------------------------------


def plan_title_padding(
    rows: Iterable[Any], *, template: naming.NameTemplate
) -> Plan:
    """Zero-pad the Camelot head on each title that carries an unpadded one.

    Idempotence is a property of the SELECTION, not of the transform: an already
    padded head produces an identical string, which never becomes a change here
    and would report ``skip_same`` even if it did. Padding runs through
    :func:`naming.pad_head`, which splices the key's own span and leaves every
    other byte alone. The source system's two hand-rolled copies disagreed with
    each other, and one of them prepended a second head onto titles that already
    had one.
    """
    changes: list[Change] = []
    skipped: list[Skipped] = []
    for row in rows:
        content_id = str(getattr(row, "ID", "") or "")
        current = getattr(row, "Title", None)
        if not current:
            skipped.append(Skipped(content_id, "no-title"))
            continue
        padded = naming.pad_head(str(current), template=template)
        if padded == str(current):
            continue
        changes.append(Change(content_id, PAD_CAMELOT, "Title", current, padded))
    return Plan(PAD_CAMELOT, tuple(changes), tuple(skipped))


def plan_genre_retag(
    rows: Iterable[Any], genres: Mapping[str, str], *, db: Any
) -> Plan:
    """Link each row to the existing lookup row for its reviewed genre name.

    A name with no lookup row is skipped and surfaced. Creating one is refused
    structurally as well: ``djmdGenre`` is absent from
    ``rb_writer.PERMITTED_ROW_TABLES``, so even a caller that tried would be
    rolled back at the commit. Belt and braces, deliberately.

    EACH DISTINCT NAME IS RESOLVED ONCE. A sweep names a handful of genres over
    hundreds of rows, and a lookup per row asked the same question of the
    database hundreds of times.
    """
    changes: list[Change] = []
    skipped: list[Skipped] = []
    resolved: dict[str, Any | None] = {}
    for row in rows:
        content_id = str(getattr(row, "ID", "") or "")
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
            Change(
                content_id,
                RETAG_GENRE,
                "GenreID",
                getattr(row, "GenreID", None),
                genre_id,
            )
        )
    return Plan(RETAG_GENRE, tuple(changes), tuple(skipped))


def rating_for(level: int, cuts: Sequence[taxonomy.RatingCut]) -> int | None:
    """The star value for an energy level, read off the taxonomy's own curve.

    The curve is the user's, declared in their taxonomy, so the numbers are never
    written here. The source system hardcoded three of them in a module comment
    and a fourth somewhere else.
    """
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

    TWO SCALES, ONE HOME FOR THE CONVERSION. A rekordbox xml spells five stars
    255, and the taxonomy's cuts are written on that scale because the export
    writer consumes them as they stand. The database stores 0 to 5, read off a
    real library at the eleventh attended sitting: six distinct values and no
    byte anywhere. So a cut value crosses into the database here and nowhere
    else, and the export path never calls this.

    A value already on the star scale passes through, so a taxonomy that
    declares stars directly means what it says. Zero is unrated on both scales
    and comes back as zero. Anything else is refused rather than guessed at,
    because the only alternative is writing it as it stands into a field whose
    largest value is 5.
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

    A curve is on ONE scale. Each value folding on its own is not enough: cuts
    of 51 and 3 both fold, to one star and three, and the database path would
    plan something plausible from a curve the export writer spells as nearly
    unrated at the top. A mix is a typo in the template, so it is refused here
    rather than resolved in either direction. Zero belongs to both scales.
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
    """Fill a star rating from an energy level, on rows that carry no rating.

    The rating planned is a database star, 1 to 5, folded from the taxonomy's
    export scale by :func:`database_stars`. The whole curve is folded BEFORE any
    row is planned, so a curve holding one value that means nothing refuses the
    whole plan rather than the rows that happen to land in that cut. A partial
    plan over a misdeclared curve would read as a sweep that worked. A cut that
    declares zero leaves its band unrated on purpose, so its rows are skipped as
    ``level-unrated`` and the rest of the plan stands.

    Fill-if-empty is enforced by the policy rather than by a check written here.
    A row whose rating a person set reaches :func:`rb_writer.metadata_decision`
    and comes back ``skip_present``, which is the same answer this function would
    have produced and one fewer place for the two to disagree (P2).
    """
    curve = _database_curve(cuts)
    changes: list[Change] = []
    skipped: list[Skipped] = []
    for row in rows:
        content_id = str(getattr(row, "ID", "") or "")
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
            Change(
                content_id,
                RATING_BACKFILL,
                "Rating",
                getattr(row, "Rating", None),
                stars,
            )
        )
    return Plan(RATING_BACKFILL, tuple(changes), tuple(skipped))


# ---------------------------------------------------------------------------
# Applying a plan
# ---------------------------------------------------------------------------


def write_plan(
    plan: Plan,
    rows_by_id: Mapping[str, Any],
    *,
    policies: Mapping[str, rb_writer.FieldPolicy] | None = None,
) -> Report:
    """Apply every change in a plan and report what each one decided.

    DOES NOT COMMIT. The caller batches, then calls
    :func:`rb_writer.commit_guarded`, whose structural whitelist is the backstop
    underneath this semantic layer. Splitting it that way is what lets one
    session carry several operations and still be judged once.

    A change naming a row the caller did not supply is surfaced rather than
    raised, for the same reason every other skip is.
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

    The decision function already answers ``SKIP_UNOWNED`` for such a change, so
    applying one is harmless. This exists because harmless is not the same as
    correct: a sweep that silently writes nothing looks exactly like a sweep with
    nothing to do, and the difference is a bug the user cannot see.
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
    "plan_genre_retag",
    "plan_rating_backfill",
    "plan_title_padding",
    "rating_for",
    "resolve_genre_id",
]
