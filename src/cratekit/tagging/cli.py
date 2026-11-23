"""``crate tag folder``: queue genre tagging over a folder, and drive it.

Every file is one or more paced questions to a public catalogue, so a folder
is long work, and long work is queued (conformance 5): the verb freezes the
folder and the configuration (KTD9), queues one job with one item per audio
file, and reports the job. :func:`handle` is the worker behind it. Run by hand
it drives the job before returning (U192), through
:func:`cratekit.modules.foreground.settle`; ``--queue-only`` only queues.

The items are the engine's own walk, :func:`cratekit.tagging.tag.audio_files`
(KTD7), so the job cannot cover files the engine would not tag. They are
relative to the folder, and a report is named by the item's ordinal, so no
filename is built from one. The folder is frozen absolute, since a resume is a
fresh process started in any directory.

The genres and match needles of every registered label are frozen with the
job (U178, U240), so a resume tags by what was registered when it was asked
for, and a file with no label tag in a sweep given no ``--label`` is matched
by its copyright line through :func:`copyright_matcher`. A job queued before
either froze none and is tagged as it always was.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING

from cratekit.cli.output import Envelope, load_config
from cratekit.core import active_taxonomy, config, jobs, taxonomy, taxonomy_word
from cratekit.core.cause import Cause, CratekitError, Outcome, rebuilt, refuse
from cratekit.modules import foreground
from cratekit.tagging import artifacts, published, searchers, shell

# Aliased: this module's ``tag_folder`` is the verb, the engine's is the engine.
from cratekit.tagging import tag as tag_engine
from cratekit.tagging.summary import WAY_CATALOGUE, WAY_LABEL, WAY_NONE, _files, _summary
from cratekit.tagging.summary import _refusal_stop as _refusal_stop
from cratekit.tagging.summary import _refused_out as _refused_out

if TYPE_CHECKING:
    from cratekit.label import registry as labels

# Warning codes, not causes: in each the sweep succeeded and what it says is a
# fact a person should see, never a reason anything did not happen.

#: Some tagged files took a word the declared taxonomy does not know (R-650).
OFF_TAXONOMY = "tag-folder-off-taxonomy"

#: Files left untagged because a catalogue went unread for them, not because
#: none carried them (R-791); since U244 that includes not asked for want of a
#: token. They are askable again on the next run.
SOURCES_UNREAD = "tag-folder-sources-unread"

#: A catalogue refused every search it was sent (U281). Apart from the count
#: above: a whole catalogue gave the run nothing, which a person must know
#: before trusting any decline in it.
SOURCE_BLOCKED = "tag-folder-source-blocked"

#: The general catalogue could not be read on files it was asked about,
#: blocked, unreachable or unparsable (R-796); one code, one consequence.
PUBLISHED_UNREAD = "tag-folder-published-unread"

#: Files the general catalogue could not be asked about for want of an ISRC
#: (R-796); another run will not move them. Named apart from the engine's
#: ``NO_ISRC`` so one name does not mean two strings.
NO_ISRC_FILES = "tag-folder-no-isrc"

#: Files Discogs was not asked about for want of a recorded token (U244).
DISCOGS_NO_TOKEN_FILES = "tag-folder-discogs-no-token"

#: Files Discogs was not read for because it refused the recorded token (U282's
#: review), or a sweep Beatport settled whole would end clean over it.
DISCOGS_TOKEN_REFUSED_FILES = "tag-folder-discogs-token-refused"

#: ``--label`` names a label registered with no genre (U178); its files are
#: searched as always, which is a correct sweep, so not a refusal.
LABEL_NO_GENRE = "tag-folder-label-no-genre"

#: The label registry could not be read at queue time (U178); no label's genre
#: was applied, rather than reading it as a registry holding none.
LABEL_REGISTRY_UNREAD = "tag-folder-label-registry-unread"

#: Under ``--label``, files whose own label tag names no label with a genre
#: (U178); the file's tag outranks ``--label``, so they were searched.
LABEL_TAG_OUTRANKED = "tag-folder-label-tag-outranked"

#: A resume was given ``--label`` (U178), which it does not apply: the label is
#: frozen at queue time.
LABEL_ON_RESUME = "tag-folder-label-on-resume"

#: Files whose copyright line named more than one registered label (U240);
#: they were searched rather than given either label's genre.
COPYRIGHT_AMBIGUOUS = "tag-folder-copyright-ambiguous"


def build(parser, entry) -> None:
    """Declare the verb's arguments; unannotated, since ``Entry`` is a layer up (KTD23)."""
    parser.add_argument("folder", help="folder of audio to tag")
    foreground.add_job_options(parser, what="tagging")
    parser.add_argument(
        "--label",
        default=None,
        metavar="NAME",
        help=(
            "the registered label of every file here that carries no label tag; a "
            "label registered with a genre gives it to each such file with no "
            "genre, and no catalogue is asked about it; without it, a file's "
            "copyright line naming one registered label names its label"
        ),
    )
    parser.set_defaults(_handler=tag_folder)


