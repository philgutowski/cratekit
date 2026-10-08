# R-777 mutation notes

The author's table, one pass, 20 rows over the guards of `sync mark --pass`,
the native proof in `sync/marks.py` and the landing record in
`intake/native.py`. No independent verifier; every zero below reads as "the
author could not kill it".

- **16 of 20 killed** on the first table, `r777.md`.
- **N7_digest_marks refused**: the fix round put the `landings` line between
  the two lines the row matched, so the first table never applied it. Rerun on
  `r777-confirm.md` with the moved text: **killed**, by the stale answer test.
- **N4_plain_name, zero, user facing**: an unplain name was still refused,
  by the no-landing guard, for a different reason. A test was given the
  refusal's own words, and the confirm table **killed** it.
- **N8_digest_pass, zero, maintainer facing**: the landings carried in the
  digest already differ per pass, since a landing records exactly one pass.
- **N20_both_or_neither, zero, maintainer facing**: neither proof falls to the
  plain name refusal and both falls to the intake file check, so the explicit
  refusal is a second layer over two others. The verb's own parser holds the
  same rule as a usage error, which N11 measures and kills.
