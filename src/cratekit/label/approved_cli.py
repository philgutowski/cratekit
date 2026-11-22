"""``label.approved``: the list document for the label releases a person accepted.

R-402's acquire half. Every ACCEPTED release on the label queue is read again
from the provider, resolved against the library, and its missing tracks handed
to the one emitter, :func:`cratekit.acquire.listdoc.write`, with a manifest
naming the label, year and release each came from. Every artist and title comes
from the provider's rows, never the payload (which can carry a memory address);
the label travels into the manifest as provenance, never as a key (R-381).

NO HANDED OFF STATE: a landed track resolves owned, so a second run lists only
what is still owed. The list's name digests WHAT IT WRITES, so the same work
writes the same bytes to the same name and other work takes a new name. Only
missing is listed; a track held in another version is offered into the match
queue, and the same recording on two releases is listed once under the first.

A RELEASE THAT CANNOT BE READ IS NAMED AND THE REST STILL LIST, with the step
its kind needs (revoke the acceptance, or ask again). A run that read nothing,
or listed nothing while some were unread, is refused, since as a no-op it reads
like a library holding everything. :data:`OUTAGE_AFTER` provider failures in a
row end the asking.

THE GENRE GATE JUDGES EVERY RELEASE READ BEFORE ANY IS LISTED: the share rule
per label over the releases read this run (U101, R-420, R-462), and the kind
rule per release on the sweep's recorded words or the general catalogue
(R-798). A held release is named and neither listed nor offered; a returned one
passes unjudged; one neither rule judged is listed on a failing ``ungated``
line. A release the library holds in full is never asked about.

Not a confirm gate and not destructive: it writes two new files and the
emitter refuses rather than replaces. Nothing here composes
``acquire download``, so nothing here can spend a download.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import shlex
from collections.abc import Callable, Container, Mapping
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any

from cratekit.acquire import listdoc, match, match_cli
from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, review, routing, taxonomy
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.review import Queue
from cratekit.intake.missing_cli import LISTS_DIR
from cratekit.label import catalogue, review_common, sweep
from cratekit.label import cli as label_cli
from cratekit.label import gate as genre_gate
from cratekit.label import registry as labels
from cratekit.label.harvest import _text

#: What the provenance sidecar says a listed row came from, the word ``intake
#: land`` reads. Not ``PROVENANCE_SOURCE``, which ``intake.missing_cli`` exports
#: with another meaning.
LABEL_SOURCE = "label"

#: What every list this verb writes is named after, before the digest.
LIST_PREFIX = "label-approved"

#: How many provider failures IN A ROW end the asking: one is a bad release, two
#: a coincidence, and each has already cost a full retry ladder.
OUTAGE_AFTER = 3

#: The four ways an accepted release yields no tracks, by what settles each.
GONE = "gone"
NO_IDENTIFIER = "no-identifier"
PROVIDER = "provider"
NOT_ASKED = "not-asked"

#: How many bytes of digest a list's name carries, as twice that many hex
#: characters; a collision costs a refusal to replace a file, never a wrong list.
#: Asked of the hash as its size, so no bare integer here reads as an exit code.
DIGEST_BYTES = 6


def build_approved(parser, entry) -> None:
    parser.add_argument(
        "--out", default=None, metavar="DIR",
        help="folder to write the list into (default: the lists folder under download staging)",
    )
    parser.set_defaults(_handler=label_approved)


def _unusable(message: str, *steps: str, **detail: Any):
    return refuse(
        "label-list-unusable", message, steps=steps, origin=("label.approved",), detail=detail
    )


def _check(
    key: str, status: str, detail: str, *, namespace: str = "label.approved"
) -> dict[str, Any]:
    return review_common.check(namespace, key, status, detail)


def _ids(release: _Release) -> dict[str, Any]:
    return {"release_id": release.release_id, "item_id": release.item_id}


@dataclass(frozen=True, slots=True)
class _Release:
    """One accepted review item, reduced to what names and places its release."""

    item_id: str
    release_id: str
    title: str
    label_id: str | None
    label_name: str | None
    #: The general catalogue's words the sweep recorded, or None (R-798).
    genres: tuple[str, ...] | None = None
    returned: bool = False


@dataclass(frozen=True, slots=True)
class _Failed:
    release: _Release
    kind: str
    why: str

    def to_json(self) -> dict[str, Any]:
        return {**_ids(self.release), "kind": self.kind, "gone": self.kind == GONE, "why": self.why}


@dataclass(frozen=True, slots=True)
class _Read:
    """One release the provider answered for: its readable rows, and the rest.

    ``genre`` is the one genre its rows report, or ``None`` with ``ungated``
    saying why the gate cannot judge it.
    """

    wanted: tuple[match.Wanted, ...]
    year: int | None
    unreadable: tuple[str, ...]
    genre: str | None = None
    ungated: str | None = None
    #: The provider's rows, where the kind gate reads its ISRCs.
    rows: tuple[Any, ...] = ()


@dataclass(frozen=True, slots=True)
class _Held:
    """One release the genre gate held, and the numbers it was held on."""

    release: _Release
    genre: str
    family: str
    of_family: int
    classified: int
    share: float

    def to_json(self) -> dict[str, Any]:
        numbers = ("genre", "family", "of_family", "classified", "share")
        return {**_ids(self.release), **{name: getattr(self, name) for name in numbers}}


@dataclass(frozen=True, slots=True)
class _OutOfKind:
    """One release held because it is not the kind of music its label is followed for."""

    release: _Release
    judged: genre_gate.Judged

    def to_json(self) -> dict[str, Any]:
        judged = self.judged
        return {
            **_ids(self.release),
            "genres": list(judged.genres), "kind": judged.kind, "reason": judged.reason,
        }


def _genre_of(rows: tuple[Any, ...]) -> tuple[str | None, str | None]:
    """The one genre a release's rows report, or ``None`` and why there is none.

    Read from a mapping or an attribute, the two shapes a provider row comes in.
    Rows that disagree are not a genre: choosing one would hold a release on a
    guess.
    """
    said: dict[str, str] = {}
    for row in rows:
        value = row.get("genre") if isinstance(row, Mapping) else getattr(row, "genre", None)
        text = _text(value)
        if text is not None:
            said.setdefault(text.casefold(), text)
    if not said:
        return None, "the catalogue reports no genre for it"
    if len(said) > 1:
        return None, "its tracks report " + " and ".join(repr(one) for one in said.values())
    return next(iter(said.values())), None


def _label_of(release: _Release) -> str:
    """What a release is grouped under for the gate: its label, else itself.

    A release naming no label is judged alone, and so never held, rather than
    against releases it shares nothing with.
    """
    return release.label_id or release.label_name or f"release:{release.release_id}"


def _gated(
    declared: taxonomy.Taxonomy, read: list[tuple[_Release, _Read]], failures: list[_Failed]
) -> tuple[dict[str, _Held], dict[str, str]]:
    """Every read release the genre gate holds, and every one it could not judge.

    Both keyed by review item. ONE CALL PER LABEL, the share being a fraction of
    its accepted releases; a label with a release unread is not judged at all.
    """
    unread = {_label_of(one.release) for one in failures}
    groups: dict[str, list[tuple[_Release, _Read]]] = {}
    for release, outcome in read:
        groups.setdefault(_label_of(release), []).append((release, outcome))
    share = declared.label_gate.out_of_place_share
    held: dict[str, _Held] = {}
    unjudged: dict[str, str] = {}
    for label, members in groups.items():
        if label in unread:
            for release, outcome in members:
                unjudged[release.item_id] = outcome.ungated or (
                    "another accepted release on its label could not be read, so the "
                    "label's share of its genre is not known"
                )
            continue
        genres = [outcome.genre for _release, outcome in members]
        verdicts = routing.gate_decisions(declared, genres)
        families = [routing.gate_family(declared, genre) for genre in genres]
        classified = sum(1 for genre in genres if genre)
        for (release, outcome), verdict, family in zip(members, verdicts, families, strict=True):
            if outcome.ungated is not None:
                unjudged[release.item_id] = outcome.ungated
            elif verdict is routing.GateVerdict.DROP and family and outcome.genre:
                held[release.item_id] = _Held(
                    release, outcome.genre, family, families.count(family), classified, share
                )
    return held, unjudged


def _judged_by_kind(
    declared: taxonomy.Taxonomy, read: list[tuple[_Release, _Read]], followed: labels.Registry,
    owned: Callable[[_Release], bool],
) -> tuple[dict[str, _OutOfKind], dict[str, str]]:
    """Every read release held as another kind of music, and every one not judged.

    Both keyed by review item, one release at a time. Recorded words first, else
    the lookup with the rows already read, except for a release ``owned`` in
    full. A returned release is not judged; an unfollowed label is the default kind.
    """
    held: dict[str, _OutOfKind] = {}
    unjudged: dict[str, str] = {}
    # One asking for the run, so an unreachable catalogue is given up on.
    asking = genre_gate.Asking()
    for release, outcome in read:
        if release.returned:
            continue
        entry = followed.by_id(release.label_id) if release.label_id else None
        kind = entry.kind if entry is not None else None
        # What the release's own record settles comes first, as in ``label
        # judge``. Its ``not-asked`` is the general catalogue's, not this
        # module's ``NOT_ASKED`` (a release the provider was not asked for).
        judged = genre_gate.judge_recorded(declared, kind, release.genres)
        if judged is None and owned(release):
            unjudged[release.item_id] = (
                "every track of it is already in the library, so the general "
                "catalogue was not asked about it"
            )
            continue
        if judged is None:
            judged = genre_gate.judge_rows(declared, kind, outcome.rows, asking)
        if judged.held:
            held[release.item_id] = _OutOfKind(release, judged)
        elif judged.verdict is routing.KindVerdict.NOT_JUDGED:
            unjudged[release.item_id] = judged.reason
    return held, unjudged


def release_of(items: review.ReviewStore, item: review.Item) -> _Release:
    """The release an accepted item names, from its IDENTITY before its payload.

    An item naming no release is kept with an empty identifier, to be reported
    as a failure. Returned by either record, the hold or the payload's word.
    """
    standing = review.find_hold(items, queue=str(Queue.LABEL_RELEASE), item_id=item.item_id)
    returned = genre_gate.returned_by(standing, item.payload)
    payload = item.payload
    return _Release(
        item.item_id, genre_gate.release_id_of(items, item), _text(payload.get("title")) or "",
        _text(payload.get("label_id")), _text(payload.get("label_name")),
        genre_gate.recorded_genres(payload, genre_gate.GENRES_FIELD), returned,
    )


def _queued(items: review.ReviewStore) -> tuple[list[_Release], int, int]:
    """The accepted releases in queue order, and how many were rejected or open.

    An item whose verdict this build cannot read counts as OPEN, undecided
    rather than decided the wrong way. A SUPERSEDED item, answered by the
    guided label sync, counts as neither (U107).
    """
    page = review.list_items(
        items, queue=str(Queue.LABEL_RELEASE), kinds=(sweep.KIND,), include_resolved=True,
        limit=None,
    )
    accepted: list[_Release] = []
    rejected = still_open = 0
    for item in page.items:
        if item.verdict is review.Verdict.ACCEPTED:
            accepted.append(release_of(items, item))
        elif item.verdict is review.Verdict.REJECTED:
            rejected += 1
        elif item.verdict is not review.Verdict.SUPERSEDED:
            still_open += 1
    return accepted, rejected, still_open


def _tracks_or_failure(found: catalogue.Catalogue, release: _Release) -> _Read | _Failed:
    """One release's tracks as ``Wanted`` rows and its year, or why there are none.

    The catch is broad, bounded by the ``CratekitError`` passthrough. Only the
    seam's own exception means gone (``LookupError`` would catch a parse
    failure). Each row is read alone, so one odd row costs only itself.
    """
    if not release.release_id:
        return _Failed(release, NO_IDENTIFIER, "the review item names no release identifier")
    try:
        rows, year, _short = found.release_tracks(release.release_id)
    except CratekitError:
        raise
    except catalogue.ReleaseUnresolvable as exc:
        return _Failed(release, GONE, str(exc))
    except Exception as exc:  # noqa: BLE001 - named per release, never swallowed
        return _Failed(release, PROVIDER, f"{type(exc).__name__}: {exc}")
    wanted: list[match.Wanted] = []
    unreadable: list[str] = []
    for row in rows:
        try:
            wanted.extend(match.read_tidal_tracks((row,)))
        except match.UnreadableList as exc:
            unreadable.append(str(exc))
    genre, ungated = _genre_of(tuple(rows))
    return _Read(tuple(wanted), year, tuple(unreadable), genre, ungated, tuple(rows))


def _out_dir(ctx, cfg) -> Path:
    staging = cfg.paths.download_staging / LISTS_DIR
    out = Path(str(ctx.args.out)).expanduser().absolute() if ctx.args.out else staging
    if out.exists() and not out.is_dir():
        raise _unusable(
            f"{out} exists and is not a folder, so no list can be written into it",
            "name a folder with --out",
            out=str(out),
        )
    return out


def list_name(
    body: Mapping[str, Any], provenance: Mapping[str, listdoc.Provenance], *,
    prefix: str = LIST_PREFIX,
) -> str:
    """The name a list of exactly these rows, from exactly these releases, takes.

    Over everything the emitter compares, the manifest's year and label
    included, so corrected work takes a new name instead of a refusal.
    """
    said = {
        "tracks": body["tracks"],
        "provenance": [
            dataclasses.asdict(provenance[track["id"]]) for track in body["tracks"]
        ],
    }
    encoded = json.dumps(said, ensure_ascii=False, sort_keys=True).encode("utf-8")
    digest = hashlib.blake2s(encoded, digest_size=DIGEST_BYTES)
    return f"{prefix}-{digest.hexdigest()}"


def _named(release: _Release) -> str:
    said = f"release {release.release_id or '(no identifier)'}"
    if release.title:
        said += f" ({release.title!r}"
        said += f" on {release.label_name})" if release.label_name else ")"
    return said


#: Each failure kind's words, before and after its reason, ending in what settles it.
_REVOKE = "so revoke its acceptance with: crate review clear {item}"
_AGAIN = "run this again once the provider answers"
_FAILED_SAID = {
    GONE: ("is gone from the provider", "waiting will not bring it back, " + _REVOKE),
    NO_IDENTIFIER: ("cannot be asked for", "running again will not change that, " + _REVOKE),
    NOT_ASKED: ("was NOT ASKED FOR", _AGAIN),
}


def _failure_check(failed: _Failed, *, namespace: str = "label.approved") -> dict[str, Any]:
    """One failing line per release, ending in the act that settles ITS kind."""
    release = failed.release
    what, settle = _FAILED_SAID.get(failed.kind, ("could not be read", _AGAIN))
    detail = (
        f"{_named(release)} {what} and none of it is in the list ({failed.why}); "
        + settle.format(item=release.item_id)
    )
    return _check(
        f"release.{release.release_id or release.item_id}", "fail", detail, namespace=namespace
    )


def _held_check(held: _Held | _OutOfKind, *, namespace: str = "label.approved") -> dict[str, Any]:
    """One line per held release, carrying what it was held on."""
    release = held.release
    if isinstance(held, _OutOfKind):
        detail = (
            f"{_named(release)} is HELD by the genre gate and none of it is in the "
            f"list: {held.judged.reason}; to list this one anyway: crate label held "
            f"return {release.release_id}; to pass its kind for the whole label: "
            f"crate label registry set LABEL --kind KIND"
        )
    else:
        label = release.label_name or release.label_id or "no named label"
        detail = (
            f"{_named(release)} is HELD by the genre gate and none of it is in the list: "
            f"its genre {held.genre!r} is the {held.family} family, {held.of_family} of "
            f"the {held.classified} release(s) with a genre accepted from {label}, "
            f"under the {held.share:.0%} share a family needs to belong to that label"
        )
    return _check(
        f"held.{release.release_id or release.item_id}", "info", detail, namespace=namespace
    )


@dataclass(frozen=True, slots=True)
class Listing:
    """What listing a set of accepted releases did, for a caller to report.

    The guided label sync's go lists down this same path (U108).
    """

    accepted: int
    read: int
    held: Mapping[str, _Held | _OutOfKind]
    failures: tuple[_Failed, ...]
    unreadable: tuple[tuple[_Release, str], ...]
    undated: tuple[_Release, ...]
    ungated: tuple[tuple[_Release, str], ...]
    counts: Mapping[str, int]
    written: listdoc.Written

    @property
    def passed(self) -> int:
        """The releases read that the genre gate did not hold."""
        return self.read - len(self.held)

    @property
    def listed(self) -> int:
        return len(self.written.listed)

    @property
    def command(self) -> str | None:
        """The command that downloads the list, or None when none was written."""
        if self.written.list_path is None:
            return None
        return shlex.join(["crate", "acquire", "download", str(self.written.list_path)])


def list_releases(
    cfg, accepted: list[_Release], *, out: Callable[[], Path], handler_key: str,
    prefix: str = LIST_PREFIX, already: Container[str] = frozenset(),
    excuse: Container[str] = frozenset(), elsewhere: str = "name another folder with --out",
) -> Listing:
    """Read, gate, resolve and list the missing tracks of ``accepted``, or refuse.

    ``out`` is asked for only when there is something to write. ``already`` names
    track ids another job holds, counted ``queued``. ``excuse`` names failure
    KINDS that alone do not make an empty listing a refusal. ``elsewhere`` is
    the remedy for a folder that cannot take the list.
    """
    # The taxonomy and the registry before the first login (R-685, R-798): an
    # unreadable one refuses here, not after every release was fetched.
    declared = active_taxonomy.load(cfg)
    followed = labels.RegistryStore().load()
    # Looked up on the module at call time, so a suite can substitute the seam.
    found = catalogue.resolve(cfg)
    index, suppresses, identify = match_cli.library_view(cfg)

    counts = dict.fromkeys(("owned", "offered", "suppressed", "duplicate", "missing", "queued"), 0)
    failures: list[_Failed] = []
    undated: list[_Release] = []
    unreadable: list[tuple[_Release, str]] = []
    missing: list[match.Wanted] = []
    origins: list[tuple[_Release, int | None]] = []
    seen: set[str] = set()
    answered: list[tuple[_Release, _Read]] = []
    in_a_row = 0
    for release in accepted:
        if in_a_row >= OUTAGE_AFTER:
            failures.append(_Failed(release, NOT_ASKED, (
                f"the provider failed {OUTAGE_AFTER} releases in a row, so the "
                f"rest were not spent on it"
            )))
            continue
        outcome = _tracks_or_failure(found, release)
        if isinstance(outcome, _Failed):
            failures.append(outcome)
            # Only a provider that did not answer counts: gone is an answer.
            in_a_row = in_a_row + 1 if outcome.kind == PROVIDER else 0
            continue
        in_a_row = 0
        answered.append((release, outcome))
        unreadable.extend((release, why) for why in outcome.unreadable)
    read = len(answered)

    # The gate before any offer, so a held release is never offered or listed.
    # A release is UNJUDGED only when neither rule judged it. Each release is
    # resolved once here, a read writing nothing, for the kind rule's question
    # whether the library holds it in full and for the listing loop below.
    by_share, unjudged = _gated(declared, answered, failures)
    resolutions = {
        release.item_id: tuple(
            match.resolve_one(one, index, suppresses=suppresses, suppression_id=identify)
            for one in outcome.wanted
        )
        for release, outcome in answered
    }
    rows_unread = {release.item_id for release, _why in unreadable}

    def fully_owned(release: _Release) -> bool:
        """Every row read, and every one already in the library. At least one."""
        return release.item_id not in rows_unread and sweep.every_track_owned(
            resolutions[release.item_id]
        )

    by_kind, kind_unjudged = _judged_by_kind(declared, answered, followed, fully_owned)
    held: dict[str, _Held | _OutOfKind] = {**by_share, **by_kind}
    ungated = [
        (release, f"{unjudged[release.item_id]}, and {kind_unjudged[release.item_id]}")
        for release, _outcome in answered
        if release.item_id in unjudged and release.item_id in kind_unjudged
    ]
    for release, outcome in answered:
        if release.item_id in held:
            continue
        year = outcome.year
        if year is None:
            undated.append(release)
        resolved = match.MatchResult(matches=resolutions[release.item_id])
        if any(match_cli.touches_the_queue(one) for one in resolved.matches):
            # The review store is opened only when a row touches it, and the
            # offer is idempotent on the question.
            with review.open_store(cfg) as items:
                resolved = match_cli.adjudicate(
                    items, resolved, handler_key=handler_key, suppresses=suppresses,
                    suppression_id=identify,
                )
        for settled in resolved.matches:
            word = match_cli.SETTLED_WORDS.get(settled.state)
            if word is not None:
                counts[word] += 1
            elif settled.match_id in seen:
                counts["duplicate"] += 1
            elif str(settled.wanted.ref or "").strip() in already:
                # Another job already holds it, so a second start never asks
                # the provider for a track twice (U108).
                seen.add(settled.match_id)
                counts["queued"] += 1
            else:
                seen.add(settled.match_id)
                counts["missing"] += 1
                missing.append(settled.wanted)
                origins.append((release, year))

    failed_detail = [one.to_json() for one in failures]
    why_failed = "; ".join(f"{_named(one.release)}: {one.why}" for one in failures)
    # A failure the caller excused is still reported by its own failing line.
    unexcused = [one for one in failures if one.kind not in excuse]
    settle = (
        "run this again once the provider answers",
        "a release that is gone, or an item naming no release, stays that way; "
        "revoke its acceptance with: crate review clear ITEM_ID",
    )
    if not read and (unexcused or not failures):
        # No release read is not nothing missing.
        raise _unusable(
            f"none of the {len(accepted)} accepted release(s) could be read from the "
            f"provider, so nothing is known about what they hold and nothing was "
            f"written: {why_failed}",
            *settle,
            failed=failed_detail,
        )

    written = listdoc.Written(None, None, (), ())
    if missing:
        rows = listdoc.rows_of(missing)
        provenance = _provenance(rows, origins)
        try:
            body, _listed, _unlisted = listdoc.document(rows)
            folder, name = out(), list_name(body, provenance, prefix=prefix)
            written = listdoc.write(folder, name, rows, provenance)
        except listdoc.ListDocRefused as exc:
            raise _unusable(str(exc), f"move the file aside, or {elsewhere}") from exc
        except OSError as exc:
            # A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL. Let through,
            # it reads as an internal error asking a person to report a defect.
            raise _unusable(
                f"the list could not be written ({type(exc).__name__}: "
                f"{exc.strerror or exc}); nothing acquire download could read was "
                f"left behind",
                f"{elsewhere}, or make this one writable",
                path=str(exc.filename or ""),
            ) from exc
    listed = len(written.listed)
    if missing and not listed:
        raise _unusable(
            f"{len(written.unlisted)} missing track(s) and none carries a provider identifier, so "
            f"there is nothing acquire download could be asked for; nothing was written",
            "this is a defect in what the provider returned for these releases; "
            "run this again, and report it if it repeats",
            unlisted_tracks=_tracks(written.unlisted),
        )
    if unexcused and not listed:
        # Nothing listed with releases unread is not a library that holds them.
        raise _unusable(
            f"nothing is missing from the {read - len(held)} release(s) that could be read"
            + (f" and passed the genre gate ({len(held)} more held by it)" if held else "")
            + f", and {len(failures)} could not be, so this is not a library holding "
            f"every approved release: {why_failed}",
            *settle,
            failed=failed_detail,
        )
    return Listing(
        len(accepted), read, held, tuple(failures), tuple(unreadable), tuple(undated),
        tuple(ungated), counts, written,
    )


def listing_checks(listing: Listing, *, namespace: str = "label.approved") -> list[dict[str, Any]]:
    """Every line a listing reports, after the caller's own ``written`` line."""
    counts = listing.counts
    unlisted = len(listing.written.unlisted)

    check = partial(_check, namespace=namespace)

    def tally(key: str, found: Any, said: str, fine: str) -> dict[str, Any]:
        """A line that fails when ``found`` holds anything, and says ``fine`` otherwise."""
        return check(key, "fail" if found else "ok", said if found else fine)

    return [
        check("owned", "info", f"{counts['owned']} already in the library, not listed"),
        check("offered", "info", f"{counts['offered']} held in another version, offered "
              "for review and not listed until answered; see: crate review list"),
        check("suppressed", "info", f"{counts['suppressed']} deleted on purpose, not listed"),
        check("duplicate", "info", f"{counts['duplicate']} the same recording as a track "
              "already listed from an earlier release, listed once"),
        tally(
            "unlisted", unlisted,
            f"{unlisted} missing track(s) carry no provider identifier and are NOT in the list",
            "every missing track is in the list",
        ),
        tally(
            "unreadable", listing.unreadable,
            f"{len(listing.unreadable)} track row(s) the provider returned could not be "
            f"read and are NOT in the list: "
            + "; ".join(f"{_named(release)}: {why}" for release, why in listing.unreadable),
            "every track row the provider returned was read",
        ),
        tally(
            "undated", listing.undated,
            f"{len(listing.undated)} release(s) carry no year the provider could be read "
            f"for, so their manifest rows say none: "
            + ", ".join(_named(release) for release in listing.undated),
            "every release the genre gate passed carries its year",
        ),
        check(
            "held",
            "info",
            f"{len(listing.held)} accepted release(s) held by the genre gate and NOT in "
            f"the list: " + ", ".join(_named(one.release) for one in listing.held.values())
            if listing.held
            else "no release was held by the genre gate",
        ),
        tally(
            "ungated", listing.ungated,
            f"{len(listing.ungated)} release(s) the genre gate could not judge, so they "
            f"are listed unjudged: "
            + "; ".join(f"{_named(release)}: {why}" for release, why in listing.ungated),
            "every release read was judged by the genre gate",
        ),
        tally(
            "releases", listing.failures,
            f"{len(listing.failures)} accepted release(s) could not be read and are NOT "
            f"in the list",
            "every accepted release was read",
        ),
        *(_failure_check(one, namespace=namespace) for one in listing.failures),
        *(_held_check(one, namespace=namespace) for one in listing.held.values()),
    ]