def tag_argv(job) -> list[str]:
    """The command line that continues one queued sweep (KTD9).

    It names the job as well as the folder, so a resume never queues a second
    record for one piece of work.
    """
    folder = job.payload.get("folder", "")
    return ["tag", "folder", folder, "--job", job.job_id]


def _ambiguous_warnings(summary: dict) -> tuple[dict[str, str], ...]:
    """Name the files a copyright line could not settle because it named two labels (U240)."""
    ambiguous = summary.get("copyright_ambiguous") or {}
    if not ambiguous:
        return ()
    files = sum(ambiguous.values())
    named = "; ".join(f"{labels_named} on {count}" for labels_named, count in sorted(ambiguous.items()))
    return (
        {
            "code": COPYRIGHT_AMBIGUOUS,
            "message": (
                f"{_files(files)} not given a label's genre because the copyright "
                f"line names more than one registered label ({named}), and each was "
                f"asked of the catalogues instead. A file still without a genre "
                f"takes its label's once it carries its label tag and the folder "
                f"is run again; a file a catalogue tagged keeps that genre"
            ),
        },
    )


def _unread_warnings(summary: dict) -> tuple[dict[str, str], ...]:
    """Say how many files no catalogue answer settled, and which catalogue refused all.

    The count keeps a sweep whose fallbacks were all refused from reading as a
    clean no-hit (R-791), and names each unread answer per source, since each
    sends a person somewhere else; a parse break is said to be a defect a rerun
    will not move. A catalogue is named when it was blocked on every file it
    was sent, not every file in the folder, in the walk's source order. The
    general catalogue is in the count only; its refusal and parse break are
    :func:`_published_warnings`'s (R-796).
    """
    warnings: list[dict[str, str]] = []
    answers = summary.get("answers") or {}
    unread = (summary.get("skipped") or {}).get(tag_engine.SOURCES_UNREAD, 0)
    if unread:
        seen = "; ".join(
            _unread_phrase(summary, source, word, counted[word])
            for source, counted in answers.items()
            for word in searchers.UNREAD_ANSWERS
            if counted.get(word)
        )
        # A catalogue nobody asked is in the tally too (U244's review), or a
        # sweep with no Discogs token ends its sentence on an empty list.
        passed = int(summary.get("discogs_without_token") or 0)
        if passed:
            seen = "; ".join(
                part
                for part in (seen, f"{searchers.DISCOGS} not asked for want of a token on {passed}")
                if part
            )
        broken = any(
            (answers.get(source) or {}).get(searchers.Answer.PARSE_BREAK.value)
            for source in searchers.SOURCES
        )
        warnings.append(
            {
                "code": SOURCES_UNREAD,
                "message": (
                    f"{_files(unread)} left untagged because at least one "
                    f"catalogue went unread for them, so whether any "
                    f"catalogue carries them is unknown. They are not reported as "
                    f"no-hit, and the next run over this folder asks again; each "
                    f"file's record says what every catalogue answered. Across "
                    f"the sweep: {seen or 'nothing counted'}"
                    + (
                        ". A parse break is a defect in this software that "
                        "another run will not move; report it"
                        if broken
                        else ""
                    )
                ),
            }
        )
    # The record shops only: the general catalogue's refusal has its own warning.
    for source in searchers.SOURCES:
        counted = answers.get(source) or {}
        # Sent, not only answered (U281): a file answered from the run's memory
        # of a refusal was never a search this catalogue was sent.
        held = int((summary.get("not_sent") or {}).get(source) or 0)
        asked = sum(count for word, count in counted.items() if word != searchers.NOT_ASKED)
        sent = asked - held
        if sent > 0 and counted.get(searchers.Answer.BLOCKED.value, 0) - held == sent:
            warnings.append(
                {
                    "code": SOURCE_BLOCKED,
                    "message": (
                        f"{source} refused every one of the {sent} searches it "
                        f"was sent, with a bot check, a block page or a rate "
                        f"limit that outlasted the backoff, rather than a result, "
                        f"so it contributed nothing to this run"
                        + (
                            f", and was not asked about {held} more file(s) once "
                            f"it had refused this client"
                            if held
                            else ""
                        )
                        + f". This tool does not try to get past one; {source} "
                        f"stays unread until it answers this machine again"
                    ),
                }
            )
    return tuple(warnings)


