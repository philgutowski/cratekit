# U28 independent adversarial review

Commit `ffded5c`, "feat(skills): twelve operator skills, the verb that installs
them, and two rules that stop them rotting (U28)".

Reviewed by an agent that did not write the code, in its own worktree, with its
own virtual environment built from the system Python 3.12 and verified to resolve
`cratekit` to that worktree's own `src`.

Paths in this file are written as `<repo>` and `<scratch>` because the
repository's own portability scan refuses an absolute home directory in a shipped
artifact.

## Verdict

**BLOCKING.** Three findings meet all three conditions of the merge bar in
`docs/METHOD.md`: each was driven end to end, each has a named user facing cost,
and for each the input is reachable with its producer driven.

The headline claim "twelve skills, zero lint problems" is true about the lint and
false about the skills. The lint is green and eight of the two hundred and
seventy eight fenced `crate` invocations in the twelve shipped skills exit 2 when
typed. The lint cannot see it because rule (g) checks verb paths and flags and
never checks a positional argument, and because it unions the root flag set into
every verb's allowed set.

| # | Finding | Class | Measured cost |
|---|---------|-------|---------------|
| 1 | Eight fenced commands in six shipped skills exit 2 | **BLOCKING** | 8 of 278 `crate` lines fail; 6 omit a required positional, 1 puts a root flag after the verb, 1 names a subcommand that does not exist |
| 2 | `crate skills install` deletes a user's own file inside a skill directory and reports `ok` | **BLOCKING** | file gone, `status: ok`, detail "already written by this build", `current: 12` |
| 3 | Two shipped skills state the opposite of how a profile disabled verb behaves | **BLOCKING** | `crate report library` under `slim` is argparse "invalid choice", exit 2, no cause, no remedy; 56 of 278 commands are affected |
| 4 | `first-run` says every setup answer can be supplied up front | residual | 2 of 8 questions have no flag; a scripted setup leaves `rekordbox.pins` failing, which refuses every database write |
| 5 | Rule (g) checks no positional argument at all | residual | 6 of the 8 commands in finding 1 pass the lint |
| 6 | Rule (g) unions the root flag set into every verb's allowed set | residual | 1 live violation, `crate name apply --decision ...` |
| 7 | Rule (g) skips any line ending in a backslash | residual | an entire multi line invocation is unchecked; measured on a synthetic skill |
| 8 | Rule (g) reads only lines whose first token is exactly `crate` | residual | `$ crate ...` and `sudo crate ...` bypass it; measured |
| 9 | Every fenced rule reads backtick fences only | residual | a four space indented block, this repository's own house style, bypasses rules (b), (c), (e), (g) and (h); so does a `~~~` fence |
| 10 | Rule (h) substring matches and does not split comment from command | residual | fires on `` `Medium` ``, `` `Lowercase` ``, and a fenced comment saying "High" |
| 11 | Rule (g) fires on a legitimate shell pipeline | residual | `crate status \| grep -v ok` is reported as naming an undeclared flag |
| 12 | A symlinked or file destination raises INTERNAL and leaves a partial install | residual | exit 1, "this is a defect; report it", 2 of 12 skills written |
| 13 | `package-data` ships only `SKILL.md` | residual | a second file in a skill directory exists in a checkout and in no wheel; measured by rebuilding |
| 14 | An empty skill directory installs and reports `ok` with no `SKILL.md` | residual | reachable in a checkout only; the lint catches it |
| 15 | Nothing pins that twelve skills ship | residual | eleven of twelve deleted, 38 of 38 skills tests still pass |
| 16 | `SKILLS_ROOT` pointing at nothing makes the real tree lint pass vacuously | residual | all 24 lint tests pass with zero skills present |
| 17 | The `--into` sample argument comment claims a hazard the autouse fixture already prevents | residual | `HOME` in the suite resolves to a pytest temporary directory |
| 18 | `default_target()` ignores `CLAUDE_CONFIG_DIR` | residual | unmeasured on a machine that sets it |
| 19 | `library-status` says "three of these seven verbs report, three move a job" | residual | four report, two move a job, one decides |
| 20 | Writing a mutation table that kills a portability guard reddens `scan_repo.py` | residual, pre-existing | the killed tests' parametrize ids carry the synthetic volume literal; scrubbed after measurement |

## Battery, from inside the worktree with its own venv

    ./.venv/bin/ruff check src tests scripts        All checks passed
    ./.venv/bin/python -m pytest --tb=no            6224 passed, 1 skipped in 256.92s
    ./.venv/bin/python scripts/scan_repo.py         exit 0, no output

    pytest --collect-only -o addopts=               6225 collected

The commit message's numbers reproduce exactly.

## Mutation headline

