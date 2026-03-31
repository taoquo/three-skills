# Volumetric Lighting (Froxel-based) Replication Report

## Summary

- Goal: Replicate the volumetric lighting effect described in the Three.js forum post, aiming for froxel-based volumetric lighting with physically grounded scattering, multiple light support, and better edge handling than the stock post-process approach.
- Status: MVP implemented with a post-process volumetric baseline. Froxel-based upgrade remains planned.
- Confidence: Medium-high. The research coverage is strong, but the current implementation still lands short of the intended froxel architecture.
- Effect archetype: `scene-post`
- Authoring path: `pure-tsl`
- Runtime renderer: `webgpu-renderer`
- Resource model: `uniforms`
- Pass topology: `scene-plus-post`
- Compatibility contract: `desktop-webgpu-plus-webgl2-fallback`
- Target device class: `desktop-mid`
- Performance contract: `balanced`
- Dominant bottleneck: `post-chain`
- Post pipeline type: `selective-post`
- Render-target layout: `single-intermediate`
- History requirement: `none`
- Fallback path: Keep the current post-process volumetric approach for WebGL2 or constrained WebGPU environments, with reduced quality and no compute-style froxel pre-integration.

## Source Set

| URL | Type | Contribution |
| --- | --- | --- |
| `https://discourse.threejs.org/t/volumetric-lighting-in-webgpu/87959` | discussion | Primary reference, froxel technique rationale, pass structure, and tradeoff discussion |
| `https://www.youtube.com/watch?v=SW30QX1wxTY` | talk | Hillaire 2020 sky and atmosphere rendering background |
| `https://research.nvidia.com/labs/rtr/approximate-mie/publications/approximate-mie.pdf` | paper | Mie scattering approximation reference |
| `https://threejs.org/examples/webgpu_volume_lighting.html` | example | Baseline Three.js volumetric implementation used for MVP landing |
| `https://github.com/mrdoob/three.js/pull/30530` | pull request | Three.js implementation details and current landing constraints |

## Archetype Route

| Field | Choice | Notes |
| --- | --- | --- |
| Chosen archetype | `scene-post` | The current browser-facing implementation is a conventional scene with a separate volumetric pass and post-style composition. |
| Nearest rejected route | `fullscreen-raymarch` | The effect is not a pure full-screen procedural scene; geometry, shadows, and scene composition still matter. |
| Internal decision domains | `implementation surface/post pipeline/performance contract` | The implementation-surface module defines the WebGPU path, the post-pipeline module shapes the compositing chain, and the performance-contract module keeps the volumetric pass honest. |

## Link Tree

```text
[0] https://discourse.threejs.org/t/volumetric-lighting-in-webgpu/87959 - overall reference and froxel rationale
  [1] https://www.youtube.com/watch?v=SW30QX1wxTY - atmospheric scattering background
  [1] https://research.nvidia.com/labs/rtr/approximate-mie/publications/approximate-mie.pdf - scattering approximation details
  [1] https://threejs.org/examples/webgpu_volume_lighting.html - current Three.js landing path
  [1] https://github.com/mrdoob/three.js/pull/30530 - implementation notes and constraints
  [2] Frostbite volumetric fog presentation - production volumetric patterns
  [2] SIGGRAPH 2014 volumetric fog paper - compute-style fog integration
  [2] SIGGRAPH 2015 unified volumetric rendering paper - multi-scattering context
```

## External Links

| Link | Type | Contribution |
| --- | --- | --- |
| `https://company-named.com/dev/prototypes/2025/11-09-shade-volumetrics-sponza/` | demo | Original live demo reference, currently inaccessible |
| `https://www.youtube.com/watch?v=SW30QX1wxTY` | talk | Atmosphere and LUT background |
| `https://research.nvidia.com/labs/rtr/approximate-mie/publications/approximate-mie.pdf` | paper | Scattering phase behavior |
| `https://threejs.org/examples/webgpu_volume_lighting.html` | example | Practical landing path for the MVP |
| `https://github.com/mrdoob/three.js/pull/30530` | pull request | Current Three.js volumetric implementation details |

## Solution Hierarchy

| Priority | Source type | Candidate | Why it matters |
| --- | --- | --- | --- |
| `1` | `mainstream/paper/talk/canonical repo` | Hillaire 2020, Wronski 2014, unified volumetric rendering papers | Establish the physically grounded volumetric model |
| `2` | `UE5/Unity/custom renderer` | Frostbite volumetric fog style froxel solutions | Show how production engines structure multi-pass volume lighting |
| `3` | `Three.js landing path` | `VolumeNodeMaterial` and WebGPU examples | Defines what can land cleanly in current Three.js |

