import Foundation

/// Why one `crate status` call gave no glance. Each case is shown with its
/// message, never as a quiet menu.
public enum StatusFailure: Equatable, Sendable {
    /// The crate path is not usable, so nothing was run.
    case setup(CrateSetup)
    /// The process could not be started.
    case launchFailed(String)
    /// The call ran past its timeout and was stopped.
    case timedOut(after: TimeInterval)
    /// The call was ended by a signal the app did not send.
    case signalled(Int32)
    /// Standard output was not an envelope.
    case undecodable(reason: String, firstBytes: String)
    /// The verb refused, its cause's reason and message.
    case refused(reason: String, message: String)
    /// The verb printed an envelope but exited non zero.
    case exitStatus(Int32, stderr: String)
    /// The envelope's glance could not be read.
    case glance(GlanceError)

    public var message: String {
        switch self {
        case .setup(let setup):
            return setup.summary
        case .launchFailed(let reason):
            return "crate could not be started: \(reason)"
        case .timedOut(let after):
            return "crate status did not answer within \(Int(after)) seconds"
        case .signalled(let signal):
            return "crate status was ended by signal \(signal)"
        case .undecodable(let reason, let firstBytes):
            let start = firstBytes.isEmpty ? "nothing" : "\"\(Self.oneLine(firstBytes))\""
            return "crate status printed no envelope (\(reason)); it printed \(start)"
        case .refused(let reason, let message):
            return "crate status refused (\(reason)): \(message)"
        case .exitStatus(let status, let stderr):
            let said = Self.oneLine(stderr)
            return said.isEmpty
                ? "crate status exited with status \(status)"
                : "crate status exited with status \(status): \(said)"
        case .glance(let error):
            return error.message
        }
    }

    /// At most a line's worth of `text`, its whitespace runs folded.
    static func oneLine(_ text: String, limit: Int = 200) -> String {
        let folded = text.split(whereSeparator: { $0.isWhitespace }).joined(separator: " ")
        return folded.count > limit ? String(folded.prefix(limit)) + "..." : folded
    }
}

/// What one status call came to: a glance, or why there is none.
public enum StatusOutcome: Equatable, Sendable {
    case reading(Glance)
    case failure(StatusFailure)

    /// Read the result of running `crate status`.
    public init(_ result: VerbResult) {
        switch result {
        case .setup(let setup):
            self = .failure(.setup(setup))
        case .launchFailed(let reason):
            self = .failure(.launchFailed(reason))
        case .timedOut(let after, _):
            self = .failure(.timedOut(after: after))
        case .signalled(let signal, _):
            self = .failure(.signalled(signal))
        case .undecodable(_, let firstBytes, let reason, _):
            self = .failure(.undecodable(reason: reason, firstBytes: firstBytes))
        case .envelope(let envelope, let status, let stderr):
            if let cause = envelope.cause {
                self = .failure(.refused(reason: cause.reason, message: cause.message))
            } else if status != 0 {
                self = .failure(.exitStatus(status, stderr: stderr))
            } else {
                do {
                    self = .reading(try Glance.from(envelope: envelope))
                } catch let error as GlanceError {
                    self = .failure(.glance(error))
                } catch {
                    self = .failure(.glance(.wrongType(path: "glance", expected: "\(error)")))
                }
            }
        }
    }
}

/// A glance and the moment the call that read it finished.
public struct GoodReading: Equatable, Sendable {
    public let glance: Glance
    public let at: Date

    public init(glance: Glance, at: Date) {
        self.glance = glance
        self.at = at
    }
}

/// What the app knows: the last call's glance if it succeeded, or its
/// failure, and the last good reading either way, kept with its time.
public struct StatusState: Equatable, Sendable {
    /// The last call's reading, nil unless the last call succeeded.
    public private(set) var current: GoodReading?
    /// The latest reading any call gave, which outlives a failed call.
    public private(set) var lastGood: GoodReading?
    /// The last call's failure, nil unless the last call failed.
    public private(set) var failure: StatusFailure?
    /// When the failed call finished.
    public private(set) var failedAt: Date?

    /// Nothing read yet.
    public static let initial = StatusState()

    /// This state after a call that finished at `at` with `outcome`.
    public func recording(_ outcome: StatusOutcome, at: Date) -> StatusState {
        var next = self
        switch outcome {
        case .reading(let glance):
            let reading = GoodReading(glance: glance, at: at)
            next.current = reading
            next.lastGood = reading
            next.failure = nil
            next.failedAt = nil
        case .failure(let failure):
            // Never the last reading as current: it is kept only as lastGood.
            next.current = nil
            next.failure = failure
            next.failedAt = at
        }
        return next
    }
}

