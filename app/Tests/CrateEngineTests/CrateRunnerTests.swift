import Foundation
import XCTest

@testable import CrateEngine

/// The runner over small fake `crate` executables in a temporary directory.
/// The fakes are shell scripts; the runner itself never starts a shell.
final class CrateRunnerTests: XCTestCase {
    private var folder: URL!

    override func setUpWithError() throws {
        folder = FileManager.default.temporaryDirectory
            .appendingPathComponent("crate-runner-\(UUID().uuidString)", isDirectory: true)
        try FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
    }

    override func tearDownWithError() throws {
        try? FileManager.default.removeItem(at: folder)
    }

    /// A fake crate whose body is `script`, executable unless told otherwise.
    private func fake(_ script: String, executable: Bool = true) throws -> String {
        let path = folder.appendingPathComponent("crate").path
        try ("#!/bin/sh\n" + script + "\n").write(toFile: path, atomically: true, encoding: .utf8)
        let mode: Int16 = executable ? 0o755 : 0o644
        try FileManager.default.setAttributes([.posixPermissions: mode], ofItemAtPath: path)
        return path
    }

    /// Fail unless the process whose pid the fake wrote to `pidFile` is gone.
    private func assertEnded(
        _ pidFile: URL, file: StaticString = #filePath, line: UInt = #line
    ) throws {
        let text = try String(contentsOf: pidFile, encoding: .utf8)
            .trimmingCharacters(in: .whitespacesAndNewlines)
        let pid = try XCTUnwrap(pid_t(text), "no pid in \(text)", file: file, line: line)
        errno = 0
        XCTAssertEqual(kill(pid, 0), -1, "the verb is still running", file: file, line: line)
        XCTAssertEqual(errno, ESRCH, file: file, line: line)
    }

    private func envelopeText(_ name: String) throws -> String {
        try String(contentsOf: Fixtures.url(name), encoding: .utf8)
    }

    // MARK: setup states

    func testNoPathIsTheUnsetState() {
        XCTAssertEqual(CrateRunner(path: nil).runBlocking(VerbCall(["doctor"])), .setup(.unset))
        XCTAssertEqual(CrateRunner(path: "").runBlocking(VerbCall(["doctor"])), .setup(.unset))
    }

    func testAMissingPathIsTheSetupStateNotACrash() {
        let path = folder.appendingPathComponent("nowhere/crate").path
        XCTAssertEqual(CrateRunner(path: path).runBlocking(VerbCall(["doctor"])), .setup(.missing(path)))
    }

    func testANonExecutablePathIsTheSetupState() throws {
        let path = try fake("echo '{}'", executable: false)
        XCTAssertEqual(
            CrateRunner(path: path).runBlocking(VerbCall(["doctor"])), .setup(.notExecutable(path)))
    }

    func testARelativePathIsRefusedRatherThanSearched() {
        XCTAssertEqual(
            CrateRunner(path: "crate").runBlocking(VerbCall(["doctor"])),
            .setup(.notAbsolute("crate")))
    }

    func testADirectoryIsTheSetupState() {
        XCTAssertEqual(CrateSetup.check(folder.path), .directory(folder.path))
    }

    func testAnExecutableFileIsReady() throws {
        let path = try fake("exit 0")
        XCTAssertEqual(CrateSetup.check(path), .ready(URL(fileURLWithPath: path)))
        XCTAssertTrue(CrateSetup.check(path).isReady)
    }

    // MARK: running

    func testAnEnvelopeOnStdoutIsDecoded() throws {
        let doctor = folder.appendingPathComponent("doctor.json")
        try envelopeText("doctor").write(to: doctor, atomically: true, encoding: .utf8)
        let path = try fake("cat '\(doctor.path)'")
        guard case .envelope(let envelope, let status, _) = CrateRunner(path: path)
            .runBlocking(VerbCall(["doctor"]))
        else { return XCTFail("no envelope") }
        XCTAssertEqual(status, 0)
        XCTAssertEqual(envelope.verb, "doctor")
        XCTAssertEqual(envelope.outcome, .ok)
    }

