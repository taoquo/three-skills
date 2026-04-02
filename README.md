# Three Skills

[English](./README.md) | [简体中文](./README.zh-CN.md)

Reusable Three.js skills for assistant-driven workflows. The canonical skill sources live under `skills/`; host-specific metadata and installation notes live under `.codex/`, `.claude/`, `.cursor-plugin/`, and `.opencode/`.

## Available Skills

This repository currently exposes four public skills:

| Skill | Human Name | Focus |
| --- | --- | --- |
| `replicator` | Three.js Replicator | Recreate reference-driven effects from URLs, screenshots, image inputs, keywords, or mixed source sets. |
| `material-lab` | Three.js Material Lab | Study materials, lighting rigs, and surface treatments in isolated prototypes. |
| `perf-doctor` | Three.js Performance Doctor | Diagnose bottlenecks, define measurement plans, and produce degradation ladders. |
| `shader-port` | Three.js Shader Port | Port Shadertoy, GLSL, or WGSL shader logic into current Three.js paths. |

Repository scope:

- `skills/` is the only canonical source for public skills.
- `effects/` contains browser-facing example effects generated from the repository workflows.
- `scripts/` contains repository validation and smoke-test tooling.
- Host-specific folders keep install notes and marketplace metadata aligned with the shared `skills/` directory.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `skills/` | Canonical public skills and their references, assets, agents, and fixtures. |
| `effects/` | Public example effects intended for browser preview and validation. |
| `scripts/` | Repository validators and replicator smoke tests. |
| `.codex/` | Codex installation notes. |
| `.claude/` | Claude Code installation notes plus local mirror entries under `.claude/skills/`. |
| `.claude-plugin/` | Claude marketplace metadata for this repository. |
| `.cursor-plugin/` | Cursor plugin metadata and installation notes. |
| `.opencode/` | OpenCode installation notes and package metadata. |
| `docs/` | Repository-level documentation that does not belong in the root README. |
| `plugins/` | Reserved for heavier standalone plugin packages. No package is published here yet. |

## Skill Guide

### `replicator`

Use `replicator` for full effect reconstruction work. It accepts multimodal inputs, routes the effect archetype, selects an implementation surface, defines post and performance contracts, and produces a runnable demo with a `REPORT.md`.

### `material-lab`

Use `material-lab` when the problem is narrower than a full remake: material classification, lighting validation, scan cleanup, transmission, SSS, or other surface-focused experiments.

#### `material-lab` Typical Usage

- Common requests:
  - "Should this wax, jade, or skin-like surface use `transmission` or true `SSS`? Build the smallest honest Three.js prototype."
  - "This scanned PBR set looks muddy. Clean up the scan-driven inputs and show the before or after difference."
  - "Compare `MeshStandardMaterial`, `MeshPhysicalMaterial`, and an SSS route for this surface under the same lighting rig."
  - "Dial in this coated metal, glass, or translucent plastic material under a fixed HDRI and explain which tuning levers matter."
- Recommended inputs:
  - one or more reference images, short turntable clips, scan notes, or existing material assets
  - the target surface description and what cue matters most, such as edge tint, roughness spread, backlighting, thickness, or scan fidelity
  - any renderer or pipeline constraint if already known, such as `WebGL2`, `WebGPU`, `R3F`, `glTF`, or `MaterialX`
- Expected outputs:
  - a minimal runnable Three.js material study instead of a full scene remake
  - a short report that states the material family, chosen route, lighting assumptions, major controls, and what is physically grounded versus art-directed

### `perf-doctor`

Use `perf-doctor` for explicit performance diagnosis. It is designed around current Three.js runtime routes and produces an evidence-based report instead of generic optimization advice.

#### `perf-doctor` Input Contract

- Minimum input:
  - page, route, scene, or component with the issue
  - symptom description
  - repro steps
  - approximate target device class
- Discovery policy:
  - do not require the user to identify `WebGLRenderer`, `WebGPURenderer`, R3F, or the post stack up front
  - `perf-doctor` should discover the runtime route from the repository, code, or running page first
  - ask for extra data only when one missing capture would materially change the recommendation
- Useful accelerators:
  - renderer hints such as `WebGLRenderer`, `WebGPURenderer`, or `@react-three/fiber`
  - post stack hints such as `EffectComposer`, `postprocessing`, `@react-three/postprocessing`, or `RenderPipeline`
  - measurements such as `renderer.info`, frame times, flame charts, or pass timings
  - visual constraints such as "keep shadows" or "do not blur"

### `shader-port`

Use `shader-port` when the source is a standalone shader or post-processing effect that needs an honest Three.js implementation path, fallback contract, and verification notes.

#### `shader-port` Typical Usage

