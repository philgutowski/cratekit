"""``intake missing --list PATH``: a text list's missing rows, named or offered (U79, R-302).

Every row is resolved against the library first, as ``match run`` resolves it,
so a track held, held in another version or deleted on purpose is never
searched for. A row still missing with no identifier is asked by ISRC, and
otherwise handed to :mod:`cratekit.intake.candidates`, where a search is a
proposal and never a pick. Nothing is ever listed from a fuzzy score.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
import shlex
from collections.abc import Callable, Mapping
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.acquire import listdoc, match, match_cli
from cratekit.cli.output import Envelope
from cratekit.core import review
from cratekit.core.cause import CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import candidates
from cratekit.intake import cli as intake_cli
from cratekit.intake.missing_common import (
    _WORDS,
    _catalogue_once,
    _check,
    _download_command,
    _isrc_check,
    _named_by_isrc,
    _out_dir,
    _summary_head,
    _Unnamed,
    _unusable,
    _written_or_refuse,
    provider_ref,
)

if TYPE_CHECKING:
    from cratekit.label import catalogue

#: What the sidecar says a row named from a list somebody already had came from.
LIST_SOURCE = "list"

#: What follows the input's name in the name of the list ``--list`` writes.
FOUND_SUFFIX = "-found"

#: How many bytes of digest follow that, the width ``label approved`` names its
#: lists with.
DIGEST_BYTES = 6

#: The suffixes an input list's file name may end in, longest first, taken off
#: before the list written from it is named.
_LIST_SUFFIXES = (listdoc.UNLISTED_SUFFIX, listdoc.LIST_SUFFIX, ".json", ".txt")


def found_name(
    path: Path,
    rows: tuple[listdoc.Row, ...] = (),
    provenance: Mapping[str, listdoc.Provenance] | None = None,
) -> str:
    """The name of the list written from the text list at ``path``.

    The input's own name with its list suffix off, ``-found`` after it, and a
    digest of everything the emitter compares: the rows and their provenance,
    which carries the input's full path. ``intake-J.unlisted.json`` writes
    ``intake-J-found-<digest>.list.json`` beside the job's ``intake-J.list.json``
    and never onto it. A character a file name should not carry becomes a
    hyphen, and a name with nothing left is ``tracklist``.

    THE DIGEST IS WHAT LETS THE SECOND RUN HAPPEN. The run after a review answer
    lists more by design, and under a fixed name the emitter refused it. The
    same work still rewrites the same bytes under the same name.
    """
    body, _listed, _unlisted = listdoc.document(rows)
    said = {
        "tracks": body["tracks"],
        "provenance": [
            dataclasses.asdict((provenance or {})[track["id"]]) for track in body["tracks"]
        ],
    }
    encoded = json.dumps(said, ensure_ascii=False, sort_keys=True).encode("utf-8")
    digest = hashlib.blake2s(encoded, digest_size=DIGEST_BYTES).hexdigest()
    stem = path.name
    for suffix in _LIST_SUFFIXES:
        if stem.lower().endswith(suffix) and len(stem) > len(suffix):
            stem = stem[: -len(suffix)]
            break
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-.")
    return f"{stem or 'tracklist'}{FOUND_SUFFIX}-{digest}"


def _searched(
    resolve: Callable[[], catalogue.Catalogue], wanted: list[match.Wanted]
) -> list[candidates.Answer]:
    """One search answer per row, every one in hand before anything is offered.

    The catalogue is resolved only when a row has to be searched for. A provider
    that could not answer refuses the whole verb with nothing offered and no
    file written: a partial pass would report the unasked rows as candidateless.
    """
    if not wanted:
        return []
    found = resolve()
    answers: list[candidates.Answer] = []
    for one in wanted:
        try:
            rows = tuple(found.search_tracks(one.artist, candidates.query_title(one)))
        except CratekitError:
            raise
        except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
            raise refuse(
                "unavailable-transient",
                f"the streaming provider could not answer a search for "
                f"{one.artist} - {one.listed} ({exc}), so the missing tracks cannot "
                f"be sorted into listed and offered; no provider candidate was "
                f"offered and no list was written",
                remedy=Remedy.RETRY_LATER,
                steps=(
                    "run it again later",
                    "if the search for this one row fails on every run, take the "
                    "row out of the list and run it again, so the rest are not "
                    "held back by it",
                ),
                scope=Scope.RUN,
                origin=("intake.missing",),
                detail={"artist": one.artist, "title": one.listed},
            ) from exc
        answers.append(candidates.read_answer(one, rows))
    return answers


def _resolved(ctx, cfg, path: Path, subject: Mapping[str, Any]):
    """The list's counts, its distinct missing rows, and the library view it was read by."""
    wanted = match_cli.read_list(path)
    music = Path(cfg.library.root) / cfg.library.music_dir
    if not music.is_dir():
        # AN ABSENT LIBRARY IS NOT AN EMPTY ONE: every row would resolve missing
        # and be listed for download, held or not.
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no row of "
            f"the list can be told from a track the library already holds",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME,
            origin=("intake.missing",),
            detail={"music": str(music), **subject},
        )
    view = match_cli.library_view(cfg)
    index, suppresses, identify = view
    resolved = match.resolve_all(wanted, index, suppresses=suppresses, suppression_id=identify)
    if any(match_cli.touches_the_queue(one) for one in resolved.matches):
        with review.open_store(cfg) as items:
            resolved = match_cli.adjudicate(
                items,
                resolved,
                handler_key=ctx.entry.handler_key,
                suppresses=suppresses,
                suppression_id=identify,
            )
    counts = {word: 0 for word in _WORDS}
    missing: list[match.Wanted] = []
    seen: set[str] = set()
    for settled in resolved.matches:
        word = match_cli.SETTLED_WORDS.get(settled.state)
        if word is not None:
            counts[word] += 1
        else:
            counts["missing"] += 1
            # THE SAME LINE TWICE IS ONE ROW, on the match identifier.
            if settled.match_id not in seen:
                seen.add(settled.match_id)
                missing.append(settled.wanted)
    return counts, missing, view


