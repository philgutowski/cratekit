import AppKit
import Foundation
import XCTest

@testable import CrateEngine

/// What a status call comes to, the icon, the menu and the refresher, over
/// glances written here as JSON, so each case is the one shape it names.
final class StatusTests: XCTestCase {
    /// A glance with every source readable and nothing waiting, `attention`
    /// and any key replaced by `overrides`, each given as JSON text.
    static func glanceText(_ overrides: [String: String] = [:]) -> String {
        var keys: [String: String] = [
            "version": "1",
            "attention": "\"ok\"",
            "backup": """
                {"files": {"state": "known", "age_seconds": 90000, "completed_at": "2026-01-01T00:00:00+00:00"},
                 "database": {"state": "known", "age_seconds": 3600, "completed_at": "2026-01-01T00:00:00+00:00"}}
                """,
            "rekordbox": "\"closed\"",
            "jobs_running": "[]",
            "gates": "[]",
            "night": "null",
        ]
        for (key, value) in overrides { keys[key] = value }
        let members = keys.sorted { $0.key < $1.key }.map { "\"\($0.key)\": \($0.value)" }
        return "{" + members.joined(separator: ", ") + "}"
    }

    static func json(_ text: String) throws -> JSONValue {
        try JSONDecoder().decode(JSONValue.self, from: Data(text.utf8))
    }

    static func glance(_ overrides: [String: String] = [:]) throws -> Glance {
        try Glance.decode(try json(glanceText(overrides)))
    }

    /// The envelope `crate --output json status` prints around `glance`.
    static func envelope(glance: String, cause: String = "null", exitCode: Int = 0) -> Data {
        Data("""
            {"envelope": 1, "schema": "diagnostic/1", "verb": "status", "run_id": "run-x",
             "outcome": "ok", "exit_code": \(exitCode), "started": "2026-01-01T00:00:00+00:00",
             "ended": "2026-01-01T00:00:00+00:00", "pending_human_action": null, "cause": \(cause),
             "warnings": [], "resumable": false,
             "data": {"checks": [], "summary": {"open_runs": 0, "glance": \(glance)}}}
            """.utf8)
    }

    static let noon = Date(timeIntervalSince1970: 1_764_072_000)  // 2025-11-25 12:00 UTC

    private func outcome(_ data: Data, status: Int32 = 0, stderr: String = "") -> StatusOutcome {
        StatusOutcome(CrateRunner.read(data, status: status, stderr: stderr))
    }

    // MARK: the icon

    func testEachAttentionWordHasItsOwnIcon() throws {
        let words: [(String, StatusIcon)] = [
            ("ok", .ok), ("gate", .gate), ("running", .running),
            ("backup-due", .backupDue), ("fail", .fail),
        ]
        for (word, icon) in words {
            let glance = try Self.glance(["attention": "\"\(word)\""])
            XCTAssertEqual(StatusIcon(glance.attention), icon, word)
            let state = StatusState.initial.recording(.reading(glance), at: Self.noon)
            XCTAssertEqual(StatusIcon(state), icon, word)
        }
    }

    func testEveryIconIsADistinctShapeTheSystemDraws() {
        let names = StatusIcon.allCases.map(\.symbolName)
        XCTAssertEqual(Set(names).count, StatusIcon.allCases.count, "two states share a shape")
        for icon in StatusIcon.allCases {
            XCTAssertNotNil(
                NSImage(systemSymbolName: icon.symbolName, accessibilityDescription: nil),
                "\(icon.symbolName) is not a symbol on this system")
            XCTAssertFalse(icon.label.isEmpty)
        }
        XCTAssertEqual(Set(StatusIcon.allCases.map(\.label)).count, StatusIcon.allCases.count)
    }

