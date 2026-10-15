"""The playlists source: list the account, keep what is new, queue it as intake.

The third R25 source, and the one the slim profile runs alone. It has no worker
of its own. Each account playlist it keeps is queued through
``intake.cli.queue_playlist``, under ``intake.playlist``, which is exactly the job
``crate intake playlist`` queues for the same playlist, with two keys added: the
intake run the pass shares (R29) and ``source_id``, which is how this module
later finds the jobs it queued. A separate playlists worker with its own item
shape was rejected for the reason U61 rejected a fourth worker: it would rebuild
the intake path one layer down.

**WHAT IS NEW, IN THE ORDER IT IS DECIDED.** A playlist is excluded when its
name carries the swept prefix the source system applies after a sweep, when its
name ends with the suffix the source system's label batch leaves on its run
debris (R-361), when its identifier is in this source's cursor, when its name
is a quarterly favourites placeholder, which is the favourites source's to
sweep, when a playlist intake job for it is still open, or when the listing
says it holds no tracks. Everything else is listed track by track and queued. A
playlist whose tracks come back empty is reported empty rather than queued, and
a playlist that cannot be read is reported unreadable rather than skipped in
silence.

**THE DEBRIS RULE IS THE SOURCE SYSTEM'S, SUFFIX AND CASE (R-361).** Its label
batch builds one `<label> LIBRARY` playlist per run and leaves it on the
account, and its own sweep drops any name ending ` LIBRARY`, leading space,
case sensitive. The fourth attended sitting found eleven of them among the
eighteen playlists a pass queued, about 1600 tracks of label catalogue offered
as ordinary intake. The name rule is copied rather than narrowed: a playlist a
person named `My Night LIBRARY` is excluded too, which is the collision the
source system already accepts, and every debris name the sitting listed was a
label run. The source system's sweep ALSO drops every playlist id its run
manifests registered as run created, and that half has no counterpart here,
because Cratekit reads no manifest of the source system's: a run playlist
whose name lost the suffix is still offered. Jobs already queued for debris
are not cancelled by this rule; it decides what a later pass offers, and
:func:`pending_marks` keeps the same names out of the mark, so a debris job
that succeeds, one queued before the rule or by hand, never has the source
system's throwaway renamed under it.

**THE CURSOR IS IDENTIFIERS, AND IT MOVES ON CLEAN COMPLETION ONLY.** Queueing
is not completion. At the start of every pass :func:`reconcile` reads every
playlist intake job for this library, the ones this source queued AND the ones
``crate intake playlist`` queued by hand (R-382), and records the playlist of
every one that SUCCEEDED, which is the state a job reaches only when every item
is done. A failed or cancelled job is not recorded and its playlist is offered
again, and an open one, whichever verb queued it, holds its playlist back as in
flight. The cursor still moves only here, at the top of a pass, and never on a
job's completion. Nothing is ever filtered by title except the three naming
conventions above, which are conventions spelled in the name by the systems
that apply them, and none is stored (D5).

**SWEPT MEANS RESOLVED, NOT ACQUIRED, AND THE PASS SAYS SO (R-359).** The job a
sweep composes resolves every track to owned, offered or missing and acquires
none, so a SUCCEEDED job is a playlist whose missing tracks are still not in the
library, and once it is recorded no later pass offers it again. The cursor is
deliberately left recording on success, because the alternative needs an
acquisition step the pass does not compose. What changed is the report: every
block carries :data:`SWEPT_MEANS`, and :func:`said` gives the check a person
reads by default the same fact in words.

**THE MARK IS ITS OWN VERB, AND THE PASS STILL MARKS NOTHING (U82).**
``sync/marks.py`` states the rule: a remote playlist is renamed only after the
importable file exists and a recheck holds. The account seam,
``modules.outbound.service.RemoteAccount``, declares ``rename_playlist``, and
:func:`mark_swept` is the application. The file arrives three verbs after the
pass, once its missing tracks were listed, downloaded and landed, so the caller
is the gated verb in ``sync/mark_cli.py`` and never the pass. A pass therefore
still reports the mark as :data:`MARK_UNBOUND`, which is true of the pass: it
resolves tracks, acquires none and writes no importable file.

**THE RECHECK IS A SECOND READ, NOT THE PLAN'S OWN.** :func:`mark_swept` reads
the account listing again rather than trusting the one :func:`plan` already took.
A recheck served from the planning read confirms only that the plan was
internally consistent, which it always is, and the thing it is supposed to catch
is a playlist that changed between the plan and the mark. That second read is
taken once and shared by every mark in the batch.

**THE MARK SET IS THE CURSOR, NOT WHAT THIS PASS ADDED TO IT.** The cursor is
written before anything is marked and moves whether or not the mark lands, so a
set taken from the newly recorded is a set nothing can offer a second time. See
:func:`pending_marks`, which is where the reasoning lives.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.favorites import placeholders
from cratekit.intake import cli as intake_cli
from cratekit.label.catalogue import (
    AccountPlaylist,
    Catalogue,
    PlaylistReferenceInvalid,
)
from cratekit.label.catalogue import playlist_id as typed_playlist_id
from cratekit.sync import marks
from cratekit.sync.watermarks import WatermarkStore

if TYPE_CHECKING:  # pragma: no cover - the seam's type, never imported at runtime
    # Behind the guard because this source is CORE, the slim profile runs it
    # alone, and the outbound package is a feature module. The annotation is the
    # honest one, and a slim install still imports nothing extra to read it.
    from cratekit.modules.outbound.service import RemoteAccount

#: This source's identifier, as ``sync.sources`` declares it and as the jobs it
#: queues carry it.
SOURCE_ID = "playlists"

#: The prefix the source system puts on a playlist it has swept. The same
#: convention its analysis pass skips a prefixed name by, kept rather than
#: reinvented, because the live account already carries it.
SWEPT_PREFIX = "DOWNLOADED "

#: The suffix the source system's label batch leaves on the throwaway playlist
#: each run builds, `<label> LIBRARY`. Its own sweep drops any name ending with
#: it, leading space and upper case exactly, and this is that rule kept rather
#: than reinvented (R-361). Case sensitive on purpose: `Colorize Library` is a
#: name a person could give a playlist, and the batch never writes it.
LIBRARY_PLAYLIST_SUFFIX = " LIBRARY"

#: What a recorded playlist means in this build, on the block a machine reads.
#: The cursor records a playlist whose intake job SUCCEEDED, which is every track
#: resolved and none acquired (R-359).
SWEPT_MEANS = "resolved-not-acquired"

#: The same fact in words, keyed by the token the block carries, so the human
#: sentence is there exactly when the machine field is.
SWEPT_MEANS_SAID: Mapping[str, str] = MappingProxyType(
    {
        SWEPT_MEANS: (
            "a recorded playlist had its tracks resolved against the library, not "
            "acquired, so a track its intake job reported missing is still not in "
            "the library, crate intake missing lists it, and no later sync offers "
            "that playlist again"
        ),
    }
)

#: What the pass says about the mark step when nothing marked the account,
#: which is every pass, since a pass writes no importable file. The mark is the
#: gated verb in ``sync/mark_cli.py``, run once the pass has been landed.
MARK_UNBOUND = "unbound"

#: What the pass says when :func:`mark_swept` ran against the account seam.
MARK_APPLIED = "applied"

#: The kind every mark this source defers carries. One kind, because the only
#: remote side effect a sweep leaves is the swept prefix on a title.
MARK_KIND = "prefix"

#: The two refusals one playlist's listing may end in that are about THAT
#: playlist. Any other refusal, a credential or an unbound adapter, is about the
#: whole source and ends it.
PER_PLAYLIST_REASONS = frozenset({"label-playlist-unreadable", "intake-list-unusable"})


class Excluded(StrEnum):
    """Why a listed playlist was not queued."""

    SWEPT = "already-swept"
    LABEL_DEBRIS = "label-debris"
    #: A year playlist ``label playlists`` built for a followed label (R-835).
    #: It is that label's catalogue, and swept as intake every release on it
    #: would be listed as missing from the library.
    LABEL_FOLDER = "label-folder"
    #: A playlist ``export set`` made from a set's tracklist (R-837). The set's
    #: tracks are fetched from that tracklist, so swept as intake it would be a
    #: second download of the same set.
    SET_PLAYLIST = "set-playlist"
    #: A playlist the author marked to stay the same list as a rekordbox
    #: playlist (U130). ``sync pair`` keeps it, queueing for acquisition what
    #: the library lacks, so swept as intake it would be queued twice and
    #: marked with the swept prefix under the author.
    PAIRED = "paired"
    #: A playlist ``crate organize`` made to mirror a rekordbox playlist
    #: (U147). It holds tracks the library already owns, so swept as intake it
    #: would be marked with the swept prefix under the mirror.
    MIRROR = "mirror"
    RECORDED = "recorded"
    PLACEHOLDER = "favorites-placeholder"
    IN_FLIGHT = "in-flight"
    EMPTY = "empty"
    UNREADABLE = "unreadable"


def is_swept_name(name: str) -> bool:
    """Whether the name carries the swept prefix."""
    return str(name or "").startswith(SWEPT_PREFIX)


def is_library_debris(name: str) -> bool:
    """Whether the name ends with the label batch's debris suffix, case exactly."""
    return str(name or "").endswith(LIBRARY_PLAYLIST_SUFFIX)


