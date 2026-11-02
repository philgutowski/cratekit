"""``crate taxonomy alias`` and ``crate taxonomy folder``: a genre word answered in one command (U194).

WHAT THEY ANSWER. ``tag folder`` and ``tag guess`` name each word a catalogue
gave a file that the library's taxonomy has no place of its own for, offering
two answers: save it as an alias of one of your genres and retag its files, or
make it a genre folder of its own. Each is one of these verbs.

- ``taxonomy alias WORD GENRE`` adds the word to the tagging aliases of the
  genre folder GENRE names, so a catalogue giving it again is tagged as that
  genre, and rewrites the genre of every audio file under the library root
  (or ``--folder``) whose one genre is the word, in any case, to that genre.
  The rows follow by ``tag rows``, which a run that wrote names.
- ``taxonomy folder WORD`` adds a top level genre folder named the word, with
  energy bands, so the files already wearing it route there with nothing
  rewritten. ``route resort`` files them, which the run names.

THE ORDER IS THE UPGRADE'S (U132): plan, the explicit gate over the digested
plan, the plan taken again and refused as stale when its digest moved, the
copy as it was kept under a dated name, the new copy written atomically and
read back through the loader, and put back when it does not read back. The
alias's files are written after the copy, each read again before its write
and read back after, so a run that stops part way has saved the alias and
the next run, which plans no change to the copy, finishes the files.

THE DIGEST COVERS THE TWO TEXTS AND THE ITEMS, and each file by its path
under the folder walked, never the folder itself, so a rehearsal on a
disposable copy matches the live plan.

Layer: cli.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.cli import gates, output, registry
from cratekit.cli.output import Envelope
from cratekit.cli.verbs import taxonomy as upgrade_cli
from cratekit.core import active_taxonomy, config, tags, taxonomy, taxonomy_upgrade
from cratekit.core import taxonomy_word as word_edit
from cratekit.core.cause import Outcome, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.tagging.tag import audio_files

if TYPE_CHECKING:  # pragma: no cover
    from cratekit.cli import Context

#: The two gates, explicit: the copy is the declaration every verb routes by.
ALIAS_GATE = "taxonomy.alias.apply"
FOLDER_GATE = "taxonomy.folder.apply"

#: The notes the verbs carry on their warnings channel.
ALIAS_SAVED = "taxonomy-alias-saved"
FILES_RETAGGED = "taxonomy-alias-retagged"
FILES_LEFT = "taxonomy-alias-left-alone"
FILES_NOT_READ = "taxonomy-alias-file-not-read"
NOTHING_TO_DO = "taxonomy-alias-nothing-to-do"
FOLDER_MADE = "taxonomy-folder-made"
FOLDER_ALREADY = "taxonomy-folder-already-declared"

#: What a file of the alias's plan is, as its item says.
WRITE = "write"
LEFT = "left"
UNREAD = "unread"

#: Why a file carrying the word is left: it carries another genre too.
SEVERAL_GENRES = "several-genres"

#: The verbs a run that wrote names, for the rows and for the tree.
ROWS_FOLLOW = "crate tag rows"
TREE_FOLLOWS = "crate route resort"

#: How many files a sentence names. The items carry every one.
_NAMED = 5

#: How several genre values on one file are shown as one string.
_JOINED = " | "

_ORIGIN = ("cli", "verbs", "taxonomy_word")


# ---------------------------------------------------------------------------
# Arguments
# ---------------------------------------------------------------------------


def build_alias(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    del entry
    parser.add_argument("word", help="the genre word the taxonomy has no place for, as the files carry it")
    parser.add_argument("genre", help="the genre folder it means, by its name or its id")
    parser.add_argument(
        "--folder",
        default=None,
        metavar="FOLDER",
        help="retag only the files under this folder, rather than every file under the library root",
    )
    parser.set_defaults(_handler=taxonomy_alias_verb)


def build_folder(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    del entry
    parser.add_argument("word", help="the genre word to make a genre folder of its own, as the files carry it")
    parser.add_argument(
        "--like",
        default=None,
        metavar="GENRE",
        help=(
            "the genre folder whose family, tempo window and rating it takes; by "
            "default the one the word's tracks are filed in now"
        ),
    )
    parser.set_defaults(_handler=taxonomy_folder_verb)


def _gate(entry: registry.Entry, name: str) -> registry.GateSpec:
    for spec in entry.gates:
        if spec.name == name:
            return spec
    raise RuntimeError(f"registry entry {entry.name!r} declares no gate {name!r}")


# ---------------------------------------------------------------------------
# The plan of an answer
# ---------------------------------------------------------------------------


def _refused(exc: word_edit.Refused, word: str) -> Exception:
    """A refusal of the word or the genre, before anything is written."""
    if exc.why == word_edit.NO_SUCH_GENRE:
        reason, steps = "taxonomy-genre-unknown", ("name a genre folder the taxonomy declares",)
    elif exc.why in (word_edit.NOT_EDITABLE, word_edit.WOULD_NOT_LOAD):
        reason, steps = "config-unusable", ("make the edit by hand, as the message says",)
    else:
        reason, steps = "taxonomy-word-refused", ()
    return refuse(
        reason,
        f"{exc}; nothing was written",
        steps=steps,
        origin=_ORIGIN,
        detail={"word": word, "why": exc.why, "problems": list(exc.problems)},
    )


def _edit(cfg: config.Config, plan_it) -> tuple[Path, word_edit.Edit]:
    """The copy's path and the planned edit, refusing a copy that does not load or an answer that cannot be written."""
    path, text = active_taxonomy.read_text(cfg)
    if text is None:
        raise refuse(
            "config-unusable",
            f"this library has no active taxonomy copy at {path}, so there is nothing to "
            f"answer the word in; setup makes one",
            remedy=Remedy.RUN_SETUP,
            origin=_ORIGIN,
            detail={"path": str(path)},
        )
    try:
        return path, plan_it(text)
    except taxonomy.TaxonomyError as exc:
        raise refuse(
            "config-unusable",
            f"the active taxonomy copy at {path} is not usable: {exc}; it is repaired by "
            f"hand before a word can be answered in it",
            remedy=Remedy.FIX_CONFIG_VALUES,
            origin=_ORIGIN,
            detail={"path": str(path)},
        ) from exc