    func testAnUnknownAttentionWordReadsFailNamingTheWord() throws {
        let glance = try Self.glance(["attention": "\"snoozed\""])
        XCTAssertEqual(glance.attention, .unknown("snoozed"))
        XCTAssertEqual(StatusIcon(glance.attention), .fail)
        let state = StatusState.initial.recording(.reading(glance), at: Self.noon)
        XCTAssertEqual(StatusIcon(state), .fail)
        let first = StatusMenu.lines(for: state)[0]
        XCTAssertEqual(first.kind, .problem)
        XCTAssertTrue(first.text.contains("\"snoozed\""), first.text)
        XCTAssertTrue(first.text.hasPrefix("fail"), first.text)
    }

    func testNothingReadYetIsItsOwnIconNotOk() {
        XCTAssertEqual(StatusIcon(StatusState.initial), .reading)
        XCTAssertEqual(StatusMenu.lines(for: StatusState.initial), [MenuLine(.heading, "Reading crate status")])
    }

    // MARK: decoding the glance

    func testAGlanceOfAnotherVersionIsRefusedByName() throws {
        XCTAssertThrowsError(try Self.glance(["version": "2", "attention": "\"calm\""])) { error in
            XCTAssertEqual(error as? GlanceError, .unsupportedVersion(2))
        }
    }

    func testEveryRequiredKeyIsRequired() throws {
        for key in ["version", "attention", "backup", "rekordbox", "jobs_running", "gates", "night"] {
            var value = try Self.json(Self.glanceText())
            guard case .object(var members) = value else { return XCTFail("not an object") }
            members.removeValue(forKey: key)
            value = .object(members)
            XCTAssertThrowsError(try Glance.decode(value), key) { error in
                XCTAssertEqual(error as? GlanceError, .missing("glance.\(key)"))
            }
        }
    }

    func testAPortionMissingItsAgeIsMalformedButANullAgeIsNone() throws {
        let missing = """
            {"files": {"state": "known", "completed_at": null},
             "database": {"state": "never-recorded", "age_seconds": null, "completed_at": null}}
            """
        XCTAssertThrowsError(try Self.glance(["backup": missing])) { error in
            XCTAssertEqual(error as? GlanceError, .missing("glance.backup.files.age_seconds"))
        }
        let nulls = """
            {"files": {"state": "never-recorded", "age_seconds": null, "completed_at": null},
             "database": {"state": "never-recorded", "age_seconds": null, "completed_at": null}}
            """
        let glance = try Self.glance(["backup": nulls])
        XCTAssertEqual(
            glance.backup,
            .value(BackupAges(
                files: BackupPortion(state: .neverRecorded, ageSeconds: nil, completedAt: nil),
                database: BackupPortion(state: .neverRecorded, ageSeconds: nil, completedAt: nil))))
    }

    func testAWrongTypeIsNamedByItsPath() throws {
        XCTAssertThrowsError(try Self.glance(["gates": "{\"run\": 1}"])) { error in
            XCTAssertEqual(error as? GlanceError, .wrongType(path: "glance.gates", expected: "an array"))
        }
        XCTAssertThrowsError(try Self.glance(["version": "1.5"])) { error in
            XCTAssertEqual(error as? GlanceError, .wrongType(path: "glance.version", expected: "an integer"))
        }
        XCTAssertThrowsError(try Self.glance(["rekordbox": "true"])) { error in
            XCTAssertEqual(error as? GlanceError, .wrongType(path: "glance.rekordbox", expected: "a string"))
        }
    }

