---
title: Four Discogs styles file by substring rules written for the record shops, Afro-Cuban and Afro-Cuban Jazz as Afro House among them
found: at the review of #673, U244, 2026-11-12.
issue: no
---

**The mechanism.** A Discogs style with no row in `[vocabulary.discogs]` goes
on to the taxonomy's `[[suggest]]` substring rules, which were written for the
record shops' combined names and read a style by any word it contains. The fix
rounds gave rows to four such styles. Afro-Cuban and Afro-Cuban Jazz (to Afro
House), Electro House (to Tech House) and Progressive Breaks (to Progressive
House) still file this way, and the full Discogs style list was not read. The
two Afro-Cuban styles belong in Jazz, and a row writing Jazz was taken out in
round two: a copy made before the Jazz folder gains the Discogs table in the
run that holds Jazz, and after the hold's own hand edits it would not load.

**Measured cost.** Driven at the review through `tag.tag_one` with recorded
styles. The style names were the reviewer's, not read from the live API, so
how many files carry them is not measured.

**Closes when:** the attended Discogs trial reads the styles a real folder
answers, and each misfiled one gains a row (the Jazz ones once the upgrade can
add a row only where its tag names a folder in the copy), or Discogs' words
skip the substring pass. Ledger only until measured.
