import Foundation
import XCTest

@testable import CrateEngine

/// The decoder over envelopes the Python side really emits: each fixture is
/// written by tests/test_app_fixtures.py from a real verb, and that test fails
/// the battery when the verb stops emitting it.
final class EnvelopeDecodingTests: XCTestCase {
    private func decoded(_ name: String) throws -> Envelope {
        try Envelope.decode(try Fixtures.data(name))
    }

    func testDoctorDecodesWithItsChecks() throws {
        let envelope = try decoded("doctor")
        XCTAssertEqual(envelope.envelope, 1)
        XCTAssertEqual(envelope.schema, "diagnostic/1")
        XCTAssertEqual(envelope.verb, "doctor")
        XCTAssertEqual(envelope.outcome, .ok)
        XCTAssertTrue(envelope.outcome.succeeded)
        XCTAssertEqual(envelope.exitCode, 0)
        XCTAssertNil(envelope.cause)
        XCTAssertFalse(envelope.isRefusal)
        XCTAssertNil(envelope.pendingHumanAction)
        XCTAssertEqual(envelope.warnings, [])
        let checks = try XCTUnwrap(envelope.data["checks"]?.arrayValue)
        XCTAssertGreaterThan(checks.count, 10)
        XCTAssertEqual(checks[0]["key"]?.stringValue, "interpreter.version")
        XCTAssertEqual(checks[0]["status"]?.stringValue, "ok")
        XCTAssertEqual(checks[0]["remedy"], .null)
        XCTAssertEqual(envelope.data["summary"]?["failing"]?.numberValue, 0)
        XCTAssertEqual(
            envelope.data["summary"]?["checked"]?.numberValue, Double(checks.count))
    }

    func testAGateRefusalDecodesWithWhatItShowed() throws {
        let envelope = try decoded("gate_refusal")
        XCTAssertEqual(envelope.verb, "profile.set")
        XCTAssertEqual(envelope.outcome, .blocked)
        XCTAssertFalse(envelope.outcome.succeeded)
        XCTAssertEqual(envelope.exitCode, 10)
        XCTAssertTrue(envelope.resumable)
        XCTAssertTrue(envelope.isRefusal)
        let cause = try XCTUnwrap(envelope.cause)
        XCTAssertEqual(cause.reason, "decision-required")
        XCTAssertEqual(cause.code, 10)
        XCTAssertEqual(cause.remediation.remedy, "answer-decision")
        XCTAssertEqual(cause.remediation.steps, [])
        XCTAssertNil(cause.remediation.doc)
        XCTAssertEqual(cause.scope, "run")
        XCTAssertTrue(cause.retryable)
        XCTAssertEqual(cause.origin, ["gates", "cli"])
        XCTAssertNil(cause.inner)
        XCTAssertEqual(cause.detail["gate"]?.stringValue, "profile.set.apply")
        XCTAssertEqual(cause.detail["options"], .array([.string("apply"), .string("abort")]))
        XCTAssertEqual(cause.detail["explicit"], .bool(false))
        XCTAssertEqual(cause.detail["run_id"]?.stringValue, envelope.runId)
        let shown = try XCTUnwrap(cause.shown)
        XCTAssertEqual(shown["profile"]?.stringValue, "slim")
        let items = try XCTUnwrap(shown["items"]?.arrayValue)
        XCTAssertEqual(shown["count"]?.numberValue, Double(items.count))
        XCTAssertEqual(items[0]["change"]?.stringValue, "off")
        XCTAssertNotNil(shown["digest"]?.stringValue)
    }

    func testARefusalWithStepsDecodesEveryStep() throws {
        let envelope = try decoded("refusal_with_steps")
        XCTAssertEqual(envelope.verb, "audit.coverage")
        XCTAssertEqual(envelope.outcome, .failed)
        XCTAssertEqual(envelope.exitCode, 27)
        let cause = try XCTUnwrap(envelope.cause)
        XCTAssertEqual(cause.reason, "governed-tree-absent")
        XCTAssertEqual(cause.remediation.steps.count, 2)
        XCTAssertNil(cause.remediation.remedy)
        XCTAssertTrue(cause.remediation.steps[0].hasPrefix("check that the export"))
        XCTAssertNil(cause.shown)
        XCTAssertEqual(cause.detail["tree"]?.stringValue, "genre_energy")
    }

