---
title: The citation rule's coverage is contagious, and the file you join carries old numbers
date: 2026-09-20
category: workflow-issues
module: tests/test_reserved_causes.py
problem_type: guard_interaction
component: testing_framework
severity: medium
root_cause: derived_coverage_set
resolution_type: wording_fix
applies_when:
  - A unit wants to reference the residual finding it closes from the code or the
    tests it is landing
  - The file it wants to write that reference in already cites some other
    finding by R number, which most long lived files in this repository do
  - The reference is written in the scanned citation form, the word residual
    then whitespace then a quoted title
tags:
  - citation
  - residual-numbers
  - derived-coverage
  - guard-interaction
  - test-reserved-causes
---

# The citation rule's coverage is contagious, and the file you join carries old numbers

## Context

`tests/test_reserved_causes.py` bans citing a residual by NUMBER, because numbers
are append only and an incoming branch's numbers move at a merge, so a number in
a file silently changes subject. Cite the TITLE instead, declare it in
`CITED_RESIDUALS`, and the test checks both directions.

The rule does not apply to every file. `owned_sources()` DERIVES the covered set:
a file is covered when it already contains a citation in the scanned form, which
`CITATION` defines as the word `residual` or `residuals`, then nothing but
whitespace, `#` or `:`, then a title in double quotes. The docstring is explicit
that this is on purpose, since a hand written list falls out of date and a diff
derived list goes empty at the merge.

## What actually happens

Adopting the form in a file ENROLS that file in the whole rule, retroactively.
Landing item 4 of the five-places finding meant writing one sentence of context
in four files, and in the scanned form. All four are long lived and all four
already carried R numbers for other units' findings, placed there when the file
was outside the rule. The suite went from green to:

```
these files cite a residual by NUMBER:
  {'src/cratekit/cli/setup.py': ['R-347'],
   'src/cratekit/core/cause.py': ['R-102', 'R-116', 'R-130', 'R-154', 'R-172',
                                  'R-342', 'R-368', 'R-500', 'R-80'],
   'tests/test_config.py': ['R-116'],
   'tests/test_doctor.py': ['R-1', 'R-116', 'R-344', 'R-346', 'R-347', 'R-80']}
```

Seventeen numbers, none of them this unit's, all of them belonging to findings
this unit had no business renaming. Converting them means seventeen new
`CITED_RESIDUALS` entries, each of which has to resolve to exactly one heading in
a twelve thousand line document, for a unit whose diff is one reader function.

Note what `setup.py` was already doing at `_seed_taxonomy`: it cites the same
finding as `the residual finding "Five places where ..."`. The word `finding`
between `residual` and the quote means `CITATION` does not match, so the file
stayed outside the rule and its `R-347` stayed legal. That was not obviously
deliberate, and it is the shape the rule's own docstring warns about, a citation
the scan cannot see.

## Guidance

Write the reference in words, not in the scanned form, unless you intend to
convert every number already in that file:

- Reference the finding descriptively. "Item 4 of the five-places residual
  finding" carries as much as a number does and cannot rot at a merge.
- Put the ONE formal, registered citation in a file that is already covered and
  already clean. For this unit that was `tests/test_reserved_causes.py` itself,
  where the population re-pins live and where a title has to be declared anyway.
- If a title contains double quotes, as this one does, the form cannot carry it:
  `CITATION` stops at the first inner quote. Declare the leading phrase, which
  the resolver already allows for the two headings that read badly inline, and
  say in a comment that it is a prefix and why.

The cost of getting this wrong is not a broken product, it is a red suite an hour
before a merge and a tempting shortcut: write the citation in a form the scan
cannot see, which is how `R-347` in `setup.py` survived in the first place.
