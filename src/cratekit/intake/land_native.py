"""The native landing's steps (R-746): its planner, its write order, its archive and its notes.

Split out of :mod:`cratekit.intake.land_cli`, whose ``_land_native`` runs these
in order and which re-exports every name a caller reads there.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Callable, TypeVar

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import analysis_store, config, jobs, rb_writer, session
from cratekit.core.cause import CratekitError, Outcome
from cratekit.intake import (
    account_playlists,
    batch_name,
    filing,
    ingest,
    label_filing,
    landing,
    native,
    set_playlist,
    shelve,
)
from cratekit.intake.land_report import (
    FAVORITES_PLACED,
    FAVORITES_SKIPPED,
    _colour_notes,
    _twin_notes,
    awaiting_analysis,
    dyn_warnings,
    favorites_notes,
    vox_warnings,
)

#: The fact a native write's answer is pinned to outside its digest (U161):
#: the database file the handle opened, as the screen's reads and writes line
#: names it.
DATABASE_PIN = "database"


def unfiled_reason(ctx, medium: ingest.IntakeMedium) -> str:
    """Why the landing files nothing after it, empty when it files (U165).

    Asked with ``--land-only``, or a routing tree still on the bridge, where no
    database writer may write its membership and a filing could only end refused.
    """
    declared = medium.declared
    return (
        "asked with --land-only"
        if getattr(ctx.args, "land_only", False)
        else (
            ""
            if medium.files_natively
            else (
                f"the tree {declared.tree.id!r} is on the xml bridge; cut it over with "
                f"crate tree cutover {declared.tree.id}"
            )
        )
    )


def read_set(ctx) -> tuple[jobs.Job | None, set_playlist.SetWords | None, tuple[dict, ...]]:
    """The set job, its words and its reports, read before the gate (U121).

    A job that is not a finished set, and a name the page and the flags cannot
    complete, refuse with the files still in staging and nothing shown.
    """
    if not ctx.args.set_job:
        return None, None, ()
    with jobs.open_store() as store:
        set_job = set_playlist.set_job_or_refuse(store, str(ctx.args.set_job))
        words = set_playlist.words_for(
            set_job, dj=ctx.args.dj, set_name=ctx.args.set_name, set_date=ctx.args.set_date
        )
        return set_job, words, set_playlist.reports_of(store, set_job)


def native_planner(
    ctx,
    medium: ingest.IntakeMedium,
    *,
    manifest: landing.LabelManifest | None,
    label: str | None,
    label_from_tags: bool,
    claims: tuple[account_playlists.Claim, ...],
    hearted: tuple[account_playlists.Hearted, ...],
    owned: tuple[account_playlists.HeartRow, ...],
    unfiled: str,
    set_job: jobs.Job | None,
    words: set_playlist.SetWords | None,
    reports: tuple[dict[str, Any], ...],
    set_planned: list[set_playlist.SetPlaylistPlan],
) -> Callable[[config.Config, landing.Plan], Callable[[Any], native.NativePlan]]:
    """The landing's planner: given a library and its staged files, a plan made on a handle.

    ONE PLANNER, TWO PLACES (U162): the live landing plans its own staging
    folder and music folder, and a rehearsal plans the same files again at its
    scratch area, through this same code, to apply them there. Each set plan
    made is appended to ``set_planned``.
    """
    declared, registry = medium.declared, medium.registry
    tree_id = declared.intake.id

    def planner(cfg: config.Config, planned: landing.Plan) -> Callable[[Any], native.NativePlan]:

        def set_plan(db, files) -> set_playlist.SetPlaylistPlan | None:
            if set_job is None or words is None:
                return None
            made = set_playlist.plan_for_landing(
                cfg,
                db,
                declared,
                set_job,
                words,
                reports,
                files=files,
                posted=getattr(ctx.args, "posted", None),
            )
            set_planned.append(made)
            return made

        def label_plan(db, files) -> label_filing.LabelPlan | None:
            # A MANIFEST WITH NO LABEL ROW FILES NOTHING, and asks nothing of the
            # catalogue tree, as the bridge's own check returns early on it.
            if manifest is not None and manifest.rows:
                return label_filing.plan_for_manifest(
                    cfg, db, medium, manifest=manifest, files=files
                )
            if label is not None:
                return label_filing.plan_for_label(db, medium, label=label, files=files)
            if label_from_tags:
                return label_filing.plan_for_tags(db, medium, files=files)
            return None

        def plan(db) -> native.NativePlan:
            # THE FILED FOLDER, CHOSEN ON THIS HANDLE (U164): the batch lands
            # where a shelve would have filed it, so every row carries its
            # final FolderPath from the first commit and no shelve follows.
            target = shelve.landing_target(cfg, db, planned.batch, on=batch_name.today())
            files = [(item, target / item.name) for item in planned.items]
            # THE INBOX PLAYLIST FOR A SET (U135): named for the set, and an earlier
            # landing of the same job's playlist is added to under its first name.
            # The batch folder stays the dated (or --name) landing name so two
            # landings never share a folder; only the playlist joins.
            inbox_name = planned.batch
            batch_playlist_id = ""
            set_job_id = ""
            leftovers: tuple[str, ...] = ()
            inbox_found_by_name = False
            if set_job is not None and words is not None:
                set_job_id = set_job.job_id
                root_id = native.anchored_intake_root(db, tree_id, registry)
                recorded = native.recorded_inbox_playlist(cfg, db, set_job_id, root_id)
                if recorded is not None:
                    batch_playlist_id, inbox_name = recorded
                else:
                    inbox_name = set_playlist.frozen_name(set_job) or set_playlist.playlist_name(
                        words
                    )
                    inbox_found_by_name = native.live_inbox_named(db, inbox_name, root_id)
                leftovers = native.leftover_set_inbox(
                    cfg, db, set_job_id, root_id, inbox_name, keep_id=batch_playlist_id
                )
            split, emptied = _native_split(
                db,
                cfg,
                claims,
                tree_id=tree_id,
                registry=registry,
                batch=inbox_name,
                target=target,
            )
            # EACH ACCOUNT PLAYLIST'S TWIN (U149), planned on this handle for
            # the ones not paired yet, into the landing year's twin folder.
            from cratekit.favorites import backfill, placement  # noqa: PLC0415 - toggleable
            from cratekit.modules.outbound import pairs
            from cratekit.sync import twins

            landing_twins = twins.plan_landing(
                db,
                [(one.account, one.account_name or one.name) for one in split],
                year=batch_name.today().year,
                paired=pairs.PairStore(cfg).all(),
            )
            made = native.plan_rows(
                cfg,
                db,
                tree_id=tree_id,
                registry=registry,
                batch=inbox_name,
                files=files,
                split=split,
                unplanned_left=emptied,
                pass_name=ctx.args.pass_name,
                hearts=tuple(
                    native.HeartItem(target=target / one.path.name, month=one.month, ref=one.ref)
                    for one in hearted
                ),
                favorites_source=placement.source_name(declared),
                owned_hearts=tuple(
                    native.OwnedHeartItem(
                        content_id=one.content_id, month=one.month, ref=one.ref, title=one.title
                    )
                    for one in backfill.owned_in_library(cfg, db, owned)
                ),
                set_plan=set_plan(db, files),
                batch_playlist_id=batch_playlist_id,
                set_job_id=set_job_id,
                inbox_leftovers=leftovers,
                inbox_found_by_name=inbox_found_by_name,
                labels=label_plan(db, files),
                twins=landing_twins,
            )
            made = replace(made, folder=target, batch=planned.batch)
            # WHERE EACH NEW ROW WILL BE FILED, BEFORE IT EXISTS (U165), shown
            # and digested, so the one answer covers the filing after the commit.
            if unfiled:
                return made
            return native.with_filing(made, filing.predict(declared, made.to_add()))

        return plan

    return planner


def landed_warnings(
    cfg: config.Config,
    payload: dict,
    landed: landing.LandedNative,
    *,
    applied: list[native.NativePlan],
    archive_notes: list[dict[str, str]],
    set_planned: list[set_playlist.SetPlaylistPlan],
) -> list[dict[str, str]]:
    """What a person reads after a native landing wrote, in the order it is said."""
    warnings = [{"code": entry.reason, "message": entry.sentence} for entry in landed.refused]
    warnings.extend(account_playlists.left_warning(landed.collection.left))
    warnings.extend(_twin_notes(cfg, applied[-1] if applied else None, landed.collection))
    warnings.extend(awaiting_analysis(landed.collection))
    warnings.extend(vox_warnings(landed.collection))
    warnings.extend(dyn_warnings(landed.collection))
    warnings.extend(favorites_notes(payload, landed.collection))
    warnings.extend(archive_notes)
    if set_planned:
        # ONCE PER RUN, from the first plan: the write takes the plan again.
        warnings.extend(set_playlist.ignored_note(set_planned[0]))
    kept = landed.collection.set_playlist
    if kept is not None and kept.playlist_id:
        set_playlist.assert_read_back(kept)
        warnings.extend(set_playlist.written_note(kept))
        warnings.extend(set_playlist.left_warning(kept.left))
    elif kept is not None and set_planned:
        # NOTHING WRITTEN, and the left rows are the write's own answer: the
        # members whose files did not land as well as the plan's left rows.
        warnings.extend(set_playlist.nothing_note(set_planned[0], left=len(kept.left)))
        warnings.extend(set_playlist.left_warning(kept.left))
    filed = landed.collection.labels
    if filed is not None:
        label_filing.assert_read_back(filed)
        warnings.extend(label_filing.unfiled_warning(filed.left))
    return warnings


def _native_split(
    db,
    cfg: config.Config,
    claims: tuple[account_playlists.Claim, ...],
    *,
    tree_id: str,
    registry,
    batch: str,
    target: Path,
) -> tuple[tuple[native.PlaylistPlan, ...], tuple[tuple[str, account_playlists.Left], ...]]:
    """Each account playlist named against what the database's INBOX holds, on the write handle.

    AND EACH OWNED TRACK'S ROW FOUND BY PATH ON THE SAME HANDLE (U128), at plan
    time, so the screen and the digest name the rows the apply adds and the
    apply finds nothing again. Asked of the candidate rows whose stored path
    ends in the file's name, the native landing's own lookup, rather than of
    the whole collection. Answers the playlists and the left rows of the ones
    left holding nothing.
    """
    if not claims:
        return (), ()
    held = native.inbox_held(db, native.anchored_intake_root(db, tree_id, registry))
    named = account_playlists.named(claims, held, batch=batch)
    names = {Path(path).name for one in named for member in one.members for path in member.paths}
    resolved, emptied = account_playlists.resolve_owned(
        cfg, named, native.candidate_rows(db, names)
    )
    return (
        tuple(
            native.PlaylistPlan(
                name=claimed.name,
                account=claimed.playlist_id,
                members=tuple(
                    native.PlaylistMember(target=target / member.file.name, member=member)
                    if member.file is not None
                    else native.PlaylistMember(content_id=member.row, member=member)
                    for member in claimed.members
                ),
                account_name=claimed.account_name,
                left=claimed.left,
            )
            for claimed in resolved
        ),
        emptied,
    )


#: Why a set landing's account archive did not finish after the rows wrote (U129).
LAND_ARCHIVE_FAILED = "intake-land-archive-failed"


def _apply_landing_archive(cfg, archived) -> list[dict[str, str]]:
    """Apply the account archive after the landing wrote. Failures are warnings.

    The landing's rows are already in the library. An account call that raises,
    or an apply that leaves the playlist unrenamed, must not turn the landing
    into a failure: both ride the warnings channel on the landed envelope.
    """
    if archived is None or not archived.writes:
        return []
    from cratekit.export import set_cli

    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    except Exception as exc:
        message = (
            exc.cause.message if isinstance(exc, CratekitError) else f"{type(exc).__name__}: {exc}"
        )
        return [
            {
                "code": LAND_ARCHIVE_FAILED,
                "message": (
                    f"the account archive could not finish after the landing wrote "
                    f"({message}); the batch is in the library, run crate export "
                    f"archive over the set once the account can be reached"
                ),
            }
        ]
    return list(warnings)


def _plan_set_archive(cfg, *, set_job, words, pass_name: str):
    """The account archive for this set landing, or None when there is none to file (U129)."""
    if set_job is None:
        return None
    from cratekit.export import set_cli
    from cratekit.modules.outbound import ledger

    name = set_playlist.frozen_name(set_job)
    if not name and words is not None:
        name = set_cli.set_name(set_playlist.playlist_name(words))
    if not name or ledger.set_playlist(cfg, name) is None:
        return None
    try:
        return set_cli.plan_archive_named(cfg, name, pass_name=pass_name)
    except CratekitError:
        # Soft: the landing still lands; archive can run later via export archive.
        return None


def _with_archive(payload: dict, archived) -> dict:
    """Fold the archive plan into the landing's digest and items so one approval covers both."""
    if archived is None:
        return payload
    identity = {
        "land": payload["digest"],
        "archive": archived.payload["digest"],
    }
    items = list(payload.get("items") or [])
    for item in archived.payload.get("items") or []:
        items.append({**item, "area": "account-archive"})
    totals = dict(payload.get("totals") or {})
    totals["archive_writes"] = bool(archived.writes)
    return {
        **payload,
        "digest": digest_of(identity),
        "items": items,
        "totals": totals,
    }


