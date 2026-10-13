---
title: Tidal nests a folder through the move endpoint and the app does not draw it, so the account root stays flat
date: 2026-10-13
category: integration-issues
module: "outbound tidal_account folders, organize account area"
problem_type: integration_issue
component: provider_api
severity: medium
applies_when:
  - "A brief or residual proposes parent folders on the Tidal account (Labels, Sets, a year under a parent)"
  - "A session reads the vendored client's create_folder(parent_id) or a trn:folder: move and takes it as proof of nesting"
  - "A folder scheme is planned around sort order on the account"
tags:
  - "tidal"
  - "folders"
  - "nesting"
  - "organize"
  - "probe"
related_components:
  - "tooling"
---

# Tidal nests a folder through the move endpoint and the app does not draw it, so the account root stays flat

## Context

The brainstorm of 2026-10-13 (`docs/plans/2026-10-13-1407-feat-tidal-account-convention-plan.md`, commit abcfceb4) started from residual R-992, which deferred a nested `Labels / <Label>` and `Sets / <year>` scheme because the adapter creates folders at the root only and moves playlists only. The vendored client reads as if nesting were one call away: `LoggedInUser.create_folder(title, parent_id)` sends a `folderId` parent, and `Folder.move_items_to_folder` passes any `trn:` string through, `trn:folder:` included. Phillip asked for the capability to be checked before anything was designed on it, and a live probe answered it.

## Guidance

**1. Create with a parent is ignored.** `create_folder("C", parent_id=A)` returned a folder whose `parent_folder_id` is `root`, listed at the root beside A. The parameter the client sends does nothing on the account.

**2. A folder move is accepted and reads back nested.** `move_items_to_folder(["trn:folder:B"], A)` returned `True`, and `folder_folders(A)` then listed B, gone from the root. The API holds the nesting.

**3. The Tidal app does not draw it.** With B inside A by the API, the app showed A as empty. Nesting organises what Cratekit reads and nothing Phillip sees, and the account is organised for him, so he ruled nesting out the same day. R-992 is closed as decided, not as built.

**4. Name forms sort nothing.** The app lists folders and playlists by recent activity, not by name, so a prefix that sorts product folders first is pointless. The levers that remain on a flat root are which folders exist and which playlists sit loose, and that is what the plan above commits.

**5. A probe on the live account is a write and the session cannot make it.** The permission layer refused the probe script from the session; Phillip ran it from the prompt with the `!` prefix, and the cleanup of the three `Cratekit nesting probe` folders is his too, through `Favorites.remove_folders_playlists(type="folder")`. Read the root before planning any legacy or empties step: a probe folder left behind would be offered for removal.

## Why This Matters

The client's surface overstates the provider. A session that trusts `parent_id` or a folder `trn` designs a scheme the person never sees, and R-992's "closes when" line read as an invitation to build exactly that. Two sentences of probe result retire a whole branch of design.

## When to Apply

Any proposal that puts a folder under a folder on the account, or that relies on the account's order. The answer stands until someone shows the app drawing a nested folder, in which case read the account first and rerun the probe rather than trusting the memory of this note.

## Examples

Probe output, 2026-10-13: `child: ... parent_folder_id= root`; `move folder B into A -> True`; `folders inside A: {'3ecb2ae0-...': 'Cratekit nesting probe B (moved into A)'}`; `probe names at root: {A, C}`.