    func testEachSourceCarriesItsUnreadableMessage() throws {
        let glance = try Self.glance([
            "attention": "\"fail\"",
            "backup": "{\"unreadable\": \"the volume is not there\"}",
            "rekordbox": "{\"unreadable\": \"OSError: no process table\"}",
            "jobs_running": "{\"unreadable\": \"DatabaseError: locked\"}",
            "gates": "{\"unreadable\": \"PermissionError: runs\"}",
            "night": "{\"unreadable\": \"JSONDecodeError: night\"}",
        ])
        XCTAssertEqual(glance.backup, .unreadable("the volume is not there"))
        XCTAssertEqual(glance.rekordbox, .unreadable("OSError: no process table"))
        XCTAssertEqual(glance.jobsRunning, .unreadable("DatabaseError: locked"))
        XCTAssertEqual(glance.gates, .unreadable("PermissionError: runs"))
        XCTAssertEqual(glance.night, .some(.unreadable("JSONDecodeError: night")))
        let lines = StatusMenu.readingLines(for: GoodReading(glance: glance, at: Self.noon))
        for message in [
            "the volume is not there", "OSError: no process table", "DatabaseError: locked",
            "PermissionError: runs", "JSONDecodeError: night",
        ] {
            let shown = lines.filter { $0.text.contains(message) }
            XCTAssertEqual(shown.count, 1, message)
            XCTAssertEqual(shown.first?.kind, .problem, message)
        }
    }

    // MARK: the menu

    func testTheMenuListsEachSourceInOrder() throws {
        let glance = try Self.glance([
            "attention": "\"gate\"",
            "rekordbox": "\"open\"",
            "jobs_running": "[{\"job_id\": \"j-1\", \"verb\": \"intake.tidal\", \"state\": \"running\"}]",
            "gates": """
                [{"run_id": "r-1", "verb": "intake.land", "gate": "intake.land.native",
                  "options": ["apply", "abort"], "explicit": true, "writes_database": true,
                  "since": "2025-11-22T12:00:00+00:00", "old": false},
                 {"run_id": "r-2", "verb": "profile.set", "gate": "profile.set.apply",
                  "options": [], "explicit": null, "writes_database": false,
                  "since": "2025-11-25T09:30:00+00:00", "old": true},
                 {"run_id": "r-3", "unreadable": "JSONDecodeError: Expecting value"}]
                """,
            "night": """
                {"outcome": "nothing", "line": "night of 2025-11-24: nothing new to land",
                 "gate_run": null, "pass_run": null, "staging": null}
                """,
        ])
        let texts = StatusMenu.readingLines(for: GoodReading(glance: glance, at: Self.noon)).map(\.text)
        XCTAssertEqual(texts, [
            "gate: a run is waiting for an answer",
            "Files backup: 1 day old",
            "Database backup: under a day old",
            "rekordbox: open",
            "Jobs running:",
            "intake.tidal, job j-1, running",
            "Gates waiting:",
            "intake.land at intake.land.native, waiting 3 days, writes the database",
            "profile.set at profile.set.apply, waiting 2 hours, writes no database, old",
            "Run r-3 could not be read: JSONDecodeError: Expecting value",
            "Night pass: night of 2025-11-24: nothing new to land",
        ])
        guard case .value(let items) = glance.gates, case .gate(let second) = items[1] else {
            return XCTFail("no second gate")
        }
        XCTAssertNil(second.explicit)
        XCTAssertEqual(second.options, [])
    }

    func testAQuietGlanceSaysNothingWaitsAndNoNightPass() throws {
        let texts = StatusMenu.readingLines(for: GoodReading(glance: try Self.glance(), at: Self.noon))
            .map(\.text)
        XCTAssertEqual(texts, [
            "ok: nothing unreadable, no gate, no job running, both backups under five days",
            "Files backup: 1 day old",
            "Database backup: under a day old",
            "rekordbox: closed",
            "No job running",
            "No gate waiting",
            "Night pass: none recorded",
        ])
    }

