"""Declines and tombstones, on the revocable decision stores U11 shipped.

R35 and R36 both say REVOCABLE. A private ledger would remember and offer no way
back, which is the worst one way door to build in the part that removes music. So
both stores are :class:`cratekit.core.review.DecisionStore`: content addressed,
idempotent, revocation stamped on the kept record, a positive field by field read
that refuses what it cannot recognise, and the read then write cycle under a
sibling lock. None of that is re-implemented here.

**TWO STORES.** A decline is about one ROW and one file: leave it. A tombstone is
about a RECORDING that outlives the row: never acquire it again. One store would
make revoking a decline un-suppress an acquisition.

Layer note: MODULES. Every store key and kind comes from ``cratekit.core.tombstone``,
below both this and the acquisition passes that consult the same records.
"""

from __future__ import annotations

import ast
import enum
import functools
import hashlib
import inspect
import json
import re
import textwrap
import types
import weakref
from typing import Any, Callable, Mapping

from cratekit.core import config, review, tombstone
from cratekit.deletion import library
from cratekit.deletion.library import VERSION_IS_A_DESIGNATION, VERSION_IS_AN_ARTIST, RemovedRow


def declines(cfg: config.Config) -> review.DecisionStore:
    """R35's store: files a person looked at and decided to keep."""
    return review.DecisionStore(tombstone.DECLINE_STORE_KEY, cfg)


def tombstones(cfg: config.Config) -> review.DecisionStore:
    """R36's store: versions this library has deliberately stopped holding."""
    return review.DecisionStore(tombstone.STORE_KEY, cfg)


def row_identity(row: RemovedRow) -> dict[str, str]:
    return tombstone.removed_file_identity(content_id=row.content_id, recorded=row.recorded)


def version_of(row: RemovedRow) -> dict[str, str]:
    """This row's version identity, with the mix name composed into the title.

    Two remixes of one recording often share a bare ``Title`` with the mix in
    ``RemixerName`` or ``Subtitle``, so composing is what makes the identity
    unique; the rules live in ``core.tombstone``.

    The consulter (:func:`suppressed_version`) composes nothing, since a provider
    hands one title with the mix inside, so the RECORDER must produce exactly
    that string. A ``RemixerName`` is an artist name, so it is spelled through
    ``tombstone.remixer_title`` (``Strobe (Michael Woods Remix)``, never
    ``strobe (michael woods)``).
    """
    if row.version_kind == VERSION_IS_AN_ARTIST:
        title = tombstone.remixer_title(row.title, row.version)
    else:
        title = tombstone.version_title(row.title, row.version)
    return tombstone.version_identity(artist=row.artist, title=title)


def uncredited_version_of(row: RemovedRow) -> dict[str, str] | None:
    """This row's identity with its featured credits taken out, or None (R-431).

    The companion a provider that never spells the guest can reach. Built on top
    of :func:`version_of`, never inside it, so the column rules are decided once
    and the identity stamp does not move. None for a row with no bracketed
    credit; see ``tombstone.uncredited_title`` and ``KIND_VERSION_UNCREDITED``.
    """
    verbatim = version_of(row)
    stripped = tombstone.uncredited_title(verbatim["title"])
    if not stripped:
        return None
    return tombstone.version_identity(artist=verbatim["artist"], title=stripped)


#: The payload field on a companion naming the tombstone it was written beside,
#: for the listing. A shared companion names only the row that arrived first.
CREDITED_ID_FIELD = "credited_id"

#: The pointer from the other end: the field on a TOMBSTONE naming its companion,
#: empty for a row with no credit. A LOOKUP, so a changed stripping rule cannot
#: strand a companion nobody can lift.
UNCREDITED_ID_FIELD = "uncredited_id"

#: The payload field carrying the composition rules a tombstone's identity was
#: written under, named once for the writer and the reader.
IDENTITY_SCHEME_FIELD = "identity_scheme"

#: Prefix on the stamp. ``is2_`` measures the rules themselves as well as probe
#: outputs, where ``is1_`` measured outputs only; the prefix lets a person reading
#: a payload tell which question the value answered.
_SCHEME_PREFIX = "is2_"


class _SchemeProbe:
    """A collection row, shaped as far as ``library._version_of`` reads one.

    A column the reader starts reading that this lacks answers empty through
    ``library._text``, a narrower measurement rather than a raise.
    """

    __slots__ = ("RemixerName", "Subtitle")

    def __init__(self, remixer: str, subtitle: str) -> None:
        self.RemixerName = remixer
        self.Subtitle = subtitle