def _held_since(proposals: list[candidates.Proposal], named: list[match.Wanted], view) -> None:
    """Add each named proposal's track to ``named``, unless the library holds it now."""
    index, suppresses, identify = view
    for n, one in enumerate(proposals):
        if one.state not in candidates.NAMED or one.track is None:
            continue
        if one.state == candidates.ACCEPTED:
            # AN ACCEPTED CANDIDATE IS ASKED OF THE LIBRARY AS ITSELF. The row it
            # answers stays missing when the candidate is another spelling or
            # version, so every later run would download the same track again.
            now = match.resolve_one(
                one.track, index, suppresses=suppresses, suppression_id=identify
            )
            if now.state in (match.MatchState.MATCHED, match.MatchState.SUPPRESSED):
                proposals[n] = replace(one, state=candidates.HELD)
                continue
        named.append(one.track)


def _missing_for_list(ctx, given: str) -> Envelope:
    """List what a text list's missing rows can be named as, and offer the rest."""
    path = Path(given).expanduser().absolute()
    subject = {"list_in": str(path)}
    cfg = intake_cli._load()
    counts, missing, view = _resolved(ctx, cfg, path, subject)
    named: list[match.Wanted] = []
    by_isrc = 0
    proposals: list[candidates.Proposal] = []
    out: Path | None = None
    if missing:
        # THE FOLDER BEFORE THE PROVIDER, so a bad --out spends no lookup.
        out = _out_dir(ctx, subject)
        # ONLY THE PROVIDER'S OWN IDENTIFIER NAMES A ROW, the emitter's rule: a
        # row carrying another service's id is written with none, so it is bare.
        resolve = _catalogue_once(cfg)
        bare = [one for one in missing if not provider_ref(one)]
        named = [one for one in missing if provider_ref(one)]
        unnamed: list[match.Wanted] = []
        for one, answer in zip(bare, _named_by_isrc(bare, resolve), strict=True):
            if isinstance(answer, _Unnamed):
                unnamed.append(one)
            else:
                # THE ORIGIN WITH THE REF, or the emitter takes the ref off again.
                named.append(replace(one, ref=answer, origin=match.TIDAL))
                by_isrc += 1
        if unnamed:
            # THE QUEUE BEFORE THE PROVIDER, and every answer before any offer: a
            # row already answered or in front of a person spends no search, and
            # a provider failing part way leaves nothing offered.
            with review.open_store(cfg) as items:
                held = [candidates.settled(items, one) for one in unnamed]
            unasked = [one for one, said in zip(unnamed, held, strict=True) if said is None]
            answers = iter(_searched(resolve, unasked))
            with review.open_store(cfg) as items:
                for one, said in zip(unnamed, held, strict=True):
                    proposals.append(
                        said
                        if said is not None
                        else candidates.propose(
                            items, one, next(answers), handler_key=ctx.entry.handler_key
                        )
                    )
    _held_since(proposals, named, view)
    written = listdoc.Written(None, None, (), ())
    if named:
        rows = listdoc.rows_of(named)
        provenance = {
            str(row.ref).strip(): listdoc.Provenance(source=LIST_SOURCE, source_ref=str(path))
            for row in rows
        }
        written = _written_or_refuse(
            out, found_name(path, rows, provenance), rows, provenance, subject
        )
    return _found_report(ctx, path, subject, counts, by_isrc, proposals, written)


