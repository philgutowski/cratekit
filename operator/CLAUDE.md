# Cratekit operator workspace

This folder is where an AI assistant helps you run Cratekit against a real
rekordbox library. It is not the Cratekit source, and it is deliberately outside
that clone, because the clone's own instructions are about building the product
rather than running it.

`crate` is the command. Every workflow runs from the command line without an
assistant, so nothing here is required. What an assistant buys you is the order
of the steps, the reading of a refusal, and a second pair of eyes on a plan
before it writes.

## What the assistant may do on its own

Anything that reports and nothing that writes:

```
crate doctor
crate status
crate profile show
crate job list
crate run show RUN_ID
crate review list
crate restore list
crate report library EXPORT
crate audit coverage EXPORT
crate audit duplicates EXPORT
crate converge
crate route unplaced
```

Reports and audits read a collection export, which is the XML file rekordbox
writes from its File menu, and never the live database. Ask for a fresh export
when the answer matters, because a stale one answers every question confidently
and wrongly.

## What waits for you, every time

- **Any verb that writes.** Intake, routing, naming, tagging, syncing,
  exporting, deleting, restoring, and anything carrying `--apply`. The assistant
  names the verb, says what it will write, and stops. One approval covers one
  run, not the next one.
- **Answering a gate.** A gate is a named question the product stops at before
  it writes, and the answer is recorded against whoever gave it. There is no
  flag that answers them all.
- **The backup acknowledgment.** `crate session ack` is yours. The product
  accepts one from a session working on your behalf only while both backup
  ages are under five days, and never over older ones, which is deliberate
  rather than an obstacle to work around.
- **Quitting rekordbox.** Writing verbs refuse while rekordbox or its background
  agent is running. Closing them is something you do at the machine, and nothing
  here ever starts them.
- **Changing the Cratekit clone.** Reading its docs is fine. Editing it,
  updating it, or switching its branch is your decision, and developing Cratekit
  happens in its own checkout under its own rules.

## How a session runs

1. `crate doctor`, reading the `fail` lines first. A `note` is worth knowing and
   needs no action.
2. `crate status`, for open runs, per source sync state, and any tree whose
   membership no longer matches the database.
3. Say what you want to do. The assistant names the verbs, the order, and what
   each one writes, then stops.
4. You approve. The writing verb runs, and you answer its gate by name.
5. Read what the run reports it actually did, rather than assuming the plan
   happened. A plan is a proposal and the envelope is the record.

## Reading a refusal

Every refusal carries a reason and a remedy. Read it instead of retrying it. The
same inputs produce the same refusal, and a retry that works around a guard
defeats it on the machine it was protecting.

A verb the parser has never heard of is usually a module the active profile
leaves out, so `crate profile show` answers that before anything else does.

## Where the answers are

- `crate --help`, and `crate VERB --help`. When a document and the help disagree,
  the help is right and the document is stale.
- `docs/GUIDE.md` in the Cratekit clone, for the recipes, the gate table, and
  which workflows have been run for real.
- `docs/adapters.md` there, for signing in to the streaming provider.
- The guides under `.claude/skills/` in this folder, one per workflow area.