def exclusion(
    playlist: AccountPlaylist,
    *,
    recorded: frozenset[str] | set[str],
    in_flight: frozenset[str] | set[str],
    label_built: frozenset[str] | set[str] = frozenset(),
    set_built: frozenset[str] | set[str] = frozenset(),
    paired: frozenset[str] | set[str] = frozenset(),
    mirrored: frozenset[str] | set[str] = frozenset(),
) -> Excluded | None:
    """Why this playlist is not new, or ``None`` when it is. Pure.

    The ORDER is the report's, not a precedence any one playlist depends on: a
    playlist can meet several rules, and the first one named is the one a person
    is told.
    """
    if is_swept_name(playlist.name):
        return Excluded.SWEPT
    if is_library_debris(playlist.name):
        return Excluded.LABEL_DEBRIS
    if playlist.playlist_id in label_built:
        return Excluded.LABEL_FOLDER
    if playlist.playlist_id in set_built:
        return Excluded.SET_PLAYLIST
    if playlist.playlist_id in paired:
        return Excluded.PAIRED
    if playlist.playlist_id in mirrored:
        return Excluded.MIRROR
    if playlist.playlist_id in recorded:
        return Excluded.RECORDED
    if placeholders.is_placeholder(playlist.name):
        return Excluded.PLACEHOLDER
    if playlist.playlist_id in in_flight:
        return Excluded.IN_FLIGHT
    if playlist.tracks == 0:
        return Excluded.EMPTY
    return None


