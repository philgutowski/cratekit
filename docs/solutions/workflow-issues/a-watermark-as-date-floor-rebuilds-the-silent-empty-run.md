---
title: "A watermark as a date floor rebuilds the silent empty run"
date: 2026-08-17
category: workflow-issues
module: "src/cratekit/sync/scope.py, src/cratekit/sync/run.py, tests/test_incremental_sync.py"
problem_type: workflow_issue
component: development_workflow
severity: high
root_cause: inadequate_documentation
resolution_type: documentation_update
applies_when:
  - "A session is implementing or changing incremental sync scope and reads the U22 brief test scenario as the spec"
  - "A re-run after a clean sync is being designed to process only items newer than each watermark"
  - "A watermark cursor is about to be compared against item recency to decide what enters scope"
  - "KTD11 is being reconciled with a brief sentence that sounds like a date floor"
symptoms:
  - "A re-run after a clean sync processes nothing even though unowned items remain in the newest N"
  - "scoped or increment is written to skip items at or before the stored cursor"
  - "The user visible outcome is an empty run rather than owned dedup of the newest N"
  - "The silent date-floor empty run (the favorite-label year floor, encoded in KTD11) is back under a new name"
related_components:
  - testing_framework
  - documentation
tags:
  - silent-failure
  - incremental-sync
  - owned-dedup
  - ktd11
  - date-floor
---

# A watermark as a date floor rebuilds the silent empty run

## Context

U22 landed as `dc830ef` on `main` in this repository. Cratekit merges locally. There is no pull request. The unit is incremental sync per source. Its load bearing rule is KTD11, written in the reengineering plan as:

> Watermarks are audit records that gate nothing on their own. Scope comes from most-recent-N plus dedup against what is owned. A watermark advances only on a source completing without error, and a total-failure path raises rather than returning an empty result. This repo removed scope-driving watermarks once already after a silent zero-scope failure.

That text is in the sibling DJ_tools reengineering plan (2026-08-01-001), around KTD11. The same plan's U22 brief then lists this test scenario:

> A re-run after a clean sync processes only items newer than each watermark.

Those two sentences sit in one document and look like they disagree. KTD11 says the watermark gates nothing. The brief names the watermark as the thing the second run filters by. A session that treats the issue as the brief, and treats a test scenario as an implementation instruction, will wire the cursor into `scoped()` and rebuild the silent empty run DJ_tools already paid for.

They are not a contradiction. The brief is naming the user visible outcome. The KTD is naming the mechanism. After a clean sync the already taken items are owned, so owned dedup drops them. The watermark is written as an audit of how far that clean run got. It is never a date floor.

The landed code holds the mechanism, not the brief's noun.

`src/cratekit/sync/scope.py:21` is the defining signature:

```python
def scoped(
    candidates: Sequence[ScopedItem],
    *,
    owned: set[str] | frozenset[str],
    limit: int,
) -> list[ScopedItem]:
```

Three inputs: the list the source just returned, the identities already owned, and a count. There is no watermark parameter. The function docstring states the refusal in one sentence: this function does not sort, does not read a watermark, and does not treat an empty owned set as "everything is new" in any special way. The module docstring names KTD11 and the historical failure: using the watermark as a date floor is the silent zero-scope failure DJ_tools already removed once.

`src/cratekit/sync/run.py:121` is the only call site inside an increment:

```python
chosen = scope.scoped(listed, owned=owned, limit=limit)
```

`increment` receives a `WatermarkStore` at `src/cratekit/sync/run.py:100`. It does not hand that store to `scoped`. It lists, scopes, processes, and only then, after a clean completion with no errors, advances the cursor. The advance is at `src/cratekit/sync/run.py:152`.

`src/cratekit/sync/watermarks.py:3` records the same split on the store itself: a cursor is a record of how far a source got, not a floor the next increment filters by. `WatermarkStore.advance` says callers must not call this on a shortfall.

A total listing failure does not return an empty catalogue. `src/cratekit/sync/run.py:111` catches `LookupFailure` and raises `sync-source-lookups-failed`. The registry comment at `src/cratekit/core/cause.py:1097` states why: the source system treated that empty list as "nothing new" and advanced a watermark over a playlist that had never been read.

The landed tests name the mechanism, not the brief's noun. `tests/test_incremental_sync.py:158`, `test_a_rerun_after_a_clean_sync_processes_only_unowned_items`, is the brief scenario. A first increment takes `old` and `mid`. The second increment is given those identities as `owned` and a list that also contains `new`. It processes only `new`. The watermark is read after the first run to prove it advanced. It is not an input to the second run's scope.

`tests/test_incremental_sync.py:198`, `test_a_watermark_does_not_empty_the_scope_of_unowned_items`, is the test that would go red if someone later implemented the brief literally. It advances a cursor to `"zzz"`, lists two older unowned items, calls `increment`, and expects both processed. A date floor, a string floor, or any "newer than the cursor" filter would drop them and the run would look empty.