    func testBackupAgesAreWholeDaysAndTheirStatesAreSaid() {
        XCTAssertEqual(StatusMenu.days(0), "under a day")
        XCTAssertEqual(StatusMenu.days(86_399), "under a day")
        XCTAssertEqual(StatusMenu.days(86_400), "1 day")
        XCTAssertEqual(StatusMenu.days(5 * 86_400 - 1), "4 days")
        XCTAssertEqual(StatusMenu.days(5 * 86_400), "5 days")
        let future = BackupPortion(
            state: .recordedInTheFuture, ageSeconds: nil, completedAt: "2030-01-01T00:00:00+00:00")
        XCTAssertEqual(
            StatusMenu.portionLine("Files backup", future),
            MenuLine(.problem, "Files backup: recorded ahead of now, at 2030-01-01T00:00:00+00:00"))
        let never = BackupPortion(state: .neverRecorded, ageSeconds: nil, completedAt: nil)
        XCTAssertEqual(
            StatusMenu.portionLine("Database backup", never),
            MenuLine(.item, "Database backup: never recorded"))
    }

    func testRekordboxUnknownIsNeverReadAsClosed() {
        XCTAssertEqual(
            StatusMenu.rekordboxLine(.value(.unknown)).text,
            "rekordbox: unknown, the scan could not confirm it is closed")
    }

    // MARK: a status call

    func testAGoodCallReadsTheGlance() throws {
        let read = outcome(Self.envelope(glance: Self.glanceText(["attention": "\"running\""])))
        guard case .reading(let glance) = read else { return XCTFail("\(read)") }
        XCTAssertEqual(glance.attention, .running)
    }

    func testEachFailedCallIsAFailureWithItsMessage() throws {
        let refusal = """
            {"reason": "config-missing", "code": 3, "message": "no config at the path",
             "remediation": {"remedy": null, "steps": [], "doc": null}, "scope": "run",
             "retryable": false, "origin": ["cli"], "detail": {}}
            """
        let cases: [(StatusOutcome, StatusFailure, String)] = [
            (StatusOutcome(.setup(.unset)), .setup(.unset), "Set the path to crate"),
            (StatusOutcome(.launchFailed("denied")), .launchFailed("denied"), "denied"),
            (StatusOutcome(.timedOut(after: 30, stderr: "slow\n")), .timedOut(after: 30, stderr: "slow\n"),
             "within 30 seconds: slow"),
            (StatusOutcome(.signalled(9, stderr: "")), .signalled(9, stderr: ""), "signal 9"),
            (outcome(Data("Traceback (most recent call last)".utf8), status: 1),
             .undecodable(
                status: 1, reason: "", firstBytes: "Traceback (most recent call last)", stderr: ""),
             "Traceback (most recent call last)"),
            (outcome(Self.envelope(glance: "null", cause: refusal, exitCode: 3), status: 3),
             .refused(reason: "config-missing", message: "no config at the path"),
             "no config at the path"),
            (outcome(Self.envelope(glance: Self.glanceText()), status: 2, stderr: "boom\nhere"),
             .exitStatus(2, stderr: "boom\nhere"), "status 2: boom here"),
            (outcome(Self.envelope(glance: Self.glanceText(["version": "7"]))),
             .glance(.unsupportedVersion(7)), "version 7"),
        ]
        for (found, failure, words) in cases {
            guard case .failure(let failed) = found else {
                XCTFail("\(found) is not a failure"); continue
            }
            if case .undecodable = failure, case .undecodable(let status, _, let first, _) = failed {
                // The decoder's own reason is the platform's text; the bytes are ours.
                XCTAssertEqual(first, "Traceback (most recent call last)")
                XCTAssertEqual(status, 1)
            } else {
                XCTAssertEqual(failed, failure)
            }
            XCTAssertTrue(failed.message.contains(words), "\(failed.message) lacks \(words)")
        }
    }

    func testAnEnvelopeWithNoGlanceIsAFailureNotAQuietMenu() {
        let read = outcome(Self.envelope(glance: "null"))
        XCTAssertEqual(
            read, .failure(.glance(.wrongType(path: "data.summary.glance", expected: "an object"))))
    }

