# XML splice golden files

Byte-exact captures of what each rekordbox XML splicer emits, driven by
`tests/test_xml_splice_golden.py` against the synthetic fixtures in
`tests/xml_fixtures.py`.

Nine of these files are ported byte for byte from the source system, and the table says which one is not. They exist to
make one specific change safe: the source system carried **five duplicated splice
implementations**, and Cratekit collapses them into one writer. Collapsing five
implementations into one is exactly the change that produces a byte difference
nobody notices, and in this format a byte difference means a playlist that
renders wrong in rekordbox or a document tail that is quietly truncated.

**These pin CURRENT behaviour, bugs included.** A golden failing means the bytes
changed. Decide whether that change was intended before you do anything else.

## Regenerating (intended changes only)

```
REGEN=1 pytest tests/test_xml_splice_golden.py
```

Then review the byte diff before committing. **Never hand-edit a `.bytes` file.**
The producing code is the source of truth; a hand-edited golden pins a fiction,
and the next person to read it has no way to know.

## What each golden locks

Every row here is checked by a test. `test_every_declared_golden_is_present_and_no_others`
asserts the table and the directory agree in both directions, and
`test_golden_still_carries_the_invariant_it_documents` asserts the bytes still
contain the structure the row claims. A golden cannot rot into an opaque blob.

| Golden | Invariant locked | Unit that may change it |
|---|---|---|
| `splice_subplaylist.bytes` | CRLF only, 12-space TRACK indent, Entries bumped on the target sub | U17 (the XML bridge; must stay byte-identical) |
| `splice_subplaylist_collision.bytes` | A COLLECTION track named after the genre folder does not hijack the anchor; the bait TRACK stays self-closed | U17 |
| `sort_inbox_route.bytes` | CRLF-only routing splice with the Entries count bumped to match | U18 (tree writers) |
| `sort_inbox_rating.bytes` | The Rating value is patched in place and CRLF is undisturbed | U18 |
| `sort_unplaced_existing_sub.bytes` | The existing-sub insert path emits CRLF, not the bare LF it once did | U18 |
| `sort_unplaced_new_sub.bytes` | The sub-creation path emits CRLF and opens the new node correctly | U18 |
| `sort_unplaced_rating.bytes` | The second copy of the rating writer, pinned so the consolidation is byte-checked from both sides | U18 |
| `create_vox_playlists.bytes` | CRLF only, a self-closed vocal sub-playlist node, folder Count bumped | U18 |
| `label_library_insert.bytes` | CRLF label subtree, ROOT Count bumped, newest year ordered first | U18 |
| `land_label_tree.bytes` | A landed batch's one document carries both the intake playlist and the label tree, labels A to Z, newest year first. NOT ported, the source system had no landing step. Regenerate with `REGEN=1 pytest tests/test_landing_labels.py`. The library's location, the date added and the container size are put back to fixed values before the compare | U77 (the landing engine and the catalog writer) |

## Why the producer tests are skipped right now

U6 ports the guards **before** the engine they guard, so a violation cannot be
introduced silently in the units between. The writers these goldens compare
against land in U17 and U18. Until then:

- the **integrity** tests run and pass: each golden is CRLF only, well formed,
  correctly terminated, and still carries the structure its table row claims;
- the **producer** tests are skipped with a reason naming the unit that unblocks
  them, and `tests/test_pending_units.py` fails the build the moment that unit
  lands unless the skip is removed.

Nothing is stubbed to make a skipped test pass. A stub would turn a real guard
into a test of the stub.
