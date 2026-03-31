# __EFFECT_TITLE__ Replication Report

## Summary

- Goal:
- Status:
- Confidence:
- Effect archetype:
- Authoring path:
- Runtime renderer:
- Resource model:
- Pass topology:
- Compatibility contract:
- Target device class:
- Performance contract:
- Dominant bottleneck:
- Post pipeline type:
- Render-target layout:
- History requirement:
- Fallback path:

## Source Set

| URL | Type | Contribution |
| --- | --- | --- |
| `TODO` | `TODO` | `TODO` |

## Archetype Route

| Field | Choice | Notes |
| --- | --- | --- |
| Chosen archetype | `material-study/scene-post/fullscreen-raymarch/instanced-particles/feedback-trails/mixed` | `Why this route fits the effect` |
| Nearest rejected route | `TODO` | `Why it was not selected` |
| Supporting skills | `platform/postfx/performance` | `Which ones materially shaped the plan` |

## Link Tree

```text
[0] TODO - overall reference
  [1] TODO - technique explanation
    [2] TODO - implementation detail
      [3] TODO - pitfall or optimization note
```

## External Links

| Link | Type | Contribution |
| --- | --- | --- |
| `TODO` | `paper/repo/demo/discussion/doc` | `TODO` |

## Solution Hierarchy

| Priority | Source type | Candidate | Why it matters |
| --- | --- | --- | --- |
| `1` | `mainstream/paper/talk/canonical repo` | `TODO` | `TODO` |
| `2` | `UE5/Unity/custom renderer` | `TODO` | `TODO` |
| `3` | `Three.js landing path` | `TODO` | `TODO` |

## Comment Takeaways

| Source | Takeaway | Evidence |
| --- | --- | --- |
| `TODO` | `TODO` | `quote/paraphrase` |

## Terminology and Modules

| Module | Keywords | Why it matters |
| --- | --- | --- |
| `TODO` | `TODO` | `TODO` |

## Search Log

| Query | Why it mattered | Decision changed |
| --- | --- | --- |
| `TODO` | `TODO` | `TODO` |

## Evidence vs Inference

| Claim | Status | Evidence |
| --- | --- | --- |
| `TODO` | `evidenced/inferred/uncertain` | `TODO` |

## Shortest Convincing Path

- `TODO`

## Research Coverage

| Module | Principle source | Implementation source | Pitfall source | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| `TODO` | `TODO` | `TODO` | `TODO` | `covered/gap` | `TODO` |

## Effect Spec

- Shape:
- Surface and lighting:
- Atmosphere and post:
- Motion:
- Interaction:
- Invariants:
- Constraints:

## Implementation Surface Decision

| Field | Choice | Notes |
| --- | --- | --- |
| Authoring path | `pure-tsl/tsl-plus-interop/raw-wgsl/raw-glsl/dual-path` | `Why this path fits the task` |
| Runtime renderer | `webgpu-renderer/webgl-renderer/dual-renderer` | `Why this renderer was selected` |
| Resource model | `uniforms/instanced-attributes/sampled-textures/storage-buffer/storage-texture/render-target-history` | `Why this data model fits` |
| Pass topology | `single-pass-material/fullscreen-procedural/scene-plus-post/simulation-plus-render/feedback-loop/compute-plus-render` | `Why this pipeline shape fits` |
| Compatibility contract | `desktop-webgpu/desktop-webgpu-plus-webgl2-fallback/webgl2-first` | `What browser support this plan assumes` |
| Rejected options | `TODO` | `Why they were not selected` |
| Fallback path | `TODO` | `When to use it` |

## Implementation Surface Check

| Module | Authoring fit | Renderer dependency | Resource need | Fallback need | Notes |
| --- | --- | --- | --- | --- | --- |
| `TODO` | `pure-tsl/tsl-plus-interop/raw shader` | `shared/webgpu/webgl2` | `uniforms/textures/history/storage` | `none/partial/full` | `TODO` |