    func testAFailedCallKeepsTheLastReadingLabelledWithItsTime() throws {
        let utc = try XCTUnwrap(TimeZone(identifier: "UTC"))
        let good = try Self.glance(["attention": "\"gate\""])
        let later = Self.noon.addingTimeInterval(120)
        let state = StatusState.initial
            .recording(.reading(good), at: Self.noon)
            .recording(.failure(.timedOut(after: 30, stderr: "")), at: later)
        XCTAssertNil(state.current, "the last reading is never current after a failed call")
        XCTAssertEqual(state.lastGood, GoodReading(glance: good, at: Self.noon))
        XCTAssertEqual(StatusIcon(state), .fail, "the icon never shows the last reading's word")
        let lines = StatusMenu.lines(for: state, timeZone: utc)
        XCTAssertEqual(lines[0], MenuLine(.problem, "Status could not be read: crate status did not answer within 30 seconds"))
        XCTAssertEqual(lines[1], MenuLine(.item, "Failed at 2025-11-25 12:02"))
        XCTAssertEqual(lines[2], MenuLine(.heading, "Last good reading, at 2025-11-25 12:00:"))
        XCTAssertEqual(Array(lines[3...]), StatusMenu.readingLines(for: GoodReading(glance: good, at: Self.noon)))

        let recovered = state.recording(.reading(try Self.glance()), at: later)
        XCTAssertNil(recovered.failure)
        XCTAssertEqual(StatusIcon(recovered), .ok)
    }

    func testAFailureBeforeAnyGoodReadingSaysSo() {
        let state = StatusState.initial.recording(.failure(.setup(.unset)), at: Self.noon)
        let texts = StatusMenu.lines(for: state, timeZone: TimeZone(identifier: "UTC")!).map(\.text)
        XCTAssertEqual(texts, [
            "Status could not be read: Set the path to crate in the settings",
            "Failed at 2025-11-25 12:00",
            "No good reading yet",
        ])
        XCTAssertEqual(StatusIcon(state), .fail)
    }

    func testACrashBeforeTheEnvelopeShowsTheEndOfWhatCrateSaid() {
        let trace = "Traceback (most recent call last):\n" + String(repeating: "  File x, line 1\n", count: 40)
            + "ModuleNotFoundError: No module named 'cratekit.cli'\n"
        let read = outcome(Data(), status: 1, stderr: trace)
        guard case .failure(let failed) = read else { return XCTFail("\(read)") }
        XCTAssertTrue(failed.message.contains("exiting with status 1"), failed.message)
        XCTAssertTrue(
            failed.message.hasSuffix("ModuleNotFoundError: No module named 'cratekit.cli'"), failed.message)
        XCTAssertFalse(failed.message.contains("Traceback"), "the start is dropped, not the end")
    }

    func testTheCurrentReadingSaysWhenItWasRead() throws {
        let utc = try XCTUnwrap(TimeZone(identifier: "UTC"))
        let reading = GoodReading(glance: try Self.glance(), at: Self.noon)
        let state = StatusState.initial.recording(.reading(reading.glance), at: Self.noon)
        let lines = StatusMenu.lines(for: state, timeZone: utc)
        XCTAssertEqual(lines.last, MenuLine(.item, "Read at 2025-11-25 12:00"))
        XCTAssertEqual(Array(lines.dropLast()), StatusMenu.readingLines(for: reading))
    }

    func testAKeyThisAppDoesNotKnowIsSaidWhenItCouldNotBeRead() throws {
        let glance = try Self.glance([
            "attention": "\"fail\"",
            "library_volume": "{\"unreadable\": \"the volume did not answer\"}",
            "playlists": "[]",
        ])
        XCTAssertEqual(glance.otherUnreadable, ["library_volume": "the volume did not answer"])
        let lines = StatusMenu.readingLines(for: GoodReading(glance: glance, at: Self.noon))
        XCTAssertEqual(lines.last, MenuLine(.problem, "library_volume could not be read: the volume did not answer"))
        XCTAssertFalse(lines.contains { $0.text.contains("playlists") })
    }