def source_jobs(store, cfg: config.Config, *, handler_key: str) -> tuple[jobs.Job, ...]:
    """Every job THIS source queued for THIS library, newest first.

    All three fields, because each alone names jobs this source does not own:
    the key is shared with ``crate intake playlist`` run by hand, and the queue is
    installation scoped while the cursor is per library.

    NOT WHAT THE CURSOR IS RECONCILED OVER, since R-382. That is
    :func:`playlist_jobs`, which a playlist run by hand also reaches. This set is
    for a reader that needs a pass's own jobs, the mark verb grouping them by the
    run they share.
    """
    return tuple(
        job
        for job in jobs.list_jobs(store)
        if job.handler_key == handler_key
        and (job.payload or {}).get("source_id") == SOURCE_ID
        and job.library_id == cfg.library.volume_id
    )


def playlist_of(job: jobs.Job) -> str:
    """The account playlist a job this source queued is about, or ``""``."""
    return str((job.payload or {}).get(intake_cli.SOURCE) or "")


_playlist_of = playlist_of


def recorded_as(job: jobs.Job) -> str:
    """The identifier the cursor records for a playlist intake job, or ``""``.

    A job THIS SOURCE queued carries the listing's own identifier, and it is
    returned verbatim, because that is what the next listing is compared with.
    A job ``crate intake playlist`` queued carries what a person TYPED, which may
    be a URL or a share link, so it is read through the provider's reference
    parser and records the identifier the listing would carry. A reference the
    parser does not recognise is kept as typed: the job that succeeded listed
    it, so the catalogue it ran against took it as an identifier.

    THE HEARTS ARE NOT A PLAYLIST. Both verbs that list the account's hearts,
    ``crate intake playlist favorites`` and the favourites source, queue them
    under the reserved reference, and that is never an account playlist this
    cursor could hold, so such a job records nothing.
    """
    reference = _playlist_of(job)
    if not reference:
        return ""
    if (job.payload or {}).get("source_id") == SOURCE_ID:
        return reference
    if intake_cli.is_favorites(reference):
        return ""
    try:
        return typed_playlist_id(reference)
    except PlaylistReferenceInvalid:
        return reference


