# Concepts

Shared domain vocabulary for this project: entities, named processes, and status
concepts with project-specific meaning. Seeded with core domain vocabulary, then
accretes as units file learnings in `docs/solutions/`; direct edits are
fine. Glossary only, not a spec or catch-all.

## The build

### Unit
A numbered increment of the build, specified by its own issue and delivered on
its own branch. The unit is the atom of this project: work is picked as a unit,
verified as a unit, and merged as a unit, and a unit's issue is its full brief
rather than a pointer to one.

A unit's number and its issue number are not guaranteed to match, so the issue is
looked up rather than assumed. Units declare dependencies on other units, and
those declarations are the only input to whether a unit is ready.

### Board
The queue that says which unit to take next. Ready and blocked are derived values,
computed from unit dependencies and issue closure rather than set by hand, so the
board is recomputed rather than remembered. Ranking is by how much of the
remaining build a unit releases, counted transitively, so a unit whose single
dependent gates a whole phase outranks one with several dead end dependents.

That transitive count currently reaches through every open issue a dependency
edge leads to, not only units. A residual or an attended item that names a unit
as what it closes still counts toward that unit's rank, even though neither is
board work by the paragraph below. So a unit's ranked position is not yet a pure
measure of build released.

Ready and blocked being derived from a unit's own declared dependencies cuts
both ways. It is what keeps the board from being hand maintained, and it is
also the board's one blind spot: a unit whose declared dependencies are all
closed derives as ready even when its own verification depends on a unit that
was never added to that declaration. The derived state cannot catch that, by
construction, since a declaration is the only input it has. The check that
catches it is reading the unit's own written verification criteria for a
blocker its dependency list does not name, not trusting the derived ready or
blocked state.

Ready is silent about who may perform the work, which is a second blind spot and
not the same one. A unit that only a person can carry out, because it has to run
against the live library, derives as ready like any other once its dependencies
close, and the queue then recommends it. The status vocabulary does have a
separate attended state, but a unit reaches that state by carrying the attended
label rather than by being attended in fact, so an attended unit nobody labelled
is indistinguishable from available work. A ready queue holding nothing takeable
is therefore not a statement that the build is finished, and the register of
known and accepted problems is where the rest of that answer lives.

WHAT BELONGS ON IT is a separate question from how it derives, and the two were
confused for weeks. The board carries WORK: units, and the attended chores that are
somebody's to do. It does not carry the register of known and accepted problems,
which is a ledger rather than a queue, so a residual finding earns a place here
only when somebody decides to act on it. Mirroring the ledger onto the board would
assert intent that does not exist and would swamp the few items genuinely ready.

Two failure states are distinct and are not repaired the same way. Drift is a
derived value that fell out of date, and is repaired by recomputing it.
Contradiction is the board and the repository disagreeing about whether work
landed, and is never repaired automatically, because doing so means choosing one
source of truth to overwrite silently.

### Coordination note
A warning written into source on one branch, addressed to whoever performs a
future merge, about a collision no tool will report. It exists for the case where
two branches each change the same thing correctly and both merge cleanly, so the
only thing that can raise the alarm is a person who saw it coming.

It is the unenforced counterpart of the pending register, and the difference
decides which to reach for: a register entry is an obligation the suite fails on,
while a note is prose whose claim no check evaluates. So a note has no expiry, no owner,
and no way to go red, and it is written in the present tense about a branch its
author cannot run and often has not read. Its instruction and the fact that
instruction rests on are separate claims with separate lifetimes, and the fact
may have been unmeasured from the moment it was written, so a reader obeys the
warning and re-measures the fact. A note whose fact was actually checked says so.
A note that survives the merge it was written for is corrected or deleted,
because it has stopped describing anything that exists. Notes come in pairs more
often than their authors realize, since each side of a collision has its own
reason to write one, so a merge reads both branches' records rather than only the
one it is standing on.

### Board bar
The test a residual finding has to pass to earn an issue, decided 2026-09-18. A
finding passes when it is open and a person using the shipped verbs pays for it
in one of four ways: data can be lost, the product says something false, a
workflow cannot finish, or a guard on a path that writes or deletes is absent.
Everything else stays in the ledger with no card. It exists because the board
is the queue, so a finding that matters and has no card is a finding nobody
does, and because a ledger of four hundred entries put on the board whole would
claim an intention to do four hundred things. The session that files a residual
applies the bar and files the card itself.

### Feeder
The loop that keeps a native Relay run continuous. Relay reads its manifest once
per run, so the feeder appends a few ready board cards to the manifest, runs it,
reads the summary and repeats. It lives beside the manifest in `~/.relay`, never
in this repository. "Ready" is the board's derivation and not the feeder's
opinion, which is what stops a unit launching before the units it depends on
have landed. It excludes a task that halts twice and waits out a cycle in which
every task died within minutes, which is what a usage limit looks like.

