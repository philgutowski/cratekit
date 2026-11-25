import Foundation

/// The glance version this app reads. `src/cratekit/cli/status_glance.py`
/// bumps `VERSION` only when a key changes meaning or goes, and a glance of
/// another version is refused by name rather than read as if it were this one.
public let supportedGlanceVersion = 1

/// The one word `crate status` says about whether Cratekit needs Phillip,
/// most urgent first. A word this app does not know, from a newer engine, is
/// kept as `unknown`, never folded into one it does, and the icon reads it as
/// `fail` (U966).
public enum Attention: Equatable, Sendable {
    case fail
    case gate
    case running
    case backupDue
    case ok
    case unknown(String)

    public init(rawValue: String) {
        switch rawValue {
        case "fail": self = .fail
        case "gate": self = .gate
        case "running": self = .running
        case "backup-due": self = .backupDue
        case "ok": self = .ok
        default: self = .unknown(rawValue)
        }
    }

    public var rawValue: String {
        switch self {
        case .fail: return "fail"
        case .gate: return "gate"
        case .running: return "running"
        case .backupDue: return "backup-due"
        case .ok: return "ok"
        case .unknown(let raw): return raw
        }
    }
}

/// A source the glance read, or the message it carries instead when the
/// source could not be read. Never an empty answer standing in for one.
public enum Readable<Value: Equatable & Sendable>: Equatable, Sendable {
    case value(Value)
    case unreadable(String)
}

/// How a backup portion's age stands, in the glance's words.
public enum BackupAgeState: Equatable, Sendable {
    case known
    case neverRecorded
    case recordedInTheFuture
    case unknown(String)

    public init(rawValue: String) {
        switch rawValue {
        case "known": self = .known
        case "never-recorded": self = .neverRecorded
        case "recorded-in-the-future": self = .recordedInTheFuture
        default: self = .unknown(rawValue)
        }
    }
}

/// One backup portion: its state, its age in whole seconds and when it
/// completed, the last two null when nothing is recorded.
public struct BackupPortion: Equatable, Sendable {
    public let state: BackupAgeState
    public let ageSeconds: Int?
    public let completedAt: String?
}

/// Both backup portions.
public struct BackupAges: Equatable, Sendable {
    public let files: BackupPortion
    public let database: BackupPortion
}

/// Whether rekordbox is running, as doctor's process scan says it. `unknown`
/// is the scan's own word for a process it could not read, never closed.
public enum RekordboxState: Equatable, Sendable {
    case closed
    case open
    case unknown
    /// A word this app does not know, kept as it was said.
    case unrecognised(String)

    public init(rawValue: String) {
        switch rawValue {
        case "closed": self = .closed
        case "open": self = .open
        case "unknown": self = .unknown
        default: self = .unrecognised(rawValue)
        }
    }
}

/// One job in state running.
public struct RunningJob: Equatable, Sendable {
    public let jobId: String
    public let verb: String
    public let state: String
}

/// One run waiting at a gate.
public struct WaitingGate: Equatable, Sendable {
    public let runId: String
    public let verb: String
    public let gate: String
    public let options: [String]
    /// Null when this build no longer declares the gate.
    public let explicit: Bool?
    public let writesDatabase: Bool
    /// When the run went idle, as an ISO 8601 instant.
    public let since: String
    /// Past the age `crate run retire` acts on.
    public let old: Bool
}

/// An item of the glance's gate list: a waiting gate, or a run record that
/// could not be read, which is listed rather than hidden.
public enum GateItem: Equatable, Sendable {
    case gate(WaitingGate)
    case unreadable(runId: String, message: String)
}

/// How the last night pass ended, its fields as `crate sync night --last`
/// prints them.
public struct NightPass: Equatable, Sendable {
    public let outcome: String
    public let line: String
    public let gateRun: String?
    public let passRun: String?
    public let staging: String?
}

/// `crate status`'s `data.summary.glance`, decoded against
/// `tests/schemas/status_glance.v1.json`. The menu is a projection of this
/// and nothing else.
public struct Glance: Equatable, Sendable {
    public let version: Int
    public let attention: Attention
    public let backup: Readable<BackupAges>
    public let rekordbox: Readable<RekordboxState>
    public let jobsRunning: Readable<[RunningJob]>
    public let gates: Readable<[GateItem]>
    /// Nil when no night pass is recorded.
    public let night: Readable<NightPass>?
    /// Any key this app does not know that carries an unreadable message,
    /// from a newer engine at the same version, so a source it could not read
    /// is still said rather than dropped.
    public let otherUnreadable: [String: String]
}

/// Why a status envelope's glance could not be read.
public enum GlanceError: Error, Equatable, Sendable {
    /// The glance names a version this app does not read.
    case unsupportedVersion(Int)
    /// A required key is absent; the path names it.
    case missing(String)
    /// A value is not the type the schema gives it.
    case wrongType(path: String, expected: String)

    public var message: String {
        switch self {
        case .unsupportedVersion(let version):
            return "the status glance is version \(version), and this app reads version \(supportedGlanceVersion)"
        case .missing(let path):
            return "the status glance has no \(path)"
        case .wrongType(let path, let expected):
            return "the status glance's \(path) is not \(expected)"
        }
    }
}

extension Glance {
    /// The glance in a `crate status` envelope's data.
    public static func from(envelope: Envelope) throws -> Glance {
        try decode(Field(envelope.data, "data").member("summary").member("glance"))
    }

    /// The glance from its own JSON value, `data.summary.glance`.
    public static func decode(_ value: JSONValue) throws -> Glance {
        try decode(Field(value, "glance"))
    }