#: What a native write plans: a landing's rows, or the owned hearts alone (U146).
_Planned = TypeVar("_Planned")


def ask_then_write(
    ctx,
    cfg: config.Config,
    spec,
    *,
    plan: Callable[[Any], _Planned],
    payload: Callable[[_Planned], dict],
    shown: Callable[[_Planned], dict[str, Any]],
    write: Callable[[Any, _Planned], Any],
) -> tuple[dict, Any | None]:
    """The order every native intake write keeps, held once. Answers (payload, written).

    SHARED BY THE LANDING AND ``intake file`` (R-770), and by the landing's
    owned hearts when no file came (U146), because the order is the contract
    and two hand kept copies of it would come to differ:

    * THE DATABASE IS OPENED WITH WRITE INTENT BEFORE THE PLAN, so a running
      rekordbox or its agent refuses before anything is shown, and the plan is
      made against the database the write will be made to;
    * THE ACKNOWLEDGMENT IS READ BEFORE THE GATE (R-733): an approval is the
      one way door on a live library, and a person who reads the whole plan
      and answers should not then be refused by something the verb could have
      read first;
    * the gate is asked over the digested plan, and only ``apply`` writes;
    * the handle is closed whatever happened.

    * THE ANSWER IS PINNED TO THE FILE THE HANDLE OPENED (U161). The digest
      names the library and not the file, so a copy rehearsal digests as the
      live plan; the file is pinned on the run beside it, and a continuation
      that opens another file is refused stale rather than writing there.

    ``written`` is None when the answer was not ``apply``, and the payload is
    then the plan as it was shown.
    """
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        rows = plan(db)
        data = payload(rows)
        session.assert_backup_acknowledged(cfg)
        opened = rb_writer.handle_path(db) or rb_writer.live_db_path(cfg)
        option = ctx.gate.require(
            spec, plan=data, context=shown(rows), pinned={DATABASE_PIN: str(opened)}
        )
        if option != "apply":
            return data, None
        return data, write(db, rows)
    finally:
        rb_writer.close_db(db)


