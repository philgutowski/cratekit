---
title: An undated heart stays in Undated when a date later resolves, and nothing moves it to its quarter
found: at the build of #277, U120, 2026-10-10.
issue: no
---

**The mechanism.** The source system kept an undated backlog and moved a
heart out of it into its quarter once the account dated it. This engine adds
and never removes, by the standing rule for every favourites writer, so a
heart placed in `Undated` stays there if a later listing carries its date. A
heart listed by a build before U120 carries no frozen date, so the landing of
such a job puts it in `Undated` too; the backfill asks the account for those
and places the rest in `Undated` only when the account dates them nowhere.

**Measured cost.** Not driven live: the live library holds no `Undated`
playlist yet and every hearts job queued from now on freezes its dates. The
cost is one hand drag per heart the account dates after the fact.

**Closes when:** a verb moves a heart from `Undated` to its quarter behind the
refresh's explicit gate, since a move is a removal. Ledger only.
