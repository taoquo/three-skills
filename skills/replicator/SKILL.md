---
name: replicator
description: Analyze one or more graphics references and recreate the effect in Three.js. Use when the user shares a demo, article, video, Shadertoy, CodePen, GitHub repo, social thread, or screenshot and wants: a visual breakdown, a faithful or improved Three.js remake, research on likely rendering techniques, a runnable demo, tuning controls, or a REPORT.md that records sources, decisions, and revisions.
---

# Replicator

## Overview

Recreate effects with a visual-first workflow: observe, research, model, implement, verify, and document. Default priority is visual fidelity, then controllability, then performance unless the user explicitly changes that order.

## Deliver Required Outputs

Produce all of the following for each effect:

- A measurable effect spec covering look, motion, interaction, invariants, and constraints.
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

### 2. Research before coding

Treat the user links as the starting point, not the full source of truth.

- Parse every provided link and extract the core idea, likely pipeline, important parameters, outbound links, and implementation hints.
- Pull high-signal details from code blocks, captions, issues, discussions, and comments when available.
- Expand the research tree up to depth 3 unless the trail runs out, becomes repetitive, or is blocked by login or dead links.
- Prefer English search queries for technique discovery and pitfall hunting, then translate the findings into a Three.js/WebGL2 implementation.

Read [references/research.md](references/research.md) before doing this step. Do not start implementation until the research coverage gate in that file is satisfied or the remaining gaps are documented with a fallback plan.

### 3. Choose the implementation plan

Pick the smallest technique set that explains the reference convincingly. Mark each module as either:

- Required: cannot change without materially changing the look.
- Replaceable: may swap for a simpler or more robust technique if the look survives.

Use these defaults:

- Prefer WebGL2 and `THREE.WebGLRenderer`.
- Borrow ideas from any engine, shader language, or paper, then translate them into Three.js-friendly structure.
- Use WebGPU only when the user explicitly asks for it.
- Keep the first implementation path simple enough to debug in a browser.

Use these scene archetypes:

- Screen-space effect: full-screen quad and post stack.
- Many elements: `InstancedMesh`, `Points`, or GPU feedback.
- Volume or fractal: raymarch with early exit and budgeted steps.
- Post-shaped effect: make the base pass correct before stacking post-processing.

Read [references/webgl2-visual.md](references/webgl2-visual.md) for the default visual-quality render path.

### 4. Scaffold the effect folder

Create the output under `effects/<effect-slug>/`.

- Use `scripts/init_effect.py` when you want a fast starting point.
- Copy `assets/report-template.md` to `effects/<effect-slug>/REPORT.md` if the script is not used.
- Reuse `assets/template/` as the zero-build baseline unless the project already has a stronger local setup.

Keep the folder self-contained and easy to run.

### 5. Implement in passes

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

### 6. Validate and document

Before finishing:

- Compare the output against the measurable effect spec.
- Call out the dominant bottleneck: fill rate, ray steps, particle count, bandwidth, or post chain.
- Add degradation switches for resolution, step count, particle count, and post quality when the task has device or FPS constraints.
- Update `REPORT.md` with source notes, choices, open risks, and the latest change log entry.

Do not treat the report as optional. Every meaningful edit must be reflected there.

## Use Bundled Resources

Load only the files that help the current task:

- [references/research.md](references/research.md): use for source parsing, link-tree expansion, English search planning, and the research coverage gate.
- [references/visual-quality.md](references/visual-quality.md): use for effect-spec writing and visual self-checks.
- [references/webgl2-visual.md](references/webgl2-visual.md): use for WebGL2, HDR, MSAA, tone mapping, and output-chain decisions.
- [references/gui.md](references/gui.md): use for GUI grouping and parameter selection.
- `scripts/init_effect.py`: use to scaffold `effects/<effect-slug>/` from the included template.
- `assets/template/`: use as the baseline Three.js demo when a zero-build setup is appropriate.
- `assets/report-template.md`: use as the required report skeleton.

## Keep Decisions Explicit

State these decisions clearly in the report and the user-facing summary:

- What the effect is made of.
- Which techniques are required versus replaceable.
- Which sources influenced the final plan.
- Which risks remain unresolved.
- Which switches preserve the look when performance drops.