Full pass, driven by `scripts/mutate.py` from the main checkout against this
worktree. Table and JSON sidecar at
`docs/mutation/u28-skills-independent.md` and `.json`.

    rows run              45, the full pass cap exactly
    rows dropped          6, each logged in the spec with the reason it ranked below
    null control          0 deaths, so the apparatus is believable
    baseline              green, 6225 collected, re-established three times
    total deaths          72
    zero rows             10, seven user facing and three maintainer facing
    collect drift         1 row, R1_planned_in_restored, expected and explained below
    pytest invocations    27 in the final batch

The ten zero rows: `S1_shipped_names_dir_filter`, `S2_shipped_names_sorted`,
`S3_files_regular_only`, `S4_stamp_is_file`, `S6_stamp_key_exact`,
`L13_taxonomy_energy_bands`, `L15_skills_root_moved_back`,
`P3_empty_register_assertion`, `P4_is_absent_path_key`,
`K1_package_data_removed`. Every one was promoted to a full suite run before
being reported as a zero.

## Finding 1, BLOCKING. Eight fenced commands in six shipped skills exit 2

Every fenced line beginning `crate ` in all twelve skills was extracted and
handed to the real assembled parser with a full profile membership, the same
parser the lint's own `verb_table()` walks.

    cd <repo>
    ./.venv/bin/python  # the extractor is in <scratch>/, it reads
                        # src/cratekit/skills/assets/*/SKILL.md, splits the
                        # fenced blocks, and calls
                        # build_parser(membership=profiles.resolve("full")).parse_args

    total crate lines: 278   structurally invalid: 8

The eight, with the parser's own message:

| Skill | Command | Parser |
|-------|---------|--------|
| adopt-a-library | `crate audit coverage --limit 200` | the following arguments are required: EXPORT |
| adopt-a-library | `crate report library` | the following arguments are required: EXPORT |
| analyze-audio | `crate report library` | the following arguments are required: EXPORT |
| intake-and-name | `crate name apply --decision name.apply.confirm=apply` | unrecognized arguments: `--decision name.apply.confirm=apply` |
| restore-and-converge | `crate audit coverage --limit 200` | the following arguments are required: EXPORT |
| review-queue | `crate audit duplicates` | the following arguments are required: EXPORT |
| review-queue | `crate run show` | the following arguments are required: run_id |
| route-the-library | `crate audit coverage --limit 200` | the following arguments are required: EXPORT |

Four of them were then driven through the installed console script rather than
through `parse_args`, to confirm the exit status a person actually sees:

    cd <repo>
    ./.venv/bin/crate audit coverage --limit 200     exit 2
    ./.venv/bin/crate audit duplicates               exit 2
    ./.venv/bin/crate report library                 exit 2
    ./.venv/bin/crate run show                       exit 2

None of the eight is a placeholder problem. `crate audit coverage --limit 200`
appears in three separate skills as the verification step after a write, and
`library-reports` spells the same verb correctly in the same commit:

    crate audit coverage /path/to/export.xml --limit 2000

So two shipped skills disagree about the shape of one verb, and the lint passed
both.

**Reachability, condition 3.** The producer is `crate skills install`, and it was
driven:

    cd <repo>
    ./.venv/bin/crate --decision profile.set.apply=apply profile set full
    ./.venv/bin/crate skills install --into <scratch>/target

    skills.install: ok
      [ok  ] skill.adopt-a-library: written to <scratch>/target/adopt-a-library
      ... twelve of these ...

    ls <scratch>/target/first-run
    .cratekit-skill.toml   SKILL.md

The twelve `SKILL.md` files land on a person's machine, unaltered, from the verb
this commit ships.

**Why the lint cannot see it.** `_verb_problems` consumes the verb path greedily
while it stays a prefix of a real path, then treats everything after it as a
value and scans only for tokens beginning with a dash. A missing required
positional is not a token, so nothing looks for it. That is finding 5. The
`--decision` case is finding 6.

## Finding 2, BLOCKING. The install verb deletes a user's file and reports ok

`install_one` calls `shutil.rmtree(destination)` whenever the destination exists,
including on the path where it has just decided the copy is `current`. The report
for that path says the copy was "already written by this build" and the check
status is `ok`.

Driven against an unmodified copy of the commit's tree in the scratch directory,
so the running mutation table could not have contaminated it:

    first install: 0 {'current': 0, 'installed': 12, 'refreshed': 0, ...}
    notes exist before second run: True
    second install: 0 {'current': 12, 'installed': 0, 'refreshed': 0, ...}
    reported status: ok | detail: "already written by this build at .../first-run"
    notes exist AFTER second run: False

