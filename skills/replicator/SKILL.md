---
name: replicator
license: MIT
description: Analyze one or more graphics references and recreate the effect in Three.js. Use when the user shares a demo, article, video, Shadertoy, CodePen, GitHub repo, social thread, or screenshot and wants: a visual breakdown, a faithful or improved Three.js remake, research on likely rendering techniques, a runnable demo, tuning controls, or a REPORT.md that records sources, decisions, and revisions.
metadata:
  version: "3.0.0"
  category: threejs
  render_backends:
    - webgpu
    - webgl2
  shader_language: tsl
  skill_type: workflow
  owns_templates: "true"
  owns_scaffolder: "true"
---

# Replicator

## Overview

Recreate effects with a visual-first workflow: route the archetype, research the effect, choose the implementation surface, set the post and performance contracts, implement, verify, and document. Default priority is visual fidelity, then controllability, then performance unless the user explicitly changes that order.

`replicator` is the orchestration layer in this repository. It should pull in `platform`, `postfx`, and `performance` as needed instead of re-explaining their domains.

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

## Route By Archetype First

Pick the closest archetype before you do deep research or implementation planning.

Use [references/archetypes.md](references/archetypes.md) as the routing table.

Canonical archetypes:

- `material-study`
- `scene-post`
- `fullscreen-raymarch`
- `instanced-particles`
- `feedback-trails`
- `mixed`

If the effect spans multiple archetypes, choose the dominant one and call out the secondary archetype in `REPORT.md`.

## Do Not Use This Skill For

- Pure material or lighting exploration with no external reference to match. Use `platform` plus a material-focused workflow instead.
- Isolated renderer or compatibility decisions. Use `platform`.
- Pure performance diagnosis or degradation planning. Use `performance`.
- Pure post-chain design or feedback-buffer routing with no reference-driven remake. Use `postfx`.

## Deliver Required Outputs

Produce all of the following for each effect:

- A chosen archetype and a short justification for why it fits better than the nearest alternative route.
- A measurable effect spec covering look, motion, interaction, invariants, and constraints.
- An implementation-surface decision covering authoring path, runtime renderer, resource model, pass topology, compatibility contract, and fallback path.
- A performance decision covering target device class, performance contract, dominant bottleneck, degradation ladder, and exposed controls.
- A post-processing decision covering post pipeline type, render-target layout, pass order, history requirement, and quality tiers when post is part of the look.
- A research package with a link tree, extracted external links, comment takeaways, search terms, and a coverage table.
- A runnable Three.js demo under `effects/<effect-slug>/`.
- A GUI with stable group names and the key tuning controls exposed.
- A `REPORT.md` that stays current after every material change.
- Optional optimization or degradation strategies that preserve the intended look.

## Follow This Workflow

### 1. Route the effect archetype before coding

Pick the archetype before you expand research or choose templates.

Use the routing table in [references/archetypes.md](references/archetypes.md).

At minimum, record:

- chosen archetype
- why it fits
- nearest rejected archetype
- which supporting skills are expected to matter: `platform`, `postfx`, `performance`

If the archetype is unclear, write `mixed` and explain what would settle it.

### 2. Model the effect before coding

Break the target into:

- Shape: SDF, mesh deformation, particles, instances, volume, screen-space, or mixed passes.
- Surface and lighting: PBR, NPR, fresnel, edge light, shadows, fog, scattering.
- Motion: noise, flow field, feedback, physics, camera choreography, temporal phase shifts.
- Post: bloom, tone mapping, chromatic aberration, vignette, grain, depth cues.
- Interaction: pointer, touch, scroll, audio, or camera control.
- Invariants: color palette, density, silhouette, rhythm, composition, deformation range.
- Constraints: target devices, frame-rate goals, interactivity requirements, fallback allowance.

Write the effect spec in measurable terms such as element count, motion frequency, visible scale, buffer count, or whether history feedback is required. Read [references/visual-quality.md](references/visual-quality.md) when the look is ambiguous or difficult to quantify.

### 3. Route the techniques before coding

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

### 4. Check TSL fit and research before coding

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