    func testAStateThisAppDoesNotKnowIsMarkedNotShownAsFact() throws {
        let glance = try Self.glance([
            "rekordbox": "\"sleeping\"",
            "backup": """
                {"files": {"state": "partial", "age_seconds": 172800, "completed_at": null},
                 "database": {"state": "known", "age_seconds": 3600, "completed_at": null}}
                """,
        ])
        let lines = StatusMenu.readingLines(for: GoodReading(glance: glance, at: Self.noon))
        XCTAssertTrue(lines.contains(MenuLine(
            .problem, "rekordbox: \"sleeping\", a state this app does not know")), "\(lines)")
        XCTAssertTrue(lines.contains(MenuLine(
            .problem, "Files backup: \"partial\", a state this app does not know, 2 days old")), "\(lines)")
    }

    // MARK: the refresher

    func testOverlappingRefreshesRunOneCall() async throws {
        let calls = Counter()
        let body = Self.envelope(glance: Self.glanceText())
        let refresher = StatusRefresher(run: { call in
            await calls.add(call)
            try? await Task.sleep(nanoseconds: 300_000_000)
            return CrateRunner.read(body, status: 0, stderr: "")
        })
        async let first = refresher.refresh()
        async let second = refresher.refresh()
        async let third = refresher.refresh()
        let states = await [first, second, third]
        let started = await refresher.callsStarted
        XCTAssertEqual(started, 1)
        let seen = await calls.calls
        XCTAssertEqual(seen, [StatusRefresher.call])
        XCTAssertEqual(Set(states.map { StatusIcon($0) }), [.ok])

        await refresher.refresh()
        let afterwards = await refresher.callsStarted
        XCTAssertEqual(afterwards, 2, "a refresh after the call ended starts the next")
    }

    func testTheRefresherRunsStatusAloneWithATimeout() {
        XCTAssertEqual(StatusRefresher.call.arguments, ["status"])
        XCTAssertEqual(CrateRunner.arguments(for: StatusRefresher.call), ["--output", "json", "status"])
        XCTAssertLessThan(StatusRefresher.call.timeout, StatusRefresher.interval)
        XCTAssertEqual(StatusRefresher.interval, 60)
    }

    func testTheRefresherKeepsTheLastReadingThroughAFailure() async {
        let answers = Answers([
            .envelope(
                try! Envelope.decode(Self.envelope(glance: Self.glanceText(["attention": "\"backup-due\""]))),
                status: 0, stderr: ""),
            .timedOut(after: 30, stderr: ""),
        ])
        let clock = Clock(start: Self.noon)
        let refresher = StatusRefresher(run: { _ in await answers.next() }, clock: { clock.tick() })
        let first = await refresher.refresh()
        XCTAssertEqual(StatusIcon(first), .backupDue)
        let second = await refresher.refresh()
        XCTAssertEqual(StatusIcon(second), .fail)
        XCTAssertEqual(second.failure, .timedOut(after: 30, stderr: ""))
        XCTAssertEqual(second.lastGood?.at, Self.noon)
        XCTAssertEqual(second.failedAt, Self.noon.addingTimeInterval(60))
    }
}

private actor Counter {
    private(set) var calls: [VerbCall] = []
    func add(_ call: VerbCall) { calls.append(call) }
}

private actor Answers {
    private var queued: [VerbResult]
    init(_ queued: [VerbResult]) { self.queued = queued }
    func next() -> VerbResult { queued.removeFirst() }
}

/// A clock that moves a minute each time it is read.
private final class Clock: @unchecked Sendable {
    private let lock = NSLock()
    private var now: Date
    init(start: Date) { now = start }
    func tick() -> Date {
        lock.lock()
        defer { lock.unlock() }
        let read = now
        now = now.addingTimeInterval(60)
        return read
    }
}