def _unread_phrase(summary: dict, source: str, word: str, count: int) -> str:
    """One catalogue's unread answer in the sweep's tally, a refusal named as one (U281).

    A refusal read as ``unreachable`` sent a person to their network over a
    block no network check moves. The challenge is named when every refusal
    counted was one, and counted when some were.
    """
    if word != searchers.Answer.BLOCKED.value:
        return f"{source} {word} on {count}"
    challenged = int((summary.get("challenged") or {}).get(source) or 0)
    held = int((summary.get("not_sent") or {}).get(source) or 0)
    if challenged >= count:
        said = f"{source} refused this client ({searchers.CLOUDFLARE_CHALLENGE}) on {count}"
    elif challenged:
        said = (
            f"{source} refused this client on {count} "
            f"({searchers.CLOUDFLARE_CHALLENGE} on {challenged})"
        )
    else:
        said = f"{source} refused this client on {count}"
    if held:
        said += f", {held} of them not asked once it had refused this client"
    return said


def _discogs_warnings(summary: dict) -> tuple[dict[str, str], ...]:
    """Count the files Discogs was not asked about for want of a token (U244).

    Those files are not no-hit, and this says once what would let a run ask
    Discogs. A token Discogs refused is said apart (U282's review): the person
    believes it works, and a sweep Beatport settled whole would say nothing.
    """
    warnings: list[dict[str, str]] = []
    refused = int(summary.get("discogs_token_refused") or 0)
    if refused:
        warnings.append(
            {
                "code": DISCOGS_TOKEN_REFUSED_FILES,
                "message": (
                    f"Discogs refused the recorded token, so it was not read for "
                    f"{refused} file(s); the other catalogues were asked about "
                    f"them as usual. To record a working one: "
                    f"{searchers.DISCOGS_LOGIN_STEPS}"
                ),
            }
        )
    count = int(summary.get("discogs_without_token") or 0)
    if not count:
        return tuple(warnings)
    return (
        *warnings,
        {
            "code": DISCOGS_NO_TOKEN_FILES,
            "message": (
                f"Discogs was not asked about {count} file(s) because no Discogs "
                f"token is recorded, or the keychain no longer holds the recorded "
                f"one; any of them no other catalogue tagged was not reported as "
                f"no-hit. To ask it: "
                f"{searchers.DISCOGS_LOGIN_STEPS}"
            ),
        },
    )


def _published_warnings(summary: dict) -> tuple[dict[str, str], ...]:
    """Say when the general catalogue went unread, and count the no ISRC files.

    Unread files are counted against the files it was asked about (a match, a
    miss or an unread answer, never ``not-asked`` or ``no-isrc``), so a run
    Beatport mostly settled cannot hide a refusal on the rest; one warning for
    a block, an outage and a parse break. Said whatever the files' skip reason,
    since a catch-all file is ``unmapped-genre`` whatever this catalogue did.
    The no ISRC count is its own warning: ``sources-unread`` promises another
    run asks again, and for these files it asks this catalogue nothing.
    """
    counted = (summary.get("answers") or {}).get(published.SOURCE) or {}
    warnings: list[dict[str, str]] = []
    unread = {word: counted.get(word, 0) for word in published.UNREAD}
    failed = sum(unread.values())
    asked = failed + sum(
        counted.get(word, 0)
        for word in (searchers.Answer.MATCHED.value, searchers.Answer.MISS.value)
    )
    if failed:
        seen = "; ".join(f"{word} on {count}" for word, count in unread.items() if count)
        if failed == asked:
            reach = f"any of the {asked} files it was asked about"
            cost = "no file in this run got a published genre from it"
        else:
            reach = f"{failed} of the {asked} files it was asked about"
            cost = "those files got no published genre from it"
        warnings.append(
            {
                "code": PUBLISHED_UNREAD,
                "message": (
                    f"{published.SOURCE}, the general catalogue asked by ISRC, "
                    f"could not be read on {reach} ({seen}), so {cost} and "
                    f"their declines were made without it. This tool does not "
                    f"try to get past a block or a rate limit, and once refused "
                    f"it asks nothing more in the same run; run the folder again "
                    f"once the catalogue answers this machine"
                    + (
                        ". A parse break is a defect in this software that "
                        "another run will not move; report it"
                        if unread.get(searchers.Answer.PARSE_BREAK.value)
                        else ""
                    )
                ),
            }
        )
    bare = counted.get(tag_engine.NO_ISRC, 0)
    if bare:
        warnings.append(
            {
                "code": NO_ISRC_FILES,
                "message": (
                    f"{_files(bare)} not asked about at {published.SOURCE} because "
                    f"the file carries no ISRC, or a value that does not read as "
                    f"one, and that catalogue is asked by ISRC and never by a "
                    f"search. They are not reported as tracks no catalogue "
                    f"carries, and another run will not change it; each file's "
                    f"record says what its tag held"
                ),
            }
        )
    return tuple(warnings)


