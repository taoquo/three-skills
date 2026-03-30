---
name: replicator
license: MIT
description: Analyze one or more graphics references and recreate the effect in Three.js. Use when the user shares a demo, article, video, Shadertoy, CodePen, GitHub repo, social thread, or screenshot and wants: a visual breakdown, a faithful or improved Three.js remake, research on likely rendering techniques, a runnable demo, tuning controls, or a REPORT.md that records sources, decisions, and revisions.
metadata:
  version: "2.0.0"
  category: threejs
  render_backends:
    - webgpu
    - webgl2
  shader_language: tsl
---

# Replicator

## Overview

Recreate effects with a visual-first workflow: observe, research, model, route techniques, select a backend, implement, verify, and document. Default priority is visual fidelity, then controllability, then performance unless the user explicitly changes that order.

Default authoring strategy:

- Use TSL as the primary shader and material language.
- Prefer `WebGPU` when the effect and runtime constraints support it.
- Fall back to `WebGL2` when compatibility, ecosystem maturity, or effect shape makes that the better choice.
- Use raw GLSL or WGSL only as a scoped fallback when TSL is a poor fit, and record that fallback explicitly in `REPORT.md`.

Do not treat `WebGL1` as a standard target for current Three.js work. Mention it only when the user explicitly requests legacy compatibility and the task must step outside the main path.

Default environment assumptions for this skill:

- Target desktop or laptop browsers first.
- Ignore aggressive performance optimization unless the user gives a hard device, FPS, or power constraint.
- Prefer the strongest visually convincing solution that still lands cleanly in current Three.js.

## Deliver Required Outputs

Produce all of the following for each effect:

- A measurable effect spec covering look, motion, interaction, invariants, and constraints.
- A backend decision that separates shader authoring language from runtime target.
- A research package with a link tree, extracted external links, comment takeaways, search terms, and a coverage table.
- A runnable Three.js demo under `effects/<effect-slug>/`.
- A GUI with stable group names and the key tuning controls exposed.
- A `REPORT.md` that stays current after every material change.
- Optional optimization or degradation strategies that preserve the intended look.

## Follow This Workflow

### 1. Model the effect before coding

Break the target into:

- Shape: SDF, mesh deformation, particles, instances, volume, screen-space, or mixed passes.
- Surface and lighting: PBR, NPR, fresnel, edge light, shadows, fog, scattering.
- Motion: noise, flow field, feedback, physics, camera choreography, temporal phase shifts.
- Post: bloom, tone mapping, chromatic aberration, vignette, grain, depth cues.
- Interaction: pointer, touch, scroll, audio, or camera control.
- Invariants: color palette, density, silhouette, rhythm, composition, deformation range.
- Constraints: target devices, frame-rate goals, interactivity requirements, fallback allowance.

Write the effect spec in measurable terms such as element count, motion frequency, visible scale, buffer count, or whether history feedback is required. Read [references/visual-quality.md](references/visual-quality.md) when the look is ambiguous or difficult to quantify.

### 2. Route the techniques before coding

Break the effect into 4 to 8 technique modules and mark each one:

- Required: cannot change without materially changing the look.
- Replaceable: may swap for a simpler or more robust approach if the look survives.

Typical modules:

- SDF or raymarch shape
- Particle field or instancing
- Surface or lighting
- Motion field
- Atmosphere or fog
- Post-processing
- Interaction mapping

Use technique names, not vague adjectives. Record the module list in `REPORT.md` before implementation.

### 3. Check TSL fit and research before coding

Treat the user links as the starting point, not the full source of truth.

- Search in this order:
  1. Mainstream or canonical graphics explanations and implementations: SIGGRAPH material, papers, talks, production notes, widely cited repos, or other authoritative references.
  2. Cross-engine rendering references: Unreal Engine, Unity, custom renderers, shader breakdowns, or engine-specific material graphs that clarify the visual method.
  3. Three.js landing guidance: decide how to reproduce the effect in the current `WebGPU` and TSL-oriented Three.js stack.
- Parse every provided link and extract the core idea, likely pipeline, important parameters, outbound links, and implementation hints.
- Pull high-signal details from code blocks, captions, issues, discussions, and comments when available.
- Expand the research tree up to depth 3 unless the trail runs out, becomes repetitive, or is blocked by login or dead links.
- Prefer English search queries for technique discovery and pitfall hunting, then translate the findings into a Three.js implementation.
- For each critical module, decide whether it is:
  - cleanly expressible in TSL
  - better served by TSL plus `code()` or interop
  - better left as a scoped raw shader fallback
- When a reference starts from GLSL, check whether the Three.js Transpiler could shorten the path from legacy shader code to a TSL-based implementation.

Read [references/research.md](references/research.md) before doing this step. Do not start implementation until the research coverage gate in that file is satisfied or the remaining gaps are documented with a fallback plan.

### 4. Select the backend and implementation plan

Use these defaults:

- Prefer the most visually convincing mainstream technique first, then adapt it into the strongest current Three.js runtime path.
- Prefer `TSL + WebGPU` for desktop-first work when the effect maps cleanly to the node-based path and the final look benefits from the modern renderer path.
- Use `TSL + WebGL2` only when the current Three.js or browser path makes it the better landing choice.
- Use raw GLSL or WGSL only when TSL creates avoidable complexity or blocks fidelity.
- Keep the first implementation path simple enough to debug in a browser.
- Borrow ideas from any engine, shader language, or paper, then translate them into Three.js-friendly structure.
- Ignore performance-first compromises until the look is locked unless the user explicitly asks otherwise.

State all of these in the report:

- Chosen shader authoring language
- Chosen runtime backend
- Rejected backend options
- Fallback path if the preferred backend or authoring path stalls

Use these scene archetypes:

- Screen-space effect: full-screen quad and post stack.
- Many elements: `InstancedMesh`, `Points`, or GPU feedback.
- Volume or fractal: raymarch with early exit and budgeted steps.
- Post-shaped effect: make the base pass correct before stacking post-processing.

Read [references/backend-selection.md](references/backend-selection.md), [references/webgpu-tsl.md](references/webgpu-tsl.md), [references/webgl2-tsl.md](references/webgl2-tsl.md), [references/legacy-shader-fallback.md](references/legacy-shader-fallback.md), and [references/three-official-guidance.md](references/three-official-guidance.md) based on the chosen route.

### 5. Scaffold the effect folder

Create the output under `effects/<effect-slug>/`.

- Use `scripts/init_effect.py` when you want a fast starting point.
- Copy `assets/report-template.md` to `effects/<effect-slug>/REPORT.md` if the script is not used.
- Reuse `assets/templates/tsl-webgpu/`, `assets/templates/tsl-webgl2/`, or `assets/templates/legacy-glsl/` based on the selected path unless the project already has a stronger local setup.
- Keep the demo shell minimal: a plain HTML page, direct browser preview, and no extra explanatory text in the body outside GUI or explicit error state.

Keep the folder self-contained and easy to run.

### 6. Implement in passes

Implement in this order:

1. Make an MVP that captures the overall composition and motion.
2. Align the signature details: palette, density, timing, layering, and interaction feel.
3. Add the post chain and polish.
4. Optimize only after the look is close enough.

Expose a GUI by default. Keep group names stable:

- `Renderer`: exposure, DPR, AA-related controls, pause toggles if needed.
- `Post`: bloom, threshold, radius, output-related controls.
- `Style`: palette, contrast, vignette, grain, aberration, fog, glow.
- `Animation`: speed, phase, time scale, autoplay, pause.

Add domain-specific groups when needed:

- `Raymarch`: step count, epsilon, max distance, fog density, shadow softness.
- `Noise`: frequency, amplitude, octaves, lacunarity, gain.
- `Particles`: count, spawn rate, drag, curl strength, lifetime.
- `Feedback`: decay, blur, mix, persistence.

Read [references/gui.md](references/gui.md) for the control layout and naming rules.

### 7. Validate and document

Before finishing:

- Compare the output against the measurable effect spec.
- Call out the dominant bottleneck: fill rate, ray steps, particle count, bandwidth, or post chain.
- Add degradation switches for resolution, step count, particle count, and post quality when the task has device or FPS constraints.
- Record which modules stayed pure TSL and which ones required interop or raw shader fallbacks.
- Cross-check the final renderer, TSL, post, and node usage against current official Three.js docs and manual pages before you call the implementation done.
- Update `REPORT.md` with source notes, choices, open risks, and the latest change log entry.

Do not treat the report as optional. Every meaningful edit must be reflected there.

## Use Bundled Resources

Load only the files that help the current task:

- [references/research.md](references/research.md): use for source parsing, link-tree expansion, English search planning, and the research coverage gate.
- [references/visual-quality.md](references/visual-quality.md): use for effect-spec writing and visual self-checks.
- [references/tsl-core.md](references/tsl-core.md): use for deciding whether TSL should remain the default authoring path.
- [references/backend-selection.md](references/backend-selection.md): use for choosing `WebGPU` versus `WebGL2`.
- [references/webgpu-tsl.md](references/webgpu-tsl.md): use for `TSL + WebGPU` guidance.
- [references/webgl2-tsl.md](references/webgl2-tsl.md): use for `TSL + WebGL2` guidance.
- [references/legacy-shader-fallback.md](references/legacy-shader-fallback.md): use when a raw shader fallback is justified.
- [references/three-official-guidance.md](references/three-official-guidance.md): use to sanity-check the final code against current official Three.js guidance for `WebGPURenderer`, TSL, and official examples.
- [references/gui.md](references/gui.md): use for GUI grouping and parameter selection.
- `scripts/init_effect.py`: use to scaffold `effects/<effect-slug>/` from the included template.
- `assets/templates/`: use as the baseline starter matrix when a zero-build setup is appropriate.
- `assets/report-template.md`: use as the required report skeleton.

## Keep Decisions Explicit

State these decisions clearly in the report and the user-facing summary:

- What the effect is made of.
- Which techniques are required versus replaceable.
- Which parts fit pure TSL and which parts do not.
- Which backend was chosen and why.
- Which sources influenced the final plan.
- Which risks remain unresolved.
- Which switches preserve the look when performance drops.