### Name claim
How the contract test in `tests/test_cli_contract.py` decides a source entry
point is ported: some registry entry names it in `source_scripts`. A claim by
name says nothing about which half of that script's behaviour landed, which is
how `sync.favorites` claimed `dj-favorites` while performing one direction of
it, and how a board could read complete while no acquisition workflow finished.
A name claim is evidence that a verb exists. It is not evidence that a workflow
ends.

## Acquisition

### Adapter
A boundary component that wraps exactly one download tool or streaming
provider behind a declared contract, so a different tool can be substituted
through configuration alone when a provider integration breaks. The contract
exists because no third-party tool is guaranteed to keep working: an adapter
promises an exhaustive, typed outcome at two scales rather than an exit code a
caller has to interpret, per track, exactly one of acquired, permanently
unavailable, transiently unavailable, or refused by policy; per invocation,
exactly one of ok, authentication failed, or broken.

An adapter's lifecycle is authenticate once, then per track offer, apply
policy, fetch, pace. Authenticating establishes a session; it is a separate
fact from whether that session is then served what was actually requested, and
an adapter's own settings check confirms only the request, never the artifact
the wrapped tool produced from it.

### Searcher
A boundary component that answers "what genre is this track" from a public
music catalogue, injected into the tagging engines so the suite can prove the
write path with no network. It reports exactly one of four outcomes per
source: matched, answered with no match, unreachable, or parsed to no
recognizable shape. Only the second is a miss. The third keeps a catalogue
that was down from reading as a catalogue that has never heard of the track,
and the fourth keeps a scraper whose target page moved from reading as a
network problem, which is a permanent state wearing a transient remedy. A
searcher no source answered refuses rather than declining, so a job cannot
report a clean sweep over answers it never got. A decline is a question the
next run asks again; a refusal fails that one item and leaves the job
resumable.

### Landing
The step between a download and a rekordbox import: moving a batch of acquired
files out of download staging into `Music/<batch>/` and splicing them into one
intake file. Staging is deliberately invisible to ownership, which walks the
music directory only, so an acquired file that has not landed still reads as
missing and would be offered for download again. R-413 records that the step did
not exist. U71 built its engine, `intake/landing.py`, and the verb is still owed.

### List document
The one file format `acquire download` reads: a versioned, closed document of
provider track identifiers, read by `match_cli.read_list` and nothing else. Until
Phase G nothing in the product wrote one, which is R-400. One shared emitter,
`acquire/listdoc.py` since U68, writes it, and what each identifier came from, a
playlist, a label and year, a sync run, rides a sidecar manifest beside it
because the document's own keys are closed. A row with no provider identifier
is never written into it and comes back as unlisted.

### Provider candidate
A track the provider's text search returned for a missing row that nothing
names exactly, since U79. A candidate is a PROPOSAL and never a pick. It is
EXACT when it folds to the row in artist, title and version under `match`'s own
fold, and a row is listed without a person only on one distinct exact
candidate, in an answer that was read whole, was shorter than the seam's page,
and answered a title that reads one way. Anything else is offered as a review
item of kind `provider-candidate` on the `version-match` queue, keyed on the
folded row, and `crate intake missing --list` lists the accepted one on its
next run. A candidate's score orders the screen and never lists anything.

### Fallback candidate
An upload on a second source, SoundCloud or YouTube, that `crate acquire
fallback` found for a missing row the configured provider has no route to,
since U80. Offered as a review item of kind `fallback-candidate` on the
`fallback-source` queue, keyed on the same folded row a provider candidate is,
one option per upload page URL, ranked by a score that orders the screen and
drops nothing. It is never picked and, until R-404's download half lands,
never downloaded. A row with a provider route, its own provider id or a
provider candidate waiting or accepted, is not searched for one.

### Hearts reference
The reserved word `favorites` in place of a playlist reference, since U70:
`crate intake playlist favorites` lists every track hearted on the account and
resolves each against the library as owned, offered or missing, exactly as a
playlist's tracks are. It cannot shadow a real playlist, because a playlist
reference is only ever an identifier or a URL. It is the inbound direction of
favourites. The outbound direction, hearting local favourites on the account, is
`crate sync favorites`. Unlike the source system, it parks nothing in a
placeholder playlist: a heart the library lacks is a missing item carrying its
provider identifier.

## Verification

### Guard
A test that enforces a standing constraint rather than exercising a feature.
Guards exist to make a class of violation impossible to introduce silently, which
is why some are written before the code they govern: a guard that arrives after
its subject can only confirm what already shipped.