/// The menu bar icon: one state per `attention` word, each its own shape so
/// it reads without colour, and one for the time before the first call ends.
public enum StatusIcon: Equatable, Sendable, CaseIterable {
    case reading
    case ok
    case gate
    case running
    case backupDue
    case fail

    /// The icon for `attention`; a word this app does not know reads `fail`.
    public init(_ attention: Attention) {
        switch attention {
        case .ok: self = .ok
        case .gate: self = .gate
        case .running: self = .running
        case .backupDue: self = .backupDue
        case .fail, .unknown: self = .fail
        }
    }

    /// The icon for what the app knows: a failed call reads `fail`, never
    /// the last reading's word.
    public init(_ state: StatusState) {
        if let current = state.current {
            self = StatusIcon(current.glance.attention)
        } else if state.failure != nil {
            self = .fail
        } else {
            self = .reading
        }
    }

    /// The SF Symbol drawn in the menu bar, a distinct shape per state.
    public var symbolName: String {
        switch self {
        case .reading: return "ellipsis.circle"
        case .ok: return "checkmark.circle"
        case .gate: return "hand.raised"
        case .running: return "arrow.triangle.2.circlepath"
        case .backupDue: return "externaldrive.badge.exclamationmark"
        case .fail: return "xmark.octagon"
        }
    }

    /// What the icon says to a screen reader and in its tooltip.
    public var label: String {
        switch self {
        case .reading: return "Cratekit: reading status"
        case .ok: return "Cratekit: nothing needs you"
        case .gate: return "Cratekit: a gate is waiting"
        case .running: return "Cratekit: a job is running"
        case .backupDue: return "Cratekit: a backup is due"
        case .fail: return "Cratekit: something failed or could not be read"
        }
    }
}

/// One line of the status menu.
public struct MenuLine: Equatable, Sendable {
    public enum Kind: Equatable, Sendable {
        /// A line that names a section or the state of the whole.
        case heading
        /// A fact the glance says.
        case item
        /// A source or a call that could not be read, with its message.
        case problem
    }

    public let kind: Kind
    public let text: String

    public init(_ kind: Kind, _ text: String) {
        self.kind = kind
        self.text = text
    }
}

/// The status menu as lines: a projection of the glance that adds nothing
/// the verb did not say, so the tests read the menu without a screen.
public enum StatusMenu {
    /// The menu for what the app knows. A failed call leads with its failure
    /// and shows the last good reading under its time, never as current.
    public static func lines(for state: StatusState, timeZone: TimeZone = .current) -> [MenuLine] {
        if let current = state.current {
            return lines(for: current)
        }
        guard let failure = state.failure else {
            return [MenuLine(.heading, "Reading crate status")]
        }
        var made = [MenuLine(.problem, "Status could not be read: \(failure.message)")]
        if let failedAt = state.failedAt {
            made.append(MenuLine(.item, "Failed at \(stamp(failedAt, timeZone))"))
        }
        guard let last = state.lastGood else {
            made.append(MenuLine(.item, "No good reading yet"))
            return made
        }
        made.append(MenuLine(.heading, "Last good reading, at \(stamp(last.at, timeZone)):"))
        return made + lines(for: last)
    }

    /// The menu for one reading, its ages measured at the reading's time.
    public static func lines(for reading: GoodReading) -> [MenuLine] {
        let glance = reading.glance
        return [attentionLine(glance.attention)]
            + backupLines(glance.backup)
            + [rekordboxLine(glance.rekordbox)]
            + jobLines(glance.jobsRunning)
            + gateLines(glance.gates, at: reading.at)
            + [nightLine(glance.night)]
    }

    static func attentionLine(_ attention: Attention) -> MenuLine {
        switch attention {
        case .ok:
            return MenuLine(.heading, "ok: nothing needs you")
        case .gate:
            return MenuLine(.heading, "gate: a run is waiting for an answer")
        case .running:
            return MenuLine(.heading, "running: a job is running")
        case .backupDue:
            return MenuLine(.heading, "backup-due: a backup is five days old, or its age is unknown")
        case .fail:
            return MenuLine(
                .heading, "fail: a source could not be read, or a backup is recorded ahead of now")
        case .unknown(let word):
            return MenuLine(
                .problem,
                "fail: crate said \"\(word)\", a word this app does not know, so it is read as fail")
        }
    }

    static func backupLines(_ backup: Readable<BackupAges>) -> [MenuLine] {
        switch backup {
        case .unreadable(let message):
            return [MenuLine(.problem, "Backup ages could not be read: \(message)")]
        case .value(let ages):
            return [portionLine("Files backup", ages.files),
                    portionLine("Database backup", ages.database)]
        }
    }

