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

---

## Round seven, 2026-08-04

**Baseline: 3424 passed, 14 skipped, 3438 collected.** Measured on branch
`unit/u27-setup-wizard-and-doctor` with round seven's changes applied. EVERY
number below was measured against THAT tree, after the round's own tests landed,
because a count taken before them is stale by construction and this file already
records one round losing two counts that way.

Method, per `docs/mutation-rows.md` on `main`: one exact textual substitution,
the whole suite, count from the summary line, restore from a snapshot taken
before the substitution rather than with `git checkout`, which would throw away
the round's uncommitted work along with the mutation. `pyproject.toml` already
sets `addopts = "-q"`, so no second `-q` is passed and the summary line survives.

| id | file | guard | deaths |
|-|-|-|-|
| `M7-01-constructor` | `core/cause.py` | the refusal constructor classifies against its declared cause chain | 6 |
| `M7-02-sqlite-path` | `core/jobs.py` | the driver records WHICH database its error was about | 1 |
| `M7-03-require-path` | `core/cause.py` | a refusal with no path is not claimed as one | 3 |
| `M7-04-erofs` | `core/cause.py` | EROFS is a read only volume, not a permission to grant | 1 |
| `M7-05-locked` | `core/cause.py` | an immutable flag is a lock to clear, not a permission to grant | 1 |
| `M7-06-destination` | `core/cause.py` | a rename names the DESTINATION rather than the temporary file | 1 |
| `M7-07-session-record` | `core/session.py` | the session reader declares its cause, so the refusal can overrule it | 1 |
| `M7-08-session-ack` | `core/session.py` | the acknowledgment reader declares its cause | 1 |
| `M7-09-snapshot-manifest` | `core/snapshot.py` | the manifest reader declares its cause | 1 |
| `M7-10-setup-config` | `cli/setup.py` | the wizard's second read declares its cause | 1 |
| `M7-11-note-path` | `cli/render.py` | the access sentence names the path it is about | 4 |
| `M7-12-cycle-guard` | `core/cause.py` | the cause walk terminates on a chain that names itself | 1 |
| `M7-13-mountpoint-null` | `core/preflight.py` | `is_mount_point` answers an unrepresentable path | 1 |
| `M7-14-slot-null` | `core/preflight.py` | `slot_holds_a_volume` answers an unrepresentable path | 1 |
| `M7-15-doctor-config` | `cli/doctor.py` | `config.present` does not call an intact file corrupt | 1 |
| `M7-16-dispatch-config` | `cli/__init__.py` | a `ConfigError` reaching the dispatcher is classified | 1 |

### The row definitions

Each is the exact `old` -> `new` substitution. Applying it by hand reproduces the
count beside it.

**`M7-01-constructor`.** In `CratekitError.cause`:

    -        return classified(self._declared, self.__cause__)
    +        return self._declared

The round's whole subject. Eighteen of the nineteen `except OSError` sites in
the package that raise a structured refusal never reach either blanket, so the
correction happens where the refusal is BUILT. Reverting it takes every one of
them back to whatever token the site happened to write.

**`M7-02-sqlite-path`.** In `JobStore.__init__`:

    -        except sqlite3.Error as exc:
    -            name_the_database(exc, path)
    -            raise
    +        except sqlite3.Error:
    +            raise

`sqlite3.OperationalError` is not an `OSError`: no errno, no filename, no
`__cause__`. Without the path recorded at the connection site there is nothing
for the classification to measure, and a sealed `queue.db` exits `internal-error`
with "report it".

**`M7-03-require-path`.** In `_from_os_error`:

    -    if path is None:
    -        # A refusal with no path is not a refusal this program can tell anybody
    -        # how to fix, so it is not claimed as one. See ``AccessRefusal``.
    -        return None
    +    if path is None:
    +        path = ""

The over-classification guard. A kernel refusal with no path, which a bind to a
privileged port and a signal to another account's process both produce, is not
dressed up as a path to grant access to.

**`M7-04-erofs`.**

    -READ_ONLY_ERRNOS: frozenset[int] = frozenset({errno.EROFS})
    +READ_ONLY_ERRNOS: frozenset[int] = frozenset()

**`M7-05-locked`.** In `_from_os_error`, delete the immutable-flag loop and keep
only its final line:

    -        for candidate in (exc.filename2, exc.filename):
    -            if candidate is None:
    -                continue
    -            spelled = os.fsdecode(candidate) if isinstance(candidate, bytes) else str(candidate)
    -            if _immutable(spelled):
    -                return AccessRefusal(kind=AccessKind.LOCKED, path=spelled)
             return AccessRefusal(kind=AccessKind.PERMISSION, path=path)

