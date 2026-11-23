# U301's mutation table, notes

The table is `u301.md`, 18 rows over the helpers #858 added or rewrote,
measured on `b50588ff` with its full baseline read from that commit's
battery record: 17 killed, one zero, the null control zero over 22,923
tests. The guards each helper took over from its copies are held by the
kill set replay, `u301-replay-before` against `u301-replay-after`.

**T2 is an equivalent mutant.** It removes `_rewrite`'s skip of the save when
`clear_tags` finds an ID3 container with no tag block. Mutagen's save of such
a file writes nothing, so the file is byte for byte the same with or without
the skip; driven by hand on synthesized MP3, AIFF and WAV files, the mutated
and the real code leave identical bytes. The composite that holds the
property is `tests/test_tags.py::test_clearing_a_file_with_no_tag_block_writes_nothing`,
added at `3b6aa0a3`, which passes on both.

**Five rows first read zero and were given a test** before this measurement:
P1, G3 and F1 in a run cut at its time limit, J2 and R1 on their subsets by
hand. Each test was driven against its row by hand first (`7e06ad05`,
`b50588ff`), and the table above measured all five killed.

**Driven by hand, not by the driver:** the three reads the review parts make
through `core.review` (`_review.item_id_for` in `hold`, `_review.list_items`
in `grouped`, `_review._item_from_row` in `import_document`). Reverting a read
to a direct import is not a one line mutation the driver can apply without
also changing the import block, so each was reverted by hand with the name
imported directly, and its case of
`tests/test_review_queue.py::test_a_name_patched_on_review_reaches_the_module_it_moved_to`
failed, three of three.
