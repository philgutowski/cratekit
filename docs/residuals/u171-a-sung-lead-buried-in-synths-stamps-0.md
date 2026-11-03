---
title: The frame model hears no singing on a sung lead buried in synths, so a vocal track like I Feel Love stamps 0 and gets no vox tag
found: at the build of #352, U171, 2026-11-03, from A64's frame tables.
issue: no
---

**The mechanism.** The vocal score is the share of frames whose AudioSet
Singing score reaches 0.05 (`analysis/vocal.py`, `presence_score`). On Donna
Summer "I Feel Love", which has a sung lead, A64 measured the loudest Singing
frame at 0.034, Male singing 0.0007, Female singing 0.0004, Vocal music
0.0006, Rapping 0.0012 and Speech 0.0128, with the top classes by mean
Electronic music, Trance and Techno. The model does not hear the voice as a
voice, so no floor, rounding or choice among its vocal classes scores it
without also scoring instrumentals: at a 0.01 floor it would stamp 1 while
Rick Wade "Shinjuku Strut" would stamp 16. Among the 80 zeros of sitting 47,
several tracks with spoken, rapped or chopped vocal hooks reach the floor on
Speech or Rapping and never on Singing (Pedestrian, Mr. Tophat, Wajatta,
Luke Vibert), but Speech reaches the floor on at least one percent of the
frames of 43 of the 116, and on only two of the ten known sung leads, so
counting it needs ground truth the session does not have.

**Measured cost.** One sung lead among ten known vocals scored 0 and carries
no `vox` tag, so a DJ filtering on `with vox` does not see it. How many of the
other 80 zeros carry a vocal a DJ would call one is unmeasured: Phillip has
named none of them, and the session could not listen.

**Closes when:** Phillip chooses on the decisions page (question
`352-vox-meaning-1`) whether `vox` keeps meaning a sung lead the model can
hear, also counts rap and speech, or is scored on a separated vocal stem, and
a card builds the choice with its restamp. Ledger only until then: the
product says what its model heard, and a change is a product decision rather
than a defect.
