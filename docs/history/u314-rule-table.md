# Rules before the card #871 cut

Every rule in the three documents at `origin/main`, read whole on 2026-11-22: `CLAUDE.md` (173 lines), `docs/METHOD.md` (739 lines), `.claude/skills/cloud-unit/SKILL.md` (546 lines). Line numbers are those at origin/main. Ids are in reading order, C for CLAUDE.md, M for METHOD, S for the skill.

Convention: command flags are written without their leading double hyphen (for example "`board.py residuals` with the `land` flag") so that this file carries no double hyphens. Rows sharing a concept are cross referenced in `also in` in both directions; a row naming a rule as superseded keeps the old date so nothing is lost.

## Counts

| document | rows |
|-|-|
| CLAUDE.md | 101 |
| docs/METHOD.md | 351 |
| cloud-unit SKILL.md | 233 |
| total | 685 |
| rows with something in `also in` | 485 |
| of those, rows duplicated in another document | 425 |

## Rule table

| id | source | rule | also in | now reads |
|-|-|-|-|-|
| C001 | CLAUDE.md, Cratekit (intro), L6-7 | CLAUDE.md is kept short because every session and every agent loads it on every call (U196). |  | |
| C002 | CLAUDE.md, Cratekit (intro), L7-10 | `docs/METHOD.md` is the operating instruction and is what to read next; it holds the pipeline, card sizes, merge bar, mutation method, driver rules, merge constraints and do-not-touch list. | M002, S006 | |
| C003 | CLAUDE.md, Cratekit (intro), L10-11 | `docs/METHOD-local.md` is the part only a session on Phillip's Mac needs: local board commands, attended cards and releases. | M003, M341 | |
| C004 | CLAUDE.md, Cratekit (intro), L12 | `RESTART-cratekit.md` is the verified current state, read by a local session. | M004 | |
| C005 | CLAUDE.md, Cratekit (intro), L12-13 | Each unit's own record is a file in `docs/restart/`. | M033, M214, M215, S189 | |
| C006 | CLAUDE.md, Cratekit (intro), L13-15 | `docs/history/` is the narrative of how the rules were arrived at, read for reasoning, never for instruction. | M009, M010 | |
| C007 | CLAUDE.md, Cratekit (intro), L17-19 | `docs/solutions/` (YAML frontmatter `module`, `problem_type`, `tags`) is searched, not read: grep it by module before touching an area. | M018, S131 | |
| C008 | CLAUDE.md, Cratekit (intro), L19-20 | Grep `CONCEPTS.md` for an unclear term; never read it whole. | M017 | |
| C009 | CLAUDE.md, How a session runs, L24 | The cloud is where Cratekit is built, decided by Phillip on 2026-10-27. | M231, M232, S002 | |
| C010 | CLAUDE.md, How a session runs, L25-26 | Of Phillip's two Claude projects, one turns his ideas and bugs into cards with the `file-card` skill and keeps the decisions page. | C092, M234, M300 | |
| C011 | CLAUDE.md, How a session runs, L26-28 | The coordinator of the other (building) project keeps build threads going, each running the `cloud-unit` skill on its card. | M233, S064 | |
| C012 | CLAUDE.md, How a session runs, L28-30 | A unit's stages are: plan, build, Fable's review to the merge bar, the mutation table, the record, and a pull request merged to `main` with the closing trailer once CI is green. | M236, S003 | |
| C013 | CLAUDE.md, How a session runs, L30 | A session does the whole of a unit itself. | M011, S003 | |
| C014 | CLAUDE.md, How a session runs, L30-31 | The compound engineering plugin is not used. | M005, M006 | |
| C015 | CLAUDE.md, How a session runs, L31-33 | Only a card that cannot be built without the machine is built locally; the cloud sets it aside with a comment carrying the steps, and `docs/METHOD-local.md` is how. | M239, M240, S004, S054, S109, S111 | |
| C016 | CLAUDE.md, How a session runs, L35-37 | Every question for Phillip reaches the decisions page, https://claude.ai/artifact/FUqChoK5qKhztLdzzEADaS, where he answers with a tap. | M253, M264, S070 | |
| C017 | CLAUDE.md, How a session runs, L37 | A build thread asks on its card only. | M254, M304, S071 | |
| C018 | CLAUDE.md, How a session runs, L37-38 | The other (filing) project copies the question to the page and his answer back to the card. | M257, M307, S076 | |
| C019 | CLAUDE.md, How a session runs, L38-39 | Nobody watches a running session, so a question is a stop: make the conservative call, record it as a residual, and keep going. | M012, M013, M259, M306, S008, S075 | |
| C020 | CLAUDE.md, The board is the queue, L43-44 | Work is picked from the board, https://github.com/users/philgutowski/projects/2, never from a plan document or a conversation. |  | |
| C021 | CLAUDE.md, The board is the queue, L44-45 | Every implementation unit `U-N` and every attended chore `A-N` is an issue. |  | |
| C022 | CLAUDE.md, The board is the queue, L45-47 | The issue is the brief: goal, requirements, dependencies, key files, approach, test scenarios, verification. | M015 | |
| C023 | CLAUDE.md, The board is the queue, L47-48 | If the brief is insufficient, fix the issue rather than working around it. | M023, S134 | |
| C024 | CLAUDE.md, The board is the queue, L48-49 | An issue number does not always match its unit number (U38 is issue #51), so look it up before writing a trailer. |  | |
| C025 | CLAUDE.md, The board is the queue, L51-52 | U29, #29, is attended and never a session's to take, whatever a queue says. | M347, M350 | |
| C026 | CLAUDE.md, The board is the queue, L54 | `docs/residual-findings.md` is the LEDGER. |  | |
| C027 | CLAUDE.md, The board is the queue, L54-56 | A residual `R-N` is a real problem recorded rather than fixed; a unit files it unnumbered in `docs/residuals/`. | M030, S190 | |
| C028 | CLAUDE.md, The board is the queue, L56 | A residual takes its number when it lands on `main`. | M205 | |
| C029 | CLAUDE.md, The board is the queue, L56-57 | A residual earns an issue only when it meets METHOD's board bar. | M068, M069 | |
| C030 | CLAUDE.md, The board is the queue, L57 | Do not backfill the rest (residuals that do not meet the bar get no issue). |  | |
| C031 | CLAUDE.md, The board is the queue, L57-58 | The ledger is over forty thousand lines: search it with `board.py residuals` and its `search WORDS` flag. | M132 | |
| C032 | CLAUDE.md, The board is the queue, L60 | The merge commit ends with the closing trailer, `Closes #N`. | S040, S218 | |
| C033 | CLAUDE.md, The board is the queue, L60-62 | Pushing `main` closes the issue, and the board workflow then flips every unit waiting on it from blocked to ready. | S228 | |
| C034 | CLAUDE.md, The board is the queue, L62 | Never hand-edit `ready` and `blocked` labels. | M243, S037 | |
| C035 | CLAUDE.md, The board is the queue, L62-63 | Never drag cards. | S037 | |
| C036 | CLAUDE.md, The board is the queue, L63-64 | To change readiness, change the dependency line in an issue body and let the sync recompute the labels. |  | |
| C037 | CLAUDE.md, The board is the queue, L64-65 | Run `board.py closing` with `since origin/main` before writing a trailer; it refuses a trailer that closes a unit a register still owes a module. | M198, S196, S199, S200 | |
| C038 | CLAUDE.md, The board is the queue, L67-68 | `DJ_tools/docs/migration/00-SEAM-DECISIONS.md` remains authoritative over any brief. |  | |
| C039 | CLAUDE.md, The board is the queue, L68-69 | Its Part 5, seven failure shapes, applies to every unit. |  | |
| C040 | CLAUDE.md, The battery, L73 | Nothing merges until all three battery commands are clean. | M164 | |
| C041 | CLAUDE.md, The battery, L75-77 | The three commands: `.venv/bin/ruff check src tests scripts`, `.venv/bin/python -m pytest`, `.venv/bin/python scripts/scan_repo.py`. | M165, S184 | |
| C042 | CLAUDE.md, The battery, L79-80 | On a Linux cloud container the suite is read against the base's own failures with `scripts/cloud_battery.py`. | M275, S018, S181 | |
| C043 | CLAUDE.md, The battery, L80-81 | The suite is the merge gate, not the edit loop: while building, run the test files for what you touched. | M170, M171, S139 | |
| C044 | CLAUDE.md, The battery, L81-84 | An author's own battery is not a review; after a green suite, hunt what a green suite cannot see, as METHOD lists. | M028, S153 | |
| C045 | CLAUDE.md, Standing constraints, L88-90 | Never write a beat grid: no tempo element, no BPM tag, no average-BPM field, no ANLZ grid, in any container. Absolute. | S033 | |
| C046 | CLAUDE.md, Standing constraints, L89-90 | Two suites enforce the beat grid ban across five surfaces. |  | |
| C047 | CLAUDE.md, Standing constraints, L91-93 | The live rekordbox database is protected, not untouchable: the default is hands off, and a unit needing a real database makes a disposable copy in a temporary directory. | M349, S034 | |
| C048 | CLAUDE.md, Standing constraints, L93-96 | Exception: the backup feature may read and copy the live database, but only with both `rekordbox` and `rekordboxAgent` confirmed gone, only into a new dated destination, and never in place. |  | |
| C049 | CLAUDE.md, Standing constraints, L96-97 | Writing to the live database outside a gated destructive session stays forbidden. |  | |
| C050 | CLAUDE.md, Standing constraints, L98-99 | rekordbox is opened by an attended session and by nothing else, decided 2026-09-29. |  | |
| C051 | CLAUDE.md, Standing constraints, L99-101 | A session Phillip is present for may open, drive and quit rekordbox on the live library through the desktop control tool, to import, to let it analyse, and to read what it shows. |  | |
| C052 | CLAUDE.md, Standing constraints, L101-105 | Where an attended card asks what rekordbox itself writes, the session may make, on a throwaway track and a playlist made by hand for the check, the change that card names (removing it from the collection, setting cues, playing it on a deck, deleting that playlist) (U321). | C054 | |
| C053 | CLAUDE.md, Standing constraints, L105-106 | It may change an analysis setting a probe names and put it back to Phillip's standard, read back by a screenshot (U321). |  | |
| C054 | CLAUDE.md, Standing constraints, L106-107 | Never on a real track, and never a change the card does not name (U321). | C052 | |
| C055 | CLAUDE.md, Standing constraints, L107-108 | A cloud session, a job, a verb and a test never launch rekordbox or its background agent. |  | |
| C056 | CLAUDE.md, Standing constraints, L108-110 | Before opening rekordbox: no Cratekit job is running, and `crate doctor` reads both backup ages under five days. |  | |
| C057 | CLAUDE.md, Standing constraints, L110-111 | After quitting rekordbox: `rekordbox` and `rekordboxAgent` are both confirmed gone before any verb runs. |  | |
| C058 | CLAUDE.md, Standing constraints, L111-112 | The analysis visit after a landing follows the project's `rekordbox-visit` skill step by step (U173). |  | |
| C059 | CLAUDE.md, Standing constraints, L112-114 | A whole sync pass, from the account's new music to filed and analysed, follows the project's `crate-sync` skill (U174). |  | |
| C060 | CLAUDE.md, Standing constraints, L114-116 | A whole attended sitting, every open attended card driven with worker sessions, follows the project's `attended-orchestrator` skill (U316). |  | |
| C061 | CLAUDE.md, Standing constraints, L117-118 | A backup is needed only when the library is more than five days out of date, or when Phillip asks for one, decided by Phillip on 2026-10-10. | C062 | |
| C062 | CLAUDE.md, Standing constraints, L118-119 | That decision relaxes (supersedes) the one day backup rule of 2026-09-29. | C061 | |
| C063 | CLAUDE.md, Standing constraints, L119-121 | Below five days a session opens rekordbox and mints the acknowledgment without running `crate backup run` first. |  | |
| C064 | CLAUDE.md, Standing constraints, L121-122 | At or over five days, or with either age unknown, the session runs the backup before anything else. |  | |
| C065 | CLAUDE.md, Standing constraints, L123-124 | A database write gate is approved by the session only when a rehearsal matches, decided 2026-09-29. |  | |
| C066 | CLAUDE.md, Standing constraints, L124-126 | The session drives the same verb on a disposable copy with library state redirected, reads the result, then brings the live plan to its gate. |  | |
| C067 | CLAUDE.md, Standing constraints, L126-127 | If the live digest equals the rehearsed one, the session approves and reports. |  | |
| C068 | CLAUDE.md, Standing constraints, L127-130 | If the digest differs, the session still approves, decided by Phillip on 2026-10-09 ("don't ask for my approval on anything going forward"), after reading the difference and recording it in the sitting record. |  | |
| C069 | CLAUDE.md, Standing constraints, L130-131 | A rehearsal that fails, or a difference in what is written rather than in a path, is the one case that still stops. |  | |
| C070 | CLAUDE.md, Standing constraints, L131-132 | The actor on every gate is `session`. |  | |
| C071 | CLAUDE.md, Standing constraints, L132-134 | The backup acknowledgment may be minted by the session, decided by Phillip on 2026-10-09, reversing the 2026-09-29 rule. |  | |
| C072 | CLAUDE.md, Standing constraints, L134-136 | The session reads both backup ages, refuses unless both are under five days, and answers with the actor `session`. |  | |
| C073 | CLAUDE.md, Standing constraints, L136-139 | Since U138 the verb accepts that answer with no controlling terminal and itself refuses unless both ages are under five days; until the installed copy carries U138, run it under `script -q /dev/null`. |  | |
| C074 | CLAUDE.md, Standing constraints, L139-140 | Answer as `session` either way: any other actor takes the terminal rule, which checks no age. |  | |
| C075 | CLAUDE.md, Standing constraints, L140-142 | Since U184 it is one command, `crate session ack` with the `as session` flag, with no gate and no run left waiting; until the installed copy carries U184, use the gate. |  | |
| C076 | CLAUDE.md, Standing constraints, L143-144 | DJ_tools is read-only for code; it is the live system until each workflow's replacement is proven. |  | |
| C077 | CLAUDE.md, Standing constraints, L144 | DJ_tools `docs/` are the exception to read-only. |  | |
| C078 | CLAUDE.md, Standing constraints, L145-146 | Do not symlink `.venv` into a worktree (the editable install names the checkout it was installed from). | M176 | |
| C079 | CLAUDE.md, Standing constraints, L147-148 | A pull request per unit, merged by the session that opened it once CI is green, decided by U158, replacing the old no pull requests rule. | M037, M185, S194 | |
| C080 | CLAUDE.md, Standing constraints, L148-149 | Feature branch per unit; open a pull request against `main`. | M186, S120 | |
| C081 | CLAUDE.md, Standing constraints, L149-151 | Merge it through the API as `merge(uN): ...` ending with the closing trailer once every check on its head is green. | M188, S216, S217 | |
| C082 | CLAUDE.md, Standing constraints, L151 | The merge takes the branch. | C088, M194, M293, M311, S013 | |
| C083 | CLAUDE.md, Standing constraints, L151-152 | Never a pull request that waits on a person. | M189, M238, S035, S194 | |
| C084 | CLAUDE.md, Standing constraints, L152 | Never a closing keyword in a pull request's body. | M191, S036, S205 | |
| C085 | CLAUDE.md, Standing constraints, L152-153 | CI reads the card a merge will close off a `cloud/N-slug` head only. | M192, S212 | |
| C086 | CLAUDE.md, Standing constraints, L153-154 | A local unit's pull request is judged on its range, and its close on the push to `main`. |  | |
| C087 | CLAUDE.md, Standing constraints, L154-156 | A cloud session merges itself, attended or not, authorized by Phillip on 2026-10-27 ("I authorize you to merge to main here in the cloud now and going forward"). | M237 | |
| C088 | CLAUDE.md, Standing constraints, L157-158 | A cloud session cannot delete a remote branch, so "Automatically delete head branches" stays on and a merged pull request takes its branch with it. | C082, M194, M293, M311, S013 | |
| C089 | CLAUDE.md, Standing constraints, L159 | Any other stale `cloud/` branch is listed for Phillip's next local session. | M310, M312, S014 | |
| C090 | CLAUDE.md, Standing constraints, L160 | Other builders share the board, decided by Phillip on 2026-11-04. | M297 | |
| C091 | CLAUDE.md, Standing constraints, L160-161 | Never take a card or touch a branch held on `grok/`. | M298, M299, S098, S099 | |
| C092 | CLAUDE.md, Standing constraints, L161-162 | One Claude project builds and the other files cards and keeps the decisions page. | C010, M234, M300 | |
| C093 | CLAUDE.md, Standing constraints, L164-165 | No em dashes, en dashes, or double hyphens in any prose, code comment, commit message, or issue body. | M196, S043 | |
| C094 | CLAUDE.md, Standing constraints, L165-166 | Do not swap a dash for a colon; favor commas, and keep colons for a genuine list or definition. | M197 | |
| C095 | CLAUDE.md, Standing constraints, L167 | Every doc is kept up to date, decided by Phillip on 2026-11-07. | M329, M331 | |
| C096 | CLAUDE.md, Standing constraints, L167-169 | A change lands with every doc it makes untrue corrected in the same pull request, a user's doc and a session's alike. | M332, S187 | |
| C097 | CLAUDE.md, Standing constraints, L169 | The change's record names each doc corrected. | M338, S188 | |
| C098 | CLAUDE.md, Standing constraints, L171 | Explanations are batched per phase. | M226, M227 | |
| C099 | CLAUDE.md, Standing constraints, L171-172 | A unit lands with its commit messages and its record. | M228 | |
| C100 | CLAUDE.md, Standing constraints, L172-173 | Phillip runs the explainer over a merged phase when he wants it. | M229 | |
| C101 | CLAUDE.md, Standing constraints, L173 | A session does not run the explainer. | M034, M230 | |
| M001 | docs/METHOD.md, Method (intro), L3 | METHOD.md is deliberately fixed in size. |  | |
| M002 | docs/METHOD.md, Method (intro), L3-4 | METHOD.md is the only document a session reads to learn how to work here; CLAUDE.md is the session contract and points at it. | C002, S006 | |
| M003 | docs/METHOD.md, Method (intro), L5-7 | `docs/METHOD-local.md` holds the part only a session on Phillip's Mac needs (local board commands, attended cards, releases), moved there by U196 so a cloud session does not carry it. | C003, M341 | |
| M004 | docs/METHOD.md, Method (intro), L8 | `RESTART-cratekit.md` is verified state and nothing else. | C004 | |
| M005 | docs/METHOD.md, Method (intro), L10 | The compound engineering plugin is out of the loop, decided 2026-09-07. | C014, M006 | |
| M006 | docs/METHOD.md, Method (intro), L10-11 | No `ce-plan`, no `ce-work`, no `ce-code-review`, no `ce-compound`. | C014, M005 | |
| M007 | docs/METHOD.md, Method (intro), L14-15 | The rules the plugin enforced that were paid for are kept as rules; its ceremony is not. |  | |
| M008 | docs/METHOD.md, Method (intro), L15-16 | Native Relay ran the pipeline until 2026-10-27 and is retired; the cloud lane replaced it. |  | |
| M009 | docs/METHOD.md, Method (intro), L18-19 | `docs/history/` is HISTORY: wave state files, independent reviews, the long narrative handoff. | C006, M010 | |
| M010 | docs/METHOD.md, Method (intro), L19-20 | Read a history file for the reasoning behind a rule; never read one to find out how to work. | C006, M009 | |
| M011 | docs/METHOD.md, The pipeline, one unit per session, L24 | A session takes one unit from the board and runs it to a pushed merge. | C013, S003 | |
| M012 | docs/METHOD.md, The pipeline, one unit per session, L24-26 | Nobody is watching, so a question is a stop, and a stop with nothing recorded is the one ending the next session cannot diagnose. | C019, M013, M259, M306, S008, S075 | |
| M013 | docs/METHOD.md, The pipeline, one unit per session, L26-28 | When a decision is genuinely the person's, record it as a residual with the options and pick the conservative one. | C019, M012, M259, M306, S008, S075 | |
| M014 | docs/METHOD.md, The pipeline, one unit per session, L30-31 | Orient: `board.py next`, `board.py show N`, `board.py start N` locally; `board.py cloud` in the cloud. | S015, S095 | |
| M015 | docs/METHOD.md, The pipeline, one unit per session, L31 | The issue is the brief. | C022 | |
| M016 | docs/METHOD.md, The pipeline, one unit per session, L31-32 | Read METHOD, and locally `RESTART-cratekit.md`. | S005 | |
| M017 | docs/METHOD.md, The pipeline, one unit per session, L32-33 | Grep `CONCEPTS.md` for any unclear term rather than reading it whole. | C008 | |
| M018 | docs/METHOD.md, The pipeline, one unit per session, L33-34 | Grep `docs/solutions/` by module and tag for the area you are about to touch, and read the entries that match. | C007, S131 | |
| M019 | docs/METHOD.md, The pipeline, one unit per session, L35 | Plan in plan mode, as a message (the cloud overrides plan mode, see also). | M021, S130 | |
| M020 | docs/METHOD.md, The pipeline, one unit per session, L35-37 | The plan names the seam, the files, the test scenarios from the brief, the residuals the unit closes, and what is out of scope. | S132 | |
| M021 | docs/METHOD.md, The pipeline, one unit per session, L37 | The plan is not a document. | M019, S130 | |
| M022 | docs/METHOD.md, The pipeline, one unit per session, L37-38 | `docs/plans/` is closed: nothing new is written there; existing files are the record of units already built. |  | |
| M023 | docs/METHOD.md, The pipeline, one unit per session, L39-40 | If the brief is insufficient, fix the issue body, then plan against the fixed brief. | C023, S134 | |
| M024 | docs/METHOD.md, The pipeline, one unit per session, L41-42 | Build: guard first, then the code it governs, so a violation cannot be introduced silently. | S137 | |
| M025 | docs/METHOD.md, The pipeline, one unit per session, L42-43 | Commit in units of meaning with subjects that name the unit, `feat(u57): ...`. | S138 | |
| M026 | docs/METHOD.md, The pipeline, one unit per session, L44-46 | Review: run the built in `/code-review` on the branch, drive every finding rather than arguing with it, apply what holds, commit the fixes. | S144 | |
| M027 | docs/METHOD.md, The pipeline, one unit per session, L46 | Then the mutation table, capped at 25 rows. | M096 | |
| M028 | docs/METHOD.md, The pipeline, one unit per session, L46-47 | Then the hunts a green suite cannot see. | C044, S153 | |
| M029 | docs/METHOD.md, The pipeline, one unit per session, L47-48 | At most two fix rounds; when spent, what is still open becomes a residual and the unit merges. | M063, M330, S151, S213 | |
| M030 | docs/METHOD.md, The pipeline, one unit per session, L49-50 | Record: each residual is a file, `docs/residuals/<unit>-<slug>.md`, with no number; `docs/residuals/README.md` is the form. | C027, S190 | |
| M031 | docs/METHOD.md, The pipeline, one unit per session, L50-53 | A residual meeting the board bar says `issue: yes`, and the issue is filed once the number exists. | M080 | |
| M032 | docs/METHOD.md, The pipeline, one unit per session, L53-55 | A `docs/solutions/` entry only if the unit found something a future session would get wrong without it, written in the existing frontmatter form. | M222, S192 | |
| M033 | docs/METHOD.md, The pipeline, one unit per session, L55-57 | The unit's restart paragraph is its own file, `docs/restart/<unit>.md` (`u114.md`, `r572.md`), never a paragraph in `RESTART-cratekit.md`, which `scan_repo.py` refuses. | C005, M214, M215, S189 | |
| M034 | docs/METHOD.md, The pipeline, one unit per session, L57-58 | No explainer. | C101, M230 | |
| M035 | docs/METHOD.md, The pipeline, one unit per session, L59 | Merge: the battery from inside the checkout. |  | |
| M036 | docs/METHOD.md, The pipeline, one unit per session, L59-60 | Merge: the closing keyword scan over the whole range. | M199, M200, S197, S199 | |
| M037 | docs/METHOD.md, The pipeline, one unit per session, L60-61 | Merge: a pull request merged once CI on its head is green. | C079, M185, S194 | |
| M038 | docs/METHOD.md, The pipeline, one unit per session, L61-62 | Then on `main` run `board.py residuals` with the `land` flag and commit what it numbered. | S220 | |
| M039 | docs/METHOD.md, The pipeline, one unit per session, L63 | Then push `main`. | S220 | |
| M040 | docs/METHOD.md, The pipeline, one unit per session, L63 | Delete the local branch (the merged pull request takes the remote one). | M194 | |
| M041 | docs/METHOD.md, The pipeline, one unit per session, L64 | Then `board.py audit`. | S226 | |
| M042 | docs/METHOD.md, The pipeline, one unit per session, L64-65 | File the issue for each residual the `land` run names as meeting the board bar. | M075, S223 | |
| M043 | docs/METHOD.md, Card sizes, decided by Phillip on 2026-11-02, L67 | Card sizes were decided by Phillip on 2026-11-02. |  | |
| M044 | docs/METHOD.md, Card sizes, decided by Phillip on 2026-11-02, L69-70 | The plan names the card's size from its brief, so the process is sized to what the card can damage (U196). | S133 | |
| M045 | docs/METHOD.md, Card sizes, decided by Phillip on 2026-11-02, L70-71 | A card that adds or changes a path that writes or deletes is large, whatever its size in lines. |  | |
| M046 | docs/METHOD.md, Card sizes, decided by Phillip on 2026-11-02, L73-74 | Small: under about 200 lines of source, no new or changed path that writes or deletes, or docs and skill text only. |  | |
| M047 | docs/METHOD.md, Card sizes, decided by Phillip on 2026-11-02, L74 | A small card builds at medium effort. | S021 | |
| M048 | docs/METHOD.md, Card sizes, decided by Phillip on 2026-11-02, L74-75 | A small card gets one review round by Fable at high effort. |  | |
| M049 | docs/METHOD.md, Card sizes, decided by Phillip on 2026-11-02, L75-76 | A small card's second review round is spent only if the first finds something BLOCKING. | S149 | |
| M050 | docs/METHOD.md, Card sizes, decided by Phillip on 2026-11-02, L77-78 | Medium: everything else that writes or deletes nothing; built at high effort, up to two review rounds. |  | |
| M051 | docs/METHOD.md, Card sizes, decided by Phillip on 2026-11-02, L79-80 | Large: anything that writes or deletes; built at high effort, up to two review rounds, the full mutation table. |  | |
| M052 | docs/METHOD.md, Card sizes, decided by Phillip on 2026-11-02, L82-84 | A thread may build up to three small cards in the same module in a row, each with its own branch from the current `main`, its own pull request, review, record and landing. | S230, S231 | |
| M053 | docs/METHOD.md, Card sizes, decided by Phillip on 2026-11-02, L84-86 | The second and third reuse the thread's Linux baseline unless `main` moved in `src`, `tests`, `scripts` or `pyproject.toml` since it was measured, in which case it is measured again. | S232 | |
| M054 | docs/METHOD.md, Card sizes, decided by Phillip on 2026-11-02, L88-89 | The merge bar, the two round cap and every standing constraint are the same for every size. | M270 | |
| M055 | docs/METHOD.md, The merge bar, decided 2026-08-09, L91 | The merge bar was decided 2026-08-09. | M056 | |
| M056 | docs/METHOD.md, The merge bar, decided 2026-08-09, L93 | A branch merges when it has no open BLOCKING finding. | M055 | |
| M057 | docs/METHOD.md, The merge bar, decided 2026-08-09, L95-97 | A finding is BLOCKING only if all three hold; first, it was driven end to end, not argued from reading the source. |  | |
| M058 | docs/METHOD.md, The merge bar, decided 2026-08-09, L98-100 | Second, it has a named user facing cost: someone loses data, is told something false, is blocked from a verb, or is shown a clean report over state the tool could not read. |  | |
| M059 | docs/METHOD.md, The merge bar, decided 2026-08-09, L101-103 | Third, its input is reachable and the producer was DRIVEN: name the producer and drive it. | M060 | |
| M060 | docs/METHOD.md, The merge bar, decided 2026-08-09, L103-104 | If the producer cannot be driven, the finding is a RESIDUAL and the report says the reachability is unmeasured. | M059 | |
| M061 | docs/METHOD.md, The merge bar, decided 2026-08-09, L104-105 | Say "N candidates were driven and none produces it", never "nothing produces it". |  | |
| M062 | docs/METHOD.md, The merge bar, decided 2026-08-09, L107-110 | Everything else is a RESIDUAL (an overclaiming docstring, an assertion naming the wrong number, a guard that kills zero tests, an unreproduced document count): file it with its measured cost, never hold a merge for it. |  | |
| M063 | docs/METHOD.md, The merge bar, decided 2026-08-09, L116 | Hard cap: each unit has at most two fix rounds. | M029, M330, S151, S213 | |
| M064 | docs/METHOD.md, The merge bar, decided 2026-08-09, L119 | Round two reviews the fix, not the branch again, decided by U196. | S147 | |
| M065 | docs/METHOD.md, The merge bar, decided 2026-08-09, L119-121 | When round one found nothing BLOCKING and no file under `src`, `tests` or `scripts` changed after it, there is no round two. | S148 | |
| M066 | docs/METHOD.md, The merge bar, decided 2026-08-09, L121-123 | Otherwise round two reads only the commits after round one, `git diff <round one head>..HEAD`, with the branch's whole diff at hand for context. | S150 | |
| M067 | docs/METHOD.md, The merge bar, decided 2026-08-09, L123-124 | Round two hunts the class one file over, as the fifth pattern says. | M158 | |
| M068 | docs/METHOD.md, The board bar, decided 2026-09-18, L127 | The board bar was decided 2026-09-18. | C029, M069 | |
| M069 | docs/METHOD.md, The board bar, decided 2026-09-18, L129-131 | Most residuals stay in the ledger and earn no issue; one earns an issue, the moment it is filed, only when it is open and a person using the shipped verbs pays for it in one of four ways. | C029, M068 | |
| M070 | docs/METHOD.md, The board bar, decided 2026-09-18, L131-132 | Way (a): files or database rows can be lost or damaged. |  | |
| M071 | docs/METHOD.md, The board bar, decided 2026-09-18, L132-133 | Way (b): the product says something false, a clean report over state it could not read, or a declared write it never performs. |  | |
| M072 | docs/METHOD.md, The board bar, decided 2026-09-18, L133-134 | Way (c): a workflow a DJ needs cannot finish. |  | |
| M073 | docs/METHOD.md, The board bar, decided 2026-09-18, L134-135 | Way (d): a guard on a path that writes or deletes is absent or kills nothing. |  | |
| M074 | docs/METHOD.md, The board bar, decided 2026-09-18, L135-136 | A maintainer facing finding, a wording fix, a count in a document, or anything that closes only at an attended sitting earns no issue. |  | |
| M075 | docs/METHOD.md, The board bar, decided 2026-09-18, L138 | File it with `gh issue create` for repo philgutowski/cratekit with label `residual`. | M042, S223 | |
| M076 | docs/METHOD.md, The board bar, decided 2026-09-18, L139-140 | Title it `R-N: ` followed by the ledger heading EXACTLY, since `board.py audit` compares the two. | S223 | |
| M077 | docs/METHOD.md, The board bar, decided 2026-09-18, L140-141 | The body opens `**Depends on:** none` and carries goal, key files, approach, test scenarios and out of scope. | S223 | |
| M078 | docs/METHOD.md, The board bar, decided 2026-09-18, L141 | Add the residual issue to project 2. |  | |
| M079 | docs/METHOD.md, The board bar, decided 2026-09-18, L142-143 | Create the issue AFTER `board.py residuals` with `land` numbers it on `main`, because a number is not the finding's until then. |  | |
| M080 | docs/METHOD.md, The board bar, decided 2026-09-18, L143-144 | The unit marks it `issue: yes` in its residual file so whoever lands it knows to file. | M031 | |
| M081 | docs/METHOD.md, The board bar, decided 2026-09-18, L144-145 | The Relay feeder picks up any open issue labelled `residual` or `unit` that the board derives as ready. |  | |
| M082 | docs/METHOD.md, The board bar, decided 2026-09-18, L147 | Never write a literal dot claude path in a card, title, body or comment, not even to forbid one. | M083, M084, S044 | |
| M083 | docs/METHOD.md, The board bar, decided 2026-09-18, L147-150 | Reason: Relay skips, silently, any card whose text names that directory, because an edit there needs an attended session. | M082, M084, S044 | |
| M084 | docs/METHOD.md, The board bar, decided 2026-09-18, L151 | Describe the location in words instead. | M082, M083, S044 | |
| M085 | docs/METHOD.md, Verification is the author's, and says so, L155 | No independent verifier, decided 2026-09-07. | M086 | |
| M086 | docs/METHOD.md, Verification is the author's, and says so, L155-156 | The author runs the mutation table and the review. | M085 | |
| M087 | docs/METHOD.md, Verification is the author's, and says so, L156-157 | The gap is measured: independent tables found 17 where the author found 10, 49 against 39, 83 against 49. |  | |
| M088 | docs/METHOD.md, Verification is the author's, and says so, L157-159 | Every zero row reads as "the author could not kill it", and the record says exactly that in one line. |  | |
| M089 | docs/METHOD.md, Verification is the author's, and says so, L159-160 | Phillip can ask for a full pass on a unit that writes or deletes; it is his to ask for. |  | |
| M090 | docs/METHOD.md, Verification is the author's, and says so, L162-163 | Verification depth is proportional to blast radius, decided by Phillip on 2026-11-02 (U196). | S154 | |
| M091 | docs/METHOD.md, Verification is the author's, and says so, L163-164 | A unit that writes or deletes gets its full 25 rows and a composite on every user facing zero. | S155 | |
| M092 | docs/METHOD.md, Verification is the author's, and says so, L164-165 | A read only report or static registry gets about 8 rows scoped to its new guards and a line per zero. | S156 | |
| M093 | docs/METHOD.md, Verification is the author's, and says so, L165-167 | A unit changing only docs or skill text gets no table; its record says so in one line. | S157 | |
| M094 | docs/METHOD.md, The mutation table, L171-172 | Revert each new guard one at a time, run the suite, count the deaths; a guard that kills zero tests is a finding. |  | |
| M095 | docs/METHOD.md, The mutation table, L174-175 | Scope the table to the round's own diff, plus a fixed sample of the unit's existing guards. | S158 | |
| M096 | docs/METHOD.md, The mutation table, L175 | Hard cap: 25 rows, one pass per unit per session. | M027 | |
| M097 | docs/METHOD.md, The mutation table, L175-177 | On hitting the cap, stop and log what you dropped and why you ranked it below the cap. |  | |
| M098 | docs/METHOD.md, The mutation table, L179 | Use `scripts/mutate.py`; do not hand roll a driver. |  | |
| M099 | docs/METHOD.md, The mutation table, L181-183 | Do not edit `tests/` while the driver runs (it snapshots and restores only the src file it mutates). |  | |
| M100 | docs/METHOD.md, The mutation table, L185 | Confirm deaths on a subset; spend a full suite only on zero rows. |  | |
| M101 | docs/METHOD.md, The mutation table, L185-186 | Select the subset as the test files importing the mutated module. |  | |
| M102 | docs/METHOD.md, The mutation table, L186-188 | A death on a subset is real; a zero on a subset is promoted to a full run before it is reported. |  | |
| M103 | docs/METHOD.md, The mutation table, L190-191 | The full baseline may be read, never the rest, decided by Phillip on 2026-11-13 (U271). | M104, M281, S162 | |
| M104 | docs/METHOD.md, The mutation table, L191-194 | On a cloud container `cloud_battery.py compare` and `baseline` leave a run record, `.cloud-battery/verdict.json`, and the driver given `known-failures` reads its full baseline from it instead of running the suite again. | M103, M281, S162 | |
| M105 | docs/METHOD.md, The mutation table, L194-198 | Only when: the record is for this HEAD's commit; the tree was clean throughout that run and is clean now; host, boot, checkout and interpreter are this run's; the known failures file is the same by sha256; that run ran every collected test with no `PYTEST_ADDOPTS` editing it. | M106, S162 | |
| M106 | docs/METHOD.md, The mutation table, L198-199 | Any difference and the driver measures, naming why. | M105, S162 | |
| M107 | docs/METHOD.md, The mutation table, L199 | A red record refuses the batch as a red baseline does. |  | |
| M108 | docs/METHOD.md, The mutation table, L200 | Every subset baseline is still measured. | S164 | |
| M109 | docs/METHOD.md, The mutation table, L200-201 | The null control still runs the full suite in the driver's own environment, held to the read collected count. | S164 | |
| M110 | docs/METHOD.md, The mutation table, L202 | The table says which baseline was read and which measured. |  | |
| M111 | docs/METHOD.md, The mutation table, L202-203 | The `measure-baseline` flag measures regardless. |  | |
| M112 | docs/METHOD.md, The mutation table, L203-204 | So the rows are committed and `compare` run on that head before the driver. | S159, S182 | |
| M113 | docs/METHOD.md, The mutation table, L206-208 | A zero death row on a guard with a USER FACING surface is acceptable only when a composite shows what it does hold: pair it with a mutation of the thing it guards and report both counts. | M114, S169 | |
| M114 | docs/METHOD.md, The mutation table, L208 | A prose argument is not evidence. | M113, S169 | |
| M115 | docs/METHOD.md, The mutation table, L210 | A zero row on a maintainer facing guard gets one line, not a composite. |  | |
| M116 | docs/METHOD.md, The mutation table, L212-214 | Write the table into the repository under `docs/mutation/`, with full row descriptions, not only counts; a table only in chat is a claim. | S170 | |
| M117 | docs/METHOD.md, The mutation table, L216 | A recorded kill can be replayed, and a restructuring is held to it (U297). | S171 | |
| M118 | docs/METHOD.md, The mutation table, L217-220 | `scripts/killset.py list` says which recorded kills under `docs/mutation/` still apply; `killset.py rows PATH ...` with `out FILE` writes them as a row file for the driver's third pass kind, `replay`. | S174 | |
| M119 | docs/METHOD.md, The mutation table, L220-221 | A replay has no row cap; every replay row must name the table and id it came from. |  | |
| M120 | docs/METHOD.md, The mutation table, L221-222 | A replay is never a unit's own table, whose cap of 25 stands. | S171 | |
| M121 | docs/METHOD.md, The mutation table, L222-224 | A unit that restructures code replays the kills of the files it owns before its first edit and after its last. | S172 | |
| M122 | docs/METHOD.md, The mutation table, L224-226 | The second replay comes from `killset.py rows` with `after BEFORE.json`, which follows text to another file only when that file did not hold it at the commit the first table was measured on. |  | |
| M123 | docs/METHOD.md, The mutation table, L226-228 | `killset.py check BEFORE.json AFTER.json` fails on any kill the second table lost that is not mapped, with its reason, to a row that is killed. | S173, S176 | |
| M124 | docs/METHOD.md, The mutation table, L228-229 | The driver checks every replay row's source against the table it names. |  | |
| M125 | docs/METHOD.md, The mutation table, L229 | A replay resumes only from a sidecar of the same commit. | S177 | |
| M126 | docs/METHOD.md, The mutation table, L231 | Behaviour is compared, not argued (U297). | S178 | |
| M127 | docs/METHOD.md, The mutation table, L231-237 | `scripts/behaviour_compare.py capture` with `out DIR` runs the scenarios under `tests/behaviour/` (one file per package, or per package and verb where fixtures share a name) on a disposable library with clock and generated ids pinned, keeping output, exit codes, files with permission bits, and every database's schema, settings and rows. | S179 | |
| M128 | docs/METHOD.md, The mutation table, L237-239 | `rev` runs the scenarios against another revision's `src/`; `compare` prints each difference and exits 1 on any. | S179 | |
| M129 | docs/METHOD.md, The mutation table, L240-242 | A unit that must leave behaviour unchanged compares its base with its branch, and first adds a scenario for any verb it touches that has none. | S178 | |
| M130 | docs/METHOD.md, Reading discipline, because context is what you are billed for, L249 | Never read a file over 400 lines whole. |  | |
| M131 | docs/METHOD.md, Reading discipline, because context is what you are billed for, L249-250 | Grep for the symbol, then read the region around it. |  | |
| M132 | docs/METHOD.md, Reading discipline, because context is what you are billed for, L250-252 | `docs/residual-findings.md` is over forty thousand lines with over a thousand headings: find a finding with `board.py residuals` and `search WORDS`, grep for `^## R-NNN`, and read that entry. | C031 | |
| M133 | docs/METHOD.md, Reading discipline, because context is what you are billed for, L252-253 | Never print every ledger heading. |  | |
| M134 | docs/METHOD.md, Reading discipline, because context is what you are billed for, L254-255 | Delegate a sweep: a search across many files goes to a read only subagent that returns the answer, not the file dumps. |  | |
| M135 | docs/METHOD.md, Reading discipline, because context is what you are billed for, L256-258 | Every report opens with a verdict header under 60 lines: the verdict, a numbered finding table with each finding's classification, and the battery numbers. |  | |
| M136 | docs/METHOD.md, Reading discipline, because context is what you are billed for, L259 | Do not re-read a prior round's full mutation table; read its summary rows. |  | |
| M137 | docs/METHOD.md, Driver rules, every one of them paid for, L263-265 | Never pass `-q`, including to a collection run (`pyproject.toml` already sets it, so yours becomes `-qq` and hides the summary and collect listing). |  | |
| M138 | docs/METHOD.md, Driver rules, every one of them paid for, L265-266 | Use `pytest` with `tb=no` for counts and `pytest` with `collect-only -o addopts=` for the collected count. |  | |
| M139 | docs/METHOD.md, Driver rules, every one of them paid for, L267-268 | Check the collected count on every row. | M213 | |
| M140 | docs/METHOD.md, Driver rules, every one of them paid for, L269 | One driver at a time, waited on, with nothing else touching the tree. |  | |
| M141 | docs/METHOD.md, Driver rules, every one of them paid for, L272-275 | Corrected by U65, 2026-09-17: `mutate.py`'s fixed overhead exceeds 600 seconds, the harness tool ceiling, so a foreground run is killed mid row; the old run-in-the-foreground rule is gone. |  | |
| M142 | docs/METHOD.md, Driver rules, every one of them paid for, L275-279 | The driver inherits `-n auto` since 2026-09-18 and worksteal distribution since U251; a full baseline was about a minute on 11 cores at 7,678 tests and is about twelve on a four core container at 18,550, and a 25 row table passes the ceiling either way. | M167, S121 | |
| M143 | docs/METHOD.md, Driver rules, every one of them paid for, L281-283 | Run the driver as a tracked background job, start nothing else against the tree until it reports, and then check `git status` plus every row's `head_verified`. | S160 | |
| M144 | docs/METHOD.md, Driver rules, every one of them paid for, L284-285 | Never let a driver invoke git; snapshot and rewrite file text yourself. |  | |
| M145 | docs/METHOD.md, Driver rules, every one of them paid for, L286-287 | Verify restores against `git show HEAD:<path>`, never against a scratch copy. |  | |
| M146 | docs/METHOD.md, Driver rules, every one of them paid for, L288-289 | Set `PYTHONDONTWRITEBYTECODE=1`. |  | |
| M147 | docs/METHOD.md, Driver rules, every one of them paid for, L290-293 | Read node ids from pytest report objects, never by splitting a `FAILED` line on `" - "` nor by cutting it at a space; the cloud battery did so until U268. | M280, S124, S166 | |
| M148 | docs/METHOD.md, Driver rules, every one of them paid for, L294 | Reword a message mutation, never append (the suite asserts with `in`). |  | |
| M149 | docs/METHOD.md, Driver rules, every one of them paid for, L295-296 | Mutate to a realistic nearby value, and mutate coefficients too. |  | |
| M150 | docs/METHOD.md, Driver rules, every one of them paid for, L297-298 | Remove each guard layer alone. |  | |
| M151 | docs/METHOD.md, Driver rules, every one of them paid for, L299 | A timing row carries a repeat count and a pass rate, never one number. |  | |
| M152 | docs/METHOD.md, Driver rules, every one of them paid for, L300 | Every number was measured or the report says it was not. |  | |
| M153 | docs/METHOD.md, Driver rules, every one of them paid for, L300-301 | Offer no mechanism for a discrepancy without a measurement showing it operating. |  | |
| M154 | docs/METHOD.md, The four recurring defect patterns, L305-306 | Pattern 1 to hunt: absence read as evidence of absence, the most productive pattern here. |  | |
| M155 | docs/METHOD.md, The four recurring defect patterns, L307-308 | Pattern 2: identity that is not unique to the thing it identifies (a single field trusted alone). |  | |
| M156 | docs/METHOD.md, The four recurring defect patterns, L309-310 | Pattern 3: a fix that lands on the performing path instead of the checking path. |  | |
| M157 | docs/METHOD.md, The four recurring defect patterns, L311-314 | Pattern 4: a fix justified by a measurement on a fixture rather than the tree; ask of every justifying number whether it was taken on the tree. |  | |
| M158 | docs/METHOD.md, The four recurring defect patterns, L316-318 | Pattern 5: a fix round reproduces the class one file over; after every fix, look for the same shape elsewhere and say what you found. | M067 | |
| M159 | docs/METHOD.md, What a green suite cannot see, so hunt it separately, L322-324 | Hunt a test whose expected value comes from the code under test; sweep with an AST walk over every `assert` in `tests/`, not a grep. |  | |
| M160 | docs/METHOD.md, What a green suite cannot see, so hunt it separately, L325-326 | Hunt a test that forbids a feature by naming the last implementation's symbols. |  | |
| M161 | docs/METHOD.md, What a green suite cannot see, so hunt it separately, L327 | Hunt duplicate keys in a mapping several branches appended to. |  | |
| M162 | docs/METHOD.md, What a green suite cannot see, so hunt it separately, L328 | Hunt one symbol meaning two things in two modules. |  | |
| M163 | docs/METHOD.md, What a green suite cannot see, so hunt it separately, L329-331 | The first caller of an engine owns its unreviewed failure paths: `git grep -n <engine>` in `src` before binding a worker, and if the definition is the only hit, read the engine's error paths as your own. |  | |
| M164 | docs/METHOD.md, The battery, L335-336 | Nothing merges until all three are clean, run from inside the checkout that holds the branch, with that checkout's own venv. | C040 | |
| M165 | docs/METHOD.md, The battery, L338-340 | Commands: `./.venv/bin/ruff check src tests scripts`, `./.venv/bin/python -m pytest` with `tb=no`, `./.venv/bin/python scripts/scan_repo.py`. | C041, S184 | |
| M166 | docs/METHOD.md, The battery, L342-346 | The suite is parallel: `addopts` carries `-n auto` with worksteal distribution, so the command uses every core (U251). |  | |
| M167 | docs/METHOD.md, The battery, L346-350 | Measured 2026-11-12 on a four core Linux container at 18,550 tests: a full run is about twelve minutes, 680 to 771 seconds over three runs, against 964 under the default distribution; on 11 cores it was 61 to 67 seconds at 7,678 tests on 2026-09-18, not measured since. | M142, S121 | |
| M168 | docs/METHOD.md, The battery, L350-351 | A venv made before 2026-09-18 needs `pip install -e '.[dev]'` once for `pytest-xdist`. |  | |
| M169 | docs/METHOD.md, The battery, L351 | Pass `-n 0` for a debugger or a profiler. |  | |
| M170 | docs/METHOD.md, The battery, L353 | The full battery is the MERGE gate, not the edit loop. | C043, M171, S139 | |
| M171 | docs/METHOD.md, The battery, L353-355 | While building, run the test files for the modules you touched, `pytest tests/test_x.py`. | C043, M170, S139 | |
| M172 | docs/METHOD.md, The battery, L355-356 | Run the full suite before the review, after each fix round and at the merge, not after every edit. |  | |
| M173 | docs/METHOD.md, The battery, L359 | A new slow test is a finding; run `pytest` with `durations=10` at the merge. |  | |
| M174 | docs/METHOD.md, The battery, L360-361 | A test over ten seconds is either real work (a process pool or a disk image) or a real sleep nobody faked. |  | |
| M175 | docs/METHOD.md, The battery, L364 | Run the battery on a COMMITTED tree. |  | |
| M176 | docs/METHOD.md, The battery, L370 | Do not symlink `.venv` into a worktree. | C078 | |
| M177 | docs/METHOD.md, The battery, L372-373 | A worktree gets its own venv, `python3.12 -m venv .venv` then `pip install -e '.[dev]'`, and its own scratch directory named for its unit. | S010 | |
| M178 | docs/METHOD.md, What CI is for, decided 2026-08-15, L375 | CI's purpose was decided 2026-08-15. | M180 | |
| M179 | docs/METHOD.md, What CI is for, decided 2026-08-15, L377-378 | The battery is the merge gate; CI is not, and does not run the suite. | S183 | |
| M180 | docs/METHOD.md, What CI is for, decided 2026-08-15, L378-382 | CI proves packaging and portability: install from a clean checkout on 3.12 and 3.13, the slim profile pulls in no DSP and no ML stack, the vendored downloader shipped, ruff is clean, no personal path or credential reached the tree. | M178 | |
| M181 | docs/METHOD.md, What CI is for, decided 2026-08-15, L384 | A step in `.github/workflows/ci.yml` must be able to pass. | M182 | |
| M182 | docs/METHOD.md, What CI is for, decided 2026-08-15, L384-385 | A check that cannot pass belongs in the battery (bought by R-115). | M181 | |
| M183 | docs/METHOD.md, What CI is for, decided 2026-08-15, L387 | Nothing is deselected, deliberately. | M286, S020 | |
| M184 | docs/METHOD.md, What CI is for, decided 2026-08-15, L388-389 | Before blaming the platform for a red run, drive it. |  | |
| M185 | docs/METHOD.md, Committing and merging, L393-395 | A pull request per unit, merged by the session that opened it once CI is green, decided by U158 on 2026-10-28, replacing the old no pull requests rule. | C079, M037, S194 | |
| M186 | docs/METHOD.md, Committing and merging, L395-396 | Feature branch per unit, push it, open a pull request against `main`. | C080, S120 | |
| M187 | docs/METHOD.md, Committing and merging, L396 | Wait for every check on its head commit to finish green. | S209, S210 | |
| M188 | docs/METHOD.md, Committing and merging, L396-398 | Merge through the GitHub API as a merge commit titled `merge(uN): <what landed>` whose message ends with the closing trailer. | C081, S216, S217 | |
| M189 | docs/METHOD.md, Committing and merging, L398-399 | Never a pull request that waits on a person: no reviewer is requested and nobody approves it. | C083, M238, S035, S194 | |
| M190 | docs/METHOD.md, Committing and merging, L399-401 | The pull request body is the landing's record: the battery, the review rounds, the mutation table, the residuals, what is OWED. | S202, S203, S204 | |
| M191 | docs/METHOD.md, Committing and merging, L401-403 | The body carries no closing keyword (a close from the body would bypass the closing check); the merge commit's trailer is the one close. | C084, S036, S205 | |
| M192 | docs/METHOD.md, Committing and merging, L403-404 | CI judges the pull request's own range and the card its head branch names, so a unit a register still owes cannot merge. | C085, S212 | |
| M193 | docs/METHOD.md, Committing and merging, L405-406 | If the merge endpoint is refused, merge locally with the same message and push `main`; the pull request stays as the record. | S219 | |
| M194 | docs/METHOD.md, Committing and merging, L406-408 | "Automatically delete head branches" removes a merged pull request's branch; delete the local one with `git branch -d <branch>`. | C082, C088, M040, M293, M311, S013 | |
| M195 | docs/METHOD.md, Committing and merging, L409-410 | `git push origin` with the `all` flag fails on this connection with `RPC failed; HTTP 400`; push one branch at a time. |  | |
| M196 | docs/METHOD.md, Committing and merging, L411-412 | No em dashes, no en dashes, no double hyphens in prose, comments, commit messages or issue bodies. | C093, S043 | |
| M197 | docs/METHOD.md, Committing and merging, L412 | Favor commas over colons. | C094 | |
| M198 | docs/METHOD.md, Committing and merging, L413-416 | Check `tests/_pending.py` before writing a closing trailer; if the register still owes the unit a module, merge without the trailer and close the issue when the register is discharged. | C037, S196, S199, S200 | |
| M199 | docs/METHOD.md, Committing and merging, L417-418 | GitHub matches a closing keyword anywhere in a body and scans every commit in the pushed range. | M036, M200, S197, S199 | |
| M200 | docs/METHOD.md, Committing and merging, L418-420 | Scan the RANGE before every push, not only a merge, with the `git log origin/main..main` grep given. | M036, M199, S197, S199 | |
| M201 | docs/METHOD.md, Committing and merging, L422-424 | NEVER write a closing keyword adjacent to an issue number, even to quote one, even inside backticks, even to say it is unsafe. | M202, S045 | |
| M202 | docs/METHOD.md, Committing and merging, L425-426 | Put words between the keyword and the number, or name the unit instead of its number. | M201, S045 | |
| M203 | docs/METHOD.md, Committing and merging, L426-428 | A branch already carrying such a string cannot be made safe by the merge commit: rewrite those bodies, or expect the close and reopen the issue after the push. |  | |
| M204 | docs/METHOD.md, Committing and merging, L429-430 | Residual numbers are APPEND ONLY; a number once given is that finding's for life. | M206, M207 | |
| M205 | docs/METHOD.md, Committing and merging, L430-433 | A number is given at landing and nowhere else, decided by U124: units file unnumbered, and `board.py residuals` with `land`, which refuses off `main`, gives each the next number past the ledger's highest. | C028 | |
| M206 | docs/METHOD.md, Committing and merging, L433-434 | Numbers on `main` never move, no branch is ever renumbered, and gaps are fine. | M204, M207 | |
| M207 | docs/METHOD.md, Committing and merging, L434-436 | A renumber is forbidden (issue titles carry residual numbers, a surface the repository cannot see). | M204, M206 | |
| M208 | docs/METHOD.md, Committing and merging, L436-437 | A branch built before U124 that numbers its own entries takes fresh numbers above `main`'s highest at the merge. |  | |
| M209 | docs/METHOD.md, Committing and merging, L438-441 | Verify a merge with both greps: duplicate `^## R-` headings must be empty, and removed `## R-` lines in the ledger diff against `origin/main` must be empty. |  | |
| M210 | docs/METHOD.md, Committing and merging, L443-444 | Use git's merge algorithm only; `diff3 -m` silently breaks `tests/_pending.py`. |  | |
| M211 | docs/METHOD.md, Committing and merging, L445-448 | A countdown entry is discharged in THREE edits in one commit (delete the `PENDING` entry, delete the `EXPECTED_PENDING` key, remove `@requires("<key>")` from EVERY guard it gated after a grep); one alone is worse than none. |  | |
| M212 | docs/METHOD.md, Committing and merging, L451-452 | Then run the newly armed guard on purpose, because it has never executed. |  | |
| M213 | docs/METHOD.md, Committing and merging, L453-454 | Reconcile the collected count by identifier, not by total. | M139 | |
| M214 | docs/METHOD.md, Committing and merging, L455-457 | A unit's restart paragraph is its own file, decided by U124: `docs/restart/<unit>.md`. | C005, M033, M215, S189 | |
| M215 | docs/METHOD.md, Committing and merging, L457-458 | `RESTART-cratekit.md` keeps only the sections no unit owns, and `scan_repo.py` refuses a unit's paragraph anywhere in it. | C005, M033, M214, S189 | |
| M216 | docs/METHOD.md, Committing and merging, L458-460 | A branch built before U124 that conflicts there moves its paragraph into its fragment and takes `main`'s `RESTART-cratekit.md` as it is. |  | |
| M217 | docs/METHOD.md, Committing and merging, L462 | Reserved-cause pins are per module, decided by U125. | M218 | |
| M218 | docs/METHOD.md, Committing and merging, L462-466 | `tests/test_reserved_causes.py` populations are pinned through `tests/_pinned_reserved_populations.py`: kebab literals and holders by module, one file per package under `tests/ratchets/reserved_causes/` since U296, non-reserved causes one slug per line. | M217 | |
| M219 | docs/METHOD.md, Committing and merging, L466-467 | Pin totals are derived from the pins, never hand-edited. |  | |
| M220 | docs/METHOD.md, Committing and merging, L467-469 | When a merge moves a pin, update only the modules or slugs that joined or left, measured on the merged tree, with a dated comment on those entries. |  | |
| M221 | docs/METHOD.md, Committing and merging, L469-470 | Do not reintroduce a whole-repository total tuple. |  | |
| M222 | docs/METHOD.md, Learnings, filed directly, L474-476 | A learning goes to `docs/solutions/<category>/<slug>.md` with `module`, `problem_type`, `tags` frontmatter, written by the session that found it, in the same commit as the record. | M032, S192 | |
| M223 | docs/METHOD.md, Learnings, filed directly, L476-479 | The bar: a cause not where it looked, a contract or seam whose rules are not visible in the code, a decision reversed with a reason, or a trap that cost real time. | M224 | |
| M224 | docs/METHOD.md, Learnings, filed directly, L479 | Routine work files nothing. | M223 | |
| M225 | docs/METHOD.md, Learnings, filed directly, L479-480 | `CONCEPTS.md` gains a term when a unit introduces a word with a specific meaning here. |  | |
| M226 | docs/METHOD.md, Explanations, batched per phase, decided 2026-09-07, L482 | Explanations batched per phase, decided 2026-09-07. | C098, M227 | |
| M227 | docs/METHOD.md, Explanations, batched per phase, decided 2026-09-07, L484-485 | The rule that every change ships with an explanation Phillip can give in an interview is met per phase, not per unit. | C098, M226 | |
| M228 | docs/METHOD.md, Explanations, batched per phase, decided 2026-09-07, L485-486 | Units land with commit messages and the record. | C099 | |
| M229 | docs/METHOD.md, Explanations, batched per phase, decided 2026-09-07, L486-487 | When a phase merges, Phillip runs the `code-explainer` skill over the merged range once. | C100 | |
| M230 | docs/METHOD.md, Explanations, batched per phase, decided 2026-09-07, L487 | A session does not run it. | C101, M034 | |
| M231 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L489 | The cloud lane was decided 2026-10-27. | C009, M232, S002 | |
| M232 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L491 | The cloud is where Cratekit is built. | C009, M231, S002 | |
| M233 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L491-494 | The building project's coordinator fills the cloud's lanes with fresh build threads on Opus 5.5, one card each, waking hourly to fill any lane that freed. | C011, S064, S066 | |
| M234 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L494-495 | The other project files the cards and keeps the decisions page. | C010, C092, M300 | |
| M235 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L495-497 | The coordinator replaced the lane dispatcher (a long lived cloud session woken by a scheduled task), which ran from 2026-10-27 and was retired on 2026-10-31. |  | |
| M236 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L498-503 | Each build thread runs the `cloud-unit` skill (METHOD's pipeline with the cloud's changes): take card, brainstorm if an idea, plan, build, review, mutation table, record, pull request merged to `main` with the closing trailer once CI is green (U158). | C012, S003 | |
| M237 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L503-505 | Phillip authorized the cloud to write `main` on 2026-10-27; a self-merged pull request is that same authority with a record and a CI run first. | C087 | |
| M238 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L506 | No pull request waits on a person. | C083, M189, S035, S194 | |
| M239 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L506-508 | Only a card that cannot be built without the machine (live database, library volume, live account, rekordbox, or Phillip at the desktop) is built locally. | C015, M240, S004, S054, S109, S111 | |
| M240 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L509-510 | The session sets such a card aside with a comment carrying the local steps. | C015, M239, S004, S054, S109, S111 | |
| M241 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L510 | A card labelled `attended` is never offered at all. | S061 | |
| M242 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L512-513 | The queue is every open unit and residual card that is ready, read by `board.py cloud` from each card's comments over REST. | S096 | |
| M243 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L513-514 | The session writes no label and no status. | C034, S037 | |
| M244 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L514-515 | Its hold is its own comment headed `Started`. | S047, S101 | |
| M245 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L515-516 | Plan, progress notes, brainstorm, set-aside and landing are comments headed `Plan`, `Progress`, `Brainstorm`, `Needs the machine` and `Landed`. | S046 | |
| M246 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L516-518 | Phillip's answer is any comment without the session footer after the question, or any comment headed `Answer from Phillip` whoever posts it. | S053, S060 | |
| M247 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L518-520 | The cloud has ten lanes, and the building project runs at most ten threads at once, Phillip's decision of 2026-11-21 (`CLOUD_LANES` in `scripts/board.py`). | M301, S065, S096 | |
| M248 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L521-522 | Superseded lane decisions: three lanes on 2026-10-28, five on 2026-10-31, Phillip's cap of four threads on 2026-11-05. |  | |
| M249 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L522-524 | The coordinator counts lanes by its own running threads, not by the held count `board.py cloud` prints (which stops counting a card once its thread posts a question). | S065 | |
| M250 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L524-526 | Each worker merges the latest `main` into its branch and runs the battery again before it merges. | S195, S211, S215 | |
| M251 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L527-528 | A hold beyond the lane count withdraws, the earliest holds keeping theirs. | S055, S102 | |
| M252 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L528-530 | A hold with no comment for eight hours is a session that died, and the next session resumes it from its pushed branch. | S062, S104 | |
| M253 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L532-533 | A decision that is Phillip's goes on the decisions page, https://claude.ai/artifact/FUqChoK5qKhztLdzzEADaS, decided 2026-10-28. | C016, M264, S070 | |
| M254 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L533-536 | A build thread that reaches one (a brainstorm's questions or a question a brief leaves open) posts it on its card only, under a `Brainstorm` or `Question for Phillip` heading. | C017, M304, S071 | |
| M255 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L535 | Each question is a multiple choice with its recommendation first. | M316, S073, S115 | |
| M256 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L536 | The build thread never writes the decisions page. | M303, S071, S077, S116 | |
| M257 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L537 | The project that files the cards copies the question there. | C018, M307, S076 | |
| M258 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L538 | A brainstorm waits for his answer. | S051 | |
| M259 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L538-539 | A question does not stop the build, which makes the conservative call, records it and keeps going. | C019, M012, M013, M306, S008, S075 | |
| M260 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L540-546 | The relay thread ("Wire decisions page answers to cards", woken by the scheduled task "Cratekit decisions relay" every hour at 34 minutes past) posts each answer on its card under `Answer from Phillip`, or sends it to the session that asked, sets the document `relayed`, and tells the coordinator. | S086, S087 | |
| M261 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L544-545 | `board.py cloud` reads `Answer from Phillip` as his reply and offers the card as `answered`. | S089, S104 | |
| M262 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L546-547 | The coordinator's own hourly wake fills free lanes only. | S067, S090 | |
| M263 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L547-549 | The page's "Pass on your answers" box lets Phillip paste answers into the project chat, and the coordinator has the relay thread pass them on at once. | S091, S092, S093 | |
| M264 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L549-550 | Any session, attended or not, asks Phillip this way rather than stopping. | C016, M253, S070 | |
| M265 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L552-553 | Opus 5.5 brainstorms, plans and builds, at high effort, or medium for a small card; Fable at high effort reviews. | S021, S022 | |
| M266 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L553-555 | The coordinator starts each build thread on Opus 5.5 at the effort its card's size calls for. | S023 | |
| M267 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L555-556 | The review is the `fable-reviewer` agent whatever the session runs. | S026, S143 | |
| M268 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L556-557 | A session on another model hands the plan and the build to the `opus-builder` agent. | S025, S136 | |
| M269 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L557-559 | The plan is posted on the card rather than proposed in plan mode, because plan mode waits for an approval nobody is there to give. | S049, S130, S135 | |
| M270 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L559 | The merge bar and the two round cap are unchanged in the cloud. | M054 | |
| M271 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L559-562 | When Fable is out of usage, Opus 5.5 at high effort reviews in its place, decided by Phillip on 2026-11-08, with the same reviewer definition and merge bar. | S028, S029 | |
| M272 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L562 | The substitution is named in the record and the pull request. | S030 | |
| M273 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L562-565 | No follow up Fable pass is owed, decided by Phillip on 2026-11-12, unless the session judges the Opus review missed something, and then it files a residual naming what to look at. | S031 | |
| M274 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L565 | Only a usage limit refusal allows the substitution. | S032 | |
| M275 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L567 | The battery on Linux is read against the base's own failures. | C042, S018, S181 | |
| M276 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L567-570 | About 170 tests fail on the container for machine-bound reasons (root reads every directory, no `hdiutil`, timing calibration pinned to one Mac, darwin paths). | S017 | |
| M277 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L570-571 | `scripts/cloud_battery.py baseline` measures them on the base commit before the first edit, and `compare` reads the branch against them. | S121, S128 | |
| M278 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L572-573 | `scripts/mutate.py` with `known-failures` subtracts them from every mutation run, so the driver's baseline is green net of them and its table says so. | S018, S165 | |
| M279 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L573-576 | Battery and driver read the full history first, since the clone is shallow (U200): the battery unshallows or refuses, and the driver refuses a shallow clone. | S123, S166 | |
| M280 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L576-581 | Both compare every failing id whole off pytest's own reports, and both refuse a baseline whose header does not end `ids whole`, which is measured again (U268). | M147, S124, S166 | |
| M281 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L581-583 | Each battery run reaching its reading leaves a record the mutation driver may read in place of its own full baseline for the same commit (U271). | M103, M104, S162 | |
| M282 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L584-589 | Both name where the run kept temporary files, `disk` or `memory` (U273): `baseline` runs on disk unless `temp memory` asks otherwise, the header records the place, `compare` runs in the baseline's place and refuses a `temp` naming the other, and the driver keeps every child in the place its known failures name. | M285, S125, S166 | |
| M283 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L589-591 | In memory, tests on the battery's `ON_DISK` list (the inode bound test alone today) run a second time on disk and their disk outcome stands. |  | |
| M284 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L591-594 | Disk stays the default while Phillip decides (#702); `temp memory` is not for a merge battery until #702 is answered. | S126 | |
| M285 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L594-595 | A baseline naming no place is measured again. | M282, S125, S166 | |
| M286 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L595-596 | Nothing is skipped or marked. | M183, S020 | |
| M287 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L596 | A newly failing test is the branch's. | S185 | |
| M288 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L596-598 | A test that fails only under a parallel run on ext4 is rerun alone before it is called either. | S167, S185 | |
| M289 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L598-599 | The macOS battery is owed on a Mac and named in each record's OWED paragraph; it runs whenever Phillip next builds or sits locally. | S189 | |
| M290 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L601-603 | GitHub GraphQL is refused on the container: `gh issue`, `gh repo`, `gh project` and `gh api` with `paginate` fail; `board.py` reads issues over REST a numbered page at a time. | S011 | |
| M291 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L604-605 | `start`, `sync` and a plain `audit` stay local; `audit` with `labels-only` runs in the cloud. | S016 | |
| M292 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L605-606 | The project's cards move only with a `BOARD_TOKEN` secret on the board workflow, since no cloud session can write the project. |  | |
| M293 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L606-609 | Deleting a remote branch is refused, so "Automatically delete head branches" stays on and a merged pull request takes its branch. | C082, C088, M194, M311, S013 | |
| M294 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L609-610 | The repo scan reads the container's mounts as the harness's under `CLAUDE_CODE_REMOTE`. |  | |
| M295 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L612 | A local session merges between cloud units, never during one. | M296 | |
| M296 | docs/METHOD.md, The cloud lane, decided 2026-10-27, L612-615 | When `board.py cloud` says the lane is held, a local merge to `main` waits until the card lands. | M295 | |
| M297 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L617 | Sharing the board was decided by Phillip on 2026-11-04. | C090 | |
| M298 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L619-620 | A builder that is not Claude works the repository on `grok/` branches. | C091, M299, S098, S099 | |
| M299 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L620-622 | A card with a `grok/` branch, or held by that builder's comment, is never a cloud thread's to take, and a `grok/` branch is never touched, merged in or pruned by a cloud thread. | C091, M298, S098, S099 | |
| M300 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L624-626 | The project on Phillip's first account builds nothing: it files cards from his ideas, keeps the decisions page, and relays his answers. | C010, C092, M234 | |
| M301 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L626-629 | The project on his second account does all of the building, up to ten threads at once, taking every card `board.py cloud` lists as takeable, in order. | M247, S065, S096, S098 | |
| M302 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L629-630 | A held card belongs to a building thread or to the `grok/` builder, and is never taken. |  | |
| M303 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L630-631 | The building project cannot reach the decisions page and never writes to it. | M256, S071, S077, S116 | |
| M304 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L631-634 | A thread's question goes on its card only, in the skill's Asking Phillip form, under `Brainstorm` or `Question for Phillip`. | C017, M254, S071 | |
| M305 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L633-635 | A bare `Question` heading is unknown to `board.py cloud`, so it reads as a hold. | S058, S072 | |
| M306 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L635 | The thread carries on with the conservative call. | C019, M012, M013, M259, S008, S075 | |
| M307 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L635-638 | The first project copies the question onto the page and posts Phillip's answer on the card under `Answer from Phillip`, which makes the card takeable again. | C018, M257, S076 | |
| M308 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L638-640 | An idea or bug Phillip raises in the building project's chat is filed there with the `file-card` skill, after a search of the open cards so nothing is filed twice. |  | |
| M309 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L640-641 | A new card's `U` or `A` number is read from the board just before it is filed, never earlier, because parallel threads file cards. | M343, S224 | |
| M310 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L645 | No stale branches: Phillip does not want branches left to go stale. | C089, M312, S014 | |
| M311 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L645-647 | "Automatically delete head branches" stays on, so a merged pull request takes its branch. | C082, C088, M194, M293, S013 | |
| M312 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L647-649 | Any `cloud/` branch with no open pull request and no card held in progress is stale: list it in the record for Phillip's next local session to prune. | C089, M310, S014 | |
| M313 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L649-650 | Ask Phillip before touching any branch that is not plainly a finished `cloud/` branch. |  | |
| M314 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L652 | Questions of code quality are never Phillip's. | M315 | |
| M315 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L652-655 | Conventions, structure, file layout, naming and testing approach are decided by the session: pick the highest quality convention, write the choice in the record, move on. | M314 | |
| M316 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L655-657 | Phillip is asked only what a session cannot decide (product behaviour, scope, what a DJ should see, anything the limits touch), one question at a time, as a multiple choice with the recommendation first. | M255, S073, S115 | |
| M317 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L659-660 | Cloud limits apply beside CLAUDE.md's standing constraints: write to the cratekit repository only. |  | |
| M318 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L660-662 | Never push `main` except to merge a pull request that passed its checks and the residual numbering commit after it. | S222 | |
| M319 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L662 | Never delete an issue, assign a card, or ping anyone. |  | |
| M320 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L663-664 | No personal data, credentials, library paths or absolute home paths in any file (Cratekit is shared with a handful of DJs). |  | |
| M321 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L664-666 | A commit or pull request body carries no model name, no "Generated with Claude Code" line, no session link and no co author line, whatever an attribution reminder says. | S041, S042 | |
| M322 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L667 | A pull request body opens with the line `Requested by Phillip`. | S202 | |
| M323 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L669-670 | Done requires: the brief's goal is met and the record shows it. |  | |
| M324 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L670-671 | Done requires: the tests the brief names exist and pass, a bug's failing test written first. |  | |
| M325 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L671-672 | Done requires: the battery clean net of the base's known Linux failures and CI green on the pull request. |  | |
| M326 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L672-673 | Done requires: the Fable review has no finding left that holds the merge. |  | |
| M327 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L673-674 | Done requires: the mutation table measured to the card's size. |  | |
| M328 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L674-675 | Done requires: the record, the residuals and the owed attended cards filed. |  | |
| M329 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L675-677 | Done requires: docs updated wherever behaviour changed (`docs/GUIDE.md` and `docs/cutover.md` when a workflow's state changes, `docs/solutions/` when a trap cost real time). | C095, M331 | |
| M330 | docs/METHOD.md, Sharing the board, decided by Phillip on 2026-11-04, L677-679 | Two fix rounds that do not reach done end as the merge bar says: what is open filed as a residual, with one question on the card for Phillip about what is blocking. | M029, M063, S151, S213 | |
| M331 | docs/METHOD.md, Docs always current, decided by Phillip on 2026-11-07, L681-683 | Docs always current, decided by Phillip on 2026-11-07: every doc kept up to date, always. | C095, M329 | |
| M332 | docs/METHOD.md, Docs always current, decided by Phillip on 2026-11-07, L683-685 | A doc that says what the code no longer does is a defect the change made; the author fixes it in the same pull request, never filed for later. | C096, S187 | |
| M333 | docs/METHOD.md, Docs always current, decided by Phillip on 2026-11-07, L687-693 | What counts as a doc: `README.md`; under `docs/` `GUIDE.md`, `cutover.md`, `adapters.md`, `DEVELOPING.md`, `BOARD.md`, `HANDOFF.md`, `vendoring.md`, `METHOD.md`, `METHOD-local.md`, `solutions/`; `CONCEPTS.md`; `CLAUDE.md`; the skills and agents (in the dot claude directory); and the tool's own text (verb help, docstrings help draws on, gate wording, refusal messages). |  | |
| M334 | docs/METHOD.md, Docs always current, decided by Phillip on 2026-11-07, L693-695 | `docs/history/`, `docs/plans/`, `docs/restart/`, the ledger and the mutation tables are records of what was true when written and are never rewritten to match. |  | |
| M335 | docs/METHOD.md, Docs always current, decided by Phillip on 2026-11-07, L698-700 | Before the record, grep the docs for the verb, config key, message and behaviour the change touched, and correct every line it made untrue, an example, a count or a default included. | S187 | |
| M336 | docs/METHOD.md, Docs always current, decided by Phillip on 2026-11-07, L700-702 | A new verb, key, flag or behaviour a person can see goes into `GUIDE.md` and, where it changes setup, `README.md`. |  | |
| M337 | docs/METHOD.md, Docs always current, decided by Phillip on 2026-11-07, L703-705 | A doc found stale for another reason is corrected in the same branch when the branch already edits that doc, otherwise left for the next docs sweep card, named in the record. |  | |
| M338 | docs/METHOD.md, Docs always current, decided by Phillip on 2026-11-07, L706-708 | The record carries a `Docs` line naming each doc corrected, or `none, because` and the reason. | C097, S188 | |
| M339 | docs/METHOD.md, Docs always current, decided by Phillip on 2026-11-07, L709-710 | Fable's review reports a doc the branch made untrue, quoting the line and what the code now does. | M340 | |
| M340 | docs/METHOD.md, Docs always current, decided by Phillip on 2026-11-07, L710-712 | Such a doc is fixed in the fix round, not filed as a residual; the merge bar's floor still decides what holds a merge of code, and this rule is part of a card being done. | M339 | |
| M341 | docs/METHOD.md, Local and attended work, releases, L716-717 | `docs/METHOD-local.md` holds the local board commands (`next`, `start`, `sync`, `audit`), the queue's order, the retired Relay, releases and attended cards. | C003, M003 | |
| M342 | docs/METHOD.md, Local and attended work, releases, L718-720 | A release is cut only when Phillip asks, and the cut runs on his Mac, since a cloud session's proxy refuses tag pushes. |  | |
| M343 | docs/METHOD.md, Local and attended work, releases, L720-722 | Work only his Mac can do is an attended card, titled `A<N>:` and labelled `attended`, one per live check a landing owes, its number read from the board just before it is filed. | M309, S224, S225 | |
| M344 | docs/METHOD.md, Do not touch, L726 | Do not touch: U30's board state, U20, R-9, A1, A2. |  | |
| M345 | docs/METHOD.md, Do not touch, L728-729 | The conformance branch is UNPARKED as of 2026-09-07; it is a unit on the board and lands like any unit. | M346 | |
| M346 | docs/METHOD.md, Do not touch, L729-730 | Until it lands, its `write/metadata.py` soft delete defect is live on main, and the branch is 377 commits behind. | M345 | |
| M347 | docs/METHOD.md, Do not touch, L732 | U29 stays attended, for a reason that will not expire. | C025, M350 | |
| M348 | docs/METHOD.md, Do not touch, L732-734 | U29's brief says "attended per workflow, do not batch cutovers" and requires each replacement to run correctly on the live library at least once. |  | |
| M349 | docs/METHOD.md, Do not touch, L734-736 | The live rekordbox database is off limits by standing constraint, so a session can prepare for U29 and cannot perform it. | C047, S034 | |
| M350 | docs/METHOD.md, Do not touch, L736-737 | `board.py next` will say "Take #29"; ready is a statement about dependencies, not about who can do the work. | C025, M347 | |
| M351 | docs/METHOD.md, Do not touch, L738-739 | The parity table U29's test scenario asks for already ships in `tests/test_cutover_parity.py`. |  | |
| S001 | cloud-unit SKILL.md, frontmatter, L3 | The skill is used when a cloud session is asked to take the next card, build a card, or run the cloud lane. |  | |
| S002 | cloud-unit SKILL.md, Cloud unit (intro), L8 | The cloud is where Cratekit is built, decided by Phillip on 2026-10-27. | C009, M231, M232 | |
| S003 | cloud-unit SKILL.md, Cloud unit (intro), L8-13 | A cloud session takes one card and runs METHOD's whole pipeline on it: brainstorm if an idea, plan, build with Opus 5.5 at the effort its size calls for, review with Fable at high effort, drive findings to the merge bar, mutation table sized to the card, record, a pull request merged to `main` with the closing trailer once CI on its head is green. | C012, C013, M011, M236 | |
| S004 | cloud-unit SKILL.md, Cloud unit (intro), L13-14 | A card that cannot be built without the machine is set aside with the steps to build it locally, and only those are built locally. | C015, M239, M240, S054, S109, S111 | |
| S005 | cloud-unit SKILL.md, Cloud unit (intro), L16 | Read `CLAUDE.md` and `docs/METHOD.md` before anything in the skill. | M016 | |
| S006 | cloud-unit SKILL.md, Cloud unit (intro), L16-17 | The skill says what a cloud container changes; METHOD says what a unit is. | C002, M002 | |
| S007 | cloud-unit SKILL.md, Where you are, L21-22 | The container has a fresh clone, no rekordbox, no library volume, no live account, and nobody watching. |  | |
| S008 | cloud-unit SKILL.md, Where you are, L22-23 | A question is a stop: make the conservative call, record it as a residual file, and keep going. | C019, M012, M013, M259, M306, S075 | |
| S009 | cloud-unit SKILL.md, Where you are, L25-26 | The session hook built `.venv` with the dev extras; run every tool through `.venv/bin/`. |  | |
| S010 | cloud-unit SKILL.md, Where you are, L26-27 | If the hook could not, build it yourself: `uv venv` with python 3.12 `.venv` and `uv pip install` with python `.venv/bin/python -e '.[dev]'`. | M177 | |
| S011 | cloud-unit SKILL.md, Where you are, L28-29 | GitHub GraphQL is refused here: `gh issue`, `gh repo`, `gh project` and `gh api` with `paginate` all fail. | M290 | |
| S012 | cloud-unit SKILL.md, Where you are, L29-31 | `gh api` on `repos/<owner>/<repo>/...` works for reads, comments, issue creation and body edits, and the GitHub MCP tools work for issues and comments. |  | |
| S013 | cloud-unit SKILL.md, Where you are, L31-33 | Deleting a remote branch is refused, so "Automatically delete head branches" removes a merged pull request's branch. | C082, C088, M194, M293, M311 | |
| S014 | cloud-unit SKILL.md, Where you are, L33-34 | A branch that survives its merge is listed in the record for Phillip's next local session. | C089, M310, M312 | |
| S015 | cloud-unit SKILL.md, Where you are, L35-38 | `scripts/board.py cloud` is the queue, `board.py show N` the brief, `board.py closing` with `since origin/main` the closing check, `board.py residuals` with `land` the numbering, `board.py audit` with `labels-only` the audit. | M014, S095 | |
| S016 | cloud-unit SKILL.md, Where you are, L38 | `start`, `sync` and a plain `audit` need GraphQL and stay local. | M291 | |
| S017 | cloud-unit SKILL.md, Where you are, L39-41 | The Linux suite carries about 170 failures bound to this machine (root reads every directory, no `hdiutil`, timing calibration pinned to one Mac, darwin paths). | M276 | |
| S018 | cloud-unit SKILL.md, Where you are, L41-43 | `scripts/cloud_battery.py` measures them on the base and reads the branch against them; `scripts/mutate.py` with `known-failures` subtracts them from every mutation run. | C042, M275, M278, S165, S181 | |
| S019 | cloud-unit SKILL.md, Where you are, L43 | Never edit the calibration file. |  | |
| S020 | cloud-unit SKILL.md, Where you are, L43-44 | Never skip, deselect or mark a test. | M183, M286 | |
| S021 | cloud-unit SKILL.md, Models, L48-49 | Brainstorm, plan and build are Opus 5.5's, at high effort, or medium for a small card (METHOD's card sizes). | M047, M265, S022 | |
| S022 | cloud-unit SKILL.md, Models, L49 | Review is Fable's at high effort. | M265, S021 | |
| S023 | cloud-unit SKILL.md, Models, L49-51 | The coordinator starts its build threads on Opus 5.5 at the effort the card's size calls for, so a build thread plans and builds itself. | M266 | |
| S024 | cloud-unit SKILL.md, Models, L51-53 | A thread that finds its card a different size from the one it was started for says so in the plan and carries on. | S233 | |
| S025 | cloud-unit SKILL.md, Models, L53-54 | A session on any other model hands the plan and the build to the `opus-builder` agent and does the rest itself. | M268, S136 | |
| S026 | cloud-unit SKILL.md, Models, L54-55 | The review is always the `fable-reviewer` agent, whatever the session's own model. | M267, S143 | |
| S027 | cloud-unit SKILL.md, Models, L55-58 | If a project thread's harness cannot load the repository's agents by name, run a general purpose agent on the `fable` model at high effort, told to read the reviewer definition's body first and follow it. |  | |
| S028 | cloud-unit SKILL.md, Models, L60 | When Fable is out of usage: decided by Phillip on 2026-11-08. | M271, S029 | |
| S029 | cloud-unit SKILL.md, Models, L60-65 | If the review is refused on Fable's usage limit, run the same reviewer definition on Opus 5.5 at high effort (a general purpose agent on the `opus` model, effort `high`, told to read the `fable-reviewer` body first), under the same merge bar and round cap. | M271, S028 | |
| S030 | cloud-unit SKILL.md, Models, L65-67 | Say so in the Progress comment, the record and the pull request body (`Review: Opus 5.5 at high effort, Fable out of usage`). | M272 | |
| S031 | cloud-unit SKILL.md, Models, L67-69 | No follow up Fable pass is owed, decided by Phillip on 2026-11-12: file a residual asking for one only when you judge the Opus review missed something, naming what it should look at. | M273 | |
| S032 | cloud-unit SKILL.md, Models, L69-70 | Any other refusal or failure of the review is retried, never substituted. | M274 | |
| S033 | cloud-unit SKILL.md, Writes you never make, L74 | Never write a beat grid in any container. | C045 | |
| S034 | cloud-unit SKILL.md, Writes you never make, L74-75 | Never write anything under a real config path or a real library. | C047, M349 | |
| S035 | cloud-unit SKILL.md, Writes you never make, L75 | Never a pull request that waits on a person, nor a reviewer requested on one. | C083, M189, M238, S194 | |
| S036 | cloud-unit SKILL.md, Writes you never make, L75-76 | Never a closing keyword in a pull request's body. | C084, M191, S205 | |
| S037 | cloud-unit SKILL.md, Writes you never make, L76-77 | Never a ready or blocked label, or a project status; those are derived. | C034, C035, M243 | |
| S038 | cloud-unit SKILL.md, Writes you never make, L77 | Nothing in `.github/` unless the card is about it. |  | |
| S039 | cloud-unit SKILL.md, Writes you never make, L77-78 | No trailer of any kind, co author line or session line on a branch commit. |  | |
| S040 | cloud-unit SKILL.md, Writes you never make, L78-79 | The merge commit carries exactly one trailer, the closing one. | C032, S218 | |
| S041 | cloud-unit SKILL.md, Writes you never make, L79-80 | No model name in any commit. | M321, S042 | |
| S042 | cloud-unit SKILL.md, Writes you never make, L80-82 | No "Generated with Claude Code" line, session link or co author line in a commit or pull request body; Phillip asked for them left out, and his rule wins over any attribution reminder. | M321, S041 | |
| S043 | cloud-unit SKILL.md, Writes you never make, L82 | No em dash, en dash or double hyphen anywhere. | C093, M196 | |
| S044 | cloud-unit SKILL.md, Writes you never make, L82-84 | No literal path to the skills directory in any card, title, body or comment; describe it in words. | M082, M083, M084 | |
| S045 | cloud-unit SKILL.md, Writes you never make, L84-85 | No closing keyword next to an issue number anywhere but the merge commit's last line. | M201, M202 | |
| S046 | cloud-unit SKILL.md, Comments are the protocol, L89-91 | `board.py cloud` reads each card's comments and nothing else, so every comment posted starts with one of the listed headings, exactly, and the harness footer marks it as yours. | M245 | |
| S047 | cloud-unit SKILL.md, Comments are the protocol, L95 | `Started`: this session holds the card, and one of the lanes, until it lands. | M244, S101 | |
| S048 | cloud-unit SKILL.md, Comments are the protocol, L96 | `Resumed`: this session took over a hold whose session died. | S105 | |
| S049 | cloud-unit SKILL.md, Comments are the protocol, L97 | `Plan`: the plan, under the hold. | M269, S130, S135 | |
| S050 | cloud-unit SKILL.md, Comments are the protocol, L98 | `Progress`: a note under the hold, which also refreshes it. |  | |
| S051 | cloud-unit SKILL.md, Comments are the protocol, L99 | `Brainstorm`: the card is an idea; the questions wait on Phillip. | M258 | |
| S052 | cloud-unit SKILL.md, Comments are the protocol, L100 | `Question for Phillip`: one decision the brief leaves open that cannot be made conservatively. |  | |
| S053 | cloud-unit SKILL.md, Comments are the protocol, L101 | `Answer from Phillip`: his answer from the decisions page, posted by the relay thread, read as his reply. | M246, S060 | |
| S054 | cloud-unit SKILL.md, Comments are the protocol, L102 | `Needs the machine`: set aside, with the steps to build it locally. | C015, M239, M240, S004, S109, S111 | |
| S055 | cloud-unit SKILL.md, Comments are the protocol, L103 | `Withdrawn`: this session lost a race for the lane and released the card. | M251, S102 | |
| S056 | cloud-unit SKILL.md, Comments are the protocol, L104 | `Landed`: merged and pushed on `main`. |  | |
| S057 | cloud-unit SKILL.md, Comments are the protocol, L106-107 | The reader forgives markdown, emphasis and punctuation around a heading (U203). |  | |
| S058 | cloud-unit SKILL.md, Comments are the protocol, L107-109 | Never a different word: a bare `Question`, or `Brainstorm notes`, is unknown, and a card under one is read as held, then as a session that died. | M305, S072 | |
| S059 | cloud-unit SKILL.md, Comments are the protocol, L111 | Post with `gh api -X POST repos/<owner>/<repo>/issues/N/comments -F body=@file.md`. |  | |
| S060 | cloud-unit SKILL.md, Comments are the protocol, L112-113 | Phillip's comments, and the relay thread's `Answer from Phillip`, are read only as answers to a `Brainstorm` or a `Question for Phillip`. | M246, S053 | |
| S061 | cloud-unit SKILL.md, Comments are the protocol, L113-114 | To stop the cloud building a card Phillip labels it `attended` or closes it, and a session that finds either on its card stops. | M241 | |
| S062 | cloud-unit SKILL.md, Comments are the protocol, L115-116 | A hold with no comment for eight hours is read as a dead session and offered to the next one as `resume`. | M252, S104 | |
| S063 | cloud-unit SKILL.md, Comments are the protocol, L116-117 | Post a `Progress` note at each phase: built, each review round, mutation measured. | S142, S152, S170 | |
| S064 | cloud-unit SKILL.md, Telling the coordinator, L121-122 | The lanes are filled by the coordinator, the Claude in Phillip's building project that started this thread. | C011, M233 | |
| S065 | cloud-unit SKILL.md, Telling the coordinator, L123 | The coordinator runs at most ten threads at once and counts them itself. | M247, M249, M301, S096 | |
| S066 | cloud-unit SKILL.md, Telling the coordinator, L123-124 | It wakes hourly to fill any free lane, and whenever a thread reports. | M233 | |
| S067 | cloud-unit SKILL.md, Telling the coordinator, L124-125 | The coordinator never reads the decisions page; that is the relay thread's job. | M262, S090 | |
| S068 | cloud-unit SKILL.md, Telling the coordinator, L125-128 | Tell the coordinator, with the project's messaging tool, right after the last comment this session posts (`Landed`, `Brainstorm`, `Needs the machine` or `Withdrawn`), so the freed lane fills. | S229 | |
| S069 | cloud-unit SKILL.md, Telling the coordinator, L128-129 | A session outside a project has no coordinator and skips this. |  | |
| S070 | cloud-unit SKILL.md, Asking Phillip, L133-135 | Every question for Phillip, a brainstorm's or a `Question for Phillip`, reaches the decisions page, https://claude.ai/artifact/FUqChoK5qKhztLdzzEADaS. | C016, M253, M264 | |
| S071 | cloud-unit SKILL.md, Asking Phillip, L137-138 | A build thread posts it on its card only and never writes the page, decided by Phillip on 2026-11-04. | C017, M254, M256, M303, M304, S077, S116 | |
| S072 | cloud-unit SKILL.md, Asking Phillip, L138-140 | The comment is headed `Brainstorm` or `Question for Phillip`, exactly, never a bare `Question`, which `board.py cloud` reads as a hold. | M305, S058 | |
| S073 | cloud-unit SKILL.md, Asking Phillip, L140-141 | Give each question two to four multiple choice options with the recommendation first. | M255, M316, S081, S115 | |
| S074 | cloud-unit SKILL.md, Asking Phillip, L141-143 | Give enough context, two or three sentences and the cost of each way, that it can be answered without the rest of the card. | S082 | |
| S075 | cloud-unit SKILL.md, Asking Phillip, L143-144 | A question never stops the build: make the conservative call, record it, and keep going. | C019, M012, M013, M259, M306, S008 | |
| S076 | cloud-unit SKILL.md, Asking Phillip, L144-146 | Phillip's other project, which files the cards, copies the question onto the page and posts his answer back. | C018, M257, M307 | |
| S077 | cloud-unit SKILL.md, Asking Phillip, L148-149 | The page's form is for the filing project, which writes it; a build thread never does. | M256, M303, S071, S116 | |
| S078 | cloud-unit SKILL.md, Asking Phillip, L149-152 | One document per question into the page's `decisions` collection with the `ArtifactData` tool (loaded with ToolSearch `select:ArtifactData`), action `set`, `url` the page, `collection` `decisions`, `doc_id` `<card>-<short slug>-<n>`. | S079 | |
| S079 | cloud-unit SKILL.md, Asking Phillip, L154-160 | The document body carries `card`, `card_title`, `group`, `order`, `kind` (brainstorm or question), `question`, `context`, `options` (label and one line detail), `recommended`, `status` `open`, `answer` null, `asked_by`, `asked_session`, `asked_at` (ISO 8601 UTC). | S078 | |
| S080 | cloud-unit SKILL.md, Asking Phillip, L162-163 | The recommendation is the option at index `recommended`; the page shows it first and marked. |  | |
| S081 | cloud-unit SKILL.md, Asking Phillip, L163-164 | Give two to four options; the page adds its own "something else". | S073 | |
| S082 | cloud-unit SKILL.md, Asking Phillip, L164-165 | Write the context so the question can be answered without opening the card. | S074 | |
| S083 | cloud-unit SKILL.md, Asking Phillip, L165-168 | The filing project then ends a comment on the card with a line linking the page and, where it has `PushNotification`, sends one short notification naming the card. |  | |
| S084 | cloud-unit SKILL.md, Asking Phillip, L168-169 | A document is marked answered by the page and relayed by the relay thread, never by the writer. |  | |
| S085 | cloud-unit SKILL.md, Asking Phillip, L171-172 | Phillip presses Answer on the page, which saves his choice and sets `status` to `answered`. |  | |
| S086 | cloud-unit SKILL.md, Asking Phillip, L173-175 | The scheduled task "Cratekit decisions relay" wakes the relay thread ("Wire decisions page answers to cards") every hour at 34 minutes past. | M260, S087 | |
| S087 | cloud-unit SKILL.md, Asking Phillip, L175-178 | The relay thread posts each answered document on its card under `Answer from Phillip`, or sends it to `asked_session` when it names no card, sets `status` to `relayed` with `relayed_at` and `relayed_note`, and tells the coordinator. | M260, S086 | |
| S088 | cloud-unit SKILL.md, Asking Phillip, L178-179 | The coordinator starts a thread on the card if none of its threads is still building it. |  | |
| S089 | cloud-unit SKILL.md, Asking Phillip, L179-180 | `board.py cloud` reads `Answer from Phillip` as his reply whoever posts it, and offers the card as `answered`. | M261, S104 | |
| S090 | cloud-unit SKILL.md, Asking Phillip, L180-181 | The coordinator's own hourly wake fills free lanes only and never reads the page. | M262, S067 | |
| S091 | cloud-unit SKILL.md, Asking Phillip, L183-185 | The page cannot reach a project session by itself (a page comment wakes only a session watching that page, and no project session can watch one). | M263, S092, S093 | |
| S092 | cloud-unit SKILL.md, Asking Phillip, L185-189 | While any answer is saved but not relayed, the page shows a "Pass on your answers" box with a ready prompt listing each (card, question, answer, note, decision id), a button that copies it and opens the project chat, and a copy-only button. | M263, S091, S093 | |
| S093 | cloud-unit SKILL.md, Asking Phillip, L189-191 | Phillip pastes it into the project chat, its Claude messages the relay thread, and the thread relays at once. | M263, S091, S092 | |
| S094 | cloud-unit SKILL.md, Asking Phillip, L192 | Without the paste an answer waits for the hourly check. |  | |
| S095 | cloud-unit SKILL.md, 1. Orient, L196-197 | Run `git fetch origin main` then `.venv/bin/python scripts/board.py cloud`. | M014, S015 | |
| S096 | cloud-unit SKILL.md, 1. Orient, L199-201 | `board.py cloud` lists every open unit and residual card by state, says how many lanes are held (ten by default, `CLOUD_LANES` in `scripts/board.py`), and names the next card. | M242, M247, M301, S065 | |
| S097 | cloud-unit SKILL.md, 1. Orient, L201-203 | If your prompt names a card, take that one, as long as the queue lists it as takeable (the coordinator chose it so parallel threads never pick the same card). |  | |
| S098 | cloud-unit SKILL.md, 1. Orient, L203-205 | Otherwise take the card the queue names, passing over any card held by the `grok/` builder. | C091, M298, M299, M301, S099 | |
| S099 | cloud-unit SKILL.md, 1. Orient, L205-209 | `board.py cloud` cannot see that builder's hold, so before posting `Started` look for a `grok/` branch naming the card's number (`git ls-remote` heads on origin `grok/*`) and a comment of that builder's on the card. | C091, M298, M299, S098 | |
| S100 | cloud-unit SKILL.md, 1. Orient, L209-210 | If every lane is held, or nothing is takeable, say so in one line, tell the coordinator, and stop. |  | |
| S101 | cloud-unit SKILL.md, 1. Orient, L212-214 | Post `Started` on the card at once, before reading anything else, then run `board.py cloud` again. | M244, S047 | |
| S102 | cloud-unit SKILL.md, 1. Orient, L214-217 | If it now says more cards are held than there are lanes, it names those that held first; if yours is not among them, post `Withdrawn` and stop. | M251, S055 | |
| S103 | cloud-unit SKILL.md, 1. Orient, L217 | A `Brainstorm` or `Needs the machine` posted later replaces the hold. |  | |
| S104 | cloud-unit SKILL.md, 1. Orient, L220-224 | State `answered`: if a `Progress` comment or pushed `cloud/N-...` commit is newer than the question and under eight hours old, the card is still that thread's, so pass over it; otherwise fold his answer into the brief and go to step 3. | M252, M261, S062, S089 | |
| S105 | cloud-unit SKILL.md, 1. Orient, L225-228 | State `resume`: post `Resumed` rather than `Started`, check out `origin/cloud/N-...` if it exists and read its log against the card's comments; otherwise start fresh from step 3. | S048 | |
| S106 | cloud-unit SKILL.md, 1. Orient, L229 | State `ready`: nobody has taken it; go to step 2. |  | |
| S107 | cloud-unit SKILL.md, 1. Orient, L231-233 | Read the brief with `board.py show N` and every comment on the card (the `gh api` comments command given). |  | |
| S108 | cloud-unit SKILL.md, 2. Classify the card, L237 | Decide from the brief which of three kinds the card is, and say which in the plan. | S133 | |
| S109 | cloud-unit SKILL.md, 2. Classify the card, L239-242 | It needs the machine when it cannot be built and proven without the live rekordbox database, the library volume, the live account, rekordbox itself, a backup of the real library, or Phillip at the desktop. | C015, M239, M240, S004, S054, S111 | |
| S110 | cloud-unit SKILL.md, 2. Classify the card, L242-244 | Needing live verification afterwards is not needing the machine: a unit whose code and tests run on fixtures and disposable copies is the cloud's, and its live proof is an OWED line in its record. |  | |
| S111 | cloud-unit SKILL.md, 2. Classify the card, L244-246 | Post `Needs the machine` with why, and the exact local steps as commands Phillip can paste (`board.py start N`, the verbs, the attended sitting). | C015, M239, M240, S004, S054, S109 | |
| S112 | cloud-unit SKILL.md, 2. Classify the card, L246-247 | Then run `board.py cloud` again and take the next card. | S117 | |
| S113 | cloud-unit SKILL.md, 2. Classify the card, L247-248 | A session sets aside as many cards as it must and builds at most one. |  | |
| S114 | cloud-unit SKILL.md, 2. Classify the card, L250-252 | It needs a brainstorm when the brief has no goal, no test scenarios or no verification, reads as an idea, or carries the `idea` label. |  | |
| S115 | cloud-unit SKILL.md, 2. Classify the card, L252-256 | Post `Brainstorm`: restate the idea in two or three sentences, name what already does part of the job, give two or three approaches each with cost and main risk, recommend one, and ask at most four questions, each multiple choice with your recommendation first, answerable in a word. | M255, M316, S073 | |
| S116 | cloud-unit SKILL.md, 2. Classify the card, L256-257 | The thread never writes the decisions page; the filing project copies the questions there. | M256, M303, S071, S077 | |
| S117 | cloud-unit SKILL.md, 2. Classify the card, L258 | Then take the next card. | S112 | |
| S118 | cloud-unit SKILL.md, 2. Classify the card, L258-261 | When the card comes back `answered`, rewrite the brief with his answers folded in (`gh api -X PATCH`), keeping the `**Depends on:**` line first and every field the brief form has. |  | |
| S119 | cloud-unit SKILL.md, 2. Classify the card, L263 | It is buildable: everything else; go on. |  | |
| S120 | cloud-unit SKILL.md, 3. Start, L267 | Create the branch: `git checkout -b cloud/N-<slug> origin/main`, the name `board.py cloud` printed. | C080, M186 | |
| S121 | cloud-unit SKILL.md, 3. Start, L268 | Run `cloud_battery.py baseline` as a background job, about twelve minutes. | M142, M167, M277, S128 | |
| S122 | cloud-unit SKILL.md, 3. Start, L270-271 | The baseline measures the machine's failures on the base and writes them to `.cloud-battery/baseline.txt`. |  | |
| S123 | cloud-unit SKILL.md, 3. Start, L271-274 | The clone is shallow, so the baseline first fetches `main`'s full history and refuses if it cannot (U200, from R-1191). | M279, S166 | |
| S124 | cloud-unit SKILL.md, 3. Start, L274-277 | Every failing id is read whole off pytest's own reports (U268), and `compare` refuses a baseline measured before that, giving the command that measures it again. | M147, M280, S166 | |
| S125 | cloud-unit SKILL.md, 3. Start, L277-280 | It runs on disk unless `temp memory` is given (U273) and names the place in its header; `compare` and the driver run in that place, and a baseline naming none is measured again. | M282, M285, S166 | |
| S126 | cloud-unit SKILL.md, 3. Start, L280-281 | Leave it on disk: until #702 is answered a memory baseline reads the inode bound test as the machine's. | M284 | |
| S127 | cloud-unit SKILL.md, 3. Start, L281-283 | Run it as a tracked background job with a two hour timeout from the start (a cloud thread's background job is stopped at 30 minutes otherwise). | S160, S206 | |
| S128 | cloud-unit SKILL.md, 3. Start, L283-284 | Run it before the first edit, so it measures the base, and edit nothing under `src` or `tests` until it reports. | M277, S121 | |
| S129 | cloud-unit SKILL.md, 3. Start, L286 | Post `Progress`: the branch, the base commit, the session URL if you know it. |  | |
| S130 | cloud-unit SKILL.md, 4. Plan, L290-291 | Plan per METHOD's step 2, as a message and never in plan mode (plan mode waits for an approval nobody gives). | M019, M021, M269, S049, S135 | |
| S131 | cloud-unit SKILL.md, 4. Plan, L291-292 | Grep `docs/solutions/` by module and tag for the area and read the matches. | C007, M018 | |
| S132 | cloud-unit SKILL.md, 4. Plan, L292-294 | The plan names the seam, the files, the test scenarios from the brief, the residuals the unit closes, and what is out of scope. | M020 | |
| S133 | cloud-unit SKILL.md, 4. Plan, L294-296 | The plan also names which of the three the card was and its size (small, medium or large), which sets its effort, review rounds and mutation table. | M044, S108 | |
| S134 | cloud-unit SKILL.md, 4. Plan, L296-298 | If the brief is insufficient on a point the plan needs, fix the issue body, then plan against the fixed brief. | C023, M023 | |
| S135 | cloud-unit SKILL.md, 4. Plan, L298 | Post it as `Plan`, then build it. | M269, S049, S130 | |
| S136 | cloud-unit SKILL.md, 4. Plan, L300-301 | On a session that is not Opus 5.5, hand steps 4 and 5 to the `opus-builder` agent with the card number and branch, and wait for its report. | M268, S025 | |
| S137 | cloud-unit SKILL.md, 5. Build, L305 | Guard first, then the code it governs (METHOD's step 3). | M024 | |
| S138 | cloud-unit SKILL.md, 5. Build, L305-307 | Commit in units of meaning with subjects naming the unit, `feat(u57): ...`, subject and body only. | M025 | |
| S139 | cloud-unit SKILL.md, 5. Build, L307-308 | Run the test files for what you touched as you go; the full suite is the gate, not the edit loop. | C043, M170, M171 | |
| S140 | cloud-unit SKILL.md, 5. Build, L308-309 | Register what a later unit owes in `tests/_pending.py`, never in a docstring. |  | |
| S141 | cloud-unit SKILL.md, 5. Build, L309-311 | Push the branch at each commit of meaning (`git push -u origin cloud/N-<slug>`), so a dead session leaves work the next one resumes. |  | |
| S142 | cloud-unit SKILL.md, 5. Build, L311 | Post `Progress` when it is built. | S063, S152, S170 | |
| S143 | cloud-unit SKILL.md, 6. Review with Fable, to the merge bar, L315-316 | Run the `fable-reviewer` agent on the branch, telling it the card's size. | M267, S026 | |
| S144 | cloud-unit SKILL.md, 6. Review with Fable, to the merge bar, L316 | Take its report as findings to drive, not to argue with. | M026 | |
| S145 | cloud-unit SKILL.md, 6. Review with Fable, to the merge bar, L317 | Apply what holds, commit the fixes as `fix(uN): ...`, and push. |  | |
| S146 | cloud-unit SKILL.md, 6. Review with Fable, to the merge bar, L317-318 | Note the head round one reviewed. |  | |
| S147 | cloud-unit SKILL.md, 6. Review with Fable, to the merge bar, L320 | Round two only when it can find something, decided by U196. | M064 | |
| S148 | cloud-unit SKILL.md, 6. Review with Fable, to the merge bar, L320-322 | If round one found nothing BLOCKING and no file under `src`, `tests` or `scripts` changed after it, there is no round two. | M065 | |
| S149 | cloud-unit SKILL.md, 6. Review with Fable, to the merge bar, L322-323 | A small card gets round two only when round one found something BLOCKING. | M049 | |
| S150 | cloud-unit SKILL.md, 6. Review with Fable, to the merge bar, L323-325 | Otherwise run the agent again with round one's head, and it reviews the fix commits (`git diff <round one head>..HEAD`) rather than the whole branch. | M066 | |
| S151 | cloud-unit SKILL.md, 6. Review with Fable, to the merge bar, L325-326 | At most two fix rounds; what is still open when they are spent becomes a residual file and the unit goes on. | M029, M063, M330, S213 | |
| S152 | cloud-unit SKILL.md, 6. Review with Fable, to the merge bar, L326-327 | Post `Progress` after each round, naming what it drove. | S063, S142, S170 | |
| S153 | cloud-unit SKILL.md, 6. Review with Fable, to the merge bar, L327 | Then the hunts a green suite cannot see, METHOD's list. | C044, M028 | |
| S154 | cloud-unit SKILL.md, 7. The mutation table, L331-332 | The mutation table is sized to blast radius, decided by Phillip on 2026-11-02. | M090 | |
| S155 | cloud-unit SKILL.md, 7. The mutation table, L332 | Up to 25 rows for a unit that writes or deletes. | M091 | |
| S156 | cloud-unit SKILL.md, 7. The mutation table, L332-333 | About 8 rows for a read only report or a static registry. | M092 | |
| S157 | cloud-unit SKILL.md, 7. The mutation table, L333-335 | None for a unit that changes only docs or skill text, whose record says so in one line and skips the rest of the step. | M093 | |
| S158 | cloud-unit SKILL.md, 7. The mutation table, L335-336 | Rows target the code the unit added, in `docs/mutation/uN-rows.toml` in the form of `docs/mutation/u99-b-rows.toml`. | M095 | |
| S159 | cloud-unit SKILL.md, 7. The mutation table, L337 | Commit the rows, then run step 8's `compare` on that head first. | M112, S182 | |
| S160 | cloud-unit SKILL.md, 7. The mutation table, L337-339 | Measure the rows as a tracked background job with a two hour timeout from the start, starting nothing else against the tree until it reports. | M143, S127, S206 | |
| S161 | cloud-unit SKILL.md, 7. The mutation table, L341-342 | Commands: `cloud_battery.py compare`, then `mutate.py docs/mutation/uN-rows.toml` with `known-failures .cloud-battery/baseline.txt`. |  | |
| S162 | cloud-unit SKILL.md, 7. The mutation table, L344-347 | The driver reads its full baseline from that `compare` run's record (U271) only for the same commit on a clean tree, this machine, checkout and interpreter, and the same known failures file; otherwise it measures its own and the table says why. | M103, M104, M105, M106, M281 | |
| S163 | cloud-unit SKILL.md, 7. The mutation table, L347-348 | Edit nothing and commit nothing between `compare` and the driver. |  | |
| S164 | cloud-unit SKILL.md, 7. The mutation table, L348-349 | The driver still measures every subset baseline and runs the null control. | M108, M109 | |
| S165 | cloud-unit SKILL.md, 7. The mutation table, L349-351 | The driver subtracts the machine's failures from every run, so its baseline is green net of them and its table says so. | M278, S018 | |
| S166 | cloud-unit SKILL.md, 7. The mutation table, L351-354 | The driver refuses a known failures file whose header does not end `history full ids whole` (a pre-U268 baseline, or one naming no temp place, U273) and refuses a shallow clone; pass it only a baseline `cloud_battery.py` measured. | M147, M279, M280, M282, M285, S123, S124, S125 | |
| S167 | cloud-unit SKILL.md, 7. The mutation table, L354-358 | If the driver refuses a red baseline, rerun the named test alone: failing alone it is yours, fix it; passing alone it is intermittent, run the driver again, and if the same test reddens the baseline a second time treat it as yours. | M288, S185 | |
| S168 | cloud-unit SKILL.md, 7. The mutation table, L358-359 | Never write an id into the baseline file by hand: it is measured, and a hand added id is a regression excused for every later run. |  | |
| S169 | cloud-unit SKILL.md, 7. The mutation table, L360 | A zero row is driven the way METHOD says. | M113, M114 | |
| S170 | cloud-unit SKILL.md, 7. The mutation table, L360-361 | Commit the table, `docs/mutation/uN.md` and `.json`, and post `Progress`. | M116, S063, S142, S152 | |
| S171 | cloud-unit SKILL.md, 7. The mutation table, L363-364 | A card that restructures code proves two more things, beside its own table and never in place of it (U297). | M117, M120 | |
| S172 | cloud-unit SKILL.md, 7. The mutation table, L364-366 | It replays the recorded kills of the files it owns before its first edit and after its last. | M121 | |
| S173 | cloud-unit SKILL.md, 7. The mutation table, L366-367 | Each replay runs as a table does, `compare` on the committed head then the driver, and `check` must exit 0. | M123, S176 | |
| S174 | cloud-unit SKILL.md, 7. The mutation table, L369-373 | Replay commands: `killset.py rows <paths>` with `out` a before rows file; `mutate.py` on it; `killset.py rows` with `after` the before json; `mutate.py` on that; `killset.py check` before json after json. | M118 | |
| S175 | cloud-unit SKILL.md, 7. The mutation table, L375-376 | `rows` names the batch for its row file without the closing `-rows`, so the driver writes the tables the next command reads. |  | |
| S176 | cloud-unit SKILL.md, 7. The mutation table, L376-378 | A row that `rows` with `after` lists as unplaced is anchored by hand (same `source`, new text, a `moved` reason) or mapped under `[[mapped]]` to the row that now covers it. | M123, S173 | |
| S177 | cloud-unit SKILL.md, 7. The mutation table, L379-380 | A replay cut at its timeout is run again with `resume`, on the same commit; it reuses nothing measured at another. | M125 | |
| S178 | cloud-unit SKILL.md, 7. The mutation table, L380-382 | It compares what the verbs print and write, base against branch, in a scratch directory, first adding a scenario under `tests/behaviour/` for any verb it touches that has none. | M126, M129 | |
| S179 | cloud-unit SKILL.md, 7. The mutation table, L384-386 | Behaviour commands: `behaviour_compare.py capture` with `out <scratch>/base` and `rev origin/main`; `capture` with `out <scratch>/branch`; `compare` base branch. | M127, M128 | |
| S180 | cloud-unit SKILL.md, 7. The mutation table, L388-389 | The record carries both results, and every difference `compare` printed is either removed or named there as a listed cleanup. |  | |
| S181 | cloud-unit SKILL.md, 8. The battery, L393 | Run `.venv/bin/python scripts/cloud_battery.py compare`. | C042, M275, S018 | |
| S182 | cloud-unit SKILL.md, 8. The battery, L395-396 | Run it on the head the rows were committed on, before the driver; a card with no table runs it after the review. | M112, S159 | |
| S183 | cloud-unit SKILL.md, 8. The battery, L396-400 | If anything under `src`, `tests` or `scripts` changed after that run, run it again on the final head before step 9: CI does not run the suite, so the last reading must cover every line that merges. | M179 | |
| S184 | cloud-unit SKILL.md, 8. The battery, L402 | Ruff and the scan must be clean. | C041, M165 | |
| S185 | cloud-unit SKILL.md, 8. The battery, L402-404 | Every test under `NEWLY FAILING, yours` is yours: rerun it alone first (one test is known intermittent on ext4 under a parallel run), and fix every one that fails alone. | M287, M288, S167 | |
| S186 | cloud-unit SKILL.md, 8. The battery, L404-405 | A test under `no longer failing` is worth a line in the record. |  | |
| S187 | cloud-unit SKILL.md, 9. Record, L409-411 | Docs first, by METHOD's Docs always current: grep every doc it lists for what the change touched and correct each untrue line in this branch, committed as `docs(uN): ...`. | C096, M332, M335 | |
| S188 | cloud-unit SKILL.md, 9. Record, L411 | The record carries the `Docs` line. | C097, M338 | |
| S189 | cloud-unit SKILL.md, 9. Record, L413-416 | `docs/restart/uN.md` in the form of any recent file there, with an OWED paragraph naming what this container could not run: the macOS battery, and the live verification at an attended sitting if the unit has one. | C005, M033, M214, M215, M289 | |
| S190 | cloud-unit SKILL.md, 9. Record, L416-417 | A residual is `docs/residuals/uN-<slug>.md` in the form `docs/residuals/README.md` gives, with no number. | C027, M030 | |
| S191 | cloud-unit SKILL.md, 9. Record, L417-418 | Never write into `docs/residual-findings.md`. |  | |
| S192 | cloud-unit SKILL.md, 9. Record, L418-419 | A `docs/solutions/` entry only if the unit found something a future session would get wrong without it. | M032, M222 | |
| S193 | cloud-unit SKILL.md, 9. Record, L419-420 | Commit the record as `record(uN): ...` and push the branch. |  | |
| S194 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L424-426 | The unit reaches `main` through a pull request this session opens and merges itself once CI is green, decided by U158; nobody reviews it and nothing waits on a person. | C079, C083, M037, M185, M189, M238, S035 | |
| S195 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L428-429 | Run `git fetch origin main`, and `git merge origin/main` only if main moved, then step 8 again in full. | M250, S211, S215 | |
| S196 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L430 | Run `board.py closing` with `since origin/main`. | C037, M198, S199, S200 | |
| S197 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L431 | Run the closing keyword scan over `origin/main..HEAD`. | M036, M199, M200, S199 | |
| S198 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L432 | Push the branch with `git push -u origin cloud/N-<slug>`. |  | |
| S199 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L434 | The closing check must exit 0, and the keyword scan must print nothing. | C037, M036, M198, M199, M200, S196, S197, S200 | |
| S200 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L434-437 | Check `tests/_pending.py` first: a register still owing this unit a module makes CI red whatever the trailer says, so discharge the entry or point it at the later unit that owes it before opening the pull request. | C037, M198, S196, S199 | |
| S201 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L439-443 | Open the pull request over REST (`gh pr` needs GraphQL; the GitHub MCP `create_pull_request` tool also works), titled `UN: <what landed>`, head `cloud/N-<slug>`, base `main`. |  | |
| S202 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L445-447 | The body is short, because the record holds the detail (U196): first line `Requested by Phillip`, then a line naming the card by its link (the issue URL, never a keyword and a number), then a link to `docs/restart/uN.md` on the branch. | M190, M322, S203, S204 | |
| S203 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L447-449 | Then five lines at most: the `cloud_battery.py compare` counts, the review rounds, the mutation table's result, the residual files, and what is OWED. | M190, S202, S204 | |
| S204 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L449 | Never restate the record in the pull request body. | M190, S202, S203 | |
| S205 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L449-451 | No closing keyword anywhere in the body (GitHub closes from a body on merge, bypassing `board.py closing`); the merge commit's trailer is the one close. | C084, M191, S036 | |
| S206 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L453-456 | Wait for CI on the head commit with one tracked background job, never a foreground sleep and never a hand-repeated poll, so the session wakes once (U196), with a two hour timeout (the script waits up to an hour; a background job is stopped at 30 minutes otherwise). | S127, S160, S207 | |
| S207 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L458-459 | Run `wait_ci.py $SHA`: exit 0 green, 1 red, 2 timed out, 3 unread. | S206 | |
| S208 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L461-463 | Exit 3 means the runs could not be read three times in a row: fix the read (the token, the repository), never the branch. |  | |
| S209 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L463-465 | Every check run on the head must be `completed`, and green means each conclusion is `success`, `neutral` or `skipped` (hand-read commands given). | M187, S210 | |
| S210 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L472-475 | The branch push runs CI on the same head, so wait until the actions runs query lists a completed `success` run for the pull request; that run judges the range and the card. | M187, S209 | |
| S211 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L475-478 | A pull request conflicting with `main` gets no `pull_request` run: when the head shows a push run only, merge `origin/main`, run step 8 again, push, and wait on the new head. | M250, S195, S215 | |
| S212 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L480-482 | CI judges the pull request's own range and the card its head branch names (`board.py closing` with `pull-request-head`), so a branch whose card a register still owes is red. | C085, M192 | |
| S213 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L482-483 | If CI is red, fix it on the branch and push again, inside the two fix rounds METHOD allows. | M029, M063, M330, S151 | |
| S214 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L483-484 | A failure that is the machine's and not the branch's is said in the body. |  | |
| S215 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L484-486 | If `main` moved while you waited, merge `origin/main` into the branch, run step 8 again in full, push, and wait on the new head. | M250, S195, S211 | |
| S216 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L488-490 | Merge through the API as a merge commit, title and trailer exactly as a local merge would carry them, with `sha` pinned to the head CI judged. | C081, M188, S217 | |
| S217 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L492-494 | Merge commands: message file ending `Closes #N`; `gh api -X PUT .../pulls/<pr>/merge` with `merge_method=merge`, `sha`, `commit_title='merge(uN): <what landed>'`, `commit_message`. | C081, M188, S216 | |
| S218 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L496 | The trailer is the message's last line and the only closing keyword in it. | C032, S040 | |
| S219 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L497-500 | If the merge endpoint is refused, merge locally with the same message (`git checkout -B main origin/main`, `git merge` no-ff) and push `main`; GitHub marks the pull request merged, and the refusal is a residual file if none records it. | M193 | |
| S220 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L502-507 | Then on `main`: fetch and reset to `origin/main`, `board.py residuals` with `land`, commit "docs(residuals): number what landed" only if it numbered any, `git push origin main`. | M038, M039 | |
| S221 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L509-511 | If that push is refused because `main` moved, fetch, merge `origin/main` into `main`, push again; the numbering commit carries no code, so the battery need not rerun. |  | |
| S222 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L511 | Never force push `main`. | M318 | |
| S223 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L512-515 | For each residual the `land` run named as meeting the board bar, file its issue over REST, titled `R-N: ` and the ledger heading exactly, body opening `**Depends on:** none` with goal, key files, approach, test scenarios and out of scope, label `residual`. | M042, M075, M076, M077 | |
| S224 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L519-523 | For each live check the OWED paragraph names (live library, account, rekordbox, macOS battery), file one attended card for Phillip's Mac titled `A<N>: <the check>`, N one past the highest `A` title on the board, read just before filing. | M309, M343, S225 | |
| S225 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L523-526 | The attended card is labelled `attended` and nothing else, its body opens `**Depends on:** #<the release card or this card>` and says what to run and when it is done; METHOD-local's attended work section is the form. | M343, S224 | |
| S226 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L528 | Then `board.py audit` with `labels-only`. | M041 | |
| S227 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L528-532 | Post `Landed` on the card, short, linking the record rather than restating it (U196): the pull request, merge commit, link to `docs/restart/uN.md` on `main`, residuals numbered and issues filed, attended cards filed, one line each for battery, review rounds and mutation table. |  | |
| S228 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L532-533 | The push of the trailer closes the card and the board workflow relabels what it released. | C033 | |
| S229 | cloud-unit SKILL.md, 10. Merge and land, through a pull request, L534 | Then tell the coordinator, so the lane fills at once, and stop. | S068 | |
| S230 | cloud-unit SKILL.md, Small card runs, L538-540 | A thread handed two or three small cards in the same module builds them one after another, decided by Phillip on 2026-11-02. | M052, S231 | |
| S231 | cloud-unit SKILL.md, Small card runs, L540-541 | Each card is its own unit from step 1: its own `Started`, plan, branch from the current `main`, review, record, pull request and `Landed`. | M052, S230 | |
| S232 | cloud-unit SKILL.md, Small card runs, L542-544 | The thread's reading and baseline carry over; measure the baseline again only if `main` moved in `src`, `tests`, `scripts` or `pyproject.toml` since it was measured. | M053 | |
| S233 | cloud-unit SKILL.md, Small card runs, L544-546 | If a card turns out not to be small, build it as its size calls for and hand the rest of the run back to the coordinator. | S024 | |

## Divergences noticed while reading

Places where two statements of the same rule disagree, so the shortened text has to pick one on purpose.

- Plan mode: M L35 says plan in plan mode; M L557-559 and S L290-291 say never plan mode in the cloud (the cloud is where everything is built per C L24).
- Reviewer: M L44-46 names the built in `/code-review`; C L28, M L555-556 and S L315 name the `fable-reviewer` agent.
- Pull request body: M L399-401 says the body is the landing's record (battery, rounds, table, residuals, OWED); S L445-449 says it is short, five lines at most, and never restates the record.
- Owed register: M L413-416 says merge without the trailer and close the issue later; S L434-437 says discharge the entry or point it at a later unit before opening the pull request (CI is red otherwise).
- Battery commands: C L75-77 omit `./` and `tb=no`; M L338-340 carry both.
- A question: C L38 and M L24-25 say "a question is a stop"; M L538-539 and S L143-144 say a question never stops the build. All agree on the conservative call.
- Relay: M L144-145 (Relay feeder) and M L147-150 (Relay skips cards) describe Relay as live, while M L15-16 and M L717 say it is retired.
- Residual issues: M L138 and L141 say `gh issue create` and add to project 2; in the cloud `gh issue` fails (M L601-603, S L28-29) and no cloud session can write the project (M L605-606); S L512-517 files over REST and does not add to the project.
- Small card review: M L74-76 says one round, a second only on BLOCKING; S L322-323 agrees; M L119-121 adds the no change condition for all sizes.


## Narrative candidates

Line ranges at origin/main that tell how a rule was arrived at, what a previous version did, or a past incident, rather than stating a rule. Each is a candidate to move to docs/history/; where a dated decision sits inside one, its row above keeps the decision and only the story moves.

### CLAUDE.md

- L6-7: "(U196)" reason for keeping the file short (one clause).
- L82-84: "every defect the adversarial reviews found here passed a green suite written by its author" (justification).
- L118-119: "relaxing the one day rule of 2026-09-29" (superseded rule).
- L127-129: Phillip's quote "don't ask for my approval on anything going forward".
- L132-136: "reversing the 2026-09-29 rule: the gate shows both backup ages and the person only pasted a command, so..." (why the reversal).
- L136-142: the U138 and U184 transition clauses ("until the installed copy carries U138 ... as before", "until the installed copy carries U184, use the gate as before"), transitional history once both are installed.
- L145-146: "The editable install names the checkout..." (reason, duplicated in METHOD L370-373).
- L148: "replacing the old no pull requests rule".
- L155-156: Phillip's quote "I authorize you to merge to main here in the cloud now and going forward".

### docs/METHOD.md

- L11-16: why the compound engineering plugin went (multi agent passes, the verifier at 258k tokens per round trip, "ceremony is not"), and Native Relay running the pipeline until 2026-10-27.
- L112-114: why the merge bar floor exists (a mutation table always finds a zero death row).
- L116-117: "The floor is meant to end the loop on merit. The cap is what guarantees an end date" (rationale).
- L124-125: U179's round two catching a fix round's own defect.
- L144-145: the Relay feeder sentence (Relay is retired per L15-16 and L717, so this is stale history, not a rule).
- L147-151: why no dot claude path (Relay skips such cards; the Phase G brief that would have sat unlaunched).
- L156-157: the measured verifier gap (17 vs 10, 49 vs 39, 83 vs 49).
- L180-181: "Three of this project's recorded incidents were hand rolled driver mistakes."
- L213-214: "A table that lives only in a chat message is a claim. One was lost that way."
- L246-247: why context is billed (tool calls times context size).
- L263-265: why `-q` hurts (pyproject sets it, `-qq` result), rationale.
- L270-283: the history of the driver rule (used to say foreground, a backgrounded driver outliving its parent twice, U65 2026-09-17 correction, the 600 second ceiling measured on the serial suite, timings since 2026-09-18 and U251, two partial mutations restored from `git show HEAD:`).
- L291-293: "the cloud battery read them this way until U268".
- L346-351: the suite timing measurements of 2026-11-12 and 2026-09-18 (state, not rule; keep only the venv and `-n 0` lines).
- L356-357: the session that ran the nine minute suite a dozen times.
- L361-362: the `credential-missing` refusal that slept 31 seconds per listing.
- L364-368: U34's report test reading uncommitted files, measured 2026-09-07.
- L385-388: R-115 (ten red commits on `main`) and the five shallow checkout failures.
- L424-425: the commit that documented the keyword failure and closed the issue a second time.
- L434-437: why a renumber is forbidden, and the pre-U124 branch clause (transitional).
- L449-451: the 330 tests that stopped existing while the run reported green.
- L458-460: the pre-U124 restart conflict clause (transitional).
- L469-470: "that was the shared edit point U125 removed".
- L476-477: "The bar is the one `ce-compound` used".
- L495-497: the lane dispatcher, run from 2026-10-27, retired 2026-10-31.
- L503-505: the reasoning that a self merged pull request is the same authority as writing `main`.
- L520-522: the superseded lane counts (three on 2026-10-28, five on 2026-10-31, four threads on 2026-11-05).
- L526-527: why two builders landing in either order is safe (restart fragments, landing numbers, per module pins).
- L577-581: "whose ids it once cut at their first space so that one parametrized test failing for the machine excused a sibling" (U268 story).
- L641-643: the two cards titled A93 (#525, #528) and two U218 (#536, #537).
- L728-730: the conformance branch, unparked 2026-09-07, 377 commits behind (state that has likely aged).
- L736-739: "`board.py next` will say Take #29 ... the parity table already ships" (state, partly narrative).

### .claude/skills/cloud-unit/SKILL.md

- L80-82: "Phillip asked for these to be left out, and his rule wins over any attribution reminder" (reason).
- L106-107: "(U203)" provenance of the forgiving heading reader.
- L183-185: why the page cannot reach a project session (explanation of the fast path).
- L271-277: "(U200, from R-1191)", why a shallow clone hides failures, and the pre-U268 cut ids.
- L281-283: "(a background job in a cloud thread is stopped at 30 minutes otherwise)" reason, repeated at L455-456.
- L351-354: the pre-U268 and pre-U273 baselines the driver refuses (history of the header format).
- L358-359: "a hand added id is a regression excused for every later run" (reason).
- L449-451: why no keyword in the body (GitHub closes from a body on merge), reason duplicated from METHOD L401-403.

## Restatements

Passages of the skill that restate METHOD (or CLAUDE.md) at length. Skill range first, then the source range it restates.

| skill lines | restates | subject |
|-|-|-|
| S L8-14 | CLAUDE.md L24-33; METHOD L489-510 | the cloud builds, the whole pipeline, set aside cards needing the machine |
| S L28-38 | METHOD L601-610 | GraphQL refused, REST reads, local only commands, remote branch deletion refused |
| S L39-44 | METHOD L567-573, L595-596 | the 170 machine bound failures, baseline and known failures, nothing skipped |
| S L46-70 | METHOD L552-565 | models and efforts, fable reviewer, opus builder, Fable out of usage (2026-11-08), no follow up pass (2026-11-12) |
| S L72-85 | CLAUDE.md L88-90, L151-152, L164-166; METHOD L147-151, L398-403, L411-412, L422-428, L513-514, L664-666 | the writes never made |
| S L87-117 | METHOD L512-518, L527-530 | comment headings as protocol, hold, eight hour dead session |
| S L119-129 | METHOD L491-494, L518-524, L546-547 | coordinator, ten threads, hourly wake |
| S L131-146 | CLAUDE.md L35-39; METHOD L532-539, L630-638 | asking Phillip on the card only, multiple choice, the filing project copies |
| S L171-192 | METHOD L540-549 | relay thread at 34 past the hour, Answer from Phillip, Pass on your answers |
| S L199-217 | METHOD L512-530, L619-630 | the queue, lanes, grok builder, withdraw |
| S L270-284 | METHOD L570-595 | baseline before first edit, full history (U200), ids whole (U268), temp place (U273), #702 |
| S L290-298 | METHOD L35-40, L557-559 | plan contents, plan on the card not in plan mode, fix the brief |
| S L305-311 | METHOD L41-43, L353-355 | guard first, commit units, test files while building |
| S L315-327 | METHOD L44-48, L73-80, L116-124 | review, round two rules (U196), two fix rounds |
| S L331-361 | METHOD L162-210, L567-583 | blast radius rows (25, about 8, none), read baseline (U271), subset and null control, zero rows |
| S L363-389 | METHOD L216-242 | replay (U297), killset, behaviour compare |
| S L393-405 | METHOD L353-356, L377-378, L595-598 | battery on the final head, CI runs no suite, ext4 rerun |
| S L409-420 | METHOD L49-58, L697-708 | docs first, Docs line, restart fragment, residual files, solutions entries |
| S L424-451 | CLAUDE.md L147-159; METHOD L393-428 | pull request per unit (U158), closing check, keyword scan, body without keyword |
| S L480-500 | METHOD L403-408 | CI judges range and card, merge commit and trailer, refused merge endpoint |
| S L502-526 | METHOD L59-65, L138-143, L429-441, L660-662, L716-722 | landing on main, numbering, residual issues, attended cards |
| S L536-546 | METHOD L82-86 | small card runs (2026-11-02), baseline reuse |

