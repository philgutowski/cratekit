---
title: A pass stopped by one file every catalogue refused and another no catalogue could reach explains only the refusal
found: at the review of #790, U284, 2026-11-13.
issue: no
---

**The mechanism.** A sweep with no Discogs token where one file meets
Beatport's refusal and another a Beatport timeout fails both items. The
sweep's report lists the first under `refusal_stop` and the tail adds its
words and steps to the pass's stop; the second is counted in the job's
"failed 2" and explained nowhere on the pass's stop, which carries no network
step for it. Before U284 the pass's stop carried no network step either: the
job's own refusal counts its failures, and the network step lives only on each
item's cause.

**Measured cost.** Driven at review round one (probe P1 in the reviewer's
scratch copy): the stop names a.flac as refused and says nothing of b.flac's
outage. Nothing false is said; a person reading the item causes or `job show`
learns the outage.

**Closes when:** the pass's stop at its tag step names the files no catalogue
could be read for, with the network step, beside those every catalogue
refused. Ledger only.
