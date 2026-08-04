# U27 mutation table

Every guard, assertion and constant a review round of U27 added or changed, with
the mutation that reverts it ALONE and the number of tests that die when it is
reverted. A row that kills zero tests is a claim nobody has checked, which is a
finding rather than a curiosity.

**This file exists because the previous table did not.** Round five measured
forty six mutations and reported them in a chat message. The verifier could
reconstruct twelve of the forty six, could not check the rest, and found two of
the reported counts wrong. A table that lives only in a conversation cannot be
audited by the next person and cannot be re-run, so the table lives here now and
the driver's row descriptions live with it.

Method for every row: apply exactly one mutation to a clean tree, run the whole
suite, count distinct failures, restore, move to the next. The `passed` column is
the suite total under the mutation; the clean tree passes 3409 and skips 14, so a
row that killed N shows `3409 - N`. No row changed the collected count.

---

## Round six, 2026-08-04

Measured at the tip of `unit/u27-setup-wizard-and-doctor`, against the clean
baseline of 3409 passed and 14 skipped.

| id | guard | deaths |
|-|-|-|
| R6-01 | the dispatcher classifies EACCES or EPERM as a permission rather than an internal defect (`cli/__init__.py::_unhandled_cause`) | 1 |
| R6-02 | doctor's check runner attaches grant-path-access, not report-defect, to an unstructured break that is a permission (`doctor.answer`) | 2 |
| R6-03 | the check runner appends the permission sentence to the failed check's detail | 1 |
| R6-04 | `_probe_db_path` guards its stat and still proposes an unstattable path (`cli/setup.py`) | 1 |
| R6-05 | `is_mount_point` confirms a False answer instead of calling an unstattable slot an empty one (`core/preflight.py`) | 2 |
| R6-06 | `_names_one_path` re-raises a comparison the operating system refused rather than answering "different" (`core/preflight.py`) | 1 |
| R6-07 | `backup_facts` calls an unreadable fact file a permission rather than a corruption (`core/backup_facts.py`) | 1 |
| R6-08 | an unreadable `.git` marker carries grant-path-access rather than report-defect (`doctor._git_dir`) | 1 |
| R6-09 | the `UnicodeDecodeError` member of the commondir handler (`doctor.py:338` in the reviewed revision) | 1 |
| R6-10 | the `UnicodeDecodeError` member of the `taxonomy.active` read (`doctor.py:904` in the reviewed revision) | 1 |
| R6-11 | `taxonomy.active` chooses its remedy by classification rather than always report-defect | 1 |
| R6-12 | the `UnicodeDecodeError` member of the pre-commit hook read (`doctor.py:1837` in the reviewed revision) | 1 |
| R6-13 | `repo.commit_hook` chooses its remedy by classification rather than always report-defect | 1 |
| R6-14 | `_membership` tolerates a configuration directory the operating system will not open, so the parser is built at all (`cli/__init__.py`) | 2 |
| R6-15 | `permission_denied` follows the declared `__cause__` chain (`core/cause.py`) | 1 |
| R6-16 | `permission_denied` reads the errno as well as the class, for an `OSError` rebuilt across a boundary | 1 |
| R6-17 | the persisted `path-permission-denied` slug, spelled the same in the registry and at the raise site | 1 |

### The whole-verb row

R6-01 is the row the review asked for by name: `crate setup` and `crate doctor`
driven through the REAL dispatcher, against a real directory with mode `0o000`,
must both produce actionable permission advice and no report-defect. The test is
`test_both_verbs_answer_a_real_permission_with_an_act_the_user_can_perform`, and
the arrangement is a configuration directory behind a sealed ancestor, because
that is a site NOBODY guards: `config.load` stats the file before it reads it and
a stat is not a `ConfigError`. Reverting the dispatcher's classification kills it.

R6-14 is the same arrangement one step earlier. `_membership` runs during parser
construction, OUTSIDE the dispatcher's try, so before this round the permission
escaped `cli.run` entirely and `crate --help` exited with a traceback.

### Rows re-confirmed from earlier rounds

| id | guard | deaths |
|-|-|-|
| C-01 | `identity_source` refuses a mount slot with nothing mounted in it | 13 |
| C-02 | the equality shortcut in `_names_one_path`, so a declared mount directory absent from this machine still names itself | 1 |
| C-03 | `mount_location_ancestors` walks the given spelling as well as the resolved chain | 1 |
| C-04 | `identity_source` asks `slot_holds_a_volume` rather than `is_mount_point` | 1 |
| C-05 | the `UnicodeDecodeError` member of the wizard's packaged template read (`cli/setup.py`) | 1 |
| C-06 | the persisted `grant-path-access` slug in the remediation vocabulary | 6 |
| C-07 | the walk up to an ancestor never clamps at the filesystem root (`_is_a_volume_mount_location`) | 1 |

---

## The two counts the fifth round's table got wrong

The fifth round's table is not recoverable. It was reported in a chat message,
its identifiers were `M01` to `M46` and `N01` upward, and neither the message nor
any mapping from identifier to guard survives in this repository or in the commit
body. So the two disputed rows are answered by DESCRIPTION and re-measured here,
and the identifiers are retired rather than reused.

**M33, claimed 1 and measured 0. The measurement was right and the claim was
about a different mutation.** M33 is the commondir handler at `doctor.py:338`.
Deleting the whole handler kills one test, because a `PermissionError` from an
unreadable `commondir` then escapes to the blanket rescue. Narrowing its
`except (OSError, UnicodeDecodeError)` to `except OSError` killed zero, because
only the permission leg was ever driven and the `UnicodeDecodeError` member, the
entire reason the tuple has two, was covered by nothing. The claim of 1 was a
count taken against the handler and reported against the member. It is now R6-09
and it kills 1, driven by a `commondir` that is present and does not decode.

**M08, claimed 6 and measured 8. The verifier's measurement governs, and neither
number is reproducible now.** The best reconstruction of M08 is the empty mount
slot refusal in `identity_source`, which is round four's highest-count row (9 at
that revision) and the only guard in the unit whose count is in that range. It is
C-01 here and it now kills 13: five tests were added to that rule in rounds five
and six. The lesson is the one this file exists for. A count is a measurement of a
guard AND of the suite on the day it was taken, so a count that cannot be re-run
against a named guard is not evidence, and a claimed count that was never re-run
after the round's own tests landed is stale by construction.
