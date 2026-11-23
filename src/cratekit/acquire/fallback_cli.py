"""``acquire.fallback``: second source candidates for the rows a provider does not carry.

``crate acquire fallback PATH`` searches SoundCloud then YouTube for each list row the
library lacks and that has no provider route, offering the hits for review; nothing is
picked or downloaded. ``crate acquire fallback-fetch PATH`` (U81) queues each accepted
row for a lossy, marked download into staging, tagged from the row.
"""

from __future__ import annotations

import shlex
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from cratekit.acquire import cli as acquire_cli
from cratekit.acquire import fallback, match, match_cli
from cratekit.acquire.adapter import AdapterSettings, decide_lossless
from cratekit.cli.output import Envelope
from cratekit.core import binaries, binary_refusal, config, jobs, naming, review, tags
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import candidates, missing_cli

#: The verb's origin on every refusal it raises.
ORIGIN = ("acquire.fallback",)


def searcher() -> fallback.FallbackSearcher:
    """The searcher a run uses, looked up at call time so the suite can replace it."""
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


def _named(proposals: list[fallback.Proposal]) -> str:
    return "; ".join(
        f"{one.wanted.artist} - {one.wanted.listed} ({one.item_id})" for one in proposals
    )


def _outage(
    exc: Exception, wanted: match.Wanted, offered: list[fallback.Proposal], subject: dict[str, Any],
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
            "artist": wanted.artist, "title": wanted.listed,
            "offered": [one.to_json() for one in offered], **subject,
        },
    )


