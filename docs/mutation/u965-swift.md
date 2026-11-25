# U965, the Swift guards, measured on the App workflow

No container compiles Swift, so `scripts/mutate.py` cannot measure the guards
in `app/Sources/CrateEngine/`. Each was reverted alone in its own pushed
commit on `cloud/1084-menu-bar-swift-package`, read on the App workflow's push
run on that commit (macos-15, Swift 6.1.2), and every guard was restored byte
for byte in the commit after the last, `git diff` against the base empty. A
row is killed when the run failed at its Test step; every kill below failed
there, after a clean Build, and the tests named are the ones the log reports
as failed. Applied by an exact replacement that matched once in the base text,
by a script kept out of the repository; the base for rows S1 to S14 is
`9fd3930e`, restored at `9f4160e4` (green, 29 tests).

| Row | The guard reverted | Commit | Run | Result | Killed by |
|---|---|---|---|---|---|
| S1_relative_path_searched | `CrateSetup.check` drops the refusal of a relative path | `819b9344` | 45580661152 | killed | `testARelativePathIsRefusedRatherThanSearched` |
| S2_executable_unchecked | `CrateSetup.check` drops the executable check | `97f2d340` | 45580665664 | killed | `testANonExecutablePathIsTheSetupState` |
| S3_no_output_json | the arguments lose `--output json` | `03dd998f` | 45580670691 | killed | `testTheArgumentsAreFixedAndNeverReadByAShell` |
| S4_whole_environment | crate gets the app's whole environment | `a465c616` | 45580673320 | killed | `testTheEnvironmentIsMinimal` |
| S5_no_kill_escalation | no SIGKILL after the grace | `8530be5d` | 45580677849 | killed | `testAVerbThatIgnoresTerminateIsKilled` |
| S6_no_terminate | no SIGTERM at the timeout, only the kill after the grace | `98b00b10` | 45580681766 | survived, then killed at `f46b2738` | `testATimedOutVerbIsAskedToStopBeforeItIsKilled`, added after |
| S7_first_bytes_dropped | undecodable output reported with no first bytes | `59836a67` | 45580685524 | killed | `testTheFirstBytesAreCappedAtTheLimit`, `testUndecodableOutputIsReportedWithItsFirstBytes` |
| S8_empty_not_named | empty output not named, left to the decoder's error | `a96f749b` | 45580688725 | killed | `testEmptyOutputIsReportedNeverAnEmptyResult`, `testTheAsyncRunGivesTheSameResult` |
| S9_version_unchecked | an envelope of another version decoded | `4dc71dce` | 45580693272 | killed | `testAnotherEnvelopeVersionIsRefusedByName`, `testAnotherEnvelopeVersionIsReportedByItsNumber` |
| S10_cause_key_optional | a missing `cause` key read as none | `295102ab` | 45580697680 | killed | `testAMissingRequiredKeyIsMalformedNotDefaulted` |
| S11_numbers_before_bools | `JSONValue` tries a number before a bool | `ce96a64c` | 45580701883 | survived | none |
| S12_blocked_read_as_failed | outcome `blocked` read as `failed` | `65b72882` | 45580705008 | killed | `testAGateRefusalDecodesWithWhatItShowed`, `testEveryKnownOutcomeReadsAsItself` |
| S13_stdin_inherited | crate inherits the app's standard input | `330e8716` | 45580708629 | survived | none |
| S14_signal_read_as_status | a signal death read as an exit status | `c0f77e85` | 45580714043 | killed | `testASignalDeathIsNotReadAsAnExitCode` |

**11 of 14 killed on the first pass, 12 of 14 after the test S6 asked for.** The three that survived:

- **S6, a user facing guard, closed.** The kill after the three second grace
  ended the verb inside the old timeout test's ten second bound, so nothing
  saw that crate was never asked to stop, which a job driver needs to stop at
  an item boundary. `testATimedOutVerbIsAskedToStopBeforeItIsKilled` was
  added at `aabd1868`, and S6 reverted again at `f46b2738` (run 45582154263) was killed by that test, and restored at `1dc24fee` (run 45582157318, green, 30 tests).
- **S11, an equivalent mutant here.** Foundation's `JSONDecoder` on the
  runner refuses to decode a `Double` from `true` and a `Bool` from `1`, so
  the order of the two attempts changes nothing;
  `testTrueAndFalseNeverReadAsNumbers` passed under it. The order is kept for
  a decoder that would coerce.
- **S13, unobservable on the runner.** `swift test` already runs with a
  standard input that holds nothing, so a crate that inherits it reads the
  same as one given the null device. Maintainer facing: the app started from
  Finder has no terminal either; residual
  `u965-the-app-passes-its-terminal-to-crate.md` covers the terminal case.

**Two guards of the fix round have no row**, found by review round two and
not measured: the `isRunning` check before the SIGKILL, and the bound on the
wait after it. Neither can be reached by a fake: a SIGKILL always ends and
reaps a shell script, so reverting either changes no test's result.
Maintainer facing; the unkillable case is part of residual
`u965-a-timed-out-verb-leaves-its-children-running.md`.

The Python fixture guard's own table is `docs/mutation/u965.md`.
