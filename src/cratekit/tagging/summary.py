"""What one tagging sweep's committed reports say happened to its folder.

:func:`_summary` reads every report back, so a resumed sweep counts every
file, and the warnings ``cratekit.tagging.cli`` raises are built off the one
dictionary it returns.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Mapping

from cratekit.core import art, config
from cratekit.core.cause import Cause
from cratekit.tagging import artifacts, published, refused, searchers
from cratekit.tagging import tag as tag_engine

#: The three ways a file can leave a sweep, as the per file report says (U240):
#: its genre written from its registered label, written from a catalogue, or
#: not written at all, whether it already had one, nothing answered, or its
#: item failed before a report was kept.
WAY_LABEL = "label"
WAY_CATALOGUE = "catalogue"
WAY_NONE = "none"
WAYS: tuple[str, ...] = (WAY_LABEL, WAY_CATALOGUE, WAY_NONE)


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
    discogs_refused = 0
    refused_files: list[str] = []
    refusing: dict[str, None] = {}
    for report in artifacts.committed(cfg, job_id):
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
        shut_out = _refused_out(report, reason)
        if shut_out:
            refused_files.append(str(report.get("item") or ""))
            refusing.update(dict.fromkeys(shut_out))
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
            # owed to, so it is not counted (U244's review): it already has one,
            # its own or its label's (U282's review).
            owed = (
                reason != tag_engine.HAS_GENRE
                and str(report.get("source") or "") != tag_engine.LABEL_GENRE
            )
            if (
                owed
                and said.get("source") == searchers.DISCOGS
                and word == searchers.NOT_ASKED
                and said.get("note") in searchers.DISCOGS_UNASKED_NOTES
            ):
                discogs_without_token += 1
            # A REFUSED TOKEN IS COUNTED ON EVERY FILE IT CAME UP ON, owed a
            # genre or not (U282's review): the walk goes on to Beatport past
            # it, so this count is the only place the refusal reaches.
            if (
                said.get("source") == searchers.DISCOGS
                and word == searchers.NOT_ASKED
                and str(said.get("note") or "").startswith(searchers.DISCOGS_TOKEN_REFUSED)
            ):
                discogs_refused += 1
    reported = {row["item"] for row in files}
    stopped: dict[str, Cause] = {}
    for item_id, cause in (causes or {}).items():
        if item_id in reported:
            continue
        if cause is not None and isinstance((cause.detail or {}).get(searchers.REFUSED_DETAIL), dict):
            stopped[item_id] = cause
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
        "discogs_token_refused": discogs_refused,
        "art_repair": art_repair,
        "art_fetch": art_fetch,
        "refused": _refused_report(refused_files, tuple(refusing)),
        "refusal_stop": _refusal_stop(stopped),
    }


def _refused_out(report: Mapping, reason: str) -> tuple[str, ...]:
    """The record shops that refused a file Discogs read and could not tag, or none (U284).

    THE FILE OPTION 3 CARRIES ON PAST: no genre written, Discogs ASKED AND
    ANSWERED (a miss, or a match whose styles name no folder), and every other
    catalogue of the walk that was sent the file refused this client. A file
    Discogs was not asked about never reaches here settled, since its refusal
    by every catalogue asked fails the item. An outage or a parse break beside
    a refusal is not a refusal: such a file is unread for another reason and is
    not named under this one.
    """
    if reason not in (tag_engine.SOURCES_UNREAD, tag_engine.UNMAPPED_GENRE):
        return ()
    said = {
        str(entry.get("source") or ""): str(entry.get("answer") or "")
        for entry in report.get("answers") or ()
        if isinstance(entry, dict)
    }
    if said.get(searchers.DISCOGS) not in (searchers.Answer.MISS.value, searchers.Answer.MATCHED.value):
        return ()
    others = [
        source
        for source in searchers.SOURCES
        if source != searchers.DISCOGS and source in said and said[source] != searchers.NOT_ASKED
    ]
    if not others or any(said[source] != searchers.Answer.BLOCKED.value for source in others):
        return ()
    return tuple(others)


def _refused_report(files: list[str], catalogues: tuple[str, ...]) -> dict | None:
    """The files a sweep settled untagged because every other catalogue refused, said once.

    None when there are none, so a reader tells "nothing refused" from an empty
    list it must interpret. ``catalogues`` carries the date each began refusing,
    off :mod:`cratekit.tagging.refused`, empty where none is recorded.
    """
    if not files:
        return None
    since = refused.since(catalogues)
    named = sorted(files)
    return {
        "files": named,
        "catalogues": since,
        "said": (
            f"{_files(len(named))} left with no genre because Discogs searched "
            f"and could not tag them while every other catalogue refused this "
            f"client ({searchers.refusing_since(since)}): {', '.join(named)}. "
            f"None is recorded no-hit; tag retag or tag suggest asks the "
            f"catalogues again"
        ),
    }


#: Why Discogs was not read for a file every catalogue asked refused, in words.
_DISCOGS_UNREAD_WORDS = {
    searchers.DISCOGS_NO_TOKEN: "no Discogs token is recorded",
    searchers.DISCOGS_TOKEN_LOST: (
        "a Discogs token is recorded and the keychain no longer holds it"
    ),
    searchers.DISCOGS_TOKEN_REFUSED: "Discogs refused the recorded token",
}


def _refusal_stop(stopped: Mapping[str, Cause]) -> dict | None:
    """The files whose item failed because every catalogue asked refused, said once (U284).

    THE STOP PHILLIP'S OPTION 3 KEEPS. With no token, or Discogs refusing too,
    a file every catalogue refused fails as before; what changes is that the
    sweep, and the pass that ran it, say which catalogues refused and since
    when, and, when Discogs went unasked, that recording a token lets a sweep
    carry on. None when no item failed that way.
    """
    if not stopped:
        return None
    since: dict[str, str] = {}
    unasked = ""
    for cause in stopped.values():
        detail = cause.detail or {}
        for source, began in dict(detail.get(searchers.REFUSED_DETAIL) or {}).items():
            if not since.get(str(source)):
                since[str(source)] = str(began or "")
        unasked = unasked or str(detail.get(searchers.DISCOGS_DETAIL) or "")
    named = sorted(stopped)
    said = (
        f"{_files(len(named))} failed because every catalogue asked refused this "
        f"client ({searchers.refusing_since(since)}): {', '.join(named)}"
    )
    steps = []
    if unasked:
        why = _DISCOGS_UNREAD_WORDS.get(unasked, unasked)
        said += (
            f". Discogs was not read, since {why}; recording a working token with "
            f"crate login discogs-token lets a sweep carry on past the refusing "
            f"catalogues, leaving a file Discogs searched and could not tag "
            f"untagged and askable, and a sync pass or a label go lands it under "
            f"needs genre"
        )
        steps.append(
            f"{searchers.DISCOGS_LOGIN_STEPS}, then run the pass or the sweep again"
        )
    else:
        said += (
            ". Carrying on past refusing catalogues needs Discogs to have read the "
            "file, so nothing is landed until a catalogue answers this client"
        )
    if unasked != searchers.DISCOGS_TOKEN_REFUSED:
        # NOT FOR A TOKEN DISCOGS REFUSED (round one): those files failed for
        # good, and waiting mends nothing until a working token is recorded.
        steps.append(
            "run the pass or the sweep again later; the job resumes at the files it stopped on"
        )
    return {
        "files": named,
        "catalogues": since,
        "discogs": unasked,
        "said": said,
        "steps": steps,
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


def _files(count: int) -> str:
    """``1 file was`` or ``N files were``, the head of a sentence about files."""
    return "1 file was" if count == 1 else f"{count} files were"
