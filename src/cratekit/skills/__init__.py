"""The optional operator skills, and the verb that installs them.

R7 in one sentence: the skills ship with the package, contain no personal
context, and are optional, because the CLI covers every workflow without them.

WHY THEY LIVE INSIDE THE PACKAGE. A directory beside the package is not shipped
by a wheel, so a repository-root ``skills/`` would exist in this checkout, be
absent from every install, and leave the install verb with nothing to copy on
the one machine that matters. ``cratekit.core.taxonomy`` already reads its
shipped templates through ``importlib.resources`` and this follows that
precedent rather than inventing a second answer to one question.

Empty of imports so importing the package does not import the CLI (KTD7).
"""