#: The rows :func:`identity_scheme` reads and composes, as raw column values.
#:
#: FROZEN, AND NOT A TEST FIXTURE: each makes a branch of the reader or the
#: composer observable in the stamp (absent column, remixer believed, subtitle
#: believed and not, both filled, bare and bracketed versions, tidying, credits,
#: version words, remixer designations, the fold, and each single empty field).
#:
#: Editing this tuple moves the stamp, the safe direction: a differing stamp
#: falls back to the row lookup, while a wrongly MATCHING one is the failure.
_SCHEME_PROBES: tuple[tuple[str, str, str, str], ...] = (
    # artist, title, RemixerName, Subtitle
    ("deadmau5", "Strobe", "", ""),
    ("deadmau5", "Strobe", "", "Extended Mix"),
    ("deadmau5", "Strobe Extended Mix", "", "Extended Mix"),
    ("deadmau5", "Strobe (Extended Mix)", "", "Extended Mix"),
    ("deadmau5", "Strobe [Extended Mix]", "", "Extended Mix"),
    ("deadmau5", "Strobe", "", " Extended  Mix "),
    ("deadmau5", "Strobe", "", "[Extended Mix]"),
    ("deadmau5", "Strobe", "", "(Mix)"),
    ("deadmau5", "Strobe", "", "Anjunadeep"),
    ("deadmau5", "Strobe", "Michael Woods", "Extended Mix"),
    ("Fisher", "Losing It (feat. Anna)", "Anna", ""),
    ("Fisher", "Losing It (Live with Strings)", "", "Live"),
    ("Bob Marley", "Lively Up", "", "Live"),
    ("deadmau5", "Strobe", "Michael Woods", ""),
    ("deadmau5", "Strobe", "Michael Woods Remix", ""),
    ("deadmau5", "Strobe", "The Cut", ""),
    ("deadmau5", "Strobe", " Michael Woods ", ""),
    ("deadmau5", "Strobe", "[Michael Woods]", ""),
    ("deadmau5", "Strobe (Michael Woods Remix)", "Michael Woods", ""),
    ("DEADMAU5", "  Strobe   Mix  ", "", ""),
    ("deadmau5", "Ströbe", "", ""),
    ("", "Strobe", "", "Extended Mix"),
    ("deadmau5", "", "", "Extended Mix"),
)


#: The package the walk below follows into; a function outside it is named in
#: the digest and not read.
_OWN_PACKAGE = "cratekit"

#: Parsed code, keyed by the function or class object (a rebound function misses
#: the cache and is read afresh). Weak, so a replacement a test binds is not held.
_PARSED: weakref.WeakKeyDictionary[Any, tuple[str, list[list[str]]]] = weakref.WeakKeyDictionary()


def _collect(node: ast.AST, paths: list[list[str]]) -> None:
    """Every name this code mentions, except the ones it only ever RAISES with.

    Following raises reached the whole error catalogue, which moves with every
    unit's messages and never with a composition. A raised value is never
    returned, so nothing built in a ``raise`` reaches an identity; WHETHER it
    fires is still in the function's own source. Both a chain and its root name
    are collected (``tombstone.version_title``, ``VERSION_WORDS.intersection``).
    """
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.Raise):
            continue
        if isinstance(child, ast.Attribute):
            chain = _dotted(child)
            if chain is not None:
                paths.append(chain)
        elif isinstance(child, ast.Name):
            paths.append([child.id])
        _collect(child, paths)


def _read(obj: Any) -> tuple[str, list[list[str]]]:
    """One function's normalised code and every global name it mentions, parsed once."""
    try:
        return _PARSED[obj]
    except (KeyError, TypeError):
        pass
    tree = ast.parse(textwrap.dedent(inspect.getsource(obj)))
    node = tree.body[0]
    body = getattr(node, "body", None)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        del body[0]
    paths: list[list[str]] = []
    _collect(tree, paths)
    parsed = (ast.unparse(tree), paths)
    try:
        _PARSED[obj] = parsed
    except TypeError:  # noqa: S110 - an object that cannot be weakly held is read every time
        pass
    return parsed


def _normalised_source(obj: Any) -> str:
    """One function's or class's code, docstring dropped, as ``ast.unparse`` spells it.

    Prose cannot move the stamp; unparsed source rather than bytecode, which
    moves with the interpreter. A future unparser that differs moves the value,
    the safe direction. ``docs/mutation/u24-round-11.md`` has the tables.
    """
    return _read(obj)[0]


