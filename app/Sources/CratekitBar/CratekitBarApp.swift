import AppKit
import CrateEngine
import SwiftUI

/// The menu bar app: an icon that says whether Cratekit needs Phillip, and a
/// menu of what `crate status` says, with no Dock icon (U966).
///
/// Sync and gates are the next cards'. The app talks to the engine only
/// through crate's verbs, by way of CrateEngine, and in this card runs no
/// verb but `crate status`.
@main
struct CratekitBarApp: App {
    @StateObject private var model = StatusModel()

    init() {
        // LSUIElement in the bundle's Info.plist keeps the Dock icon away;
        // this keeps it away for an unbundled `swift run` too.
        NSApplication.shared.setActivationPolicy(.accessory)
    }

    var body: some Scene {
        MenuBarExtra {
            StatusMenuView(model: model)
        } label: {
            Image(systemName: model.icon.symbolName)
                .accessibilityLabel(model.icon.label)
                .help(model.icon.label)
        }
    }
}

/// The status the menu and the icon show, refreshed every minute and when
/// the menu opens, one call at a time.
@MainActor
final class StatusModel: ObservableObject {
    @Published private(set) var state = StatusState.initial

    private let refresher = StatusRefresher.live()
    private var ticking: Task<Void, Never>?
    private var menuOpens: NSObjectProtocol?

    var icon: StatusIcon { StatusIcon(state) }
    var lines: [MenuLine] { StatusMenu.lines(for: state) }

    init() {
        ticking = Task { [weak self] in
            while !Task.isCancelled {
                await self?.refresh()
                try? await Task.sleep(nanoseconds: UInt64(StatusRefresher.interval * 1_000_000_000))
            }
        }
        // The menu bar extra's menu is the app's only menu, so a menu that
        // begins tracking is the status menu opening.
        menuOpens = NotificationCenter.default.addObserver(
            forName: NSMenu.didBeginTrackingNotification, object: nil, queue: .main
        ) { [weak self] _ in
            Task { @MainActor in await self?.refresh() }
        }
    }

    func refresh() async {
        state = await refresher.refresh()
    }
}

/// The menu: the status lines, then Refresh and Quit.
struct StatusMenuView: View {
    @ObservedObject var model: StatusModel

    var body: some View {
        ForEach(Array(model.lines.enumerated()), id: \.offset) { _, line in
            switch line.kind {
            case .heading:
                Text(line.text).bold()
            case .item:
                Text(line.text)
            case .problem:
                Label(line.text, systemImage: "exclamationmark.triangle")
            }
        }
        Divider()
        Button("Refresh") {
            Task { await model.refresh() }
        }
        .keyboardShortcut("r")
        Button("Quit Cratekit") {
            NSApplication.shared.terminate(nil)
        }
        .keyboardShortcut("q")
    }
}
