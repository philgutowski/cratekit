"""``crate tag folder``: queue genre tagging over a folder, and drive it.

WHAT THIS VERB DOES, AND WHY THAT IS QUEUEING RATHER THAN TAGGING. Every file in
a download folder is one or more questions asked of a public record catalogue,
paced so the catalogue keeps answering, so a folder of two hundred files is long
work by any definition. Conformance 5 says long work is queued rather than run
inline, for the reason the source system taught: a sweep that runs inline has no
record, no resume, and no way to answer "what is it doing" from anywhere but the
terminal it was started in. So this verb freezes the folder and the configuration
the run will use (KTD9), queues one job with one item per audio file, and reports
the job. :func:`handle` at the foot of this module is the worker behind it.

RUN BY HAND IT DRIVES THAT JOB BEFORE IT RETURNS (U192). The queue is still the
record and the resume, but a person typing the verb wants the folder tagged, so
the queue path runs the ``--job`` path on the job it just queued, through
:func:`cratekit.modules.foreground.settle`. ``--queue-only`` keeps the queue
and return answer for a caller that drives the job itself.

THE ITEMS ARE THE ENGINE'S OWN WALK, and that is KTD7 rather than a convenience.
:func:`cratekit.tagging.tag.audio_files` is what the engine tags one file per, so
it is what this shell queues one item per. A shell that walked the folder itself
would be a second opinion about which files the job covers, and the drift runs in
the expensive direction: a job reporting done over files it never queued.

THE IDENTIFIERS ARE RELATIVE TO THE FOLDER, so the frozen payload holds the only
absolute path and an item stays short enough to read in a job listing. Nothing
builds a filename out of one, because
:func:`cratekit.tagging.artifacts.final_path` names a report after the item's
ORDINAL, which is what makes an arbitrary identifier safe there.

THE LABEL GENRES ARE FROZEN TOO (U178). Every registered label that carries a
genre is written into the job's payload when it is queued, with the verb's
``--label``, so a resume tags by what was registered when the sweep was asked
for, as KTD9 freezes the configuration. A job queued before labels carried a
genre has none frozen and is tagged exactly as it always was.

SO ARE THE NEEDLES, BESIDE THE GENRES (U240). Every registered label's
``--match`` needle, or its name, is frozen with them, and a file with no label
tag in a sweep given no ``--label`` is matched to the registry by its
copyright line through :func:`copyright_matcher`. That is what lets one call
tag a folder of several labels, the label go's tail among them, with every
catalogue blocked. A job queued before U240 froze no needles, and its files
are tagged as they always were.

THE FOLDER IS FROZEN ABSOLUTE. A resume is a fresh process that
``cratekit.cli.jobs`` spawns, and a relative folder would resolve against
whatever directory that process happens to start in, which is a sweep of some
other folder wearing this job's identifier.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import replace
from pathlib import Path

from cratekit.cli.output import Envelope
from cratekit.core import active_taxonomy, art, config, jobs, taxonomy, taxonomy_word
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.label import harvest as label_harvest
from cratekit.label import registry as labels
from cratekit.label import verify as label_verify
from cratekit.modules import foreground
from cratekit.tagging import artifacts, published, searchers, shell

# THE ENGINE IS ALIASED because this module already defines ``tag_folder`` and
# that function is the VERB, while :mod:`cratekit.tagging.tag` defines a
# ``tag_folder`` that is the ENGINE. One symbol meaning two things in one file is
# the defect ``docs/METHOD.md`` says to hunt, and this unit is where the shell
# imports the engine for the first time. ``adopt/scan_cli.py`` aliased its own
# engine import for exactly this shape, and U51 aliased three modules called
# ``export``.
from cratekit.tagging import tag as tag_engine

#: The warning a sweep carries when some of what it tagged is a word the declared
#: taxonomy does not know. A WARNING CODE AND NOT A CAUSE, on the rule the three
#: no-op codes in this module already follow: the verb succeeded, the files were
#: written, and a catalogue using a word this template has never declared is a
#: fact about the template rather than a reason anything did not happen.
OFF_TAXONOMY = "tag-folder-off-taxonomy"

#: The warning a sweep carries when some files were left untagged because a
#: catalogue went unread for them, rather than because none carried them
#: (R-791): it could not be read, or since U244 it was not asked for want of a
#: token. A warning and not a cause, on the same rule: the sweep did what it
#: could and the files are askable again on the next run.
SOURCES_UNREAD = "tag-folder-sources-unread"

#: The warning that names a catalogue which refused this machine with a bot
#: check or a block page on every file it was asked about. Apart from the count
#: above because the next move differs: a whole catalogue contributed nothing to
#: the run, which a person needs to know before they trust any decline in it.
SOURCE_BLOCKED = "tag-folder-source-blocked"

#: The warning that names the general catalogue when it could not be read on
#: files it was asked about, blocked, unreachable or unparsable (R-796). One
#: code for all three because the consequence is one: those files got no
#: published genre, and their declines were made without that catalogue. It
#: says whether that was every file asked about or some of them.
PUBLISHED_UNREAD = "tag-folder-published-unread"

#: The warning that counts the files the general catalogue could not be asked
#: about because they carry no ISRC (R-796). Apart from the unread count
#: because another run will not move it: the file needs its ISRC, or a genre by
#: hand. Named apart from the engine's ``NO_ISRC``, which is the skip reason
#: and the answer word, so one name does not mean two strings in two modules.
NO_ISRC_FILES = "tag-folder-no-isrc"

#: The warning that counts the files Discogs was not asked about because no
#: Discogs token is recorded, or the keychain no longer holds the one that is
#: (U244). Apart from the unread count because the remedy is one command, and
#: a person who never recorded a token needs to hear that Discogs exists.
DISCOGS_NO_TOKEN_FILES = "tag-folder-discogs-no-token"


#: The warning a sweep queued with ``--label`` carries when that label is
#: registered with no genre (U178). Its files are searched as they always were,
#: which is a correct sweep, so this is a warning and not a refusal; it says so
#: because a person who named the label expected none of them to be searched.
LABEL_NO_GENRE = "tag-folder-label-no-genre"

#: The warning a sweep carries when the label registry could not be read as it
#: was queued (U178). The sweep goes on as it did before labels carried a
#: genre, and says that no label's genre was applied, rather than reading an
#: unreadable registry as one holding no genres.
LABEL_REGISTRY_UNREAD = "tag-folder-label-registry-unread"


#: The warning a sweep queued with ``--label`` carries when some of its files
#: carry a label tag naming no label with a genre (U178). The file's own tag
#: outranks ``--label``, so those files were asked of the catalogues, and a
#: person who named the folder's label is told which tags kept it from them.
LABEL_TAG_OUTRANKED = "tag-folder-label-tag-outranked"

#: The warning a resume carries when it is given ``--label`` (U178). The label
#: a sweep tags by is frozen when it is queued, so the one typed on a resume is
#: not applied, and saying so is cheaper than letting a person believe it was.
LABEL_ON_RESUME = "tag-folder-label-on-resume"

#: The warning a sweep carries when some files' copyright line named more than
#: one registered label (U240). Those files were asked of the catalogues rather
#: than given either label's genre, and the warning names the labels so a
#: person can give a file still without a genre its label tag by hand.
COPYRIGHT_AMBIGUOUS = "tag-folder-copyright-ambiguous"

#: The three ways a file can leave a sweep, as the per file report says (U240):
#: its genre written from its registered label, written from a catalogue, or
#: not written at all, whether it already had one, nothing answered, or its
#: item failed before a report was kept.
WAY_LABEL = "label"
WAY_CATALOGUE = "catalogue"
WAY_NONE = "none"
WAYS: tuple[str, ...] = (WAY_LABEL, WAY_CATALOGUE, WAY_NONE)


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause.

    The remedy token is carried straight through from the configuration error
    that raised it, so "no config at all" and "config written by a newer build"
    keep their different answers all the way to the CLI.
    """
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("tagging.cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry) -> None:
    """Declare the verb's arguments. The parameters are unannotated on purpose.

    ``entry`` is a ``cratekit.cli.registry.Entry`` and naming that type here
    would be this modules-ranked file importing the layer above it (KTD23).
    """
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
    """The command line that continues one queued sweep.

    THE CONTRACT EVERY LONG-RUNNING VERB OWES: the payload is frozen at queue
    time (KTD9), so only the verb that queued it knows how to turn it back into
    an invocation. It names the JOB as well as the folder, which is what stops a
    resume from queueing a second record for one piece of work.
    """
    folder = job.payload.get("folder", "")
    return ["tag", "folder", folder, "--job", job.job_id]


def _summary(
    cfg: config.Config, job_id: str, causes: Mapping[str, Cause | None] | None = None
) -> dict:
    """What this job's committed artifacts say happened to the folder.

    DERIVED FROM WHAT RAN, never from what was queued. A sweep that tagged three
    files of five and is continued tomorrow has five reports on disk and the
    person asking what happened means all five, which is why this reads the
    artifacts back rather than accumulating counts in memory.

    ZEROES INCLUDED for the skip reasons, on the rule
    :func:`cratekit.adopt.scan.categories` states: a summary listing only the
    reasons it happened to see makes "nothing here was already tagged" and "this
    build does not count that" the same output.

    THE UNRESOLVED STRINGS ARE NOT ZERO FILLED, and that is the opposite rule
    rather than an inconsistency. The skip reasons are a closed set this build
    declares, so their absence is a fact worth stating; a source genre is a word
    a catalogue chose, so there is no set to fill and every key present is one a
    person can go and add an alias for (R24).

    ``off_taxonomy`` IS THE THIRD DISPOSITION AND IS COUNTED APART FROM BOTH. A
    file whose genre came from the catalogue's own word was written, so it is
    still in ``tagged``, and it is not a clean tag, so its string is listed here
    the way a decline's is listed in ``unresolved``. The two maps are never
    merged: a decline left the file askable and this one is already on disk,
    which are different jobs for the person reading them. Same not zero filled
    rule, for the same reason, and keyed on the SOURCE string rather than the
    written one, because the alias a person would add is written against what
    the catalogue said (R-650).

    ``art_repair`` COUNTS EVERY STATUS THE REPAIR CAN REPORT, zero filled on the
    first rule, because it is a closed set this build declares. A report
    committed before the repair existed carries no status and is counted under
    none of them, since which status it would have had is not known.
    ``art_fetch`` is the same rule over new art, so ``unavailable`` stands next
    to ``embedded`` as a count a person can see was zero.

    ``answers`` COUNTS FILES BY WHAT EACH CATALOGUE ANSWERED, zero filled over
    every source and every answer, so "Bandcamp was blocked on all 66" and
    "Bandcamp matched none of 66" are two different lines rather than one silence
    (R-791). A report committed before the answers were recorded counts under
    none of them, for the art repair's reason.

    ``challenged`` AND ``not_sent`` COUNT A RECORD SHOP'S REFUSALS TWO MORE
    WAYS (U281), zero filled over every source: the ``blocked`` answers whose
    note names a Cloudflare challenge, and those the catalogue was never sent
    because it had already refused this client in the run, read off the
    searcher's own :data:`cratekit.tagging.searchers.NOT_SENT` head. Both are
    counted within ``blocked``, never apart from it.

    THE GENERAL CATALOGUE IS COUNTED BESIDE THE THREE, over its own answers
    (R-796). Its set is the record shops' and ``no-isrc``, the one answer only a
    catalogue asked by ISRC can give, so the three do not gain a count that can
    never be anything but zero.

    ``tagged_by`` COUNTS THE FILES WRITTEN PER SOURCE, zero filled, so how many
    genres the general catalogue supplied is a number in the summary rather
    than a subtraction. A file tagged by a searcher that names no source, or by
    one this build does not declare, is in ``tagged`` and in none of these.

    ``label_genres`` COUNTS THE FILES EACH REGISTERED LABEL TAGGED (U178), and
    ``tagged_by`` carries them under :data:`cratekit.tagging.tag.LABEL_GENRE`,
    zero filled, so a label genre is counted apart from every catalogue's and
    never as an off taxonomy word. ``label_tags`` counts the files whose own
    label tag named no label with a genre, by the tag's text, so a spelling the
    registry does not know is a line a person can act on. The labels are not zero filled, on the
    unresolved strings' rule: they are names a person registered, not a set
    this build declares.

    ``ways`` COUNTS EVERY FILE BY THE WAY IT LEFT THE SWEEP (U240), zero
    filled over :data:`WAYS`, and ``files`` lists each one, sorted by item,
    with its way, the label whose genre it took, how that label was named, and
    the reason its item failed. Derived from fields every report has carried
    since U178, so a report committed before U240 is still placed, with no
    ``named_by``. ``causes`` holds every item of the job with its cause, so a
    file whose item failed, and so kept no report, is listed as tagged not at
    all with its reason rather than left out (U240's review).
    ``copyright_ambiguous`` counts the files whose copyright line named more
    than one registered label, keyed by the labels it named, read off a failed
    file's cause when it kept no report.
    """
    skipped = dict.fromkeys(tag_engine.SKIP_REASONS, 0)
    answer_values = (*(answer.value for answer in searchers.Answer), searchers.NOT_ASKED)
    answers = {source: dict.fromkeys(answer_values, 0) for source in searchers.SOURCES}
    answers[published.SOURCE] = dict.fromkeys(published.ANSWERS, 0)
    challenged = dict.fromkeys(searchers.SOURCES, 0)
    not_sent = dict.fromkeys(searchers.SOURCES, 0)
    tagged_by = dict.fromkeys(answers, 0)
    tagged_by[tag_engine.LABEL_GENRE] = 0
    label_genres: dict[str, int] = {}
    label_tags: dict[str, int] = {}
    ways = dict.fromkeys(WAYS, 0)
    files: list[dict[str, str]] = []
    ambiguous: dict[str, int] = {}
    art_repair = dict.fromkeys(art.REPAIR_STATUSES, 0)
    art_fetch = dict.fromkeys(tag_engine.ART_FETCH_STATUSES, 0)
    unresolved: dict[str, int] = {}
    off_taxonomy: dict[str, int] = {}
    tagged = 0
    discogs_without_token = 0
    for report in artifacts.committed(cfg, job_id):
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
        if reason in skipped:
            skipped[reason] += 1
        elif report.get("genre_written"):
            tagged += 1
            wrote = str(report.get("source") or "")
            if wrote in tagged_by:
                tagged_by[wrote] += 1
            if wrote == tag_engine.LABEL_GENRE:
                named = str(report.get("label") or "")
                label_genres[named] = label_genres.get(named, 0) + 1
            if report.get("off_taxonomy") and source_genre:
                off_taxonomy[source_genre] = off_taxonomy.get(source_genre, 0) + 1
        own = str(report.get("label_tag") or "")
        if own:
            label_tags[own] = label_tags.get(own, 0) + 1
        way = _way(report, reason)
        ways[way] += 1
        by_label = way == WAY_LABEL
        files.append(
            {
                "item": str(report.get("item") or ""),
                "way": way,
                "label": str(report.get("label") or "") if by_label else "",
                "named_by": str(report.get("label_from") or "") if by_label else "",
                "failed": "",
            }
        )
        _count_ambiguous(ambiguous, report.get("copyright_labels"))
        if reason == tag_engine.UNMAPPED_GENRE and source_genre:
            unresolved[source_genre] = unresolved.get(source_genre, 0) + 1
        status = str(report.get("art_repair") or "")
        if status in art_repair:
            art_repair[status] += 1
        fetched = str(report.get("art_fetch") or "")
        if fetched in art_fetch:
            art_fetch[fetched] += 1
        for said in report.get("answers") or ():
            if not isinstance(said, dict):
                continue
            counted = answers.get(str(said.get("source") or ""))
            word = str(said.get("answer") or "")
            if counted is not None and word in counted:
                counted[word] += 1
            # A REFUSAL IS COUNTED BY WHAT REFUSED AND WHETHER IT WAS SENT
            # (U281), off the note words the searcher wrote it with, so the
            # warning names a Cloudflare challenge and the files a catalogue
            # was not asked about after it refused this client.
            source = str(said.get("source") or "")
            if word == searchers.Answer.BLOCKED.value and source in challenged:
                note = str(said.get("note") or "")
                if searchers.CLOUDFLARE_CHALLENGE in note:
                    challenged[source] += 1
                if note.startswith(searchers.NOT_SENT):
                    not_sent[source] += 1
            # A FILE SEARCHED ONLY FOR ITS PICTURE is not one Discogs' genre was
            # owed to, so it is not counted (U244's review): it already has one.
            if (
                reason != tag_engine.HAS_GENRE
                and said.get("source") == searchers.DISCOGS
                and word == searchers.NOT_ASKED
                and said.get("note") in searchers.DISCOGS_UNASKED_NOTES
            ):
                discogs_without_token += 1
    reported = {row["item"] for row in files}
    for item_id, cause in (causes or {}).items():
        if item_id in reported:
            continue
        ways[WAY_NONE] += 1
        files.append(
            {
                "item": item_id,
                "way": WAY_NONE,
                "label": "",
                "named_by": "",
                "failed": cause.reason if cause is not None else "",
            }
        )
        if cause is not None:
            _count_ambiguous(ambiguous, (cause.detail or {}).get(tag_engine.COPYRIGHT_LABELS_DETAIL))
    return {
        "tagged": tagged,
        "tagged_by": tagged_by,
        "label_genres": label_genres,
        "label_tags": label_tags,
        "ways": ways,
        "files": sorted(files, key=lambda row: row["item"]),
        "copyright_ambiguous": ambiguous,
        "skipped": skipped,
        "unresolved": unresolved,
        "off_taxonomy": off_taxonomy,
        "answers": answers,
        "challenged": challenged,
        "not_sent": not_sent,
        "discogs_without_token": discogs_without_token,
        "art_repair": art_repair,
        "art_fetch": art_fetch,
    }


def _count_ambiguous(ambiguous: dict[str, int], named: object) -> None:
    """Count one file under the labels its copyright line named, when it named two or more."""
    if not isinstance(named, (list, tuple)):
        return
    # NOT DEDUPLICATED: two labels may share a display name after a rename, and
    # a line naming both is still two labels (U240's review, round two).
    names = sorted(str(name) for name in named if name)
    if len(names) > 1:
        key = ", ".join(names)
        ambiguous[key] = ambiguous.get(key, 0) + 1


def _way(report: Mapping, reason: str) -> str:
    """The way one reported file left the sweep, by label, by catalogue or not at all.

    A file counts as tagged only where :func:`_summary` counts it so: written,
    and not under a skip reason. Its source decides which of the two.
    """
    if reason in tag_engine.SKIP_REASONS or not report.get("genre_written"):
        return WAY_NONE
    if str(report.get("source") or "") == tag_engine.LABEL_GENRE:
        return WAY_LABEL
    return WAY_CATALOGUE


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

    THE COUNT IS THE FIX FOR THE CLEAN NO-HIT (R-791). Without it a sweep whose
    fallbacks were all refused reads, on the surface a person reads, exactly as
    one whose fallbacks were all asked and had nothing.

    A CATALOGUE IS NAMED WHEN IT WAS BLOCKED ON EVERY FILE IT WAS ASKED ABOUT,
    and at least one. A file whose search ended at a Beatport match never asked
    the fallbacks, so "every file" is every file the catalogue was sent, not every
    file in the folder; counting the others would let a run where Beatport
    matched half the folder hide a fallback that was refused on the other half.
    In the walk's own source order, so two runs over one folder warn alike.

    THE COUNT NAMES WHAT WENT UNREAD, per source and per answer, because the
    three unread answers send a person to three places. A parse break is said to
    be a defect a rerun will not move, so it is never filed under the promise
    that the next run asks again and left there.

    THE GENERAL CATALOGUE IS IN THAT COUNT AND NOWHERE ELSE HERE (R-796). It is
    one of the catalogues a file can be left unread by, so the sentence about
    the files names it. Its parse break sentence and its refusal belong to
    :func:`_published_warnings`, so each is said once.
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
        # A CATALOGUE NOBODY ASKED IS IN THE TALLY TOO (U244's review), or a
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
    # THE RECORD SHOPS ONLY, Discogs among them. The general catalogue's refusal is said by
    # its own warning, over every unread answer rather than only this one, and
    # naming it under this code as well would say one fact in two wordings.
    for source in searchers.SOURCES:
        counted = answers.get(source) or {}
        # SENT, NOT ONLY ANSWERED (U281): a file answered from the run's memory
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

    ``beatport unreachable on 3`` for an outage, and for a refusal ``beatport
    refused this client (Cloudflare challenge) on 190, 187 of them not asked
    once it had refused this client``: a refusal read as ``unreachable`` sent a
    person to their network over a block no network check moves. The challenge
    is named when every refusal counted was one, and counted when some were.
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

    THOSE FILES ARE NOT NO-HIT. Each rides ``sources-unread`` unless another
    catalogue settled it, and the next run asks again; this says what would let
    it ask Discogs, once, however many files it was.
    """
    count = int(summary.get("discogs_without_token") or 0)
    if not count:
        return ()
    return (
        {
            "code": DISCOGS_NO_TOKEN_FILES,
            "message": (
                f"Discogs was not asked about {count} file(s) because no Discogs "
                f"token is recorded, or the keychain no longer holds the recorded "
                f"one; those files were not reported as no-hit. To ask it: "
                f"{searchers.DISCOGS_LOGIN_STEPS}"
            ),
        },
    )


def _files(count: int) -> str:
    """``1 file was`` or ``N files were``, the head of a sentence about files."""
    return "1 file was" if count == 1 else f"{count} files were"


def _published_warnings(summary: dict) -> tuple[dict[str, str], ...]:
    """Say when the general catalogue went unread, and count the no ISRC files.

    ANY FILE IT WAS ASKED ABOUT AND COULD NOT BE READ FOR is said, with how many
    of the files it was asked about that is. Asked means it answered something
    about the track or failed to: a match, a miss, or one of the three unread
    answers. ``not-asked`` and ``no-isrc`` are files it was never sent, so a run
    where Beatport settled most of the folder cannot hide a catalogue that was
    refused on the rest. One warning for a block, an outage and a parse break,
    with the count of each, because the person's first question is the same for
    all three: did these files have this catalogue at all. Unread on EVERY file
    it was asked about is said in those words, since then no file in the run
    got a published genre.

    NOT ONLY WHEN SOME FILE IS ``sources-unread``. A file a record shop gave a
    catch-all for is ``unmapped-genre`` whatever this catalogue did, so a block
    on exactly those files would otherwise show in the counts and in no
    sentence.

    THE NO ISRC COUNT IS ITS OWN WARNING, whatever skip reason those files
    carry. On a machine whose fallbacks are blocked every such file is
    ``sources-unread``, which promises that another run asks again, and for
    these files another run asks the general catalogue nothing.
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
    """The library's taxonomy for a warning's wording, or None when it cannot be read.

    A report is never refused for a sentence: an unreadable copy keeps the
    warning as it was, and doctor and every routing verb name the copy.
    """
    try:
        return active_taxonomy.load(cfg)
    except CratekitError:
        return None


def _off_taxonomy_warning(
    summary: dict, declared: taxonomy.Taxonomy | None = None
) -> tuple[dict[str, str], ...]:
    """Say out loud that some of what was tagged is outside the declared table.

    THE PAYLOAD ALONE IS NOT THE FIX, which is the product decision inside this
    unit. R-650's cost is that a person is TOLD the folder tagged cleanly, and a
    count nobody reads leaves that sentence in place on the surface they do read.
    The warning names the strings, so the next move, adding an alias or leaving
    the word alone, is one a person can make without opening the artifacts.

    IT DOES NOT MAKE THE VERB FAIL, and that is deliberate. The files ARE tagged,
    the sweep is unattended by design, and turning a new genre into a failure
    would stop the very acquisition run this tier exists to let through. A
    warning on a success is the shape this module already uses for a no-op it
    wants seen.

    SORTED, because the order artifacts are committed in is the order files were
    walked, and a warning whose text changes between two runs over one unchanged
    folder is one nobody can diff.

    IT SAYS NOTHING ABOUT WHERE THE TRACKS LANDED, and the first draft did. It
    told the person these words route to the fallback bucket, which is the
    ledger entry's own second cost and is FALSE for a measured class: driven on
    2026-09-21, ``Psy-Trance`` and ``Hardcore / Hard Techno`` are both off
    taxonomy and both routed by a fuzzy rule to a real bucket, while ``gqom``
    and ``Leftfield Bass`` landed in the catch-all. The two tiers read two
    different rule lists, so one cannot be read off the other. Telling somebody
    their correctly filed tracks are in the wrong folder is the same defect this
    warning exists to fix, one turn further on, so this says only the part that
    is true of every word it names. Which of them also landed in the catch-all
    is recorded as a residual rather than guessed at here.

    A GENRE FOLDER'S OWN NAME IN ANOTHER CASE TAKES ONE ANSWER ONLY (R-1184),
    so when the library's taxonomy could be read the warning names each such
    word with it. When it could not, the warning says what it said before.
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

    THE HONEST ZERO, and it is a different thing from a job with no items. A
    folder holding no audio is a correct outcome and a common one;
    ``core.jobs`` reports a job with no items as SUCCEEDED by design, so a verb
    that queued one here would report a clean tagging sweep over a folder
    nothing walked. Nothing is queued and the envelope says which zero this is.

    THE PAYLOAD SHAPE IS :func:`cratekit.tagging.shell.no_op`'s rather than this
    module's, so the zero paths the two tagging verbs have cannot reintroduce
    R-234's null ``job_id`` separately.
    """
    return shell.no_op("no-op"), ({"code": reason, "message": detail},)


def tag_folder(ctx) -> Envelope:
    """Queue one tagging sweep over a folder and drive it, or drive it on a resume.

    The handler key comes off the entry rather than being spelled again here, so
    the job the queue holds and the verb the registry declares cannot name two
    different things.

    THERE ARE THREE ZEROES AND THEY ARE THREE WARNINGS, because the person's
    next move differs for each: put some music in the folder, fix what they
    typed, or name a folder at all. The engine's walk answers empty for all
    three, which is correct for a walk and is exactly why they are told apart up
    here.

    THE UNNAMED FOLDER IS THE ONE THAT MATTERS. An empty string is a valid
    argument to a positional that takes one, so the parser accepts it, and
    ``Path("")`` is the CURRENT DIRECTORY. This verb writes to files, so
    resolving it would sweep whatever the person happens to be standing in.
    ``tag.retag`` refuses the same argument under ``tag-retag-folder-unknown``
    rather than defaulting, for that reason and no other. This zero is the same
    protection at the strength this unit can reach: a refusal needs a slug of its
    own in ``cause.REASONS``, and reusing the correction verb's would put that
    verb's name on this one's failure. Recorded as a residual.
    """
    cfg = _load()
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
            # ONE AUDIO FILE IS ONE ITEM, relative to the frozen folder. Without
            # them the queue holds a job with nothing to claim and the driver
            # reports an empty success over a sweep it never took.
            item_ids=tuple(str(path.relative_to(folder)) for path in files),
            cfg=cfg,
        )
        if foreground.queue_only(ctx.args):
            return ctx.envelope(data=shell.reported(store, job), warnings=label_warnings)
    # DRIVEN HERE THROUGH THE RESUME, U192. The ``--label`` this call typed is
    # the one the sweep froze, so the resume is told none was typed on it, and
    # the queue's own label warnings lead the settled envelope.
    return foreground.settle(
        job.job_id,
        lambda: _resume(ctx, cfg, job.job_id, typed_label=None, queued=label_warnings),
        argv=tag_argv(job),
        origin="tagging.cli",
    )