@dataclass(frozen=True, slots=True)
class FileItem:
    """One audio file carrying the word: written, left, or not read."""

    path: Path
    relative: str
    change: str
    current: str = ""
    reason: str = ""

    def to_json(self, wanted: str) -> dict[str, str]:
        out = {"kind": "file", "path": self.relative, "change": self.change, "current": self.current}
        if self.change == WRITE:
            out["wanted"] = wanted
        if self.reason:
            out["reason"] = self.reason
        return out


@dataclass(frozen=True, slots=True)
class Files:
    """Every audio file under the folder walked that carries the word, by what happens to it."""

    root: Path
    items: tuple[FileItem, ...] = ()
    read: int = 0

    def of(self, change: str) -> tuple[FileItem, ...]:
        return tuple(item for item in self.items if item.change == change)


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _genres(path: Path) -> tuple[str, ...] | None:
    """Every genre value the file holds, or None when it could not be read.

    The exact reader, so a failed read is never taken for a blank one.
    """
    try:
        values = tags.read_tag_values_checked(path, "genre") or ()
    except (tags.TagReadFailed, OSError):
        return None
    return tuple(word for word in (value.strip() for value in values) if word)


def carrying(root: Path, word: str, display: str) -> Files:
    """The files under ``root`` whose genre is ``word``, in any case.

    ONE GENRE AND ONLY THE WORD is a file to write. A file carrying the word
    beside another genre is left and listed, since which of the two a person
    meant is not this verb's to say. A file whose genre could not be read is
    listed as not read, because absence of the word is not what was learned.
    A file already carrying ``display`` is not listed: it is answered.
    """
    folded = word.casefold()
    items: list[FileItem] = []
    read = 0
    for path in audio_files(root):
        relative = _relative(path, root)
        values = _genres(path)
        if values is None:
            items.append(FileItem(path=path, relative=relative, change=UNREAD))
            continue
        read += 1
        if not any(value.casefold() == folded for value in values):
            continue
        current = _JOINED.join(values)
        if len(values) == 1:
            if values[0] != display:
                items.append(FileItem(path=path, relative=relative, change=WRITE, current=current))
            continue
        items.append(FileItem(path=path, relative=relative, change=LEFT, current=current, reason=SEVERAL_GENRES))
    return Files(root=root, items=tuple(items), read=read)


