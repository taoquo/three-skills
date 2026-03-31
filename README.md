# Three Skills

Skills repository for reusable Codex-oriented Three.js workflows. The current flagship skill is `replicator`, and the repository is being expanded into a focused Three.js skill collection with explicit platform guidance for `TSL`, `WebGPU`, and `WebGL2`.

## Layout

- `skills/`: reusable skills, one folder per skill
- `plugins/`: optional heavier plugin packages
- `.codex/`: Codex-specific installation notes

## Available Skills

| Skill | Description |
| --- | --- |
| `replicator` | Analyze graphics references and recreate the effect in Three.js with a TSL-first workflow, backend selection, research notes, a runnable demo, GUI controls, and a required `REPORT.md`. |
| `platform` | Choose the right Three.js implementation surface for `TSL`, `WebGPU`, `WebGL2`, raw shaders, resource models, pass topology, and compatibility contracts before coding. |
| `performance` | Diagnose Three.js bottlenecks, choose a performance contract, target device class, and degradation ladder, and decide how to preserve the look when frame budget gets tight. |
| `postfx` | Design Three.js post-processing chains, render-target layouts, history or feedback pipelines, effect ordering, and quality tiers without overcomplicating the render graph. |

## Direction

This repository is moving from a single flagship skill toward a small set of focused Three.js skills.

Near-term target:

- `replicator`: reference-driven effect recreation
- `platform`: renderer, authoring-path, and interface decision rules
- `performance`: bottleneck diagnosis and degradation strategy
- `postfx`: post chain composition, history buffers, and render-target policy

The active architecture plan is documented in [docs/threejs-skill-architecture.md](./docs/threejs-skill-architecture.md).

## Replicator v3 Highlights

- Archetype-first routing: choose `material-study`, `scene-post`, `fullscreen-raymarch`, `instanced-particles`, or `feedback-trails` before implementation.
- `TSL-first`: prefer TSL for shader and material logic, then choose the runtime backend.
- Backend priority: choose the strongest `WebGPU` path first, then fall back only when needed.
- Legacy shaders remain allowed as a documented fallback, not the default path.
- Research order is explicit: mainstream graphics references first, engine cross-checks second, Three.js landing details last.
- Reporting now includes search logs, evidence vs inference, shortest convincing path, and a visual fidelity rubric.
- Template matrix under `skills/replicator/assets/templates/` supports:
  - `tsl-webgpu`
  - `tsl-webgl2`
  - `legacy-glsl`
- Final demo output should stay as a minimal HTML page with no decorative text outside GUI or explicit error state.

## Codex Installation

Clone the repo and symlink the `skills/` directory into a location Codex discovers:

```bash
git clone <this-repo> ~/.codex/three-skills
mkdir -p ~/.agents/skills
ln -s ~/.codex/three-skills/skills ~/.agents/skills/three-skills
```

See [`.codex/INSTALL.md`](./.codex/INSTALL.md) for a shorter explanation.

## Validation

Run the validator before publishing changes:

```bash
python3 scripts/validate_skills.py
```

For `replicator`, also run the scaffolder smoke test:

```bash
python3 scripts/smoke_test_replicator.py
```

And validate checked-in replicator fixtures under `test/`:

```bash
python3 scripts/validate_replicator_fixtures.py
```

When an effect has captures under `captures/`, refresh the pair manifest and review summary:

```bash
python3 skills/replicator/scripts/capture_audit.py test/volumetric-lighting-webgpu
```