def _label_payload(label: str | None) -> tuple[dict, tuple[dict[str, str], ...]]:
    """What a sweep freezes about labels, and what it warns about them (U178).

    THE GENRES OF EVERY REGISTERED LABEL THAT CARRIES ONE, keyed by identifier,
    and the ``--label`` resolved to its registered name and its identifier,
    which is what the sweep answers it by (R-1476). Both are left out of
    the payload when there is nothing to freeze, so a sweep with no label
    genres is queued exactly as it was before them.

    ``--label`` NAMING NO REGISTERED LABEL IS REFUSED, before anything is
    queued: a typo would otherwise tag the whole folder from the catalogues
    while the person believed it was tagged by the label. One registered with
    no genre is accepted with a warning, since its sweep is a correct one.

    A REGISTRY THAT CANNOT BE READ refuses a sweep given ``--label``, which asked
    for it by name, and warns on one that did not, which goes on as every sweep
    did before labels carried a genre.
    """
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
        # EVERY LABEL'S NEEDLE, WITH A GENRE OR WITHOUT (U240), so a copyright
        # line naming a label with a genre and one without is two names and
        # settles neither. Frozen only beside genres: with none, the line could
        # tag nothing, and the payload stays the one it always was.
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
        # THE IDENTIFIER IS WHAT THE SWEEP ANSWERS BY (R-1476). Two labels can
        # share a display name after a rename, and a name looked up again among
        # the labels carrying a genre found the other one and wrote its genre.
        frozen["label_id"] = entry.label_id
        if not entry.genre:
            # THE REMEDY NAMES THE LABEL BY ITS IDENTIFIER, since ``registry
            # set`` resolves an identifier first: given the name, it would set a
            # label sharing it, or one whose identifier it is (R-1476's review).
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

    THE TAGS ARE NAMED ONLY FOR A SWEEP QUEUED WITH ``--label``. Without one, a
    label tag naming no registered genre is an ordinary file tagged as it always
    was; with one, the person said what the folder is, and the files their own
    tag kept from it are the ones they would otherwise find untagged later.
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

    THE LABELS WITH A GENRE AND, from the needles U240 freezes beside them,
    those without, joined by identifier (R-1476). Holding the labels with no
    genre is what keeps a lookup from landing on another label: a name a label
    with none holds is that label's, and answers nothing. A job queued before
    U240 froze only the labels with a genre, and is read among them as before.
    """
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
    try:
        return labels.slug(name) if name.strip() else ""
    except CratekitError:
        return ""


def _label_seam(payload: Mapping) -> tag_engine.LabelGenre | None:
    """The engine's label seam for a file's own label tag, or None for no genres.

    A TAG IS READ AS A NAME FIRST (R-1476). It names the frozen labels whose
    display name it is, in any case; failing any, those whose display name has
    its slug, so ``Liebe*Detail`` still names ``Liebe Detail``; and only when no
    label's name is it, the label whose identifier is its slug, the one first
    registered under it and since renamed. A tag equal to one label's
    identifier and another's name named the wrong one when the identifier came
    first. The label found answers with its own genre or with nothing.

    A NAME TWO LABELS HOLD NAMES NEITHER, and the file is asked of the
    catalogues, as U240 counts two labels sharing a name on a copyright line.

    A name that could never be a label, punctuation only, is an unknown label
    here and not a failed item, because it came off a file's tag and the file
    is then searched as before.
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
            # NO LABEL'S NAME IS THIS ONE: the label first registered under it,
            # since renamed, whose identifier is the name's slug.
            named = tuple(entry for entry in (held.labels.get(wanted),) if entry is not None)
        return _answered(named[0]) if len(named) == 1 else None

    return answer


