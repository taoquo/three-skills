# Official Three.js PostFX Validation

Use official Three.js docs and examples as the final check for post-processing implementation choices.

Prioritize:

- examples that use the same renderer path
- official docs or manual pages for the relevant render targets, passes, and post APIs

Useful starting points:

- https://threejs.org/examples/?q=post
- https://threejs.org/examples/?q=webgpu
- https://threejs.org/manual/

## Validate These Points

- whether the intended post approach matches current official patterns
- whether the render-target flow is still aligned with supported Three.js usage
- whether the chosen feedback or history approach depends on undocumented assumptions
- whether the fallback path stays maintainable

## Record These Notes

- which official examples or docs were checked
- which pass-order or render-target decisions they confirm
- which parts of the design still rely on inference