- Common requests:
  - "Port this Shadertoy fragment to current Three.js with a TSL-first route and tell me whether it still works on a WebGL2 backend."
  - "I have a legacy GLSL fullscreen post shader with uniforms and textures. Rebuild it in Three.js and document the resource mapping."
  - "Translate this WGSL snippet into the narrowest honest Three.js path, and call out anything that cannot be ported cleanly."
  - "Take this old WebGL shader demo or multipass effect and tell me whether it can stay in TSL, needs scoped interop, or must fall back to raw WebGL."
- Recommended inputs:
  - the authoritative shader source, such as a Shadertoy URL, GLSL files, WGSL snippet, or legacy demo code
  - any reference screenshots, video captures, or running demos that define the expected output
  - required uniforms, textures, buffers, pass order, and known interaction inputs such as time, mouse, audio, history, or depth
  - explicit target constraints if they exist, such as `WebGPU`, `WebGL2`, `R3F`, post chain integration, or "must avoid raw GLSL fallback"
- Expected outputs:
  - a minimal runnable Three.js port using the smallest honest route, usually pure TSL first and a narrower fallback only when required
  - a short report with the source contract, chosen route, renderer or backend contract, fallback plan, and verification notes
  - a resource and pass mapping summary that states what was preserved exactly, approximated, or left unsupported

## Installation

Use the shared `skills/` directory as the source of truth for every host integration.

### Claude Code

```bash
claude plugin marketplace add https://github.com/taoquo/three-skills
claude plugin install three-skills
```

For local checkout workflows, this repository also exposes `.claude/skills/<skill>` mirror entries that point back to the canonical skill folders.

See [`.claude/INSTALL.md`](./.claude/INSTALL.md) for marketplace usage, local mirrors, and maintainer notes.

### Cursor

```bash
git clone https://github.com/taoquo/three-skills.git ~/.cursor/three-skills
```

Set Cursor's skills path to:

```text
~/.cursor/three-skills/skills/
```

See [`.cursor-plugin/INSTALL.md`](./.cursor-plugin/INSTALL.md) for Windows notes, verification, and updates.

### Codex

```bash
git clone https://github.com/taoquo/three-skills.git ~/.codex/three-skills
mkdir -p ~/.agents/skills
ln -s ~/.codex/three-skills/skills ~/.agents/skills/three-skills
```

See [`.codex/INSTALL.md`](./.codex/INSTALL.md) for Windows instructions, verification steps, and uninstall notes.

### OpenCode

```bash
git clone https://github.com/taoquo/three-skills.git ~/.three-skills
mkdir -p ~/.config/opencode/skills
ln -s ~/.three-skills/skills/* ~/.config/opencode/skills/
```

See [`.opencode/INSTALL.md`](./.opencode/INSTALL.md) for verification, updates, and Windows instructions.

## Example Effect

The repository ships one public example effect today:

- [`effects/volumetric-lighting-webgpu/`](./effects/volumetric-lighting-webgpu/) — a WebGPU-first volumetric lighting scene kept as a browser-facing reference implementation

Preview from the repository root:

```bash
python3 -m http.server 4173 -d .
```

Then open:

```text
http://localhost:4173/effects/volumetric-lighting-webgpu/
```

Use `http://localhost/...`, not `file://`, for these zero-build demos.

## Validation

Run the repository checks before publishing changes:

```bash
python3 scripts/validate_skills.py
python3 scripts/smoke_test_replicator.py
python3 scripts/validate_replicator_fixtures.py
```

What they cover:

- `validate_skills.py`: skill frontmatter, repository metadata, host support files, and Claude local mirror entries
- `smoke_test_replicator.py`: canonical replicator scaffold presets
- `validate_replicator_fixtures.py`: checked-in public examples under `effects/`

If an effect has file-based review artifacts under `review-artifacts/`, refresh the manifest and review summary after capture updates:

```bash
python3 skills/replicator/scripts/capture_audit.py effects/volumetric-lighting-webgpu
```

## Repository Standards

- License: [MIT](./LICENSE)
- Contribution guide: [CONTRIBUTING.md](./CONTRIBUTING.md)
- Security policy: [SECURITY.md](./SECURITY.md)
- Release history: [CHANGELOG.md](./CHANGELOG.md)

Public releases use `vX.Y.Z` tags, and repository metadata should stay on the same version across the host manifests.

## Contributing

Keep changes small, explicit, and easy to validate. Prefer updating canonical sources under `skills/`, `effects/`, and `scripts/` instead of introducing parallel copies or extra abstraction layers.

Before opening a pull request, follow [CONTRIBUTING.md](./CONTRIBUTING.md) and run the validation commands above.