def _declared(cfg: config.Config) -> taxonomy.Taxonomy | None:
    """The library's taxonomy for a warning's wording, or None when unreadable.

    A report is never refused for a sentence; doctor names an unreadable copy.
    """
    try:
        return active_taxonomy.load(cfg)
    except CratekitError:
        return None


def _off_taxonomy_warning(
    summary: dict, declared: taxonomy.Taxonomy | None = None
) -> tuple[dict[str, str], ...]:
    """Say out loud that some of what was tagged is outside the declared table (R-650).

    A count alone leaves a person told the folder tagged cleanly, so the
    warning names the words, sorted so two runs over one folder read alike. It
    never fails the verb: the files are tagged and the sweep is unattended. It
    says nothing of where the tracks landed, since routing reads other rules
    and some off taxonomy words route to a real bucket. A genre folder's own
    name in another case is named with its one answer when the taxonomy reads
    (R-1184).
    """
    counted = summary.get("off_taxonomy") or {}
    if not counted:
        return ()
    files = sum(counted.values())
    words = ", ".join(sorted(counted))
    return (
        {
            "code": OFF_TAXONOMY,
            "message": (
                f"{files} of the {summary.get('tagged', 0)} files tagged were "
                f"given a genre your taxonomy has no place of its own for, from "
                f"these catalogue answers: {words}. Each word was written onto "
                f"its file exactly as the catalogue said it, so the tags on disk "
                f"are no longer only the ones your template declares. Save any "
                f"you want the taxonomy to own as an alias of one of your genres, "
                f"with {taxonomy_word.ALIAS_VERB} WORD GENRE, or make it a genre "
                f"folder of its own, with {taxonomy_word.FOLDER_VERB} WORD"
                + taxonomy_word.own_names(declared, counted)
            ),
        },
    )


def _empty(reason: str, detail: str) -> tuple[dict, tuple[dict[str, str], ...]]:
    """The payload and warning for a folder with nothing to tag.

    Nothing is queued: a job with no items reports SUCCEEDED, a clean sweep
    over a folder nothing walked. The payload is the shared no-op shape
    (R-234).
    """
    return shell.no_op("no-op"), ({"code": reason, "message": detail},)


def tag_folder(ctx) -> Envelope:
    """Queue one tagging sweep over a folder and drive it, or drive it on a resume.

    Three zeroes, three warnings, since the next move differs: no audio, no
    such folder, or no folder named. An empty name is ``Path("")``, the
    current directory, which this writing verb must never sweep.
    """
    cfg = load_config(("tagging.cli",))
    if ctx.args.job:
        return _resume(ctx, cfg, ctx.args.job, typed_label=ctx.args.label)

    named = str(ctx.args.folder or "")
    if not named.strip():
        payload, warnings = _empty(
            "tag-folder-unnamed",
            "no folder was named, and this verb writes to the files it walks, so "
            "it will not fall back to the directory you are standing in",
        )
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=warnings)

    folder = Path(named).expanduser().absolute()
    frozen, label_warnings = _label_payload(ctx.args.label)
    files = tag_engine.audio_files(folder)
    if not files:
        payload, warnings = (
            _empty(
                "tag-folder-no-audio",
                f"{folder} holds no audio files this build can tag, so there is "
                f"nothing to sweep",
            )
            if folder.is_dir()
            else _empty(
                "tag-folder-absent",
                f"{folder} is not a folder on this machine, so there is nothing "
                f"to sweep",
            )
        )
        return ctx.envelope(data=payload, outcome=Outcome.NO_OP, warnings=warnings)

    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={"folder": str(folder), **frozen},
            item_ids=tuple(str(path.relative_to(folder)) for path in files),
            cfg=cfg,
        )
        if foreground.queue_only(ctx.args):
            return ctx.envelope(data=shell.reported(store, job), warnings=label_warnings)
    # Driven through the resume (U192): this call's ``--label`` is the frozen
    # one, so the resume is told none was typed, and the queue's warnings lead.
    return foreground.settle(
        job.job_id,
        lambda: _resume(ctx, cfg, job.job_id, typed_label=None, queued=label_warnings),
        argv=tag_argv(job),
        origin="tagging.cli",
    )


