---
title: label heard writes nothing in the Record Labels tree, since the catalogue tree never leaves the xml bridge
found: at the plan of #282, U123, 2026-10-10.
issue: no
---

**The mechanism.** The brief asked `crate label heard` to merge the dated
playlist into the year and remove it in the Record Labels tree too, through the
gated database writer `inbox rotate` uses. That writer refuses a tree that is
not cut over (`tree-unconverged`), and `tree_registry.cutover_trees` admits the
routing tree and the intake tree only: the catalogue tree stays on the xml
bridge for good, because a catalogue crawl is not rebuildable (R39). Nothing
writes a dated playlist into the Record Labels tree either, since U117 built the
account half only, and `organize`'s rekordbox area lists that tree and plans
nothing in it. So the verb writes the account and the label review store, and
says on every run, under `label-heard-tree-unchanged`, that rekordbox is not
changed.

**Measured cost.** None today: no dated playlist exists in the tree to merge,
measured by reading every writer of the tree (`write/trees.py`'s
`insert_record_labels_trees` builds `Record Labels / <Label> / <Label> <year>`
and nothing dated). A tree half built against a database native Record Labels
tree would be code over a state the product cannot reach.

**Closes when:** the author decides whether the dated playlist belongs in
rekordbox at all, and if it does, through which writer: the intake file's xml
for the add and something else for the removal, since an xml import cannot take
a playlist away. A31, issue #289, filed with this unit, carries the question.
Ledger only.
