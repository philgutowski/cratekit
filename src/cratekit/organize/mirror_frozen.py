"""The account mirror's plan, frozen on the run whose gate showed it (R-1031).

WHY. The account gate is explicit, so the mirror is always planned twice: once
by the run that shows the gate and once by the run that applies after a person
records the answer. Planned from scratch the second time, a first build paid
its matching twice, about two hours of provider requests, and any library write
between the two acts, a landing, a refresh or a split, moved the digest and
refused the approved plan ``decision-stale``.

WHAT IS FROZEN is what the plan read that is not the account: the library, every
folder, playlist and row ``read_library`` returned with each name it refused,
and every match the plan made, ``(account track, ISRC, reason)`` per row. The
run that applies rebuilds the mirror from them and reads the account listing
afresh, so the digest it compares is the plan the person approved as long as
the account did not move, and the provider is asked only about a row the frozen
plan does not carry.

THE SNAPSHOT IS FROZEN WITH THE LIBRARY (U222). The edit rule decides each
mirrored playlist from three readings, the library, the account and the
snapshot the ledger keeps of what both sides last agreed. A library frozen
beside a snapshot read live is two moments, and the rekordbox area's
``mirror-edits`` step settles the snapshot when it takes an account edit into
the library, so an edit taken between the acts read as rekordbox's own change
and planned the edit off the account again (sitting 66). So the snapshot each
recorded playlist had when the gate's plan read it is frozen too, and the run
that applies reads it wherever the playlist is still recorded under the same
remote identifier, with each folder's placements beside it (U236); everything
else of the ledger is read live.

WHAT THE GATE SHOWED IS KEPT TO NAME WHAT MOVED (U222). Each step's digest, and
each playlist's or folder's line inside it, is frozen as the gate showed it, so
a run that applies and finds the area's digest moved names the steps and the
playlists that moved, rather than only saying that something did.

ONE FILE PER RUN, under the library scoped ``mirror_plans`` directory, named
by the run's identifier, which is generated and checked against a plain
pattern before it names a file. A frozen plan older than :data:`KEPT_DAYS` is
pruned when another is written.

ABSENT IS NOT A REFUSAL. A record that is missing, unreadable or of another
version is no plan to rebuild from, and the caller plans afresh and says so; a
fresh plan's digest is still compared with the decision, so the worst it costs
is the second pass this module exists to save.

Layer: modules.
"""

from __future__ import annotations

import json
import re
import time
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config
from cratekit.core.cause import Cause
from cratekit.modules.outbound import ledger, mirror

#: The frozen record's own schema version. 2 since U150, which froze the
#: INBOX folder's retirement and the titles INBOX holds; a version 1 record
#: is planned afresh, never read as a library with no INBOX. 3 since U201,
#: which froze each genre folder's flag and each row's membership time, so a
#: version 2 record is planned afresh rather than read as a tree with no genre.
#: 4 since U204, which names each folder's edit rule rather than a genre flag,
#: so the Favorites folder and INBOX are read as edited by the run that applies.
#: 5 since U214, which froze each node INBOX leaves off, so a version 4 record
#: is planned afresh rather than rebuilt with those lines lost. 6 since U222,
#: which froze each recorded playlist's snapshot and what the gate showed, so a
#: version 5 record is planned afresh rather than rebuilt over a live snapshot.
#: 7 since U236, which froze each mirrored folder's placements with its
#: snapshot, so a version 6 record is planned afresh rather than rebuilt over
#: live placements.
VERSION = 7

#: How long a frozen plan is kept once another is written.
KEPT_DAYS = 7

_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")


@dataclass(frozen=True, slots=True)
class Shown:
    """One step as the gate showed it (U222): its title, digest and each line's digest."""

    title: str
    digest: str
    lines: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Frozen:
    """What a gate's plan read, the library and the matches, to rebuild it from."""

    #: The library, as ``account_mirror.read_library`` returned it.
    library: Any
    matches: Mapping[str, tuple[str, str, str]]
    #: Each recorded playlist's snapshot as the gate's plan read it (U222),
    #: ``folder -> title -> (remote id, agreed or None)``.
    agreed: Mapping[str, Mapping[str, tuple[str, frozenset[str] | None]]] = field(
        default_factory=dict
    )
    #: Each mirrored folder's placements as the gate's plan read them (U236),
    #: ``folder -> title -> tracks``, read with the snapshot they stand beside.
    placed: Mapping[str, Mapping[str, frozenset[str]]] = field(default_factory=dict)
    #: Each step of the area as the gate showed it (U222), by its key.
    steps: Mapping[str, Shown] = field(default_factory=dict)
    #: Whether a gate showed this plan, or a run that applies planned it afresh
    #: because the gate's own could not be read (U222, review round one).
    shown: bool = True


