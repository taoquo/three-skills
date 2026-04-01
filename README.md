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

### `perf-doctor`

Use `perf-doctor` for explicit performance diagnosis. It is designed around current Three.js runtime routes and produces an evidence-based report instead of generic optimization advice.

#### `perf-doctor` Input Contract

English:

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

中文：

- 最小输入：
  - 出问题的页面、路由、场景或组件
  - 症状描述
  - 复现步骤
  - 大致目标设备类型
- 发现策略：
  - 不要求用户预先判断自己使用的是 `WebGLRenderer`、`WebGPURenderer`、R3F 或哪条后处理链路
  - `perf-doctor` 应先从仓库、代码或运行页面中自行识别 runtime route
  - 只有当某个缺失采样会实质影响结论时，才向用户补要数据
- 可选加速信息：
  - 渲染器线索，例如 `WebGLRenderer`、`WebGPURenderer`、`@react-three/fiber`
  - 后处理线索，例如 `EffectComposer`、`postprocessing`、`@react-three/postprocessing`、`RenderPipeline`
  - 测量数据，例如 `renderer.info`、帧时间、flame chart、pass timings
  - 视觉约束，例如“必须保留阴影”或“不能变糊”

### `shader-port`

Use `shader-port` when the source is a standalone shader or post-processing effect that needs an honest Three.js implementation path, fallback contract, and verification notes.

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