def _stable_value(value: Any) -> Any:
    """A module level constant as something JSON can hold and two processes agree on.

    Containers are ORDERED first (a frozenset iterates by hash seed), and a repr
    carrying an address is dropped to its type.
    """
    if value is None or isinstance(value, (bool, int, float, str)):
        return ["literal", type(value).__name__, value]
    if isinstance(value, enum.Enum):
        return ["enum", type(value).__module__, type(value).__qualname__, value.name]
    if isinstance(value, re.Pattern):
        return ["pattern", value.pattern, value.flags]
    if isinstance(value, bytes):
        return ["bytes", value.hex()]
    if isinstance(value, (set, frozenset)):
        return ["set", sorted(json.dumps(_stable_value(item), sort_keys=True) for item in value)]
    if isinstance(value, (tuple, list)):
        return ["sequence", [_stable_value(item) for item in value]]
    if isinstance(value, Mapping):
        return [
            "mapping",
            sorted(
                [json.dumps(_stable_value(key), sort_keys=True), _stable_value(item)]
                for key, item in value.items()
            ),
        ]
    shown = repr(value)
    if " at 0x" in shown or " object at " in shown:
        return ["opaque", type(value).__module__, type(value).__qualname__]
    return ["opaque", type(value).__module__, type(value).__qualname__, shown]


def _dotted(node: ast.AST) -> list[str] | None:
    """An attribute chain as its dotted parts, or None where its root is not a name."""
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if not isinstance(node, ast.Name):
        return None
    parts.append(node.id)
    parts.reverse()
    return parts


def _referenced_paths(obj: Any) -> list[list[str]]:
    """Every global name and attribute chain this code mentions, see :func:`_collect`."""
    return _read(obj)[1]


def _composition_rules() -> dict[str, Any]:
    """Everything reachable from ``library._version_of``, which decides what is
    BELIEVED, and :func:`version_of`, which decides what is COMPOSED."""
    return _rules_reachable_from(library._version_of, version_of)


def _rules_reachable_from(*roots: Any) -> dict[str, Any]:
    """Everything reachable from these roots, keyed by where it is defined.

    COMPUTED, NOT ENUMERATED: a hand list of the rules has a hole one helper
    below it after the next change. Each root's code is read, every global it
    mentions resolved, and those inside :data:`_OWN_PACKAGE` followed; anything
    else is named and not read. Locals, arguments and builtins do not resolve
    and are skipped. Taking roots lets the same walk show that
    :func:`_row_coordinates` reaches no composition rule.
    """
    reached: dict[str, Any] = {}
    queue: list[Any] = list(roots)
    while queue:
        obj = queue.pop()
        key = f"code:{getattr(obj, '__module__', '?')}.{getattr(obj, '__qualname__', obj)}"
        if key in reached:
            continue
        try:
            reached[key] = _normalised_source(obj)
        except Exception:  # noqa: BLE001 - a body nobody can read is still a node
            reached[key] = ["source-unavailable", str(getattr(obj, "__qualname__", obj))]
            continue
        namespace = getattr(obj, "__globals__", None)
        if namespace is None:
            module = inspect.getmodule(obj)
            namespace = vars(module) if module is not None else {}
        for path in _referenced_paths(obj):
            if path[0] not in namespace:
                continue
            root = namespace[path[0]]
            try:
                value = functools.reduce(getattr, path[1:], root)
            except Exception:  # noqa: BLE001 - an unresolvable chain names nothing
                continue
            if isinstance(value, types.ModuleType):
                continue
            # Keyed by where it is DEFINED, so two spellings of one rule are one entry.
            if isinstance(root, types.ModuleType):
                named = f"{root.__name__}.{'.'.join(path[1:])}"
            else:
                named = f"{obj.__module__}.{'.'.join(path)}"
            defined_in = getattr(value, "__module__", None)
            if isinstance(value, (types.FunctionType, type)) and str(defined_in).startswith(
                _OWN_PACKAGE
            ):
                queue.append(value)
            elif callable(value) and not isinstance(value, (types.FunctionType, type)):
                reached.setdefault(f"foreign:{named}", ["foreign-callable", named])
            elif callable(value):
                reached.setdefault(f"foreign:{named}", ["foreign", str(defined_in), named])
            else:
                reached.setdefault(f"value:{named}", _stable_value(value))
    return reached


