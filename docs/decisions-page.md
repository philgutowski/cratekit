# The decisions page

Every question for Phillip, a brainstorm's or a `Question for Phillip`,
reaches the decisions page, because the page is where he answers:
https://claude.ai/artifact/FUqChoK5qKhztLdzzEADaS

**A build thread posts it on its card only and never writes the page**,
decided by Phillip on 2026-11-04 (METHOD's Sharing the board section), in the
form the `cloud-unit` skill's Asking Phillip gives. Phillip's other project,
which files the cards, copies the question onto the page in the form below
and posts his answer back. This file moved here from the `cloud-unit` skill
by U314, since no build thread writes the page.

**The page's form**, for the filing project, which writes it; a build
thread never does. One document per question into the page's `decisions` collection with
the `ArtifactData` tool (load it with ToolSearch, `select:ArtifactData`),
action `set`, `url` the page above, `collection` `decisions`, `doc_id`
`<card>-<short slug>-<n>`, and this body:

    {"card": N, "card_title": "U158: ...", "group": "<card>-<slug>", "order": n,
     "kind": "brainstorm" or "question", "question": "...",
     "context": "two or three sentences a reader needs, and the cost of each way",
     "options": [{"label": "...", "detail": "one line"}, ...],
     "recommended": 0, "status": "open", "answer": null,
     "asked_by": "the lane worker on #N", "asked_session": "<the asking thread's session id>",
     "asked_at": "<now, ISO 8601 UTC>"}

The recommendation is the option at index `recommended`, and the page shows
it first and marked. Give two to four options; the page adds its own
"something else". Write the context so the question can be answered without
opening the card. The filing project then ends a comment on the card with a
line linking the page and, where it has the `PushNotification` tool, sends
one short notification naming the card and that a decision waits on the
page. A document is marked answered by the page and relayed by the relay
thread, never by the writer.

**How his answer reaches the card.** Phillip presses Answer on the page,
which saves his choice in the document and sets its `status` to `answered`.
The scheduled task "Cratekit decisions relay" wakes the project thread "Wire
decisions page answers to cards", called the relay thread here, every hour
at 34 minutes past. It posts each answered document on its card under
`Answer from Phillip`, or sends it to the document's `asked_session` when it
names no card, sets the document's `status` to `relayed` with `relayed_at`
and `relayed_note`, and tells the building project's coordinator, which
starts a thread on the card if none of its threads is still building it.
`board.py cloud` reads that heading as his reply whoever posts it, and
offers the card as `answered`. The coordinator's own hourly wake fills free
lanes only and never reads the page.

**The fast path.** The page cannot reach a project session by itself, because a
comment on a page sent to Claude wakes only a session watching that page,
and no project session can watch one. So while any answer is saved but not
relayed, the page shows a "Pass on your answers" box holding a ready prompt
that lists each one (card, question, answer, note and decision id), with a
button that copies the prompt and opens the Cratekit project chat in a new
window, and a button that only copies it. Phillip pastes it into that
project's chat, its Claude messages the relay thread, and the thread relays
at once. Without the paste an answer waits for the hourly check.
