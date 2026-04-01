---
name: replicator
license: MIT
description: Analyze multimodal graphics references and recreate the effect in Three.js. Use when the user shares a URL, demo, article, video, Shadertoy, CodePen, GitHub repo, social thread, screenshot, image URI, local image path, or a keyword/topic prompt and wants: a visual breakdown, a faithful or improved Three.js remake, research on likely rendering techniques, a runnable demo, tuning controls, or a REPORT.md that records sources, decisions, and revisions.
metadata:
  version: "4.6.0"
  category: threejs
  render_backends:
    - webgpu
    - webgl2
  shader_language: tsl
  skill_type: workflow
  owns_templates: "true"
  owns_scaffolder: "true"
---

# Three.js Replicator

## Overview

Recreate effects with an evidence-first visual workflow: lock the reference contract, route the archetype, research the effect, choose the implementation surface, set the post and performance contracts, implement, verify, and document. Default priority is visual fidelity, then controllability, then performance unless the user explicitly changes that order.

`replicator` remains the canonical skill id for compatibility. The human-facing name is `Three.js Replicator` to reflect that the workflow can start from URLs, keywords, image URIs, screenshots, local image paths, or mixed reference sets.

The `replicator` skill is a complete Three.js effect workflow. It includes three internal decision modules:

- implementation surface decision
- post pipeline decision
- performance contract decision

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

## Accept Multimodal Inputs

Treat all of the following as valid entry points:

- URLs to demos, posts, repos, videos, articles, or code sandboxes.
- Keywords or topic prompts such as a style, effect name, or rendering technique.
- Image URIs, screenshots, or local image paths.
- Mixed input sets that combine any of the above.

Normalize the intake before route selection:

- `primary`: the main reference that defines silhouette, motion language, and composition
- `secondary`: an explicit module donor such as post polish, surface treatment, or interaction
- `accent`: palette, timing, or a narrow finish cue only
- `derived`: a reference discovered during research from a keyword or image-first start

For keyword-only or image-only starts:

- extract 3 to 8 English-first search phrases from the visual or textual cues
- gather 2 to 5 high-signal external references before choosing the route
- promote one result to the primary reference and record why it won
- use `AskUserOption` only if the remaining ambiguity would materially change the pipeline

Do not reject the task merely because the user did not provide a URL.

## Enforce Evidence Gates

Use these hard rules as the compact execution layer for every reference-driven remake:

1. Reference access gate

- If the task is `faithful-remake`, require at least one accessible primary visual artifact before implementation: directly inspectable URL, screenshot, video or recording, local image or video, or a high-confidence multi-source replacement set.
- Product copy, SEO summaries, titles, feature lists, and search snippets are not enough for a faithful route.
- If the gate fails, do not start implementation. Ask for stronger reference material or block the faithful route.

2. Mode contract

- Classify the task as `faithful-remake`, `approximation-from-limited-evidence`, or `inspired-variant` before implementation.
- If the user asked for faithful but the reference gate failed, do not silently continue as faithful. Request approval to downgrade or stop.

3. Visual evidence table

- Build a table with `Module`, `Target visual trait`, `Evidence source`, `Confidence`, and `Implementation plan` before implementation.
- Cover framing or camera language, silhouette or shape language, motion behavior, reflection or refraction behavior, palette or tonal range, atmosphere or post, interaction cues, and any signature modules.

4. Classic graphics baseline fallback

- When the target reference is accessible but the expected completion depth is unclear, use canonical graphics and game-industry references only to decide what a competent implementation normally includes.
- Record separately what came from the target reference versus the classic baseline.

5. No blind filling rule

- If a critical visual module lacks evidence, do not invent concrete sky, sun, terrain, palette, foam, post, or other scene dressing and pretend it came from the reference.
- Only add placeholder content when approximation or inspired mode is explicit and the report says it is not reference-driven.

6. First-frame review gate

- Stage A locks composition, silhouette, primary material relationships, main form profile, and primary light or color read.
- Only after Stage A is close enough should Stage B add animation, post, GUI expansion, review artifacts, and polish.

7. Browser validation gate