Some guards assert a BEHAVIOUR and some assert an ARGUMENT, and the second kind
behaves differently enough to be worth separating. An argument asserting guard
carries a claim in prose about what some part of the system can reach or do, and
enforces that claim mechanically. Such a guard is more valuable than a behavioural
one because the claim is falsifiable, and it is also the only kind that can be
falsified by somebody who never read it: any change that gives a new capability
to anything the claim covers can make the sentence untrue, from a different unit,
in a different file, with every suite still green. That failure is a property of
the combined tree rather than of either contributing change, so nothing short of
the combination can observe it.

A third axis cuts across both kinds: whether the guard consults the real subject
or a hand rolled model of it. A guard that hands its input to the component that
owns the answer, the parser, the loader, the dispatcher, cannot disagree with
that component. A guard that reimplements the component's rules is a second
implementation of the same semantics, and it will drift, silently, because its
own fixtures were written from the same model and can only ever confirm it. The
drift is not in the rules the author wrote, it is in the rules the author never
knew were there, and a model's silence produces no failing test. Deriving the SET
a guard quantifies over is a separate question from deriving its JUDGMENT, and
satisfying the first says nothing about the second.

A fourth axis is what the assertion OBSERVES, and it decides whether a guard
holds anything at all. An assertion pins an observation and not the mechanism
that produced it, so where several code paths reach the same observable value the
guard is satisfied by all of them and distinguishes none. An absence is the
value most exposed to this, because refusing early, refusing late, and never
arriving all look alike from the end of the pipeline. The repair is to assert
where the thing was stopped rather than only that it is missing: name the
register that caught it when the correct behaviour leaves a trace, and require
every parallel register to be empty when it leaves none. A result carrying
several registers is the warning sign, since zeroing one says nothing about its
siblings.

A fifth axis is what the FIXTURE can reach, and it sits underneath the fourth. An
assertion can be well aimed and still hold nothing when the inputs it runs on never
put the system into the state the claim is about, because a guard distinguishes only
the behaviours its fixture can provoke. The tell is that such a guard fails RED on
correct code before it is ever green, which is indistinguishable from an ordinary
wrong expectation, and the ordinary repair converts it into a characterization. The
remedies are to place the fixture where the code that writes the thing places it,
and to assert the fixture's own precondition inside the test, so a fixture that
later shrinks below the bound it was sized for reports instead of passing.

A sixth axis is whether the guard was ever in a POSITION to fail, and it is the
one the five above can all be satisfied while missing. Three things put a guard
outside that position. The first is a subject that does not exist: a guard naming
a thing the project has not built yet asserts something about an absence the
project is guaranteeing for it, so it passes on a fact about what has not been
written rather than on the property it claims, and it goes on doing so until the
day that thing lands. The second is ambient state the process already holds. A
guard that compares a snapshot before an action against a snapshot after it can
only distinguish anything if the action could still change that state, and a
process wide cache which everything running earlier has already filled cannot
change again. The third is a second, correct guard standing between the entry
point under test and the value, deciding the identical condition the value
depends on. Unlike the first two, this cause is POSITIONAL rather than global:
the value can still differ somewhere in the system, just not from the entry
point being driven, because the intervening guard has already turned every
input that would separate the two outcomes into an early exit before the value
is ever computed from it. The tell is the same condition appearing twice in one
call path, once as a raise-or-continue decision and once as a value read
downstream of it; reading the two side by side, rather than assuming a guard and
a value it precedes are unrelated concerns, is what surfaces it. Restating such
a guard as a difference is the natural repair for the first problem and no
repair at all for the second or third, so all three are worth separating: a
difference is a measurement only where the thing could have differed, and an
entry point is a measurement only where the intervening guard has not already
decided it.

The remedy differs by which one applies. A named subject that has not landed
either goes in the pending register, where it is a countdown, or is replaced by a
subject derived from the tree, so no unbuilt name appears in the guard at all.
Ambient state is answered by moving the measurement into the state the claim is
actually about, which usually means a fresh process rather than one the suite has
already warmed, because the state a claim describes and the state a suite runs in
are different worlds and an assertion evaluated in the second is not evidence
about the first. A positional foreclosure is answered by moving the measurement
to an entry point below the intervening guard, where the excluded input space is
still reachable; when no such entry point exists anywhere in the tree, the value
is unreachable-as-false everywhere the guard runs, which is a finding about the
design rather than a gap in the guard, and is recorded rather than chased.

When such a guard offers remedies for its own failure, the remedies are driven
rather than reasoned about, and a remedy that makes the guard report MORE is
propagating rather than converging. When every offered remedy terminates in
breaking something else, that is a finding about the design and never a licence
to widen the guard so it accepts what it was written to catch. That last rule
governs a guard that is a faithful checker. A guard that reimplements its subject
is a third state, neither correct nor merely too narrow, and replacing it with
the real thing is not the forbidden widening.