def _label_payload(label: str | None) -> tuple[dict, tuple[dict[str, str], ...]]:
    """What a sweep freezes about labels, and what it warns about them (U178).

    Every registered label's genre by identifier, and ``--label`` resolved to
    its name and identifier (R-1476); nothing when there is nothing to freeze.
    A ``--label`` naming no registered label is refused before anything is
    queued, since a typo would tag the folder from the catalogues; one with no
    genre is warned about. An unreadable registry refuses a sweep given
    ``--label`` and warns on one that was not.
    """
    from cratekit.label import registry as labels

    try:
        held = labels.RegistryStore().load()
    except CratekitError as exc:
        if label is not None:
            raise
        return {}, (
            {
                "code": LABEL_REGISTRY_UNREAD,
                "message": (
                    f"the label registry could not be read ({exc.cause.message}), "
                    f"so no label's genre was applied and every file is asked of "
                    f"the catalogues as before"
                ),
            },
        )
    frozen: dict = {}
    warnings: tuple[dict[str, str], ...] = ()
    genres = {
        entry.label_id: {"name": entry.name, "genre": entry.genre}
        for entry in held.labels.values()
        if entry.genre
    }
    if genres:
        frozen["label_genres"] = genres
        # Every label's needle, with a genre or without (U240), so a line naming
        # one of each settles neither; only beside genres, which it could tag.
        frozen["label_needles"] = {
            entry.label_id: {"name": entry.name, "needle": entry.match or entry.name}
            for entry in held.labels.values()
        }
    if label is not None:
        entry = held.resolve(label) if label.strip() else None
        if entry is None:
            raise refuse(
                "label-unknown",
                f"no favourite label is named {label!r}, so the files of this folder "
                f"cannot be given its genre; nothing was queued",
                steps=(
                    "list the registry with crate label registry and pass a name from "
                    "it, or add the label first",
                ),
                origin=("tagging", "cli"),
                detail={"label": label},
            )
        frozen["label"] = entry.name
        # The sweep answers by identifier (R-1476): two labels can share a name.
        frozen["label_id"] = entry.label_id
        if not entry.genre:
            # The remedy names the identifier, which ``registry set`` resolves
            # first; a name could set another label (R-1476's review).
            shared = len(held.named(entry.name)) > 1
            called = f"{entry.name} ({entry.label_id})" if shared else entry.name
            handle = entry.label_id
            warnings = (
                {
                    "code": LABEL_NO_GENRE,
                    "message": (
                        f"{called} is registered with no genre, so its files are "
                        f"asked of the catalogues as before; give it one with crate "
                        f"label registry set {handle!r} --genre WORD"
                    ),
                },
            )
    return frozen, warnings


def _label_warnings(
    typed: str | None, payload: Mapping, summary: dict
) -> tuple[dict[str, str], ...]:
    """What a resume says about labels: a ``--label`` it did not apply, and tags that outranked one.

    The tags are named only for a sweep queued with ``--label``: the person
    said what the folder is, and would otherwise find those files untagged.
    """
    warnings: list[dict[str, str]] = []
    if typed is not None:
        warnings.append(
            {
                "code": LABEL_ON_RESUME,
                "message": (
                    f"--label {typed!r} was not applied: a sweep tags by the label it "
                    f"was queued with, "
                    + (
                        f"{payload['label']}"
                        if payload.get("label")
                        else "none for this one"
                    )
                    + ", so queue a new sweep over the folder to tag by another"
                ),
            }
        )
    outranked = summary.get("label_tags") or {}
    if payload.get("label") and outranked:
        files = sum(outranked.values())
        named = ", ".join(f"{tag} on {count}" for tag, count in sorted(outranked.items()))
        warnings.append(
            {
                "code": LABEL_TAG_OUTRANKED,
                "message": (
                    f"{_files(files)} not given {payload['label']}'s genre because "
                    f"the file's own label tag names no one label with a genre: the "
                    f"registry holds its label with no genre, names two labels or "
                    f"more by it, or does not hold it at all ({named}), and a "
                    f"file's own tag outranks --label; they were asked of the "
                    f"catalogues instead. Correct the tag, or give its label a genre "
                    f"in the registry, and run the folder again"
                ),
            }
        )
    return tuple(warnings)


