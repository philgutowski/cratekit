---
name: label-catalogues
description: Follow record labels as a source, and take their catalogues into the library. Use when somebody wants to start or stop following a label, pull one imprint's catalogue in, find out which labels are behind the tracks in a playlist, or bring every followed label current with its new releases. Trigger words include favourite labels, label registry, follow this label, import the catalogue, harvest the labels, imprint, and new releases from my labels.
---

# Label catalogues

A record label is a source, the same way a set recording or a playlist is. Four
verbs cover it, and they answer four different questions rather than being four
ways to do one thing.

```bash
crate label registry
crate label import "Some Label"
crate label harvest https://provider.example/playlist/PLAYLIST_ID
crate sync labels
```

The registry says which labels are followed. Import brings one catalogue in on
demand. Harvest reads labels back off a playlist and imports nothing at all. The
labels sync brings the whole followed set current against its own watermark.

## The registry holds intent, not history

The registry is one document per installation recording which labels are
followed. It is deliberately not a record of what has been pulled, because those
two facts rot at different rates and a file that mixes them cannot be edited
safely.

```bash
crate label registry
crate label registry add "Some Label"
crate label registry remove some-label
```

With no action it lists, which is why the bare verb is the cheapest way to see
the followed set. Adding a name that already yields the same identifier updates
that entry in place rather than creating a second one, so re-adding a label is
harmless.

## Identity is the identifier, never the display name

A label's identifier is derived from its name once, at the moment it is added,
and never again. Every per label watermark is keyed on that identifier. That is
what makes the rename safe and the remove expensive:

```bash
crate label registry rename some-label --to "Some Label Recordings"
```

Renaming changes the display name and leaves the identifier, so the record of
what has already been pulled follows the label through the rename. Removing a
label and re-adding it under a different spelling produces a different
identifier, which orphans the old watermark, and the next sync treats the whole
catalogue as new. When the label has only changed what it calls itself, rename
it. Reach for remove only when you genuinely want to stop following it.

## The match needle, and why nothing is guessed

Discovery works off copyright text and artist credits, which is a heuristic and
is treated as one. Every candidate release is then verified against an external
catalogue, and anything that does not come back confirmed is dropped rather than
acquired. Without that step a distributor credit, a compilation, or a
neighbouring imprint with a similar name gets pulled in and has to be unpicked
by hand later.

```bash
crate label registry add "Some Label" --match "Some Label Rec"
```

Supply `--match` when the string the catalogue actually credits is not the name
you want to see in the library. The needle is used for verification, the name is
used for display, and keeping them apart is what lets you call a label whatever
you like without breaking the check.

## Importing one catalogue

Import resolves the name against the registry first and refuses if it is not
there. That is not a formality: resolving through the registry is what records
the pull against the same identity the sync uses, so an import and a later sync
do not each think they are seeing the catalogue for the first time.

```bash
crate label registry add "Some Label"
crate label import "Some Label"
```

The verb queues a job and returns its identifier rather than blocking, because a
catalogue pull is long, interruptible work. Watch it, or pick it back up, with
the job verbs:

```bash
crate job show JOB_ID
crate job resume JOB_ID
crate job list --state blocked
```

A resumed job does not repeat completed work. A blocked job always carries a
cause saying what it is waiting for, which is usually a review decision or a
credential, and that is a different thing from a failure.

## Harvest reads, and writes nothing

Harvest lists a playlist's tracks, pulls a label name off each copyright or
label credit, verifies every distinct name it finds, and offers the confirmed
ones for review. It adds nothing to the registry and downloads nothing.

```bash
crate label harvest https://provider.example/playlist/PLAYLIST_ID
crate review list --queue label-release --kind harvested-label
```

The separation is the whole point. A playlist tells you which imprints you are
already listening to, and deciding to follow one is a second, explicit act you
perform with `label registry add`. If the playlist cannot be listed, harvest
refuses and says so rather than inventing a label name out of a track title.

## Deciding on releases, once

A label sweep proposes releases, it does not take them. Decisions land in the
review queue and they persist, so the next sweep does not ask again about a
release you already turned down.

```bash
crate review list --queue label-release
crate review resolve ITEM_ID --verdict accepted --actor curator
crate review resolve ITEM_ID --verdict rejected --actor curator
```

A rejection is a decision rather than an absence, and it suppresses the item
until somebody explicitly revokes it. That is why rejected items are hidden by
default and why clearing one is a deliberate act:

```bash
crate review list --queue label-release --suppressed
crate review clear ITEM_ID --actor curator
```

Releases you previously buried at the version level are consulted too. A sweep
reports those separately as suppressed instead of re-offering them, so a version
you deliberately declined does not come back in through the label door:

```bash
crate tombstone list --all
```

## Syncing the followed set

The labels sync pulls new releases across every followed label and advances its
own watermark. It is one source among several, and it keeps its own cursor, so
running it does not disturb where any other source had got to.

```bash
crate sync labels
crate status
```

`status` is the verb that answers where each source stands, which is the
question people usually mean when they ask whether a sync worked.

When the whole set is being brought current at once, queue every source instead
and let them share one intake run, so the increments land in one intake file
rather than one per source:

```bash
crate sync all
```

The run identifier is what couples them. Pass it explicitly only when you are
attaching a labels increment to a run something else already started:

```bash
crate sync labels --run-id RUN_ID
crate sync labels --job JOB_ID
```

## When it refuses

Read the refusal. A label verb refuses for a small number of specific reasons,
each with its own remedy: the name is not in the registry, the registry document
could not be read or locked, the playlist could not be listed, or a credential
the provider needs is missing. Retrying without acting on the reason produces
the same refusal.

```bash
crate doctor
crate --output json label registry
```

The JSON form is the one to reach for when something other than a person is
reading the answer, since the human rendering is free to change and the payload
is not.
