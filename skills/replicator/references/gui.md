# GUI Conventions

## Table of Contents

1. Keep the GUI useful
2. Use stable groups
3. Choose domain-specific controls

## Keep the GUI useful

Expose the controls that help align the look or isolate artifacts. Do not dump every uniform into the GUI.

Favor:

- Parameters that change the look in an obvious way
- Parameters that help separate correctness issues from polish issues
- Parameters that are likely to be revisited while matching a reference

Mirror the GUI defaults in `REPORT.md`.

## Use stable groups

Always include these groups unless the effect is too simple to justify them.

### Renderer

Use for:

- `dpr`
- `exposure`
- `pause`
- `timeScale`
- AA or quality toggles when present

### Post

Use for:

- `bloomStrength`
- `bloomRadius`
- `bloomThreshold`
- output blend or mix controls

### Style

Use for:

- palette controls
- fog density
- vignette
- contrast
- grain
- glow or edge tint

### Animation

Use for:

- speed
- phase
- drag or inertia
- autoplay or reset actions

## Choose domain-specific controls

Add focused groups for the effect class.

### Raymarch

Expose:

- `maxSteps`
- `epsilon`
- `maxDistance`
- `shadowSoftness`
- `fogDensity`

### Noise

Expose:

- `frequency`
- `amplitude`
- `octaves`
- `lacunarity`
- `gain`

### Particles

Expose:

- `count`
- `spawnRate`
- `lifetime`
- `drag`
- `fieldStrength`

### Feedback

Expose:

- `decay`
- `mix`
- `blur`
- `persistence`

Keep group names and parameter names stable unless there is a strong reason to rename them. Stable naming makes the report, screenshots, and future tuning sessions easier to compare.
