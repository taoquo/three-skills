# Volumetric Lighting (Froxel-based) Research Summary

- Effect slug: `volumetric-lighting-webgpu`
- Effect archetype: `scene-post`
- Starter profile: `scene-post`
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
- Profile: `scene-post`
- Target environment: `desktop-first`
- Performance priority: `deferred until look is correct`
- Status: `first-runnable-pass`
- Mode contract: `approximation-from-limited-evidence`
- Reference access gate: `passed`
- Primary visual artifact: `forum thread visuals + official Three.js example + technical references`
- Classic graphics baseline: `used`
- First-frame review gate: `passed`
- Browser validation gate: `pending`
- Side-by-side review: `pending`

## Notes

- The shortest convincing path is the current `VolumeNodeMaterial`-based MVP, not the final froxel architecture.
- The intended long-term route is still froxel-style volume storage and multi-pass light integration.
- The current fixture is strong enough to validate control surfaces, scene composition, and core atmosphere.
- The original live demo is inaccessible, so this fixture is intentionally classified as `approximation-from-limited-evidence`.

## Suggested Route

- First pass: keep the scene-plus-post baseline stable, then upgrade toward froxel pre-integration later.
- Nearest rejected route: `fullscreen-raymarch`

## Suggested Modules

- scene composition
- participating media
- light integration
- volumetric composite
- denoise and polish

## Suggested Quality Ladder

- lower volumetric resolution
- reduce ray steps
- disable denoise
- reduce shadow quality