    func testARefusalWithANonZeroStatusIsAValueNotAFailure() throws {
        let gate = folder.appendingPathComponent("gate.json")
        try envelopeText("gate_refusal").write(to: gate, atomically: true, encoding: .utf8)
        let path = try fake("cat '\(gate.path)'\necho 'a gate is waiting' >&2\nexit 10")
        guard case .envelope(let envelope, let status, let stderr) = CrateRunner(path: path)
            .runBlocking(VerbCall(["profile", "set", "slim"]))
        else { return XCTFail("the refusal was not read as an envelope") }
        XCTAssertEqual(status, 10)
        XCTAssertTrue(envelope.isRefusal)
        XCTAssertEqual(envelope.cause?.reason, "decision-required")
        XCTAssertNotNil(envelope.cause?.shown)
        XCTAssertEqual(stderr, "a gate is waiting\n")
    }

    func testTheArgumentsAreFixedAndNeverReadByAShell() throws {
        let seen = folder.appendingPathComponent("argv")
        let path = try fake("for a in \"$@\"; do printf '%s\\n' \"$a\"; done > '\(seen.path)'")
        let hostile = "x; touch '\(folder.appendingPathComponent("pwned").path)'"
        _ = CrateRunner(path: path).runBlocking(VerbCall(["status", hostile, "$HOME"]))
        let argv = try String(contentsOf: seen, encoding: .utf8)
        XCTAssertEqual(argv, "--output\njson\nstatus\n\(hostile)\n$HOME\n")
        XCTAssertFalse(
            FileManager.default.fileExists(atPath: folder.appendingPathComponent("pwned").path))
        XCTAssertEqual(
            CrateRunner.arguments(for: VerbCall(["doctor"])), ["--output", "json", "doctor"])
    }

    func testTheEnvironmentIsMinimal() throws {
        let seen = folder.appendingPathComponent("env")
        let path = try fake("/usr/bin/env > '\(seen.path)'")
        let given = [
            "HOME": "/home-for-test", "LANG": "en_GB.UTF-8", "PATH": "/opt/login-shell/bin",
            "SECRET_TOKEN": "nope", "PYTHONPATH": "/elsewhere",
        ]
        _ = CrateRunner(path: path, environment: given).runBlocking(VerbCall(["doctor"]))
        let lines = try String(contentsOf: seen, encoding: .utf8).split(separator: "\n")
        var env: [String: String] = [:]
        for line in lines {
            let parts = line.split(separator: "=", maxSplits: 1).map(String.init)
            if parts.count == 2 { env[parts[0]] = parts[1] }
        }
        XCTAssertEqual(env["HOME"], "/home-for-test")
        XCTAssertEqual(env["LANG"], "en_GB.UTF-8")
        XCTAssertEqual(env["PATH"], folder.path + ":" + CrateEnvironment.systemPath)
        XCTAssertNil(env["SECRET_TOKEN"])
        XCTAssertNil(env["PYTHONPATH"])
        let allowed = Set(CrateEnvironment.passedKeys + ["PATH"])
        // The shell a fake runs in adds PWD, SHLVL and _ of its own, and
        // macOS's frameworks add their text encoding key to every process.
        let added = Set(env.keys).subtracting(allowed)
            .subtracting(["PWD", "SHLVL", "_", "OLDPWD"])
            .filter { !$0.hasPrefix("__CF") }
        XCTAssertEqual(added, [], "the environment carried \(added)")
    }

    func testTheEnvironmentFillsHomeAndLanguageWhenTheAppHasNone() {
        let made = CrateEnvironment.minimal(for: URL(fileURLWithPath: "/opt/crate/bin/crate"), from: [:])
        XCTAssertEqual(made["PATH"], "/opt/crate/bin:" + CrateEnvironment.systemPath)
        XCTAssertNotNil(made["HOME"])
        XCTAssertEqual(made["LANG"], "en_US.UTF-8")
        XCTAssertEqual(Set(made.keys), ["HOME", "LANG", "PATH"])
    }

