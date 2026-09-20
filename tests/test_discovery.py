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


def test_a_symlinked_audio_file_is_still_an_item(tmp_path):
    """``is_file`` follows a link, which is what the one level scan always did.

    Pinned deliberately rather than left implicit: only a DIRECTORY link is
    declined, and narrowing this would change the default mode every existing
    job was queued under. R-589 records the cost.
    """
    elsewhere = tmp_path.parent / "elsewhere"
    touch(elsewhere, "real.flac")
    (tmp_path / "linked.flac").symlink_to(elsewhere / "real.flac")
    assert discovery.scan_audio(tmp_path).items == ("linked.flac",)
    assert discovery.scan_audio(tmp_path, recursive=True).items == ("linked.flac",)


def test_there_is_nothing_to_say_when_no_link_was_declined(tmp_path):
    touch(tmp_path, "track.flac")
    assert discovery.walk_warnings(*_omissions(tmp_path)) == ()


def test_the_warning_names_the_links_and_counts_the_rest(tmp_path):
    touch(tmp_path, "track.flac")
    for index in range(7):
        (tmp_path / f"link{index}").symlink_to(tmp_path.parent, target_is_directory=True)
    (warning,) = discovery.walk_warnings(*_omissions(tmp_path))
    assert warning["code"] == "linked-folder-skipped"
    assert "7 folders" in warning["message"]
    assert "link0" in warning["message"]
    assert "and 2 more" in warning["message"]


def test_one_declined_link_reads_as_one_folder_and_not_as_one_folders(tmp_path):
    """A plural only sentence is a defect a person sees on the commonest case."""
    touch(tmp_path, "track.flac")
    (tmp_path / "linked").symlink_to(tmp_path.parent, target_is_directory=True)
    (warning,) = discovery.walk_warnings(*_omissions(tmp_path))
    assert "1 folder under this tree is a symbolic link and was not walked" in (
        warning["message"]
    )
    assert "1 folders" not in warning["message"]
    assert "and 0 more" not in warning["message"]


def _omissions(folder: Path) -> tuple[tuple[str, ...], tuple[str, ...]]:
    scan = discovery.scan_audio(folder, recursive=True)
    return scan.skipped_links, scan.unreadable


# ---------------------------------------------------------------------------
# A folder the walk cannot read, which no symlink rule covers
# ---------------------------------------------------------------------------


def test_an_unreadable_folder_is_collected_rather_than_silently_dropped(tmp_path):
    """``os.walk`` swallows the error by default and the pass reports cleanly."""
    touch(tmp_path, "house/track.flac")
    shut = tmp_path / "locked"
    shut.mkdir()
    (shut / "hidden.flac").write_bytes(b"")
    shut.chmod(0o000)
    try:
        scan = discovery.scan_audio(tmp_path, recursive=True)
    finally:
        shut.chmod(0o755)
    assert scan.items == ("house/track.flac",)
    assert scan.unreadable == ("locked",)


def test_the_unreadable_warning_is_its_own_code_with_its_own_remedy(tmp_path):
    """A declined link needs no action. An unreadable folder needs one."""
    (warning,) = discovery.walk_warnings(unreadable=("locked",))
    assert warning["code"] == "folder-unreadable"
    assert "1 folder under this tree could not be read" in warning["message"]
    assert "permissions" in warning["message"]
    assert "locked" in warning["message"]


def test_both_omissions_ride_together_links_first(tmp_path):
    said = discovery.walk_warnings(("linked",), ("locked",))
    assert [one["code"] for one in said] == ["linked-folder-skipped", "folder-unreadable"]


def test_an_error_carrying_no_filename_is_still_reported(tmp_path):
    """The collected trace is the only evidence the omission happened at all."""
    (warning,) = discovery.walk_warnings(
        unreadable=(discovery._relative_or_absolute(tmp_path, None),)
    )
    assert "an unnamed folder under this tree" in warning["message"]


def test_a_path_outside_the_tree_is_reported_whole_rather_than_dropped(tmp_path):
    assert discovery._relative_or_absolute(tmp_path, "/elsewhere/locked") == (
        "/elsewhere/locked"
    )


# ---------------------------------------------------------------------------
# What a resume reads back, because it never re-walks
# ---------------------------------------------------------------------------


def test_the_frozen_payload_carries_the_mode_and_both_omissions(tmp_path):
    touch(tmp_path, "track.flac")
    (tmp_path / "linked").symlink_to(tmp_path.parent, target_is_directory=True)
    frozen = discovery.frozen(discovery.scan_audio(tmp_path, recursive=True), recursive=True)
    assert frozen == {
        "recursive": True,
        "skipped_links": ["linked"],
        "unreadable_folders": [],
    }


def test_a_resume_says_what_the_queue_said_from_the_payload_alone(tmp_path):
    frozen = {"folder": str(tmp_path), "recursive": True, "skipped_links": ["linked"]}
    said = discovery.warnings_of(frozen)
    assert [one["code"] for one in said] == ["linked-folder-skipped"]
    assert said == discovery.walk_warnings(("linked",))


def test_a_resume_repeats_the_unreadable_half_and_not_only_the_links():
    """The two halves are frozen separately, so they are read back separately.

    Added after the U93 mutation table: D19, dropping the unreadable half from
    ``warnings_of``, killed zero because every resume case in the suite froze
    links only.
    """
    said = discovery.warnings_of({"unreadable_folders": ["locked"]})
    assert [one["code"] for one in said] == ["folder-unreadable"]
    both = discovery.warnings_of(
        {"skipped_links": ["linked"], "unreadable_folders": ["locked"]}
    )
    assert [one["code"] for one in both] == ["linked-folder-skipped", "folder-unreadable"]


def test_a_payload_from_a_build_that_never_walked_a_tree_says_nothing():
    """An older job carries neither key, and silence is the right answer for it."""
    assert discovery.warnings_of({"folder": "/somewhere"}) == ()
    assert discovery.warnings_of(None) == ()


def test_a_payload_whose_lists_are_the_wrong_shape_says_nothing_rather_than_raising():
    assert discovery.warnings_of({"skipped_links": "linked"}) == ()


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
