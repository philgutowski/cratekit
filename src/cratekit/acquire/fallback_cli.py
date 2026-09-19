"""``acquire.fallback``: second source candidates for the rows a provider does not carry.

R-404's search half. ``crate acquire fallback PATH`` reads a text list, the
unlisted list ``intake missing`` writes or any list ``match run`` reads,
resolves every row against the library exactly as ``intake missing --list``
does, and searches SoundCloud and then YouTube for each row that is still
missing. What comes back is ranked and OFFERED into the ``fallback-source``
review queue, one item per row. Nothing is picked and nothing downloads here.

A ROW WITH A PROVIDER ROUTE IS NOT SEARCHED. A row carrying the provider's own
id, and a row whose provider candidate is waiting in review or was accepted
there, already has a route to a lossless download, and a second source offer
beside it would ask a person to choose a worse copy of a track they are about
to get. A row whose provider candidates were all rejected is exactly the row
this verb is for, and it is searched. WHAT THIS CANNOT SEE: a row the
provider's text search would list without a person leaves no trace in the
queue, so run ``intake missing --list`` first and pass the rows it could not
route; asking the provider again here would spend a login on every run.

THE QUEUE BEFORE THE SEARCH. A row already offered, answered or rejected here
spends no search, so a second run over the same list offers nothing twice.

AN OUTAGE NAMES WHAT WAS ALREADY OFFERED. Unlike the provider search, each row
is offered as its answer arrives, because a second source is two slow
subprocesses a row and a list of forty should not be searched again from the
top because the thirty first failed. So a search that fails refuses the verb
and names every item this run already put in front of a person, and the next
run skips those and carries on.

NO CANDIDATE ANYWHERE IS REPORTED, NEVER SILENT. A run that offered nothing,
has nothing waiting and nothing accepted, over missing rows, refuses: a no-op
would read exactly like a list the library already holds.

Not gated and not destructive: it writes nothing but review items.
"""

from __future__ import annotations

import shlex
from pathlib import Path
from typing import Any

from cratekit.acquire import fallback, match, match_cli
from cratekit.cli.output import Envelope
from cratekit.core import binaries, review
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import candidates, missing_cli

#: The verb's origin on every refusal it raises.
ORIGIN = ("acquire.fallback",)


def searcher() -> fallback.FallbackSearcher:
    """The searcher a run uses, looked up on the module at call time.

    THE NETWORK SEAM. The suite replaces this function, so no test ever builds
    the shipped searcher and no test ever runs ``yt-dlp``.
    """
    return fallback.yt_dlp_searcher()


def build(parser, entry) -> None:
    parser.add_argument(
        "list",
        help=(
            "a text list, the unlisted list intake missing wrote or any tracklist, "
            "whose missing tracks to search for on SoundCloud and YouTube"
        ),
    )
    parser.set_defaults(_handler=acquire_fallback)


def _check(key: str, status: str, detail: str) -> dict[str, Any]:
    return {"key": f"acquire.fallback.{key}", "title": key, "status": status,
            "detail": detail, "remedy": None}


def _binary_refusal(exc: binaries.BinaryNotFound, subject: dict[str, Any]) -> CratekitError:
    """A missing ``yt-dlp`` as this verb's refusal, the install hint and all.

    The binaries module already decided which of its situations this is, so
    the remedy IS its token: install, install from source, or fix the override.
    The hint travels as data for the command line layer to render (D2).
    """
    hint = exc.hint
    return refuse(
        "yt-dlp-missing",
        f"{exc} A second source search runs it, so no row was searched and nothing "
        f"was offered.",
        remedy=Remedy(exc.remedy.value),
        steps=(
            (f"install {', '.join(hint.packages)} with {hint.manager}, then run it again",)
            if hint is not None
            else ()
        ),
        scope=Scope.RUN,
        origin=ORIGIN,
        detail={
            "binary": exc.binary,
            "override": binaries.env_var(exc.binary),
            "manager": str(hint.manager) if hint is not None else None,
            "packages": list(hint.packages) if hint is not None else [],
            **subject,
        },
    )


def _named(proposals: list[fallback.Proposal]) -> str:
    return "; ".join(
        f"{one.wanted.artist} - {one.wanted.listed} ({one.item_id})" for one in proposals
    )