def _digest_record(digest: Any, value: Any) -> None:
    digest.update(json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    digest.update(b"\x1e")


def identity_scheme() -> str:
    """What THIS build turns a collection row into, as one comparable value.

    A measurement, not a number somebody remembers to bump. The rules are
    digested through :func:`_composition_rules`, which walks to them, and then
    the probes run as the check that the walk reaches the code that runs. The
    walk can be too wide (a stamp that moves sends a record to the row lookup,
    which is safe); the probes alone were too narrow (U24 round 11). Computed on
    demand, never at import, and part of no identity: it only tells
    :func:`tombstone_predicate` which question to ask of a stored record.
    """
    digest = hashlib.sha256()
    for name, encoded in sorted(_composition_rules().items()):
        _digest_record(digest, [name, encoded])
    for artist, title, remixer, subtitle in _SCHEME_PROBES:
        version, kind, unbelieved = library._version_of(_SchemeProbe(remixer, subtitle))
        composed = version_of(
            RemovedRow(
                content_id="probe",
                recorded="",
                sequence=0,
                size=None,
                artist=artist,
                title=title,
                version=version,
                version_kind=kind or VERSION_IS_A_DESIGNATION,
                version_unbelieved=unbelieved,
            )
        )
        _digest_record(digest, [composed, version, kind, unbelieved])
    return f"{_SCHEME_PREFIX}{digest.hexdigest()[:16]}"


def _row_coordinates(content_id: Any, recorded: Any) -> tuple[str, str] | None:
    """Which ROW a record names, raw and uncomposed, or None where it names none.

    Asks :func:`tombstone.removed_file_identity` rather than copying its guard.
    The one local decision: a missing ``recorded`` reads as the empty path, not
    ``'None'``, which would collide with a path literally spelled so. A refusal
    is None, since a record naming no row matches no row.
    """
    try:
        identity = tombstone.removed_file_identity(
            content_id=content_id, recorded="" if recorded is None else recorded
        )
    except Exception:  # noqa: BLE001 - a record naming no row matches no row
        return None
    return (identity["content_id"], identity["recorded"])


def ambiguous_versions(rows: Any) -> frozenset[str]:
    """The rows whose version identity is shared with a row that is a DIFFERENT recording.

    A legitimate convergence (one recording filed under two conventions) and a
    collision (two recordings a closed vocabulary left with one bare title) are
    the same shape to the identity. The ISRC tells them apart: one recording
    carries one code. Codes are folded with ``tombstone.fold_code``, so case and
    the hyphenated display form are one code (``fold`` keeps punctuation). An
    absent code is no evidence; only two present, different codes refuse. This
    bounds the vocabulary's worse error, suppressing a track nobody deleted.
    """
    grouped: dict[tuple[tuple[str, str], ...], list[RemovedRow]] = {}
    for row in rows:
        try:
            identity = version_of(row)
        except Exception:  # noqa: BLE001 - a row with no identity collides with nothing
            continue
        grouped.setdefault(tuple(sorted(identity.items())), []).append(row)
    ambiguous: set[str] = set()
    for sharing in grouped.values():
        codes = {tombstone.fold_code(row.isrc or "") for row in sharing}
        codes.discard("")
        if len(codes) > 1:
            ambiguous.update(row.content_id for row in sharing)
    return frozenset(ambiguous)


def identifiable(row: RemovedRow) -> bool:
    """Whether a tombstone COULD be written for this row, asked before anything moves.

    Both identities: the version's for the tombstone (R36), and the row's for
    the review item, the decline and the suppression identifier.
    """
    try:
        version_of(row)
        row_identity(row)
    except Exception:  # noqa: BLE001 - the refusal is the answer, not the exception
        return False
    return True


def decline_predicate(cfg: config.Config) -> Callable[[RemovedRow], bool]:
    """A predicate over the declines, from ONE read of the store, so every row in
    one pass is judged against the same set."""
    held = frozenset(record.suppression_id for record in declines(cfg).suppressions())

    def declined(row: RemovedRow) -> bool:
        return (
            review.suppression_id_for(
                tombstone.DECLINE_STORE_KEY, tombstone.KIND_REMOVED_FILE, row_identity(row)
            )
            in held
        )

    return declined


def tombstone_predicate(cfg: config.Config) -> Callable[[RemovedRow], bool]:
    """Whether a run has already RECORDED the deletion of this row's version.

    Tells a resumed deletion (trashed and recorded) from a file somebody moved
    (nothing recorded), which ``GONE`` alone cannot. One read, as
    ``decline_predicate``. Revoked records count: the question is history.

    A record carrying THIS build's :data:`IDENTITY_SCHEME_FIELD` is matched on
    its identity. Any other stamp, or none, was composed by rules this build
    does not have, so it is matched on the raw ``content_id`` and ``recorded``
    it names, which no composition rule can move; an unstamped record needs no
    migration. Matching every record on its row would retire a row whose
    version column was edited since.
    """
    scheme = identity_scheme()
    records = tombstones(cfg).suppressions(include_revoked=True)
    held = frozenset(record.suppression_id for record in records)
    rows_recorded_under_other_rules = frozenset(
        coordinates
        for record in records
        if record.kind == tombstone.KIND_VERSION
        and str(record.payload.get(IDENTITY_SCHEME_FIELD) or "") != scheme
        for coordinates in (
            _row_coordinates(record.payload.get("content_id"), record.payload.get("recorded")),
        )
        if coordinates is not None
    )

    def recorded(row: RemovedRow) -> bool:
        if _row_coordinates(row.content_id, row.recorded) in rows_recorded_under_other_rules:
            return True
        try:
            identity = version_of(row)
        except Exception:  # noqa: BLE001 - a row with no identity has no tombstone
            # False, which re-offers; True would retire a confirmed removal.
            return False
        return (
            review.suppression_id_for(tombstone.STORE_KEY, tombstone.KIND_VERSION, identity) in held
        )

    return recorded


def record_decline(
    cfg: config.Config, row: RemovedRow, *, actor: str, resolved: str | None = None
) -> review.Suppression:
    """Remember that a person said to keep this file (R35)."""
    return declines(cfg).record(
        kind=tombstone.KIND_REMOVED_FILE,
        identity=row_identity(row),
        payload={
            "artist": row.artist,
            "title": row.title,
            "recorded": row.recorded,
            "resolved": resolved or "",
        },
        actor=actor,
    )


def revoke_decline(cfg: config.Config, suppression_id: str, *, actor: str) -> review.Suppression:
    """Lift a decline, so the file is offered again on the next run (R35)."""
    return declines(cfg).revoke(suppression_id, actor=actor)


def record_tombstone(
    cfg: config.Config, row: RemovedRow, *, actor: str, trashed_to: str | None = None
) -> review.Suppression:
    """Suppress this exact version from future acquisition (R36).

    The ISRC rides in the PAYLOAD, not the identity, since a provider often has
    none (``core.tombstone``). The row's own ``version`` and the value NOT
    believed ride beside the composed title for the audit of a miss, and the
    stamp of the rules that composed the identity rides with it
    (:func:`identity_scheme`). ``trashed_to`` is empty where this pass moved
    nothing.

    ONE WRITE FOR THE TOMBSTONE AND ITS COMPANION, the companion only when the
    tombstone is written: the caller puts the file back when this raises. A
    tombstone that already stood gains nothing, so a companion lifted alone
    stays lifted (residual "A credited tombstone written before the companion
    existed still misses the provider shape").
    """
    store = tombstones(cfg)
    uncredited = uncredited_version_of(row)
    uncredited_id = (
        review.suppression_id_for(
            tombstone.STORE_KEY, tombstone.KIND_VERSION_UNCREDITED, uncredited
        )
        if uncredited is not None
        else ""
    )
    identity = version_of(row)
    companion = {
        "artist": row.artist,
        "title": row.title,
        "version": row.version,
        CREDITED_ID_FIELD: review.suppression_id_for(
            tombstone.STORE_KEY, tombstone.KIND_VERSION, identity
        ),
    }
    return store.record(
        kind=tombstone.KIND_VERSION,
        identity=identity,
        payload={
            "artist": row.artist,
            "title": row.title,
            "version": row.version,
            "version_unbelieved": row.version_unbelieved,
            "isrc": row.isrc or "",
            "content_id": row.content_id,
            "recorded": row.recorded,
            IDENTITY_SCHEME_FIELD: identity_scheme(),
            "trashed_to": trashed_to or "",
            UNCREDITED_ID_FIELD: uncredited_id,
        },
        actor=actor,
        beside=((tombstone.KIND_VERSION_UNCREDITED, uncredited, companion),)
        if uncredited is not None
        else (),
    )


def _accounts_for(credited: review.Suppression) -> frozenset[str]:
    """The companion identifiers one tombstone accounts for, by the pointer and by
    stripping, since each alone loses one."""
    found = {str(credited.payload.get(UNCREDITED_ID_FIELD) or "")}
    identity = credited.identity or {}
    stripped = tombstone.uncredited_title(str(identity.get("title") or ""))
    if stripped:
        found.add(
            review.suppression_id_for(
                tombstone.STORE_KEY,
                tombstone.KIND_VERSION_UNCREDITED,
                tombstone.version_identity(
                    artist=str(identity.get("artist") or ""), title=stripped
                ),
            )
        )
    return frozenset(found - {""})


def _companions_to_lift(
    named: review.Suppression, records: Mapping[str, review.Suppression]
) -> tuple[str, ...]:
    """The companions that go when this tombstone goes. Asked under the lock.

    A companion stays while another STANDING tombstone still accounts for it:
    two rows crediting two guests share one. The companion's own pointer back is
    for the listing; it could find nothing :func:`_accounts_for` does not.
    """
    if named.kind != tombstone.KIND_VERSION:
        return ()
    mine = _accounts_for(named)
    still_accounted_for: set[str] = set()
    for other in records.values():
        if (
            other.kind == tombstone.KIND_VERSION
            and other.suppressing
            and other.suppression_id != named.suppression_id
        ):
            still_accounted_for |= _accounts_for(other)
    return tuple(sorted(mine - still_accounted_for))


def revoke_tombstone(cfg: config.Config, suppression_id: str, *, actor: str) -> review.Suppression:
    """Lift a tombstone, and its companion with it, making that version acquirable (R36).

    One write, decided under the store's lock, so there is no half lifted state.
    A companion named directly is lifted alone, leaving the credited spelling
    suppressed under the tombstone the listing names as ``credited_id``.
    """
    return tombstones(cfg).revoke(suppression_id, actor=actor, also=_companions_to_lift)


def list_tombstones(
    cfg: config.Config, *, include_revoked: bool = False
) -> tuple[review.Suppression, ...]:
    """Every tombstone, R36's LISTABLE half; revoked ones on request, for the audit."""
    return tombstones(cfg).suppressions(include_revoked=include_revoked)


def suppressed_version(cfg: config.Config, *, artist: str, title: str) -> bool:
    """Whether this library has deliberately stopped holding that version.

    The DELETION side's own consult. An acquisition pass never imports from
    here, since either feature can be switched off; it asks through
    ``core.tombstone``. A store that cannot be read refuses.
    """
    return tombstones(cfg).suppresses(
        tombstone.KIND_VERSION, tombstone.version_identity(artist=artist, title=title)
    )


def summarize(record: review.Suppression) -> Mapping[str, Any]:
    """One suppression projected for a listing or a structured payload.

    Every field that answers "why did this tombstone miss" is emitted, empty
    included: ``version``, ``version_unbelieved``, the code, the scheme (empty is
    an era before the stamp), and ``trashed_to``, whose empty value says this
    pass moved nothing (``run._settle_a_confirmed_absence``). A credited
    deletion's two records name each other.
    """
    return {
        "id": record.suppression_id,
        "kind": record.kind,
        "identity": tombstone.describe(record.identity or {}),
        "artist": record.payload.get("artist", ""),
        "title": record.payload.get("title", ""),
        "version": record.payload.get("version", ""),
        "version_unbelieved": record.payload.get("version_unbelieved", ""),
        "isrc": record.payload.get("isrc", ""),
        CREDITED_ID_FIELD: record.payload.get(CREDITED_ID_FIELD, ""),
        UNCREDITED_ID_FIELD: record.payload.get(UNCREDITED_ID_FIELD, ""),
        IDENTITY_SCHEME_FIELD: record.payload.get(IDENTITY_SCHEME_FIELD, ""),
        "trashed_to": record.payload.get("trashed_to", ""),
        "recorded": record.recorded,
        "actor": record.actor,
        "revoked": record.revoked,
    }


__all__ = [
    "CREDITED_ID_FIELD",
    "IDENTITY_SCHEME_FIELD",
    "UNCREDITED_ID_FIELD",
    "ambiguous_versions",
    "decline_predicate",
    "declines",
    "identifiable",
    "identity_scheme",
    "list_tombstones",
    "record_decline",
    "record_tombstone",
    "revoke_decline",
    "revoke_tombstone",
    "row_identity",
    "summarize",
    "suppressed_version",
    "tombstone_predicate",
    "tombstones",
    "uncredited_version_of",
    "version_of",
]
