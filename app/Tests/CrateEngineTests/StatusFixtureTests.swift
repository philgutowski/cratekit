import Foundation
import XCTest

@testable import CrateEngine

/// The status path over envelopes `crate status` really emits: one fixture
/// per `attention` word, each written by tests/test_app_fixtures.py from the
/// real verb over the setups tests/test_status_glance.py uses, read at a held
/// clock so ages and waits are fixed.
final class StatusFixtureTests: XCTestCase {
    static let words: [(fixture: String, attention: Attention, icon: StatusIcon)] = [
        ("status_ok", .ok, .ok),
        ("status_gate", .gate, .gate),
        ("status_running", .running, .running),
        ("status_backup_due", .backupDue, .backupDue),
        ("status_fail", .fail, .fail),
    ]

    /// The fixtures' held clock, 2026-01-01 12:00 UTC.
    static let heldNow = Date(timeIntervalSince1970: 1_767_268_800)

    private func glance(_ name: String) throws -> Glance {
        let read = StatusOutcome(CrateRunner.read(try Fixtures.data(name), status: 0, stderr: ""))
        guard case .reading(let glance) = read else {
            XCTFail("\(name) did not read as a glance: \(read)")
            throw GlanceError.missing(name)
        }
        return glance
    }

    private func texts(_ name: String) throws -> [String] {
        StatusMenu.readingLines(for: GoodReading(glance: try glance(name), at: Self.heldNow)).map(\.text)
    }

    func testEveryStatusFixtureIsListedHere() throws {
        let found = try FileManager.default.contentsOfDirectory(atPath: Fixtures.directory.path)
            .filter { $0.hasPrefix("status_") && $0.hasSuffix(".json") }
            .map { String($0.dropLast(".json".count)) }
        XCTAssertEqual(Set(found), Set(Self.words.map { $0.fixture }))
    }

    func testEachAttentionFixtureMapsToItsIcon() throws {
        for (fixture, attention, icon) in Self.words {
            let read = try glance(fixture)
            XCTAssertEqual(read.version, supportedGlanceVersion, fixture)
            XCTAssertEqual(read.attention, attention, fixture)
            let state = StatusState.initial.recording(.reading(read), at: Self.heldNow)
            XCTAssertEqual(StatusIcon(state), icon, fixture)
        }
    }

    func testTheQuietFixtureShowsBothAgesAndNothingWaiting() throws {
        XCTAssertEqual(try texts("status_ok"), [
            "ok: nothing unreadable, no gate, no job running, both backups under five days",
            "Files backup: 1 day old",
            "Database backup: 2 days old",
            "rekordbox: closed",
            "No job running",
            "No gate waiting",
            "Night pass: none recorded",
        ])
    }

    func testTheGateFixtureListsEachGateItsAgeItsWriteAndTheOldOne() throws {
        let read = try glance("status_gate")
        guard case .value(let items) = read.gates else { return XCTFail("gates unreadable") }
        XCTAssertEqual(items.count, 2)
        guard case .gate(let landing) = items[0], case .gate(let profile) = items[1] else {
            return XCTFail("\(items)")
        }
        XCTAssertEqual(landing.runId, "run-fixture-landing")
        XCTAssertEqual(landing.options, ["apply", "abort"])
        XCTAssertEqual(landing.explicit, true)
        XCTAssertTrue(landing.writesDatabase)
        XCTAssertFalse(landing.old)
        XCTAssertEqual(profile.runId, "run-fixture-profile")
        XCTAssertFalse(profile.writesDatabase)
        XCTAssertTrue(profile.old)
        let night = try XCTUnwrap(read.night)
        guard case .value(let pass) = night else { return XCTFail("night unreadable") }
        XCTAssertEqual(pass.outcome, "waiting-at-gate")
        XCTAssertEqual(pass.gateRun, "run-fixture-landing")
        let shown = try texts("status_gate")
        XCTAssertTrue(shown.contains(
            "intake.land at intake.land.native, waiting 3 hours, writes the database"), "\(shown)")
        XCTAssertTrue(shown.contains { $0.hasPrefix("profile.set at profile.set.apply, waiting ")
            && $0.hasSuffix(", writes no database, old") }, "\(shown)")
        XCTAssertTrue(shown.contains("Night pass: \(pass.line)"), "\(shown)")
    }

    func testTheRunningFixtureListsTheJobAndAnOpenRekordbox() throws {
        let read = try glance("status_running")
        XCTAssertEqual(
            read.jobsRunning,
            .value([RunningJob(jobId: "job-fixture-running", verb: "intake.tidal", state: "running")]))
        XCTAssertEqual(read.rekordbox, .value(.open))
        let shown = try texts("status_running")
        XCTAssertTrue(shown.contains("intake.tidal, job job-fixture-running, running"), "\(shown)")
        XCTAssertTrue(shown.contains("rekordbox: open"), "\(shown)")
    }

    func testTheBackupDueFixtureSaysEachPortionsAgeAndState() throws {
        let read = try glance("status_backup_due")
        guard case .value(let ages) = read.backup else { return XCTFail("backup unreadable") }
        XCTAssertEqual(ages.files.state, .known)
        XCTAssertEqual(ages.files.ageSeconds, 9 * 86_400)
        XCTAssertEqual(ages.database, BackupPortion(state: .neverRecorded, ageSeconds: nil, completedAt: nil))
        XCTAssertEqual(read.rekordbox, .value(.unknown))
        let shown = try texts("status_backup_due")
        XCTAssertEqual(Array(shown.prefix(4)), [
            "backup-due: a backup is five days old, or its age is unknown",
            "Files backup: 9 days old",
            "Database backup: never recorded",
            "rekordbox: unknown, the scan could not confirm it is closed",
        ])
    }

    func testTheFailFixtureShowsEachUnreadableSourceWithItsMessage() throws {
        let read = try glance("status_fail")
        guard case .unreadable(let rekordbox) = read.rekordbox else {
            return XCTFail("rekordbox read as \(read.rekordbox)")
        }
        XCTAssertEqual(rekordbox, "RuntimeError: the process table could not be read")
        guard case .value(let ages) = read.backup else { return XCTFail("backup unreadable") }
        XCTAssertEqual(ages.database.state, .recordedInTheFuture)
        guard case .value(let items) = read.gates else { return XCTFail("gates unreadable") }
        let damaged = items.compactMap { item -> (String, String)? in
            if case .unreadable(let runId, let message) = item { return (runId, message) }
            return nil
        }
        XCTAssertEqual(damaged.map(\.0), ["run-fixture-damaged"])
        let night = try XCTUnwrap(read.night)
        guard case .unreadable(let nightMessage) = night else { return XCTFail("night read") }

        let lines = StatusMenu.readingLines(for: GoodReading(glance: read, at: Self.heldNow))
        let problems = lines.filter { $0.kind == .problem }.map(\.text)
        XCTAssertTrue(problems.contains("rekordbox could not be checked: \(rekordbox)"), "\(problems)")
        XCTAssertTrue(
            problems.contains("Run run-fixture-damaged could not be read: \(damaged[0].1)"), "\(problems)")
        XCTAssertTrue(problems.contains("Night pass could not be read: \(nightMessage)"), "\(problems)")
        XCTAssertTrue(
            problems.contains { $0.hasPrefix("Database backup: recorded ahead of now") }, "\(problems)")
    }
}
