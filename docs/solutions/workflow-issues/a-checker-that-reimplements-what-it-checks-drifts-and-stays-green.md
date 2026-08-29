---
title: "A checker that reimplements what it checks drifts from it, and the drift is invisible because the checker is green"
date: 2026-08-24
category: workflow-issues
module: "tests/test_skills_lint.py"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "A test or lint rule is about to validate a command line, a config, or a payload that a real parser or loader in the product already validates"
  - "A guard builds its own table of what is legal by walking the code it is supposed to be checking against"
  - "A rule is being taught which flags consume the next token, which is argparse nargs handling written a second time"
  - "Shipped documentation carries fenced commands and a suite is cited as proof that those commands run"
  - "A green checker is the only evidence that the artifacts it covers are correct"
symptoms:
  - "Eight fenced commands across six of twelve shipped skills exit 2 when typed, and the lint covering them is green"
  - "Six of the eight omit a required positional, which the hand rolled walker checked nowhere at all"
  - "A flag that takes a value has its value read as a subcommand, and the repair is a table of which flags consume the next token"
  - "One command puts a root flag after the verb path where argparse will not take it, and the walker accepts it"
  - "The hand written correction contains a ninth defect that the real parser rejects on its first run"
related_components:
  - "development_workflow"
  - "documentation"
tags:
  - "guard"
  - "argparse"
  - "cli"
  - "test-fidelity"
  - "silent-failure"
  - "skills-lint"
---

# A checker that reimplements what it checks drifts from it, and the drift is invisible because the checker is green

## Context

U28 shipped twelve operator skills and the verb that installs them. It merged to
`main` as `f55b3ea` with the trailer `Closes #28`. The fix this learning is about
is `c24411c`, verified reachable from `main` with
`git merge-base --is-ancestor c24411c main`, which returned exit 0. This
repository forbids pull requests by contract, so the commit is the citation and
there is no PR number to give.

Among the rules U28 added to `tests/test_skills_lint.py` was rule (g), applied at
`tests/test_skills_lint.py:336`, one line per fenced command in every shipped
`SKILL.md`. Its job is one sentence. A `crate` invocation printed in a skill must
be a command a person can actually type.

It was implemented as a hand rolled token walker. The before is
`git show c24411c^1:tests/test_skills_lint.py`, where `verb_table()` at `:105`
walks the assembled parser to build a mapping from verb path to flag table, and
`_verb_problems` at `:158` walks the tokens of a line against that mapping. That
is three of argparse's jobs done by hand, subcommand resolution, option parsing,
and validation, and it checked NO POSITIONAL ARGUMENT AT ALL.

An independent adversarial review found the cost, recorded in
`docs/u28-skills-review.md`, finding 1 at `:82`. Of 278 fenced `crate` lines in
the twelve skills, eight exit 2 when a person types them, spread across six of
the twelve. The review's evidence is a table at `:100` through `:108` plus four
of the eight driven through the installed console script at `:113` through
`:116`.

Re-driven locally for this document rather than taken from the review, because
`docs/METHOD.md:166` names "a fix justified by a measurement taken on a fixture
rather than on the tree" as the most dangerous of the four defect patterns, and a
fix justified by somebody else's confident number is that pattern. Both lints
were loaded from source and run over the pre fix skills tree materialised with
`git archive c24411c^1 src/cratekit/skills/assets`:

    OLD LINT on the OLD TREE: 0 problems
    NEW LINT on the OLD TREE: 8 problems

    adopt-a-library       crate audit coverage --limit 200   required: EXPORT
    adopt-a-library       crate report library               required: EXPORT
    analyze-audio         crate report library               required: EXPORT
    intake-and-name       crate name apply --decision ...    unrecognized arguments
    restore-and-converge  crate audit coverage --limit 200   required: EXPORT
    review-queue          crate audit duplicates             required: EXPORT
    review-queue          crate run show                     required: run_id
    route-the-library     crate audit coverage --limit 200   required: EXPORT

Zero and eight over the same twelve files, same parser, same rule name. The old
number is the one `test_real_skills_pass_lint` reported on every run, which is
why the suite was green while eight shipped commands were broken.