def _path(cfg: config.Config, run_id: str) -> Path | None:
    if not _RUN_ID.match(run_id):
        return None
    return config.state_path("mirror_plans", cfg) / f"{run_id}.json"


def _library_json(library: Any) -> dict[str, Any]:
    return {
        "folders": [
            {
                "name": folder.name,
                "playlists": [
                    {
                        "name": source.name,
                        "rows": [
                            [row.content_id, row.title, row.artist, row.isrc, row.path, row.added]
                            for row in source.rows
                        ],
                    }
                    for source in folder.playlists
                ],
                "retire": folder.retire,
                "present": sorted(folder.present),
                "edits": folder.edits,
                "unmirrored": [list(one) for one in folder.unmirrored],
            }
            for folder in library.folders
        ],
        "refused": {name: cause.to_json() for name, cause in sorted(library.refused.items())},
        "favorites": library.favorites,
        "inbox": library.inbox,
    }


def _library_of(data: Mapping[str, Any]) -> Any:
    from cratekit.organize import account_mirror

    return account_mirror.Library(
        folders=tuple(
            mirror.Folder(
                name=str(folder["name"]),
                playlists=tuple(
                    mirror.Source(
                        name=str(source["name"]),
                        rows=tuple(
                            mirror.Row(
                                content_id=str(cid),
                                title=str(title),
                                artist=str(artist),
                                isrc=str(isrc),
                                path=str(path),
                                added=str(added),
                            )
                            for cid, title, artist, isrc, path, added in source["rows"]
                        ),
                    )
                    for source in folder["playlists"]
                ),
                retire=_flag(folder["retire"]),
                present=_titles(folder["present"]),
                edits=_rule(folder["edits"]),
                unmirrored=_unmirrored(folder["unmirrored"]),
            )
            for folder in data["folders"]
        ),
        refused={str(name): Cause.from_json(cause) for name, cause in data["refused"].items()},
        favorites=str(data["favorites"]),
        inbox=str(data["inbox"]),
    )


def _titles(value: Any) -> frozenset[str]:
    """Frozen titles, refused as unreadable unless a list of text: a string is no list."""
    if not isinstance(value, list) or not all(isinstance(one, str) for one in value):
        raise ValueError(f"a folder's present titles are {value!r}, not a list of text")
    return frozenset(value)


def _unmirrored(value: Any) -> tuple[tuple[str, str], ...]:
    """Frozen unmirrored nodes (U214), refused as unreadable unless pairs of text."""
    if not isinstance(value, list) or not all(
        isinstance(one, list) and len(one) == 2 and all(isinstance(part, str) for part in one)
        for one in value
    ):
        raise ValueError(f"a folder's unmirrored nodes are {value!r}, not pairs of text")
    return tuple((label, reason) for label, reason in value)


def _rule(value: Any) -> str:
    """A frozen folder's edit rule, refused as unreadable unless one this build knows (U204)."""
    from cratekit.modules.outbound import mirror_edits

    if value != "" and value not in mirror_edits.TREES:
        raise ValueError(f"a folder's edit rule is {value!r}, not one of {mirror_edits.TREES}")
    return str(value)


def _flag(value: Any) -> bool:
    """A frozen boolean, refused as unreadable when it is anything else."""
    if not isinstance(value, bool):
        raise ValueError(f"a folder's flag is {value!r}, not true or false")
    return value


