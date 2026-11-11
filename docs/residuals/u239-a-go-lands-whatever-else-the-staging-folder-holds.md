---
title: A label go's tail lands whatever else the staging folder holds, an earlier go's unlanded download or a plain download, as one batch under its own manifest and pass
found: at the review of #647, U239, 2026-11-10.
issue: yes
---

**The mechanism.** Every label go stages into the one download staging
folder, and `intake land` lands a whole folder. A fresh `label sync --go`
whose earlier go's download settled and was never landed (finished by `job
resume` or `acquire download --job`, and no `--go` under its run since)
queues its own job beside it, and its tail lands both batches as one under
the new go's manifest and pass, so the earlier go's tracks are filed under no
label. U239 makes a go under its own run refuse its tail when a LATER go job
holds tracks in the folder (`_beside` in `src/cratekit/label/go.py`), but no
check sees an earlier go job, or a download no go queued (a plain `acquire
download` into the same folder). The same fresh go, when it has nothing new to
take, asks the gate over an empty plan and ends `no_op` naming nothing about
the unlanded download (the review's row 9).

**Measured cost.** Driven at the review against the suite's stand in landing
(`test_F3`, `test_K5`, `test_G`): the tail ran over four files where the go
downloaded three and planned the landing under the go's manifest and pass; a
fresh go after a job finished by hand ended `no_op` with three tracks
unlanded. What a real landing files is unmeasured. Present since U108 and
U190; U239 did not add it.

**Closes when:** a go refuses to queue, or to run its tail, while the folder
holds tracks a landing of this go would take that are not this go's, with a
landing proof by pass on both media (the bridge's intake file, the native
landing's session record) so a landed batch is not mistaken for a waiting
one; and a fresh go with nothing to take names an unlanded go download and
the `--go` under its run that lands it. Earns an issue: the product files a
DJ's tracks under the wrong pass and label.