def _folder_seam(payload: Mapping) -> tag_engine.LabelGenre | None:
    """The engine's seam for the sweep's ``--label``, by its frozen identifier, or None.

    THE FOLDER'S LABEL IS EXACT (R-1476): ``--label`` was resolved against the
    live registry when the sweep was queued, and its identifier frozen, so it
    is answered by that label's own genre and never looked up again by a name
    another label may share. None for a sweep queued before the identifier
    was frozen, whose ``--label`` the engine then reads as a name.
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

    THE LINE IS READ AS THE LABEL VERBS READ ONE, its mark and year stripped by
    :func:`labels_from_copyright`, and it MUST CARRY THE WHOLE NEEDLE, as whole
    words after :func:`credit_names` folds both, which is U237's rule taken one
    way: ``Rawax`` names ``Rawax Records`` and never
    ``RAWAXXX``, and a line reading only ``Music`` never names ``Aus Music``.
    The other way, a short line inside a long needle, is a heuristic the label
    sweep may confirm a release on and never one to write a genre on.

    THE MOST SPECIFIC NEEDLE WINS when one carries every other one named: a
    line reading ``Rawax Motor City Edition`` names the sublabel registered
    under that needle, not also its parent ``Rawax``. Two needles neither of
    which carries the other, ``Cronos Barac under exclusive licence to
    Atipic``, are both answered, and the engine settles neither.

    Each label is answered with its own genre, so nothing is looked up by a
    display name two labels could share.
    """
    rows = tuple(
        (str(name), str(needle), str(genre) if genre else None)
        for name, needle, genre in labels
        if name and needle
    )

    def answer(line: str) -> tuple[tag_engine.CopyrightLabel, ...]:
        # THE MARK AND THE YEAR GO FIRST, as every label verb reads a line, so a
        # label named ``2020 Vision`` is never named by ``℗ 2020 Vision Quest``
        # (U240's review, round two).
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

    THE NEEDLES AND THE GENRES ARE JOINED BY THE LABEL'S IDENTIFIER, never by
    its display name, which two labels can share after a rename (U240's
    review). A job queued before U240 froze no needles, and its files are
    tagged as before.
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

    ``typed_label`` is the ``--label`` typed on a ``--job`` command, which a
    resume does not apply and says so; None from the queue path, whose label
    is the one frozen. ``queued`` is the queue's own warnings, leading the
    settled envelope when the sweep is driven at its queue (U192).

    EVERY RULE OF THE RESUME LIVES IN :func:`cratekit.tagging.shell.advance`,
    which reconciles a claim left by a driver that died, refuses a job carrying
    no items, drives, and raises rather than reporting when the job closed
    carrying a cause. That last one is R-225: a person whose folder was half
    tagged must not be handed a normal envelope the dispatcher exits 0 over.
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
        # ONE SUMMARY, READ ONCE. The warning is derived from the same dictionary
        # the payload carries, so the count a person is warned about and the
        # count they can go and read cannot disagree.
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

    A SWEEP WITH ONE FILE NO CATALOGUE COULD READ ENDS IN A REFUSAL (R-225), and
    before U240's review that refusal said nothing of the files the sweep did
    tag, so a label batch with one unsettled file showed no per file report at
    all. The refusal keeps its type and its words through
    :func:`cratekit.core.cause.rebuilt`, gains one sentence counting every file
    by label, by catalogue or not at all, and the sentence naming lines that
    named two labels, and carries the summary in its detail under ``tagging``.
    A refusal raised before the job ended, a held driver or an empty job, is
    passed through untouched.
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
    return rebuilt(
        error,
        replace(
            cause,
            message=f"{head}{'' if head.endswith(('.', '!', '?')) else '.'} {said}",
            detail={**dict(cause.detail or {}), "tagging": summary},
        ),
    )


