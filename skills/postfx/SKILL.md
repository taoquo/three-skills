---
name: postfx
license: MIT
description: Design and validate Three.js post-processing pipelines. Use when the user needs a clear decision for pass order, render-target layout, selective compositing, history or feedback buffers, bloom or grading chains, or quality tiers for post-heavy effects.
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

# Three.js PostFX

## Overview

Use this skill to make post-processing decisions explicit before or during implementation.

The job is not just adding bloom. The job is to define a post pipeline that stays readable, controllable, and honest about its costs:

- post pipeline type
- render-target layout
- pass order
- history or feedback requirement
- quality tiers
- exposed versus hidden post controls

Prefer the shortest chain that preserves the intended look.

## Deliver Required Outputs

Produce a short decision summary with these fields:

| Field | Allowed values |
| --- | --- |
| Post pipeline type | `none`, `scene-polish`, `selective-post`, `feedback-post`, `fullscreen-stack` |
| Render-target layout | `backbuffer-only`, `single-intermediate`, `ping-pong-history`, `multi-target`, `selective-mask-chain` |
| Pass order | ordered list of passes |
| History requirement | `none`, `optional`, `required` |
| Quality tiers | ordered list of safe degradations |
| Exposed controls | safe user-facing controls |
| Hidden controls | debug-only or destructive controls |

Also record what should stay in base shading instead of the post chain.

## Follow This Workflow

### 1. Decide whether post is actually needed

First ask:

- is this look fundamentally in the material or lighting already?
- is post only finishing polish?
- is the signature look impossible without feedback or a compositing chain?

Use post only where it materially helps the look.

Read [references/post-chain-selection.md](references/post-chain-selection.md).

### 2. Choose the post pipeline type

Choose one of:

- `none`
- `scene-polish`
- `selective-post`
- `feedback-post`
- `fullscreen-stack`

Use the simplest type that still matches the effect.

### 3. Choose the render-target layout

Choose one explicit layout:

- `backbuffer-only`
- `single-intermediate`
- `ping-pong-history`
- `multi-target`
- `selective-mask-chain`

Read [references/render-target-patterns.md](references/render-target-patterns.md).

### 4. Decide whether history is optional or required

Be explicit:

- `none`
- `optional`
- `required`

If the current frame depends on previous frames for the real look, mark history as `required`.

Read [references/history-feedback.md](references/history-feedback.md).

### 5. Set pass order

Write the passes in order.

Typical examples:

- scene -> bloom -> tone map -> vignette
- scene -> mask -> selective bloom -> composite -> grade
- history update -> blur -> composite -> grade

Keep the chain readable and avoid redundant intermediate passes.

### 6. Set quality tiers

Define a short degradation ladder for the post stack.

Typical levers:

- reduce post resolution
- shorten the chain
- reduce blur radius or iteration count
- disable low-value polish passes

Read [references/quality-tiering.md](references/quality-tiering.md).

### 7. Validate against official Three.js guidance

Use official docs and examples as the final check for browser-facing post code.

Read [references/official-three-postfx.md](references/official-three-postfx.md).

## Keep These Rules

- Keep the base scene correct before leaning on post.
- Do not move core shape or lighting problems into post unless the reference clearly does so.
- Use history buffers only when the look actually depends on temporal persistence.
- Prefer one strong signature effect over a long chain of weak polish.
- If the post stack cannot survive degradation, the design is too fragile.

## Typical Routes

| Situation | Recommended route |
| --- | --- |
| Geometry scene with light bloom and grading | `scene-polish` + `single-intermediate` |
| Glow on only part of the scene | `selective-post` + `selective-mask-chain` |
| Trails, smear, recursive distortion, or temporal decay | `feedback-post` + `ping-pong-history` |
| Full-screen raymarch or procedural art with several screen-space passes | `fullscreen-stack` + `single-intermediate` or `ping-pong-history` |
| Look is already in the base render | `none` or minimal `scene-polish` |

## Use Bundled Resources

- [references/post-chain-selection.md](references/post-chain-selection.md): use for deciding whether the look belongs in post at all.
- [references/render-target-patterns.md](references/render-target-patterns.md): use for choosing the simplest workable render-target layout.
- [references/history-feedback.md](references/history-feedback.md): use for deciding whether temporal persistence is optional or required.
- [references/quality-tiering.md](references/quality-tiering.md): use for quality ladders and exposed-safe post controls.
- [references/official-three-postfx.md](references/official-three-postfx.md): use to validate the final post approach against official Three.js guidance.

## Keep Decisions Explicit

State these clearly in the final answer or report:

- whether post is core or polish
- what pipeline type was chosen
- what render-target layout was chosen
- whether history is required
- what the pass order is
- which post controls are safe to expose
- which quality tier should degrade first
