---
title: "Read project cards off the issues, not the project, and write a field only when it changed"
date: 2026-10-21
category: workflow-issues
module: "scripts/board.py"
problem_type: workflow_issue
component: tooling
severity: medium
root_cause: expensive_listing
resolution_type: code_fix
applies_when:
  - "a board script runs out of GraphQL budget"
  - "gh project item-list or field-list shows up in a loop or a scheduled job"
tags: [github, graphql, rate-limit, projects-v2, board]
---

# Read project cards off the issues, not the project

**The trap.** `gh project item-list` costs about 101 GraphQL points a page of a
hundred cards, and `gh project field-list` about the same, because both ask
for every field value of every item. A sync that also rewrote a number field on
every card spent most of an hourly 5,000 point budget in one run, and the
lanes sharing that budget stalled.

**What works.** Ask the repository for its issues a hundred at a time and read
each issue's `projectItems`, with `fieldValueByName` for only the fields you
use. That cost 2 points for 324 issues. Match the card by project number and
owner login, since an issue can sit on several projects. Ask for the project
id and field ids in one query on `user(login)` or `organization(login)`.
Compare a stored field with the derived value before writing it; a number
field reads back as a float, and in Python `2.0 == 2`, so no conversion is
needed.

**Keep the completeness checks.** `projectItems.totalCount` against the nodes
read, the repository `issues.totalCount` against the issues seen, a page that
says more with no cursor, and a bound on pages. Pass the cursor with `-f`,
never `-F`, which would type it.

**Ask for the project first.** A token that cannot see a user project still
reads the issues, and their memberships come back empty, which reads exactly
like a board with no cards. Resolve the project before trusting the card read.