### 5. Select the implementation surface and implementation plan

Use these defaults:

- Prefer the most visually convincing mainstream technique first, then adapt it into the strongest current Three.js runtime path.
- Prefer `pure-tsl` first when the effect maps cleanly to the node-based path.
- Prefer `WebGPU` only when the chosen resource model, pass topology, or compatibility contract justifies it.
- Use `WebGL2` when the current Three.js or browser path makes it the better landing choice.
- Use raw GLSL or WGSL only when TSL creates avoidable complexity or blocks fidelity.
- Keep the first implementation path simple enough to debug in a browser.
- Borrow ideas from any engine, shader language, or paper, then translate them into Three.js-friendly structure.
- Ignore performance-first compromises until the look is locked unless the user explicitly asks otherwise.

State all of these in the report:

- Chosen authoring path
- Chosen runtime renderer
- Chosen resource model
- Chosen pass topology
- Chosen compatibility contract
- Rejected backend options
- Fallback path if the preferred backend or authoring path stalls

When `platform` is available, use it as the source of truth for this decision. Read [../platform/references/interface-decision-tree.md](../platform/references/interface-decision-tree.md), [../platform/references/authoring-paths.md](../platform/references/authoring-paths.md), [../platform/references/backend-capability-matrix.md](../platform/references/backend-capability-matrix.md), [../platform/references/webgpu-resource-patterns.md](../platform/references/webgpu-resource-patterns.md), [../platform/references/pipeline-archetypes.md](../platform/references/pipeline-archetypes.md), [../platform/references/renderer-compatibility.md](../platform/references/renderer-compatibility.md), and [../platform/references/official-threejs-webgpu.md](../platform/references/official-threejs-webgpu.md) based on the chosen route.

Use these scene archetypes:

- Screen-space effect: full-screen quad and post stack.
- Many elements: `InstancedMesh`, `Points`, or GPU feedback.
- Volume or fractal: raymarch with early exit and budgeted steps.
- Post-shaped effect: make the base pass correct before stacking post-processing.

### 6. Choose the post pipeline when post matters

If the look depends on post, decide these explicitly:

- post pipeline type
- render-target layout
- pass order
- history requirement
- quality tiers

When `postfx` is available, use it as the source of truth for this decision. Read [../postfx/references/post-chain-selection.md](../postfx/references/post-chain-selection.md), [../postfx/references/render-target-patterns.md](../postfx/references/render-target-patterns.md), [../postfx/references/history-feedback.md](../postfx/references/history-feedback.md), [../postfx/references/quality-tiering.md](../postfx/references/quality-tiering.md), and [../postfx/references/official-three-postfx.md](../postfx/references/official-three-postfx.md) based on the chosen route.

### 7. Scaffold the effect folder

Create the output under `effects/<effect-slug>/`.

- Use `scripts/init_effect.py` when you want a fast starting point.
- Prefer a canonical archetype profile when the effect is not mixed.
- Copy `assets/report-template.md` to `effects/<effect-slug>/REPORT.md` if the script is not used.
- Reuse `assets/templates/tsl-webgpu/`, `assets/templates/tsl-webgl2/`, or `assets/templates/legacy-glsl/` based on the selected path unless the project already has a stronger local setup.
- Keep the demo shell minimal: a plain HTML page, direct browser preview, and no extra explanatory text in the body outside GUI or explicit error state.

Keep the folder self-contained and easy to run.

### 8. Implement in passes

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

### 9. Validate performance, fidelity, post, then document

Before finishing:

- Compare the output against the measurable effect spec.
- Call out the dominant bottleneck: fill rate, ray steps, particle count, bandwidth, post chain, or CPU/driver cost.
- Choose an explicit target device class and performance contract.
- Add a short degradation ladder for resolution, step count, particle count, simulation resolution, and post quality where relevant.
- Save reference and current captures under `captures/` with stable names.
- Score silhouette, motion, density, palette, and finish using [references/fidelity-rubric.md](references/fidelity-rubric.md).
- Run `scripts/capture_audit.py` after saving captures so the pair manifest and review summary stay current.
- If the fidelity score is below the acceptance target, record the gap instead of calling the effect done.
- Record which modules stayed pure TSL and which ones required interop or raw shader fallbacks.
- Cross-check the final renderer, TSL, post, and node usage against current official Three.js docs and manual pages before you call the implementation done.
- Update `REPORT.md` with source notes, choices, open risks, and the latest change log entry.

