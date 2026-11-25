import AppKit
import CrateEngine
import SwiftUI

/// The menu bar app: a placeholder menu and Quit, with no Dock icon.
///
/// Status, Sync and gates are the next cards'. The app talks to the engine
/// only through crate's verbs, by way of CrateEngine.
@main
struct CratekitBarApp: App {
    init() {
        // LSUIElement in the bundle's Info.plist keeps the Dock icon away;
        // this keeps it away for an unbundled `swift run` too.
        NSApplication.shared.setActivationPolicy(.accessory)
    }

    var body: some Scene {
        MenuBarExtra("Cratekit", systemImage: "music.note.list") {
            Text(CrateSettings.setup().summary)
            Divider()
            Button("Quit Cratekit") {
                NSApplication.shared.terminate(nil)
            }
            .keyboardShortcut("q")
        }
    }
}