def missing_rows(
    ctx, path: Path, subject: dict[str, Any]
) -> tuple[config.Config, dict[str, int], list[match.Wanted]]:
    """The list's rows the library does not hold, one per question, and the counts."""
    cfg = match_cli._load()
    wanted = match_cli.read_list(path)
    music = Path(cfg.library.root) / cfg.library.music_dir
    if not music.is_dir():
        # An absent library is not an empty one; every row would resolve missing.
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no row of "
            f"the list can be told from a track the library already holds",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME, origin=ORIGIN,
            detail={"music": str(music), **subject},
        )
    index, suppresses, identify = match_cli.library_view(cfg)
    resolved = match.resolve_all(wanted, index, suppresses=suppresses, suppression_id=identify)
    if any(match_cli.touches_the_queue(one) for one in resolved.matches):
        with review.open_store(cfg) as items:
            resolved = match_cli.adjudicate(
                items, resolved, handler_key=ctx.entry.handler_key, suppresses=suppresses,
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
            # One row per question, on the fallback item's identity, which ignores
            # the musical key the match identifier carries.
            asked = fallback.item_id(one.wanted)
            if asked not in seen:
                seen.add(asked)
                missing.append(one.wanted)
    return cfg, counts, missing


def provider_routed(items: review.ReviewStore, one: match.Wanted) -> bool:
    """Whether a provider id or a waiting or accepted provider candidate routes this row."""
    if missing_cli.provider_ref(one):
        return True
    on_provider = candidates.settled(items, one)
    return on_provider is not None and on_provider.state in (
        candidates.WAITING, candidates.ACCEPTED,
    )


def acquire_fallback(ctx) -> Envelope:
    """Offer second source candidates for a list's missing rows, or say why not."""
    path = Path(str(ctx.args.list)).expanduser().absolute()
    subject: dict[str, Any] = {"list_in": str(path)}
    cfg, counts, missing = missing_rows(ctx, path, subject)

    routed: list[match.Wanted] = []
    proposals: list[fallback.Proposal] = []
    offered_now: list[fallback.Proposal] = []
    if missing:
        with review.open_store(cfg) as items:
            held: list[tuple[match.Wanted, fallback.Proposal | None]] = []
            for one in missing:
                if provider_routed(items, one):
                    routed.append(one)
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
                        raise binary_refusal.yt_dlp_missing(
                            exc, subject,
                            said="A second source search runs it, so no row was searched "
                            "and nothing was offered.",
                            origin=ORIGIN,
                        ) from exc
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
    if unfound and not waiting and not accepted and not routed:
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
    fetch_command = shlex.join(["crate", "acquire", "fallback-fetch", str(path)])
    if offered_now:
        said = (
            f"{len(offered_now)} missing track(s) offered for review with second source "
            f"candidates: {_named(offered_now)}; see: {review_command}"
        )
    elif waiting or accepted:
        said = "nothing new to offer: every row with candidates was offered on an earlier run"
    elif routed:
        said = "nothing searched: every missing track has a provider route in review"
    else:
        said = "nothing searched: no track in this list is missing"
    checks = [
        _check("offered", "ok" if offered_now else "info", said),
        _check("owned", "info", f"{counts['owned']} already in the library, not searched"),
        _check(
            "version", "info",
            f"{counts['offered']} held in another version, offered for review and not "
            f"searched; see: crate review list",
        ),
        _check("suppressed", "info", f"{counts['suppressed']} deleted on purpose, not searched"),
        _check(
            "provider", "info",
            f"{len(routed)} missing track(s) carry the provider's own id or "
            f"have a provider candidate waiting or accepted in review, and are not "
            f"searched elsewhere"
            + (
                ": " + "; ".join(f"{one.artist} - {one.listed}" for one in routed)
                if routed
                else ""
            ),
        ),
        _check(
            "waiting", "info",
            f"{len(waiting)} missing track(s) are waiting in review with second source "
            f"candidates; answer them with crate review resolve",
        ),
        _check(
            "accepted", "info",
            f"{len(accepted)} second source candidate(s) accepted in review; download "
            f"them into staging with: {fetch_command}"
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
        **subject, "missing": counts["missing"], "owned": counts["owned"],
        "offered": counts["offered"], "suppressed": counts["suppressed"],
        "provider_routed": len(routed), "fallback_offered": len(offered_now),
        "waiting": len(waiting), "accepted": len(accepted), "unfound": len(unfound),
        "review_next": review_command if waiting else None,
        "fetch_next": fetch_command if accepted else None, "again": again,
        "rows": [one.to_json() for one in proposals],
    }
    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        outcome=Outcome.OK if offered_now else Outcome.NO_OP,
    )



# acquire.fallback-fetch (U81): the accepted candidates, downloaded

#: The fetch verb's origin on every refusal it raises.
FETCH_ORIGIN = ("acquire.fallback-fetch",)

#: Payload keys. ``LIST`` is the frozen list path the resume argv is rebuilt from;
#: ``ROWS`` holds each item's row and accepted upload, frozen at the queue (KTD9).
LIST = "list"
ROWS = "rows"

#: The longest file stem a fetched track is committed under, the source system's cap.
STEM_LIMIT = 120


def fetcher() -> fallback.FallbackFetcher:
    """The fetcher a run uses, looked up at call time so the suite can replace it."""
    return fallback.yt_dlp_fetcher()


def build_fetch(parser, entry) -> None:
    del entry
    parser.add_argument(
        "list",
        help=(
            "the list acquire fallback searched, whose accepted second source "
            "candidates to download into staging"
        ),
    )
    parser.add_argument(
        "--job", default=None, metavar="JOB_ID",
        help="continue the download already queued under this identifier",
    )
    parser.set_defaults(_handler=acquire_fallback_fetch)


def fetch_argv(job) -> list[str]:
    """The command line that continues one queued fetch. No ``--run``: no gate."""
    payload = job.payload or {}
    return ["acquire", "fallback-fetch", str(payload.get(LIST) or ""), "--job", job.job_id]


def accepted_rows(
    items: review.ReviewStore, missing: list[match.Wanted]
) -> dict[str, dict[str, str]]:
    """Each unrouted missing row whose candidate was ACCEPTED, as a job item."""
    rows: dict[str, dict[str, str]] = {}
    for one in missing:
        if provider_routed(items, one):
            continue
        said = fallback.settled(items, one)
        # The state is the one check; an accepted answer with no upload is refused
        # by the worker.
        if said is None or said.state != fallback.ACCEPTED:
            continue
        rows.setdefault(
            str(said.item_id),
            {"artist": one.artist, "title": one.listed, "url": str(said.url or "")},
        )
    return rows


def acquire_fallback_fetch(ctx) -> Envelope:
    """Queue one item per accepted second source candidate, or drive the job.

    No gate, since a person chose every upload. Both paths sweep staging (R-291).
    """
    if ctx.args.job:
        with jobs.open_store() as store:
            # Reconcile first: a dead driver's claim is invisible to the queue.
            job = jobs.reconcile(store, ctx.args.job)
            acquire_cli.sweep_staging(
                Path(jobs.frozen_config(job).paths.download_staging), store
            )
            # The same tail as ``acquire download`` (R-290, R-225).
            job, warnings = jobs.resumed(ctx, store, job)
            return ctx.envelope(data=jobs.reported(store, job), warnings=warnings)
    path = Path(str(ctx.args.list)).expanduser().absolute()
    subject: dict[str, Any] = {"list_in": str(path)}
    cfg, _counts, missing = missing_rows(ctx, path, subject)
    rows: dict[str, dict[str, str]] = {}
    if missing:
        with review.open_store(cfg) as items:
            rows = accepted_rows(items, missing)
    if not rows:
        return ctx.envelope(
            data={"job_id": "", "state": "nothing-accepted", "cause": None, "progress": {}},
            outcome=Outcome.NO_OP,
        )
    with jobs.open_store() as store:
        acquire_cli.sweep_staging(Path(cfg.paths.download_staging), store)
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={LIST: str(path), ROWS: rows},
            cfg=cfg,
            item_ids=tuple(rows),
        )
        return ctx.envelope(data=jobs.reported(store, job))


def fetch_stem(artist: str, title: str) -> str:
    """The stem a fetched track is committed under, from the ROW and nothing else."""
    return naming.trim_dangling(naming.compose_body(artist, title)[:STEM_LIMIT])