def _alias_payload(edit: word_edit.Edit, files: Files) -> dict[str, Any]:
    listed: list[dict[str, Any]] = []
    if edit.writes:
        listed.append(
            {"kind": "tag_alias", "bucket": edit.bucket_id, "word": edit.word.lower(), "change": "add"}
        )
    listed += [item.to_json(edit.display) for item in files.items]
    return {
        "digest": output.digest_of(
            {
                "before": taxonomy.template_digest(edit.before),
                "after": taxonomy.template_digest(edit.after),
                "items": listed,
            }
        ),
        "items": listed,
        "totals": {
            "word": edit.word,
            "bucket": edit.bucket_id,
            "genre": edit.display,
            "alias_added": edit.writes,
            "files_read": files.read,
            "write": len(files.of(WRITE)),
            "left": len(files.of(LEFT)),
            "unread": len(files.of(UNREAD)),
        },
        "chunk": None,
    }


def _named(items: tuple[FileItem, ...]) -> str:
    shown = ", ".join(item.relative for item in items[:_NAMED])
    more = len(items) - _NAMED
    return shown + (f" and {more} more" if more > 0 else "")


def _file_notes(files: Files) -> list[dict[str, str]]:
    notes = []
    left = files.of(LEFT)
    if left:
        notes.append(
            {
                "code": FILES_LEFT,
                "message": (
                    f"{len(left)} file(s) carry the word beside another genre and were "
                    f"left as they are: {_named(left)}"
                ),
            }
        )
    unread = files.of(UNREAD)
    if unread:
        notes.append(
            {
                "code": FILES_NOT_READ,
                "message": (
                    f"{len(unread)} audio file(s) under {files.root} could not be read, so "
                    f"whether they carry the word is not known: {_named(unread)}"
                ),
            }
        )
    return notes


def _root(cfg: config.Config, folder: str | None) -> Path:
    root = Path(folder).expanduser().absolute() if folder else Path(cfg.library.root)
    if not root.is_dir():
        raise refuse(
            "source-missing",
            f"{root} is not a folder, so there are no files to retag; nothing was written",
            steps=("name a folder of the library's audio, or leave --folder out",),
            origin=_ORIGIN,
            detail={"folder": str(root)},
        )
    return root


# ---------------------------------------------------------------------------
# The alias
# ---------------------------------------------------------------------------


@dataclass
class _Written:
    written: list[FileItem] = field(default_factory=list)
    moved: list[FileItem] = field(default_factory=list)
    failed: list[FileItem] = field(default_factory=list)
    wrong: list[FileItem] = field(default_factory=list)


def _retag(items: tuple[FileItem, ...], display: str) -> _Written:
    """Write ``display`` onto each file, read again before and read back after.

    A file that no longer carries what the plan read is left and named, a file
    the writer could not write is untouched and named, and one written that
    does not read back is named apart from both. Nothing here raises for one
    file, so one that cannot be written does not stop the rest.
    """
    done = _Written()
    for item in items:
        if _genres(item.path) != (item.current,):
            done.moved.append(item)
            continue
        if not tags.write_genre(item.path, display):
            done.failed.append(item)
            continue
        if _genres(item.path) != (display,):
            done.wrong.append(item)
            continue
        done.written.append(item)
    return done


