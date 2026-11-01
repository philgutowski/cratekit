---
title: A Question for Phillip posted by a session that keeps building releases its lane, so the queue offers the card's lane to another thread
found: at the build of #410, R-1091, 2026-11-01.
issue: no
---

**The mechanism.** `cloud_state` in `scripts/board.py` reads a card's state
from the session's last comment that is not a `Plan` or `Progress` note, and a
`Question for Phillip` reads as `waiting-on-phillip`, which is not a hold. The
project's standing rule is that a question never stops a thread: the session
makes the conservative call and keeps building. A session that posts the
question and keeps going has therefore given up its lane in the queue's
reading while it still works the card, and `board.py cloud` counted four of
five lanes held and offered the freed one to the next card.

**Measured cost.** Driven on #410: the queue read `Held, 4 of 5` and #410 as
`waiting-on-phillip` straight after the question, and `Held, 5 of 5` with the
card `underway` again after a second `Started`. Nothing is lost while the
coordinator fills lanes by the hour, but a sixth build can start, and a reply
from Phillip would read the card as `answered` and offer it to a second
thread while the first is still on it.

**Closes when:** the cloud-unit skill says a session that asks and keeps
building posts `Started` again after its question, or `cloud_state` reads a
question followed by the same session's `Progress` as a hold.