Do not treat the report as optional. Every meaningful edit must be reflected there.

## Use Bundled Resources

Load only the files that help the current task:

- [references/archetypes.md](references/archetypes.md): use for the initial archetype route and starter-profile choice.
- [references/research.md](references/research.md): use for source parsing, link-tree expansion, English search planning, and the research coverage gate.
- [references/visual-quality.md](references/visual-quality.md): use for effect-spec writing and visual self-checks.
- [references/fidelity-rubric.md](references/fidelity-rubric.md): use for visual acceptance scoring and capture review.
- `scripts/capture_audit.py`: use to generate `captures/manifest.json` and `captures/review.md` from saved reference/current capture pairs.
- [../platform/references/interface-decision-tree.md](../platform/references/interface-decision-tree.md): use for workload classification and implementation routing.
- [../platform/references/authoring-paths.md](../platform/references/authoring-paths.md): use for `TSL`, interop, `WGSL`, and `GLSL` path selection.
- [../platform/references/backend-capability-matrix.md](../platform/references/backend-capability-matrix.md): use for renderer and authoring tradeoffs.
- [../platform/references/webgpu-resource-patterns.md](../platform/references/webgpu-resource-patterns.md): use for choosing the GPU resource model.
- [../platform/references/pipeline-archetypes.md](../platform/references/pipeline-archetypes.md): use for pass topology selection.
- [../platform/references/renderer-compatibility.md](../platform/references/renderer-compatibility.md): use for browser target and fallback policy.
- [../platform/references/official-threejs-webgpu.md](../platform/references/official-threejs-webgpu.md): use to sanity-check the final code against current official Three.js guidance.
- [../performance/references/device-targeting.md](../performance/references/device-targeting.md): use for default device assumptions and target device classes.
- [../performance/references/bottleneck-diagnosis.md](../performance/references/bottleneck-diagnosis.md): use for naming the dominant bottleneck.
- [../performance/references/degradation-playbook.md](../performance/references/degradation-playbook.md): use for choosing the quality ladder.
- [../performance/references/profiling-checklist.md](../performance/references/profiling-checklist.md): use for the final performance sanity check.
- [../postfx/references/post-chain-selection.md](../postfx/references/post-chain-selection.md): use for deciding whether the look belongs in post at all.
- [../postfx/references/render-target-patterns.md](../postfx/references/render-target-patterns.md): use for choosing the render-target layout.
- [../postfx/references/history-feedback.md](../postfx/references/history-feedback.md): use for deciding whether history is optional or required.
- [../postfx/references/quality-tiering.md](../postfx/references/quality-tiering.md): use for post quality ladders and exposed-safe controls.
- [../postfx/references/official-three-postfx.md](../postfx/references/official-three-postfx.md): use to sanity-check the final post approach against official Three.js guidance.
- [references/gui.md](references/gui.md): use for GUI grouping and parameter selection.
- `scripts/init_effect.py`: use to scaffold `effects/<effect-slug>/` from the included template.
- `assets/templates/`: use as the baseline starter matrix when a zero-build setup is appropriate.
- `assets/report-template.md`: use as the required report skeleton.

## Keep Decisions Explicit

State these decisions clearly in the report and the user-facing summary:

- Which archetype was chosen and why.
- What the effect is made of.
- Which techniques are required versus replaceable.
- Which authoring path was chosen and why.
- Which renderer, resource model, pass topology, and compatibility contract were chosen and why.
- Which target device class, performance contract, and degradation ladder were chosen and why.
- Which post pipeline type, render-target layout, history requirement, and pass order were chosen and why.
- Which captures were used for acceptance and what the fidelity score was.
- Which sources influenced the final plan.
- Which risks remain unresolved.
- Which switches preserve the look when performance drops.