The file written between the two runs was
`<scratch>/userfile/first-run/MY-NOTES.md`, containing one line of the operator's
own working notes. It is gone, the summary says twelve copies were already
correct, and no check is anything other than `ok`.

**The cost is both halves of the bar at once.** Someone loses data, and is shown a
clean report over the state the tool just destroyed.

**Reachability, condition 3.** The producer is a person or an agent writing a file
into an installed skill's directory, and that shape is not hypothetical: this
commit's own lint carries
`tests/test_skills_lint.py::test_extra_files_in_a_skill_directory_pass`, which
establishes a skill directory holding more than `SKILL.md` as a supported shape.
The producer was driven with a one line write, above.

**The mechanism, and it is a registry declaration rather than a bug in the loop.**
`crate skills install` is the only verb in the product that calls `shutil.rmtree`
on a directory the caller names. Its registry entry declares
`writes=frozenset()`, so conformance 8 asks nothing of it, and it does not
declare `destructive`, so conformance 6 asks nothing of it either:

    src/cratekit/cli/registry.py:1432   name="skills.install"   no writes=, no destructive=
    tests/test_cli_contract.py:1944     [e for e in ALL_ENTRIES if e.destructive]
    tests/test_cli_contract.py:2074     if entry.writes: assert entry.doctor_checks

The module docstring argues the exemption at length, on the grounds that the verb
"touches an agent's configuration directory and nothing the library knows about".
That is true and it is not the same claim as "nothing there is worth keeping".

Neither `crate skills install --help` ("where to write the copies") nor any of
the twelve skills says the destination is replaced whole.

The narrow fix is to stop removing on the `current` path, or to remove only the
files this build ships plus the stamp. The stated reason for replacing whole,
that a withdrawn file must disappear, is served by the second.

## Finding 3, BLOCKING. Two skills state the opposite of the refusal model

Three of the twelve skills explain what happens when the active profile does not
include a verb's module. They do not agree, and the majority answer is wrong.

`analyze-audio`, lines 187 to 190, is CORRECT:

> If the active profile does not switch the analysis module on, the verbs are not
> built at all and the shell reports an unknown command.

`first-run`, under "Profiles decide which modules exist", is WRONG:

> A verb belonging to a module the active profile does not include is not hidden,
> it refuses and says why, so the answer to "why does this verb not work" is
> usually here.

`library-reports`, under "When one of them refuses to run at all", is WRONG, and
names the exact two verbs it is wrong about:

> The duplicate audit rides on its own module, and both reports ride on the
> reports module, so a profile with those switched off gives a refusal naming the
> module rather than hiding the verb.

Driven. A library was configured through `crate setup` with `--profile slim`,
which is the profile `first-run` itself instructs a reader to set:

    cd <repo>
    ./.venv/bin/crate profile show          module.reports: off, module.duplicates: off
    ./.venv/bin/crate audit duplicates
      crate audit: error: argument <command>: invalid choice: 'duplicates'
                   (choose from 'coverage')                              exit 2
    ./.venv/bin/crate report library
      crate: error: argument <command>: invalid choice: 'report'
             (choose from 'profile', 'run', 'setup', ...)                exit 2

No cause, no reason, no remedy, no mention of a module. The source agrees with
`analyze-audio` and not with the other two:

    src/cratekit/cli/__init__.py:222
        if not entry.available_to(resolved):
            continue

The verb is never added to the parser. The stub path that does show a present
verb refusing with a name, five lines below, is for a missing EXTRA, which is a
different condition.

**Scale, measured.** Every fenced `crate` line in all twelve skills was parsed
against a `full` membership and a `slim` membership:

| skill | crate lines | valid at full | valid at slim |
|-------|------------:|--------------:|--------------:|
| adopt-a-library | 25 | 23 | 23 |
| analyze-audio | 25 | 24 | 16 |
| first-run | 12 | 12 | 12 |
| intake-and-name | 36 | 35 | 29 |
| label-catalogues | 29 | 29 | 12 |
| library-reports | 20 | 20 | 13 |
| library-status | 18 | 18 | 18 |
| remove-tracks | 16 | 16 | 7 |
| restore-and-converge | 29 | 28 | 28 |
| review-queue | 23 | 21 | 19 |
| route-the-library | 24 | 23 | 23 |
| sync-and-publish | 21 | 21 | 14 |
| **total** | **278** | **270** | **214** |

Fifty six commands stop existing under the slim profile, and the shipped
explanation for that state is wrong in two of the three places it is given.

`crate skills install` is itself one of them. `module.skills` is off in the slim
preset, so on a machine set up the way `first-run` describes, the verb that
installs the skills does not exist:

    ./.venv/bin/crate skills install --into <scratch>/target
      crate: error: argument <command>: invalid choice: 'skills'         exit 2