    // MARK: what the decoder refuses or keeps

    /// The fixture as a mutable JSON object, to edit one key.
    private func edited(_ name: String, _ change: (inout [String: Any]) -> Void) throws -> Data {
        var object = try XCTUnwrap(
            JSONSerialization.jsonObject(with: try Fixtures.data(name)) as? [String: Any])
        change(&object)
        return try JSONSerialization.data(withJSONObject: object)
    }

    func testAnotherEnvelopeVersionIsRefusedByName() throws {
        let bytes = try edited("doctor") { $0["envelope"] = 2 }
        XCTAssertThrowsError(try Envelope.decode(bytes)) { error in
            XCTAssertEqual(error as? EnvelopeError, .unsupportedVersion(2))
        }
    }

    func testAMissingRequiredKeyIsMalformedNotDefaulted() throws {
        for key in ["cause", "pending_human_action", "outcome", "exit_code", "data", "warnings"] {
            let bytes = try edited("doctor") { $0.removeValue(forKey: key) }
            XCTAssertThrowsError(try Envelope.decode(bytes), key) { error in
                guard case .malformed = error as? EnvelopeError else {
                    return XCTFail("\(key): \(error)")
                }
            }
        }
    }

    func testAnOutcomeThisAppDoesNotKnowIsKept() throws {
        let bytes = try edited("doctor") { $0["outcome"] = "deferred" }
        let envelope = try Envelope.decode(bytes)
        XCTAssertEqual(envelope.outcome, .unknown("deferred"))
        XCTAssertEqual(envelope.outcome.rawValue, "deferred")
        XCTAssertFalse(envelope.outcome.succeeded)
    }

    func testEveryKnownOutcomeReadsAsItself() {
        for raw in ["ok", "no_op", "pending", "blocked", "failed", "cancelled"] {
            let outcome = Outcome(rawValue: raw)
            XCTAssertEqual(outcome.rawValue, raw)
            if case .unknown = outcome { XCTFail("\(raw) read as unknown") }
        }
        XCTAssertTrue(Outcome.noOp.succeeded)
    }

    func testAChainedCauseAndAPendingActionDecode() throws {
        let bytes = try edited("refusal_with_steps") { object in
            var cause = object["cause"] as! [String: Any]
            var inner = cause
            inner["reason"] = "library-export-unusable"
            inner["inner"] = NSNull()
            cause["inner"] = inner
            object["cause"] = cause
            object["outcome"] = "pending"
            object["pending_human_action"] = [
                "kind": "rekordbox_import", "id": "pha_run-fixture", "summary": "import the XML",
                "artifact": NSNull(), "steps": ["open rekordbox"], "verify_verb": "sync land",
                "blocks": ["sync land"], "expires": NSNull(),
            ] as [String: Any]
        }
        let envelope = try Envelope.decode(bytes)
        XCTAssertEqual(envelope.cause?.inner?.reason, "library-export-unusable")
        XCTAssertNil(envelope.cause?.inner?.inner)
        let pending = try XCTUnwrap(envelope.pendingHumanAction)
        XCTAssertEqual(pending.kind, "rekordbox_import")
        XCTAssertEqual(pending.verifyVerb, "sync land")
        XCTAssertEqual(pending.steps, ["open rekordbox"])
        XCTAssertEqual(pending.blocks, ["sync land"])
        XCTAssertNil(pending.artifact)
    }

    func testTrueAndFalseNeverReadAsNumbers() throws {
        let value = try JSONDecoder().decode(
            JSONValue.self, from: Data(#"{"a": true, "b": 1, "c": 0, "d": [null, "x", 1.5]}"#.utf8))
        XCTAssertEqual(value["a"], .bool(true))
        XCTAssertEqual(value["b"], .number(1))
        XCTAssertEqual(value["c"], .number(0))
        XCTAssertEqual(value["d"]?[0], .null)
        XCTAssertEqual(value["d"]?[1]?.stringValue, "x")
        XCTAssertEqual(value["d"]?[2]?.numberValue, 1.5)
        XCTAssertNil(value["d"]?[3])
    }
}