    static func portionLine(_ name: String, _ portion: BackupPortion) -> MenuLine {
        switch portion.state {
        case .known:
            guard let seconds = portion.ageSeconds else {
                return MenuLine(.item, "\(name): known, with no age")
            }
            return MenuLine(.item, "\(name): \(days(seconds)) old")
        case .neverRecorded:
            return MenuLine(.item, "\(name): never recorded")
        case .recordedInTheFuture:
            let when = portion.completedAt.map { ", at \($0)" } ?? ""
            return MenuLine(.problem, "\(name): recorded ahead of now\(when)")
        case .unknown(let word):
            let age = portion.ageSeconds.map { ", \(days($0)) old" } ?? ""
            return MenuLine(.item, "\(name): \(word)\(age)")
        }
    }

    static func rekordboxLine(_ state: Readable<RekordboxState>) -> MenuLine {
        switch state {
        case .unreadable(let message):
            return MenuLine(.problem, "rekordbox could not be checked: \(message)")
        case .value(.closed):
            return MenuLine(.item, "rekordbox: closed")
        case .value(.open):
            return MenuLine(.item, "rekordbox: open")
        case .value(.unknown):
            return MenuLine(.item, "rekordbox: unknown, the scan could not confirm it is closed")
        case .value(.unrecognised(let word)):
            return MenuLine(.item, "rekordbox: \(word)")
        }
    }

    static func jobLines(_ jobs: Readable<[RunningJob]>) -> [MenuLine] {
        switch jobs {
        case .unreadable(let message):
            return [MenuLine(.problem, "Running jobs could not be read: \(message)")]
        case .value(let found) where found.isEmpty:
            return [MenuLine(.item, "No job running")]
        case .value(let found):
            return [MenuLine(.heading, "Jobs running:")]
                + found.map { MenuLine(.item, "\($0.verb), job \($0.jobId), \($0.state)") }
        }
    }

    static func gateLines(_ gates: Readable<[GateItem]>, at: Date) -> [MenuLine] {
        switch gates {
        case .unreadable(let message):
            return [MenuLine(.problem, "Waiting gates could not be read: \(message)")]
        case .value(let found) where found.isEmpty:
            return [MenuLine(.item, "No gate waiting")]
        case .value(let found):
            return [MenuLine(.heading, "Gates waiting:")] + found.map { gateLine($0, at: at) }
        }
    }

    static func gateLine(_ item: GateItem, at: Date) -> MenuLine {
        switch item {
        case .unreadable(let runId, let message):
            return MenuLine(.problem, "Run \(runId) could not be read: \(message)")
        case .gate(let gate):
            let writes = gate.writesDatabase ? "writes the database" : "writes no database"
            let old = gate.old ? ", old" : ""
            return MenuLine(
                .item, "\(gate.verb) at \(gate.gate), \(waiting(gate.since, at: at)), \(writes)\(old)")
        }
    }

    static func nightLine(_ night: Readable<NightPass>?) -> MenuLine {
        switch night {
        case .none:
            return MenuLine(.item, "Night pass: none recorded")
        case .some(.unreadable(let message)):
            return MenuLine(.problem, "Night pass could not be read: \(message)")
        case .some(.value(let pass)):
            return MenuLine(.item, "Night pass: \(pass.line)")
        }
    }

    /// Whole days, never rounded up.
    static func days(_ seconds: Int) -> String {
        let whole = seconds / 86_400
        if whole <= 0 { return "under a day" }
        return whole == 1 ? "1 day" : "\(whole) days"
    }

    /// How long a gate has waited at `at`, or its instant when that cannot
    /// be read as one.
    static func waiting(_ since: String, at: Date) -> String {
        guard let start = ISO8601DateFormatter().date(from: since) else {
            return "waiting since \(since)"
        }
        let seconds = Int(at.timeIntervalSince(start))
        if seconds < 60 { return "waiting under a minute" }
        if seconds < 3_600 { return "waiting \(count(seconds / 60, "minute"))" }
        if seconds < 86_400 { return "waiting \(count(seconds / 3_600, "hour"))" }
        return "waiting \(count(seconds / 86_400, "day"))"
    }

    static func count(_ number: Int, _ unit: String) -> String {
        number == 1 ? "1 \(unit)" : "\(number) \(unit)s"
    }

    /// A reading's time, to the minute, in `timeZone`.
    static func stamp(_ date: Date, _ timeZone: TimeZone) -> String {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: "en_US_POSIX")
        formatter.timeZone = timeZone
        formatter.dateFormat = "yyyy-MM-dd HH:mm"
        return formatter.string(from: date)
    }
}