The fix deleted the walker. `_verb_problems` at `tests/test_skills_lint.py:155`
now strips a prompt marker, truncates at a shell operator, tokenises with
`shlex`, and hands the result to `parse_args` on a parser built from the registry,
trapping `SystemExit`. It caught a ninth defect immediately, in the correction
itself. `crate profile set PRESET-NAME` had been written as a placeholder, and
driving it against the real parser gives:

    crate profile set: error: argument name: invalid choice: 'PRESET-NAME'
    (choose from 'slim', 'full', 'custom')

## Guidance

**A checker that reimplements the thing it checks will drift from it, and the
drift is invisible because the checker is green.** Hand the input to the real
thing instead. The only checker that cannot disagree with the target is the
target. Everything else is a second implementation of the same semantics,
maintained by a person who has no way to notice when the first one moves.

**The dangerous drift is not in the rules you wrote, it is in the rules you never
knew you were writing.** The walker was correct about the two things it modelled.
It resolved verb paths and it checked flags, and its fixtures proved both. What
it did not model was that a command also has positional arguments, and a model's
silence produces no error, no warning, and no failing test. Seven of the eight
defective commands were missing a required positional. The walker did not get
them wrong, it never asked.

**The first repair that reimplements one more piece of the real thing is the
signal to stop, and it arrives before the damage.** This walker had ALREADY
drifted once, and the incident is documented inside the before file's own code at
`:117` through `:123`. It read the `json` in `crate --output json sync` as a
subcommand and reported a correct command as naming no real verb. The repair was
to record, per flag, whether it consumes the following token:

```python
        found = {
            prefix: {
                name: action.nargs != 0
                for action in parser._actions
                for name in action.option_strings
            }
        }
```

That is argparse's `nargs` handling, reimplemented, and the comment above it even
says the fixture found it rather than a reading of the function. A repair whose
content is "teach my model one more rule of the target's grammar" is the moment
to delete the model.

**Fixtures written against your model cannot compare your model to the real
thing, and this is the mechanism behind the green suite.** The before file's
fixtures ran against `_FIXTURE_VERBS` at `:382`, a hand written dictionary in
exactly the walker's shape:

```python
_FIXTURE_VERBS: dict[tuple[str, ...], dict[str, bool]] = {
    (): {"--output": True, "-h": False, "--help": False},
    ("sync",): {"--ok": False, "--track-limit": True},
}
```

Every rule bit against that structure, and every rule was proved. What no fixture
could ask is whether the walker AGREED WITH ARGPARSE about what a valid command
is, because the fixture and the walker are two expressions of one model. Two
implementations can only be compared by running both.

**Replace the fixture table with a real instance of the target, small and
synthetic but real.** `_fixture_parser` at `tests/test_skills_lint.py:379` is a
tiny `argparse.ArgumentParser` rather than a dictionary, and its docstring states
the property that matters: "It is a real `argparse.ArgumentParser` rather than a
table, so the fixtures exercise the same code path the real tree does." The
fixtures stay isolated, and they stop being able to encode a private theory of
the target.

**Using the real thing costs three things, and each is smaller than the drift.**
First, translating the artifact into the target's input: a documented command is
prose, so a prompt marker is stripped, everything from a shell operator onward is
dropped as belonging to another program, and quoting is resolved by `shlex`
rather than by `split()`. Second, deciding which of the target's verdicts count:
here exit 0 is `--help` and `--version`, which are real answers rather than
failures, at `tests/test_skills_lint.py:207`. Third, handling the target's state.
`real_parser` at `:116` builds a FRESH parser per call, and its docstring says
why: "`parse_args` mutates the namespace it builds and argparse keeps state on
the parser for a failed parse. A shared instance made one skill's bad command
affect the next skill's verdict, which is the shape of a test that passes or
fails depending on ordering."

**Say which configuration of the real thing you are checking against, and pin the
other question separately.** `real_parser` deliberately builds the FULL
membership rather than the machine's active profile, because "linting against
whichever profile happens to be configured on the machine running the suite would
make the result a property of that machine". Which verbs a profile hides is a
different question, and the same commit pinned it in its own test,
`test_a_profile_disabled_verb_is_absent_rather_than_refusing` at `:672`, by
building both presets and driving a verb one of them excludes.

