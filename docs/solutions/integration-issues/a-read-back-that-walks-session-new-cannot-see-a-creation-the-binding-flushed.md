---
title: "A read back that walks session.new cannot see a creation the binding flushed, and a fixture that sorts the right way proves nothing about the rule"
date: 2026-09-29
category: integration-issues
module: "src/cratekit/core/rb_writer.py, src/cratekit/intake/native.py, tests/test_intake_land_native.py"
problem_type: integration_issue
component: database
severity: high
root_cause: missing_validation
resolution_type: code_fix
applies_when:
  - "A guard reads an object mapper session's pending collections to decide what a commit will do"
  - "A pyrekordbox helper that ends in flush() is called before the guard runs, add_content, add_album, add_artist, add_genre or add_label"
  - "A second reader of the binding's update buffer is written beside the first"
  - "A mutation row picks the wrong candidate only when the fixture's ordering happens to agree with it"
  - "A verb has one gate per medium and the conformance drive can reach one medium"
symptoms:
  - "The whitelist refuses a flushed creation through the buffer while the SQL read back never selects its row"
  - "A mutation that removes a selection rule measures zero on the full suite"
  - "A declared gate is reported silent by conformance 3 although its own suite drives it"
related_components:
  - testing_framework
  - development_workflow
tags:
  - guarded-writer
  - autoflush
  - registry-buffer
  - add-content
  - mutation-table
  - unreachable-gates
  - r746
  - r760
---

# A read back that walks session.new cannot see a creation the binding flushed

## What happened

R-746 admitted the first content row through the guarded writer. R-760 had
recorded that `commit_guarded` refused `db.add_content` on a copy, so the
whitelist was known to see the flushed creation through the binding's update
buffer (W2). What nobody had read was the SQL read back behind the whitelist,
`assert_created_rows_are_gridless`. It collected the created instances from
both sources to decide whether to run, and then iterated `session.new` alone
to select rows. `add_content` ends in `flush()`, so its row had left
`session.new` before the guard ran: the whitelist judged the row's declared
columns and the SQL check selected nothing. A tempo put on the row by SQL
after the flush, where the in memory judge cannot see it, would have been
committed.

The fix reads the created instances from the buffer as well, through one
walk of the buffer both readers share, and a content row is held to the ten
columns an analysis pass fills plus the three tables it writes rows into.

## The second finding, from the mutation table

The row that removed the device rule, "every device matches so the first by
identifier wins", measured zero on the full suite. The fixture's wrong device
was `d-other` and the right one `d-mine`, so a choice that dropped the
`MasterDBID` comparison and kept the sort still picked `d-mine`. The fixture
agreed with the mutation by accident of alphabet. Renaming the wrong device
to sort first made the same row kill.

## The third, from the conformance suite

One verb, two gates, one per medium, and the conformance drive builds one
library whose intake tree is on the bridge, so it can reach one gate. The
suite holds every declared gate to firing unless it is named in
`UNREACHABLE_GATES` with the reason. The native gate is named there, with the
suite that does drive it, rather than made reachable by an argument, because
the medium is the tree's mode and not a flag.

## How to apply

- Before a guard reads a session's pending collections, list every binding
  helper the path calls and check which end in `flush()`. For those, the
  buffer is the only record of the creation, and every reader of the guard,
  the judge and the read back alike, has to take its instances from it.
- Write one walk of the buffer and hand its entries to each reader. Two walks
  agree today and disagree the day the binding changes an entry's shape.
- When a mutation row measures zero, ask whether the fixture's incidental
  order, naming or defaults agree with the mutated rule before concluding the
  rule is untested. Rename the fixture so the wrong answer is the default.
- A per medium gate that one fixture cannot reach is an `UNREACHABLE_GATES`
  entry naming the suite that reaches it, not a second argument on the verb.