### Layer
A rank assigned to every module, from the foundation up through the CLI, that a
dependency-direction guard enforces in two independent ways: an import may only
point to its own layer or a lower one, and separately, a lower layer may not
name a higher layer's vocabulary as a string either, because a string handed to
a dynamic import is the same upward dependency the import rule forbids, just
invisible to an import-graph walk.

*Avoid:* treating the string-naming rule as redundant with the import rule, or
as a loophole the import rule leaves open. They are independent checks enforced
by independent logic; a table built to dodge the import rule by holding its
targets as plain strings still trips the naming rule when those strings are a
verb name or a feature-module package name, and a fix that satisfies one does
not satisfy the other.

### Beat grid
The rekordbox-authored timing map for a track. This product never writes one. A
wrong grid is worse than no grid, because a folded tempo moves every cue and
loop the user has set.

A mapping that carries the tag spelling of tempo is treated as a write, even
when it never reaches a file. The domain word may live on an attribute. The
serialized key may not.

### Analysis share
The `share` directory beside the rekordbox database, where every track's
analysis files and beat grids live. On an external volume it is
`PIONEER/Master/share`. `AnalysisDataPath` is stored relative to it, so
`core.analysis_store` is the one place that joins the two. Not to be confused
with `PIONEER/USBANLZ` at the volume root, which is the USB export cache: a
different key shape, regenerable, and no row resolves into it. A database
outside the library root takes its share with it.

### Pending register
The one declaration of guards whose subject does not exist yet. Each entry names
the missing thing, the unit that will land it, and what the guard behind it
asserts. It exists so that a guard written early is a countdown rather than a
hole, and so that no such gate can be created anywhere else.

An entry is an obligation with an expiry, not an exemption. When the unit lands
the subject, a meta test fails on purpose, and discharging it means removing the
entry, removing its mirrored copy in the meta suite's expected set, and removing
the gating decorator from every guard the entry covered. Removing the entry alone
does not arm the guard: the gate helper refuses an undeclared key at import time,
which takes the guard's entire file out of test collection. A full run then stops
outright and executes nothing, so the loss reads as ordinary only to a run told to
continue past collection errors, to a subset run that never names the affected
file, or to a comparison of collected totals rather than identifiers. An entry
that no guard actually cites gates nothing, and is an unenforced countdown wearing
the costume of an enforced one. A future obligation that cannot be stated as a
missing thing the suite can name is not a register entry at all and belongs in a
coordination note, which is the weaker instrument on purpose.

The register covers only what was registered, and nothing detects the guard that
should have used it and did not. A guard naming a subject that has not landed,
written without an entry, is not a countdown and is not visible as a hole: it
simply passes, for as long as the subject is missing, and its first failure is
the day somebody lands that subject. So the register's coverage is a fact about
author discipline rather than a property the suite enforces, and a guard that
names any unbuilt thing is the moment to reach for it.

### Planned verb
A command the registry names before the module that implements it exists. The
name is in the table so the whole surface can be checked before every unit has
shipped. The marker does not clear itself: a countdown fails the moment that
module is importable, and that failure is the signal to remove the marker that
has been keeping the verb out of the running command tree.

The expiry key is the module string already written on the verb, not a
directory a brief listed. A package that appears under a different path
does not make the verb importable, so the countdown stays green and the
command never enters the running tree.

A planned verb whose first typed word is already a one-word command cannot enter
the running tree as written: the parser treats that word as a finished command,
not as a group that can grow a child. The name has to change before the marker
clears, because clearing the marker is what puts the verb in front of the parser.

### Battery
The fixed set of checks that must all be clean before anything merges. It is one
named gate rather than a list assembled per change, so asking whether the battery
was run has a single unambiguous answer. An author running their own battery is
not a review: every defect the adversarial reviews have found here passed a green
suite written by the person who wrote the defect.

What it checks is code, imports and repository structure. One of its parts does
read prose, hunting machine specific paths and secrets in any text it finds, but
nothing in it evaluates whether a sentence is TRUE. So any claim made in prose is
outside the battery entirely, whether it sits in a comment, a docstring, or the
instruction files a session reads before it starts, the session contract among
them. That is the property a coordination note depends on and suffers from, and it
is what lets a confident sentence about the project's own state stay wrong
indefinitely while every check stays green.

The battery is the merge gate and continuous integration is not. Integration
runs on a hosted machine that lacks the hardware and tools the suite proves
things against, so a check that cannot pass there says nothing when it fails
there. Integration is confined to what it can actually establish, that the
package installs and imports cleanly on each supported interpreter and that no
personal path or secret reached the tree, and it does not run the suite. Nothing
in it is skipped or deselected, because a skipped proof reads as a passing one.