def playlist_jobs(store, cfg: config.Config, *, handler_key: str) -> tuple[jobs.Job, ...]:
    """Every playlist intake job for THIS library, whichever verb queued it (R-382).

    What the cursor is reconciled over and what an open job holds back. It is
    wider than :func:`source_jobs` on purpose: a playlist a person ran through
    ``crate intake playlist`` has been resolved exactly as a sweep would resolve
    it, so a pass that offered it again would repeat the work. The key keeps
    ``intake.set`` out and the library keeps another library's jobs out. The
    hearts are kept out by the readers, which ask :func:`recorded_as` and skip
    a job it records nothing for.
    """
    return tuple(
        job
        for job in jobs.list_jobs(store)
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
    )


def completed(found: Iterable[jobs.Job]) -> tuple[str, ...]:
    """The playlists whose job succeeded, oldest first, each once."""
    seen: list[str] = []
    for job in reversed(tuple(found)):
        identity = recorded_as(job)
        if job.state == jobs.JobState.SUCCEEDED and identity and identity not in seen:
            seen.append(identity)
    return tuple(seen)


def open_playlists(found: Iterable[jobs.Job]) -> frozenset[str]:
    """The playlists an open playlist intake job is still working on."""
    return frozenset(recorded_as(job) for job in found if job.is_open() and recorded_as(job))


def reconcile(store, cfg: config.Config, *, handler_key: str) -> tuple[str, ...]:
    """Record every playlist whose job completed cleanly. Returns the newly recorded."""
    # NOT ``marks``, which is this module's deferred mark engine. The local name
    # used to be ``marks`` and shadowed nothing, because nothing here imported
    # the engine until R-358 did.
    cursor = WatermarkStore(cfg)
    existing = cursor.read(SOURCE_ID)
    known = set(existing.swept) if existing is not None else set()
    fresh = [
        identity
        for identity in completed(playlist_jobs(store, cfg, handler_key=handler_key))
        if identity not in known
    ]
    cursor.record_swept(SOURCE_ID, fresh, library_id=cfg.library.volume_id)
    return tuple(fresh)


@dataclass
class Sweep:
    """What one pass decided about every playlist the account listed."""

    listed: tuple[AccountPlaylist, ...] = ()
    #: Playlist identifier to frozen tracks, in listing order, for the queue.
    ready: dict[str, dict[str, Any]] = field(default_factory=dict)
    excluded: dict[str, Excluded] = field(default_factory=dict)
    unreadable: dict[str, str] = field(default_factory=dict)
    #: Playlists that listed short of the count the provider declares, as
    #: ``ListingShortfall.block`` carries it (R-515). Queued all the same.
    short: dict[str, dict[str, int]] = field(default_factory=dict)
    recorded_now: tuple[str, ...] = ()
    #: THE WHOLE CURSOR after this pass reconciled, not only what it added. It
    #: is what :func:`mark_swept` marks from, for the reason that function
    #: gives: the cursor moves whether or not the mark lands, so a mark set
    #: taken from :attr:`recorded_now` is a set nothing can offer a second time.
    recorded: frozenset[str] = frozenset()

    def names(self) -> dict[str, str]:
        return {playlist.playlist_id: playlist.name for playlist in self.listed}


def _listed_or_refuse(found: Catalogue) -> tuple[AccountPlaylist, ...]:
    try:
        return tuple(found.account_playlists())
    except CratekitError:
        raise
    except Exception as exc:
        raise refuse(
            "sync-source-lookups-failed",
            f"the account's playlists could not be listed ({type(exc).__name__}: "
            f"{exc}); an unread listing is not an account with nothing new",
            steps=("retry the sync when the provider is reachable",),
            scope=Scope.SOURCE,
            origin=("sync.playlists",),
            detail={"source_id": SOURCE_ID},
        ) from exc


