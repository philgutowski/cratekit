import Foundation

/// The envelope fixtures beside this file, written by tests/test_app_fixtures.py
/// from the real verbs, so a decoder here is tested against what crate emits.
enum Fixtures {
    static let directory = URL(fileURLWithPath: #filePath)
        .deletingLastPathComponent()
        .appendingPathComponent("Fixtures", isDirectory: true)

    static func url(_ name: String) -> URL {
        directory.appendingPathComponent("\(name).json")
    }

    static func data(_ name: String) throws -> Data {
        try Data(contentsOf: url(name))
    }
}