The battery is unconditional and is a separate question from whether any
particular finding blocks. Whether a finding blocks on its own merits is decided
by the conditions under Blocking finding; whether a tree may merge at all is
decided here, and nothing overrides it. The two are independent, so a finding can
be a residual and still stop a merge, and the reason a merge stopped is stated
alongside the finding's classification rather than inferred from it.

### Mutation table
A measurement of whether the suite would notice the code breaking. Each row
reverts one guard, runs the tests, and counts how many fail, and that count is the
guard's death count. A guard whose removal kills nothing is untested whatever the
coverage report says, because coverage measures which lines ran and this measures
which lines mattered.

That reading carries an unstated premise, that the revert produced a tree which
behaves differently, and a row where it does not is INERT. An inert row is not a
failed measurement, it is not a measurement: deleting an argument whose value
equals the callee's own default, swapping a constant for another name bound to the
same value, and reordering operations that commute all leave the two trees
behaving identically, so the zero is correct and says nothing about any guard.
A real zero and an inert one render the same and are told apart only by reading
the mutated site, never by counting. They also want opposite fixes, since a real zero
is answered with a test and an inert one can only be answered with a better
mutation, because no test can distinguish two trees that behave the same.

There is a THIRD cause, and it is the one that looks least like a problem. The
two trees behave differently, a guard for the property exists, it runs, and it
still kills nothing, because the value its assertion observes is one both trees
produce by different routes. The commonest shape is an assertion on an absence,
an empty collection, a count of zero, a field left unchanged, since many paths
arrive at the same nothing and a mutation only has to reach one of the others.
This cause is separated from the first two by reading the ASSERTION rather than
the mutated site, and it is answered by strengthening the existing guard rather
than by writing a new one or a better mutation. Being able to state the assertion
that would kill a row proves the row is not inert; it does not prove the
assertion discriminates.

There is a FOURTH cause, and it sits underneath the third rather than beside it.
The two trees behave differently, a guard exists, its assertion is well aimed, and
the row still kills nothing because the FIXTURE never puts the system into the
state where the mutated line could change anything. It is separated from the third
by reading the FIXTURE rather than the assertion, and it has two spellings: a value
placed where the code under test cannot reach it, so its presence and absence read
the same, and a population smaller than the bound under test, so a limit holds
whether or not it is applied. A guard written for such a row fails RED on correct
code first, which is the trap, because the ordinary repair for a red assertion is
to expect whatever the code produced, and on such a fixture that value is the only
value any tree produces. It is answered by moving the fixture to where the code
that writes the thing puts it, and then by a row that mutates what the FIXTURE
depends on rather than what the guard covers, since only that row can falsify the
guard itself. A table measures what its fixtures can observe, so independence of
the reviewer does not reach this one: an independent reviewer writes rows against
the same fixtures.

There is a FIFTH cause, and it is not a diagnostic signature at all, it is how a
plain real zero gets made and mistaken for closed. The row is not inert, no
assertion anywhere aims at the property, and the fixture was always capable of
reaching the state that would kill it. What happened is that a new guard broke
an EXISTING test's stand-in, and the stand-in was edited just enough to satisfy
the guard's precondition rather than to exercise it, so the old test goes back
to green. The edit reads as coverage, because a test that reaches the guarded
code now passes, and the read is wrong, because that test's own assertion was
never about the guard and the edit's whole purpose was defensive. It is told
apart from the third and the fourth by asking a question neither needs: is
there an assertion for this property anywhere in the suite at all, rather than
whether the one that exists is well aimed or well placed. It is answered the
way any real zero is, by writing the assertion, and the moment to write it is
the moment the fixture was edited, not later: touching a shared fixture to keep
an unrelated test green under a new guard is the signal that the guard still
owes its own test.

Reading the site is necessary and not sufficient, because the judgment is about
behaviour UNDER the mutation rather than about the line as it stands. An argument
that a row could not be killed has to say what the mutated tree does with some
input and show the original doing the same, and an argument that describes only
the original is not about the row at all, however true it is. The tempting form
of the mistake notices that a subject already equals its own rendered output
today and concludes that nothing could separate the trees, when applying the
mutation is precisely what changes that output. So a dismissal is a claim and is
driven like any finding. An author's table is a draft because an author mutates
what they believe they changed; a reviewer's reason for leaving a zero at zero is
a draft in the same way, and independence from the code buys better measurements
without buying better reasoning.

