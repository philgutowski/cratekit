---
title: A campaign rehearsed on a copy of the database alone writes the live files, and its answer is pinned to no library
found: at round one of the review of #851, U294, 2026-11-21.
issue: no
---

**The mechanism.** `crate tag campaign` writes audio files in two steps: `tag suggest` writes each proposal's genre into its file, and `taxonomy alias` retags every file carrying the word under the library root. A rehearsal that copies the database and redirects library state, with the rows still naming the live files, would write those files, and the live plan afterwards would differ in what is written, which is the one case CLAUDE.md's rehearsal rule still stops on. The gate is also asked with no `pinned` fact (the shape `docs/solutions/workflow-issues/a-fact-taken-out-of-a-digest-so-a-rehearsal-can-match-must-be-pinned-on-the-run.md` describes), as `tag rows` and `tag suggest` ask theirs. Round one drove one candidate, a run answered on one library and continued under another root, and it refused with nothing written; a copy whose rows resolve under the new root was not driven.

**Measured cost.** Not driven on a real library: the rehearsal is the owed attended card's. Unless the music files are cloned with the database, a rehearsal writes genres into the live files.

**Closes when:** the campaign has a rehearsal of its own that clones the files it would write, as `core.rehearsal` does for the landing, or the attended procedure clones them and pins the database file. Ledger only; the attended card names the cloning step.
