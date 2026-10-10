---
title: "The Record Labels tree never leaves the xml bridge, so a card that sends a write there through a database writer cannot be built as written"
date: 2026-10-10
category: workflow-issues
module: "src/cratekit/core/tree_registry.py, src/cratekit/label/heard.py"
problem_type: workflow_issue
component: tooling
severity: medium
root_cause: unverified_assumption
resolution_type: documentation_update
applies_when:
  - "A card or a plan asks for a write in the Record Labels tree, the catalogue tree, in the rekordbox database"
  - "A brief names inbox rotate's writer, move_tree_membership, or any rb_writer path for a tree other than the routing tree and the intake tree"
symptoms:
  - "A brief says a rekordbox half goes through the same gated writer inbox rotate uses, for the Record Labels tree"
  - "A test fixture would need a tree registry record with Mode.DATABASE for the catalogue tree, which no verb can write"
tags:
  - "record-labels"
  - "catalogue-tree"
  - "tree-cutover"
  - "brief-premise"
  - "r39"
---

# The Record Labels tree never leaves the xml bridge

## What happened

U123's card (#282) decided that `crate label heard` merges a dated playlist into
the year and removes it "in the Record Labels tree in rekordbox through the gated
landing writer", the one `inbox rotate` uses. That writer anchors through
`tree_registry.anchored_root` and refuses `tree-unconverged` for any tree still
on the bridge. `tree_registry.cutover_trees` returns the routing tree and the
intake tree and nothing else, and its docstring says why: the catalogue tree is
declared and kept on the bridge for good, because a catalogue crawl is not
rebuildable (R39). So the Record Labels tree is xml for ever, and the decided
writer can never accept it. Nothing wrote a dated playlist into that tree
either; U117 built the account half only.

## The rule

**Before a card sends a write into a rekordbox tree, check the tree is in
`cutover_trees`.** Only those two trees can be database native. For any other
tree the writers are the intake file's xml, which adds and cannot take a
playlist away, and nothing else. A fixture that records `Mode.DATABASE` for the
catalogue tree to make a database half testable is testing a state no verb can
produce, which the merge bar's reachability clause refuses.

## What U123 did

Built the account half, made the verb say on every run that rekordbox is not
changed, filed the tree half as a residual and a follow up card for the author's
decision, and did not build a writer for an unreachable state.

## Related

- `src/cratekit/core/tree_registry.py`, `cutover_trees` and `anchored_root`.
- `src/cratekit/organize/rekordbox.py`, `_record_labels`, which lists the tree
  and plans nothing in it for the same reason.
- The U123 residual "label heard writes nothing in the Record Labels tree, since
  the catalogue tree never leaves the xml bridge".
