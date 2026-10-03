"""``crate organize``: tidy rekordbox and the account by the product's own rules (U112).

A COMPOSER, as ``crate sync all`` is one. Every tidy step is planned and
written by the verb that owns it, through that verb's own plan and apply
functions, so nothing here is a second implementation of a rule:

* the database area composes ``adopt apply``'s plan and worker, ``inbox
  rotate``'s plan and write, and says what no verb owns (the Record Labels tree
  after a landing, a rename of a batch named for its run);
* the account area composes ``label playlists`` for every followed label,
  ``sync mark`` for every landed pass, and ``export archive`` for every set
  whose download it can prove.

What the author made himself, on either side, is LISTED and never written:
:mod:`cratekit.organize.own` suggests a home where one is obvious.

Layer: modules.
"""
