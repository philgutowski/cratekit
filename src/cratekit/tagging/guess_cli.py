"""``crate tag guess``: a genre for each file in a folder no catalogue tagged (U172).

WHAT IT DOES. Over a folder ``tag folder`` has swept, each audio file that
still carries no genre is given one guessed from the same artist's other
tracks, in the library and in the folder, and, with ``--pass``, from the
playlist on the account the pass downloaded it for. The rules are
:mod:`cratekit.tagging.guess`'s. The tail runs it right after ``tag folder``,
so a sync pass lands those tracks with a genre a tree places them by.

IT WRITES WITHOUT ASKING, Phillip's answer of 2026-11-01: every guess is
written, whatever its band, and a wrong one is put right by hand later. So
this verb declares no gate, as ``tag folder``, which writes the same field on
the same files, declares none. ``--report`` writes nothing and says what a run
would write, which is how a folder that has already landed is measured.

IT NEVER CHANGES A GENRE A FILE CARRIES. Fill if empty, as ``tag folder``.

WHAT IT READS BESIDE THE FOLDER. The library's rows, through a handle opened
to read with ``require_closed`` off, as ``name apply`` reads them, and the
pass's playlist jobs through :func:`cratekit.intake.account_playlists.split`,
the landing's own reading of which playlist asked for which file. Either that
cannot be read is said in a warning and gives no votes, and the guess goes on
with what was read, since the alternative is a pass that stops over a genre it
could still guess from the other signal.

WHAT A PERSON READS. The share of the folder's files carrying a genre before
and after, the guesses by band, every file with its votes, and a warning for
each thing that needs them: the files nothing voted for, the guesses that were
a tie, a file that would not take its genre, and each word on a file the
taxonomy has no place for, with the two things Phillip asked to be offered for
it, an alias of one of his genres or a genre folder of its own.

Layer: modules. It names :mod:`cratekit.cli.output` and nothing else from the
command-line layer, for the reason ``adopt.apply_cli`` gives.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cratekit.cli.output import Envelope, digest_of
from cratekit.core import active_taxonomy, config, rb_writer, taxonomy_word
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import guess, suggest

#: The files that carry no genre and that nothing voted for.
NO_VOTES_LEFT = "tag-guess-no-votes"

#: The guesses written over a tie at the top.
SPLIT_WRITTEN = "tag-guess-split"

#: The files that would not take their guessed genre.
FILES_UNWRITTEN = "tag-guess-unwritten"

#: The files whose genre could not be read, so none was guessed.
FILES_NOT_READ = "tag-guess-file-not-read"

#: The library's rows could not be read, so the artist's library tracks gave no vote.
LIBRARY_UNREAD = "tag-guess-library-unread"

#: The pass's playlist jobs could not be read, so no playlist gave a vote.
PASS_UNREAD = "tag-guess-pass-unread"

#: A word on a file that the taxonomy has no place of its own for (R-650).
OFF_TAXONOMY = "tag-guess-off-taxonomy"

#: How many files a warning's sentence names. The items carry all of them.
_NAMED = 5

_ORIGIN = ("tagging", "guess_cli")


def _load() -> config.Config:
    """Read config, turning a configuration failure into a typed cause."""
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=_ORIGIN,
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def build(parser, entry) -> None:
    """Declare the verb's arguments. ``entry`` is unannotated for KTD23's reason."""
    del entry
    parser.add_argument("folder", help="the folder of audio tag folder has swept")
    parser.add_argument(
        "--pass",
        dest="pass_name",
        default=None,
        metavar="NAME",
        help=(
            "the sync pass the folder's files were downloaded by, so each "
            "playlist on the account that asked for a file votes for its genre"
        ),
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="write nothing, and say what a run would write",
    )
    parser.set_defaults(_handler=tag_guess)


# ---------------------------------------------------------------------------
# What is read beside the folder
# ---------------------------------------------------------------------------


def _library(cfg: config.Config) -> tuple[dict[str, tuple[str, ...]] | None, str]:
    """The library's genres by artist, or None and why it could not be read."""
    try:
        db = rb_writer.open_db(
            rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
        )
    except CratekitError as exc:
        return None, exc.cause.message
    try:
        return guess.library_by_artist(db.get_content()), ""
    except CratekitError as exc:
        return None, exc.cause.message
    finally:
        rb_writer.close_db(db)