- Do not call a visual effect runnable or validated until it opens over `http://localhost/...`, the renderer initializes, no obvious runtime failure appears, and the effect renders in-browser.

8. Review artifact gate

- Do not force still-image comparison for every 3D scene.
- Record at least one task-appropriate review artifact before calling fidelity reviewed or complete.
- Good review artifacts include still pairs for framing-driven tasks, short clips or GIFs for motion-driven tasks, keyframe sequences for camera-driven tasks, and concise interaction notes when input behavior is central.
- Use stills to judge silhouette, palette, finish, and composition. Do not pretend a still image proves motion or interaction fidelity.

9. Fidelity failure protocol

- Diagnose fidelity failures in this order: reference understanding, route selection, missing critical modules, then parameter tuning.
- Do not default to "just tuning" before checking the first three layers.

10. Honest status labels

- Use `blocked-on-reference`, `planned`, `first-runnable-pass`, `browser-validated`, `evidence-reviewed`, `fidelity-pending`, and `faithful-remake-complete`.
- Do not call a remake complete without a task-appropriate comparison review.

11. Completion rule

- A remake is not complete until an active reference artifact and at least one task-appropriate current review artifact or review note exist, they have been compared using the right medium for the effect, and the remaining gaps are below the acceptance threshold or explicitly documented.

12. Operating principle

- The job is not merely to produce a plausible effect. The job is to stay evidentially aligned with the target.

## Escalate Material Choices With AskUserOption

Use `AskUserOption` only for decisions that change product intent, compatibility promises, maintenance cost, or acceptance criteria.

Do not ask the user to choose low-level implementation details that can be decided cleanly from the references and constraints.

Good `AskUserOption` prompts are coarse, downstream-shaping choices with 2 to 4 concrete options and a clear recommended default.

Bad `AskUserOption` prompts are:

- numeric tuning values
- pass-local implementation details
- choices already forced by the reference or browser target
- questions whose answers would not change the implementation plan

Ask at most 2 to 4 questions total. If more uncertainty exists, rank the decisions by impact and ask only the ones that materially change the route.

Use this matrix:

| Decision area | Ask when | Structured options | Default stance |
| --- | --- | --- | --- |
| Delivery intent | The user shared a reference but did not say whether the goal is exact match, constrained approximation, or inspired variant | `faithful-remake`, `approximation-from-limited-evidence`, `inspired-variant` | Prefer `faithful-remake` unless the reference gate fails or the user signals creative freedom |
| Renderer and compatibility contract | The effect could land on either `WebGPU` or `WebGL2`, and browser reach or maintenance cost is unclear | `desktop-webgpu`, `webgl2-first`, `desktop-webgpu-plus-webgl2-fallback` | Prefer `desktop-webgpu` for controlled demos and `webgl2-first` for public compatibility-sensitive demos |
| Authoring path strictness | A legacy shader port or low-level route is plausible, but it is unclear whether the user values maintainability over direct porting | `pure-tsl`, `tsl-plus-interop`, `raw-port` | Prefer `pure-tsl`, then `tsl-plus-interop`, then raw shader fallback |
| Device and performance target | The user has not stated whether the effect is desktop-only, laptop-balanced, or mobile-safe | `desktop-high`, `laptop-balanced`, `mobile-safe` | Prefer `laptop-balanced` when no hard requirement exists |
| Post fidelity | The look could be achieved either with a heavy post stack or a simpler base render plus light polish | `preserve-full-post-look`, `balanced-post`, `minimal-post` | Prefer the lightest post stack that still preserves the signature finish |
| Route arbitration | Two archetypes or pipelines preserve different non-negotiable traits from the references | `route-a`, `route-b`, `hybrid-follow-up` | Prefer one dominant route first; do not build a hybrid first pass unless the user explicitly wants it |
| Interaction scope | The reference suggests possible pointer, scroll, camera, or audio interaction but the required scope is unclear | `no-extra-interaction`, `pointer-only`, `rich-interaction` | Prefer `pointer-only` when interactivity affects the look but is not the main product requirement |

Each `AskUserOption` prompt should include:

- what decision is being made
- why it changes the implementation plan
- 2 to 4 options with explicit tradeoffs
- one recommended option
- what will happen if the user does not answer and the default is applied

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

