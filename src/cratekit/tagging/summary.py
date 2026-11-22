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

#: The three ways a file can leave a sweep (U240): its genre written from its
#: registered label, from a catalogue, or not at all.
WAY_LABEL = "label"
WAY_CATALOGUE = "catalogue"
WAY_NONE = "none"
WAYS: tuple[str, ...] = (WAY_LABEL, WAY_CATALOGUE, WAY_NONE)


def _summary(
    cfg: config.Config, job_id: str, causes: Mapping[str, Cause | None] | None = None
) -> dict:
    """What this job's committed artifacts say happened to the folder.

    Read back from what ran, so a resumed sweep counts every file. A closed set
    this build declares is zero filled (skip reasons, art statuses, every
    source's answers, ``tagged_by``, ``ways``), so a zero reads as a zero; a
    word a catalogue chose or a label a person named is not (``unresolved``,
    ``off_taxonomy``, ``label_genres``, ``label_tags``), each key one a person
    can act on (R24). ``off_taxonomy`` is written and still in ``tagged``,
    keyed on the source string the alias would be written against (R-650).
    ``challenged`` and ``not_sent`` count within ``blocked`` (U281); the
    general catalogue's answers add ``no-isrc`` (R-796). ``files`` lists each
    file by item with its way (U240), and ``causes`` puts a failed item that
    kept no report there too, with its reason (U240's review).
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
            # A refusal by what refused and whether it was sent (U281), off the
            # note words the searcher wrote.
            source = str(said.get("source") or "")
            if word == searchers.Answer.BLOCKED.value and source in challenged:
                note = str(said.get("note") or "")
                if searchers.CLOUDFLARE_CHALLENGE in note:
                    challenged[source] += 1
                if note.startswith(searchers.NOT_SENT):
                    not_sent[source] += 1
            # A file searched only for its picture was owed no genre (U244's
            # and U282's reviews).
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
            # A refused token on every file, owed a genre or not (U282's
            # review): this count is the only place the refusal reaches.
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

    No genre written, Discogs asked and answered, and every other catalogue
    sent the file refused this client; an outage or parse break beside a
    refusal is not one.
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

    None when there are none. ``catalogues`` carries the date each began
    refusing, off :mod:`cratekit.tagging.refused`.
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

    Says which catalogues refused and since when, and, when Discogs went
    unasked, that a token lets a sweep carry on. None when none failed so.
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
        # NOT FOR A TOKEN DISCOGS REFUSED (round one): waiting mends nothing.
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
    # NOT DEDUPLICATED: two labels may share a display name (U240's review).
    names = sorted(str(name) for name in named if name)
    if len(names) > 1:
        key = ", ".join(names)
        ambiguous[key] = ambiguous.get(key, 0) + 1


def _way(report: Mapping, reason: str) -> str:
    """The way one reported file left the sweep, by label, by catalogue or not at all.

    Tagged only where :func:`_summary` counts it so: written, under no skip reason.
    """
    if reason in tag_engine.SKIP_REASONS or not report.get("genre_written"):
        return WAY_NONE
    if str(report.get("source") or "") == tag_engine.LABEL_GENRE:
        return WAY_LABEL
    return WAY_CATALOGUE


def _files(count: int) -> str:
    """``1 file was`` or ``N files were``, the head of a sentence about files."""
    return "1 file was" if count == 1 else f"{count} files were"