def _frozen_labels(payload: Mapping) -> labels.Registry | None:
    """Every label the job froze, each with its own genre or none, or None for no genres.

    Those without a genre come from the needles U240 freezes, joined by
    identifier (R-1476), so a name such a label holds answers nothing rather
    than landing on another label.
    """
    from cratekit.label import registry as labels

    frozen = payload.get("label_genres")
    if not isinstance(frozen, Mapping) or not frozen:
        return None
    genres = {
        str(label_id): str(row["genre"])
        for label_id, row in frozen.items()
        if isinstance(row, Mapping) and isinstance(row.get("genre"), str) and row["genre"]
    }
    entries: dict[str, labels.LabelEntry] = {}
    needles = payload.get("label_needles")
    for rows in (needles if isinstance(needles, Mapping) else {}, frozen):
        for label_id, row in rows.items():
            if isinstance(row, Mapping) and str(label_id) not in entries:
                entries[str(label_id)] = labels.LabelEntry(
                    label_id=str(label_id),
                    name=str(row.get("name") or label_id),
                    genre=genres.get(str(label_id)),
                )
    return labels.Registry(labels=entries)


def _answered(entry: labels.LabelEntry | None) -> tag_engine.LabelAnswer | None:
    if entry is None or not entry.genre:
        return None
    return tag_engine.LabelAnswer(label=entry.name, genre=entry.genre)


def _name_slug(name: str) -> str:
    """The slug a name would have, or empty for one that could never be a label."""
    from cratekit.label import registry as labels

    try:
        return labels.slug(name) if name.strip() else ""
    except CratekitError:
        return ""


def _label_seam(payload: Mapping) -> tag_engine.LabelGenre | None:
    """The engine's label seam for a file's own label tag, or None for no genres.

    A tag is read as a name first (R-1476): the labels whose display name it
    is, in any case; failing any, those whose name has its slug
    (``Liebe*Detail`` names ``Liebe Detail``); and only then the label whose
    identifier is its slug, one since renamed. A name two labels hold names
    neither. A name that could never be a label is unknown, never a failure.
    """
    held = _frozen_labels(payload)
    if held is None:
        return None

    def answer(name: str) -> tag_engine.LabelAnswer | None:
        named = held.named(name)
        wanted = _name_slug(name)
        if not named and wanted:
            named = tuple(entry for entry in held.labels.values() if _name_slug(entry.name) == wanted)
        if not named and wanted:
            # No label's name: the one registered under it and since renamed.
            named = tuple(entry for entry in (held.labels.get(wanted),) if entry is not None)
        return _answered(named[0]) if len(named) == 1 else None

    return answer


def _folder_seam(payload: Mapping) -> tag_engine.LabelGenre | None:
    """The engine's seam for the sweep's ``--label``, by its frozen identifier, or None.

    Exact (R-1476): never looked up again by a name another label may share.
    None for a sweep queued before the identifier was frozen.
    """
    held = _frozen_labels(payload)
    wanted = str(payload.get("label_id") or "")
    if held is None or not wanted:
        return None

    def answer(_name: str) -> tag_engine.LabelAnswer | None:
        return _answered(held.labels.get(wanted))

    return answer


def copyright_matcher(
    labels: Iterable[tuple[str, str, str | None]],
) -> tag_engine.CopyrightLabels:
    """The engine's copyright seam over ``(name, needle, genre)`` rows, one per label (U240).

    The line, read as the label verbs read one, must carry the whole needle as
    whole words (U237): ``Rawax`` names ``Rawax Records``, never ``RAWAXXX``,
    and ``Music`` never names ``Aus Music``. The most specific needle wins when
    it carries every other one named (a sublabel over its parent); two needles
    neither of which carries the other are both answered, settling neither.
    """
    from cratekit.label import harvest as label_harvest
    from cratekit.label import verify as label_verify

    rows = tuple(
        (str(name), str(needle), str(genre) if genre else None)
        for name, needle, genre in labels
        if name and needle
    )

    def answer(line: str) -> tuple[tag_engine.CopyrightLabel, ...]:
        # The mark and year go first, so ``2020 Vision`` is never named by
        # ``℗ 2020 Vision Quest`` (U240's review, round two).
        credits = label_harvest.labels_from_copyright(_Credit(line or ""))
        if not credits:
            return ()
        credit = credits[0]
        named = [row for row in rows if label_verify.credit_names(row[1], credit)]
        widest = [
            row
            for row in named
            if all(label_verify.credit_names(other[1], row[1]) for other in named)
        ]
        if len(widest) == 1:
            named = widest
        return tuple(tag_engine.CopyrightLabel(label=name, genre=genre) for name, _needle, genre in named)

    return answer