#: The counts the summary carries, in its order.
_SUMMED = ("missing", "owned", "offered", "suppressed", "duplicate")


def label_approved(ctx) -> Envelope:
    """List the missing tracks of every accepted label release, or say why not."""
    cfg = label_cli._load()
    with review.open_store(cfg) as items:
        accepted, rejected, still_open = _queued(items)
    queue_check = _check(
        "queue",
        "info",
        f"{len(accepted)} accepted release(s) read; {rejected} rejected and "
        f"{still_open} not yet answered were not; see: crate review list --queue "
        f"{Queue.LABEL_RELEASE}",
    )
    if not accepted:
        # ASKED BEFORE THE CATALOGUE IS RESOLVED, so nothing accepted spends a login.
        checks = [_check("written", "info", "nothing listed: no label release is accepted")]
        summary = _summary(None, accepted=0, rejected=rejected, open=still_open)
        return review_common.ended(ctx, [*checks, queue_check], summary, Outcome.NO_OP)

    listing = list_releases(
        cfg, accepted, out=lambda: _out_dir(ctx, cfg), handler_key=ctx.entry.handler_key
    )
    written, listed, held, passed = listing.written, listing.listed, listing.held, listing.passed
    command = listing.command
    checks = [
        _check(
            "written",
            "ok" if listed else "info",
            f"{listed} missing track(s) from {passed} accepted release(s) written to "
            f"{written.list_path}; next: {command}"
            if listed
            # A held release was never resolved, so the library is not said to hold it.
            else f"nothing listed: the library holds every track of the {passed} "
            f"accepted release(s) the genre gate passed, and {len(held)} more were "
            f"held by it"
            if held
            else f"nothing listed: the library holds every track of the {listing.read} "
            f"accepted release(s)",
        ),
        queue_check,
        *listing_checks(listing),
    ]
    summary = _summary(
        written,
        accepted=len(accepted), rejected=rejected, open=still_open, read=listing.read, next=command,
        **{word: listing.counts[word] for word in _SUMMED},
        unreadable=len(listing.unreadable),
        undated=[release.release_id for release in listing.undated],
        held=[one.to_json() for one in held.values()],
        ungated=[release.release_id for release, _why in listing.ungated],
        failed=[one.to_json() for one in listing.failures],
    )
    return review_common.ended(ctx, checks, summary, Outcome.OK if listed else Outcome.NO_OP)