def _place_owned(
    ctx,
    cfg: config.Config,
    spec,
    *,
    declared,
    owned: tuple[account_playlists.HeartRow, ...],
    empty: dict,
) -> Envelope:
    """The pass's owned hearts All Favorites lacks, placed when no file was downloaded (U146).

    THE LANDING'S GATE AND THE BACKFILL'S WRITER. Asked first of a handle
    opened to read, so a pass whose owned hearts are all placed, which is
    nearly every pass, opens nothing to write and asks nothing, and ends
    NO_OP exactly as an empty landing did. When some heart is missing, the
    order is :func:`ask_then_write`'s: the database opened with write intent,
    the plan taken again on it, the acknowledgment, the gate, and the guarded
    session of :func:`backfill.apply`, which takes the plan once more and
    refuses a digest that moved, then reads every membership back.

    A LIBRARY WITH NO ALL FAVORITES, OR TWO, IS NOT A REFUSAL, as a landing
    with files skips its placement: there is nothing else to land, so the
    pass ends NO_OP and says why.
    """
    from cratekit.favorites import backfill, placement  # noqa: PLC0415 - favorites is toggleable

    source = placement.source_name(declared)
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        first = backfill.plan_owned(cfg, db, source=source, rows=owned)
    except CratekitError as exc:
        if exc.cause.reason != placement.SOURCE_MISSING:
            raise
        return ctx.envelope(
            data=empty,
            outcome=Outcome.NO_OP,
            warnings=[
                {
                    "code": FAVORITES_SKIPPED,
                    "message": (
                        f"nothing to land and no owned heart was placed: "
                        f"{exc.cause.message}; run crate favorites backfill once the "
                        f"playlist exists"
                    ),
                }
            ],
        )
    finally:
        rb_writer.close_db(db)
    if not first.writes:
        return ctx.envelope(data=empty, outcome=Outcome.NO_OP)

    def written(db, approved: backfill.BackfillPlan) -> backfill.Backfilled:
        return backfill.apply(
            cfg, db, approved, source=source, analysis_roots=analysis_store.watch_roots(cfg)
        )

    payload, done = ask_then_write(
        ctx,
        cfg,
        spec,
        plan=lambda db: backfill.plan_owned(cfg, db, source=source, rows=owned),
        payload=lambda planned: backfill.payload(planned, cfg),
        shown=backfill.landing_facts,
        write=written,
    )
    if done is None:
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP)
    backfill.assert_read_back(done)
    placed = done.placed
    totals = {**payload["totals"], "hearts placed": placed.added}
    warnings = [
        {
            "code": FAVORITES_PLACED,
            "message": (
                f"{placed.said()}, for {len(payload['items'])} owned heart(s); no file "
                f"was landed; undo with a restore of session {done.session_id}"
            ),
        },
        *_colour_notes(placed),
    ]
    return ctx.envelope(data={**payload, "totals": totals}, warnings=warnings)
