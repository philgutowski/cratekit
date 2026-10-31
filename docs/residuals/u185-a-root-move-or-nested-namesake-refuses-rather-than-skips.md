---
title: A write that renumbers the root, or a name lookup that finds a namesake inside DEADCA7's folder, is refused at commit rather than kept clear of the folder
found: at the review of #392, U185, 2026-10-31.
issue: no
---

**The mechanism.** The U185 commit guard holds every row of DEADCA7's folder at the top of the tree whole, its position included. Two shapes of write would reach it without meaning to. Moving one of the author's own top level nodes out of the root makes the binding renumber every root sibling above it, the folder among them; and the unscoped `rb_writer.ensure_folder(db, name)` matches a folder of the name anywhere, so a folder of the same name nested inside the push's folder would be adopted and written into. Both are refused at commit with nothing written, so the folder is never damaged; the cost is that the verb stops.

**Measured cost.** Driven by the review on scratch databases: both commits refused, the push's rows byte for byte. No producer in `src`: the one caller of `move_playlist_node` moves within INBOX, and the one caller of `ensure_folder` passes a parent. Whether DEADCA7 pushes nested folders is not established.

**Closes when:** a writer that moves a node at the root, or calls `ensure_folder` unscoped, either keeps the foreign folder out of what it renumbers or matches, or this is read again. Ledger only: the guard holds, and no verb reaches it today.