## Final Implementation Plan

| Module | Choice | Required or replaceable | Reason |
| --- | --- | --- | --- |
| `TODO` | `TODO` | `required/replaceable` | `TODO` |

## Technique Routing

| Module | Backend dependency | Required or replaceable | Notes |
| --- | --- | --- | --- |
| `TODO` | `WebGPU/WebGL2/shared` | `required/replaceable` | `TODO` |

## Pass Graph

| Pass | Inputs | Outputs | Notes |
| --- | --- | --- | --- |
| `TODO` | `TODO` | `TODO` | `TODO` |

## PostFX Decision

| Field | Choice | Notes |
| --- | --- | --- |
| Post pipeline type | `none/scene-polish/selective-post/feedback-post/fullscreen-stack` | `What kind of post stack this effect needs` |
| Render-target layout | `backbuffer-only/single-intermediate/ping-pong-history/multi-target/selective-mask-chain` | `How intermediates and masks are organized` |
| Pass order | `TODO` | `Ordered pass list` |
| History requirement | `none/optional/required` | `Whether prior frames are part of the real look` |
| Quality tiers | `TODO` | `Ordered degradation steps for the post stack` |
| Exposed post controls | `TODO` | `Safe user-facing post controls` |
| Hidden post controls | `TODO` | `Debug-only or destructive post controls` |

## Performance Decision

| Field | Choice | Notes |
| --- | --- | --- |
| Target device class | `desktop-high/desktop-mid/laptop-balanced/mobile-safe` | `What hardware class this plan targets by default` |
| Performance contract | `fidelity-first/balanced/fps-first` | `How look versus responsiveness is prioritized` |
| Dominant bottleneck | `fill-rate/ray-steps/particle-count/bandwidth/post-chain/cpu-driver/unknown` | `What first explains the cost` |
| Degradation ladder | `TODO` | `Ordered list of quality levers` |
| Exposed controls | `TODO` | `Safe user-facing knobs` |
| Hidden controls | `TODO` | `Debug-only or dangerous knobs` |

## GUI

| Group | Controls |
| --- | --- |
| `Renderer` | `TODO` |
| `Post` | `TODO` |
| `Style` | `TODO` |
| `Animation` | `TODO` |

## Performance and Degradation

| Switch | Default | Expected impact |
| --- | --- | --- |
| `TODO` | `TODO` | `TODO` |

## Profiling Notes

| Check | Status | Notes |
| --- | --- | --- |
| Device contract | `TODO` | `TODO` |
| Bottleneck confidence | `TODO` | `TODO` |
| First degradation step | `TODO` | `TODO` |
| GUI safety | `TODO` | `TODO` |

## Visual Acceptance

| Category | Score (0-2) | Gap | Notes |
| --- | --- | --- | --- |
| Silhouette | `TODO` | `TODO` | `TODO` |
| Motion | `TODO` | `TODO` | `TODO` |
| Density | `TODO` | `TODO` | `TODO` |
| Palette | `TODO` | `TODO` | `TODO` |
| Finish | `TODO` | `TODO` | `TODO` |

- Total fidelity score:
- Acceptance target:
- Reference captures:
- Current captures:

## Compatibility Notes

| Target | Status | Notes |
| --- | --- | --- |
| `Modern WebGPU browsers` | `TODO` | `TODO` |
| `WebGL2 fallback path` | `TODO` | `TODO` |

## Official Three.js Validation

| Official source | Decision confirmed | Notes |
| --- | --- | --- |
| `WebGPURenderer docs/manual/examples` | `TODO` | `TODO` |
| `TSL docs/examples` | `TODO` | `TODO` |

## Open Risks

- `TODO`

## Implementation Log

| Date | Change | Reason |
| --- | --- | --- |
| `TODO` | `TODO` | `TODO` |

## Change Log

| Date | Change | Notes |
| --- | --- | --- |
| `TODO` | `Initial report` | `Created from template` |
