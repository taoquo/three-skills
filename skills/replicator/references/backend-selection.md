# Backend Selection

## Goal

Choose the runtime backend after the effect has been modeled and the TSL fit has been checked.

The default priority is:

1. The strongest visually convincing technique
2. `WebGPU`
3. `WebGL2`

Do not treat `WebGL1` as a standard target for current Three.js work.

## Prefer WebGPU

Choose `WebGPU` when:

- the desktop-first path is acceptable
- the project is new and not locked to older browsers
- the effect benefits from the modern renderer path
- the effect is expected to evolve over time
- the implementation stays readable in TSL

Typical examples:

- heavier procedural materials
- richer node-based pipelines
- work that may later need more advanced GPU workflows

## Prefer WebGL2

Choose `WebGL2` when:

- runtime compatibility is more important than using the newest backend
- the surrounding demo stack already assumes the WebGL ecosystem
- the effect is straightforward and does not gain much from `WebGPU`
- the `WebGPU` path adds risk without improving the result enough

## Required Report Notes

Always record:

- mainstream implementation sources considered first
- cross-engine references considered second
- chosen backend
- rejected backend options
- why the chosen backend fits
- fallback path if the primary backend is blocked
