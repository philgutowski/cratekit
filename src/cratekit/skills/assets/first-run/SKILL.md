---
name: first-run
description: Take a fresh install from nothing to a library the other verbs can write to. Use when someone has just installed the tool, when a machine has been rebuilt, or when a verb refuses with a message about configuration, a missing binary, or a credential. Covers the wizard, the health check, the profile, and provider sign in.
---

# First run

Getting from a fresh install to a library the writing verbs will accept.

Nothing here is required to use the product. Every workflow runs from the
command line without any skill installed, and this one exists so the order is
not something a person has to work out.

## The order, and why it is this order

Run the wizard, then the health check, then fix whatever the health check
names. That order matters because the wizard records the answers the health
check reads. Running the check first on a machine with no configuration reports
one large failure instead of the specific one you can act on.

```bash
crate setup
crate doctor
```

The wizard asks where the library is, which taxonomy to use, which profile to
run, and which credentials the enabled modules need. Every answer can be
supplied up front instead, which is what makes the one interactive verb
scriptable:

```bash
crate setup --library-root /path/to/library --profile slim
```

Ask the wizard for a specific taxonomy or a specific database path when the
defaults are wrong for this machine:

```bash
crate setup --taxonomy default --db-path /path/to/database
crate setup --volume-id RECORDED-VOLUME-IDENTIFIER --staging /path/to/staging
```

## Reading what the health check says

The check answers in three states, and the middle one is the one people
misread. `ok` needs nothing. `fail` blocks a verb and names the fix. `info`
means worth knowing and nothing to do now, which is what a switched off feature
module looks like. A report where everything is green or red has nowhere to put
"the backup module is off, so no backup has been recorded", so treat `info` as
information rather than as a weaker failure.

```bash
crate doctor
crate --output json doctor
```

The JSON form is the one to reach for when something else is going to read the
answer, because the human rendering is free to change and the payload is not.

## Profiles decide which modules exist

A profile switches feature modules on and off. A verb belonging to a module the
active profile does not include is not hidden, it refuses and says why, so the
answer to "why does this verb not work" is usually here.

```bash
crate profile show
crate profile set slim
```

Changing the profile changes nothing else. It does not migrate, move, or delete
anything, and it does not rewrite the taxonomy.

## Credentials

A module that talks to a provider needs a credential before it will run, and
the health check reports a missing one against the module that needs it rather
than as a general failure. Supply one from a file rather than typing it, so it
does not end up in a shell history or a process listing:

```bash
crate login provider-session --from-file /path/to/credential
```

Passing the value on the command line is not supported, and that is deliberate
rather than an omission.

## When something still refuses

Read the refusal rather than retrying it. Every refusal from this product
carries a reason and a remedy, and the remedy is a named action rather than a
command to paste, because the action is usually something outside the tool.
Re-run the health check after acting, since it is the verb that answers whether
the condition cleared.

```bash
crate doctor
crate status
```

The second reports the library's own state, open runs and per source sync
state, which is a different question from whether the machine is set up.
