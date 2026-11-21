---
title: The suite's disposable rekordbox database is built with its foreign keys in an order that changes from one process to the next
found: at the review of #854, U297, fix round one, 2026-11-21.
issue: no
---

**The mechanism.** `tests/test_rb_writer_db.py::_relaxed_schema` copies the
binding's tables into a fresh `MetaData` with `Table.to_metadata`, which
walks each table's constraints as a set of objects. The copies take their
creation order from that walk, the order follows the objects' addresses, and
`create_all` writes the FOREIGN KEY clauses of each CREATE TABLE in it. A
fixed hash seed does not hold it still.

**Measured cost.** Found by the schema comparison the review asked for, on
its first run: two captures of one commit differed in five table
declarations. The review then built the schema in ten processes and read ten
distinct digests. `scripts/behaviour_compare.py` reads a table's declaration
with its table constraints in one order, which the review checked changes
nothing but that order over the 40 declarations of a real capture. No test
of the suite reads the declaration's text, so nothing else pays.

**Closes when:** the builder orders the copied constraints, at which point
`canonical_declaration` could go; the file is on U300's list. Ledger only.
