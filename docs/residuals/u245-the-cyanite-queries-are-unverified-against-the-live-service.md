---
title: The Cyanite trial's mutations and its reading of a rejected key are written from Cyanite's documentation and never driven against the service
found: at the build of #674, U245, 2026-11-13.
issue: no
---

**The mechanism.** `tagging/cyanite.py` asks Cyanite's GraphQL API with three
texts: `fileUploadRequest`, `libraryTrackCreate(input: { uploadId, title })`
and `libraryTrack(id)` with `audioAnalysisV6`'s `genreTags`, `subgenreTags`,
`moodTags` and `energyLevel`. The documentation read on 2026-11-13 shows the
read query and the answers' shapes, not the two mutations' text or input
type, and does not say how a bad key is answered; the trial reads a 401, or a
GraphQL error coded or worded as unauthenticated, as a rejected key. The free
preflight proves the read query's shape and the key before any upload; a
mutation's shape is proved only by the first file.

**Measured cost.** Not driven: no live key and no live call in the cloud, by
standing rule. A wrong mutation text is answered with a GraphQL error, which
stops the run at the first file before anything is billed, so the cost is a
stopped run, never a silent wrong answer.

**Closes when:** the attended trial's first run reads its first row, or its
stop line, and the texts are corrected if Cyanite refused them. Ledger only.
