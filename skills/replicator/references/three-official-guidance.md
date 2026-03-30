# Three.js Official Guidance

Use official Three.js docs and manual pages as the final sanity check before you call a replication done.

Prioritize these official sources:

- `WebGPURenderer` docs and manual
  - https://threejs.org/docs/pages/WebGPURenderer.html
- `TSL` docs
  - https://threejs.org/docs/TSL.html
- official examples that use the same renderer path or node features
  - https://threejs.org/examples/?q=webgpu

## What To Validate

Before finalizing code, check:

- whether the chosen renderer import path matches current official guidance
- whether the TSL or node usage follows current documented patterns
- whether the fallback path still fits the officially supported backend model
- whether any custom post or render pipeline logic conflicts with the current docs

## Official Checks To Record

Record these in `REPORT.md`:

- Which official Three.js pages were used to validate the final approach
- Which specific renderer or TSL decisions were confirmed there
- Which parts still rely on inference rather than direct official confirmation

## Practical Rule

Use community examples, forum threads, and engine writeups to discover techniques.
Use official Three.js documentation to confirm the final browser-facing implementation.