def taxonomy_alias_verb(ctx: "Context") -> Envelope:
    """Plan the alias and the files, ask, write the copy, then the files."""
    cfg = upgrade_cli._load()
    args = ctx.args
    root = _root(cfg, getattr(args, "folder", None))

    def plan_it(text: str) -> word_edit.Edit:
        try:
            return word_edit.alias(text, args.word, args.genre)
        except word_edit.Refused as exc:
            raise _refused(exc, args.word) from exc

    path, edit = _edit(cfg, plan_it)
    files = carrying(root, edit.word, edit.display)
    data = _alias_payload(edit, files)
    notes = _file_notes(files)
    if not edit.writes and not files.of(WRITE):
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[
                *notes,
                {
                    "code": NOTHING_TO_DO,
                    "message": (
                        f"{edit.word!r} is already a tagging alias of {edit.display} in the "
                        f"copy at {path}, and no file under {root} carries it alone"
                    ),
                },
            ],
        )
    spec = _gate(ctx.entry, ALIAS_GATE)
    context = {
        "copy": str(path),
        "word": edit.word,
        "genre": edit.display,
        "bucket": edit.bucket_id,
        "folder": str(root),
    }
    if ctx.gate.require(spec, plan=data, context=context) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=notes)

    # TAKEN AGAIN AFTER THE ANSWER, the copy and the files both, so an answer
    # given to the first plan is refused as stale rather than written over an
    # edit or a file retagged since.
    _, fresh = _edit(cfg, plan_it)
    fresh_files = carrying(root, fresh.word, fresh.display)
    if _alias_payload(fresh, fresh_files)["digest"] != data["digest"]:
        raise gates.DecisionStale(spec, ctx.run.run_id, data["digest"], _alias_payload(fresh, fresh_files)["digest"])

    sentences: list[dict[str, str]] = []
    if fresh.writes:
        kept, _ending, _raw = upgrade_cli.write_copy(
            cfg, spec, ctx.run.run_id, path, fresh.before, fresh.after, data["digest"], what="answered"
        )
        sentences.append(
            {
                "code": ALIAS_SAVED,
                "message": (
                    f"{fresh.word.lower()!r} is now a tagging alias of {fresh.display} in the "
                    f"copy at {path}, so a catalogue that gives it again is tagged "
                    f"{fresh.display!r}; nothing else the copy declares was changed, and "
                    f"the copy as it was is at {kept}"
                ),
            }
        )

    done = _retag(fresh_files.of(WRITE), fresh.display)
    if done.moved or done.failed or done.wrong:
        parts = []
        if done.moved:
            parts.append(f"{len(done.moved)} no longer carried what was planned and were left: {_named(tuple(done.moved))}")
        if done.failed:
            parts.append(f"{len(done.failed)} could not be written and are untouched: {_named(tuple(done.failed))}")
        if done.wrong:
            parts.append(f"{len(done.wrong)} were written and do not read back as {fresh.display!r}: {_named(tuple(done.wrong))}")
        steps = [f"run {word_edit.ALIAS_VERB} again, which plans only what still carries the word"]
        if done.written:
            steps.append(f"then {ROWS_FOLLOW}, so the rows of the files that took it follow")
        raise refuse(
            "taxonomy-word-unwritten",
            (
                ("the alias was saved; " if fresh.writes else "")
                + f"{len(done.written)} file(s) were retagged {fresh.display!r} and read back, and "
                + "; ".join(parts)
            ),
            steps=tuple(steps),
            origin=_ORIGIN,
            detail={
                "written": [item.relative for item in done.written],
                "moved": [item.relative for item in done.moved],
                "failed": [item.relative for item in done.failed],
                "wrong": [item.relative for item in done.wrong],
                "alias_saved": fresh.writes,
            },
        )
    if done.written:
        sentences.append(
            {
                "code": FILES_RETAGGED,
                "message": (
                    f"{len(done.written)} file(s) under {root} carrying {fresh.word!r} were "
                    f"retagged {fresh.display!r} and read back; run {ROWS_FOLLOW} so their "
                    f"rows follow, then {TREE_FOLLOWS} to file them in {fresh.display}"
                ),
            }
        )
    return ctx.envelope(data=data, warnings=[*notes, *sentences])


