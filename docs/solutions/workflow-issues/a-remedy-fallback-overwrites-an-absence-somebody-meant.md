---
title: "A remedy fallback overwrites an absence somebody meant, and a test named for an invariant can pass without asserting it"
date: 2026-09-09
category: workflow-issues
module: "src/cratekit/acquire/cli.py, src/cratekit/acquire/adapter.py, src/cratekit/core/cause.py"
problem_type: workflow_issue
component: cause
severity: high
root_cause: unverified_assumption
applies_when:
  - "A shell translates another layer's optional field into its own vocabulary and supplies a fallback for the absent case"
  - "A producer leaves a remedy, a remediation or a hint off deliberately because there is nothing for the person to do"
  - "A refusal builder picks its fallback with a conditional over an outcome enum"
  - "A test is named for an invariant and asserts the fields around it"
symptoms:
  - "A refusal tells somebody to weaken a policy over a condition that policy has nothing to do with"
  - "A named test passes over the exact defect its name describes"
  - "A fallback fires for an outcome nobody had in mind when the conditional was written"
related_components:
  - "cause"
  - "acquire"
  - "adapter"
tags:
  - "remedy"
  - "fallback"
  - "absence-as-evidence"
  - "test-naming"
  - "first-caller"
---

# A remedy fallback overwrites an absence somebody meant, and a test named for an invariant can pass without asserting it

## Context

U54 bound the acquisition worker, so `acquire/cli.py` became the first thing in
the product to read a `TrackResult` and turn it into an item's row. Each of the
adapter's outcomes had to become a cause with a reason and a remedy, and the
adapter's remedy field is optional.

## What happened

The translation read:

    remedy=_remedy(result.remedy, Remedy.RETRY_LATER if transient else Remedy.RELAX_LOSSLESS_POLICY)

which is correct for the two outcomes the author had in mind. `transient` is
true for `UNAVAILABLE_TRANSIENT`; the non transient side was written for
`REFUSED_BY_POLICY`, where relaxing the policy genuinely is the answer. But a
`REFUSED_BY_POLICY` result always carries its own remedy, which the
`TrackResult` validator enforces, so it never reaches the fallback at all. The
only outcome that can reach it is `UNAVAILABLE_PERMANENT`, and
`adapter._unavailable` leaves the remedy off that one ON PURPOSE, because there
is nothing a person can do about a track the provider no longer has.

So the one outcome the fallback ever fired for was the one whose remedy was
deliberately absent, and a delisted track told the person to relax the
product's central promise.

The test over that path was called
`test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`.
It asserted the reason and the retryable flag. It did not assert the remedy. It
passed, green, for the whole unit, over the defect in its own name.

## Why the source does not explain it

Nothing at the raise site looks wrong. The conditional is readable, both
branches name a plausible remedy, and the absent case is visibly handled rather
than forgotten. The defect is only visible by asking which outcomes can
actually REACH each branch, which means reading the producer's validator, one
module away, to learn that one of the two branches is dead.

## The rule

**A fallback for an absent optional field must be justified by the producer's
reason for leaving it absent, not by the consumer's need to have something
there.** When the producer omits a field deliberately, pass the absence on and
let the default that the whole class of failure already declares answer it. A
fallback parameter that cannot be `None` is a fallback that cannot express "the
right answer here is nothing".

And the second half, which is what let it live: **a test named for an invariant
must assert that invariant.** The name is a claim about coverage, and it is
read as one at every later review. Asserting the fields around it is worse than
having no test, because it spends the name.

## The test that holds it

    assert item.cause.remediation.remedy != Remedy.RELAX_LOSSLESS_POLICY
    assert item.cause.remediation.remedy is Remedy.CHANGE_POLICY_OR_INPUT

Both lines, not just the first: the negative pins the harm and the positive
pins that the reason table's own default is what answered.

## Where else this applies

Every place a shell translates an adapter's or an engine's optional field into
a cause. `_remedy` in the same file is now typed to take `Remedy | None`, which
is what makes the honest answer expressible at the other call sites too.

The reachability question generalises past remedies: a conditional over an enum
whose branches were written for the outcomes in mind is worth re-reading
against the outcomes that can actually arrive, and the producer's validator is
where that is settled.

## See also

- METHOD's first recurring defect pattern, absence read as evidence of absence.
  This is its inverse and the same root: an absence that carried information,
  overwritten by a consumer that assumed it carried none.
- R-292, the gap the same fix round left open on purpose, where a probe that
  cannot read a file answers nothing and the code declines to invent an answer.