There is a SIXTH cause, and unlike the fifth it does present as an ordinary zero.
The row is not inert, an assertion for the property exists and is well aimed, and
the fixture is capable of reaching the state. What is missing is that the guard was
never in a POSITION to fail: it names a subject the project has not built, so it
passes on an absence the project is guaranteeing for it; it compares a snapshot of
state the running process already holds, so the mutation changes nothing the
snapshot can see; or a second, correct guard standing earlier in the same call
path already decides the identical condition, so the entry point under test can
never carry the input that would separate the two trees, even though the value
could still differ from a different entry point. It is told apart from the third
and fourth by asking neither whether the assertion is well aimed nor whether the
fixture can reach the state, but whether anything reachable FROM WHERE THE ROW WAS
DRIVEN could have reached the assertion differently. The remedies differ by which
cause applies and are set out under Guard's sixth axis, and the three are worth
separating because restating such a guard as a difference repairs the first,
moving the measurement to a fresh process repairs the second, and moving it below
the intervening guard repairs the third, and none of the three remedies touches
either of the other two causes.

Every batch already contains one deliberate inert row, the null control, which the
driver writes and which must kill nothing or the apparatus rather than the code is
broken. It is the concept implemented and, until it was named here, never named.

A death confirmed on a narrow subset is a real death, while a zero on a subset is
not yet a zero and is promoted to a full run before it is reported. That promotion
is what makes inertness expensive rather than merely misleading, since a row that
could not have moved still costs a whole suite. Row counts are capped by the depth
of the pass, and a truncation that nobody logged reads as coverage.

### Composite
The paired row a zero on a user facing guard owes: a second mutation aimed at the
thing the guard protects, reported beside the zero, so the pair shows what the
guard does hold rather than arguing it in prose.

It exists because a zero and an explanation are not the same evidence. A guard
whose removal kills nothing may still be load bearing, and the only way to say so
in the table's own currency is to measure the neighbouring thing and show that it
moves. A zero on a maintainer facing guard owes no composite, because such a row
can never block on its own and the pair would buy documentation rather than a
decision. The distinction between the two surfaces is therefore not cosmetic: it
decides what a zero costs to leave standing.

### Pinned population
A count the suite recomputes from the tree on every run and asserts as an exact
figure, so that a number a document argues from cannot decay silently as the
tree grows. When a merge moves it the pin fails, and the rule is to look, then
re-measure and re-pin, never to widen the assertion.

A re-pin names its members rather than matching a delta, because a member
leaving while another joins reads as no change and two joining while one leaves
reads as one joining. The comment above the pin is a dated ledger of what joined
and what left at each merge. When the members are literals in the tree, each is
asked of git against the pre-merge commit; when a walk derives them, the same
walk is run over the pre-merge tree and the two sets are differenced.

## Queued work

### Job
One unit of long running work that outlives the process that queued it. A verb
freezes the whole configuration it will run against, records the work as a job,
and reports. Nothing about the work happens at that moment. The job carries a
handler key, a frozen payload, the configuration's own bytes, and its state; it
does not carry a function.

*Avoid:* reading "the job ran" as "the work happened". A job is reported,
respawned, claimed and driven, and only the last of those does anything.

### Item
One claimable piece of a job, identified by a stable identifier the queueing verb
supplies and ordered so a resumed run walks the same sequence. The item is the
unit of work, and a handler reads the recording, folder, or track from the ITEM
rather than from the job's payload. Reading it from the payload is how every item
of a multi item job comes to do the same piece of work.

A job with no items is not an error. The driver reports it as a success over
nothing, which is exactly what a verb that queues without items produces.

### Rename intent
The record a worker writes, before it renames the file its item identifies, of
the name the file is about to take. It lives in the item's staging directory,
carries the item id and the target path, and is what a resume reads when the
item's source is missing: a target that exists is the item, finished before a
kill flipped its row, and anything else is a missing source. Introduced by U58
after a resume that guessed the finished file from the folder matched an
unrelated older file and missed a file the naming template had rewritten.

*Avoid:* recovering a missing item by scanning its folder for something that
looks like the result. The scan is the guess the intent replaces.

### Handler key
The stable string a job stores instead of a function, so a process can validate,
list, or rebuild the command line for a queued job without importing the module
that would do the work (KTD26). Every verb declares one, and for every verb it is
the verb's own name.

*Avoid:* treating a known handler key as a runnable one. Whether the build
declares a key is a question about the CLI registry; whether the build has a
FUNCTION behind it is a question about the handler table, and most declared
keys today answer yes to the first and no to the second.

### Handler
The function that does one item's work. It receives the job, the item, and the
configuration the job was frozen against, and returns what it produced or nothing.
It is declared as a `"module:function"` string and resolved lazily, at the moment
the driver needs it, which is the only import in the chain.

A handler runs against the FROZEN configuration, handed to it rather than loaded.
Loading a fresh one is the resume bug KTD9 closes, reintroduced.