def handle(job, item, cfg) -> jobs.Produced:
    """Tag ONE file. The per item worker behind ``tag.folder``.

    THE SEARCHER IS LOOKED UP RATHER THAN CONSTRUCTED (KTD11, R23).
    ``ItemHandler`` is a fixed three argument callable, so a worker that built
    its own searcher inline would leave a test nowhere to hand a fake in and
    R18's no network proof unwritable. The lookup happens at CALL TIME, on the
    module rather than on a name imported from it, which is what makes the
    substitution reach this line. R-226 records the honest limit: the child
    ``crate job resume`` spawns is a fresh process and inherits nothing patched
    in another one, so a detached run always gets the live searcher.

    THE FOLDER IS FROZEN AND THE FILES IN IT ARE NOT. A file deleted between the
    queueing and the drive is refused with its own slug rather than skipped, on
    the rule ``adopt/scan_cli.handle`` states: an item that reported done having
    tagged nothing is the clean-report-over-unreadable-state cost
    ``docs/METHOD.md`` names. ``source-missing`` rather than a slug of this
    verb's own, because its reserved remediation is "nothing was read and
    nothing was written", which is exactly what this refusal promises, and
    because ``adopt-item-absent`` and ``outbound-item-absent`` each name the
    frozen SOURCE they were derived from rather than a file on disk.

    A CATALOGUE NOBODY COULD READ RAISES OUT OF HERE, and that is R19x working
    rather than a gap. :func:`cratekit.tagging.searchers.catalogue_searcher`
    declines when a source answered and had nothing, and refuses only when none
    of them answered at all, so this item fails, the rest of the folder is
    unaffected, and a retry redoes exactly the one that failed.

    THE GENERAL CATALOGUE'S SEAM IS LOOKED UP THE SAME WAY (R-796), off
    :mod:`cratekit.tagging.published` at call time, and the engine decides when
    it is consulted. This worker only hands it over.

    THE CONFIGURATION IS THE FROZEN ONE AND IS NOT LOADED HERE. KTD9 closes the
    recorded resume bug where a queued run re-resolved its configuration; a
    handler that loaded one is that defect wearing a new hat.
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
        # THE RUN'S REFUSALS IN A ROW, found by the run's identity (U281): the
        # job and the drive's attempt, so a catalogue that refused this run
        # three times in a row is not asked by its later files, and a new
        # sweep or a resumed run asks it again from its first file.
        searcher=searchers.for_taxonomy(
            declared, refusals=searchers.for_run(f"{job.job_id}@{job.attempts}")
        ),
        fetch_image=searchers.for_images(),
        published=published.for_taxonomy(declared),
        label_genre=_label_seam(payload),
        label=str(payload.get("label") or "") or None,
        # THE FOLDER'S LABEL BY ITS IDENTIFIER (R-1476), answered apart from
        # any file's tag; None for a sweep queued before the identifier was.
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
            # EVERY CATALOGUE'S ANSWER, so a later reader can tell what each one
            # said rather than only the disposition they added up to (R-791).
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
            # THE REGISTERED LABEL WHOSE GENRE WAS WRITTEN, empty for every
            # other file (U178).
            "label": result.label,
            "label_tag": result.label_tag,
            # HOW THAT LABEL WAS NAMED, and the labels a copyright line named
            # when it could not settle the file (U240).
            "label_from": result.label_from,
            "copyright_labels": list(result.copyright_labels),
        },
    )