**Check what the repository already drives before you build a second model of
it.** `tests/test_cli_contract.py` has driven every landed registry entry through
the real dispatcher since long before U28, and `_sample_arguments` at `:1349`
already carried the answer to four of the five defective command shapes.

**Keep the anti vacuity guard next to the checker, because a checker with nothing
to check is also green.** `lint_skills` over an empty directory returns an empty
problem list, which is correct and indistinguishable from twelve clean skills.
`test_the_real_tree_holds_exactly_the_skills_that_are_meant_to_ship` at `:765`
asserts the membership so the lint cannot be satisfied by deletion. A checker
that delegates its verdict to the real thing still owes you proof that it ran.

**This is the JUDGMENT axis, and it is not the same axis as deriving the set.**
The seam decisions live in the sibling DJ_tools repository rather than in this
one, at `docs/migration/00-SEAM-DECISIONS.md` there. Part 5 P3, "Audit by
walking, not by enumerating", already forbids hand listing the MEMBERS a test quantifies over,
and requires the set be derived at run time by walking the directory, iterating
the registry, or introspecting the module. Rule (g) obeyed P3 completely. It
walked every fence in every skill and missed no line. Then it judged each line
it found with a hand rolled model. A checker can derive its set perfectly and
still decide each member wrongly, so P3 being satisfied is not evidence that this
one is. P4 in the same part states the cost in a sentence worth keeping, "a
derivation that is 90 percent complete is worse than an honest list, because it
invites trust", and the token walker did three of argparse's four jobs. P2 is the
closest existing statement of this learning, one level down at the value rather
than at the checker: a check runs against the value the rest of the system
actually sees, because a check and a consumer that can disagree eventually will.

**The same shape had already fired on this seam the day before, and the surface
it fired on was a document rather than a suite (session history).** While
establishing which shipped verbs carried the queued job defect, a quick predicate
tested whether a verb's argv builder contained the root run flag, by substring
search over the builder's SOURCE TEXT. `sync_favorites_argv` emits that verb's own
intake run flag, whose name contains the root flag's name as a substring, so the
predicate cleared `sync.favorites`, which was a second live shipped defect. The
predicate fell for exactly the ambiguity that caused the underlying bug. Nothing
in the battery caught it. It was caught by a read only semantic grounding
validator checking the finished document's claims against source, after the
document was written, and the code, the doc, and `CONCEPTS.md` all had to be
amended. Reading tokens near a component is the same move as modelling its
grammar, and the false all clear it produces is the same false green.

**A derived set does not immunise you, because a derived guard can still smuggle
a model (session history).** The registry derived queued resume guard was built
correctly under P3, walking the registry for the combination of `long_running`,
an argv builder, and an explicit gate, so it covers verbs that do not exist yet.
It caught `delete.review` within minutes. But its assertion, that every matching
verb's resume argv carries a `job` option, turned out to be the author's own
assumption rather than the contract, and `delete.review`'s resume is legitimately
the same command. The set was derived. The judgment was still hand written, and
the hand written half is the half that was wrong.

**Text matching over a proxy for the real question fails the same way outside a
test, and it fails silently there too (session history).** Five background wait
loops of the form `until ! pgrep -f "mutate.py"` never terminated, because each
loop's own command line contains the string it greps for, so `pgrep` matched the
waiter. The condition could never go false. Same defect, no suite involved: a
question about a process asked of the text near it rather than of the thing that
owns the answer.

## Why This Matters

WHAT THE SILENCE COST, MEASURED. Eight commands across six skills shipped to a
person's machine, unaltered, through `crate skills install`. The review drove the
producer to establish reachability under the merge bar's third condition,
`docs/u28-skills-review.md:127` onward, installing all twelve skills into a
scratch directory and listing the files that landed. Three of the eight are
`crate audit coverage --limit 200`, which is the verification step a skill tells
a person to run AFTER a write. So the failure mode is a person following a
recommended check on a library they have just modified and getting an argument
error, at the moment they most need the answer.

The eight were not typos in a rarely read corner. `library-reports` spells the
same verb correctly in the same commit, `crate audit coverage /path/to/export.xml
--limit 2000`, so two shipped skills disagreed about the shape of one verb and
the lint passed both. That is `docs/METHOD.md:183` in a new medium, "one symbol
meaning two things in two modules", where here the two modules are two markdown
files and the symbol is a command line.