## Comment Takeaways

| Source | Takeaway | Evidence |
| --- | --- | --- |
| Forum post #11 | Froxel storage avoids edge aliasing issues present in post-process-only volumetrics | direct quote about 3D texture and edge handling |
| Forum post #11 | Post-process volumetrics are expensive, alias at edges, and move bandwidth around rather than eliminating cost | precise paraphrase of the tradeoff explanation |
| Forum post #12 | The intended froxel approach splits into participating media integration, light integration, and final gather passes | direct quote about the 3-pass architecture |
| Forum post #12 | Polynomial integration improves energy conservation relative to a simple Riemann sum | direct quote about the integration method |
| Forum post #5 | HG, CS, and NVIDIA HG+D phase functions materially change the look | discussion summary from the phase-function comparison |

## Terminology and Modules

| Module | Keywords | Why it matters |
| --- | --- | --- |
| Froxel field | `frustum-aligned 3D texture`, `volume grid`, `froxel` | Intended final storage model |
| Participating media | `extinction`, `scattering`, `optical depth` | Defines physically grounded volume properties |
| Light integration | `in-scattering`, `shadow sampling`, `phase function` | Shapes the actual lighting inside the medium |
| Final gather | `view ray accumulation`, `transmittance`, `screen composite` | Browser-facing render path |
| Denoise and polish | `gaussian blur`, `tone mapping`, `bloom-like polish` | Current MVP finishing path |

## Search Log

| Query | Why it mattered | Decision changed |
| --- | --- | --- |
| `volumetric lighting froxel webgpu three.js` | Confirmed the Three.js landing path is still closer to post-process than full froxel pre-integration | Land MVP on `VolumeNodeMaterial` first |
| `approximate mie scattering nvidia pdf` | Clarified phase-function options and terminology | Keep phase function as a replaceable module |
| `volumetric fog froxel compute shader` | Confirmed froxel architecture is valid but heavier than current MVP path | Keep froxel approach as planned upgrade, not MVP |

## Evidence vs Inference

| Claim | Status | Evidence |
| --- | --- | --- |
| Froxel storage is the intended long-term direction for this effect | `evidenced` | forum discussion and cited production references |
| Current Three.js MVP should start with `VolumeNodeMaterial` rather than immediate custom froxel compute | `inferred` | official example exists, but exact forum implementation is not fully available |
| A WebGL2 fallback can preserve basic look but not full froxel parity | `inferred` | derived from renderer constraints and post-process fallback shape |
| Mobile or integrated-GPU performance for the final froxel path is still uncertain | `uncertain` | no measured fixture data yet |

## Shortest Convincing Path

- Use the current Three.js WebGPU volumetric example style as the MVP landing path.
- Match scene composition, light placement, density controls, and denoise behavior first.
- Treat the froxel-based multi-pass architecture as the next upgrade once the baseline look and controls are stable.

## Research Coverage

| Module | Principle source | Implementation source | Pitfall source | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| Froxel field | Hillaire talk, production volumetric references | forum post #11-13 | forum tradeoff discussion | `covered` | enough to plan the upgrade path |
| Participating media | Wronski 2014, volumetric rendering papers | forum post #12 | forum note about energy conservation | `covered` | current MVP still simplifies density |
| Light integration | forum post #12 | current MVP and forum notes | shadow and cost tradeoffs from forum | `covered` | good enough for baseline |
| Final gather | production volumetric references | `VolumeNodeMaterial` MVP | aliasing limitations from forum | `covered` | current landing path is proven, final path still deferred |
| Phase functions | NVIDIA Mie paper | forum post #5 | no direct Three.js implementation note | `covered` | replaceable module |
| Denoise and polish | official Three.js example | current MVP blur chain | post cost tradeoffs | `covered` | current approach is simple and debuggable |

## Effect Spec

- Shape: A scene-scale volumetric medium with fog-like density occupying a bounded region around hero geometry.
- Surface and lighting: Physically inspired scattering with point and spot lights, shadow interaction, and phase-driven volume response.
- Atmosphere and post: Volume contribution composited into the scene, then lightly denoised and tone mapped.
- Motion: Mostly static medium with controllable temporal evolution in density; lights and camera can move.
- Interaction: GUI controls for density, light intensity, ray steps, denoise, and exposure.
- Invariants: Visible shafts, readable light cones, stable density field, and atmospheric depth around the hero object.
- Constraints: Target modern WebGPU desktops first. Current MVP should stay debuggable and maintainable in plain browser code.

