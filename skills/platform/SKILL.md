---
name: platform
license: MIT
description: Choose the right Three.js implementation surface before coding. Use when the user needs a clear decision for `TSL`, `WebGPURenderer`, `WebGLRenderer`, raw `WGSL` or `GLSL`, GPU resource model, pass topology, fallback policy, or browser compatibility for a Three.js effect or app.
metadata:
  version: "1.0.0"
  category: threejs
  render_backends:
    - webgpu
    - webgl2
  shader_language: tsl
  skill_type: decision
  owns_templates: "false"
  owns_scaffolder: "false"
---

# Three.js Platform

## Overview

Use this skill to decide the implementation surface before coding.

The job is not just picking `WebGPU` or `WebGL2`. The job is to produce a complete platform decision:

- authoring path
- runtime renderer
- resource model
- pass topology
- compatibility contract
- fallback path

Prefer the lowest-complexity surface that can still produce the intended look.

## Deliver Required Outputs

Produce a short decision summary with these fields:

| Field | Allowed values |
| --- | --- |
| Authoring path | `pure-tsl`, `tsl-plus-interop`, `raw-wgsl`, `raw-glsl`, `dual-path` |
| Runtime renderer | `webgpu-renderer`, `webgl-renderer`, `dual-renderer` |
| Resource model | `uniforms`, `instanced-attributes`, `sampled-textures`, `storage-buffer`, `storage-texture`, `render-target-history` |
| Pass topology | `single-pass-material`, `fullscreen-procedural`, `scene-plus-post`, `simulation-plus-render`, `feedback-loop`, `compute-plus-render` |
| Compatibility contract | `desktop-webgpu`, `desktop-webgpu-plus-webgl2-fallback`, `webgl2-first` |
| Fallback path | explicit degraded or alternate path |

Also record rejected options and why they were rejected.

## Follow This Workflow

### 1. Classify the workload

First decide what kind of problem this is:

- material or lighting
- full-screen procedural effect
- geometry scene plus post
- simulation plus render
- persistent feedback system

Read [references/interface-decision-tree.md](references/interface-decision-tree.md) first.

### 2. Choose the authoring path

Default rules:

- Use `pure-tsl` when the effect is mostly composable nodes and does not need explicit low-level GPU control.
- Use `tsl-plus-interop` when most of the effect fits TSL but one module needs custom math or tightly scoped interop.
- Use `raw-wgsl` when the effect genuinely depends on WebGPU-specific behavior such as compute-heavy flows, storage resources, or explicit GPU data control.
- Use `raw-glsl` when the task is `WebGL2`-first or when a mature legacy shader is the most efficient landing path.
- Use `dual-path` only when broad compatibility is required and the better `WebGPU` path is still worth maintaining.

Read [references/authoring-paths.md](references/authoring-paths.md) before making this call.

### 3. Choose the runtime renderer

Default rules:

- Choose `webgpu-renderer` when the effect benefits materially from the modern path and the compatibility contract allows it.
- Choose `webgl-renderer` when compatibility, ecosystem maturity, or lower implementation risk matter more.
- Choose `dual-renderer` only when the product requirement truly needs both paths.

Read [references/backend-capability-matrix.md](references/backend-capability-matrix.md) and [references/renderer-compatibility.md](references/renderer-compatibility.md).

### 4. Choose the resource model

Use the smallest workable GPU data model:

- `uniforms` for small global parameter sets
- `instanced-attributes` for many renderable elements with per-instance state
- `sampled-textures` for lookup-driven inputs and image-like data
- `render-target-history` for ping-pong or feedback state across frames
- `storage-buffer` for large structured mutable GPU state
- `storage-texture` for writable image grids and similar WebGPU-oriented workloads

Read [references/webgpu-resource-patterns.md](references/webgpu-resource-patterns.md).

### 5. Choose the pass topology

Use one of these shapes:

- `single-pass-material`
- `fullscreen-procedural`
- `scene-plus-post`
- `simulation-plus-render`
- `feedback-loop`
- `compute-plus-render`

Read [references/pipeline-archetypes.md](references/pipeline-archetypes.md).

### 6. Set the compatibility contract

Choose one explicit contract:

- `desktop-webgpu`
- `desktop-webgpu-plus-webgl2-fallback`
- `webgl2-first`

Do not leave compatibility implicit.

### 7. Validate against official Three.js guidance

Use official docs and examples to confirm the final import path, renderer choice, and supported programming model.

Read [references/official-threejs-webgpu.md](references/official-threejs-webgpu.md) before finalizing.

## Keep These Rules

- Prefer the lowest-power abstraction that still matches the effect.
- Do not choose `WebGPU` only because it is newer.
- Do not choose raw shaders only because the reference started in raw shaders.
- If compute, storage, or persistent GPU state is essential, say so explicitly.
- If the fallback cannot preserve parity, say that explicitly instead of pretending the paths are equal.

## Typical Routes

| Situation | Recommended surface |
| --- | --- |
| Layered material, fresnel, distortion, moderate post | `pure-tsl` + `webgpu-renderer` or `webgl-renderer` depending compatibility |
| Full-screen noise or raymarch demo | `pure-tsl` or `tsl-plus-interop` + `fullscreen-procedural` |
| Many instances with simple per-instance animation | `pure-tsl` + `instanced-attributes` + `scene-plus-post` |
| Image-like feedback effect | `render-target-history` + `feedback-loop` |
| Stateful particles, boids, cloth, or dense simulation | `simulation-plus-render` with `storage-buffer` or `render-target-history` |
| Workgroup-style compute or explicit GPU dataflow | `raw-wgsl` + `webgpu-renderer` + `compute-plus-render` |

## Use Bundled Resources

- [references/interface-decision-tree.md](references/interface-decision-tree.md): use for the initial workload split and implementation routing.
- [references/authoring-paths.md](references/authoring-paths.md): use for `TSL`, interop, `WGSL`, and `GLSL` path selection.
- [references/backend-capability-matrix.md](references/backend-capability-matrix.md): use for renderer and authoring tradeoffs.
- [references/webgpu-resource-patterns.md](references/webgpu-resource-patterns.md): use for GPU data model decisions.
- [references/pipeline-archetypes.md](references/pipeline-archetypes.md): use for pass topology and render-graph shape.
- [references/renderer-compatibility.md](references/renderer-compatibility.md): use for browser-target and fallback policy.
- [references/official-threejs-webgpu.md](references/official-threejs-webgpu.md): use to validate the final decision against official Three.js guidance.

## Keep Decisions Explicit

State these clearly in the final answer or report:

- what kind of rendering problem this is
- why the chosen authoring path fits
- why the chosen renderer fits
- what GPU resource model is required
- what pass topology is required
- what compatibility contract the implementation is making
- which fallback is real versus merely theoretical
