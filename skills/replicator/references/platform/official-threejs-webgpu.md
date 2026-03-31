# Official Three.js WebGPU Validation

Use official Three.js documentation as the final check for browser-facing implementation choices.

Prioritize:

- `WebGPURenderer` docs and manual
- `TSL` docs
- official examples using the same renderer path or node features

Official sources:

- https://threejs.org/docs/pages/WebGPURenderer.html
- https://threejs.org/docs/TSL.html
- https://threejs.org/examples/?q=webgpu

## Validate These Points

- the renderer import and setup path
- whether the chosen programming model matches documented Three.js usage
- whether the intended fallback still uses an officially supported path
- whether any custom pipeline assumptions go beyond what official docs confirm

## Record These Notes

- which official pages confirmed the final approach
- which decisions are directly documented
- which decisions still rely on reasoned inference
