---
title: "A parametrize id copies an assembled literal whole into the mutation records, where the repository scan refuses it"
date: 2026-11-24
category: workflow-issues
module: "tests/test_portability.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "A test assembles a bad literal from fragments so the repository scan does not flag the test file"
  - "That literal is a parametrize value, so pytest builds the node id from it"
  - "A mutation table, a kill set or any record copies node ids into a tracked file"
symptoms:
  - "The suite and the scan are clean on the branch, then the committed mutation sidecar fails test_the_repository_itself_is_clean"
  - "The scan names a home directory or volume path inside docs/mutation/<unit>.json or .md"
tags:
  - "scan"
  - "portability"
  - "pytest"
  - "mutation-table"
  - "node-id"
---

# A parametrize id copies an assembled literal whole into the mutation records

## What happened

U957's tests in `tests/test_portability.py` build path and host literals from
fragments (`"/" + "Users" + "/" + _W + "/Music"`), as the module docstring
asks, so a machine named by the fixture word does not fail the test file. The
literals were `@pytest.mark.parametrize` values, and pytest makes a string
value the node id, whole: `test_...[` followed by the assembled path itself. `scripts/mutate.py`
writes every killing node id into `docs/mutation/<unit>.json` and `.md`. The
first table, 21 of 21 killed, committed cleanly, and the next run of
`test_the_repository_itself_is_clean` found 48 home directory and volume paths
in the two records. The fragments protected the source and nothing else.

## The fix

Give a parametrize whose values are bad literals opaque ids:

    def _opaque_id(written: str) -> str:
        return hashlib.sha256(written.encode()).hexdigest()[:10]

    @pytest.mark.parametrize("written", [...], ids=_opaque_id)

Check with `pytest --collect-only -o addopts= <file>` and a grep of the ids
before the table runs, not after. A table already written with the literal
ids cannot be edited by hand; it is measured again.

## Where else

Older parametrized tests in the same file (`test_guard_covers_every_shipped_surface`)
carry made up paths in their ids. They are safe only because no unit's table
has killed them yet; a row on the path classes would write them into its
record.
