"""``label.approved``: the list document for the label releases a person accepted.

R-402's acquire half. A label sweep offers each new release into the review
queue, a person accepts or rejects it, and until this verb the answer went
nowhere: ``review resolve`` records a verdict and produces nothing acquirable.
This verb reads every ACCEPTED release on the label queue, reads its tracks
again from the provider, resolves each against the library, and hands the
missing ones to the one emitter, :func:`cratekit.acquire.listdoc.write`, with a
manifest that says which label, which year and which release each came from.

THE REVIEW ITEM'S PAYLOAD NAMES THE RELEASE AND NOTHING ELSE IS TAKEN FROM IT
ABOUT A TRACK. A payload written before R-379 carries a memory address where
the artist belongs, and 98 such rows sit on the live queue. Every artist and
title in the list comes from the provider's own track rows, read by release
identifier through :meth:`~cratekit.label.catalogue.Catalogue.release_tracks`.
The label's identifier and name do travel from the payload into the manifest,
as provenance and never as a key: R-381 records that an accented name yields a
mangled identifier, so nothing here looks anything up by one.

THERE IS NO HANDED OFF STATE, and that is what makes a second run safe.
Ownership is the record. A track downloaded and landed since the last run
resolves owned and is left out, so the verb may be run after every review
sitting and lists only what is still owed. The list's name carries a digest of
the identifiers it lists: the same work writes the same bytes to the same name,
which the emitter recognises, and different work takes a different name rather
than meeting the emitter's refusal to replace a file holding something else.

ONLY MISSING IS LISTED, on the rule ``intake missing`` states. A track the
library holds in another version is a question, offered into the match queue
the way an intake offers it, and an answer already given is read back, so a
person who said "that is not the same record" finds the track listed next run.
The same recording on two accepted releases, a single and the album it came
from, is listed once under the first.

A RELEASE THAT CANNOT BE READ IS NAMED AND THE REST STILL LIST. One withdrawn
release among ninety must not hold the other eighty nine, so it becomes a
failing check carrying its identifier and the step that settles it. What is
refused outright is a run that read NO release, or listed nothing while some
could not be read, because reported as a no-op either reads exactly like a
library that already holds everything. A ``CratekitError`` from the seam passes
through untouched: an expired session fails every release the same way, and the
act it names is the person's to take once.

Not gated and not destructive: it writes two new files and the emitter refuses
rather than replaces. Nothing here composes ``acquire download``, so nothing
here can spend a download.
"""

from __future__ import annotations

import hashlib
import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.acquire import listdoc, match, match_cli
from cratekit.cli.output import Envelope
from cratekit.core import review
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.review import Queue
from cratekit.intake.missing_cli import LISTS_DIR
from cratekit.label import catalogue, sweep
from cratekit.label import cli as label_cli

#: What the provenance sidecar says a listed row came from. ``intake land``
#: reads exactly this word to find the rows it files under the labels tree.
PROVENANCE_SOURCE = "label"

#: What every list this verb writes is named after, before the digest.
LIST_PREFIX = "label-approved"

#: How many bytes of digest a list's name carries, as twice that many hex
#: characters. Six bytes is 48 bits, and a collision costs a refusal to replace
#: a file, never a wrong list. Asked of the hash as its size rather than sliced
#: off a longer one, so this module holds no bare integer an exit code could be
#: mistaken for, which is a population ``tests/test_reserved_causes.py`` pins.
DIGEST_BYTES = 6


def build_approved(parser, entry) -> None:
    parser.add_argument(
        "--out",
        default=None,
        metavar="DIR",
        help="folder to write the list into (default: the lists folder under download staging)",
    )
    parser.set_defaults(_handler=label_approved)


def _unusable(message: str, *steps: str, **detail: Any):
    return refuse(
        "label-list-unusable",
        message,
        steps=steps,
        origin=("label.approved",),
        detail=detail,
    )


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return {"key": f"label.approved.{key}", "title": key, "status": status,
            "detail": detail, "remedy": None}


@dataclass(frozen=True, slots=True)
class _Release:
    """One accepted review item, reduced to what names and places its release."""

    item_id: str
    release_id: str
    title: str
    label_id: str | None
    label_name: str | None


@dataclass(frozen=True, slots=True)
class _Failed:
    release: _Release
    gone: bool
    why: str


