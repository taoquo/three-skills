# WebGL2 Visual Defaults

## Table of Contents

1. Use the default render path
2. Configure the renderer
3. Configure the post chain
4. Choose degradations when needed

## Use the default render path

When the user does not give a hard performance target, favor visual stability over aggressive optimization.

Default to:

- WebGL2 if available
- Correct output color management
- Tone mapping with an explicit exposure control
- A post chain that ends with `OutputPass`
- HDR-capable intermediate render targets when the effect benefits from bloom or high-intensity highlights
- Stable AA or multisampling where it is available and worthwhile

State these decisions in the report:

- Whether WebGL2 was used
- Whether HDR targets were enabled
- Whether multisampled render targets were enabled
- Whether the post chain ended in `OutputPass`

## Configure the renderer

Start from this baseline:

```js
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = params.exposure;
renderer.setPixelRatio(Math.min(window.devicePixelRatio, params.dpr));
```

Prefer a capped DPR. On laptops and phones, uncontrolled DPR is often the easiest way to lose the frame budget without improving the look enough.

Use antialiasing or multisampling intentionally. For shader-heavy or raymarched effects, render cost often dominates, so a DPR cap plus post AA may outperform brute-force MSAA.

## Configure the post chain

Use a clear order:

1. Base render pass
2. Effect-specific passes
3. Bloom or blur passes
4. Color and output pass

Keep `OutputPass` last so tone mapping and sRGB output happen once, in one place.

When an HDR target is needed, prefer half-float over full-float unless the effect proves otherwise. Keep the chain as short as the look allows.

## Choose degradations when needed

When the user specifies frame-rate, device, or power constraints, lower cost in this order:

1. Cap DPR
2. Reduce post resolution
3. Reduce step counts or particle counts
4. Reduce feedback blur or sample count
5. Disable the least visible polish pass

Avoid visual regressions that destroy the identity of the effect. Document every degradation switch in the report with the expected quality impact.
