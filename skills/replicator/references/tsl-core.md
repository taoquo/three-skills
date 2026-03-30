# TSL Core

## Why TSL Is The Default

Use TSL as the default shader authoring path for current Three.js work.

- It keeps shader logic close to Three.js material and node workflows.
- It can target both `WebGPU` and `WebGL2`.
- It reduces the need to maintain separate shader dialects for the same effect.
- It leaves room to evolve an effect without immediately dropping to raw shader code.

## Good Fits For TSL

Prefer TSL when the effect can be described as composable node modules:

- Material layering
- Fresnel, rim light, glow shaping
- Procedural color mixing
- Distortion or displacement driven by noise
- Screen-space post logic that still benefits from graph composition
- Effects that may need both `WebGPU` and `WebGL2` runtime paths

## How To Break The Effect Down

Before implementation, map the effect into modules:

- base shape or surface
- motion field
- lighting response
- atmosphere
- post chain
- interaction mapping

For each module, decide whether it is:

- pure TSL
- TSL plus `code()` or interop
- raw shader fallback

## When TSL Is A Bad Fit

Do not force TSL when the effect clearly wants lower-level control.

Common warning signs:

- the reference depends on an existing raw shader that is already clean and well-scoped
- the effect needs backend-specific shader code that would be obscured by a graph wrapper
- the time cost of translating into TSL exceeds the benefit

If you fall back, keep the fallback local and document why it exists.
