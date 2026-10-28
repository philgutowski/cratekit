---
title: A Bandcamp download whose header names its file both encoded and plain is saved under the plain name
found: at the second review of #357, U176, 2026-10-28.
issue: no
---

**The mechanism.** `bandcamp._disposition_name` reads `Content-Disposition`
with the standard library's parser, whose `get_filename` takes the plain
`filename` parameter over the encoded `filename*` one when both are present.
A single track sold as a bare file, with a name outside ASCII, would be saved
under the ASCII fallback.

**Measured cost.** Driven on the parser alone. A release arrives as an
archive and its members keep their own names, so only a bare single track is
affected, and its name is the one the person sees in staging. Bandcamp's real
header is unmeasured.

**Closes when:** the attended run reads a real download's header, and the
encoded form is preferred if both are sent. Ledger only.