WHY THE GREEN SUITE COULD NOT SEE IT, AND THIS IS THE PART THAT GENERALISES. The
before file has four fixtures for the verb rule, and two of them assert that the
walker rejects something, `test_a_command_naming_no_real_verb_fails` at
`git show c24411c^1:tests/test_skills_lint.py:584` and
`test_a_command_naming_a_flag_the_verb_does_not_declare_fails` at `:593`. Both
were driven against the walker for this document, with the skill name elided from
the message, and both genuinely bite:

    'crate synchronise --ok'    -> ["fenced command names no real verb: ..."]
    'crate sync --no-such-flag' -> ["'crate sync' does not declare the flag ..."]

The rule was tested. Each bit of it worked. What no fixture asked, and what no
fixture built from `_FIXTURE_VERBS` COULD ask, is the one question that mattered.
Driven against the same walker, with the verb table walked from the real parser:

    'crate audit coverage --limit 200'                      -> []
    'crate report library'                                  -> []
    'crate audit duplicates'                                -> []
    'crate run show'                                        -> []
    'crate name apply --decision name.apply.confirm=apply'  -> []
    'crate profile set PRESET-NAME'                         -> []

Six silent passes, six commands that exit 2. The walker's verdict and argparse's
verdict were never once compared, and a suite cannot compare them by getting
bigger.

THE CORRECT MODEL ALREADY EXISTED IN THE SAME TEST TREE, WRITTEN DOWN, AND THE
SECOND MODEL DID NOT CONSULT IT. `tests/test_cli_contract.py:1534` through
`:1536` give exactly the three verbs an export path:

```python
        "audit.coverage": [str(library / "no-such-export.xml")],
        "audit.duplicates": [str(library / "no-such-export.xml")],
        "report.library": [str(library / "no-such-export.xml")],
```

`:1364` gives `run.show` a run identifier, and `_sample_arguments`'s own
docstring at `:1349` opens "Enough POSITIONAL arguments to drive one verb". The
fifth shape is in that file too. `test_conformance_1_structured_output_is_actually_emitted`
at `:1334` builds its argv as

```python
    argv = ["--output", "json", *_sample_decisions(entry), *entry.path, *_sample_arguments(entry)]
```

with decisions BEFORE `entry.path`, and the docstring explains it, "they are
flags on the ROOT parser: a gate answer belongs to the invocation, not to the
subcommand". The skill wrote `crate name apply --decision name.apply.confirm=apply`,
with the root flag after the verb path, which is precisely what that sentence
forbids. Four of the five defective shapes had a correct answer sitting in a
sibling test file, and the walker could not benefit from any of it, because a
private model is not a thing other code can teach.

WHY THIS IS A NEW MEMBER OF METHOD'S LIST. `docs/METHOD.md:175` opens "What a
green suite cannot see, so hunt it separately" and lists four shapes, of which
the first, at `:177`, is "a test whose expected value comes from the code under
test, reducing the assertion to X equals X while genuinely exercising the
code". A hand rolled
checker with fixtures written against its own model is that shape scaled up from
one assertion to a whole rule. The expected value does not come from a single
line of the code under test, it comes from the model the checker and its fixtures
share, and the assertion is the model equals itself. It exercises real code, it
reports real failures for real defects, and it is still measuring nothing about
the target.

THE PRODUCT CODE FAILS THE SAME WAY WHEN IT MODELS WHAT THE PARSER DELIVERS
(session history). In `src/cratekit/cli/reports.py`, the `as-of` handler tested falsiness
rather than an explicit `None`, so an explicitly typed empty string was read as
"flag not given" and the report aged every grouping against today and exited OK.
The function's own docstring argued against the behaviour the function had. Six
local reviewers and the whole suite missed it, and a cross model reviewer found
it. The code held a model of what "argument absent" means that did not match what
the parser actually delivered, which is this learning with the checker and the
product swapped.