def _outage(
    exc: Exception,
    wanted: match.Wanted,
    offered: list[fallback.Proposal],
    subject: dict[str, Any],
) -> CratekitError:
    return refuse(
        "unavailable-transient",
        f"the second source search for {wanted.artist} - {wanted.listed} failed "
        f"({exc}); "
        + (
            f"{len(offered)} row(s) were already offered for review this run and "
            f"stay offered: {_named(offered)}"
            if offered
            else "nothing was offered this run"
        ),
        remedy=Remedy.RETRY_LATER,
        steps=(
            "run it again later; a row already offered is not searched again",
            "if this one row fails on every run, take it out of the list and run it again",
        ),
        scope=Scope.RUN,
        origin=ORIGIN,
        detail={
            "artist": wanted.artist,
            "title": wanted.listed,
            "offered": [one.to_json() for one in offered],
            **subject,
        },
    )


def acquire_fallback(ctx) -> Envelope:
    """Offer second source candidates for a list's missing rows, or say why not."""
    path = Path(str(ctx.args.list)).expanduser().absolute()
    subject: dict[str, Any] = {"list_in": str(path)}
    cfg = match_cli._load()
    wanted = match_cli.read_list(path)
    music = Path(cfg.library.root) / cfg.library.music_dir
    if not music.is_dir():
        # AN ABSENT LIBRARY IS NOT AN EMPTY ONE. Every row would resolve missing
        # and every track the library holds would be searched for elsewhere.
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no row of "
            f"the list can be told from a track the library already holds",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME,
            origin=ORIGIN,
            detail={"music": str(music), **subject},
        )
    index, suppresses, identify = match_cli.library_view(cfg)
    resolved = match.resolve_all(wanted, index, suppresses=suppresses, suppression_id=identify)
    if resolved.of(match.MatchState.NEEDS_REVIEW):
        with review.open_store(cfg) as items:
            resolved = match_cli.adjudicate(
                items,
                resolved,
                handler_key=ctx.entry.handler_key,
                suppresses=suppresses,
                suppression_id=identify,
            )
    counts = {"owned": 0, "offered": 0, "suppressed": 0, "missing": 0}
    missing: list[match.Wanted] = []
    seen: set[str] = set()
    for one in resolved.matches:
        if one.state is match.MatchState.MATCHED:
            counts["owned"] += 1
        elif one.state is match.MatchState.NEEDS_REVIEW:
            counts["offered"] += 1
        elif one.state is match.MatchState.SUPPRESSED:
            counts["suppressed"] += 1
        else:
            counts["missing"] += 1
            # ONE ROW PER QUESTION, on the fallback item's own identity. The
            # match identifier carries the musical key and the question does
            # not, so the same track typed with and without a key would be
            # searched twice and reported offered twice under one item.
            asked = fallback.item_id(one.wanted)
            if asked not in seen:
                seen.add(asked)
                missing.append(one.wanted)

    provider_routed: list[match.Wanted] = []
    proposals: list[fallback.Proposal] = []
    offered_now: list[fallback.Proposal] = []
    if missing:
        with review.open_store(cfg) as items:
            held: list[tuple[match.Wanted, fallback.Proposal | None]] = []
            for one in missing:
                if missing_cli.provider_ref(one):
                    # THE PROVIDER'S OWN ID IS A ROUTE. ``intake missing --list``
                    # lists such a row without a search, and a lossless download
                    # of it is one command away.
                    provider_routed.append(one)
                    continue
                on_provider = candidates.settled(items, one)
                if on_provider is not None and on_provider.state in (
                    candidates.WAITING,
                    candidates.ACCEPTED,
                ):
                    provider_routed.append(one)
                    continue
                held.append((one, fallback.settled(items, one)))
            found: fallback.FallbackSearcher | None = None
            for one, said in held:
                if said is not None:
                    proposals.append(said)
                    continue
                if found is None:
                    try:
                        found = searcher()
                    except binaries.BinaryNotFound as exc:
                        raise _binary_refusal(exc, subject) from exc
                try:
                    answer = fallback.search_all(found, one)
                except CratekitError:
                    raise
                except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
                    raise _outage(exc, one, offered_now, subject) from exc
                made = fallback.propose(items, one, answer, handler_key=ctx.entry.handler_key)
                proposals.append(made)
                if made.state == fallback.OFFERED:
                    offered_now.append(made)

    def of(*states: str) -> list[fallback.Proposal]:
        return [one for one in proposals if one.state in states]

    waiting = of(fallback.OFFERED, fallback.WAITING)
    accepted = of(fallback.ACCEPTED)
    unfound = of(fallback.NO_CANDIDATES, fallback.REJECTED, fallback.STALLED)
    if unfound and not waiting and not accepted and not provider_routed:
        raise refuse(
            "intake-list-unusable",
            f"{len(unfound)} missing track(s) and no second source has a candidate for "
            f"any of them, so nothing was offered and nothing is waiting in review: "
            + "; ".join(f"{one.wanted.artist} - {one.wanted.listed}: {one.reason}" for one in unfound),
            steps=(
                "find these tracks by hand, a purchase or a promo copy, and ingest "
                "the file with intake file",
                "a rejected or stalled row is searched again after: crate review clear ITEM_ID",
            ),
            origin=ORIGIN,
            detail={"tracks": [one.to_json() for one in unfound], **subject},
        )
    review_command = f"crate review list --queue {fallback.QUEUE} --kind {fallback.KIND}"
    again = shlex.join(["crate", "acquire", "fallback", str(path)])
    if offered_now:
        said = (
            f"{len(offered_now)} missing track(s) offered for review with second source "
            f"candidates: {_named(offered_now)}; see: {review_command}"
        )
    elif waiting or accepted:
        said = "nothing new to offer: every row with candidates was offered on an earlier run"
    elif provider_routed:
        said = "nothing searched: every missing track has a provider route in review"
    else:
        said = "nothing searched: no track in this list is missing"
    checks = [
        _check("offered", "ok" if offered_now else "info", said),
        _check("owned", "info", f"{counts['owned']} already in the library, not searched"),
        _check(
            "version",
            "info",
            f"{counts['offered']} held in another version, offered for review and not "
            f"searched; see: crate review list",
        ),
        _check("suppressed", "info", f"{counts['suppressed']} deleted on purpose, not searched"),
        _check(
            "provider",
            "info",
            f"{len(provider_routed)} missing track(s) carry the provider's own id or "
            f"have a provider candidate waiting or accepted in review, and are not "
            f"searched elsewhere"
            + (
                ": " + "; ".join(f"{one.artist} - {one.listed}" for one in provider_routed)
                if provider_routed
                else ""
            ),
        ),
        _check(
            "waiting",
            "info",
            f"{len(waiting)} missing track(s) are waiting in review with second source "
            f"candidates; answer them with crate review resolve",
        ),
        _check(
            "accepted",
            "info",
            f"{len(accepted)} second source candidate(s) accepted in review; nothing in "
            f"this build downloads them yet"
            + (
                ": " + "; ".join(
                    f"{one.wanted.artist} - {one.wanted.listed}: {one.url}" for one in accepted
                )
                if accepted
                else ""
            ),
        ),
        _check(
            "unfound",
            "fail" if unfound else "ok",
            f"{len(unfound)} missing track(s) have no second source candidate to offer: "
            + "; ".join(f"{one.wanted.artist} - {one.wanted.listed}: {one.reason}" for one in unfound)
            if unfound
            else "every missing track searched has candidates in review or a provider route",
        ),
    ]
    summary = {
        **subject,
        "missing": counts["missing"],
        "owned": counts["owned"],
        "offered": counts["offered"],
        "suppressed": counts["suppressed"],
        "provider_routed": len(provider_routed),
        "fallback_offered": len(offered_now),
        "waiting": len(waiting),
        "accepted": len(accepted),
        "unfound": len(unfound),
        "review_next": review_command if waiting else None,
        "again": again,
        "rows": [one.to_json() for one in proposals],
    }
    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        outcome=Outcome.OK if offered_now else Outcome.NO_OP,
    )


__all__ = ["ORIGIN", "acquire_fallback", "build", "searcher"]
