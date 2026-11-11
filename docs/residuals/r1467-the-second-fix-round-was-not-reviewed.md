---
title: The fix of R-1467's second review round, the tail's kept record, was not reviewed by Fable
found: at the review of #655, R-1467, 2026-11-11.
issue: no
---

**The mechanism.** Review round two found one BLOCKING finding, driven end to
end: a go whose tail started read as many foreign files as its own once its
tracks left the folder. The second and last fix round replaced that count
with `label.go.keep_tail`, kept by the CLI layer whichever way the tail ends,
and the go's own pass's landing proof. METHOD allows two fix rounds, so no
third review read that fix; its tests and its mutation rows are the author's.

**Measured cost.** None measured. The round's own drive of the finding,
rebuilt in the suite (`test_a_go_whose_tracks_left_reads_no_file_put_there_since_as_its_own`),
refuses as it should.

**Closes when:** a Fable pass over the merged range of R-1467 from the second
fix round on finds nothing BLOCKING, or its findings are filed. Ledger only.