DJ_tools already paid for this shape twice, and KTD11 names both halves. One half is a date floor: a year floor on a favorite-label crawl excluded every track the crawl surfaced, so zero in scope looked like "nothing new". That removal is recorded in the DJ_tools favorite-label recency sweep design note. The other half is a total listing failure that returned empty and then treated the source as taken. Those are different incidents with the same silent empty-run shape.

The reengineering plan records the lesson in two places that are easy to mix: plan requirement R25 (each source is its own job, the watermark advances only on clean completion, a partial or empty result leaves it unchanged and reports the shortfall), and KTD11 (the watermark is not a scope input). The plan names DJ_tools issue #14 as "the watermark bypass" whose lesson is encoded in R25. That issue is the still-open failure where a manual label import does not advance `last_pulled`. It is not the date-floor incident. Do not collapse them.

Cratekit did not previously ship a date-floor `scoped()`. U22 encodes the DJ_tools lesson so the floor is not rebuilt here.

Do not confuse plan R25 with residual finding R-25. Residual R-25 in `docs/residual-findings.md` is about a review-queue countdown. Plan R25 is the incremental-sync requirement. They share a number because they live in different registers.

## Guidance

Separate the outcome from the mechanism before you write a line. A brief sentence and a KTD that look like they disagree are usually answering two different questions.

- The brief's test scenario names what a person watching the second run should see: already taken items do not come through again.
- The KTD names how that happens: most recent N, minus what is owned. The watermark is written afterwards, as an audit of a clean completion.

When those two sentences collide, implement the outcome through the KTD's inputs. Do not promote the brief's noun into a parameter.

A KTD outranks a test-scenario noun. `CLAUDE.md` says the issue is the brief, and that is still true. The issue is a copy of the plan unit. The plan unit is governed by the KTD it cites. The sibling DJ_tools seam-decisions document remains authoritative over any brief. KTD11 itself lives in the reengineering plan, not in that seam file. A test scenario that names the watermark as a filter is not a license to ignore the KTD.

The tell is that the brief uses the watermark as a subject of a filter verb. "Newer than each watermark." "New since each source's watermark." Those describe the second run's visible set. They do not add a fourth argument to `scoped()`.

The wrong implementation is a date floor, and it is already a named bug. Filtering candidates by cursor, by `last_pulled`, by year, or by "recency greater than the stored mark" rebuilds the silent empty run. An empty scope looks like a successful "nothing new". A watermark that advances over that empty result marks the source swept. A playlist, a label, or a favorites list is then treated as fully taken with zero tracks. That is the failure KTD11 exists to keep out.

The right second test is the one that would fail the brief's literal reading. U22 planted `test_a_watermark_does_not_empty_the_scope_of_unowned_items` after the outcome test. A green suite that only has the outcome test cannot see the date-floor regression.

Rename the test to the mechanism when you land it. The brief said "newer than each watermark". The landed name is "processes only unowned items". That rename is the resolution, written where the next session will look first.

A later unit that describes incremental sync will copy the brief's noun if you let it. `src/cratekit/write/rebuild.py` currently says incremental sync's scope is a watermark plus deduplication against what the library already owns. That sentence is the brief's wording, not `scoped()`'s signature. Rebuild is right that incremental sync cannot repair an out of band restore. It is wrong about why. The files still read as owned, so owned dedup drops them. The watermark is not in that decision.

"Watermark" is not one concept in this repository. A deletion watermark is a sequence floor. Moving that floor backwards would re-present removals a person has already answered. U24 is allowed to filter removals by that floor. U22 is not allowed to filter increment scope by its cursor. Same English word, two jobs.

A total-failure path that returns empty is the same class as a date floor. Both produce a silent zero-scope run. KTD11 names both halves: the watermark is not a filter, and a listing failure raises.

When you are stuck between two sentences, write the resolution into the call signature. `scoped()` takes no watermark. That is stronger than a comment. A future session that tries to "fix" the brief by adding a cursor argument has to change the signature, the only call site, and the adversarial test together.

## Why This Matters

The literal reading is the cheaper one, and it rebuilds a bug that already marked a playlist fully taken with zero tracks.

A session starting from `board.py show` on U22 sees the test scenario first. The scenario is short, concrete, and sounds like a filter. KTD11 is a paragraph in a different repository's plan. The issue is supposed to be sufficient. The sufficient-looking sentence is the one that is wrong as an implementation instruction.

The failure is silent. A date floor that drops every listed item does not raise. It returns an empty chosen set. `increment` then reports `shortfall="empty"` and leaves the watermark unmoved. Or, if the implementation also "fixes" the shortfall so a successful nothing-new can advance, it writes a cursor over a source that was never read. The first shape looks like a clean idle run. The second shape is the historical defect.

DJ_tools learned the date-floor half on a real crawl. A year floor against Strictly Rhythm excluded every track the crawl surfaced. Zero in scope looked like "nothing new". The replacement was most recent N plus owned dedup, with `last_pulled` kept only as an informational last-swept record. Cratekit's KTD11 is that lesson promoted into a plan decision so U22 cannot put the floor back. Implementing U22 as a cursor filter would spend the lesson a second time, in the unit that exists to encode it.