If the user provides multiple references, do not average them blindly. Rank them first:

- primary reference: defines the core silhouette, motion language, and composition
- secondary reference: contributes one or two explicit modules such as post polish, surface treatment, or interaction
- accent reference: contributes palette, timing, or a narrow finish detail only

If two references conflict, preserve the primary reference and treat the other one as an optional module or a rejected route.

## Do Not Use The Full Workflow For

- Pure material or lighting exploration with no external reference to match.
- Isolated renderer or compatibility decisions with no reference-driven remake.
- Pure performance diagnosis or degradation planning.
- Pure post-chain design or feedback-buffer routing with no reference-driven remake.

## Deliver Required Outputs

Produce all of the following for each effect:

- A reference-access decision covering the accessible primary visual artifact, whether the faithful gate passed, and any blocker or downgrade reason.
- An explicit mode contract and honest status label.
- A chosen archetype and a short justification for why it fits better than the nearest alternative route.
- A visual evidence table that covers the critical visual modules and distinguishes evidence from unknowns.
- A classic-graphics baseline note whenever the completion-depth standard came from canonical graphics or game-industry references rather than the target artifact alone.
- A user-decision log whenever `AskUserOption` was used, including the question, options shown, selected answer, and impact on the plan.
- A measurable effect spec covering look, motion, interaction, invariants, and constraints.
- An implementation-surface decision covering authoring path, runtime renderer, resource model, pass topology, compatibility contract, and fallback path.
- A performance decision covering target device class, performance contract, dominant bottleneck, degradation ladder, and exposed controls.
- A post-processing decision covering post pipeline type, render-target layout, pass order, history requirement, and quality tiers when post is part of the look.
- A research package with an input set, normalized source roles, a link tree, extracted external links, comment takeaways, search terms, and a coverage table.
- A first-frame review checkpoint that records whether Stage A was close enough to continue.
- A runnable Three.js demo under `effects/<effect-slug>/`.
- A GUI with stable group names and the key tuning controls exposed.
- Browser-validation notes.
- A review-artifact note that states what medium was used for fidelity review and why it fits the task.
- A reference-vs-current comparison review, fidelity score, and explicit completion or pending gap statement.
- A `REPORT.md` that stays current after every material change.
- Optional optimization or degradation strategies that preserve the intended look.

## Follow This Workflow

### 1. Route the reference contract and effect archetype before coding

Before you expand research or choose templates, run the reference access gate, assign the mode contract, and then pick the archetype.

Use the routing table in [references/archetypes.md](references/archetypes.md).

At minimum, record:

- accessible primary visual artifact
- whether the reference access gate passed
- requested delivery intent and active mode contract
- current honest status label
- chosen archetype
- why it fits
- nearest rejected archetype
- primary reference
- secondary or accent references
- which traits are non-negotiable from each accepted reference
- which internal decision domains are expected to matter: implementation surface, post pipeline, performance contract

If the archetype is unclear, write `mixed` and explain what would settle it. If two materially different routes remain plausible after that analysis, use `AskUserOption` to let the user choose which tradeoff to preserve first. If the faithful route is blocked by missing evidence, say so explicitly and do not hide the downgrade behind the archetype writeup.

### 2. Model the effect before coding

Create the visual evidence table before implementation and use it to separate evidenced modules from inferred or unknown ones.

Break the target into:

- Shape: SDF, mesh deformation, particles, instances, volume, screen-space, or mixed passes.
- Surface and lighting: PBR, NPR, fresnel, edge light, shadows, fog, scattering.
- Motion: noise, flow field, feedback, physics, camera choreography, temporal phase shifts.
- Post: bloom, tone mapping, chromatic aberration, vignette, grain, depth cues.
- Interaction: pointer, touch, scroll, audio, or camera control.
- Invariants: color palette, density, silhouette, rhythm, composition, deformation range.
- Constraints: target devices, frame-rate goals, interactivity requirements, fallback allowance.

Write the effect spec in measurable terms such as element count, motion frequency, visible scale, buffer count, or whether history feedback is required. Read [references/visual-quality.md](references/visual-quality.md) when the look is ambiguous or difficult to quantify.

