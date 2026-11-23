---
title: The write path's code lines rose under U300 instead of falling 15 percent, and its tests stay above their line and time targets
found: at the build of #857, U300, 2026-11-22.
issue: yes
---

**The mechanism.** Phillip's answer A on #847 says every card must still
remove at least 15 percent of its code lines. #857 set the fourteen files of
the write path at most 7,189 code lines (8,458 at the survey, 9,045 on U300's
base `c9192091`) and its fifteen test files at most 10,655 lines (14,553 on
the base). U300 cut prose to its rule and its reason, by that answer, and split
the three files over 1,500 lines, so the area's source fell from 18,806 lines
to 13,872, under its 14,256 target, and no file is over 1,500. Its code lines
rose, from 9,045 to 9,287: each split adds imports, a re-export block and a
three line call-time accessor in each part, so a test that patches the facade
still bites. The tests fell to 11,992 lines, prose only, and their summed time 25
percent (35 seconds to 26), short of the 30 percent the card asks. The area held no
copied block of six logical lines to fold (the survey's own count was 0).
Reflowing message fragments or call arguments onto fewer lines would meet the
count without simplifying anything, and was not done.

**Measured cost.** None to a person. The area misses the 15 percent code rule
by 1,599 lines (7,688 is 15 percent under the base) and the card's code target
by 2,098; its tests miss their line target by 1,337. U300 asked Phillip on
#857 and took the recommended option, land with the miss named.

**Closes when:** a unit cuts this area's code lines to 7,688 or fewer, with
behaviour frozen, the behaviour comparison and the kill set replay, likely by
narrowing the parts' re-export blocks, folding the accessors into one shared
reader per module, and shortening the longest guards named on #857
(`guard_violations`, `node_change_violations`, `assert_app_version`,
`assert_gates`, `verify_commit`, restore's `plan`).
