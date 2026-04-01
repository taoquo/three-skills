---
name: shader-port
license: MIT
description: Port Shadertoy, GLSL, or WGSL shader logic into current Three.js TSL-first implementations with explicit unsupported-case reporting, renderer-aware fallbacks, and verification notes.
metadata:
  category: threejs
  render_backends:
    - webgpu
    - webgl2
  shader_language: tsl
  skill_type: utility
---

# Three.js Shader Port

## Purpose

Use `shader-port` when the user has a standalone shader source (Shadertoy, raw GLSL, WGSL snippet, fullscreen post fragment, legacy WebGL demo) and needs:

- a clear source contract before implementation,
- a TSL-first port into current Three.js,
- an honest statement of what cannot be ported cleanly,
- a renderer-aware fallback plan, and
- verification notes that show the result is actually correct rather than merely compiling.

Repository baseline for this skill:

- Three.js `0.180.0`
- `WebGPURenderer` imported from `three/webgpu`
- TSL symbols imported from `three/tsl`

## Non-Negotiables

- Start by classifying the source correctly: single-pass fragment, material logic, multipass post, raymarcher, feedback chain, or compute/storage-heavy pipeline.
- Prefer one honest TSL path first. Only widen into backend-specific escape hatches when the source actually requires them.
- Distinguish two different fallback types:
  - `TSL-on-WebGL2-backend`: still a node and TSL path, typically through `WebGPURenderer` with `forceWebGL`.
  - `legacy-WebGL-raw`: `WebGLRenderer` plus `ShaderMaterial`, `RawShaderMaterial`, or `ShaderPass`.
- Do not claim a WebGPU path supports raw custom materials. Current official Three.js docs say `ShaderMaterial`, `RawShaderMaterial`, and `onBeforeCompile()` are not supported in `WebGPURenderer`.
- Do not claim automatic WGSL-to-TSL conversion. Current official `Transpiler` support is `GLSL -> TSL` only.
- If a port cannot be kept correct and maintainable, say so explicitly and give the narrowest fallback that still works.

## Status Labels

Use one status label in the final report:

- `ported-cleanly`: pure TSL, same behavior class, no backend-specific escape hatch
- `ported-with-scoped-interop`: mostly TSL, one or more tightly scoped native code helpers
- `webgpu-only`: correct result depends on WebGPU-only resources or compute/storage features
- `legacy-webgl-fallback`: correct result requires a raw GLSL path on `WebGLRenderer`
- `blocked`: missing source information, unsupported feature contract, or no honest maintainable route

## Workflow

1. **Source contract** – record the source URI or files, pass topology, required inputs, coordinate space, precision assumptions, and whether the source is authoritative enough to verify against.
2. **TSL fit** – map each module into one of these routes:
   - `pure-tsl`
   - `tsl-plus-interop`
   - `tsl-webgpu-only`
   - `legacy-webgl-raw`
   - `blocked`
3. **Port plan** – define the uniform and texture mapping, screen and viewport mapping, pass ordering, history/depth dependencies, and the exact renderer contract.
4. **Implementation** – prefer direct TSL primitives such as `Fn`, `uniform`, `varying`, `If`, `Loop`, `screenUV`, `screenCoordinate`, `pass`, and `mrt`. Use `glslFn` or `wgslFn` only as narrow escape hatches for isolated helpers.
5. **Fallback decision** – if the preferred path stalls, choose the smallest honest fallback: stay TSL but WebGPU-only, stay TSL and use the WebGL2 backend, or drop to a raw WebGL path.
6. **Verification** – confirm compile status on every promised path, verify visual parity against the authoritative source, and record exactly what was preserved, simplified, or dropped.

## Authoring Route Rules

### `pure-tsl`

Use this when the shader is mostly math, shading, UV warping, moderate raymarching, or post logic that maps cleanly to the current TSL surface.

Good signals:

- single-pass or modest multipass
- no storage buffers or compute requirement
- no dependency on undocumented driver-specific behavior
- the same logic should run on WebGPU and WebGL2 backend paths

### `tsl-plus-interop`

Use this when most of the port is still readable in TSL but one local function is better kept as native code.

Hard rules:

- Keep the boundary small and named.
- Prefer one small math or noise helper, not an entire hidden fragment program.
- Treat single-language native helpers as backend-specific unless an equivalent exists for the other backend. That is a reasoned inference from the official `FunctionNode` API exposing explicit `wgsl` and `glsl` language modes.

### `tsl-webgpu-only`

Use this when correctness depends on resources or execution models that are effectively WebGPU-only in current Three.js, such as compute or storage-texture driven pipelines.

Do not promise WebGL2 parity here unless you have implemented and verified a separate non-compute approximation.

### `legacy-webgl-raw`

Use this only when the correct effect depends on raw GLSL and current Three.js does not offer a clean TSL route.

Be explicit:

- this route uses `WebGLRenderer`
- this route is not supported by `WebGPURenderer`
- this route is a compatibility or fidelity fallback, not the preferred architecture

### `blocked`

Use this when the source or target contract makes an honest port impossible right now.

Typical blockers:

- missing multipass source buffers or hidden textures
- compute/storage/atomics/subgroup behavior with a required WebGL2 target
- dependence on raw custom material control in a `WebGPU` route
- the only possible solution is a large opaque native shader blob that defeats the maintainability goal

## Deliverables

- A short report that includes:
  - the status label
  - the source contract
  - the chosen authoring route
  - the renderer and backend contract
  - the fallback plan
  - verification notes
- A minimal runnable Three.js snippet using the chosen route.
- A resource and pass mapping table.
- An explicit unsupported-case note whenever parity is not exact.
- Optional tuning or degradation notes when the shader is expensive.

## Reference Pack

Use the references under [`references/`](references/) as the porting decision layer:

- [`references/README.md`](references/README.md) for the default port sequence
- [`references/source-intake.md`](references/source-intake.md) to classify shader inputs and pass topology
- [`references/tsl-mapping.md`](references/tsl-mapping.md) for the current TSL landing surface
- [`references/coordinate-mapping.md`](references/coordinate-mapping.md) for `fragCoord`, UV, ray, and camera translation
- [`references/resource-mapping.md`](references/resource-mapping.md) for uniforms, textures, buffers, and multipass routing
- [`references/porting-notes.md`](references/porting-notes.md) for authoring-path decisions, official constraints, and fallback rules
- [`references/verification-checklist.md`](references/verification-checklist.md) to validate the final port cleanly

## When To Call Out `Cannot Port Cleanly`

Say the port cannot be done cleanly when any of these is true:

- the requested backend contract and the source requirements conflict
- the authoritative source artifact is incomplete or missing critical passes
- the only correct implementation would be backend-specific native code across most of the material
- the fallback would materially change the effect and the user has not accepted an approximation

When that happens, always give one concrete fallback:

- `WebGPU-only TSL`
- `TSL with WebGL2 backend`
- `raw WebGL GLSL`
- `approximation with disclosed visual trade-offs`
- `blocked pending missing assets or user decision`

## When Not to Use

- Reference-driven full effect replication that needs the entire `replicator` workflow.
- Pure performance diagnosis or profiling work unrelated to shader translation.
- Pure material-look exploration with no shader source to translate.

## Tone

Keep explanations sharp and focused. Prefer small decision tables over prose when comparing routes. Whenever compatibility is discussed, mention the current Three.js baseline and separate documented facts from reasoned inference.