## Finding 4, residual. "Every answer can be supplied up front" is false

`first-run` says:

> Every answer can be supplied up front instead, which is what makes the one
> interactive verb scriptable

followed by `crate setup --library-root /path/to/library --profile slim`.

Driven with standard input at end of file, which is the scripted case the
sentence is about:

    ./.venv/bin/crate setup --library-root <scratch>/lib --profile slim < /dev/null
      config-unusable: library.db_path has no recorded value and no question
      could be asked (standard input is at end of file)                  exit 30

With every declared flag supplied, the wizard still asks two questions that have
no flag: whether to record the installed rekordbox version as the pin, and
whether to record the provider credential. Both default to no, and the first one
matters:

    [FAIL] rekordbox.pins: no rekordbox application version is pinned, so every
           database write refuses
           fix: crate setup

So a reader who follows the sentence and scripts the wizard ends with a library
whose every database write refuses, and the remedy is the interactive wizard the
sentence said was avoidable.

Filed as a residual rather than as blocking because on a terminal the wizard asks
and the person answers, and `crate doctor` names the remaining failure with its
fix. The false clause costs a scripted run rather than a normal one.

## Findings 5 to 11, residual. What rules (g) and (h) do not see

Each was measured by calling `lint_skills` against a synthetic skill with the
REAL verb table and the REAL taxonomy names, not the fixtures' synthetic ones.

| Probe | Result |
|-------|--------|
| `crate no-such-verb-at-all \` then a continuation line | PASSES CLEAN |
| `crate name apply --decision name.apply.confirm=apply` | PASSES CLEAN |
| `crate audit coverage --limit 200` | PASSES CLEAN |
| `$ crate no-such-verb --no-such-flag` | PASSES CLEAN |
| `sudo crate no-such-verb --no-such-flag` | PASSES CLEAN |
| four space indented block with a bogus verb and a bogus script | PASSES CLEAN |
| `~~~bash` fence with a bogus verb and a bogus script | PASSES CLEAN |
| `crate status \| grep -v ok` | CAUGHT, wrongly: "does not declare the flag '-v'" |
| `crate doctor && crate status` | PASSES CLEAN |

**Finding 5, positionals.** Nothing in `_verb_problems` looks at a positional.
Six of the eight commands in finding 1 are missing a required one.

**Finding 6, the root flag union.** `allowed = set(verbs[path]) | set(verbs[()])`
means a flag the root declares is accepted anywhere after the verb. `--decision`
is a root flag that must precede the verb, and `intake-and-name` writes it after.
Three other skills spell the same flag correctly, before the verb.

**Finding 7, continuation lines.** `if line.rstrip().endswith("\\"): return []`
returns before the verb path is walked, so the first line of a multi line
invocation is not checked and the remaining lines are not checked either, because
they do not begin with `crate`. A whole invocation can be hidden by writing it
across two lines. No shipped skill currently does.

**Finding 8, the entry point filter.** `tokens[0] != "crate"` excludes every
prefixed form. A prompt marker, `sudo`, `time`, `env FOO=1` and `uv run` all
defeat the rule.

**Finding 9, and this is the widest one.** `_FENCED` matches backtick fences
only. A four space indented code block, which is CommonMark and which is this
repository's own house style in `CLAUDE.md` and in `docs/METHOD.md`, is invisible
to rules (b), (c), (e), (g) and (h) together. So is a `~~~` fence. A skill author
following the conventions of the documents they were told to read would produce
unlintable skills and nothing would say so.

The same hole is the answer to the rule (h) question. With the real taxonomy
names loaded:

| Probe | Result |
|-------|--------|
| a display name inside a four space indented block | PASSES CLEAN |
| a display name inside a `~~~` fence | PASSES CLEAN |
| a display name in `**bold**` prose written as a path | PASSES CLEAN |
| a display name inside a backtick fence, control | CAUGHT |

**Finding 10, rule (h) fires on correct content.** The match is
`if name in span`, a substring test, and the span list is
`_CODE_SPANS.findall(text) + _FENCED.findall(text)`, which is the RAW fenced
text rather than the command half that rules (b) and (g) carefully separate.
The energy bands are `High`, `Med` and `Low`. Measured:

| Probe | Result |
|-------|--------|
| `` `Medium` `` in prose | FIRES on `Med` |
| `` `Lowercase` `` in prose | FIRES on `Low` |
| a fenced COMMENT reading `# a High confidence match` | FIRES on `High` |
| `` `--technology` ``, control | clean |

This is the P7 shape the commit message says the scoping decision avoids. The
scoping avoids it for whole files and reintroduces it inside code spans, and
`Med` and `Low` are three letter substrings of ordinary English words.

