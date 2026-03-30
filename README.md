# Three Skills

Skills repository for reusable Codex-oriented Three.js workflows. The current flagship skill is `replicator`, which now uses a TSL-first workflow with backend-aware guidance for `WebGPU` and `WebGL2`.

## Layout

- `skills/`: reusable skills, one folder per skill
- `plugins/`: optional heavier plugin packages
- `.codex/`: Codex-specific installation notes

## Available Skills

| Skill | Description |
| --- | --- |
| `replicator` | Analyze graphics references and recreate the effect in Three.js with a TSL-first workflow, backend selection, research notes, a runnable demo, GUI controls, and a required `REPORT.md`. |

## Replicator v2 Highlights

- `TSL-first`: prefer TSL for shader and material logic, then choose the runtime backend.
- Backend priority: choose the strongest `WebGPU` path first, then fall back only when needed.
- Legacy shaders remain allowed as a documented fallback, not the default path.
- Research order is explicit: mainstream graphics references first, engine cross-checks second, Three.js landing details last.
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
