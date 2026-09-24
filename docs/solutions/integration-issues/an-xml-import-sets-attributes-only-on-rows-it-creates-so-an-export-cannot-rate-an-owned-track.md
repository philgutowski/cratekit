---
title: "An xml import sets a track's attributes only on a row it creates, so a Rating patched into an export never reaches a track rekordbox already holds"
date: 2026-09-24
category: integration-issues
module: src/cratekit/write/routing_cli.py, src/cratekit/write/rbxml.py, src/cratekit/write/trees.py
problem_type: integration_issue
component: rekordbox_xml_bridge
severity: medium
resolution_type: code_fix
refines: "the source system's A2 spike, which found the same rule for Location matching"
applies_when:
  - "A verb writes a COLLECTION TRACK attribute (Rating, Comments, Genre, Colour) into an export and tells a person to import it"
  - "The rows it writes came from a collection export rekordbox produced, rather than being spliced in by this product"
  - "An attended sitting reads an attribute back as unchanged after an import that reported success"
  - "A plan or a pending text counts attribute changes as delivered by an import"
---

# The xml bridge cannot change a track rekordbox already holds

Measured at the tenth attended sitting, 2026-09-24, and recorded as R-688.
`route inbox --export` set `Rating` on four collection rows in the file it
wrote. Each was a track the library already held and nobody had rated. After
the import and a fresh export, all four read `Rating="0"`.

## The rule

rekordbox takes a row's attributes from an xml file only for a row it
**creates** on that import. A row it already holds, matched by `Location`,
keeps its database values, and the file's attributes are ignored without a
warning. The source system's A2 spike found the same rule for `Location`.

So every row of a collection export is out of reach, because rekordbox
produced the export from rows it holds. A writer that patches an attribute
in place, such as `rbxml.apply_rating_changes`, never adds a row. On an
export it therefore can only write values that will not land.

## What this is not

- It is not the playlist rule. Playlist membership through the file has its
  own rules: a root playlist replaces, a nested playlist lands at the root,
  and a folder appends. See
  `folder-level-xml-import-appends-children-and-the-playlist-xml-is-parsed-on-every-play.md`.
- It does not touch rows this product creates. `intake/collection_xml.py`
  splices new rows with their `Rating` already set from energy, and the
  import creates them, so those ratings land.

## How to apply

Before a verb writes a track attribute into an xml file, ask whose row it is.
If the row came from rekordbox, the value has to go to the database behind
the session gates, or the verb has to say it cannot deliver it. R-688 took
the second path. The export sweep counts the owed ratings into a
`rating-not-landable` warning and writes none. A green suite cannot catch
this, because the fixture export is parsed back by the same tests that wrote
it, and nothing in a fixture plays rekordbox's import.
