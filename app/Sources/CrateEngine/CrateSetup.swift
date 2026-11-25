import Foundation

/// Whether the app can run crate, read from the one path its settings hold.
///
/// Every state but `ready` is something the UI shows and the person fixes in
/// the settings, never a crash and never a search of a login shell's PATH.
public enum CrateSetup: Equatable, Sendable {
    /// No path is set.
    case unset
    /// The path is not absolute, so it would be resolved against a directory
    /// nobody chose.
    case notAbsolute(String)
    /// Nothing is at the path.
    case missing(String)
    /// A directory is at the path.
    case directory(String)
    /// A file is at the path that this account cannot execute.
    case notExecutable(String)
    /// An executable file is at the path.
    case ready(URL)

    /// Read the state of `path` from the file system.
    public static func check(_ path: String?, fileManager: FileManager = .default) -> CrateSetup {
        guard let path, !path.isEmpty else { return .unset }
        var isDirectory: ObjCBool = false
        guard fileManager.fileExists(atPath: path, isDirectory: &isDirectory) else {
            return .missing(path)
        }
        if isDirectory.boolValue { return .directory(path) }
        guard fileManager.isExecutableFile(atPath: path) else { return .notExecutable(path) }
        return .ready(URL(fileURLWithPath: path))
    }

    public var isReady: Bool {
        if case .ready = self { return true }
        return false
    }

    /// One line the menu can show.
    public var summary: String {
        switch self {
        case .unset: return "Set the path to crate in the settings"
        case .notAbsolute(let path): return "The crate path is not absolute: \(path)"
        case .missing(let path): return "Nothing is at the crate path: \(path)"
        case .directory(let path): return "The crate path is a folder: \(path)"
        case .notExecutable(let path): return "The crate path is not executable: \(path)"
        case .ready(let url): return "crate at \(url.path)"
        }
    }
}

/// Where the app keeps the path to crate.
public enum CrateSettings {
    /// The defaults key holding the absolute path to the crate executable.
    public static let cratePathKey = "cratePath"

    public static func cratePath(_ defaults: UserDefaults = .standard) -> String? {
        defaults.string(forKey: cratePathKey)
    }

    public static func setup(_ defaults: UserDefaults = .standard) -> CrateSetup {
        CrateSetup.check(cratePath(defaults))
    }
}
