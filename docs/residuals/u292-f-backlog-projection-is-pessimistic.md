---
title: The needs genre backlog's projection leaves out rows filed under another word's answer and rows tag rows moves in, so it reads pessimistic
found: at round two of the review of #849, U292, 2026-11-21.
issue: no
---

**The mechanism.** `Backlog.projected` in `tagging/backlog.py` counts each word's widest answer over that word's own rows. A row grouped under its file's word whose row carries another word is filed when that other word gets a folder, and a joining row is filed by its new word's answer; neither is counted. Round two ran 300 random libraries through the printed campaign: 164 ended below the projection and none above, and 42 of 1,075 answered words moved more of their rows than claimed.

**Measured cost.** The projection overstates what stays in needs genre after the campaign, never understates it. A person reading it is told the campaign does less than it does.

**Closes when:** U294 (#851) reads needs genre again after each step, or the projection counts rows reached by another word's answer. Ledger only.