def _text(value: Any) -> str | None:
    """A payload value as text, or ``None``. Only a string is believed."""
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()


def _release_of(items: review.ReviewStore, item: review.Item) -> _Release:
    """The release an accepted item names, from its IDENTITY before its payload.

    The identity is what the item is addressed by and is what the sweep keyed
    on. An item that arrived through ``review import`` carries none, because
    the export format does not, and then the payload's own copy of the
    identifier is all there is. An item naming no release at all is kept, with
    an empty identifier, so it is reported as a failure rather than skipped.
    """
    identity = review.identity_of(items, item.item_id) or {}
    release_id = _text(identity.get("release_id")) or _text(item.payload.get("identity")) or ""
    return _Release(
        item_id=item.item_id,
        release_id=release_id,
        title=_text(item.payload.get("title")) or "",
        label_id=_text(item.payload.get("label_id")),
        label_name=_text(item.payload.get("label_name")),
    )


def _queued(items: review.ReviewStore) -> tuple[list[_Release], int, int]:
    """The accepted releases in queue order, and how many were rejected or open.

    An item whose stored verdict this build cannot read counts as OPEN, which
    is the direction ``review`` argues for everywhere: undecided rather than
    decided the wrong way.
    """
    page = review.list_items(
        items,
        queue=str(Queue.LABEL_RELEASE),
        kinds=(sweep.KIND,),
        include_resolved=True,
        limit=None,
    )
    accepted: list[_Release] = []
    rejected = still_open = 0
    for item in page.items:
        if item.verdict is review.Verdict.ACCEPTED:
            accepted.append(_release_of(items, item))
        elif item.verdict is review.Verdict.REJECTED:
            rejected += 1
        else:
            still_open += 1
    return accepted, rejected, still_open


def _tracks_or_failure(
    found: catalogue.Catalogue, release: _Release
) -> tuple[tuple[match.Wanted, ...], int | None] | _Failed:
    """One release's tracks as ``Wanted`` rows and its year, or why there are none.

    THE FIRST CALLER OF ``release_tracks`` OWNS ITS FAILURE PATHS. Two exception
    shapes arrive and neither is this module's to predict, the argument
    ``label_cli.playlist_tracks_or_refuse`` makes: the provider's own error once
    the retry ladder is spent, and the listing module's plain ``RuntimeError``
    for a truncated or unpageable listing. So the catch is broad, bounded by the
    ``CratekitError`` passthrough above it. A ``LookupError`` is the seam's
    contract for a release the provider has nothing for, and is reported as
    gone, which no retry will change.
    """
    if not release.release_id:
        return _Failed(release, gone=False, why="the review item names no release identifier")
    try:
        rows, year = found.release_tracks(release.release_id)
        return match.read_tidal_tracks(rows), year
    except CratekitError:
        raise
    except LookupError as exc:
        return _Failed(release, gone=True, why=str(exc))
    except Exception as exc:  # noqa: BLE001 - named per release, never swallowed
        return _Failed(release, gone=False, why=f"{type(exc).__name__}: {exc}")


def _out_dir(ctx, cfg) -> Path:
    given = ctx.args.out
    if given:
        out = Path(str(given)).expanduser().absolute()
    else:
        out = cfg.paths.download_staging / LISTS_DIR
    if out.exists() and not out.is_dir():
        raise _unusable(
            f"{out} exists and is not a folder, so no list can be written into it",
            "name a folder with --out",
            out=str(out),
        )
    return out


def list_name(listed: tuple[str, ...]) -> str:
    """The name a list of exactly these identifiers, in this order, is written under."""
    digest = hashlib.blake2s("\n".join(listed).encode("utf-8"), digest_size=DIGEST_BYTES)
    return f"{LIST_PREFIX}-{digest.hexdigest()}"


def _named(release: _Release) -> str:
    said = f"release {release.release_id or '(no identifier)'}"
    if release.title:
        said += f" ({release.title!r}"
        said += f" on {release.label_name})" if release.label_name else ")"
    return said