# ---------------------------------------------------------------------------
# The genre folder
# ---------------------------------------------------------------------------


def _folder_payload(edit: word_edit.Edit) -> dict[str, Any]:
    listed = (
        [
            {
                "kind": taxonomy_upgrade.BUCKET,
                "id": edit.bucket_id,
                "display": edit.display,
                "like": edit.like,
                "change": "add",
            }
        ]
        if edit.writes
        else []
    )
    return {
        "digest": output.digest_of(
            {
                "before": taxonomy.template_digest(edit.before),
                "after": taxonomy.template_digest(edit.after),
                "items": listed,
            }
        ),
        "items": listed,
        "totals": {"word": edit.word, "bucket": edit.bucket_id, "like": edit.like, "buckets": len(listed)},
        "chunk": None,
    }


def taxonomy_folder_verb(ctx: "Context") -> Envelope:
    """Plan the genre folder, ask, write the copy, read it back."""
    cfg = upgrade_cli._load()
    args = ctx.args

    def plan_it(text: str) -> word_edit.Edit:
        try:
            return word_edit.folder(text, args.word, getattr(args, "like", None))
        except word_edit.Refused as exc:
            raise _refused(exc, args.word) from exc

    path, edit = _edit(cfg, plan_it)
    data = _folder_payload(edit)
    if not edit.writes:
        return ctx.envelope(
            data=data,
            outcome=Outcome.NO_OP,
            warnings=[
                {
                    "code": FOLDER_ALREADY,
                    "message": (
                        f"the copy at {path} already declares the genre folder "
                        f"{edit.display} ({edit.bucket_id}), so nothing was written"
                    ),
                }
            ],
        )
    spec = _gate(ctx.entry, FOLDER_GATE)
    context = {"copy": str(path), "word": edit.word, "bucket": edit.bucket_id, "like": edit.like}
    if ctx.gate.require(spec, plan=data, context=context) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP)

    _, fresh = _edit(cfg, plan_it)
    moved = _folder_payload(fresh)
    if moved["digest"] != data["digest"]:
        raise gates.DecisionStale(spec, ctx.run.run_id, data["digest"], moved["digest"])
    kept, _ending, _raw = upgrade_cli.write_copy(
        cfg, spec, ctx.run.run_id, path, fresh.before, fresh.after, data["digest"], what="answered"
    )
    return ctx.envelope(
        data=data,
        warnings=[
            {
                "code": FOLDER_MADE,
                "message": (
                    f"the copy at {path} now declares the genre folder {fresh.display} "
                    f"({fresh.bucket_id}), with the {fresh.like} bucket's family, tempo window "
                    f"and rating, and a file whose genre is {fresh.word!r} routes there; run "
                    f"{TREE_FOLLOWS} to file the tracks already carrying it. Nothing else the "
                    f"copy declares was changed, and the copy as it was is at {kept}"
                ),
            }
        ],
    )


__all__ = [
    "ALIAS_GATE",
    "ALIAS_SAVED",
    "FILES_LEFT",
    "FILES_NOT_READ",
    "FILES_RETAGGED",
    "FOLDER_ALREADY",
    "FOLDER_GATE",
    "FOLDER_MADE",
    "NOTHING_TO_DO",
    "build_alias",
    "build_folder",
    "carrying",
    "taxonomy_alias_verb",
    "taxonomy_folder_verb",
]
