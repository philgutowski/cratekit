---
title: tag set cannot make a genre row the library lacks, so a new genre folder still needs one hand edit in rekordbox first
found: at the battery of #988, U339, 2026-11-23.
issue: yes
---

**The mechanism.** U339's brief asks `crate tag set GENRE` to mint the `djmdGenre` row for a word the library has no active row for, linked on the same commit. `tests/test_rb_writer_guard.py::test_every_other_writer_in_the_package_asks_for_no_creation` allows only `intake/native.py` to pass `creations=` to `rb_writer.commit_guarded`, and `test_rb_writer_guard.py` keeps the lookup tables out of `PERMITTED_ROW_TABLES`. A build session may not edit that suite, so `tag set` (`tagging/genre_set.py`) links an existing active row and, when there is none, leaves every named row `genre-unknown`, writes nothing on any file or row, and warns `set-genre-has-no-row`.

**Measured cost.** Driven: `tests/test_tag_set.py::test_a_genre_the_library_has_no_row_for_writes_nothing_and_names_the_act`. A DJ who makes a new genre folder, as Phillip did with Deep and Soulful House on 2026-11-22, must give one track that genre in rekordbox before `tag set` files anything under it: the workflow cannot finish from the command line (board bar c).

**Closes when:** the guard suite names `tagging/genre_set.py` as a second asker, admitting `djmdGenre` alone on the commit that links it, and `tag set` mints the row by hand as `intake/native.py`'s `_Mints._mint` does (ID from `generate_unused_id`, text; `Name`; a fresh `UUID`), flushed before `metadata.plan_genre_retag` resolves it, with tests for a mint shared by many rows, a tombstoned namesake skipped, and nothing minted when no row is written. The decision is on #988's card.
