# Three.js Replicator Skill

Skills repository for a single reusable Codex-oriented Three.js workflow: `replicator`. It packages reference-driven effect recreation together with internal implementation-surface, post-pipeline, and performance-contract decision frameworks for `TSL`, `WebGPU`, and `WebGL2`.

## Layout

- `skills/`: reusable skills, one folder per skill
- `plugins/`: optional heavier plugin packages
- `.codex/`: Codex-specific installation notes

## Available Skills

| Skill | Description |
| --- | --- |
| `replicator` | Analyze graphics references and recreate the effect in Three.js with an archetype-first, TSL-first workflow, internal implementation-surface selection, post-pipeline design, performance-contract planning, research notes, a runnable demo, GUI controls, and a required `REPORT.md`. |

## Direction

This repository now exposes one public skill: `replicator`.

Inside `replicator`, the workflow still makes three explicit decision classes:

- implementation surface: authoring path, renderer, resource model, pass topology, and compatibility contract
- post pipeline: post-chain type, render-target layout, pass order, and history requirement
- performance contract: target device class, dominant bottleneck, and degradation ladder

The knowledge for those domains now lives under [`skills/replicator/references/`](skills/replicator/references/).

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

See [`.codex/INSTALL.md`](./.codex/INSTALL.md) for a shorter explanation of the single-skill install model.

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