### Driver
Here, the loop that claims a job's items and runs the handler against each,
taking the driver lock first, releasing an orphaned claim once, checking the
interrupt flag between items and before a commit, making an artifact durable
before the row flips to done, and recording a total failure as failed rather than
returning it as an empty success. One function owns all of that and it is not
reimplemented by callers.

*Avoid:* the other driver. `docs/METHOD.md` uses the same word for the MUTATION
driver, the script that reverts a guard at a time and counts the deaths. The two
share nothing. When either could be meant, say "the job driver" or "the mutation
driver".

## Sync

### Sync watermark
An audit record of how far one source got on a clean increment. It does not
decide what the next increment lists or keeps.

A sync watermark advances only when that source completed without error and
actually processed items. A listing that failed entirely is not an empty
catalogue, and it does not write one. Status reads the record. Restore replaces
the coupled file. Scope does not read it.

The one exception is the playlists source's record, which is a set rather than a
position: its `swept` list holds the provider ids of playlists whose intake job
succeeded, and the next pass excludes those ids. It is still never a date floor
and never a title.

*Avoid:* treating this as the deletion watermark, or as a date floor.

### Swept playlist
An account playlist the playlists source will not queue again: its name carries
the source system's `DOWNLOADED ` prefix, or its id is in the playlists record
because a job this source queued for it SUCCEEDED for this library. Queued is not
swept, and in this build swept means every track was resolved against the library,
not that any was acquired (R-359). `crate sync all` says so, as `swept_means`,
`resolved-not-acquired`, on the playlists block and as a sentence on the
`sync.playlists` check.

*Avoid:* reading swept as downloaded, or deciding it from a title.

### Owned dedup
The sync scope rule: take the newest N items the source listed, then drop any
identity the library already holds. That is how a second run processes only what
is new, without reading the sync watermark.

### Composer
A verb that queues no work of its own and queues other verbs' work through
THEIR queueing paths, under THEIR handler keys. `crate sync all` is the one
composer: it plans every enabled source, asks the one question favourites needs,
then queues each source's own job, so the workers that already run `sync labels`
and `sync favorites` run what it queues. It declares no `long_running` and no
`argv_builder`, because nothing is ever queued under its own key.

*Avoid:* a composer that spells a source's payload again. Each source owns one
`queue_sweep`, and the composer calls it.

### Inbound half
A source's read only half, declared as `inbound_key` on its spec. Favourites is
the one source with one: its outbound half hearts local favourites on the account
behind the confirmation, and its inbound half lists the account's hearts into the
library as an `intake.playlist` job. `crate sync all` queues the inbound half
whatever the confirmation's answer, because a read needs no consent a write does,
and reports it apart, as `summary.favorites.inbound` and the
`sync.favorites.inbound` check.

*Avoid:* reading `not_queued.favorites` as the whole source. It is the outbound
half's answer only.

### Hand off
Carrying a decision recorded on one run to a new run owned by another verb, so
that verb's queued job can resume. The dispatcher refuses a `--run` whose record
belongs to a different verb, so a composer cannot give a job its own run as the
gate run. `Gates.hand_off` copies the option, actor, time and digest onto a run
of the target verb, and refuses unless a digest compared decision was recorded
and the target verb declares the target gate offering that option.

*Avoid:* reading it as a way to answer a gate. It copies an answer a person gave
and never supplies one.

## Review

### Review item
A persisted, addressable question the product asks a person, never a file they
must edit. A report is an output. A review item is a decision that has to survive
a later session and a different process.

### Verdict
The stored decision on a review item: for an offered candidate, or against every
candidate. A later act that moves files or settles work reads this store. It does
not infer the decision from some other confirmation.

### Confirm gate
A recorded act that this invocation may proceed. It is not a verdict. Honouring
the gate confirms the run. It does not accept any review item.

A gate is either ordinary or explicit, and the difference is not severity, it is
how many acts answer it. An ordinary gate is answerable in the same invocation
that discovered it. An explicit gate is not.

### Explicit gate
A gate whose answer must be a separate, deliberate act recorded against the run,
never supplied in the invocation that discovered it. No blanket affirmative
satisfies one: there is no flag, no configuration key and no environment variable
that can answer it, and that absence is deliberate rather than unimplemented,
because any of those would answer every gate at once.

The behaviour that follows from this is what surprises people. Answering an
explicit gate takes two acts, so a verb declaring one refuses its first
invocation, is answered by a second command naming the run and the actor, and
proceeds only on a third invocation that continues that same run. Any invocation
that cannot name the run therefore cannot proceed, however many times it is
retried, because a fresh run carries no decision and nothing about retrying
creates one. That is the whole of why a process with no person at it, such as the
child a queued job spawns, has to inherit the run rather than start its own.