## Implementation Surface Decision

| Field | Choice | Notes |
| --- | --- | --- |
| Authoring path | `pure-tsl` | The MVP lands cleanly in current Three.js node workflows. |
| Runtime renderer | `webgpu-renderer` | The effect benefits from modern WebGPU examples and future froxel evolution. |
| Resource model | `uniforms` | Current MVP does not yet use storage or history resources. |
| Pass topology | `scene-plus-post` | Base scene render plus volumetric and blur/composite chain. |
| Compatibility contract | `desktop-webgpu-plus-webgl2-fallback` | Premium path is WebGPU; fallback should preserve only the simpler post-process look. |
| Rejected options | `raw-wgsl`, `compute-plus-render`, `webgl-renderer` | These are still valid later, but they add complexity before the MVP look is stable. |
| Fallback path | `VolumeNodeMaterial`-style post-process volumetrics with reduced quality | Honest fallback, not a full froxel equivalent. |

## Implementation Surface Check

| Module | Authoring fit | Renderer dependency | Resource need | Fallback need | Notes |
| --- | --- | --- | --- | --- | --- |
| Froxel field | `tsl-plus-interop` | `webgpu` | `storage/history` | `full` | planned upgrade, not MVP |
| Participating media | `pure-tsl` | `shared` | `uniforms/textures` | `partial` | current MVP uses simplified density |
| Light integration | `pure-tsl` | `shared` | `uniforms/textures` | `partial` | works in MVP path |
| Final gather | `pure-tsl` | `shared` | `textures` | `partial` | current MVP lands here |
| Denoise and polish | `pure-tsl` | `shared` | `textures` | `none` | stable current path |

## Final Implementation Plan

| Module | Choice | Required or replaceable | Reason |
| --- | --- | --- | --- |
| Scene baseline | Teapot + floor + point/spot lights | `required` | Provides stable visual reference and shadow interaction |
| Participating media field | Noise-driven density in `VolumeNodeMaterial` | `required` | Necessary MVP medium representation |
| Volumetric pass | Screen-space volume raymarch | `required` | Shortest browser-facing path |
| Denoise pass | Gaussian blur | `replaceable` | Low-risk polish step |
| Froxel upgrade | 3D volume pre-integration / compute-style path | `replaceable` | Target architecture after MVP parity improves |

## Technique Routing

| Module | Backend dependency | Required or replaceable | Notes |
| --- | --- | --- | --- |
| Scene baseline | `WebGPU/WebGL2/shared` | `required` | Ordinary scene work |
| Volumetric pass | `WebGPU/WebGL2/shared` | `required` | Current MVP works this way |
| Froxel field | `WebGPU` | `replaceable` | Deferred upgrade path |
| Denoise pass | `WebGPU/WebGL2/shared` | `replaceable` | Can be simplified or disabled |

## Pass Graph

| Pass | Inputs | Outputs | Notes |
| --- | --- | --- | --- |
| `scene` | geometry, materials, lights | scene color + depth | base scene render |
| `volumetric` | scene depth, density field, light data | volumetric lighting buffer | current MVP volume contribution |
| `denoise` | volumetric buffer | blurred volumetric buffer | optional polish |
| `composite` | scene color, volumetric buffer | final image | additively composes volume into scene |

## PostFX Decision

| Field | Choice | Notes |
| --- | --- | --- |
| Post pipeline type | `selective-post` | The volumetric contribution is treated as a separate composited layer, not just global scene polish. |
| Render-target layout | `single-intermediate` | Current MVP keeps the chain intentionally short. |
| Pass order | `scene -> volumetric -> denoise -> composite -> tone map` | Good enough for the baseline. |
| History requirement | `none` | Current MVP does not depend on temporal persistence. |
| Quality tiers | `reduce volumetric resolution -> disable denoise -> reduce ray steps -> reduce shadow quality` | Ordered by least visible damage first. |
| Exposed post controls | `denoiseStrength`, `denoise`, `resolution`, `exposure` | Safe for interactive tuning. |
| Hidden post controls | `pass layout changes`, `composite mode rewrites` | Too destructive for normal GUI use. |

## Performance Decision

