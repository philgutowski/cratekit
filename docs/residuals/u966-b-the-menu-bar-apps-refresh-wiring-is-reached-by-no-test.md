---
title: The menu bar app's minute tick and menu open refresh are reached by no test
found: at review round one of #1085, U966, 2026-11-25.
issue: no
---

**The mechanism.** `StatusModel` in `app/Sources/CratekitBar/CratekitBarApp.swift`
starts the minute loop and observes `NSMenu.didBeginTrackingNotification` to
refresh when the menu opens. `CratekitBar` is an executable target no test
imports, so only the constants (`StatusRefresher.interval`, the call's
timeout) and the refresher are tested; removing the loop or the observer
fails nothing. The observer is registered for every menu (`object: nil`), so a
later card that adds another menu also starts a status call when it opens.
Whether a menu style `MenuBarExtra` redraws a menu that is already open when
the refresh lands is unmeasured; the menu's last line says when its reading
was taken, so an old one is seen as old.

**Measured cost.** Not driven: no Swift runs on this container, and the
runner has no menu bar to open. A person would see a status that stops
refreshing only by reading the time on the menu's last line.

**Closes when:** the install card (#1088) reads the refresh on the Mac (the
time on the last line moves each minute and on opening), or the wiring moves
into a tested type in `CrateEngine`. Ledger only: nothing is lost or
misreported, and the time is shown.