def account_names(found: Catalogue) -> dict[str, str]:
    """Every playlist the account lists, identifier to name, or the refusal.

    The listing ``sync unmark`` plans and rechecks against (R-838), through the
    same refusal an unread listing gets everywhere else here.
    """
    return {playlist.playlist_id: playlist.name for playlist in _listed_or_refuse(found)}


def plan(
    store,
    cfg: config.Config,
    found: Catalogue,
    *,
    handler_key: str,
    label_built: frozenset[str] = frozenset(),
    set_built: frozenset[str] = frozenset(),
    paired: frozenset[str] = frozenset(),
    mirrored: frozenset[str] = frozenset(),
) -> Sweep:
    """Reconcile the cursor, list the account, and decide every playlist.

    Reconciled FIRST so a playlist whose job finished since the last pass is
    excluded as recorded in this one rather than queued again.

    ``label_built`` is every year playlist ``label playlists`` recorded, HANDED
    IN rather than read here, because this source is core and the record is
    the outbound package's, which a core module does not import (R-835).
    ``set_built`` is every playlist ``export set`` made, handed in for the same
    reason (R-837). ``paired`` is every account playlist ``sync pair`` keeps,
    handed in for the same reason (U130). ``mirrored`` is every playlist
    ``crate organize`` mirrors a rekordbox playlist into, for the same reason
    (U147).
    """
    recorded_now = reconcile(store, cfg, handler_key=handler_key)
    existing = WatermarkStore(cfg).read(SOURCE_ID)
    recorded = frozenset(existing.swept) if existing is not None else frozenset()
    in_flight = open_playlists(playlist_jobs(store, cfg, handler_key=handler_key))

    sweep = Sweep(
        listed=_listed_or_refuse(found),
        recorded_now=recorded_now,
        recorded=recorded,
    )
    for playlist in sweep.listed:
        reason = exclusion(
            playlist,
            recorded=recorded,
            in_flight=in_flight,
            label_built=label_built,
            set_built=set_built,
            paired=paired,
            mirrored=mirrored,
        )
        if reason is not None:
            sweep.excluded[playlist.playlist_id] = reason
            continue
        try:
            tracks, short = intake_cli.list_playlist_declared(found, playlist.playlist_id)
        except CratekitError as exc:
            if exc.cause.reason not in PER_PLAYLIST_REASONS:
                raise
            sweep.excluded[playlist.playlist_id] = Excluded.UNREADABLE
            sweep.unreadable[playlist.playlist_id] = exc.cause.message
            continue
        if short is not None:
            # SAID, NEVER REFUSED (R-515): the rows served are queued, and the
            # summary carries how many the provider counted and withheld.
            sweep.short[playlist.playlist_id] = short.block()
        if not tracks:
            # THE COUNT WAS UNKNOWN OR STALE, and the listing is what answers.
            sweep.excluded[playlist.playlist_id] = Excluded.EMPTY
            continue
        sweep.ready[playlist.playlist_id] = tracks
    return sweep


def queue(
    store,
    cfg: config.Config,
    sweep: Sweep,
    *,
    handler_key: str,
    run_id: str,
    filed: list[jobs.Job],
) -> None:
    """Queue one intake playlist job per ready playlist, under the shared run.

    ``filed`` is appended to AS EACH JOB IS QUEUED, because each enqueue is its
    own transaction: a refusal on the third playlist leaves the first two filed,
    and the caller has to be able to name them.

    EACH JOB CARRIES THE NAME THE ACCOUNT LISTED (U113), so the landing can
    give the playlist its own INBOX playlist under that name without listing
    the account again, after ``sync mark`` has prefixed it.
    """
    names = sweep.names()
    for playlist_id, tracks in sweep.ready.items():
        filed.append(
            intake_cli.queue_playlist(
                store,
                cfg,
                handler_key=handler_key,
                reference=playlist_id,
                tracks=tracks,
                run_id=run_id,
                source_id=SOURCE_ID,
                name=names.get(playlist_id),
            )
        )


