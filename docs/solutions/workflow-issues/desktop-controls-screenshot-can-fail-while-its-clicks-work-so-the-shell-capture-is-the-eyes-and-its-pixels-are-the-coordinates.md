---
title: Desktop control's screenshot can fail while its clicks work, so the shell's screen capture is the eyes and its retina pixels are the click coordinates
date: 2026-10-27
category: workflow-issues
module: "attended sittings, rekordbox through desktop control"
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "A session drives rekordbox through the computer-use tools and every screenshot call returns nil or a backstop error while request_access succeeds"
  - "Two Claude sessions on one machine both want desktop control and the lock passed between them by deleting the lock file"
tags:
  - "desktop-control"
  - "computer-use"
  - "screenshot"
  - "rekordbox"
  - "attended-sitting"
  - "cross-session"
related_components:
  - "tooling"
---

# Desktop control's screenshot can fail while its clicks work, so the shell's screen capture is the eyes and its retina pixels are the click coordinates

## Context

Sitting 46 (2026-10-27, the PULS Bandcamp batch) needed rekordbox opened to analyse 96 landed rows and build a label folder by hand. The desktop control lock (`~/.config/claude-work/computer-use.lock`) was held by the other Cratekit session on the machine, which had taken it hours earlier and never used it. It had no tool that releases the lock, so Phillip had its lock file deleted. This session then took the lock, `request_access` granted rekordbox at the full tier, `open_application` opened it, and every `screenshot` call failed: "Screenshot capture returned nil (permission missing or SCContentFilter failure)", then "CU screenshot backstop". An `/mcp` reset of the server and a fresh grant changed nothing. The screen was not locked, the display was online, and `screencapture -x` from the same terminal produced a full image at once, so Screen Recording permission was not the cause; the failure was inside the server's own capture path, most likely the state left by the forced lock handover.

## Guidance

**1. The clicks still work, so do not stop.** `mouse_move`, `left_click`, `type` and `key` kept working with rekordbox frontmost. What was missing was the picture, and the shell has one: `screencapture -x -C -t png <file>` writes the whole display, cursor included, and `Read` on that file shows it. One capture after each action, read, then the next action.

**2. With no server screenshot taken, click coordinates are the capture's own pixels.** The capture is at retina resolution (3024 by 1964 on this machine, logical 1512 by 982). A `mouse_move` to (300, 500) put the cursor tip at pixel (296, 495) of the capture, so a coordinate read off the capture image is the coordinate to click, with no halving and no scaling. `Read` downsamples the image it shows and states the factor (1.51 here); multiply what you read off the displayed image by that factor and click. Verify the mapping once per session with a `mouse_move` and a `-C` capture before the first click, since the server states that without a screenshot it reads logical points, and on this machine it did not.

**3. Sequence the capture after the action in one response.** Send the click first and the `sleep 2; screencapture` second in the same response; either order of execution yields a post-click image. A sleep over a few seconds in a foreground command is refused by the harness; for a wait on rekordbox itself, watch its analysis store instead (below).

**4. Rekordbox's analysis progress is readable from the volume.** Each analysed track writes `ANLZ*.DAT` under `PIONEER/Master/share/PIONEER/USBANLZ/<xxx>/<uuid>/`. `find <store> -name 'ANLZ*.DAT' -newer <a file written when the batch was selected> | wc -l` counts finished tracks, and a run in the background that exits when the count reaches the batch size and the store has been quiet for twenty seconds is the one notification needed. Roughly five seconds a track with BPM/Grid, high precision and Phrase on.

**5. Hand the lock over through `/mcp`, not by deleting the file.** The holder disables `computer-use` for its session from `/mcp`, which releases the lock cleanly. A deleted lock file lets the next session acquire, and the capture failure above followed that path. Whether a clean release avoids it is not yet measured; the next sitting that needs the lock from another session should release it cleanly and record whether `screenshot` then works.

**6. Analyze Tracks opens on the last run's settings, and its Analysis Mode list needs a held press.** Found at sitting 47 (2026-10-27): the dialog came up on Dynamic, high precision on and KEY off, none of them Phillip's standard, and a click on the Analysis Mode control did nothing, so the run started on Dynamic and could be stopped only by quitting rekordbox. The list opens only while the mouse is held down on it: press, move to the item still holding, release on it, then read the control back. Read every field back from a screenshot before OK. The `rekordbox-visit` project skill carries the whole procedure and the settings table (U173).

## Why This Matters

An attended sitting is the only place rekordbox is opened, and its rows in the record are what the product's native writes are proven against. A session that stops at the first screenshot failure leaves rekordbox open on the live library, every `crate` verb in every other session held, and the landed rows unanalysed. The shell capture costs one extra round trip per action and loses nothing.

## When to Apply

Any attended sitting that drives rekordbox or another desktop app through the computer-use tools, and any handover of the desktop control lock between sessions on one machine.