    private static func decode(_ glance: Field) throws -> Glance {
        _ = try glance.object()
        // The version first, so a glance of another version is named as one
        // instead of failing on whichever key it moved.
        let version = try glance.member("version").int()
        guard version == supportedGlanceVersion else {
            throw GlanceError.unsupportedVersion(version)
        }
        let nightField = try glance.member("night")
        let night: Readable<NightPass>? =
            try nightField.value.isNull ? nil : nightField.readable(nightPass)
        return Glance(
            version: version,
            attention: Attention(rawValue: try glance.member("attention").string()),
            backup: try glance.member("backup").readable { source in
                BackupAges(
                    files: try portion(source.member("files")),
                    database: try portion(source.member("database")))
            },
            rekordbox: try glance.member("rekordbox").readable { source in
                RekordboxState(rawValue: try source.string())
            },
            jobsRunning: try glance.member("jobs_running").readable { source in
                try source.array().map(job)
            },
            gates: try glance.member("gates").readable { source in
                try source.array().map(gateItem)
            },
            night: night,
            otherUnreadable: try otherUnreadable(glance)
        )
    }

    /// The keys a version 1 glance carries.
    static let knownKeys: Set<String> = [
        "version", "attention", "backup", "rekordbox", "jobs_running", "gates", "night",
    ]

    private static func otherUnreadable(_ glance: Field) throws -> [String: String] {
        var found: [String: String] = [:]
        for key in try glance.object().keys where !knownKeys.contains(key) {
            if let message = try glance.member(key).unreadableMessage() { found[key] = message }
        }
        return found
    }

    private static func portion(_ field: Field) throws -> BackupPortion {
        BackupPortion(
            state: BackupAgeState(rawValue: try field.member("state").string()),
            ageSeconds: try field.member("age_seconds").optionalInt(),
            completedAt: try field.member("completed_at").optionalString())
    }

    private static func job(_ field: Field) throws -> RunningJob {
        RunningJob(
            jobId: try field.member("job_id").string(),
            verb: try field.member("verb").string(),
            state: try field.member("state").string())
    }

    private static func gateItem(_ field: Field) throws -> GateItem {
        if let message = try field.unreadableMessage() {
            return .unreadable(runId: try field.member("run_id").string(), message: message)
        }
        return .gate(
            WaitingGate(
                runId: try field.member("run_id").string(),
                verb: try field.member("verb").string(),
                gate: try field.member("gate").string(),
                options: try field.member("options").array().map { try $0.string() },
                explicit: try field.member("explicit").optionalBool(),
                writesDatabase: try field.member("writes_database").bool(),
                since: try field.member("since").string(),
                old: try field.member("old").bool()))
    }

    private static func nightPass(_ field: Field) throws -> NightPass {
        NightPass(
            outcome: try field.member("outcome").string(),
            line: try field.member("line").string(),
            gateRun: try field.member("gate_run").optionalString(),
            passRun: try field.member("pass_run").optionalString(),
            staging: try field.member("staging").optionalString())
    }
}

/// One value in the glance with the path that reached it, so an error names
/// the key it is about.
private struct Field {
    let value: JSONValue
    let path: String

    init(_ value: JSONValue, _ path: String) {
        self.value = value
        self.path = path
    }

    func object() throws -> [String: JSONValue] {
        guard let members = value.objectValue else {
            throw GlanceError.wrongType(path: path, expected: "an object")
        }
        return members
    }

    /// A required key: absent is malformed, null is a value.
    func member(_ key: String) throws -> Field {
        guard let found = try object()[key] else {
            throw GlanceError.missing("\(path).\(key)")
        }
        return Field(found, "\(path).\(key)")
    }

    func string() throws -> String {
        guard let text = value.stringValue else {
            throw GlanceError.wrongType(path: path, expected: "a string")
        }
        return text
    }

    func optionalString() throws -> String? {
        try value.isNull ? nil : string()
    }

    func bool() throws -> Bool {
        guard let flag = value.boolValue else {
            throw GlanceError.wrongType(path: path, expected: "a boolean")
        }
        return flag
    }

    func optionalBool() throws -> Bool? {
        try value.isNull ? nil : bool()
    }

    /// A whole number. JSON numbers arrive as doubles, so one with a fraction,
    /// or past what a double holds exactly, is not an integer.
    func int() throws -> Int {
        guard let number = value.numberValue, number == number.rounded(),
            abs(number) <= 9_007_199_254_740_992
        else {
            throw GlanceError.wrongType(path: path, expected: "an integer")
        }
        return Int(number)
    }

    func optionalInt() throws -> Int? {
        try value.isNull ? nil : int()
    }

    func array() throws -> [Field] {
        guard let elements = value.arrayValue else {
            throw GlanceError.wrongType(path: path, expected: "an array")
        }
        return elements.enumerated().map { Field($0.element, "\(path)[\($0.offset)]") }
    }

    /// The message of an `{"unreadable": "..."}` object, else nil.
    func unreadableMessage() throws -> String? {
        guard let members = value.objectValue, let message = members["unreadable"] else {
            return nil
        }
        guard let text = message.stringValue else {
            throw GlanceError.wrongType(path: "\(path).unreadable", expected: "a string")
        }
        return text
    }

    /// The source's value read by `read`, or its unreadable message.
    func readable<Value: Equatable & Sendable>(_ read: (Field) throws -> Value) throws -> Readable<Value> {
        return .value(try read(self))
    }
}