**Finding 11.** `crate status | grep -v ok` reports `-v` as a flag
`crate status` does not declare, because everything after the verb path is
scanned for leading dashes without regard for what ended the command. Also P7.

## Finding 12, residual. A symlinked or file destination raises INTERNAL

`install_one` calls `shutil.rmtree(destination)` on anything that exists.
`shutil.rmtree` refuses a symlink and raises on a file, and neither is caught.

Driven. A skill directory symlinked to a directory the operator maintains
themselves, which is a common way to keep agent skills under version control:

    ln -s <scratch>/symcase/mine/first-run <scratch>/symcase/target/first-run
    ./.venv/bin/crate skills install --into <scratch>/symcase/target

    skills.install: failed (INTERNAL)
    internal-error: OSError: [Errno None] None: PosixPath('.../first-run')
      fix: this is a defect; report it with the cause identifier below
                                                                        exit 1

And with a regular file at the same path:

    internal-error: NotADirectoryError: [Errno 20] Not a directory: ...
                                                                        exit 1

In both cases the loop stops at the first offending name in sorted order, so
`adopt-a-library` and `analyze-audio` are installed and the other nine are never
attempted. The person's own content is not destroyed, which is the one good part.

`tests/test_skills_install.py::test_a_refusal_leaves_no_half_written_target`
covers the `into.mkdir` refusal only. The per skill loop has no such guarantee
and the test's name is wider than what it measures.

**Path traversal, asked and answered no.** `shipped_names()` derives names from
`packaged_root().iterdir()`, which cannot yield a separator or a dot entry, so no
name reaches outside the target. The only way to have the verb delete something
unexpected is to point `--into` at a directory that already holds a directory
named after a shipped skill, which is finding 2 rather than traversal.

## Finding 13, residual. The wheel ships only SKILL.md

The packaging claim was verified rather than argued. A clean tree of `ffded5c`
was extracted and a wheel built from it:

    python -m pip wheel --no-deps -w <scratch>/dist <scratch>/pkgsrc
    Successfully built cratekit

    cratekit/skills/assets/adopt-a-library/SKILL.md
    ... twelve of these ...
    SKILL.md count: 12

**The claim holds.** The twelve skills are inside the wheel.

What the same experiment also shows is that `[tool.setuptools.package-data]`
names `assets/*/SKILL.md` and nothing else. A second file was added to one skill
and the wheel rebuilt:

    ['cratekit/skills/assets/first-run/SKILL.md']

`REFERENCE.md` and `nested/DEEP.md` did not ship. Meanwhile `_files()` copies
every regular file one level deep and the lint asserts extra files are legal.
So a supporting document added beside a `SKILL.md` tomorrow would exist in the
checkout, pass the lint, be installed by a development checkout, and be absent
from every wheel. That is the same defect shape the commit message says the
package location decision avoided, one level further in. No live cost today: all
twelve directories hold exactly `SKILL.md`.

## Findings 14 to 16, residual. What the skills suite does not hold

**Finding 14.** An empty directory under `assets/` is offered by `shipped_names()`
and installed:

    [ok  ] skill.zz-half-written: written to <scratch>/emptycase/zz-half-written
    ls -a <scratch>/emptycase/zz-half-written    .cratekit-skill.toml

A stamp and no skill, reported `ok`. The lint does catch it
(`zz-half-written: missing SKILL.md`), and a wheel cannot contain it because the
glob requires a `SKILL.md`, so this is reachable in a checkout only. The
directory was removed and `git status` verified clean afterwards.

**Finding 15.** Nothing pins that twelve skills ship, and nothing names one.
Measured on an independent copy of the tree:

    eleven of twelve skill directories moved aside
    pytest tests/test_skills_install.py tests/test_skills_lint.py
    38 passed

Both count assertions derive the expected value from the code under test:
`summary["installed"] == len(shipped_names())` and
`written == {e.name for e in packaged_root().iterdir()}`. Five of the fourteen
install tests have this shape. The floor the suite actually holds is "at least
one skill exists", which comes from
`assert shipped, "the package ships no skills, so this proves nothing"`.

**Finding 16.** With ALL twelve moved aside, `tests/test_skills_lint.py` passes
all 24 of its tests, because `lint_skills` globs a root and reports nothing when
the glob is empty. `test_real_skills_pass_lint` therefore cannot distinguish
"the skills are clean" from "SKILLS_ROOT points at nothing", which is exactly the
state the constant was in before this commit moved it.

## Findings 17 to 19, residual. Three small ones

**Finding 17.** The new entry in `tests/test_cli_contract.py::_sample_arguments`
justifies its `--into` with "a bare drive would write twelve directories into a
person's actual configuration". Measured: `tests/conftest.py`'s autouse
`_isolate_state_roots` sets `HOME`, so inside the suite

    Path.home()             <pytest tmp>/pytest-569/state_roots0/{home}
    default_target()        <pytest tmp>/pytest-569/state_roots0/{home}/.claude/skills

