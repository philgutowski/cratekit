import Foundation

/// One verb to run: its arguments after `crate --output json`, and how long
/// it may take.
public struct VerbCall: Equatable, Sendable {
    public let arguments: [String]
    public let timeout: TimeInterval

    public init(_ arguments: [String], timeout: TimeInterval = 60) {
        self.arguments = arguments
        self.timeout = timeout
    }
}

/// What came of running a verb. Every case is a value the UI can show.
public enum VerbResult: Equatable, Sendable {
    /// The verb printed an envelope. A refusal is one too, its `cause` set,
    /// and `status` is the process's exit status.
    case envelope(Envelope, status: Int32, stderr: String)
    /// The crate path is not usable, so nothing was run.
    case setup(CrateSetup)
    /// The verb ran past its timeout and was ended.
    case timedOut(after: TimeInterval, stderr: String)
    /// The verb was ended by a signal it did not send itself, numbered here,
    /// so a signal's number is never read as one of crate's exit codes.
    case signalled(Int32, stderr: String)
    /// Standard output was not an envelope. `firstBytes` is the start of what
    /// it held, empty only when it held nothing.
    case undecodable(status: Int32, firstBytes: String, reason: String, stderr: String)
    /// The process could not be started.
    case launchFailed(String)
}

/// The environment a verb runs in: only what crate needs, never the app's.
public enum CrateEnvironment {
    /// The keys passed on from the app's own environment when present.
    public static let passedKeys = ["HOME", "LANG", "LC_ALL", "LC_CTYPE", "TMPDIR"]
    /// The system directories after crate's own on PATH, so a tool crate
    /// calls by name resolves to the system's, never a login shell's.
    public static let systemPath = "/usr/bin:/bin:/usr/sbin:/sbin"

    public static func minimal(for crate: URL, from environment: [String: String]) -> [String: String] {
        var made: [String: String] = [:]
        for key in passedKeys {
            if let value = environment[key], !value.isEmpty { made[key] = value }
        }
        if made["HOME"] == nil { made["HOME"] = NSHomeDirectory() }
        if made["LANG"] == nil { made["LANG"] = "en_US.UTF-8" }
        made["PATH"] = crate.deletingLastPathComponent().path + ":" + systemPath
        return made
    }
}

/// Runs crate verbs the one safe way: the absolute path from the settings,
/// no shell, a fixed argument list, a minimal environment and a timeout.
public struct CrateRunner: Sendable {
    /// How many bytes of an undecodable standard output are reported.
    public static let firstBytesLimit = 256
    /// How long a verb has to exit after it is asked to, before it is killed.
    public static let terminationGrace: TimeInterval = 3
    /// How long output is still read after the verb exits, since a child it
    /// left behind may hold the pipe open.
    public static let drainGrace: TimeInterval = 2

    public let setup: CrateSetup
    public let environment: [String: String]

    public init(path: String?, environment: [String: String] = ProcessInfo.processInfo.environment) {
        self.setup = CrateSetup.check(path)
        self.environment = environment
    }

    /// The arguments crate is started with for `call`.
    public static func arguments(for call: VerbCall) -> [String] {
        call.arguments
    }

    /// Run `call` off the caller's thread.
    public func run(_ call: VerbCall) async -> VerbResult {
        await withCheckedContinuation { continuation in
            DispatchQueue.global(qos: .userInitiated).async {
                continuation.resume(returning: runBlocking(call))
            }
        }
    }

    /// Run `call` and wait for it, at most its timeout and the graces.
    public func runBlocking(_ call: VerbCall) -> VerbResult {
        guard case .ready(let crate) = setup else { return .setup(setup) }

        let process = Process()
        process.executableURL = crate
        process.arguments = Self.arguments(for: call)
        process.environment = CrateEnvironment.minimal(for: crate, from: environment)
        process.standardInput = FileHandle.nullDevice
        let stdout = Pipe()
        let stderr = Pipe()
        process.standardOutput = stdout
        process.standardError = stderr

        let exited = DispatchSemaphore(value: 0)
        process.terminationHandler = { _ in exited.signal() }
        let drained = DispatchGroup()
        let out = Collected(stdout.fileHandleForReading, group: drained)
        let err = Collected(stderr.fileHandleForReading, group: drained)

        do {
            try process.run()
        } catch {
            out.stop()
            err.stop()
            return .launchFailed(String(describing: error))
        }

        var timedOut = false
        if exited.wait(timeout: .now() + call.timeout) == .timedOut {
            timedOut = true
            process.terminate()
            if exited.wait(timeout: .now() + Self.terminationGrace) == .timedOut {
                if process.isRunning { kill(process.processIdentifier, SIGKILL) }
                _ = exited.wait(timeout: .now() + Self.terminationGrace)
            }
        }
        _ = drained.wait(timeout: .now() + Self.drainGrace)
        out.stop()
        err.stop()

        let errText = String(decoding: err.data, as: UTF8.self)
        if timedOut { return .timedOut(after: call.timeout, stderr: errText) }
        if process.terminationReason == .uncaughtSignal {
            return .signalled(process.terminationStatus, stderr: errText)
        }
        return Self.read(out.data, status: process.terminationStatus, stderr: errText)
    }

    /// What a verb's standard output says, as a result.
    public static func read(_ bytes: Data, status: Int32, stderr: String) -> VerbResult {
        let first = String(decoding: bytes.prefix(firstBytesLimit), as: UTF8.self)
        if bytes.allSatisfy({ $0 == 0x20 || $0 == 0x0A || $0 == 0x0D || $0 == 0x09 }) {
            return .undecodable(
                status: status, firstBytes: first,
                reason: "standard output held no envelope", stderr: stderr)
        }
        do {
            return .envelope(try Envelope.decode(bytes), status: status, stderr: stderr)
        } catch EnvelopeError.unsupportedVersion(let version) {
            return .undecodable(
                status: status, firstBytes: first,
                reason: "envelope version \(version) is not \(supportedEnvelopeVersion)",
                stderr: stderr)
        } catch {
            return .undecodable(
                status: status, firstBytes: first, reason: String(describing: error),
                stderr: stderr)
        }
    }
}

/// The bytes read from one pipe as they arrive, so what was written before
/// a timeout or a held pipe is kept.
private final class Collected: @unchecked Sendable {
    private let lock = NSLock()
    private var bytes = Data()
    private var open = true
    private let handle: FileHandle
    private let group: DispatchGroup

    init(_ handle: FileHandle, group: DispatchGroup) {
        self.handle = handle
        self.group = group
        group.enter()
        handle.readabilityHandler = { [weak self] readable in
            let chunk = readable.availableData
            guard let self else { return }
            if chunk.isEmpty {
                self.finish()
            } else {
                self.lock.lock()
                self.bytes.append(chunk)
                self.lock.unlock()
            }
        }
    }

    var data: Data {
        lock.lock()
        defer { lock.unlock() }
        return bytes
    }

    /// Stop reading, whether or not the pipe reached its end.
    func stop() {
        handle.readabilityHandler = nil
        finish()
    }

    private func finish() {
        lock.lock()
        let wasOpen = open
        open = false
        lock.unlock()
        if wasOpen {
            handle.readabilityHandler = nil
            group.leave()
        }
    }
}
