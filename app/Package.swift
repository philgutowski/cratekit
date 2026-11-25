// swift-tools-version:5.9
//
// The Cratekit menu bar app (U965). SwiftPM alone, no Xcode project, so a
// cloud session writes it as text and the app workflow on a macOS runner
// builds, tests and bundles it. macOS 13 is the floor, the first with
// MenuBarExtra. The engine stays the authority: CrateEngine only runs crate
// verbs and decodes what they print.

import PackageDescription

let package = Package(
    name: "CratekitBar",
    platforms: [.macOS(.v13)],
    products: [
        .library(name: "CrateEngine", targets: ["CrateEngine"]),
        .executable(name: "CratekitBar", targets: ["CratekitBar"]),
    ],
    targets: [
        .target(name: "CrateEngine"),
        .executableTarget(name: "CratekitBar", dependencies: ["CrateEngine"]),
        .testTarget(
            name: "CrateEngineTests",
            dependencies: ["CrateEngine"],
            // Read beside the test file rather than as a resource bundle, and
            // written by tests/test_app_fixtures.py from the real verbs.
            exclude: ["Fixtures"]
        ),
    ]
)
