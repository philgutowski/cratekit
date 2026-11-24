---
title: A message catalogue made reachable after the suite configures is not read by argparse's stand in, which answers untranslated
found: at the review of #985, U336, 2026-11-24.
issue: no
---

**The mechanism.** `tests/conftest.py` asks `gettext.find` once, at `pytest_configure`, whether a catalogue exists for the default domain, and where none does it hands argparse `NullTranslations`' `gettext` and `ngettext` for the rest of the run. A catalogue that becomes reachable afterwards, by a test setting `LANGUAGE`, `LC_ALL`, `LC_MESSAGES` or `LANG`, or binding a domain, is read by `gettext.gettext` and not by the stand in: the review wrote a `messages.mo` mapping `usage: ` to `USO: `, bound it, set `LANGUAGE=xx` after configure, and `gettext.gettext` answered `USO: ` while argparse's stand in answered `usage: `.

**Measured cost.** None measured. Reachability is unmeasured: no test, source file, script or installed package sets a locale variable or calls `textdomain` or `bindtextdomain`, no `messages.mo` exists on the cloud container, and Phillip's Mac was not read. A test that did would read argparse's English where a person's machine would print the translation, which no test asserts today.

**Closes when:** a test that changes the locale or binds a domain runs with argparse on `gettext` itself (the conftest's `_give_argparse_its_lookups_back` and `_answer_argparse_untranslated` around it), or the conftest asks again where the environment changes. Ledger only.
