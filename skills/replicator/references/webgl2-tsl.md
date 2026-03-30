# WebGL2 TSL Path

## Use This Path When

- the effect still fits TSL cleanly
- broader runtime stability matters more than using `WebGPU`
- the project benefits from mature WebGL-oriented Three.js patterns

## Implementation Notes

- Keep TSL as the shader authoring language.
- Use a backend path that clearly targets `WebGL2`.
- Keep post-processing intentional and short.
- Cap quality controls early so performance stays predictable.

## Risks

- the effect may not benefit from some newer renderer capabilities
- a direct port from raw GLSL can still drift into legacy-style code if not scoped carefully

## Report Expectations

Record:

- why `WebGL2` beat `WebGPU` for this task
- which modules are shared with a future `WebGPU` path
- whether any raw shader fallback was required