| Field | Choice | Notes |
| --- | --- | --- |
| Target device class | `desktop-mid` | Current MVP is desktop-first but should not assume flagship hardware only. |
| Performance contract | `balanced` | Preserve the look while keeping obvious degradation levers available. |
| Dominant bottleneck | `post-chain` | Current MVP cost is dominated by the separate volumetric pass, denoise, and composite work. |
| Degradation ladder | `lower volumetric resolution -> reduce ray steps -> disable denoise -> reduce shadow map size` | Keeps the core scene and light shafts readable longer. |
| Exposed controls | `dpr`, `steps`, `resolution`, `denoise`, `denoiseStrength`, `exposure` | Useful without destroying the look immediately. |
| Hidden controls | `phase-function rewrites`, `pass removal`, `renderer path changes` | Better kept out of the normal GUI. |

## GUI

| Group | Controls |
| --- | --- |
| `Renderer` | `dpr`, `exposure`, `paused`, `autoRotate` |
| `Post` | `resolution`, `denoise`, `denoiseStrength` |
| `Style` | `smokeAmount`, `fogIntensity`, `background` |
| `Animation` | `speed`, `lightIntensity`, `spotIntensity` |
| `Raymarch` | `steps` |

## Performance and Degradation

| Switch | Default | Expected impact |
| --- | --- | --- |
| Volumetric resolution | `0.25` | Largest first-line post cost lever |
| Raymarch steps | `12` | Directly affects quality and cost |
| Denoise | `enabled` | Improves finish at extra post cost |
| Shadow map size | `1024` | Affects light quality and GPU work |

## Profiling Notes

| Check | Status | Notes |
| --- | --- | --- |
| Device contract | `partial` | Desktop-mid is reasonable, but no measured low-end data yet |
| Bottleneck confidence | `medium` | Current code shape suggests post-chain cost, but no formal capture yet |
| First degradation step | `good` | Resolution drop is the safest first move |
| GUI safety | `good` | Current controls are understandable and bounded |

## Visual Acceptance

| Category | Score (0-2) | Gap | Notes |
| --- | --- | --- | --- |
| Silhouette | `2` | `low` | Scene and hero objects read clearly |
| Motion | `1` | `medium` | The scene moves, but the full froxel behavior is not present |
| Density | `1` | `medium` | Volume density is convincing but still simplified |
| Palette | `2` | `low` | Warm shafts and cool background are already close |
| Finish | `1` | `medium` | Denoise helps, but final polish and edge quality still lag |

- Total fidelity score: `7/10`
- Acceptance target: `8/10`
- Reference captures: `not stored yet`
- Current captures: `not stored yet`

## Compatibility Notes

| Target | Status | Notes |
| --- | --- | --- |
| `Modern WebGPU browsers` | `supported` | Current MVP is aimed here |
| `WebGL2 fallback path` | `planned` | Simpler post-process fallback only |
| `Mobile devices` | `limited` | Final froxel path remains uncertain on mobile |

## Official Three.js Validation

| Official source | Decision confirmed | Notes |
| --- | --- | --- |
| `WebGPURenderer docs/manual/examples` | `current landing path` | Confirms the browser-facing WebGPU path |
| `TSL docs/examples` | `current landing path` | Confirms the node-based MVP approach |

## Open Risks

- The original live demo is not accessible, so some behavior is inferred from discussion and secondary references.
- The froxel-based upgrade path is not implemented yet, so the current MVP still inherits limitations of post-process volumetrics.
- Mobile and integrated-GPU viability remain uncertain.
- A future compute-style froxel implementation may require a materially different resource model than the current MVP.

## Implementation Log

| Date | Change | Reason |
| --- | --- | --- |
| `2026-03-29` | Initial research and planning | Started replication from the forum reference |
| `2026-03-29` | Landed MVP with `VolumeNodeMaterial` baseline | Needed a debuggable browser-facing starting point |
| `2026-03-31` | Migrated report to replicator v3 structure | Align fixture with current skill outputs |

## Change Log

| Date | Change | Notes |
| --- | --- | --- |
| `2026-03-29` | Initial report | Research phase completed |
| `2026-03-29` | Implemented MVP using post-process volumetric lighting | Based on the official Three.js example and adapted for this fixture |
| `2026-03-29` | Updated implementation plan | Documented the froxel upgrade path |
| `2026-03-31` | Upgraded report format | Added archetype route, evidence tracking, and visual acceptance scoring |