The flag is still the right thing to pass. The reason given for it is a hazard
the fixture already removed, which is METHOD's defect pattern 4: a justification
whose number was never taken on the tree.

**Finding 18.** `default_target()` composes `Path.home() / ".claude" / "skills"`.
Claude Code honours `CLAUDE_CONFIG_DIR`, and this ignores it, so on a machine
that sets it the copies land where nothing reads them and the verb reports `ok`.
Not driven, because doing so would require establishing what the agent reads on
this machine, and that is the agent's convention rather than this product's. The
reachability is UNMEASURED and the report says so.

**Finding 19.** `library-status` opens with "Three of these seven verbs report,
three move a job, and one records a decision." Counting the seven it then
documents: `status`, `job list`, `job show` and `run show` report, which is four;
`job resume` and `job cancel` move a job, which is two; `run decide` records a
decision.

## What was checked and found correct

Stated because a review that lists only defects reads as a survey of everything.

* **The wheel carries the skills.** Twelve `SKILL.md` files, verified by building
  and unpacking rather than by reading `pyproject.toml`.
* **No skill instructs anyone to write a beat grid.** Every occurrence of tempo,
  BPM and grid across the twelve was read. Four skills restate the prohibition
  and none contradicts it. `analyze-audio` gives the octave folding reason.
* **Every gate name and every gate option cited in a skill is real.** Nine gates,
  checked against `src/cratekit/cli/registry.py`: `adopt.apply.approve`,
  `delete.review.confirm`, `export.playlist.confirm`, `name.apply.confirm`,
  `profile.set.apply`, `restore.run.confirm`, `route.inbox.apply`,
  `sync.favorites.confirm`, `write.cloudsync.unreadable`. Every option spelled in
  a skill is one the gate declares.
* **Every review queue slug is real.** Eight of eight against `review.Queue`. The
  four `--kind` values are real too: `adoption-collision`, `harvested-label`,
  `label-release`, `duplicate-recording`. The `rv_` item identifier in
  `review-queue` is the right prefix and the right length, 24 hex characters.
* **The countdown discharge is complete.** `_pending.PENDING == {}` at run time,
  `EXPECTED_PENDING == frozenset()`, and `grep -rn 'requires(' tests/` finds no
  decorator site at all, only prose and failure messages.
* **The collected count reconciles by identifier**, under `LC_ALL=C`, not by
  total:

      origin/main   6201 collected
      ffded5c       6225 collected

      only in main, 2:   test_a_planned_verb_whose_module_has_landed_must_lose_its_marker[skills.install]
                         test_a_pending_target_that_has_landed_must_be_removed_from_the_registry[path:skills]
      only in head, 26:  3 conformance ids for skills.install, 14 in test_skills_install.py,
                         6 in test_skills_lint.py, 2 in test_pending_units.py,
                         and test_the_empty_register_is_a_discharged_register_and_not_a_lost_one

  Nothing collapsed out of collection.
* **R-158's claim is true.** `_is_absent("path:skills")` answers `True` on this
  tree and `<repo>/skills` does not exist, so the countdown could never have
  fired.
* **Residual numbering is clean.** No duplicate `## R-` heading, and
  `git diff origin/main -- docs/residual-findings.md | grep '^-## R-'` is empty.
* **No symbol collisions from the new module.** `STAMP_NAME`, `DEFAULT_TARGET`,
  `packaged_root`, `shipped_names`, `install_one`, `installed_version`,
  `default_target` and `_files` are each defined once in `src`. No duplicate
  `name=` in the registry's `ENTRIES`.

## Finding 20, residual, and it is about the review apparatus rather than U28

`docs/METHOD.md` tells every reviewer to write the mutation table into
`docs/mutation/`. Doing that reddens the merge battery whenever a row kills a
test in `tests/test_portability.py`.

Row `X2_mount_rule_removed` kills three parametrized cases of
`test_guard_covers_every_shipped_surface`, and those cases carry the synthetic
volume literal in their parametrize IDs. `tests/test_portability.py` assembles
that literal at runtime, from concatenated fragments, precisely so it never
appears in the tree. Recording killed node ids materialized it, and then:

    ./.venv/bin/python scripts/scan_repo.py
    repository scan found content that must not ship:
      docs/mutation/u28-skills-independent.json: hardcoded volume path ...
      docs/mutation/u28-skills-independent.md: hardcoded volume path ...
                                                                        exit 1