def _playlists(
    cfg: config.Config, pass_name: str, staged: tuple[guess.Staged, ...]
) -> tuple[tuple[guess.Playlist, ...], str]:
    """Each playlist of the pass holding a staged file, or nothing and why it was unread."""
    from cratekit.intake import account_playlists, batch_name

    paths = [one.path for one in staged if one.readable]
    try:
        # A PASS NO JOB CARRIES IS NOT A PASS WHOSE PLAYLISTS KNEW NOTHING
        # (review round 1). A mistyped name read as "no playlists" would report
        # every file the playlists could have tagged as one nothing voted for.
        # Only a sync pass is named here: the tail hands a label go's and a
        # Bandcamp batch's guess no pass, since no account playlist asked for
        # them (review round 2).
        if not batch_name.pass_jobs(cfg, pass_name):
            return (), (
                f"no intake job of pass {pass_name} succeeded on this library, so "
                f"the name is not one of its sync passes or the pass never finished"
            )
        claims = account_playlists.split(cfg, pass_name, paths)
    except CratekitError as exc:
        return (), exc.cause.message
    found: list[guess.Playlist] = []
    for claim in claims:
        files = tuple(member.file for member in claim.members if member.file is not None)
        owned: list[guess.Member] = []
        for member in claim.members:
            if member.file is not None:
                continue
            read = next(
                (
                    one
                    for one in (guess.read_member(Path(path)) for path in member.paths)
                    if one is not None
                ),
                None,
            )
            if read is not None:
                owned.append(read)
        if files:
            found.append(guess.Playlist(name=claim.source.name, files=files, owned=tuple(owned)))
    return tuple(found), ""


def signals(
    cfg: config.Config, staged: tuple[guess.Staged, ...], pass_name: str | None
) -> guess.Signals:
    """The library and the pass's playlists, each read or said to be unread.

    Nothing is read when no file needs a genre, so a folder the catalogues
    tagged whole costs no database open and no job read.
    """
    if not any(one.readable and not one.genre for one in staged):
        return guess.Signals(pass_name=pass_name or "")
    library, library_unread = _library(cfg)
    playlists, playlists_unread = ((), "")
    if pass_name:
        playlists, playlists_unread = _playlists(cfg, pass_name, staged)
    return guess.Signals(
        library=library,
        library_unread=library_unread,
        playlists=playlists,
        pass_name=pass_name or "",
        playlists_unread=playlists_unread,
    )


# ---------------------------------------------------------------------------
# What a person reads
# ---------------------------------------------------------------------------


def _named(values: list[str] | tuple[str, ...]) -> str:
    shown = ", ".join(values[:_NAMED])
    more = len(values) - _NAMED
    return f"{shown} and {more} more" if more > 0 else shown


def _payload(found: guess.GuessPlan) -> dict[str, Any]:
    counts = found.counts
    total = len(found.items)
    return {
        "digest": digest_of(found.identity()),
        "items": [item.to_json() for item in found.items],
        "totals": {
            "count": total,
            "outcomes": counts,
            "bands": found.bands(),
            "before": found.before,
            "after": found.after,
            "written": sum(1 for item in found.items if item.written),
            "unread": counts[guess.FILE_UNREADABLE],
            "report": found.report,
            "library_read": found.signals.library is not None,
            "pass": found.signals.pass_name or None,
            "playlists": [one.name for one in found.signals.playlists],
            "off_taxonomy": {word: len(paths) for word, paths in found.off_taxonomy.items()},
        },
        "chunk": None,
    }


