---
title: A machine named by a plain word is caught only in the host forms the scan lists, not a tailnet name, an unlisted suffix or a host typed in a shell prompt
found: at the review of #1025, U957, 2026-11-23.
issue: no
---

**The mechanism.** `_host_forms` in `scripts/scan_repo.py` lists the shapes
in which a detected ordinary word names the machine: `<t>.local`, `.lan`,
`.localdomain`, `.home.arpa`, `user@<t>`, `//<t>/` or `//<t>:port`, a UNC
`\\<t>\`, and `<t>:/path` or `<t>:~`. The base matched the bare word anywhere,
so every other form it used to catch now passes: a tailnet or router suffix
(`.ts.net`, `.fritz.box`), `.home` and `.internal`, which were tried and
removed because `Path.home()` and attribute access read as hosts, a default
shell prompt (`<user>@<t> ~ %` is caught by the `@` form, `<t>:~ <user>$` by
the scp form, but `[<t> ~]` is not), and a UNC path inside a source literal
with doubled backslashes.

**Measured cost.** Round one drove thirteen such forms: the base flagged all,
the first head none; the fix round restored the listed ones. The tree writes
none of the remaining forms today (grepped), so no producer was driven. The
other way, the `user@<t>` form reads `someone@somewhere` and `line@hours`
in two test files as hosts, so a machine named `somewhere` or `hours` is red
there (round two, through `scan_tree`); a URL host such as `https://host/x`
is red by design.

**Closes when:** a form that names the machine and not ordinary prose is
added to `_host_forms` with a test, after driving it over the tree for the
words the tree writes. Ledger only: maintainer facing.