def _provenance(
    rows: tuple[listdoc.Row, ...], origins: list[tuple[_Release, int | None]]
) -> dict[str, listdoc.Provenance]:
    """Each listed id's provenance. First release wins, as the document's row does."""
    found: dict[str, listdoc.Provenance] = {}
    for row, (release, year) in zip(rows, origins, strict=True):
        ref = str(row.ref or "").strip()
        if ref and ref not in found:
            found[ref] = listdoc.Provenance(
                source=LABEL_SOURCE, source_ref=release.release_id, label_id=release.label_id,
                label_name=release.label_name, year=year, release_id=release.release_id,
            )
    return found


def _tracks(rows: Any) -> list[dict[str, Any]]:
    return [{"artist": row.artist, "title": row.title} for row in rows]


def _summary(written: listdoc.Written | None, **fields: Any) -> dict[str, Any]:
    held = written or listdoc.Written(None, None, (), ())
    return {
        "list": str(held.list_path) if held.list_path is not None else None,
        "manifest": str(held.manifest_path) if held.manifest_path is not None else None,
        "next": None,
        "written": len(held.listed),
        "unlisted": len(held.unlisted),
        "unlisted_tracks": _tracks(held.unlisted),
        **fields,
    }


__all__ = [
    "DIGEST_BYTES", "GONE", "LABEL_SOURCE", "LIST_PREFIX", "NOT_ASKED", "Listing", "NO_IDENTIFIER",
    "OUTAGE_AFTER", "PROVIDER", "build_approved", "label_approved", "list_name", "list_releases",
    "listing_checks", "release_of",
]