The literal in both artifacts was replaced by a placeholder after measurement,
the substitution is recorded in the table's own header, no count was touched, and
the scan is green again. This is pre-existing and not a defect in `ffded5c`; it
is recorded because the next reviewer who mutates a portability guard will hit
it, and because the failure presents as a red battery on a clean tree.

## The mutation table

Full row descriptions, the mutated text, and the killed node ids are in
`docs/mutation/u28-skills-independent.md`. What follows is the reading.

### The install verb is held where it matters and not at its edges

Sixteen of the twenty rows over `src/cratekit/skills/cli.py` killed something.
The strongest are the ones a person would notice:

| row | what it removed | deaths |
|-----|-----------------|-------:|
| `S14_into_ignored` | `--into` ignored, the default target always used | 8 |
| `S5_stamp_quote_strip` | stamp quotes no longer stripped | 5 |
| `S8_outcome_collapse_refreshed` | every pre-existing copy called `current` | 3 |
| `S9_previous_always_none` | the existing stamp never read | 3 |
| `S16_counts_miscounted` | every skill counted as installed | 3 |
| `S11_typed_cause_lost` | the mkdir `OSError` no longer typed | 2 |
| `S12_reason_slug` | the reason slug swapped for a neighbour | 2 |
| `S7_replace_whole` | the destination copied over rather than replaced | 1 |
| `S15_drift_never_warns` | every check reported `ok` | 1 |
| `S17_outcome_always_ok` | `NO_OP` never reached | 1 |
| `S18_detail_reworded` | the refreshed sentence reworded, not appended to | 1 |
| `S19_default_target_literal` | `default_target` stopped composing from home | 1 |
| `S20_packaged_root_via_file` | `packaged_root` resolved from `__file__` | 1 |
| `S13_expanduser` | `--into` stopped expanding a tilde | 1 |
| `S10_stamp_skill_name` | the stamp stopped naming its own skill | 1 |

`S7` deserves a note. Replacing the destination whole is the decision behind
finding 2, and exactly ONE test holds it,
`test_a_file_this_build_no_longer_ships_disappears`. That test asserts a
withdrawn file disappears. Nothing asserts anything about a file the person put
there, which is why finding 2 passes a green suite.

### Four zero rows are the input filters, and each guards correct behaviour nothing supplies input for

`S1`, `S2`, `S3` and `S4` are user facing, so each owes a composite.

**`S1`, the directory filter in `shipped_names`, 0 deaths.** Composite, driven
against an independent copy of the tree with a stray file planted beside the
skill directories:

    echo "..." > src/cratekit/skills/assets/README.md
    shipped_names() -> 12 names, README.md included? False
    crate skills install -> exit 0, installed 12

The guard is correct and reachable. No test plants the file, so removing the
guard kills nothing.

**`S2`, `sorted()` in `shipped_names`, 0 deaths.** Composite, by observation of
the driven verb: the twelve checks are reported alphabetically,
`adopt-a-library` through `sync-and-publish`. That ordering is what a person
reads and what an agent would diff between runs, and nothing asserts it.

**`S3`, the regular-file filter in `_files`, 0 deaths.** Composite, driven with a
nested directory planted inside a skill:

    src/cratekit/skills/assets/first-run/nested/DEEP.md created
    copy contains: ['.cratekit-skill.toml', 'SKILL.md']
    nested/ shipped into the copy? False

Correct, reachable, untested. It is also the mechanism behind finding 13: a
nested file is dropped silently rather than reported.

**`S4`, `stamp.is_file()` rather than `exists()`, 0 deaths.** Composite:

    a directory named .cratekit-skill.toml planted in a skill copy
    installed_version(...) -> None            # reads as unstamped, then refreshed
    without the guard, read_text() raises IsADirectoryError

Defensive against a state nothing in the product produces. Correct to keep,
correct that it kills nothing.

**`S6`, the exact match on the `version` key, 0 deaths, maintainer facing.** One
line, as METHOD asks: a `version_written_by` line would win under a prefix match,
and no stamp has ever carried a second key.

### The lint rules are held, and rule (h)'s name SOURCE is not

Twelve of the fifteen rows over `tests/test_skills_lint.py` killed something.
`L1` removing rule (g) entirely killed 2. `L2`, `L4` and `L5`, the three
mechanisms inside the walker, killed 2, 2 and 3. `L6`, `L7` and `L8`, the three
halves of rule (h), killed 1 each. `L10`, the fence regex reverted to the source
system's `[a-z]*` form, killed 1, so the documented evasion stays closed. `L11`,
removing rule (d)'s delegation to the portability scanner, killed 2.

Two zero rows, both user facing.

**`L13`, dropping the energy bands from `taxonomy_display_names`, 0 deaths.**
Composite:

    taxonomy names lost when the bands are dropped: ['High', 'Low', 'Med']
    occurrences of those names inside a code span or fence, all twelve skills: 0

