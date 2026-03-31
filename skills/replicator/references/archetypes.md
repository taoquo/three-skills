# Effect Archetypes

Choose the closest archetype before deep research or implementation.

## `material-study`

Use when:

- the reference is mostly about surface response, lighting behavior, or a hero object material
- the scene exists only to present the material
- post is optional polish, not the main look

Default route:

- `platform`: `single-pass-material`
- `postfx`: `none` or `scene-polish`
- `performance`: usually `balanced`

## `scene-post`

Use when:

- the base scene and its composition matter
- the final look clearly depends on bloom, grading, fog, or similar polish
- the post chain is important, but history feedback is not the main effect

Default route:

- `platform`: `scene-plus-post`
- `postfx`: `scene-polish` or `selective-post`
- `performance`: watch `post-chain` and `fill-rate`

## `fullscreen-raymarch`

Use when:

- the image is generated mostly from screen coordinates or camera rays
- SDF, volume, or procedural image generation dominates
- the main bottleneck is likely shader cost or ray steps

Default route:

- `platform`: `fullscreen-procedural`
- `postfx`: `fullscreen-stack` only if it materially helps
- `performance`: watch `ray-steps` and `fill-rate`

## `instanced-particles`

Use when:

- the look is driven by many particles, points, instances, or lightweight GPU entities
- density, field motion, or spawn behavior defines the effect

Default route:

- `platform`: `scene-plus-post` or `simulation-plus-render`
- `postfx`: `scene-polish`
- `performance`: watch `particle-count`

## `feedback-trails`

Use when:

- the current frame depends on previous frames
- temporal persistence, trails, recursive distortion, or accumulation define the look

Default route:

- `platform`: `feedback-loop`
- `postfx`: `feedback-post`
- `performance`: watch `bandwidth` and `post-chain`

## `mixed`

Use when:

- two archetypes are genuinely co-equal
- the dominant route is not obvious yet

Rule:

- still pick one dominant archetype for scaffolding
- explicitly name the secondary archetype in `REPORT.md`

## Quick Rejections

If the task is only:

- renderer selection -> use `platform`
- post-chain design -> use `postfx`
- performance tuning -> use `performance`

then `replicator` is not the right entry point.
