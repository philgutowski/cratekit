---
title: The needs genre campaign walks every audio file under the library root three times per alias word
found: at round two of the review of #851, U294, 2026-11-21.
issue: no
---

**The mechanism.** For each settled or answered alias, `plan_words` in `cli/verbs/tag_campaign.py` walks every audio file under the library root to list the files the alias retags. It does so at the run that shows the gate and again at the run that answers it, and `_words_step` walks once more through the verb's own `plan_alias` to hold the apply to what the gate listed. Round two counted 40 tag reads at the first act and 86 at the answering run, on 20 files and 2 words. Round one's head walked once per word, and showed none of the files.

**Measured cost.** Time on the live campaign, which reads one tag of every file under the root three times per word. Not measured on a real library.

**Closes when:** the answering run reuses one walk for the gate check and the apply, or the walk reads each file once for every word. Ledger only.