def marking_sweep(store, cfg: config.Config, found: Catalogue, *, handler_key: str) -> Sweep:
    """The sweep a mark is taken from, built WITHOUT MOVING THE CURSOR.

    :func:`plan` reconciles first, which writes the cursor, and lists every new
    playlist track by track, which is provider calls a mark has no use for. A
    mark is asked for between passes, by a verb that stops at a gate before it
    does anything, and a verb that wrote the cursor on its way to the question
    would have moved state for an answer of abort.

    So ``recorded`` here is what the cursor holds TOGETHER WITH what
    :func:`reconcile` would add at the top of the next pass, the playlists whose
    job this source queued has SUCCEEDED. Read from the cursor alone, the
    ordinary sequence of pass, list, download, land, mark would find nothing
    recorded, because nothing reconciles between the pass and the mark. The rule
    for what counts as recorded is :func:`completed`, the one :func:`reconcile`
    uses, so this reads the policy and does not restate it.
    """
    existing = WatermarkStore(cfg).read(SOURCE_ID)
    held = set(existing.swept) if existing is not None else set()
    held.update(completed(playlist_jobs(store, cfg, handler_key=handler_key)))
    return Sweep(listed=_listed_or_refuse(found), recorded=frozenset(held))


def pending_marks(
    sweep: Sweep, *, only: frozenset[str] | None = None
) -> tuple[marks.PendingMark, ...]:
    """Every recorded playlist the account still lists under an unprefixed name.

    ``only`` NARROWS AND NEVER WIDENS. A caller that knows which playlists a
    landed file completes passes them, and the set is what was already pending
    AND is named there, so an identifier that is not recorded, not listed or
    already prefixed is not marked because somebody named it. ``None`` is every
    pending playlist, and an empty set is none of them: the two are different
    answers and ``if only`` would have read them as one.

    **THE SET IS THE WHOLE CURSOR AND NOT** :attr:`Sweep.recorded_now`. The
    cursor is written by :func:`reconcile` at the top of :func:`plan`, before
    anything could have marked anything, and it moves whether the mark then
    lands, refuses or finds a stale recheck. So a set taken from what this pass
    ADDED is a set no later pass can offer again: the playlist is recorded, it
    is excluded as :attr:`Excluded.RECORDED` forever after, and it never carries
    the prefix. Taking the set from what the cursor HOLDS makes a mark that did
    not land this pass an ordinary candidate on the next one.

    What ends the retrying is the mark itself. A playlist the prefix reached is
    listed under a swept name, and a swept name is skipped here, so the set
    shrinks by exactly what landed. That is also why a name already carrying the
    prefix is skipped rather than marked again: the prefix goes on the title, so
    a second pass over one would build ``DOWNLOADED DOWNLOADED Warmup``.

    A recorded playlist the account no longer lists has no name to prefix and is
    not pending. Nothing is owed to a playlist that is gone.

    **THE LABEL BATCH'S DEBRIS IS NEVER MARKED (R-361).** A pass no longer
    queues a ` LIBRARY` name, and a job for one can still reach the cursor: the
    eleven the fourth sitting left queued, resumed, or one a person ran through
    ``crate intake playlist``, which R-382 records. Its name is the source
    system's throwaway and the source system's own sweep never prefixes it, so
    neither does this one. Asked here and not only in :func:`exclusion`, because
    the exclusion decides what is OFFERED and this decides what is RENAMED, and
    a rule on the offering path leaves the renaming path open.
    """
    listed = sweep.names()
    return tuple(
        marks.PendingMark(target_id=identity, kind=MARK_KIND)
        for identity in sorted(sweep.recorded)
        if listed.get(identity)
        and not is_swept_name(listed[identity])
        and not is_library_debris(listed[identity])
        and (only is None or identity in only)
    )


