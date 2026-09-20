"""U93: one walker for the queued analysis verbs, and the join that checks itself.

``core.discovery`` replaced two identical one level scans, one in
``analysis/cli.py`` and one in ``vocals/cli.py``, and grew the recursive mode
both needed. These are the walker's own guards. The verbs' behaviour over a tree
is pinned in ``test_analysis_workers.py`` and ``test_vocals_cli.py``, because a
walker that returns the right list and a job that queues the wrong one are two
different failures.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.core import discovery
from cratekit.core.cause import CratekitError


def touch(folder: Path, relative: str) -> Path:
    path = folder / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")
    return path


# ---------------------------------------------------------------------------
# The one level mode, which has to stay exactly what it was
# ---------------------------------------------------------------------------


def test_one_level_is_the_default_and_a_subfolder_is_invisible(tmp_path):
    """The default is what every existing job and every existing resume assumed."""
    touch(tmp_path, "top.flac")
    touch(tmp_path, "genre/nested.flac")
    assert discovery.scan_audio(tmp_path).items == ("top.flac",)


def test_a_folder_that_is_not_there_is_an_empty_scan_rather_than_an_error(tmp_path):
    scan = discovery.scan_audio(tmp_path / "unmounted", recursive=True)
    assert scan.items == ()
    assert scan.skipped_links == ()


def test_a_non_audio_suffix_is_not_an_item(tmp_path):
    touch(tmp_path, "cover.jpg")
    touch(tmp_path, "notes.txt")
    touch(tmp_path, "track.flac")
    assert discovery.scan_audio(tmp_path).items == ("track.flac",)


def test_a_directory_carrying_an_audio_suffix_is_not_an_item(tmp_path):
    """``is_file`` and not ``exists``: a folder called ``mix.flac`` is not a track."""
    (tmp_path / "mix.flac").mkdir()
    touch(tmp_path, "real.flac")
    assert discovery.scan_audio(tmp_path).items == ("real.flac",)


def test_the_suffix_match_is_case_insensitive(tmp_path):
    touch(tmp_path, "shouted.FLAC")
    assert discovery.scan_audio(tmp_path).items == ("shouted.FLAC",)


# ---------------------------------------------------------------------------
# The recursive mode
# ---------------------------------------------------------------------------


def test_a_nested_tree_queues_every_file_once_in_sorted_order(tmp_path):
    for relative in (
        "house/b.flac",
        "house/a.flac",
        "techno/deep/c.aiff",
        "top.mp3",
    ):
        touch(tmp_path, relative)
    assert discovery.scan_audio(tmp_path, recursive=True).items == (
        "house/a.flac",
        "house/b.flac",
        "techno/deep/c.aiff",
        "top.mp3",
    )


def test_the_same_filename_in_two_folders_is_two_items(tmp_path):
    """``job_items`` is keyed ``(job_id, item_id)``, so bare names would collide.

    This is the whole reason the id is a relative path rather than a name. Every
    real library holds one track name in more than one genre folder, and a
    recursive walk that kept names would fail the insert on the first one.
    """
    touch(tmp_path, "house/track.flac")
    touch(tmp_path, "techno/track.flac")
    items = discovery.scan_audio(tmp_path, recursive=True).items
    assert items == ("house/track.flac", "techno/track.flac")
    assert len(set(items)) == len(items)


def test_a_top_level_file_has_the_same_id_in_both_modes(tmp_path):
    """The modes agree where they overlap, so switching one on is not a renumber."""
    touch(tmp_path, "top.flac")
    assert discovery.scan_audio(tmp_path).items == (
        discovery.scan_audio(tmp_path, recursive=True).items
    )


def test_an_appledouble_sidecar_under_a_nested_folder_is_skipped(tmp_path):
    touch(tmp_path, "house/track.flac")
    touch(tmp_path, "house/._track.flac")
    touch(tmp_path, "house/.DS_Store.flac")
    assert discovery.scan_audio(tmp_path, recursive=True).items == ("house/track.flac",)


def test_a_dot_directory_is_not_descended(tmp_path):
    touch(tmp_path, "keep.flac")
    touch(tmp_path, ".Trashes/deleted.flac")
    touch(tmp_path, ".Spotlight-V100/index.flac")
    assert discovery.scan_audio(tmp_path, recursive=True).items == ("keep.flac",)


def test_the_id_separator_is_posix(tmp_path):
    """The id is persisted and read back by a later process, so it is not a local fact."""
    touch(tmp_path, "a/b/c.flac")
    assert discovery.scan_audio(tmp_path, recursive=True).items == ("a/b/c.flac",)


# ---------------------------------------------------------------------------
# Symlinks: the loop hazard, and the skip said out loud
# ---------------------------------------------------------------------------


def test_a_symlinked_directory_is_not_walked_and_is_reported(tmp_path):
    touch(tmp_path, "house/track.flac")
    elsewhere = tmp_path.parent / "elsewhere"
    touch(elsewhere, "other.flac")
    (tmp_path / "linked").symlink_to(elsewhere, target_is_directory=True)

    scan = discovery.scan_audio(tmp_path, recursive=True)
    assert scan.items == ("house/track.flac",)
    assert scan.skipped_links == ("linked",)


def test_a_symlink_loop_terminates(tmp_path):
    """``followlinks=False`` makes the loop impossible rather than survivable.

    A visited set has to be correct to defeat this. Not entering a link cannot
    be incorrect, and the cost of that choice is the warning above.
    """
    touch(tmp_path, "track.flac")
    (tmp_path / "loop").symlink_to(tmp_path, target_is_directory=True)
    assert discovery.scan_audio(tmp_path, recursive=True).items == ("track.flac",)


def test_a_one_level_scan_reports_no_links_even_when_one_is_there(tmp_path):
    """Nothing is walked, so nothing was declined, so there is nothing to say."""
    touch(tmp_path, "track.flac")
    (tmp_path / "linked").symlink_to(tmp_path.parent, target_is_directory=True)
    assert discovery.scan_audio(tmp_path).skipped_links == ()


def test_the_warning_is_none_when_no_link_was_declined(tmp_path):
    touch(tmp_path, "track.flac")
    assert discovery.skipped_links_warning(discovery.scan_audio(tmp_path, recursive=True)) is None


def test_the_warning_names_the_links_and_counts_the_rest(tmp_path):
    touch(tmp_path, "track.flac")
    for index in range(7):
        (tmp_path / f"link{index}").symlink_to(tmp_path.parent, target_is_directory=True)
    warning = discovery.skipped_links_warning(discovery.scan_audio(tmp_path, recursive=True))
    assert warning is not None
    assert warning["code"] == "linked-folder-skipped"
    assert "7 folders" in warning["message"]
    assert "link0" in warning["message"]
    assert "and 2 more" in warning["message"]


# ---------------------------------------------------------------------------
# The join, which is a guard because an id may now carry separators
# ---------------------------------------------------------------------------


def test_a_relative_id_joins_under_the_folder(tmp_path):
    assert discovery.item_path(tmp_path, "house/track.flac") == tmp_path / "house/track.flac"


def test_a_bare_filename_still_joins(tmp_path):
    """``analyze run`` never gets the flag, so its ids stay one segment."""
    assert discovery.item_path(tmp_path, "track.flac") == tmp_path / "track.flac"


def test_an_absolute_id_is_refused_rather_than_discarding_the_folder(tmp_path):
    """``Path("/library") / "/etc/passwd"`` is ``/etc/passwd``, silently."""
    with pytest.raises(CratekitError) as raised:
        discovery.item_path(tmp_path, "/etc/passwd")
    assert raised.value.cause.reason == "internal-error"
    assert "/etc/passwd" in raised.value.cause.message


def test_a_parent_segment_is_refused(tmp_path):
    with pytest.raises(CratekitError) as raised:
        discovery.item_path(tmp_path, "house/../../outside.flac")
    assert raised.value.cause.reason == "internal-error"


def test_the_refusal_names_the_folder_it_was_leaving(tmp_path):
    with pytest.raises(CratekitError) as raised:
        discovery.item_path(tmp_path, "../outside.flac")
    assert raised.value.cause.detail["folder"] == str(tmp_path)
    assert raised.value.cause.detail["item"] == "../outside.flac"
