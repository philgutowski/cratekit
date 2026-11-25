import Foundation

/// The envelope version this app reads. `src/cratekit/cli/output.py` bumps
/// `ENVELOPE_VERSION` only when the frame itself changes, and a frame this
/// app does not know is refused by name rather than read as if it were one.
public let supportedEnvelopeVersion = 1

/// How a run ended, as `cratekit.core.cause.Outcome` names it. A value this
/// app does not know is kept, never folded into one it does.
public enum Outcome: Equatable, Sendable {
    case ok
    case noOp
    case pending
    case blocked
    case failed
    case cancelled
    case unknown(String)

    public init(rawValue: String) {
        switch rawValue {
        case "ok": self = .ok
        case "no_op": self = .noOp
        case "pending": self = .pending
        case "blocked": self = .blocked
        case "failed": self = .failed
        case "cancelled": self = .cancelled
        default: self = .unknown(rawValue)
        }
    }

    public var rawValue: String {
        switch self {
        case .ok: return "ok"
        case .noOp: return "no_op"
        case .pending: return "pending"
        case .blocked: return "blocked"
        case .failed: return "failed"
        case .cancelled: return "cancelled"
        case .unknown(let raw): return raw
        }
    }

    /// The run finished what it was asked, or found nothing to do.
    public var succeeded: Bool { self == .ok || self == .noOp }
}

extension Outcome: Decodable {
    public init(from decoder: Decoder) throws {
        self.init(rawValue: try decoder.singleValueContainer().decode(String.self))
    }
}

/// What a refusal says the person can do about it.
public struct Remediation: Equatable, Sendable, Decodable {
    public let remedy: String?
    public let steps: [String]
    public let doc: String?

    public init(remedy: String?, steps: [String], doc: String?) {
        self.remedy = remedy
        self.steps = steps
        self.doc = doc
    }
}

/// Why a run did not succeed, with the cause it wraps, if any.
public struct Cause: Equatable, Sendable {
    public let reason: String
    public let code: Int
    public let message: String
    public let remediation: Remediation
    public let scope: String
    public let retryable: Bool
    public let origin: [String]
    public let detail: JSONValue
    // An array, since a struct cannot hold itself; never more than one.
    private let innerChain: [Cause]

    /// The cause this one wraps.
    public var inner: Cause? { innerChain.first }

    /// What a gate put in front of the person, when this refusal carries it.
    public var shown: JSONValue? { detail["shown"] }
}

extension Cause: Decodable {
    private enum Keys: String, CodingKey {
        case reason, code, message, remediation, scope, retryable, origin, detail, inner
    }

    public init(from decoder: Decoder) throws {
        let keyed = try decoder.container(keyedBy: Keys.self)
        reason = try keyed.decode(String.self, forKey: .reason)
        code = try keyed.decode(Int.self, forKey: .code)
        message = try keyed.decode(String.self, forKey: .message)
        remediation = try keyed.decode(Remediation.self, forKey: .remediation)
        scope = try keyed.decode(String.self, forKey: .scope)
        retryable = try keyed.decode(Bool.self, forKey: .retryable)
        origin = try keyed.decode([String].self, forKey: .origin)
        detail = try keyed.decode(JSONValue.self, forKey: .detail)
        let inner = try keyed.decodeIfPresent(Cause.self, forKey: .inner)
        innerChain = inner.map { [$0] } ?? []
    }
}

/// Something a person must do outside the tool before the run is complete.
public struct PendingHumanAction: Equatable, Sendable {
    public let kind: String
    public let id: String
    public let summary: String
    public let artifact: String?
    public let steps: [String]
    public let verifyVerb: String
    public let blocks: [String]
    public let expires: String?
}

extension PendingHumanAction: Decodable {
    private enum Keys: String, CodingKey {
        case kind, id, summary, artifact, steps, blocks, expires
        case verifyVerb = "verify_verb"
    }

    public init(from decoder: Decoder) throws {
        let keyed = try decoder.container(keyedBy: Keys.self)
        kind = try keyed.decode(String.self, forKey: .kind)
        id = try keyed.decode(String.self, forKey: .id)
        summary = try keyed.decode(String.self, forKey: .summary)
        artifact = try keyed.decodeIfPresent(String.self, forKey: .artifact)
        steps = try keyed.decodeIfPresent([String].self, forKey: .steps) ?? []
        verifyVerb = try keyed.decode(String.self, forKey: .verifyVerb)
        blocks = try keyed.decodeIfPresent([String].self, forKey: .blocks) ?? []
        expires = try keyed.decodeIfPresent(String.self, forKey: .expires)
    }
}

/// Why standard output could not be read as an envelope.
public enum EnvelopeError: Error, Equatable {
    /// The frame names a version this app does not read.
    case unsupportedVersion(Int)
    /// The bytes are not an envelope at all; the reason is the decoder's.
    case malformed(String)
}

/// One verb's machine readable result, the frame `crate --output json` prints.
///
/// A refusal is an envelope like any other, its `cause` set, so it is read
/// as a value the UI shows, never thrown away.
public struct Envelope: Equatable, Sendable {
    public let envelope: Int
    public let schema: String
    public let verb: String
    public let runId: String
    public let outcome: Outcome
    public let exitCode: Int
    public let started: String
    public let ended: String
    public let pendingHumanAction: PendingHumanAction?
    public let cause: Cause?
    public let warnings: [JSONValue]
    public let resumable: Bool
    public let data: JSONValue

    /// The run stopped short and says why.
    public var isRefusal: Bool { cause != nil }

    /// Read one envelope from what a verb printed on standard output.
    public static func decode(_ bytes: Data) throws -> Envelope {
        do {
            return try JSONDecoder().decode(Envelope.self, from: bytes)
        } catch let error as EnvelopeError {
            throw error
        } catch {
            throw EnvelopeError.malformed(String(describing: error))
        }
    }
}

extension Envelope: Decodable {
    private enum Keys: String, CodingKey {
        case envelope, schema, verb, outcome, started, ended, cause, warnings, resumable, data
        case runId = "run_id"
        case exitCode = "exit_code"
        case pendingHumanAction = "pending_human_action"
    }

    public init(from decoder: Decoder) throws {
        let keyed = try decoder.container(keyedBy: Keys.self)
        // The version first, so a frame from another version is named as one
        // instead of failing on whichever key it moved.
        envelope = try keyed.decode(Int.self, forKey: .envelope)
        guard envelope == supportedEnvelopeVersion else {
            throw EnvelopeError.unsupportedVersion(envelope)
        }
        schema = try keyed.decode(String.self, forKey: .schema)
        verb = try keyed.decode(String.self, forKey: .verb)
        runId = try keyed.decode(String.self, forKey: .runId)
        outcome = try keyed.decode(Outcome.self, forKey: .outcome)
        exitCode = try keyed.decode(Int.self, forKey: .exitCode)
        started = try keyed.decode(String.self, forKey: .started)
        ended = try keyed.decode(String.self, forKey: .ended)
        // Required keys with nullable values: absent is malformed, null is none.
        pendingHumanAction = try keyed.decode(PendingHumanAction?.self, forKey: .pendingHumanAction)
        cause = try keyed.decodeIfPresent(Cause.self, forKey: .cause)
        warnings = try keyed.decode([JSONValue].self, forKey: .warnings)
        resumable = try keyed.decode(Bool.self, forKey: .resumable)
        data = try keyed.decode(JSONValue.self, forKey: .data)
    }
}
