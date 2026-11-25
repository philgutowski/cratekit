import Foundation

/// Reads `crate status` for the menu, at most one call at a time.
///
/// A refresh asked for while a call runs joins that call rather than starting
/// another, so a minute's tick and the menu opening never stack two verbs.
/// The only verb it runs is `crate status`: the app reads in this card.
public actor StatusRefresher {
    /// Runs one verb; the live app's runs crate, a test's a fake.
    public typealias Run = @Sendable (VerbCall) async -> VerbResult

    /// The one call this refresher makes.
    public static let call = VerbCall(["status"], timeout: 30)
    /// How often the app refreshes on its own, besides when the menu opens.
    public static let interval: TimeInterval = 60

    private let run: Run
    private let clock: @Sendable () -> Date
    private var inFlight: Task<StatusState, Never>?

    /// What the app knows after the last call that finished.
    public private(set) var state = StatusState.initial
    /// How many calls this refresher has started.
    public private(set) var callsStarted = 0

    public init(run: @escaping Run, clock: @escaping @Sendable () -> Date = { Date() }) {
        self.run = run
        self.clock = clock
    }

    /// A refresher that runs crate at the path the settings hold when each
    /// call starts, so a path set while the app runs is used at the next.
    public static func live() -> StatusRefresher {
        StatusRefresher(run: { call in
            await CrateRunner(path: CrateSettings.cratePath()).run(call)
        })
    }

    /// Read status once, or wait for the call already running, and return
    /// what the app knows when it ends.
    @discardableResult
    public func refresh() async -> StatusState {
        if let running = inFlight {
            return await running.value
        }
        callsStarted += 1
        // Made on this actor, so the state is recorded here, once per call,
        // however many refreshes wait on it.
        let task = Task { () -> StatusState in
            let result = await self.run(Self.call)
            let next = self.state.recording(StatusOutcome(result), at: self.clock())
            self.state = next
            self.inFlight = nil
            return next
        }
        inFlight = task
        return await task.value
    }
}
