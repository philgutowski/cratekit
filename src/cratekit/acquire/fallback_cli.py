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

THE DOWNLOAD IS A SECOND VERB (U81). ``crate acquire fallback-fetch PATH`` takes
the same list, resolves it the same way, and queues one job item per row whose
candidate a person ACCEPTED. The worker downloads that upload into staging,
lossy and marked, tagged from the row, and a strict lossless policy refuses
each such item before anything downloads.
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
from cratekit.core import binaries, config, jobs, naming, review, tags
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


def _binary_refusal(
    exc: binaries.BinaryNotFound,
    subject: dict[str, Any],
    *,
    said: str = "A second source search runs it, so no row was searched and nothing was offered.",
    origin: tuple[str, ...] = ORIGIN,
) -> CratekitError:
    """A missing ``yt-dlp`` as this verb's refusal, the install hint and all.

    The binaries module already decided which of its situations this is, so
    the remedy IS its token: install, install from source, or fix the override.
    The hint travels as data for the command line layer to render (D2).
    """
    hint = exc.hint
    return refuse(
        "yt-dlp-missing",
        f"{exc} {said}",
        remedy=Remedy(exc.remedy.value),
        steps=(
            (f"install {', '.join(hint.packages)} with {hint.manager}, then run it again",)
            if hint is not None
            else ()
        ),
        scope=Scope.RUN,
        origin=origin,
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


def missing_rows(
    ctx, path: Path, subject: dict[str, Any]
) -> tuple[config.Config, dict[str, int], list[match.Wanted]]:
    """The list's rows the library does not hold, one per question, and the counts.

    SHARED BY BOTH VERBS, so the rows ``acquire fallback-fetch`` downloads for
    are exactly the rows ``acquire fallback`` searched for: the same reader, the
    same library resolution, the same answered version questions, and the same
    fold to one row per question. A row the library came to hold between the
    search and the download resolves owned here and is not fetched.
    """
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
    return cfg, counts, missing


def provider_routed(items: review.ReviewStore, one: match.Wanted) -> bool:
    """Whether a lossless route to this row exists, so no second source is used.

    THE PROVIDER'S OWN ID IS A ROUTE. ``intake missing --list`` lists such a row
    without a search, and a lossless download of it is one command away. So is a
    provider candidate waiting or accepted in review.
    """
    if missing_cli.provider_ref(one):
        return True
    on_provider = candidates.settled(items, one)
    return on_provider is not None and on_provider.state in (
        candidates.WAITING,
        candidates.ACCEPTED,
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
            "version",
            "info",
            f"{counts['offered']} held in another version, offered for review and not "
            f"searched; see: crate review list",
        ),
        _check("suppressed", "info", f"{counts['suppressed']} deleted on purpose, not searched"),
        _check(
            "provider",
            "info",
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
            "waiting",
            "info",
            f"{len(waiting)} missing track(s) are waiting in review with second source "
            f"candidates; answer them with crate review resolve",
        ),
        _check(
            "accepted",
            "info",
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
        **subject,
        "missing": counts["missing"],
        "owned": counts["owned"],
        "offered": counts["offered"],
        "suppressed": counts["suppressed"],
        "provider_routed": len(routed),
        "fallback_offered": len(offered_now),
        "waiting": len(waiting),
        "accepted": len(accepted),
        "unfound": len(unfound),
        "review_next": review_command if waiting else None,
        "fetch_next": fetch_command if accepted else None,
        "again": again,
        "rows": [one.to_json() for one in proposals],
    }
    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        outcome=Outcome.OK if offered_now else Outcome.NO_OP,
    )



# ---------------------------------------------------------------------------
# acquire.fallback-fetch (U81): the accepted candidates, downloaded
# ---------------------------------------------------------------------------

#: The fetch verb's origin on every refusal it raises.
FETCH_ORIGIN = ("acquire.fallback-fetch",)

#: Payload keys. ``LIST`` is the frozen list path the resume argv is rebuilt
#: from. ``ROWS`` is what each item IS, keyed by the review item it came from:
#: the row's artist and title and the upload a person accepted, frozen at the
#: queue so the worker reads nothing but the job (KTD9). An answer changed in
#: review after queueing does not change what a queued item downloads.
LIST = "list"
ROWS = "rows"

#: The longest file stem a fetched track is committed under, the source
#: system's cap. The naming stage renames it to the library's own form later.
STEM_LIMIT = 120


def fetcher() -> fallback.FallbackFetcher:
    """The fetcher a run uses, looked up on the module at call time.

    THE NETWORK SEAM, the searcher's twin. The suite replaces this function, so
    no test builds the shipped fetcher and no test downloads anything.
    """
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
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the download already queued under this identifier",
    )
    parser.set_defaults(_handler=acquire_fallback_fetch)


def fetch_argv(job) -> list[str]:
    """The command line that continues one queued fetch. No ``--run``: no gate."""
    payload = job.payload or {}
    return ["acquire", "fallback-fetch", str(payload.get(LIST) or ""), "--job", job.job_id]