def _failure_check(failed: _Failed) -> dict[str, Any]:
    release = failed.release
    if failed.gone:
        detail = (
            f"{_named(release)} is gone from the provider and none of it is in the "
            f"list ({failed.why}); waiting will not bring it back, so revoke its "
            f"acceptance with: crate review clear {release.item_id}"
        )
    else:
        detail = (
            f"{_named(release)} could not be read and none of it is in the list "
            f"({failed.why}); run this again once the provider answers"
        )
    return _check(f"release.{release.release_id or release.item_id}", "fail", detail)


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
        # ASKED BEFORE THE CATALOGUE IS RESOLVED, so a queue with nothing
        # accepted spends no login and refuses over no missing credential.
        return ctx.envelope(
            data={
                "checks": [
                    _check("written", "info", "nothing listed: no label release is accepted"),
                    queue_check,
                ],
                "summary": _summary(None, accepted=0, rejected=rejected, open=still_open),
            },
            outcome=Outcome.NO_OP,
        )

    # LOOKED UP ON THE MODULE AT CALL TIME, the contract ``catalogue`` states,
    # which is what lets a suite substitute the seam.
    found = catalogue.resolve(cfg)
    index, suppresses, identify = match_cli.library_view(cfg)

    counts = {"owned": 0, "offered": 0, "suppressed": 0, "duplicate": 0, "missing": 0}
    failures: list[_Failed] = []
    undated: list[_Release] = []
    missing: list[match.Wanted] = []
    origins: list[tuple[_Release, int | None]] = []
    seen: set[str] = set()
    read = 0
    for release in accepted:
        outcome = _tracks_or_failure(found, release)
        if isinstance(outcome, _Failed):
            failures.append(outcome)
            continue
        wanted, year = outcome
        read += 1
        if year is None:
            undated.append(release)
        resolved = match.MatchResult(
            matches=tuple(
                match.resolve_one(one, index, suppresses=suppresses, suppression_id=identify)
                for one in wanted
            )
        )
        if resolved.of(match.MatchState.NEEDS_REVIEW):
            # THE REVIEW STORE IS OPENED ONLY FOR A QUESTION, as the intake
            # worker opens it, and the offer is idempotent on the question.
            with review.open_store(cfg) as items:
                resolved = match_cli.adjudicate(
                    items,
                    resolved,
                    handler_key=ctx.entry.handler_key,
                    suppresses=suppresses,
                    suppression_id=identify,
                )
        for settled in resolved.matches:
            if settled.state is match.MatchState.MATCHED:
                counts["owned"] += 1
            elif settled.state is match.MatchState.NEEDS_REVIEW:
                counts["offered"] += 1
            elif settled.state is match.MatchState.SUPPRESSED:
                counts["suppressed"] += 1
            elif settled.match_id in seen:
                counts["duplicate"] += 1
            else:
                seen.add(settled.match_id)
                counts["missing"] += 1
                missing.append(settled.wanted)
                origins.append((release, year))

    failed_detail = [
        {"release_id": one.release.release_id, "item_id": one.release.item_id,
         "gone": one.gone, "why": one.why}
        for one in failures
    ]
    if not read:
        # NO RELEASE READ IS NOT NOTHING MISSING. A no-op here would read like a
        # library that holds every approved release, over a provider nobody
        # got an answer from.
        raise _unusable(
            f"none of the {len(accepted)} accepted release(s) could be read from the "
            f"provider, so nothing is known about what they hold and nothing was "
            f"written: " + "; ".join(f"{_named(one.release)}: {one.why}" for one in failures),
            "run this again once the provider answers",
            "a release that is gone stays gone; revoke its acceptance with: crate "
            "review clear ITEM_ID",
            failed=failed_detail,
        )

    written = listdoc.Written(None, None, (), ())
    if missing:
        rows = listdoc.rows_of(missing)
        provenance = _provenance(rows, origins)
        try:
            _body, listed_ids, _unlisted = listdoc.document(rows)
            written = listdoc.write(
                _out_dir(ctx, cfg), list_name(listed_ids), rows, provenance
            )
        except listdoc.ListDocRefused as exc:
            raise _unusable(
                str(exc), "move the file aside or name another folder with --out"
            ) from exc
    listed = len(written.listed)
    unlisted = len(written.unlisted)
    if missing and not listed:
        raise _unusable(
            f"{unlisted} missing track(s) and none carries a provider identifier, so "
            f"there is nothing acquire download could be asked for; nothing was written",
            "this is a defect in what the provider returned for these releases; "
            "run this again, and report it if it repeats",
            unlisted_tracks=[{"artist": row.artist, "title": row.title} for row in written.unlisted],
        )
    if failures and not listed:
        # NOTHING LISTED WITH RELEASES UNREAD IS NOT A LIBRARY THAT HOLDS THEM.
        raise _unusable(
            f"nothing is missing from the {read} release(s) that could be read, and "
            f"{len(failures)} could not be, so this is not a library holding every "
            f"approved release: "
            + "; ".join(f"{_named(one.release)}: {one.why}" for one in failures),
            "run this again once the provider answers",
            "a release that is gone stays gone; revoke its acceptance with: crate "
            "review clear ITEM_ID",
            failed=failed_detail,
        )

    command = (
        shlex.join(["crate", "acquire", "download", str(written.list_path)])
        if written.list_path is not None
        else None
    )
    checks = [
        _check(
            "written",
            "ok" if listed else "info",
            f"{listed} missing track(s) from {read} accepted release(s) written to "
            f"{written.list_path}; next: {command}"
            if listed
            else f"nothing listed: the library holds every track of the {read} "
            f"accepted release(s)",
        ),
        queue_check,
        _check("owned", "info", f"{counts['owned']} already in the library, not listed"),
        _check(
            "offered",
            "info",
            f"{counts['offered']} held in another version, offered for review and not "
            f"listed until answered; see: crate review list",
        ),
        _check("suppressed", "info", f"{counts['suppressed']} deleted on purpose, not listed"),
        _check(
            "duplicate",
            "info",
            f"{counts['duplicate']} the same recording as a track already listed from "
            f"an earlier release, listed once",
        ),
        _check(
            "unlisted",
            "fail" if unlisted else "ok",
            f"{unlisted} missing track(s) carry no provider identifier and are NOT in the list"
            if unlisted
            else "every missing track is in the list",
        ),
        _check(
            "undated",
            "fail" if undated else "ok",
            f"{len(undated)} release(s) carry no year the provider could be read for, "
            f"so their manifest rows say none: "
            + ", ".join(_named(release) for release in undated)
            if undated
            else "every release read carries its year",
        ),
        _check(
            "releases",
            "fail" if failures else "ok",
            f"{len(failures)} accepted release(s) could not be read and are NOT in the list"
            if failures
            else "every accepted release was read",
        ),
        *(_failure_check(one) for one in failures),
    ]
    summary = _summary(
        written,
        accepted=len(accepted),
        rejected=rejected,
        open=still_open,
        read=read,
        next=command,
        missing=counts["missing"],
        owned=counts["owned"],
        offered=counts["offered"],
        suppressed=counts["suppressed"],
        duplicate=counts["duplicate"],
        undated=[release.release_id for release in undated],
        failed=failed_detail,
    )
    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        outcome=Outcome.OK if listed else Outcome.NO_OP,
    )


