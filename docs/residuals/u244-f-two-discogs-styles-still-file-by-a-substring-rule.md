---
title: Afro-Cuban and Electro House file by substring rules written for the record shops, as Afro House and Tech House
found: at the review of #673, U244, 2026-11-12.
issue: no
---

**The mechanism.** A Discogs style with no row in `[vocabulary.discogs]` goes
on to the taxonomy's `[[suggest]]` substring rules, which were written for the
record shops' combined names and read a style by any word it contains. The fix
round gave rows to six such styles; Afro-Cuban (to Afro House) and Electro
House (to Tech House) have no folder that names them and still file this way,
and the full Discogs style list was not read.

**Measured cost.** Driven at the review through `tag.tag_one` with recorded
styles. The style names were the reviewer's, not read from the live API, so
how many files carry them is not measured.

**Closes when:** the attended Discogs trial reads the styles a real folder
answers, and each misfiled one gains a row, or Discogs' words skip the
substring pass. Ledger only until measured.
