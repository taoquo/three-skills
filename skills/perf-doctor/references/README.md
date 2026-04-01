# Performance Doctor References

Use this reference pack for evidence-first, route-aware Three.js performance diagnosis.

## Suggested Order

1. [ecosystem-routes.md](ecosystem-routes.md)
2. [instrumentation.md](instrumentation.md)
3. [bottlenecks.md](bottlenecks.md)
4. [diagnosis-sequence.md](diagnosis-sequence.md)
5. [device-targets.md](device-targets.md)
6. [degradation-ladders.md](degradation-ladders.md)

## What Each File Does

- [ecosystem-routes.md](ecosystem-routes.md): identify which Three.js stack the app is actually using before suggesting fixes
- [instrumentation.md](instrumentation.md): decide what to measure before changing code
- [bottlenecks.md](bottlenecks.md): classify the hotspot cleanly
- [diagnosis-sequence.md](diagnosis-sequence.md): investigate in a fixed order
- [device-targets.md](device-targets.md): set a concrete performance contract
- [degradation-ladders.md](degradation-ladders.md): design quality tiers that preserve the important look
- [../assets/report-template.md](../assets/report-template.md): fixed output format for the final diagnosis

## Operating Principle

Do not prescribe optimization from instinct alone. Name the runtime surface, the evidence, the bottleneck class, and the lowest-risk fix to test first.
