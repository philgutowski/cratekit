"""The census proof that a backup root is the library: what the root holds against
what the last completed backup held. Re-exported by :mod:`cratekit.modules.tools.backup`.
"""

from __future__ import annotations

from cratekit.core import backup_facts, config
from cratekit.modules.tools import backup_record

#: The one way past the content proof.
EMPTIED_FLAG = "--library-emptied"


def _history(cfg: config.Config) -> tuple[int | None, str] | None:
    """How many of the library's files the last completed backup held (None if
    unreadable), and which record says so, or None when none says a backup was
    kept: the census alone if there is one, then the record, then the fact."""
    census = backup_record.read_census(cfg)
    if census is not None:
        return census.files, "the last completed backup"
    manifest, _ = backup_record.read_manifest()
    if (
        manifest is not None
        and manifest.library_root == str(cfg.library.root)
        and manifest.dest == str(cfg.backup.dest)
    ):
        return (
            backup_record.count_held(manifest.entries, cfg.library.state_dirname),
            "the record of the last completed backup",
        )
    try:
        fact = backup_facts.read_facts(cfg).get(backup_facts.Portion.FILES)
    except backup_facts.BackupFactsUnreadable:
        return None, "the library's own record of its backups"
    if fact is not None:
        return None, "the library's own record of its backups"
    return None


def _unproven(
    cfg: config.Config, *, anything: bool, held: int, emptied: bool
) -> tuple[str, bool]:
    """Why what the root holds does not prove it is the library, or an empty
    string, and whether it is a new library's first backup. ``emptied`` passes
    only where the root still carries the library's own files fact, which an
    emptied library keeps and a lost volume's mount point does not."""
    root = cfg.library.root
    remedy = (
        f"Mount the library's volume and back up again; if the library was "
        f"emptied on purpose, back it up with {EMPTIED_FLAG}"
    )
    if emptied:
        try:
            carried = backup_facts.read_facts(cfg).get(backup_facts.Portion.FILES)
        except backup_facts.BackupFactsUnreadable:
            carried = None
        if carried is not None:
            return "", False
        return (
            f"the backup was asked with {EMPTIED_FLAG} and the library root {root} does not carry "
            f"the library's own record of a completed files backup, which a library emptied by its "
            f"owner keeps in its state folder and the folder an unmounted volume leaves does not, "
            f"so nothing was sent or archived. Mount the library's volume and back up again; a "
            f"library emptied before its first completed backup needs no flag"
        ), False
    history = _history(cfg)
    if not anything:
        held_before = ""
        if history is not None and history[0]:
            held_before = f", where {history[1]} held {history[0]} files"
        return (
            f"the library root {root} holds no file at all, not even the "
            f"library's own state folder{held_before}, which is what an "
            f"unmounted volume leaves, so nothing was sent or archived. {remedy}"
        ), False
    if history is None:
        return "", held == 0
    had, said = history
    if held == 0 and had != 0:
        counted = "files" if had is None else f"{had} files"
        return (
            f"the library root {root} holds no file outside the library's own state folder, and "
            f"{said} held {counted}, so nothing was sent or archived. {remedy}"
        ), False
    if had and held * backup_record.LIBRARY_FLOOR < had:
        return (
            f"the library root {root} holds {held} files outside the library's own state folder, "
            f"under a tenth of the {had} {said} held, so it is not proven to be the library and "
            f"nothing was sent or archived. {remedy}"
        ), False
    return "", False
