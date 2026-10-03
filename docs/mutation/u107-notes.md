# U107 mutation notes

**Verdict: 25 of 25 killed, after three zeros were given a test.** Measured
2026-10-02 on `relay/251` by R-857's task, the review U107 never had because
its own task hit the model usage limit. The author of these rows is the
reviewer, not the unit's builder, and every zero below reads as "the author
of this table could not kill it" until a test did.

Run in four batches because the driver pays two full suite runs before its
first row and a single 25 row call would pass the tool ceiling. The machine
was loaded, load averages near 7 with the Relay runner live, and batch a took
15 minutes. The first attempt at batch a refused on a red baseline,
`tests/test_adopt_workers.py::test_a_second_drive_adds_no_second_membership_row`,
which passed alone three times in a row (17, 1.5 and 0.7 seconds) and in
every later baseline: starvation under load, not this branch.

| Batch | Rows | Killed | Zero |
|---|---|---|---|
| `u107-a` | S01 to S09 | 8 | S02 |
| `u107-b` | S10 to S18 | 8 | S14 |
| `u107-c` | S19 to S25 | 6 | S25 |
| `u107-d` | S02, S14, S25 again | 3 | none |

The three zeros, all on user facing guards, and the test that now kills each:

- **S02**, the record's version check. No test wrote another version, so a
  record of version 2 would have been read as this build's.
  `test_a_record_of_another_version_refuses_rather_than_being_read_as_this_builds`.
- **S14**, `_take` leaving an item a person decided between the question and
  the answer. Nothing decided an item mid question.
  `test_an_item_decided_between_the_question_and_the_answer_is_left_as_decided`.
- **S25**, `_measured` passing a provider refusal through. The refusal tests
  refused the listing, never the track read, so a cooldown while counting a
  catch up release would have been shown as tracks unread and the walk would
  have gone on. `test_a_provider_refusal_while_counting_a_catch_up_release_parks_the_run`.

**Two rows measured text the second fix round then changed.** S09 mutated the
supersede comprehension's condition and S05 the sweep worker's `offered=`
argument; both lines were rewritten after the table ran, the first to
supersede by the id a release files under, the second to read the record
before the login. Each new line has a test that fails without it
(`test_a_release_the_sweep_filed_while_its_question_waited_is_settled_by_the_answer`,
`test_the_labels_sweep_refuses_an_unreadable_record_before_any_login`), and
neither was measured as a row, since the table is one pass per unit.

Five rows were considered and dropped below the cap; `u107-c-rows.toml`
lists them with the reason for each.