def _reported(store, job) -> dict[str, Any]:
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


def accepted_rows(
    items: review.ReviewStore, missing: list[match.Wanted]
) -> dict[str, dict[str, str]]:
    """Each missing row whose second source candidate was ACCEPTED, as a job item.

    A row with a lossless route is not fetched lossy, the rule the search keeps
    for the same reason: a provider id, or a provider candidate waiting or
    accepted in review, is a better copy one command away. A row waiting,
    rejected or stalled in review has no upload anybody chose, so it is not an
    item. The artist and the title are the ROW's, never the upload's.
    """
    rows: dict[str, dict[str, str]] = {}
    for one in missing:
        if provider_routed(items, one):
            continue
        said = fallback.settled(items, one)
        # ONE CHECK, THE STATE. ``settled`` names an upload only on an accepted
        # answer, so a second check for the URL could never be the one that
        # decided, and u81-b measured it covering this one to a zero. An
        # accepted answer with no upload would reach the worker as an empty
        # address and be refused there, never downloaded.
        if said is None or said.state != fallback.ACCEPTED:
            continue
        rows.setdefault(
            str(said.item_id),
            {"artist": one.artist, "title": one.listed, "url": str(said.url or "")},
        )
    return rows


def acquire_fallback_fetch(ctx) -> Envelope:
    """Queue one item per accepted second source candidate, or drive the job.

    No gate, for the reason ``acquire download`` declares none: the verb ADDS
    files into the configured download staging directory and replaces nothing,
    deletes nothing and publishes nothing. Every upload it fetches was chosen by
    a person in review, which is the decision a gate would have asked for.
    """
    if ctx.args.job:
        with jobs.open_store() as store:
            # RECONCILE FIRST. A claim left behind by a driver that died is
            # state the queue cannot see for itself.
            job = jobs.reconcile(store, ctx.args.job)
            warnings: tuple[dict[str, str], ...] = ()
            if job.is_open():
                _, warnings = ctx.run_job(store, job)
                job = jobs.get(store, job.job_id)
            return ctx.envelope(data=_reported(store, job), warnings=warnings)
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
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={LIST: str(path), ROWS: rows},
            cfg=cfg,
            item_ids=tuple(rows),
        )
        return ctx.envelope(data=_reported(store, job))


def fetch_stem(artist: str, title: str) -> str:
    """The stem a fetched track is committed under, from the ROW and nothing else."""
    joined = " - ".join(
        part for part in (naming.sanitize_segment(artist), naming.sanitize_segment(title)) if part
    )
    return naming.trim_dangling(joined[:STEM_LIMIT])


def _exists(final: Path, detail: dict[str, Any]) -> CratekitError:
    return refuse(
        "output-exists",
        f"{final} already exists, so {detail['artist']} - {detail['title']} was not "
        f"put in its place; move or delete the existing file and resume, or leave "
        f"it and treat this item as done",
        origin=FETCH_ORIGIN,
        scope=Scope.ITEM,
        detail={"path": str(final), **detail},
    )


def handle_fetch(job, item, cfg) -> jobs.Produced:
    """Download ONE accepted upload into staging, marked lossy and tagged from its row.

    The order is the order of what each step can cost:

    * a strict policy refuses the item BEFORE anything downloads, because a
      second source is lossy whatever it serves, so the answer is already known
      and a download would only be thrown away;
    * the final name is known before the download, because it is the row's, so
      a file already there refuses the item without spending one;
    * the landing goes through ``checked_landing``, the one place every
      acquisition's file passes, and is marked through ``marked_name``, which
      refuses a configuration that names no marker text;
    * every tag the upload carried is stripped, a tempo frame included, and the
      artist and title tags are written from the ROW, never from the upload's
      page, so the tagger and the naming stage downstream read the track a
      person asked for;
    * the engine commits it into the staging root, where the ordinary tag, name
      and land tail picks it up.
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
        # The review store takes an imported document, so an accepted option is
        # whatever that document said. Only a web page is handed to the tool.
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
        # PARKED, NOT FAILED. A missing program is a fact about the machine and
        # never about the track, so every later item would fail the same way.
        raise jobs.Parked(
            _binary_refusal(
                exc,
                detail,
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
        # EVERY TAG THE UPLOAD CARRIED GOES FIRST. The tool drops the upload's
        # metadata only when it converts, and an upload already served as MP3
        # is not converted, so a tempo frame an uploader wrote would otherwise
        # survive under the row's artist and title (R17).
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
    "FETCH_ORIGIN",
    "LIST",
    "ORIGIN",
    "ROWS",
    "STEM_LIMIT",
    "accepted_rows",
    "acquire_fallback",
    "acquire_fallback_fetch",
    "build",
    "build_fetch",
    "fetch_argv",
    "fetch_stem",
    "fetcher",
    "handle_fetch",
    "missing_rows",
    "provider_routed",
    "searcher",
]