def _exists(final: Path, detail: dict[str, Any]) -> CratekitError:
    return refuse(
        "output-exists",
        f"{final} already exists, so {detail['artist']} - {detail['title']} was not "
        f"put in its place; move or delete the existing file and resume, or leave "
        f"it and treat this item as done",
        origin=FETCH_ORIGIN, scope=Scope.ITEM, detail={"path": str(final), **detail},
    )


def handle_fetch(job, item, cfg) -> jobs.Produced:
    """Download ONE accepted upload into staging, marked lossy and tagged from its row.

    Ordered by cost, so a strict policy or an existing name refuses before downloading.
    """
    said = dict(((job.payload or {}).get(ROWS) or {}).get(item.item_id) or {})
    artist = str(said.get("artist") or "")
    title = str(said.get("title") or "")
    url = str(said.get("url") or "")
    detail: dict[str, Any] = {"item_id": item.item_id, "artist": artist, "title": title, "url": url}
    settings = AdapterSettings.from_config(cfg)
    policy = settings.lossless_policy
    decision = decide_lossless(policy, source_is_lossless=False)
    if not decision.permitted:
        raise refuse(
            "lossy-refused",
            f"{artist} - {title} was accepted from a second source, which is lossy, "
            f"and the strict lossless policy refuses a lossy file, so nothing was "
            f"downloaded",
            remedy=decision.remedy or Remedy.RELAX_LOSSLESS_POLICY,
            scope=Scope.ITEM,
            origin=FETCH_ORIGIN,
            detail=detail,
        )
    where = urlsplit(url)
    if where.scheme not in ("http", "https") or not where.netloc:
        # An imported review document may say anything; only a web page reaches the tool.
        raise refuse(
            "unavailable-permanent",
            f"the upload accepted for {artist} - {title} is not a web address "
            f"({url!r}), so nothing can download it",
            steps=(
                f"clear the answer and choose another candidate: crate review clear {item.item_id}",
            ),
            scope=Scope.ITEM,
            origin=FETCH_ORIGIN,
            detail=detail,
        )
    stem = fetch_stem(artist, title)
    if not stem:
        raise refuse(
            "unavailable-permanent",
            f"the row accepted as {url} names no artist and no title, so the file "
            f"could be neither named nor tagged",
            steps=("give the row an artist and a title in the list and run it again",),
            scope=Scope.ITEM,
            origin=FETCH_ORIGIN,
            detail=detail,
        )
    root = settings.download_staging
    marker = cfg.naming.lossy_marker or ""
    expected = root / acquire_cli.marked_name(
        Path(stem + fallback.FETCH_SUFFIX), marker, required=decision.marker_required
    )
    if expected.exists():
        raise _exists(expected, detail)
    directory = acquire_cli.staging_dir(root, job.job_id, item.ordinal)
    try:
        found = fetcher()
    except binaries.BinaryNotFound as exc:
        # Parked, not failed: a missing program fails every later item alike.
        raise jobs.Parked(
            binary_refusal.yt_dlp_missing(
                exc, detail,
                said="A second source download runs it, so the job is parked with this "
                "item not downloaded.",
                origin=FETCH_ORIGIN,
            ).cause
        ) from exc
    try:
        landed = found.fetch(url, directory)
    except fallback.FallbackUnavailable as exc:
        raise refuse(
            "unavailable-transient",
            f"the download of {artist} - {title} from {url} failed ({exc}); it stays "
            f"queued",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=True,
            origin=FETCH_ORIGIN,
            detail=detail,
        ) from exc
    landed = acquire_cli.checked_landing(landed, item.item_id, policy=policy)
    final = root / acquire_cli.marked_name(
        Path(stem + landed.suffix), marker, required=decision.marker_required
    )
    if final.exists():
        raise _exists(final, detail)
    untagged = (
        f"{artist} - {title} downloaded and could not be tagged from its row, so it "
        f"is not committed; it stays queued"
    )
    try:
        # Every upload tag goes first, since an MP3 upload is not converted and could
        # keep a tempo frame (R17).
        written = tags.strip_tags(landed) and tags.write_tags(
            landed, {"artist": artist or None, "title": title or None}
        )
    except tags.UnsupportedContainer as exc:
        raise refuse(
            "unavailable-transient",
            f"{untagged} ({exc})",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=True,
            origin=FETCH_ORIGIN,
            detail=detail,
        ) from exc
    if not written:
        raise refuse(
            "unavailable-transient",
            untagged,
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=True,
            origin=FETCH_ORIGIN,
            detail=detail,
        )
    return jobs.Produced(staged=landed, final=final)


__all__ = [
    "FETCH_ORIGIN", "LIST", "ORIGIN", "ROWS", "STEM_LIMIT", "accepted_rows", "acquire_fallback",
    "acquire_fallback_fetch", "build", "build_fetch", "fetch_argv", "fetch_stem", "fetcher",
    "handle_fetch", "missing_rows", "provider_routed", "searcher",
]