### Run
The record of one invocation that survives the process that made it, carrying the
decisions answered against it, the digest of whatever each gate offered, and
which verb created it. It is addressed by a generated identifier, and a later
invocation continues it by naming that identifier rather than by starting again.

A run belongs to the verb that created it, so a decision recorded on one run
cannot answer a gate in a different verb. Decisions are keyed by gate name and
each carries the actor who gave it, which is what makes an approval auditable
rather than merely present. The digest is recorded by the invocation that REACHED
the gate, never supplied by whoever answers it later, because that person is in
another process, never saw the artifact, and cannot be asked to quote its
identity; that recording is what makes a stale answer detectable at all.

## Findings

### Residual finding
A real defect, gap, or overclaim that is recorded rather than blocking a merge on
its own merits. Recording it with its measured cost is the point; residuals are
not deferred work items so much as the honest register of what is known and not
fixed. A residual therefore lives in that register and not on the board, which
carries work; it moves onto the board only if somebody decides to act on it.

"On its own merits" is the whole of the qualification and it is not the same as
"never stops a merge". A residual whose account the battery is red on stops the
merge through the battery, which answers a different question and admits no
exceptions.

A residual is also a verdict about the world as it stands rather than a permanent
grade. The same finding, over the same unchanged code, becomes blocking the moment
something makes its input reachable, so a residual recorded against code nothing
calls is a residual only until something calls it.

Residual numbers are append only. A number, once given, belongs to that finding
for life, and numbers already recorded never move when new ones arrive, because
the number is cited from surfaces the repository cannot see and a renumber
repoints those citations silently.

### Blocking finding
A finding that does hold a merge. It qualifies only on three conditions together:
it was driven end to end rather than argued from reading the source, it has a
named cost to a person, and its input is reachable by a producer that was actually
driven. Everything else is a residual.

The third condition is the one that is usually skipped. A cost over an input that
nothing can produce is not a cost, and the honest report of a failed hunt names
how many candidate producers were driven rather than claiming that nothing
produces it.

Reachability is a property of a moment, not of a line, and that is what decides
whose finding it is. A defect can sit unreachable for as long as nothing calls
the code holding it, and become blocking without that code changing at all, on
the day a change supplies the producer. The branch that made it reachable is the
branch it blocks, because asking who wrote the line asks a question whose answer
never makes anybody fix it.

## Flagged ambiguities

- "Watermark" is not one job. Deletion's watermark is a sequence floor, and
  filtering removals by it is the design. Sync's watermark is an audit record,
  and filtering increment scope by it is the silent empty-run bug.
- "Guard" and "test" are not interchangeable here. Every guard is a test, but a
  test that exercises a feature is not a guard, and the distinction decides
  whether the pending register is the right home for it.
- Discharging a pending register entry has been described as two halves, meaning
  the entry and the decorator. It is three edits, because the meta suite keeps its
  own mirrored copy of the key that must move with them.
- "Landed" names two different events. A unit lands when it merges. A verb lands
  when its planned marker clears because the module exists. They can happen in
  different sessions, and only the second puts the name in front of the parser.
- "Confirm" and "accept" are not one write. A confirm gate records that the run
  may proceed. A verdict records what to do with a review item. The first without
  the second can report success and still do nothing.
- "Reachable" names two questions that get answered at different times. One is
  whether any producer exists that can be driven to the input at all, which is
  what a hunt reports. The other is when the input became reachable, which is what
  decides which branch a finding belongs to. A finding can fail the first question
  today and pass it tomorrow with no change to the code it is about.
- "bpm" is both the domain quantity and a file-tag spelling. The quantity may
  live on an attribute. The tag spelling may not appear as a mapping key in the
  package, because a mapping that carries it is treated as a grid write.
- Unit, attended chore, and residual finding have all been called "an item on the
  board". Two of the three are work and belong there; a residual is a record of an
  accepted problem and belongs in the register instead. Collapsing them is what
  makes people ask why the board does not list everything the project owes, and the
  answer is that owing and intending are different.
- A pending register entry and a coordination note have both been called "a note
  for a future unit". They are different instruments and the choice between them
  is not stylistic: one is enforced by the suite and one is not, and only the
  register can make a future obligation fail on arrival.
- A zero death row has been read as one thing, an untested guard. It is two, and
  the table renders them identically: the suite failing to notice a real change,
  and there having been no change to notice. Only the first is a finding, and
  only the second is fixed by rewriting the mutation rather than the tests.
- "Residual" does not mean "does not stop a merge". It answers only whether a
  finding blocks on its own merits. A residual with no cost to any person still
  stops a merge whenever the battery is red on its account, and both halves are
  said out loud, because a reader given only the classification will ask why the
  merge stopped and a reader given only the outcome will assume it was blocking.
