# Three Skills

Skills repository for a single reusable Three.js workflow skill: `replicator`, displayed as `Three.js Replicator`. The repository ships host metadata and install notes for Codex, Claude Code, Cursor, and OpenCode, while keeping the actual skill source under `skills/`.

## Layout

- `skills/`: reusable skills, one folder per skill
- `effects/`: canonical public example effects generated with the Three.js Replicator workflow
- `plugins/`: reserved for future heavier plugin packages; currently unused
- `.codex/`: Codex installation notes
- `.claude/`: Claude Code local install notes plus local mirror entries that point at canonical skills
- `.claude-plugin/`: Claude Code plugin metadata
- `.cursor-plugin/`: Cursor plugin metadata and install notes
- `.opencode/`: OpenCode installation notes

## Available Skills

| Skill | Description |
| --- | --- |
| `replicator` | Analyze multimodal graphics references such as URLs, keywords, image URIs, screenshots, or mixed inputs and recreate the effect in Three.js with an archetype-first, TSL-first workflow, internal implementation-surface selection, post-pipeline design, performance-contract planning, research notes, a runnable demo, GUI controls, and a required `REPORT.md`. |

## Direction

This repository now exposes one public skill: `replicator` (`Three.js Replicator`).

Inside `replicator`, the workflow still makes three explicit decision classes:

- implementation surface: authoring path, renderer, resource model, pass topology, and compatibility contract
- post pipeline: post-chain type, render-target layout, pass order, and history requirement
- performance contract: target device class, dominant bottleneck, and degradation ladder

The knowledge for those domains now lives under [`skills/replicator/references/`](skills/replicator/references/).
The shared workflow contract for defaults, required sections, and example validation now lives under [`skills/replicator/assets/workflow-schema.json`](skills/replicator/assets/workflow-schema.json).

## Three.js Replicator v4.6 Highlights

- Multimodal input intake: start from a URL, keyword, image URI, screenshot, local image path, or a mixed reference set.
- Non-breaking naming refresh: keep the canonical skill id as `replicator` while presenting it as `Three.js Replicator`.
- Archetype-first routing: choose `material-study`, `scene-post`, `fullscreen-raymarch`, `instanced-particles`, or `feedback-trails` before implementation.
- Structured user-option escalation: ask the user to choose only when renderer, compatibility, fidelity, or scope tradeoffs would materially change the route.
- Research delegation: bounded source parsing, link-tree expansion, and pitfall scans can be split across subagents while final routing stays local.
- `TSL-first`: prefer TSL for shader and material logic, then choose the runtime backend.
- Backend priority: choose the strongest `WebGPU` path first, then fall back only when needed.
- Legacy shaders remain allowed as a documented fallback, not the default path.
- Research order is explicit: mainstream graphics references first, engine cross-checks second, Three.js landing details last.
- Reporting now includes search logs, evidence vs inference, shortest convincing path, and a visual fidelity rubric.
- Template matrix under `skills/replicator/assets/templates/` supports:
  - `tsl-webgpu`
  - `tsl-webgl2`
  - `legacy-glsl`
- Starter dependency versions are pinned in `skills/replicator/assets/runtime-versions.json`.
- Final demo output should stay as a minimal HTML page with no decorative text outside GUI or explicit error state.

## Repository Standards

- License: [MIT](./LICENSE)
- Contribution guide: [CONTRIBUTING.md](./CONTRIBUTING.md)
- Security policy: [SECURITY.md](./SECURITY.md)
- Release history: [CHANGELOG.md](./CHANGELOG.md)
- Public releases should use `vX.Y.Z` tags and keep repo metadata on the same version.

## Installation

### Claude Code

```bash
claude plugin marketplace add https://github.com/taoquo/three-skills
claude plugin install three-skills
```

For checkout-local workflows, the repository also exposes `.claude/skills/replicator` as a mirror entry that points at the canonical `skills/replicator`.

See [`.claude/INSTALL.md`](./.claude/INSTALL.md) for local checkout usage and maintainer notes.

### Cursor

```bash
git clone https://github.com/taoquo/three-skills.git ~/.cursor/three-skills
```

Point Cursor's skills path at `~/.cursor/three-skills/skills/`.

See [`.cursor-plugin/INSTALL.md`](./.cursor-plugin/INSTALL.md) for the full setup notes.

### Codex

```bash
git clone https://github.com/taoquo/three-skills.git ~/.codex/three-skills
mkdir -p ~/.agents/skills
ln -s ~/.codex/three-skills/skills ~/.agents/skills/three-skills
```

See [`.codex/INSTALL.md`](./.codex/INSTALL.md) for Windows notes and verification steps.

### OpenCode

```bash
git clone https://github.com/taoquo/three-skills.git ~/.three-skills
mkdir -p ~/.config/opencode/skills
ln -s ~/.three-skills/skills/* ~/.config/opencode/skills/
```

See [`.opencode/INSTALL.md`](./.opencode/INSTALL.md) for verification, updates, and Windows notes.

## Example Effect

The repository now includes a public example under [`effects/volumetric-lighting-webgpu/`](./effects/volumetric-lighting-webgpu/).

Preview it from the repository root with:

```bash
python3 -m http.server 4173 -d .
```

Then open:

```text
http://localhost:4173/effects/volumetric-lighting-webgpu/
```

Do not treat `file://` as a supported preview mode for the zero-build demos in this repository.

## Validation

Run the validator before publishing changes:

```bash
python3 scripts/validate_skills.py
```

This validator now checks both skill structure and the repository-level host support files under `.codex/`, `.claude/`, `.claude-plugin/`, `.cursor-plugin/`, and `.opencode/`, including the `.claude/skills/<skill>` mirror symlinks.

For `replicator`, also run the scaffolder smoke test:

```bash
python3 scripts/smoke_test_replicator.py
```

And validate the checked-in public examples:

```bash
python3 scripts/validate_replicator_fixtures.py
```

When an effect has file-based review artifacts under `review-artifacts/`, refresh the manifest and review summary:

```bash
python3 skills/replicator/scripts/capture_audit.py effects/volumetric-lighting-webgpu
```

## Contributing

Open an issue or pull request using the repository templates under `.github/`.

Before sending changes, follow [CONTRIBUTING.md](./CONTRIBUTING.md) and run the full validation set above.