    func testAVerbPastItsTimeoutIsEndedAndReported() throws {
        let pidFile = folder.appendingPathComponent("pid")
        let path = try fake("echo $$ > '\(pidFile.path)'\necho started >&2\nexec sleep 30")
        let began = Date()
        let result = CrateRunner(path: path).runBlocking(VerbCall(["sync", "land"], timeout: 0.5))
        let took = Date().timeIntervalSince(began)
        guard case .timedOut(let after, let stderr) = result else {
            return XCTFail("not reported as timed out: \(result)")
        }
        XCTAssertEqual(after, 0.5)
        XCTAssertEqual(stderr, "started\n")
        XCTAssertLessThan(took, 10, "the verb was not ended")
        try assertEnded(pidFile)
    }

    func testAVerbThatIgnoresTerminateIsKilled() throws {
        let pidFile = folder.appendingPathComponent("pid")
        let path = try fake("echo $$ > '\(pidFile.path)'\ntrap '' TERM\nwhile :; do sleep 1; done")
        let began = Date()
        let result = CrateRunner(path: path).runBlocking(VerbCall(["doctor"], timeout: 0.3))
        guard case .timedOut = result else { return XCTFail("not reported as timed out: \(result)") }
        XCTAssertLessThan(Date().timeIntervalSince(began), 15, "the verb was not killed")
        try assertEnded(pidFile)
    }

    func testUndecodableOutputIsReportedWithItsFirstBytes() throws {
        let path = try fake("echo 'Traceback (most recent call last):'\nexit 1")
        guard case .undecodable(let status, let first, _, _) = CrateRunner(path: path)
            .runBlocking(VerbCall(["doctor"]))
        else { return XCTFail("undecodable output was not reported") }
        XCTAssertEqual(status, 1)
        XCTAssertEqual(first, "Traceback (most recent call last):\n")
    }

    func testEmptyOutputIsReportedNeverAnEmptyResult() throws {
        let path = try fake("echo 'crashed' >&2\nexit 2")
        guard case .undecodable(let status, let first, let reason, let stderr) = CrateRunner(path: path)
            .runBlocking(VerbCall(["doctor"]))
        else { return XCTFail("empty output was not reported") }
        XCTAssertEqual(status, 2)
        XCTAssertEqual(first, "")
        XCTAssertEqual(reason, "standard output held no envelope")
        XCTAssertEqual(stderr, "crashed\n")
    }

    func testTheFirstBytesAreCappedAtTheLimit() {
        let long = Data(repeating: UInt8(ascii: "x"), count: CrateRunner.firstBytesLimit * 4)
        guard case .undecodable(_, let first, _, _) = CrateRunner.read(long, status: 0, stderr: "")
        else { return XCTFail("not undecodable") }
        XCTAssertEqual(first.count, CrateRunner.firstBytesLimit)
    }

    func testAnotherEnvelopeVersionIsReportedByItsNumber() throws {
        let text = try envelopeText("doctor").replacingOccurrences(
            of: "\"envelope\": 1,", with: "\"envelope\": 2,")
        guard case .undecodable(_, _, let reason, _) = CrateRunner.read(
            Data(text.utf8), status: 0, stderr: "")
        else { return XCTFail("a version 2 frame was read") }
        XCTAssertEqual(reason, "envelope version 2 is not 1")
    }

    func testOutputLargerThanAPipeBufferIsReadWhole() throws {
        // More than a pipe holds, so a runner that waits before it reads deadlocks.
        let doctor = folder.appendingPathComponent("doctor.json")
        try envelopeText("doctor").write(to: doctor, atomically: true, encoding: .utf8)
        let path = try fake("i=0; while [ $i -lt 400 ]; do printf '%0256d' 0 >&2; i=$((i+1)); done\ncat '\(doctor.path)'")
        guard case .envelope(_, _, let stderr) = CrateRunner(path: path)
            .runBlocking(VerbCall(["doctor"], timeout: 20))
        else { return XCTFail("a large stderr stopped the envelope being read") }
        XCTAssertEqual(stderr.count, 400 * 256)
    }

    func testTheAsyncRunGivesTheSameResult() async throws {
        let path = try fake("exit 3")
        let result = await CrateRunner(path: path).run(VerbCall(["doctor"]))
        XCTAssertEqual(
            result,
            .undecodable(status: 3, firstBytes: "", reason: "standard output held no envelope", stderr: ""))
    }
}