**`M7-06-destination`.** In `_refused_path`:

    -    for candidate in (exc.filename2, exc.filename):
    +    for candidate in (exc.filename,):

MEASURED ZERO ON ITS FIRST RUN and it is recorded here rather than quietly
fixed. The locked-file leg finds its path through the flag rather than through
this ordering, so the ordering was covered by nothing. A rename into a directory
this account cannot write drives it directly, and the row kills 1.

**`M7-07-session-record`, `M7-08-session-ack`, `M7-09-snapshot-manifest`,
`M7-10-setup-config`.** At each of the four sites, drop the declaration:

    -        ) from exc
    +        )

Each is a site-local revert that defeats the central classification for that
site alone, which is what makes them four rows rather than one. `from exc` is the
author's statement that this failure IS that one, and it is exactly what
`classified` reads. `__context__` is still set under the mutation and is
deliberately not read.

**`M7-11-note-path`.** In `access_note`:

    -    return f"The path is {refusal.path}. {_ACCESS_SENTENCE[refusal.kind]}"
    +    return _ACCESS_SENTENCE[refusal.kind]

Round six's version of this clause killed ZERO, because the only assertion near
it was satisfied by the raw `{exc}` text that happens to repeat the path.

**`M7-12-cycle-guard`.** In `_chain`:

    -    while current is not None and id(current) not in seen:
    +    while current is not None:

Round six's version killed zero. Under the mutation the walk over a chain that
names itself does not fail, it stops responding, so the row is driven in a
subprocess with a deadline and the death is a `TimeoutExpired`.

**`M7-13-mountpoint-null`.** In `is_mount_point`, delete the `except ValueError`
clause and its comment, leaving the trailing `return False`.

**`M7-14-slot-null`.** In `slot_holds_a_volume`:

    -    try:
    -        behind = Path(slot).resolve()
    -    except ValueError:
    +    behind = Path(slot).resolve()
    +    if False:

Found by this round's own test for the row above. Guarding the seam alone left
its caller raising over an input the seam already handles.

**`M7-15-doctor-config`.** In `_check_config`:

    -        remedy=access_remedy(error, otherwise=Remedy(str(error.remedy))),
    +        remedy=Remedy(str(error.remedy)),

**`M7-16-dispatch-config`.** In the dispatcher's `except config.ConfigError`
branch, `cause=classified(Cause(...), exc)` -> `cause=(Cause(...))`. `ConfigError`
is not a `CratekitError`, so the refusal constructor never sees it and this hop
is the only place the classification can reach that family.

### Rows re-confirmed, and one count that changed

| id | guard | round six | round seven |
|-|-|-|-|
| C-01 | `identity_source` refuses a mount slot with nothing mounted in it | 13 | 13 |
| C-06 | the persisted `grant-path-access` slug in the remediation vocabulary | 6 | **10** |
| R6-02 | doctor's check runner attaches an access remedy to an unstructured break | 2 | 2 |
| R6-05 | `is_mount_point` confirms a False answer instead of calling an unstattable slot empty | 2 | 2 |
| R6-14 | `_membership` tolerates a configuration directory the operating system will not open | 2 | 2 |
| M33w | the WHOLE commondir handler in `doctor._git_dir`, deleted | 1 (claimed) | **2** |

C-06 rose from 6 to 10 because this round added four tests that assert the token,
which is the same effect the file already records for C-01 and is not a change of
behaviour. M33w was written down as 1 and measures 2; that claim is superseded
here rather than argued.

Row definitions for the confirm rows: C-01 replaces
`if slots and not any(slot_holds_a_volume(slot) for slot in slots):` with
`if False:` in `preflight.identity_source`. C-06 renames the enum value
`GRANT_PATH_ACCESS = "grant-path-access"` to `"grant-path-access-XX"`. R6-02
replaces `remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT)` with
`remedy=Remedy.REPORT_DEFECT` in `doctor.answer`'s blanket. R6-05 inserts
`return False` as the first statement of the `try` in `preflight.is_mount_point`.
R6-14 narrows `except (config.ConfigError, OSError):` to
`except config.ConfigError:` in `cli._membership`. M33w replaces the whole
`try` / `except (OSError, UnicodeDecodeError)` around the commondir read with the
bare return.
