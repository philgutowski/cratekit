"""Read-only library reports: Feature Inventory rows 15 and 20.

Two reports land here, and what they have in common is the property rather than
the subject: **neither one writes anything to the library**. Not a database row,
not an audio file, not a rekordbox XML, not a private ledger beside the report.
That is the unit, and everything below is shaped to make it structurally true
rather than merely intended.

    row 15  duplicate audit      two library entries that may be one recording
    row 20  intake aging report  which intake groupings have gone stale

**Where the answers go, and why the two differ.** ``core.review`` declares the
split R12 rests on: a question a person must ANSWER is a persisted review item,
and a result a person merely READS is an output. The duplicate audit is the first
kind, because only a person can say whether two entries are one recording or an
intentional alternate somebody keeps on purpose, and that answer has to outlive
the run or the same pair is offered again forever. The intake aging report is the
second kind: it states the age of things, which is a fact, and asking somebody to
confirm a fact is how a queue fills up with work nobody needed to do.

So :mod:`duplicates` offers into ``review.Queue.DUPLICATES`` and :mod:`aging`
returns a value the caller renders. **The persistent ignore the brief asks for is
a REJECTED verdict in that queue**, not a file. A private ignore list beside the
report would satisfy the words of the brief and re-create the exact defect the
queue exists to remove, which is why the obligation was registered as a countdown
rather than left in a docstring (P5).

**One input, and it is read-only by construction.** Both reports read a rekordbox
XML export through :mod:`export`, which uses the byte locates in
``cratekit.write.rbxml`` rather than a second parser of its own. Two readers that
resolve one name differently eventually disagree about which node they mean, and
the writers already own the quote-aware, self-closing-aware version of every
locate these reports need. Nothing here opens the rekordbox database at all: the
guarded writer is the only thing in this product that may, and a report has no
business holding a handle that could commit.

Layer note: MODULES. Both rows are Module rather than Core in the Feature
Inventory, gated by the ``duplicates`` and ``reports`` toggles (R5). Nothing is
imported here: a package initializer that re-exports its members turns importing
one report into importing both, and KTD7's lazy module table only stays lazy if
the entries are inert.
"""