AND A FIXTURE BUILT FROM THE SAME MENTAL MODEL AS THE CODE HIDES A REAL
BEHAVIOUR CHANGE (session history). Mutation row S3 narrowed an analysis watch
from the library root to the library's own `Music` subdirectory and killed
nothing. It was explicitly ruled not
inert, because the behaviour genuinely differs. The author's own analysis file
test wrote its file inside that same subdirectory, so the narrowed root still
covered it. The
fix was to move the file so it sits directly under the library root, after which
the row killed. A mutation table is the one instrument that compares two
implementations by running both, and even it goes quiet when the fixture was
authored from the model under test.

TWO CORRECTIONS TO THE IN TREE RECORD, since this corpus is where a later reader
will check. First, the review's summary row at `docs/u28-skills-review.md:29` and
`c24411c`'s own commit message both tally the eight as "6 omit a required
positional, 1 puts a root flag after the verb, 1 names a subcommand that does not
exist". The review's own evidence table at `:100` and the parser's messages
measured here both say otherwise: SEVEN omit a required positional, six of them
`EXPORT` and one `run_id` on `crate run show`, and one is the misplaced root flag.
No shipped command named a subcommand that does not exist. Second, finding 5 at
`:33` says "6 of the 8 commands in finding 1 pass the lint". Measured, all eight
passed, since the pre fix lint over the pre fix tree returned zero problems. The
direction of both corrections is the same, the walker was blinder than the record
credits it with, so neither weakens the finding.

A THIRD CORRECTION, TO A LABEL RATHER THAN A NUMBER. The two "3"s in this
project's vocabulary are different rules and this learning touches both, so do
not let one stand in for the other. `docs/METHOD.md:163` pattern 3 is "a fix that
lands on the performing path instead of the checking path". Seam decisions Part 5
P3 is "audit by walking, not by enumerating". This learning is neither, it is the
judgment axis described in Guidance, and it is closest to P4 and P2.

AND THE SAME SHAPE SURVIVED ONE LEVEL DOWN, IN THE CORRECTION ITSELF.
`test_a_command_missing_a_required_positional_fails` at
`tests/test_skills_lint.py:613` is named for the defect the walker could not see,
and its docstring says "argparse wants an argument the skill never mentions". Its
fixture parser declares its only positional as `value` with `nargs="*"`, which
argparse treats as optional, so the command it drives fails for a different
reason:

    crate sync --track-limit -> crate sync: error: argument --track-limit: expected one argument
    crate sync               -> OK

The test still bites where the walker did not, verified, since the walker returned
`[]` for `crate sync --track-limit` by skipping the flag's argument slot. But the
property it claims to hold is held elsewhere, by `test_real_skills_pass_lint` at
`:783` against the real parser and the real tree. The fixture was named from the
model of the fix rather than measured against the parser, which is a small
instance of the very thing the fix was about, and it is worth knowing that
deleting a reimplementation does not automatically delete the habit that produced
it.

## When to Apply

- **You are writing a rule that validates text against a program's interface.**
  Documentation examples, generated snippets, a config file checked against a
  schema, a fixture argv, a README command block. Parse it with the program's own
  parser, load it with the program's own loader, and let its failure be the
  verdict.
- **You are about to write "which flags take a value", "which subcommand names
  exist", "how quoting works", or "which arguments are required" into your
  checker.** Each of those is a piece of the target's grammar. One is a
  convenience, three is a second implementation.
