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
crate label sync
```

The registry says which labels are followed. Import brings one catalogue in on
demand. Harvest reads labels back off a playlist and imports nothing at all. The
guided label sync asks, label by label, about the releases new since that label
was last asked, and downloads only what was answered for.

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
crate label registry add "Some Label" --match "Some Label Records"
```

Supply `--match` when the string the catalogue actually credits is not the name
you want to see in the library. The needle is used for verification, the name is
used for display, and keeping them apart is what lets you call a label whatever
you like without breaking the check. The needle matches whole words, so a
clipped needle confirms nothing: `Rawax` confirms `Rawax Records` and never
`RAWAXXX`, and `Some Label Rec` would confirm `Some Label Rec` but not `Some
Label Records`.

## Seed artists and the track limit

A label with no artist page of its own under its exact name cannot be crawled
until it names at least one seed artist, and it refuses by name on every sweep
until it does. A seed is an artist name, or `id:` followed by the provider's
digits when two acts share that name. The track limit is how many of the
label's newest tracks to take.

```bash
crate label registry add "Some Label" --track-limit 50 --seed "Some Artist" --seed id:12345
crate label registry set some-label --track-limit 100
crate label registry set some-label --seed "Another Artist"
```

A sweep keeps an offer window of each label's newest releases in review, ten
by default (`labels.offer_per_sweep` in the configuration). Releases already in
the queue hold their places, so a first sweep files ten and a later one files
only what is new. What the window did not reach is counted rather than dropped,
less each release whose copyright line names another label. `crate label
sync` says the label's own as a count and those with no line as "up to",
not yet checked; the grouped review list shows both as one `beyond` figure.
`--offer` raises the window for one label:

```bash
crate review list --queue label-release --group-by label
crate review list --queue label-release --group-by run
crate label registry set some-label --offer 30
```

Nothing a sweep files is accepted for you. Every label release waits for your
own verdict in review before anything downloads.

`set` changes only the fields you pass and keeps the rest. A `--seed` list
replaces the held one, so pass every seed you want kept. It refuses a label the
registry does not hold rather than creating one, and it refuses a seed that
starts with `id:` and is not digits, because that seed would be searched for as
an artist name and match nobody.

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
crate review resolve ITEM_ID --verdict accepted
crate label registry adopt
```

The separation is the whole point. A playlist tells you which imprints you are
already listening to, and deciding to follow one is a second, explicit act: you
accept the label in review, then `label registry adopt` adds every accepted
label the registry does not already hold. A label already held under another
spelling, a different case, a decomposed accent or the identifier a carried
over list gave it, is reported as held and never filed twice, so adopt is safe
to run after every review sitting. A rejected or undecided label is counted and
left alone. If the playlist cannot be listed, harvest refuses and says so rather
than inventing a label name out of a track title.

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

## From an accepted release to a download list

Accepting a release records a decision and acquires nothing. `label approved`
is the step that turns those decisions into work:

```bash
crate label approved
crate acquire download LIST_PATH
```

It reads every accepted release on the label queue, reads each release's tracks
from the provider again by release identifier, resolves every track against the
library, and writes the missing ones into a list document `acquire download`
accepts. The default output names the list's path and the next command. A
manifest is written beside the list, carrying the label, the year and the
release behind every listed track, which is what a later landing files label
tracks by.

What it does not list, and says so by count: a track the library already holds,
a track held in another version, which is offered for review under this verb's
own key and listed on a later run once answered, a track deleted on purpose,
and the same recording arriving a second time from another accepted release.

There is no handed off state. Ownership is the record, so run it as often as
you like: a track that has landed since the last run resolves owned and drops
out. The list's name carries a digest of everything it writes, rows and
provenance alike, so the same work rewrites the same file and any other work,
a corrected year included, takes a new name rather than colliding with an
earlier list.

Before anything is resolved, the genre gate judges each label's accepted
releases together. A release whose genre family is under the taxonomy's out of
place share for its label, one hip hop EP among a house label's ten, is held:
it is not listed, not offered for review, and is named on a line of its own
with its family, its count and the share. A release whose genre is not known is
listed and named on a failing `ungated` line, and so is every release of a label
that had a release unread in the same run, since its share is then unknown. The
genre is what the catalogue reports on a release's tracks, and the streaming
catalogue reports none today, so expect every release on that line for now.

Owned means landed, not listed and not staged. A list written before its tracks
landed is superseded by the next one, which holds everything the earlier one
did that is still owed. Download the newest list and ignore the older ones,
because downloading both fetches the shared tracks twice and nothing marks the
older list as spent.

A release the provider no longer has is a failing line naming the release and
the `crate review clear` that revokes its acceptance, and the other releases
still list. An accepted item that names no release at all is settled the same
way. A release the provider could not answer for is a failing line that says to
run again, and after three such failures in a row the remaining releases are
reported as not asked rather than each spending a full retry wait on a provider
that is down. A single track row the provider returned in a shape that cannot
be read is a failing line of its own, and the rest of that release still lists. If no release could be read at all, or nothing was listed
while some could not be read, it refuses with `label-list-unusable` rather than
report a clean no-op, because that would read as a library that already holds
everything. A release with no readable year is listed, reported as undated, and
carries no year in the manifest.

## Syncing the followed set

The guided label sync walks the followed labels one at a time and asks, per
label, only about the releases new since that label was last asked. Every
answer is saved as it is given, so a walk can stop at any label and resume
there. When every label is answered, one gate over one summary starts the
download, which then runs unattended.

```bash
crate label sync
crate label sync --next
crate label sync --next --label "Some Label"
crate label sync --go
```

Every go downloads into the one staging folder and its landing takes the
whole folder, so land each go before the next. A go refuses before its gate
while the folder holds anything that is not its own, another download's
tracks or files no download names, and says how each lands: an earlier go's
through `crate --run RUN label sync --go`, which takes it to its landing,
names the landing its tail reached, or refuses naming the tail by hand while
the folder holds anything else; a sync pass's through `crate sync land
--pass-run RUN`; anything else by moving it out of the folder and landing it
on its own.
`crate sync land` refuses the same way beside a go's download.

`crate sync all` does not touch labels. It makes no provider call for them and
queues nothing for them, whatever the profile enables, and its report names
`crate label sync` instead, so a routine sync can never start a label download.

`crate sync labels` is retired. It queues nothing and names the guided verb. It
still resumes a labels sweep queued before the guided verb replaced it, so a job
already in the queue is never lost:

```bash
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