If completion depth is unclear but the primary reference is accessible, use the classic graphics baseline fallback to decide which modules a competent implementation normally includes. Use that baseline only for completion depth, never as a substitute for the target look itself.

If a critical module remains unknown, do not present the task as a faithful remake. Do not blind-fill scene dressing or style choices just because they feel plausible.

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

Treat the user's references or search cues as the starting point, not the full source of truth.

Use subagents for bounded research and evidence-gathering work when that work is parallelizable.

Good subagent tasks:

- parse one provided source and extract the core idea, parameters, outbound links, and likely pass structure
- turn one keyword-only or image-only input into search phrases, candidate references, and likely technique labels
- expand one branch of the link tree
- scan comments, issues, or discussions for pitfalls and workarounds
- survey engine-specific references for one module
- survey Three.js landing references for one module
- generate terminology and English-first search phrases for one module

Subagent outputs should be structured and easy to merge:

- source
- takeaway
- evidence vs inference
- open question
- recommended next link or next search

Keep these tasks local to the main agent:

- final archetype choice
- final implementation-surface choice
- final post and performance decisions
- conflict resolution between sources
- implementation plan ownership
- code edits and report synthesis

Do not split the same source branch across multiple subagents unless the branch is large enough to partition cleanly.

If the primary reference is inaccessible and no replacement artifact set exists, stop and request better evidence instead of continuing the faithful route.

If there are multiple references, unify them into one effect spec before coding:

- keep one primary silhouette and motion model
- import only the secondary modules that survive in the same render graph
- reject combinations that require mutually incompatible pipelines unless the user explicitly wants a hybrid
- if the references imply two different pipelines, implement the dominant route first and record the secondary route as a follow-up

- Search in this order:
  1. Mainstream or canonical graphics explanations and implementations: SIGGRAPH material, papers, talks, production notes, widely cited repos, or other authoritative references.
  2. Cross-engine rendering references: Unreal Engine, Unity, custom renderers, shader breakdowns, or engine-specific material graphs that clarify the visual method.
  3. Three.js landing guidance: decide how to reproduce the effect in the current `WebGPU` and TSL-oriented Three.js stack.
- Parse every directly inspectable input and extract the core idea, likely pipeline, important parameters, and implementation hints.
- For keywords, screenshots, image URIs, or local images, derive the external link tree before treating any single result as authoritative.
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

If the renderer or compatibility route is still ambiguous after research, use `AskUserOption` instead of silently picking a product contract the user may not want.

Use the internal implementation-surface references as the source of truth for this decision. Read [references/platform/interface-decision-tree.md](references/platform/interface-decision-tree.md), [references/platform/authoring-paths.md](references/platform/authoring-paths.md), [references/platform/backend-capability-matrix.md](references/platform/backend-capability-matrix.md), [references/platform/webgpu-resource-patterns.md](references/platform/webgpu-resource-patterns.md), [references/platform/pipeline-archetypes.md](references/platform/pipeline-archetypes.md), [references/platform/renderer-compatibility.md](references/platform/renderer-compatibility.md), and [references/platform/official-threejs-webgpu.md](references/platform/official-threejs-webgpu.md) based on the chosen route.

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

If the main open question is how much finish must survive versus how much cost can be cut, use `AskUserOption` to let the user choose the post-fidelity contract.

Use the internal post-pipeline references as the source of truth for this decision. Read [references/postfx/post-chain-selection.md](references/postfx/post-chain-selection.md), [references/postfx/render-target-patterns.md](references/postfx/render-target-patterns.md), [references/postfx/history-feedback.md](references/postfx/history-feedback.md), [references/postfx/quality-tiering.md](references/postfx/quality-tiering.md), and [references/postfx/official-three-postfx.md](references/postfx/official-three-postfx.md) based on the chosen route.

### 7. Scaffold the effect folder

Create the output under `effects/<effect-slug>/`.