- **A false positive in your checker is about to be fixed by adding a rule about
  the TARGET's semantics rather than about your input handling.** The `--output
  json` repair is the worked case. Fixing how you strip a prompt marker is input
  handling and is yours. Fixing what a flag does is the target's and is the
  signal.
- **Your fixtures are data structures shaped like your checker's internals.** A
  dictionary keyed by verb path, a list of known names, a table of expected
  fields. Build a small real instance of the target instead, and the fixture
  stops being able to hold a private theory.
- **The real thing exits rather than returning.** Trap `SystemExit`, capture both
  streams, and decide explicitly which exit codes are answers and which are
  failures. Exit 0 from `--help` is not a passing command in every checker's
  sense, and here it is.
- **The real thing carries state across calls.** Build a fresh instance per
  input, or accept a suite whose result depends on ordering.
- **The real thing has a configuration dimension.** Choose it deliberately, say
  why in the docstring, and check the other configurations as their own test
  rather than as a side effect.
- **Another file in the same test tree already drives the same interface for
  real.** Read its argument table before writing a second one. Two tables of what
  a verb needs is the same defect as two implementations of what a command is.
- **You are answering a question about a component by searching text near it.**
  A substring of a builder's source, a `pgrep` pattern, a grep for a flag name.
  Both are in the record and both returned a confident wrong answer (session
  history). Ask the component: call the builder and read the list it returns, ask
  the process table for a pid you hold.
- **You have satisfied P3 and feel covered.** Deriving the set is one axis and
  deciding each member is the other. Ask separately who owns each verdict, and
  note that a registry derived guard caught a verb the author never thought of
  and still asserted something about it that was untrue (session history).
- **A table in your tree stands beside the real thing rather than being read
  from it.** `tests/test_cli_contract.py` keeps a hand curated `UNREACHABLE_GATES`
  exemption map (session history). A curated exemption list is a legitimate
  shape, since somebody must record a decision, but it is the shape that drifts,
  so it wants an assertion that every key still names something real.
- **Your checker's coverage of its INPUT surface is a separate question from the
  correctness of its VERDICT.** Rule (g) had both problems and they were fixed in
  different commits. `4a074cc`, also reachable from `main`, widened the matcher to
  tilde fences and indented command lines, and its own docstring records
  "Measured before the fix: clean", so the widening added no new violations. A
  correct verdict over half the surface is still half a checker.
- **You are recording what your delegating checker still cannot see.**
  `docs/residual-findings.md` R-159 holds this one honestly: `_verb_problems`
  reads only lines whose first token is the entry point, so `sudo crate ...` or an
  invocation inside a loop body is not checked at all. Measured cost none today,
  verified by reading all twelve skills, and the reason it is not widened is that
  every widening is a guess about shell syntax and would fire on prose, which is
  the false positive shape that gets a guard suppressed.

## Examples

THE BEFORE, at `git show c24411c^1:tests/test_skills_lint.py`. The walker's body
at `:181` onward, which is subcommand resolution and option parsing written by
hand:

```python
    prefixes = {path[:n] for path in verbs for n in range(len(path) + 1)}
    known = dict(verbs.get((), {}))
    path: tuple[str, ...] = ()
    flags: list[str] = []
    rest = tokens[1:]
    index = 0
    while index < len(rest):
        token = rest[index]
        if token.startswith("-"):
            flag = token.split("=", 1)[0]
            flags.append(flag)
            # Skip the flag's ARGUMENT when it takes one and did not carry it
            # inline, or the value is read as a subcommand.
            takes_value = known.get(flag) or verbs.get(path, {}).get(flag)
            index += 2 if takes_value and "=" not in token else 1
            continue
        if path + (token,) in prefixes and path + (token,) != path:
            path += (token,)
            known.update(verbs.get(path, {}))
            index += 1
            continue
        break
```

and then the whole of its verdict, at `:203`:

```python
    # Everything after the verb path is a value, except the flags among it.
    for token in rest[index:]:
        if token.startswith("-"):
            flags.append(token.split("=", 1)[0])

    if path not in verbs or not path:
        spelled = " ".join(path) if path else " ".join(rest[:2])
        return [f"{skill}: fenced command names no real verb: 'crate {spelled}'"]

    allowed = set(verbs[path]) | set(verbs[()])
    return [
        f"{skill}: 'crate {' '.join(path)}' does not declare the flag {flag!r}"
        for flag in sorted(set(flags))
        if flag not in allowed
    ]
```

Read the comment on the first loop against the two loops together. Everything
after the verb path is scanned for tokens beginning with a dash and nothing else.
A required positional that is ABSENT is not a token, so there is no line in this
function that could ever have noticed one. The docstring above it, at `:169`,
argues carefully and correctly for the greedy path consumption, and never
mentions positionals either, because the model did not contain them.

THE AFTER, at `tests/test_skills_lint.py:189` through `:211`. The whole verdict is
the target's:

```python
    # Everything from a shell operator onwards belongs to another program.
    for operator in ("|", ">", "<", "&&", ";"):
        if operator in text:
            text = text.split(operator, 1)[0].strip()
    try:
        argv = shlex.split(text)[1:]
    except ValueError:
        return []
    if not argv:
        return []

    parser = parser_for()
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stderr(buffer), contextlib.redirect_stdout(buffer):
            parser.parse_args(argv)
    except SystemExit as exit_code:
        # 0 is --help and --version, which are real answers rather than failures.
        if exit_code.code in (0, None):
            return []
        complaint = buffer.getvalue().strip().splitlines()
        detail = complaint[-1] if complaint else "rejected by the parser"
        return [f"{skill}: fenced command does not parse: {text!r}: {detail}"]