def _provenance(
    rows: tuple[listdoc.Row, ...], origins: list[tuple[_Release, int | None]]
) -> dict[str, listdoc.Provenance]:
    """Each listed id's provenance. First release wins, as the document's row does."""
    found: dict[str, listdoc.Provenance] = {}
    for row, (release, year) in zip(rows, origins, strict=True):
        ref = str(row.ref or "").strip()
        if not ref or ref in found:
            continue
        found[ref] = listdoc.Provenance(
            source=PROVENANCE_SOURCE,
            source_ref=release.release_id,
            label_id=release.label_id,
            label_name=release.label_name,
            year=year,
            release_id=release.release_id,
        )
    return found


def _summary(written: listdoc.Written | None, **fields: Any) -> dict[str, Any]:
    held = written or listdoc.Written(None, None, (), ())
    base: dict[str, Any] = {
        "list": str(held.list_path) if held.list_path is not None else None,
        "manifest": str(held.manifest_path) if held.manifest_path is not None else None,
        "next": None,
        "written": len(held.listed),
        "unlisted": len(held.unlisted),
        "unlisted_tracks": [{"artist": row.artist, "title": row.title} for row in held.unlisted],
    }
    base.update(fields)
    return base


__all__ = [
    "DIGEST_BYTES",
    "LIST_PREFIX",
    "PROVENANCE_SOURCE",
    "build_approved",
    "label_approved",
    "list_name",
]
