---
name: cloud-dispatch
description: The Cratekit lane dispatcher's procedure, run on every message headed Dispatch, from the hourly scheduled task or from a worker that took or freed a lane. Starts one fresh worker session per free lane and builds nothing itself.
---

# Cloud dispatch

The dispatcher is one long lived cloud session with the repository attached.
It builds nothing. On every `Dispatch` message it fills free lanes with fresh
worker sessions, each of which runs the `cloud-unit` skill on one card. A
scheduled task sends `Dispatch` every hour; a worker sends it the moment it
takes a lane or frees one, so no lane waits for the hour.

## Each Dispatch

1. Bring the checkout up to date, and build the venv if this container is new:

       cd /home/user/cratekit && git checkout -q main && git pull -q --ff-only origin main
       test -x .venv/bin/python || { uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -e '.[dev]'; }

2. Carry answered decisions back. The decisions page, https://claude.ai/artifact/FUqChoK5qKhztLdzzEADaS, holds the
   questions the lane asked Phillip. Read the answered ones with the
   `ArtifactData` tool (load it with ToolSearch, `select:ArtifactData`):
   action `query`, `url` the page, `collection` `decisions`, `query`
   `{"where": [["status", "==", "answered"]]}`. For each document:

   - It names a `card`: post a comment on that card headed exactly
     `Answer from Phillip`, quoting the question and his answer, with his
     note if he wrote one, so the worker that takes the card next reads it.
   - It names no card: send its `asked_session` the same text with the
     claude-code-remote `send_message` tool.

   Then `update` the document with `if_version` set to the version you read,
   `status` `relayed` and `relayed_at` now. If the update is refused because
   the version moved, he changed his answer meanwhile: read it again and
   relay the new one at the next `Dispatch`. Carry every answered decision
   back before reading the queue, so a card his answer released is takeable
   in this same `Dispatch`.

3. Read the queue:

       .venv/bin/python scripts/board.py cloud

   If it says every lane is held, that more cards are held than there are
   lanes, or that nothing is for the cloud to take, reply with that line and
   stop.

4. It lists the cards the cloud may take, in order. Take the first one **you
   have not started a worker for in the last twenty minutes**: a worker posts
   `Started` a minute or two after it starts, so a card you just dispatched
   still reads as ready until then. Keep a one line note in this conversation
   of every worker you start, its card and the time.

5. Start one worker with the claude-code-remote `create_session` tool:

   - source_url `https://github.com/philgutowski/cratekit`
   - environment_id: this session's own environment (read it with
     `get_session` and no session id if you do not know it)
   - model `claude-opus-5-5`, permission_mode `auto`
   - title `Cratekit lane: #N`
   - prompt, with N and this session's id filled in:

     > You are a Cratekit cloud lane worker, an unattended Claude Code cloud
     > session with nobody watching, and the cloud is where this project is
     > built. The repository philgutowski/cratekit is cloned at
     > /home/user/cratekit. Your card is #N. The lane dispatcher is session
     > <this session's id>. Invoke the repository's cloud-unit skill with the
     > Skill tool (or read it from the repository's Claude Code skills
     > directory, under cloud-unit) and follow it to the end on card #N:
     > brainstorm it if it is an idea, otherwise plan and build it to METHOD's
     > merge bar with the Fable review, measure its mutation table, merge it
     > to main with the closing trailer, push main, and comment Landed. Wake
     > the dispatcher as the skill says. Push the cloud/N-slug branch the
     > skill names and main, not a claude/ branch. Merging and pushing main is
     > authorized by Phillip, as CLAUDE.md records. Open no pull request
     > unless the skill says to. A question is a stop, so make the
     > conservative call, record it as a residual file, and keep going.

6. Reply `started worker <session id> on #N`. Start one worker per
   `Dispatch`: the worker's own `Dispatch`, sent once it holds its card, fills
   the next lane, so the lanes fill one by one without two workers ever
   reading the same free card.

## Never

Commit, push, edit a card, or build anything. The one thing it posts on
GitHub is `Answer from Phillip`, and the one thing it writes on the decisions
page is a document's `relayed` status. Start a second
worker in one `Dispatch`. Start a worker for a card the queue does not list as
takeable.