- Use `scripts/init_effect.py` when you want a fast starting point.
- Prefer a canonical archetype profile when the effect is not mixed.
- Copy `assets/report-template.md` to `effects/<effect-slug>/REPORT.md` if the script is not used.
- Reuse `assets/templates/tsl-webgpu/`, `assets/templates/tsl-webgl2/`, or `assets/templates/legacy-glsl/` based on the selected path unless the project already has a stronger local setup.
- Keep the demo shell minimal: a plain HTML page, localhost browser preview, and no extra explanatory text in the body outside GUI or explicit error state.

#### Zero-build import-map constraints

For any HTML demo that uses import maps:

- Always include a base `"three"` mapping.
- If `"three/addons/"` is present, `"three"` must also be present.
- Do not assume `"three/webgpu"` or `"three/addons/"` alone are enough.
- Do not call the demo runnable if the base `"three"` mapping is missing.

Use this baseline unless the current Three.js release requires a documented change:

```json
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@<version>/build/three.module.js",
    "three/webgpu": "https://cdn.jsdelivr.net/npm/three@<version>/build/three.webgpu.js",
    "three/tsl": "https://cdn.jsdelivr.net/npm/three@<version>/build/three.tsl.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@<version>/examples/jsm/",
    "lil-gui": "https://cdn.jsdelivr.net/npm/lil-gui@<version>/+esm"
  }
}
```

Keep the folder self-contained and easy to run.

### 8. Implement in passes

Implement in this order:

1. Stage A, first frame: lock composition, horizon or silhouette, primary material relationships, main form profile, and the primary light and color read.
2. Review the first frame. If it is clearly off, stop and correct the route before expanding scope.
3. Stage B, motion and finish: align signature motion, palette, density, timing, layering, and interaction feel.
4. Add the post chain, review artifacts, and polish only after Stage A is close enough.
5. Optimize only after the look is close enough.

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
- Verify the browser validation gate over `http://localhost/...`: renderer initialized, no obvious runtime failure, and in-browser render confirmed.
- Save task-appropriate review artifacts under `review-artifacts/` with stable names when file-based evidence helps the task. Use stills for framing-heavy checks, clips or GIFs for motion-heavy checks, and notes when interaction behavior is the main open question.
- Score silhouette, motion, density, palette, and finish using [references/fidelity-rubric.md](references/fidelity-rubric.md).
- Run `scripts/capture_audit.py` after saving file-based review artifacts so the manifest and review summary stay current.
- Compare reference and current using the right review medium before calling the task complete.
- If the fidelity score is below the acceptance target, run the fidelity failure protocol in this order: reference understanding, route selection, missing critical modules, then parameter tuning.
- If the fidelity score is below the acceptance target, record the gap instead of calling the effect done.
- Record which modules stayed pure TSL and which ones required interop or raw shader fallbacks.
- Cross-check the final renderer, TSL, post, and node usage against current official Three.js docs and manual pages before you call the implementation done.
- Cross-check against the exact pinned runtime version in `assets/runtime-versions.json`, not just the latest dev examples. Do not transplant dev-branch API names into an older pinned runtime without verification.
- Use the honest status labels in the report and user-facing summary instead of vague progress language.
- Update `REPORT.md` with source notes, choices, open risks, and the latest change log entry.

#### Preview and runtime constraints

For zero-build browser demos:

- Never assume `file://` is a supported preview mode.
- Treat `http://localhost/...` as the default preview contract.
- Final user instructions must include a local HTTP server command.
- If preview was not validated over localhost, do not claim file-url compatibility.

Before calling a zero-build HTML demo runnable, verify all of the following:

1. the import map includes a base `"three"` entry
2. the intended preview mode is `http://localhost/...`, not `file://`
3. final user instructions include a local server command or equivalent localhost preview method

Do not treat the report as optional. Every meaningful edit must be reflected there.

## Use Bundled Resources

Load only the files that help the current task:

- [references/archetypes.md](references/archetypes.md): use for the initial archetype route and starter-profile choice.
- [references/research.md](references/research.md): use for source parsing, link-tree expansion, English search planning, and the research coverage gate.
- [references/visual-quality.md](references/visual-quality.md): use for effect-spec writing and visual self-checks.
- [references/fidelity-rubric.md](references/fidelity-rubric.md): use for visual acceptance scoring and artifact selection.
- `scripts/capture_audit.py`: use to generate `review-artifacts/manifest.json` and `review-artifacts/review.md` from saved file-based review artifacts when that evidence is useful.
- [references/platform/interface-decision-tree.md](references/platform/interface-decision-tree.md): use for workload classification and implementation routing.
- [references/platform/authoring-paths.md](references/platform/authoring-paths.md): use for `TSL`, interop, `WGSL`, and `GLSL` path selection.
- [references/platform/backend-capability-matrix.md](references/platform/backend-capability-matrix.md): use for renderer and authoring tradeoffs.
- [references/platform/version-compatibility.md](references/platform/version-compatibility.md): use for current repository version assumptions and upgrade checks.
- [references/platform/webgpu-resource-patterns.md](references/platform/webgpu-resource-patterns.md): use for choosing the GPU resource model.
- [references/platform/pipeline-archetypes.md](references/platform/pipeline-archetypes.md): use for pass topology selection.
- [references/platform/renderer-compatibility.md](references/platform/renderer-compatibility.md): use for browser target and fallback policy.
- [references/platform/official-threejs-webgpu.md](references/platform/official-threejs-webgpu.md): use to sanity-check the final code against current official Three.js guidance.
- [references/performance/device-targeting.md](references/performance/device-targeting.md): use for default device assumptions and target device classes.
- [references/performance/bottleneck-diagnosis.md](references/performance/bottleneck-diagnosis.md): use for naming the dominant bottleneck.
- [references/performance/degradation-playbook.md](references/performance/degradation-playbook.md): use for choosing the quality ladder.
- [references/performance/profiling-checklist.md](references/performance/profiling-checklist.md): use for the final performance sanity check.
- [references/postfx/post-chain-selection.md](references/postfx/post-chain-selection.md): use for deciding whether the look belongs in post at all.
- [references/postfx/code-patterns.md](references/postfx/code-patterns.md): use for concrete WebGL and WebGPU post-chain implementation patterns.
- [references/postfx/render-target-patterns.md](references/postfx/render-target-patterns.md): use for choosing the render-target layout.
- [references/postfx/history-feedback.md](references/postfx/history-feedback.md): use for deciding whether history is optional or required.
- [references/postfx/quality-tiering.md](references/postfx/quality-tiering.md): use for post quality ladders and exposed-safe controls.
- [references/postfx/official-three-postfx.md](references/postfx/official-three-postfx.md): use to sanity-check the final post approach against official Three.js guidance.
- [references/gui.md](references/gui.md): use for GUI grouping and parameter selection.
- `scripts/init_effect.py`: use to scaffold `effects/<effect-slug>/` from the included template.
- `assets/templates/`: use as the baseline starter matrix when a zero-build setup is appropriate.
- `assets/report-template.md`: use as the required report skeleton.

## Keep Decisions Explicit

State these decisions clearly in the report and the user-facing summary:

- Which primary visual artifact unlocked the task, whether the faithful gate passed, and whether the mode had to be downgraded.
- Which mode contract and honest status label are active.
- Which archetype was chosen and why.
- Which critical modules were evidenced, inferred, or still unknown.
- Which parts of the plan came from the target reference versus the classic graphics baseline.
- Which `AskUserOption` prompts were used, which options were shown, and how the answers changed the plan.
- What the effect is made of.
- Which techniques are required versus replaceable.
- Which authoring path was chosen and why.
- Which renderer, resource model, pass topology, and compatibility contract were chosen and why.
- Which target device class, performance contract, and degradation ladder were chosen and why.
- Which post pipeline type, render-target layout, history requirement, and pass order were chosen and why.
- Whether the first-frame review gate passed and what remained blocked after that checkpoint.
- Whether the browser validation gate passed.
- Which review artifact type was used for acceptance and why it was appropriate.
- What evidence was used for the fidelity score.
- Whether reference and current were reviewed with a task-appropriate comparison method, and what prevents `faithful-remake-complete` if the status is still pending.
- Which sources influenced the final plan.
- Which research branches were delegated to subagents and what they contributed.
- Which risks remain unresolved.
- Which switches preserve the look when performance drops.