class _Credit:
    """A copyright line in the shape :func:`labels_from_copyright` reads, a track's."""

    __slots__ = ("copyright",)

    def __init__(self, line: str) -> None:
        self.copyright = line


def _copyright_seam(payload: Mapping) -> tag_engine.CopyrightLabels | None:
    """The engine's copyright seam over what the job froze, or None for none.

    Needles and genres are joined by identifier, never by a display name two
    labels can share (U240's review).
    """
    frozen = payload.get("label_needles")
    if not isinstance(frozen, Mapping) or not frozen:
        return None
    genres = payload.get("label_genres")
    genres = genres if isinstance(genres, Mapping) else {}
    rows = []
    for label_id, row in frozen.items():
        if not isinstance(row, Mapping):
            continue
        name = str(row.get("name") or label_id)
        held = genres.get(label_id)
        genre = held.get("genre") if isinstance(held, Mapping) else None
        rows.append((name, str(row.get("needle") or name), genre if isinstance(genre, str) else None))
    return copyright_matcher(rows)


def _resume(
    ctx,
    cfg: config.Config,
    job_id: str,
    *,
    typed_label: str | None,
    queued: tuple[dict[str, str], ...] = (),
) -> Envelope:
    """Continue the sweep already queued under this identifier, and drive it.

    ``typed_label`` is a ``--label`` typed on ``--job``, said and not applied;
    ``queued`` is the queue's own warnings (U192). Every rule of the resume is
    :func:`cratekit.tagging.shell.advance`'s, which raises when the job closed
    carrying a cause (R-225).
    """
    with jobs.open_store() as store:
        try:
            job, warnings = shell.advance(
                ctx,
                store,
                jobs.get(store, job_id),
                origin=("tagging", "cli"),
                nothing_to_run="report a tagging sweep over a folder it never walked",
            )
        except CratekitError as exc:
            raise _with_report(cfg, store, job_id, exc) from exc
        # One summary, so the warnings and the payload cannot disagree.
        summary = _summary(cfg, job.job_id, _causes(store, job.job_id))
        return ctx.envelope(
            data=shell.reported(store, job, {"tagging": summary}),
            warnings=queued
            + tuple(warnings)
            + _label_warnings(typed_label, job.payload or {}, summary)
            + _ambiguous_warnings(summary)
            + _off_taxonomy_warning(summary, _declared(cfg) if summary.get("off_taxonomy") else None)
            + _unread_warnings(summary)
            + _discogs_warnings(summary)
            + _published_warnings(summary),
        )


def _causes(store, job_id: str) -> dict[str, Cause | None]:
    """Every item of the job with its cause, None for an item that carries none."""
    return {item.item_id: item.cause for item in jobs.items(store, job_id)}


#: How many failed files a refusal names by item before it counts the rest.
_FAILED_NAMED = 10

#: The job states whose refusal carries the sweep's report (U240's review).
_REPORTED_ENDINGS = (jobs.JobState.FAILED, jobs.JobState.CANCELLED, jobs.JobState.BLOCKED)