def freeze(
    cfg: config.Config,
    run_id: str,
    library: Any,
    matches: Mapping[str, tuple[str, str, str]],
    *,
    recorded: Mapping[str, ledger.MirrorFolder] | None = None,
    steps: Iterable[Any] = (),
    shown: bool = True,
) -> str:
    """Write this run's frozen plan and prune the old ones. Returns what the gate says of it.

    ``recorded`` is the ledger's mirrored folders as the plan READ them, before
    the plan recorded any snapshot of its own, and ``steps`` the area's steps
    as its gate shows them (U222). ``shown`` is false for a plan a run that
    applies made afresh, which no gate showed: it is frozen so the next resume
    asks the provider nothing, and it is never read as what the gate showed.

    Raises ``OSError`` when the directory cannot be written, which the caller
    shows as a fact rather than a refusal: the plan stands, and the run that
    applies plans afresh.
    """
    path = _path(cfg, run_id)
    if path is None:
        return f"not frozen: the run identifier {run_id!r} cannot name a file, so the apply plans again"
    document = {
        "version": VERSION,
        "run_id": run_id,
        "library": _library_json(library),
        "matches": {cid: list(held) for cid, held in sorted(matches.items())},
        "agreed": _agreed_json(recorded or {}),
        "placed": {
            name: {title: sorted(tracks) for title, tracks in sorted(folder.placed.items())}
            for name, folder in sorted((recorded or {}).items())
        },
        "steps": {step.key: _shown_json(step) for step in steps},
        "shown": shown,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    config.atomic_write_bytes(json.dumps(document, sort_keys=True).encode("utf-8") + b"\n", path)
    _prune(path)
    if not shown:
        return (
            f"frozen on run {run_id} as planned now, so a later resume asks the provider "
            f"nothing, though the plan its gate showed is not the one frozen"
        )
    return f"frozen on run {run_id}, so the apply rebuilds it without asking the provider again"


def _agreed_json(recorded: Mapping[str, ledger.MirrorFolder]) -> dict[str, Any]:
    return {
        name: {
            title: [one.remote_id, None if one.agreed is None else sorted(one.agreed)]
            for title, one in sorted(folder.playlists.items())
        }
        for name, folder in sorted(recorded.items())
    }


def _label(item: Mapping[str, Any]) -> str:
    """What a gate line is named by: its playlist, else its folder, else nothing."""
    for key in ("playlist", "folder"):
        value = item.get(key)
        if isinstance(value, str) and value:
            return value
    return ""


def _lines(step: Any) -> dict[str, str]:
    """Each named line of a step as the gate shows it, by its name, digested."""
    named: dict[str, list[Any]] = {}
    for item in step.items:
        label = _label(item)
        if label:
            named.setdefault(label, []).append(item)
    return {label: digest_of(items) for label, items in sorted(named.items())}


def _shown_json(step: Any) -> dict[str, Any]:
    return {"title": step.title, "digest": digest_of(step.identity()), "lines": _lines(step)}


def _prune(kept: Path) -> None:
    cutoff = time.time() - KEPT_DAYS * 86400
    for one in kept.parent.glob("*.json"):
        if one == kept:
            continue
        try:
            if one.stat().st_mtime < cutoff:
                one.unlink()
        except OSError:
            continue


def load(cfg: config.Config, run_id: str) -> tuple[Frozen | None, str]:
    """This run's frozen plan, or ``None`` and why there is none to rebuild from."""
    path = _path(cfg, run_id)
    if path is None:
        return None, f"the run identifier {run_id!r} names no frozen plan"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, f"run {run_id} holds no frozen mirror plan"
    except (OSError, ValueError) as exc:
        return None, f"the frozen mirror plan of run {run_id} could not be read ({exc})"
    try:
        if data.get("version") != VERSION or data.get("run_id") != run_id:
            raise ValueError(f"it says version {data.get('version')!r} of run {data.get('run_id')!r}")
        library = _library_of(data["library"])
        matches = {
            str(cid): (str(remote), str(isrc), str(reason))
            for cid, (remote, isrc, reason) in data["matches"].items()
        }
        agreed = _agreed_of(data["agreed"])
        placed = _placed_of(data["placed"])
        steps = _steps_of(data["steps"])
        shown = data["shown"]
        if not isinstance(shown, bool):
            raise ValueError(f"whether a gate showed it is {shown!r}, not true or false")
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        return None, f"the frozen mirror plan of run {run_id} is not one this build reads ({exc})"
    return (
        Frozen(
            library=library, matches=matches, agreed=agreed, placed=placed, steps=steps, shown=shown
        ),
        "",
    )


def _text(value: Any, what: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{what} is {value!r}, not text")
    return value


def _agreed_of(data: Any) -> dict[str, dict[str, tuple[str, frozenset[str] | None]]]:
    """The frozen snapshots, refused as unreadable unless each is a remote id and a list or null."""
    found: dict[str, dict[str, tuple[str, frozenset[str] | None]]] = {}
    for name, playlists in data.items():
        found[_text(name, "a snapshot's folder")] = held = {}
        for title, (remote_id, agreed) in playlists.items():
            if agreed is not None and (
                not isinstance(agreed, list) or not all(isinstance(one, str) for one in agreed)
            ):
                raise ValueError(f"the snapshot of {title!r} is {agreed!r}, not a list of text")
            held[_text(title, "a snapshot's title")] = (
                _text(remote_id, f"the remote id of {title!r}"),
                None if agreed is None else frozenset(agreed),
            )
    return found


def _placed_of(data: Any) -> dict[str, dict[str, frozenset[str]]]:
    """The frozen placements (U236), refused as unreadable unless each is a list of text."""
    found: dict[str, dict[str, frozenset[str]]] = {}
    for name, titles in data.items():
        found[_text(name, "a placement's folder")] = held = {}
        for title, tracks in titles.items():
            if not isinstance(tracks, list) or not all(isinstance(one, str) for one in tracks):
                raise ValueError(f"the placements on {title!r} are {tracks!r}, not a list of text")
            held[_text(title, "a placement's title")] = frozenset(tracks)
    return found


def _steps_of(data: Any) -> dict[str, Shown]:
    """The steps the gate showed, refused as unreadable unless each carries text."""
    found: dict[str, Shown] = {}
    for key, shown in data.items():
        lines = shown["lines"]
        found[_text(key, "a step's key")] = Shown(
            title=_text(shown["title"], f"the title of step {key!r}"),
            digest=_text(shown["digest"], f"the digest of step {key!r}"),
            lines={
                _text(label, "a line's name"): _text(digest, f"the digest of line {label!r}")
                for label, digest in lines.items()
            },
        )
    return found


def overlay(
    recorded: Mapping[str, ledger.MirrorFolder], frozen: Frozen
) -> dict[str, ledger.MirrorFolder]:
    """The ledger's mirrored folders read now, each snapshot as the gate's plan read it (U222).

    ONLY A PLAYLIST STILL RECORDED UNDER THE SAME REMOTE IDENTIFIER takes the
    frozen snapshot: one made again on the account between the acts is another
    playlist, and keeps the snapshot recorded for it now. Every other field,
    and every playlist the gate's plan did not read, is the ledger's now.

    A FOLDER'S PLACEMENTS ARE THE GATE'S TOO (U236), whole, for every folder
    the gate's plan read, since the library step that settles a snapshot
    between the acts records and drops them in the same write.
    """
    folders: dict[str, ledger.MirrorFolder] = {}
    for name, folder in recorded.items():
        then = frozen.agreed.get(name, {})
        playlists = {}
        for title, one in folder.playlists.items():
            held = then.get(title)
            if held is not None and held[0] == one.remote_id:
                one = replace(one, agreed=held[1])
            playlists[title] = one
        folders[name] = replace(
            folder, playlists=playlists, placed=frozen.placed.get(name, folder.placed)
        )
    return folders


def moved(steps: Iterable[Any], frozen: Frozen) -> list[str]:
    """Each step whose plan is not the one the gate showed, one line each (U222).

    A step the gate did not show, or one it showed that this run did not plan,
    is a line too. Inside a step that moved, the playlists and folders whose
    line moved are named; an empty answer means every step plans as shown.
    """
    said: list[str] = []
    now = {step.key: step for step in steps}
    for key, step in now.items():
        then = frozen.steps.get(key)
        if then is None:
            said.append(f"{step.title}, which the gate did not show")
            continue
        if digest_of(step.identity()) == then.digest:
            continue
        lines = _lines(step)
        # A STEP WITH NO LINES ON ONE SIDE, refused now or at the gate, is
        # named alone: every line of the other side would read as moved.
        named = (
            sorted(
                label
                for label in set(lines) | set(then.lines)
                if lines.get(label) != then.lines.get(label)
            )
            if lines and then.lines
            else []
        )
        said.append(
            step.title
            + (", in " + ", ".join(repr(label) for label in named) if named else "")
        )
    for key, then in frozen.steps.items():
        if key not in now:
            said.append(f"{then.title}, which the gate showed and this run did not plan")
    return said


__all__ = ["KEPT_DAYS", "VERSION", "Frozen", "Shown", "freeze", "load", "moved", "overlay"]
