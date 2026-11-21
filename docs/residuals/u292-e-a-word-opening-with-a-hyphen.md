---
title: A genre word beginning with a hyphen is offered a taxonomy command argparse reads as an option
found: at round two of the review of #849, U292, 2026-11-21.
issue: no
---

**The mechanism.** `tag backlog` builds each answer's command with `shlex.join`, which quotes for the shell and not for argparse. A word such as `-x` is offered `crate taxonomy folder -x`, and that command exits 2 with a usage error. Round two drove two files tagged `-x`; the same was true at round one's head.

**Measured cost.** A person pasting the offered command for such a word is refused with a usage error. No catalogue or acquisition path that writes such a genre was driven, so reachability is unmeasured.

**Closes when:** a command for a word beginning with a hyphen is offered in a form argparse takes, or the word is offered no command. Ledger only.