def _with_report(cfg: config.Config, store, job_id: str, error: CratekitError) -> CratekitError:
    """The refusal a sweep that did not finish cleanly leaves with, carrying its report.

    The refusal (R-225) keeps its type and words through
    :func:`cratekit.core.cause.rebuilt`, gains the count of files by label, by
    catalogue or not at all, and carries the summary under ``tagging`` (U240's
    review). One raised before the job ended is passed through untouched.
    """
    job = jobs.get(store, job_id)
    if job.state not in _REPORTED_ENDINGS:
        return error
    summary = _summary(cfg, job_id, _causes(store, job_id))
    ways = summary["ways"]
    failed = [row["item"] for row in summary["files"] if row["failed"]]
    shown = ", ".join(failed[:_FAILED_NAMED]) + (
        f" and {len(failed) - _FAILED_NAMED} more" if len(failed) > _FAILED_NAMED else ""
    )
    said = (
        f"Of {len(summary['files'])} file(s), {ways[WAY_LABEL]} took their registered "
        f"label's genre, {ways[WAY_CATALOGUE]} a catalogue's and {ways[WAY_NONE]} none"
        + (f"; the item failed for {shown}" if failed else "")
        + ". With --output json the per file report is under tagging in this "
        "refusal's detail."
    )
    for warning in _ambiguous_warnings(summary):
        said += " " + warning["message"] + "."
    cause = error.cause
    head = cause.message.rstrip()
    stop = summary.get("refusal_stop")
    remediation = cause.remediation
    if stop:
        # WHO REFUSED, since when, and the token (U284), as the pass says it.
        said += " " + stop["said"] + "."
        remediation = replace(
            remediation,
            steps=(
                *remediation.steps,
                *(step for step in stop["steps"] if step not in remediation.steps),
            ),
        )
    return rebuilt(
        error,
        replace(
            cause,
            message=f"{head}{'' if head.endswith(('.', '!', '?')) else '.'} {said}",
            remediation=remediation,
            detail={**dict(cause.detail or {}), "tagging": summary},
        ),
    )


def handle(job, item, cfg) -> jobs.Produced:
    """Tag ONE file. The per item worker behind ``tag.folder``.

    The searchers and the general catalogue's seam are looked up on their
    modules at call time (KTD11, R23, R-796), so a test can hand a fake in; a
    detached child gets the live ones (R-226). A file gone since queueing is
    refused ``source-missing``, whose remedy says nothing was read or written,
    never skipped as done. A catalogue nobody could read raises here (R19x):
    this item fails and a retry redoes only it. The configuration is the frozen
    one (KTD9).
    """
    payload = job.payload or {}
    folder = Path(str(payload.get("folder") or ""))
    path = folder / item.item_id
    if not path.is_file():
        raise refuse(
            "source-missing",
            f"{path} is no longer a file, so there is nothing to tag for this "
            f"item. Nothing was read and nothing was written",
            steps=(
                "run the tagging verb again over the folder as it now stands; "
                "this job was queued against a folder that has since changed",
            ),
            origin=("tagging", "cli"),
            detail={"item": item.item_id, "folder": str(folder)},
        )
    declared = active_taxonomy.load(cfg)
    result = tag_engine.tag_one(
        path,
        # The run's refusals in a row, by job and attempt (U281): a new sweep or
        # a resumed run asks a refusing catalogue again from its first file.
        searcher=searchers.for_taxonomy(
            declared, refusals=searchers.for_run(f"{job.job_id}@{job.attempts}")
        ),
        fetch_image=searchers.for_images(),
        published=published.for_taxonomy(declared),
        label_genre=_label_seam(payload),
        label=str(payload.get("label") or "") or None,
        # The folder's label by its identifier (R-1476), apart from a file's tag.
        folder_genre=_folder_seam(payload),
        copyright_labels=_copyright_seam(payload),
    )
    return artifacts.produced(
        cfg,
        job,
        item,
        {
            "item": item.item_id,
            "path": str(result.path),
            "genre_written": result.genre_written,
            "skipped": result.skipped,
            "source": result.source,
            "source_genre": result.source_genre,
            "off_taxonomy": result.off_taxonomy,
            # Every catalogue's answer, not only the disposition (R-791).
            "answers": [
                {
                    "source": said.source,
                    "answer": said.answer,
                    "source_genre": said.source_genre,
                    "note": said.note,
                }
                for said in result.answers
            ],
            "unread": {
                said.source: said.answer
                for said in result.answers
                if said.source in result.unread
            },
            "art_repair": result.art_repair,
            "art_repair_detail": result.art_repair_detail,
            "art_fetch": result.art_fetch,
            "art_fetch_detail": result.art_fetch_detail,
            # The registered label whose genre was written, else empty (U178).
            "label": result.label,
            "label_tag": result.label_tag,
            # How that label was named, and a copyright line's labels when it
            # could not settle the file (U240).
            "label_from": result.label_from,
            "copyright_labels": list(result.copyright_labels),
            # The question the catalogues were asked, and how it was read (U289).
            "asked": {
                "artist": result.asked_artist,
                "title": result.asked_title,
                "read": result.asked_read,
            },
        },
    )