def mark_swept(
    sweep: Sweep,
    found: Catalogue,
    account: RemoteAccount,
    *,
    local_output: Path | marks.NativeLanding,
    applied: list[str] | None = None,
    only: frozenset[str] | None = None,
) -> tuple[str, ...]:
    """Prefix the recorded playlists on the account. Returns the marked ids.

    ``only`` is :func:`pending_marks`'s, handed straight through.

    **THE FILE IS CHECKED FIRST AND BY** :func:`marks.apply_deferred`, which
    refuses ``sync-marks-blocked`` when the importable file is missing or empty.
    There is deliberately no early return in front of it: a call with nothing
    pending and no file still refuses, because a caller that has no file is
    wrong about the run whether or not this pass happened to record anything.

    ``applied`` is APPENDED TO AS EACH RENAME LANDS, on :func:`queue`'s pattern
    and for its reason. Each rename is its own remote write, a failure on the
    third playlist leaves the first two renamed on the account, and the return
    value is gone when this raises. A caller that wants to name what landed
    passes a list; a caller that does not is relying on the next pass to see the
    prefix, which :func:`pending_marks` makes true.

    **THE ONE PRODUCTION CALLER IS** ``sync/mark_cli.py`` (U82), which hands it
    the intake file a landing wrote and the playlists that file completes, or,
    on a database native intake tree, a :class:`marks.NativeLanding` (R-777). The
    pass itself still never calls this, since a pass writes no importable file.
    """
    listed = sweep.names()
    landed = applied if applied is not None else []
    held: list[dict[str, str]] = []

    def current() -> dict[str, str]:
        """The account's names now, read ONCE and only when a mark asks."""
        if not held:
            held.append(
                {
                    playlist.playlist_id: playlist.name
                    for playlist in _listed_or_refuse(found)
                }
            )
        return held[0]

    def recheck(mark: marks.PendingMark) -> bool:
        name = listed.get(mark.target_id) or ""
        return bool(name) and current().get(mark.target_id) == name

    def apply(mark: marks.PendingMark) -> None:
        account.rename_playlist(mark.target_id, SWEPT_PREFIX + listed[mark.target_id])
        landed.append(mark.target_id)

    return marks.apply_deferred(
        pending_marks(sweep, only=only),
        local_output=local_output,
        recheck=recheck,
        apply=apply,
    )


def report(
    sweep: Sweep, filed: Sequence[jobs.Job], *, marked: Sequence[str] | None = None
) -> dict[str, Any]:
    """The playlists block of the pass summary. Identifiers first, names to read.

    ``marked`` is what :func:`mark_swept` returned, or ``None`` when the pass
    never reached the mark step. The two are different facts and the block says
    which: ``None`` reports :data:`MARK_UNBOUND`, and an empty result reports
    :data:`MARK_APPLIED` with nothing under ``marked``, which is a mark step that
    ran and found every recheck stale.
    """
    names = sweep.names()
    return {
        "listed": len(sweep.listed),
        "queued": [
            {
                "playlist_id": _playlist_of(job),
                "name": names.get(_playlist_of(job), ""),
                "job_id": job.job_id,
                "items": len((job.payload or {}).get(intake_cli.TRACKS) or {}),
            }
            for job in filed
        ],
        "excluded": {
            identity: {"reason": str(reason), "name": names.get(identity, "")}
            for identity, reason in sweep.excluded.items()
        },
        "unreadable": dict(sweep.unreadable),
        "withheld": {
            identity: {**block, "name": names.get(identity, "")}
            for identity, block in sweep.short.items()
        },
        "recorded_now": list(sweep.recorded_now),
        "swept_means": SWEPT_MEANS,
        "mark": MARK_UNBOUND if marked is None else MARK_APPLIED,
        "marked": list(marked or ()),
    }


def said(block: Mapping[str, Any]) -> str | None:
    """The words for what the block says swept means, or ``None`` when it says nothing.

    Read off the block's own token rather than returned unconditionally, so a
    block that stopped carrying the field is also a check that stopped saying it.
    """
    return SWEPT_MEANS_SAID.get(str(block.get("swept_means") or ""))


__all__ = [
    "LIBRARY_PLAYLIST_SUFFIX",
    "MARK_APPLIED",
    "MARK_KIND",
    "MARK_UNBOUND",
    "PER_PLAYLIST_REASONS",
    "SOURCE_ID",
    "SWEPT_MEANS",
    "SWEPT_MEANS_SAID",
    "SWEPT_PREFIX",
    "Excluded",
    "Sweep",
    "account_names",
    "completed",
    "exclusion",
    "is_library_debris",
    "is_swept_name",
    "mark_swept",
    "marking_sweep",
    "open_playlists",
    "pending_marks",
    "playlist_jobs",
    "playlist_of",
    "plan",
    "queue",
    "reconcile",
    "recorded_as",
    "report",
    "said",
    "source_jobs",
]
