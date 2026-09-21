# U97 mutation pass, notes

Issue #142, branch `relay/142`, 2026-09-21. Three tables, `u97-a.md`,
`u97-b.md` and `u97-c.md`, rows files beside each. **Thirteen rows, eleven
killed, two zero, both zeros paired with a composite that killed.** The
author's own table and no independent one, which METHOD requires to be said
here rather than implied: every number below is what the author could kill, not
what is killable.

Three tables rather than one to stay inside the harness tool ceiling, the same
reason R-338's pass was split. The cap is 25 rows and nothing was dropped for
it: thirteen is every guard the diff added plus a sample of the four existing
guards this unit now leans on.

## The shape of the pass

Batch A is the diff's own guards, six rows, six killed. Each one is a way the
remedy could go back to naming something nobody can perform: the bare verb
returning, the rejected session's wording returning, and the procedure losing
the erase, the `--from-file` flag, or the document pointer. The sixth removes
the `_ADVICE` fallback in `remedy_text`, which is not new but is the mechanism
the whole unit rests on, since the fix works by leaving the command `None`.

Batch B is the sample of existing guards the unit reaches through, five rows,
three killed and two zero.

Batch C is the two composites the zeros owe, both killed.

## The two zero rows, and what the composites showed

**`B4_outbound_path_raises_the_other_token`, kills 0 on the full suite.**
`modules/outbound/account.py` refuses a missing provider session and is the
third raiser of this token, the one the brief does not name. Swapping its
remedy to `REAUTHENTICATE_PROVIDER` tells a person who never had a session that
theirs was rejected, and nothing in 9,446 tests notices.

Composite `C1_outbound_refusal_removed` deletes the refusal outright: **kills 1**,
and only on the full suite, the subset of three worker files killed nothing.
So the refusal is held by exactly one test and its remedy is held by none. The
guard exists, the words it routes to do not.

**`B5_remediation_line_prefers_a_step`, kills 0 on the full suite.** Reading
`cause.remediation.steps[0]` before the token changes what a person reads for
every cause carrying both. **The input is reachable and was measured, not
argued**: an AST walk over `src/cratekit` finds 52 call sites passing `steps`
and `remedy` together, across twelve modules. So this is a test gap and not an
inert mutation.

Composite `C2_remediation_line_drops_the_token_branch` removes the token branch
entirely: **kills 4**. The renderer's use of the table is held. The precedence
between the table's words and a cause's own first step is not.

Both are filed, R-618 and R-619. Neither is blocking: in each case the person
still reads an actionable sentence, it is just not the one the table chose.

## Driver rules, as observed

- `PYTHONDONTWRITEBYTECODE=1` set on every batch.
- Foreground, three batches, nothing else touching the tree while one ran.
- Null control at zero on all three baselines, 1,076 collected on the subset
  and 9,446 on the full suite, matching in both directions.
- Every row's `head_verified` is true, and all four mutated files were
  differenced against `git show HEAD:` after the last batch. No drift.
- No promotion was skipped: every zero on a subset was re-run against the full
  suite before it was reported as a zero.