```

Everything before `parse_args` is translation, turning a documented line into an
argv. Everything after it is reporting. The judgement in between belongs to the
code that will actually reject the command when a person types it, and the
message a person would see is carried through into the failure rather than
paraphrased.

THE SAME EIGHT COMMANDS, THROUGH THE NEW RULE, over the pre fix tree:

    adopt-a-library: fenced command does not parse: 'crate report library':
      crate report library: error: the following arguments are required: EXPORT
    intake-and-name: fenced command does not parse:
      'crate name apply --decision name.apply.confirm=apply':
      crate: error: unrecognized arguments: --decision name.apply.confirm=apply
    review-queue: fenced command does not parse: 'crate run show':
      crate run show: error: the following arguments are required: run_id

THE CORRECTIONS, which are what a reader of the skills now sees, from
`git show c24411c -- 'src/cratekit/skills/assets/*/SKILL.md'`:

    -crate audit coverage --limit 200
    +crate audit coverage --limit 200 /path/to/collection.xml
    -crate report library
    +crate report library /path/to/collection.xml
    -crate audit duplicates
    +crate audit duplicates /path/to/collection.xml
    -crate run show
    +crate run show RUN-IDENTIFIER
    -crate name apply --decision name.apply.confirm=apply
    +crate --decision name.apply.confirm=apply name apply

All five corrected forms were driven against the real parser for this document
and all five parse.

THE NINTH DEFECT, caught by the new rule inside the fix round itself. The
placeholder `crate profile set PRESET-NAME` reads like the others in the corrected
set, and it is not the same kind of thing, because `profile set` takes a
constrained choice rather than a free value:

    crate profile set: error: argument name: invalid choice: 'PRESET-NAME'
    (choose from 'slim', 'full', 'custom')

A walker checking verb paths and flags would have passed it, and did pass it when
driven for this document. The shipped text is now `crate profile set full`,
`src/cratekit/skills/assets/first-run/SKILL.md`.

THE FIXTURE CHANGE, which is the half that makes the fix durable. Before, at
`git show c24411c^1:tests/test_skills_lint.py:394`:

```python
def _lint(root: Path, scripts: set[str], **kwargs):
    """Lint a synthetic tree with the synthetic verb table and taxonomy."""
    kwargs.setdefault("verbs", _FIXTURE_VERBS)
```

After, at `tests/test_skills_lint.py:402`, with `_fixture_parser` at `:379`:

```python
def _lint(root: Path, scripts: set[str], **kwargs):
    """Lint a synthetic tree with the synthetic verb table and taxonomy."""
    kwargs.setdefault("parser_for", _fixture_parser)
```

One keyword, and the fixtures stop being able to describe a command shape the
real parser would not recognise.

THE SIBLING APPLICATION, in the same commit, from a different finding. Two skills
described a profile disabled verb as refusing with an explanation when it is in
fact absent from the parser. The correction was not only to the prose. The
behaviour was pinned against the parser, `tests/test_skills_lint.py:672`, and the
docstring names the property:

```python
    PINNED AGAINST THE PARSER RATHER THAN THE PROSE, so this stays true when
    somebody rewrites the sentence. What it forbids is the product quietly
    changing to a refusal model while twelve skills go on describing whichever
    one they were written against.
```

with an anti vacuity assertion before the drive, so the pin cannot pass by the
presets happening to agree:

```python
    hidden = names(full) - names(slim)
    assert hidden, "no verb differs between the presets, so this pins nothing"