def _advisories(found: guess.GuessPlan) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []
    by = {
        name: [item.relative for item in found.items if item.outcome == name]
        for name in guess.OUTCOMES
    }
    if by[guess.NO_VOTES]:
        warnings.append(
            {
                "code": NO_VOTES_LEFT,
                "message": (
                    f"{len(by[guess.NO_VOTES])} file(s) carry no genre and nothing "
                    f"voted for one, no track by the artist and no playlist it came "
                    f"from carrying a genre the taxonomy declares: "
                    f"{_named(by[guess.NO_VOTES])}; they need a genre by hand"
                ),
            }
        )
    split = [item for item in found.guesses if item.band == suggest.SPLIT]
    if split:
        warnings.append(
            {
                "code": SPLIT_WRITTEN,
                "message": (
                    f"{len(split)} guess(es) were a tie at the top, "
                    f"{'would be' if found.report else 'each'} written as the "
                    f"genre the artist's tracks weigh most and then the first by "
                    f"name: "
                    + _named([f"{item.relative} as {item.genre}" for item in split])
                ),
            }
        )
    unwritten = [item for item in found.items if item.outcome == guess.UNWRITTEN]
    if unwritten:
        warnings.append(
            {
                "code": FILES_UNWRITTEN,
                "message": (
                    f"{len(unwritten)} file(s) did not take their guessed genre and "
                    f"carry none: "
                    + _named([f"{item.relative} ({item.note})" for item in unwritten])
                    + "; check each can be written, then run tag guess again"
                ),
            }
        )
    if by[guess.FILE_UNREADABLE]:
        warnings.append(
            {
                "code": FILES_NOT_READ,
                "message": (
                    f"{len(by[guess.FILE_UNREADABLE])} file(s) could not be read, so "
                    f"whether they carry a genre is unknown and none was guessed: "
                    f"{_named(by[guess.FILE_UNREADABLE])}"
                ),
            }
        )
    if found.signals.library_unread:
        warnings.append(
            {
                "code": LIBRARY_UNREAD,
                "message": (
                    f"the library could not be read, so no track of the artist's in "
                    f"it voted: {found.signals.library_unread}"
                ),
            }
        )
    if found.signals.playlists_unread:
        warnings.append(
            {
                "code": PASS_UNREAD,
                "message": (
                    f"the playlists of pass {found.signals.pass_name} could not be "
                    f"read, so no playlist voted: {found.signals.playlists_unread}"
                ),
            }
        )
    if found.off_taxonomy:
        words = [f"{word!r} on {_named(list(paths))}" for word, paths in found.off_taxonomy.items()]
        warnings.append(
            {
                "code": OFF_TAXONOMY,
                "message": (
                    f"{len(found.off_taxonomy)} genre(s) on these files have no place "
                    f"of their own in the taxonomy: {'; '.join(words)}. For each, "
                    f"either save it as an alias of one of your genres and retag "
                    f"its files, with {taxonomy_word.ALIAS_VERB} WORD GENRE, or make "
                    f"it a genre folder of its own, with {taxonomy_word.FOLDER_VERB} WORD"
                ),
            }
        )
    return warnings


def tag_guess(ctx) -> Envelope:
    """Read the folder and what votes for it, guess, write, and report."""
    cfg = _load()
    declared = active_taxonomy.load(cfg)
    root = Path(ctx.args.folder).expanduser().absolute()
    if not root.is_dir():
        raise refuse(
            "source-missing",
            f"{root} is not a folder, so there are no files to guess a genre for",
            steps=("name the folder tag folder swept, then run tag guess again",),
            origin=_ORIGIN,
            detail={"folder": str(root)},
        )
    report = bool(getattr(ctx.args, "report", False))
    staged = guess.read_folder(root)
    found = guess.plan(
        root,
        staged,
        signals(cfg, staged, getattr(ctx.args, "pass_name", None)),
        declared,
        report=report,
    )
    found = guess.write(found)
    data = _payload(found)
    written = data["totals"]["written"]
    return ctx.envelope(
        data=data,
        outcome=Outcome.OK if written else Outcome.NO_OP,
        warnings=_advisories(found),
    )


__all__ = [
    "FILES_NOT_READ",
    "FILES_UNWRITTEN",
    "LIBRARY_UNREAD",
    "NO_VOTES_LEFT",
    "OFF_TAXONOMY",
    "PASS_UNREAD",
    "SPLIT_WRITTEN",
    "build",
    "signals",
    "tag_guess",
]