Rule (h)'s matching mechanism IS held: `L8` turning the substring test into
equality killed 1. What is not held is where the names come from, because the
fixtures pass `taxonomy_names=` explicitly and the real derivation is exercised
only by `test_real_skills_pass_lint`, which currently has nothing to find. A
taxonomy edit that dropped a band would be invisible.

**`L15`, `SKILLS_ROOT` moved back to a repository-root `skills` directory,
0 deaths.** This is finding 16 and the composite is in that section: with the
root pointing at nothing, all 24 tests in `tests/test_skills_lint.py` pass. The
real-tree test cannot tell a clean tree from an absent one.

### The register and the pins

`P1` and `P2`, the two AST fixes this commit made so the empty register could be
read at all, killed 1 each, so both repairs are held. `C1`, putting the at-risk
population pin back to 73, killed 1, so the re-pin is real.

`P3` and `P4` are zero rows and both are maintainer facing, so one line each.
`P3`: the new `test_the_empty_register_is_a_discharged_register_and_not_a_lost_one`
asserts its own condition and nothing asserts it in turn, which is what a
self-stating test is. `P4`: changing how `_is_absent` resolves a `path:` key
kills nothing, because the register is empty and no `path:` key exists to
resolve. That is R-158 measured rather than argued.

`R1`, restoring `planned_in="U28"` on the registry entry, killed 1 AND drifted
the collected count from 6225 to 520 on its subset, which is the driver reporting
that the conformance parametrization shrank. Expected: a planned entry is
excluded from the landed-entry parametrizations, which is exactly the arming this
unit performed.

### Packaging

`K1_package_data_removed`, deleting the `package-data` line, killed 0 on the full
suite, and it is user facing. This is the most important zero in the table: with
that line gone, no wheel carries a single `SKILL.md`, and the entire suite is
green. Nothing in the repository tests the built artifact.

Its composite ran in the table. `K1_composite` breaks `packaged_root()` so the
shipped assets cannot be resolved, and killed 9. So the suite holds "the assets
are resolvable from the source tree" firmly and holds "the assets are in the
wheel" not at all. The claim was verified by hand instead, in finding 13.

### The existing-guard sample

`X1_placeholder_exemption` killed 2 and `X2_mount_rule_removed` killed 4, so the
portability scanner's two rules that rule (d) now depends on are both genuinely
held.

### Rows dropped, and why they ranked below the cap

The spec logs six. Recorded here so the truncation reads as a truncation rather
than as coverage.

| id | why it was dropped |
|----|--------------------|
| `S21_stamp_name_constant` | the stamp's content and its `is_file` gate are already measured by S4, S5, S6 and S10; a rename re-measures the same read path |
| `L16_rule_b_command_token` | rule (b) is not in this commit's diff and its fixtures are unchanged |
| `L17_rule_f_deep_ref` | rule (f) is unchanged and no shipped skill carries a deep reference, so the row would measure a rule with no live input |
| `L18_rule_e_year` | rule (e) is unchanged and the commit's claim rests on rules (g) and (h), which are measured across nine rows |
| `S22_build_flag_default` | S13, S14 and S19 already measure the three ways the target can resolve wrongly |
| `X3_beat_grid_guard` | no line in this commit touches a write path, and the twelve skills were read for grid writing instructions separately and carry none |

One further truncation, stated plainly. METHOD asks a user facing zero row to
carry a composite, and the pass was already at the 45 row cap when the zeros were
known. Only `K1` has an in-table `pairs_with` composite. The composites for `S1`,
`S2`, `S3`, `S4`, `L13` and `L15` were measured OUTSIDE the table, by driving the
verb or the checker against planted input, and each one's exact measurement is
printed in its section above. They are real measurements and they are not
mutation rows, and this paragraph exists so nobody reads them as rows.

### Driver incidents during this pass

Recorded because METHOD's driver rules were bought by incidents like these.

1. The first batch was killed by the harness at the sixty minute mark, part way
   through row `L13`, leaving `tests/test_skills_lint.py` mutated. It was
   restored by rewriting the bytes from `git show HEAD:tests/test_skills_lint.py`
   and verified byte identical against that same source, never against a scratch
   copy. `git diff` was empty afterwards.
2. The first resume REFUSED to run, correctly, because the baseline was red: this
   review file itself carried a path that `tests/test_portability.py` rejects.
   The driver named the failing test and ran no row. That is the guard working,
   and it is the reason every path in this document is a placeholder.
3. The batch was completed with `--resume`, which reused the 32 rows whose text
   had not changed and measured the remaining 13. The baseline was
   re-established green before those rows ran.