Every later source unit (labels in U26, favorites, playlists) will reread the brief's sentences. If this convention is not written down, each of those units is a fresh chance to put the cursor back into the filter.

## When to Apply

Apply this whenever a unit brief, an acceptance example, or a workflow step names a stored cursor as the thing that decides the next run's work, and a KTD, a residual, or a design record says that cursor is an audit.

Concretely, stop and resolve when:

- A test scenario says "newer than", "since", or "after" a watermark, a `last_pulled`, or any cursor. Ask whether the user visible set can be produced by owned dedup without reading that cursor. If it can, the brief is describing the outcome.
- You are about to add a watermark, cursor, or floor argument to a scope function. Read `src/cratekit/sync/scope.py:21` first. If the function you are editing is sync scope, the argument is the bug.
- You are writing the test that matches a brief sentence. Name the test after the mechanism. Add a second test that would fail the brief's literal reading. U22's pair at `tests/test_incremental_sync.py:158` and `:198` is the template.
- A later unit describes incremental sync in passing. Read `src/cratekit/sync/run.py`, not the plan's AE7 sentence, and not the rebuild module's opening comment.
- A listing failure is about to return an empty list. That is the other half of KTD11. Raise. An empty list is a verified empty catalogue, not a dead provider.
- Two documents share a number across registers. Plan R25 is not residual R-25. Look the identifier up in the register the sentence came from.

Do not apply this as a reason to ignore briefs. The outcome in the U22 scenario is required. A second run that re-processes already taken items is also a defect. The correction is to produce that outcome with owned dedup, then write the watermark as the audit of the clean run.

Do not apply this to deletion. U24's watermark is a contiguous sequence floor. Filtering removals by that floor is the design. Sync scope and deletion scope share a word and do not share a rule.

Do not apply this as a reason to delete the watermark. Status reads the record. Restore replaces the coupled file with the rest of the library-scoped set. The shortfall path needs the rule that empty does not advance. KTD11 forbids using that record as a filter. It does not forbid keeping the record.

## Examples

All commits below sit on `main`. This project uses no pull requests.

**The two sentences, side by side.** From the reengineering plan.

KTD11, `:399`:

> Watermarks are audit records that gate nothing on their own. Scope comes from most-recent-N plus dedup against what is owned.

U22 test scenario, `:1209`:

> A re-run after a clean sync processes only items newer than each watermark.

The first names inputs: candidates, owned, limit. The second names a visible set and attributes it to the watermark. The landed resolution is that the visible set is true and the attribution is not.

**The call that settles it.** `src/cratekit/sync/run.py:121` at `dc830ef`:

```python
chosen = scope.scoped(listed, owned=owned, limit=limit)
```

`watermarks` is in `increment`'s signature and is not an argument here. The store is used after process succeeded and after the intake file was appended.

**The outcome test, renamed to the mechanism.** `tests/test_incremental_sync.py:158`. First run takes `old` and `mid` with an empty owned set. Second run is given those identities as owned and a listing of `new`, `old`, `mid`. Asserts only `new` is processed. The watermark is checked only to prove the first run advanced.

**The adversarial test the brief cannot write.** `tests/test_incremental_sync.py:198` advances a cursor to `"zzz"`, lists two older unowned items, and expects both through `increment`. A filter on `"zzz"` would produce the silent empty run.

**The raise, not the empty list.** `src/cratekit/sync/run.py:111` and `tests/test_incremental_sync.py:110`. A `LookupFailure` becomes `sync-source-lookups-failed`. The watermark for that source stays unset.

**The first time this was removed.** DJ_tools, recorded in that repo's favorite-label recency sweep design note. After the year floor was removed there, `last_pulled` no longer drives scope. Cratekit's KTD11 is that result, written as a seam so U22 cannot put the floor back.

**The same noun, the other job.** Deletion. `src/cratekit/deletion/watermark.py` uses a floor as a lower bound on purpose. A sync session that "fixed" U22 by copying deletion's floor into `scoped()` would be applying the right rule to the wrong surface.

**The leak after the unit landed.** `src/cratekit/write/rebuild.py` still says incremental sync's scope is a watermark plus dedup. The conclusion (rebuild, not increment, repairs an out of band restore) is right. The scope sentence is the U22 brief, not `scope.scoped`. A session that learns sync from rebuild will reintroduce the floor to make the comment true.

## Related

- The sibling DJ_tools favorite-label recency sweep design note, the first removal of a scope-driving `last_pulled` date floor.
- The sibling DJ_tools reengineering plan: KTD11, plan R25, U22, AE7, and DJ_tools issue #14 named as the watermark bypass.
- `docs/residual-findings.md` R-130, the accepted leftover that U22 queued the engine and did not yet drive a real source. Later source units reread this convention.
- `src/cratekit/sync/scope.py`, `src/cratekit/sync/run.py`, `src/cratekit/sync/watermarks.py`, `tests/test_incremental_sync.py`, the landed resolution at `dc830ef` on `main`.