```

Same principle at a different altitude. A claim about the product, checked by
running the product rather than by a person agreeing with the sentence.

THE ROUND'S SHAPE, for scale. The independent pass is `docs/u28-skills-review.md`
with its 45 row mutation table at `docs/mutation/u28-skills-independent.md`, both
landed as `a695fc0`, and it returned BLOCKING on three findings of which this was
one. `c24411c`'s battery was ruff clean, `scan_repo` clean, and 6228 passed with 1
skipped against 6224 and 1 before the round. The unit merged as `f55b3ea` and
filed R-158 through R-164, of which R-159 is the honest remaining limit of this
rule.

## Related

- [An explicit gate makes a queued job undriveable without the run id](an-explicit-gate-makes-a-queued-job-undriveable-without-the-run-id.md).
  The same class, measured on the queued resume rather than on a skill fence. Its
  exposure predicate matched a flag name as a substring of the builder's SOURCE
  and declared a broken verb clean; matching the whole token in the real returned
  argv and driving it through the real dispatcher is what corrected it. That doc
  states the remedy locally three times, at its lines 147, 289 to 300, and 340 to
  356. This one names the class.
- [A merge falsifies a guard invariant and every remedy breaks something](merge-falsifies-a-guard-invariant-and-every-remedy-breaks-something.md).
  Two instances of this class live in it. Its line 82 states the shape in one
  sentence, "a guard standing in for a concept can be coarser than the concept in
  either direction", and its central guard, `_os_open_reads`, is a hand rolled
  model of `os.open` flag semantics that answers "I cannot tell what this opens"
  for any argument it cannot resolve statically. Read its rule against editing the
  checking path with this carve out in mind: a checker that reimplements its
  subject is a third state, and replacing it with the real thing is not the
  forbidden widening.
- [A planned verb cannot share a landed leaf's first path word](a-planned-verb-cannot-share-a-leafs-first-path-word.md).
  The other argparse trap in this corpus, and the same asymmetry one level up: a
  verb path that argparse would refuse can sit in the registry for months because
  `build_parser` never sees a planned verb.
- [Adding the first caller makes you the owner of its unreviewed defects](adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md).
  The other reason a green suite proves nothing: there, a path nobody called is a
  path nobody shaped a test for. Here, a checker's fixtures are shaped by the
  checker's own model, so they never ask the question the model gets wrong. Same
  green, two different causes.
- [A zero death row can be a test gap or an inert mutation](a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md).
  The small version of the same drift: one verb name spelled in two modules with
  nothing comparing them, closed by a three line guard asserting the two copies
  are equal. A reimplemented checker is that failure at the scale of a whole
  parser.
- [A cause read from a log is not a cause driven by reproducing it](a-cause-read-from-a-log-is-not-a-cause-driven-by-reproducing-it.md).
  The corpus's general form of "drive it rather than read it", applied there to a
  finding and here to the checking path itself.
- [The brief Files line is not the landing path](the-brief-files-line-is-not-the-landing-path.md).
  Another surface the real parser never saw: four verbs stayed declared and not
  landed while the battery was green, because `build_parser` never imported them
  and conformance never drove them.
- [A count that moved by the right amount is not a measurement of what moved](a-count-that-moved-by-the-right-amount-is-not-a-measurement-of-what-moved.md).
  The same instinct in a measurement rather than a checker: when a walk derives
  the set, run that same walk on both trees and difference them rather than
  trusting the total.
- Part 5 of `docs/migration/00-SEAM-DECISIONS.md` in the sibling DJ_tools
  repository, which is not a path inside this repo and is authoritative over any
  brief here. P3 is the adjacent axis, derive the SET rather than listing it; this
  learning is the other axis, derive the JUDGMENT rather than modelling it, and
  rule (g) did the first correctly while failing the second. P4 states the cost in
  one line, "a derivation that is 90 percent complete is worse than an honest
  list, because it invites trust". P2 is the closest existing statement of this
  rule, one level down: a check runs against the value the rest of the system
  actually sees, because a check and a consumer that can disagree eventually will.
- `docs/METHOD.md:175`, "What a green suite cannot see, so hunt it separately".
  This learning is a fifth item of exactly that list's shape and is not yet in it.
- Issue [#28](https://github.com/philgutowski/cratekit/issues/28), U28 Claude
  skills packaging, closed by merge `f55b3ea`. Its brief is where the skill lint
  rules were specified.