def _found_report(ctx, path, subject, counts, by_isrc, proposals, written) -> Envelope:
    """The ``--list`` refusal for nothing routed, then its checks and summary."""
    listed = len(written.listed)

    def of(*states: str) -> list[candidates.Proposal]:
        return [one for one in proposals if one.state in states]

    in_library = of(candidates.HELD)
    by_search = len(of(candidates.LISTED))
    by_review = len(of(candidates.ACCEPTED))
    asked = of(*candidates.ASKED)
    unfound = of(candidates.NO_CANDIDATES, candidates.REJECTED, candidates.STALLED)
    unfound_said = "; ".join(
        f"{one.wanted.artist} - {one.wanted.listed}: {one.reason}" for one in unfound
    )
    if unfound and not listed and not asked:
        # MISSING TRACKS, NOTHING WRITTEN AND NOTHING ASKED IS NOT NOTHING TO DO.
        raise _unusable(
            f"{len(unfound)} missing track(s) and the provider has a route to none of "
            f"them, so nothing was written and nothing is waiting in review: " + unfound_said,
            "find these tracks on the provider by hand, add them to a playlist, "
            "and run intake playlist on it",
            "a rejected or stalled row is asked again after: crate review clear ITEM_ID",
            tracks=[one.to_json() for one in unfound],
            **subject,
        )
    command = _download_command(written)
    again = shlex.join(["crate", "intake", "missing", "--list", str(path)])
    review_command = f"crate review list --queue {candidates.QUEUE} --kind {candidates.KIND}"
    if listed:
        said = f"{listed} missing track(s) written to {written.list_path}; next: {command}"
    elif asked:
        said = (
            f"nothing listed yet: {len(asked)} row(s) are waiting in review; answer "
            f"them, then run: {again}"
        )
    else:
        said = "nothing listed: no track in this list is missing"
    checks = [
        _check("written", "ok" if listed else "info", said),
        _check("owned", "info", f"{counts['owned']} already in the library, not listed"),
        _check(
            "offered",
            "info",
            f"{counts['offered']} held in another version, offered for review and not "
            f"listed until answered; see: crate review list",
        ),
        _check("suppressed", "info", f"{counts['suppressed']} deleted on purpose, not listed"),
        _isrc_check(by_isrc),
        _check(
            "search",
            "info",
            f"{by_search} missing track(s) named by the one exact candidate a provider "
            f"search held, and listed",
        ),
        _check(
            "accepted",
            "info",
            f"{by_review} missing track(s) listed as the candidate accepted in review"
            + (
                f"; {len(in_library)} more accepted candidate(s) are already in the "
                f"library or were deleted on purpose, and are not listed again"
                if in_library
                else ""
            ),
        ),
        _check(
            "candidates",
            "fail" if asked else "ok",
            f"{len(asked)} missing track(s) have provider candidates and no exact one "
            f"to list, so they are offered for review and NOT in the list: "
            + "; ".join(
                f"{one.wanted.artist} - {one.wanted.listed} ({one.item_id})" for one in asked
            )
            + f"; see: {review_command}; then run: {again}"
            if asked
            else "no missing track is waiting on a provider candidate",
        ),
        _check(
            "unfound",
            "fail" if unfound else "ok",
            f"{len(unfound)} missing track(s) have no route to a download and are NOT "
            f"in the list: " + unfound_said
            if unfound
            else "every missing track is listed or waiting in review",
        ),
    ]
    summary = {
        **_summary_head(subject, written, counts),
        "by_isrc": by_isrc,
        "by_search": by_search,
        "by_review": by_review,
        "in_library": len(in_library),
        "candidates_offered": len(asked),
        "unfound": len(unfound),
        "review_next": review_command if asked else None,
        "rows": [one.to_json() for one in proposals],
    }
    return ctx.envelope(
        data={"checks": checks, "summary": summary},
        outcome=Outcome.OK if listed or asked else Outcome.NO_OP,
    )
