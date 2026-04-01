# Three Skills

[English](./README.md) | [简体中文](./README.zh-CN.md)

这是一个面向 Three.js 的可复用技能仓库，服务于不同 AI 编码助手的工作流。规范的技能源码统一放在 `skills/` 下；Codex、Claude Code、Cursor 和 OpenCode 的宿主元数据与安装说明分别放在 `.codex/`、`.claude/`、`.cursor-plugin/` 和 `.opencode/`。

## 仓库概览

当前仓库对外提供四个公开技能：

| 技能 | 对外名称 | 关注点 |
| --- | --- | --- |
| `replicator` | Three.js Replicator | 从 URL、截图、图片输入、关键词或混合参考资料出发，复刻参考驱动的视觉效果。 |
| `material-lab` | Three.js Material Lab | 以小范围原型研究材质、灯光和表面处理，而不是整套效果复刻。 |
| `perf-doctor` | Three.js Performance Doctor | 定位性能瓶颈，制定测量方案，并给出可维护的降级路径。 |
| `shader-port` | Three.js Shader Port | 将 Shadertoy、GLSL 或 WGSL 着色器逻辑迁移到当前可维护的 Three.js 实现路径。 |

仓库边界：

- `skills/` 是所有公开技能的唯一规范来源。
- `effects/` 放浏览器可预览的公开示例效果。
- `scripts/` 放仓库级校验脚本和 smoke test。
- 各宿主目录负责把安装说明和 marketplace 元数据与共享的 `skills/` 目录保持一致。

## 目录结构

| 路径 | 作用 |
| --- | --- |
| `skills/` | 公开技能本体，以及各自的 references、assets、agents 和 fixtures。 |
| `effects/` | 面向浏览器预览和验证的公开示例效果。 |
| `scripts/` | 仓库校验脚本和 replicator 的 smoke test。 |
| `.codex/` | Codex 安装说明。 |
| `.claude/` | Claude Code 安装说明，以及 `.claude/skills/` 下的本地镜像入口。 |
| `.claude-plugin/` | Claude marketplace 元数据。 |
| `.cursor-plugin/` | Cursor 插件元数据与安装说明。 |
| `.opencode/` | OpenCode 安装说明和包元数据。 |
| `docs/` | 不适合放在根 README 的仓库级文档。 |
| `plugins/` | 预留给更重的独立插件包；当前这里还没有正式发布内容。 |

## 技能说明

### `replicator`

`replicator` 用于完整的效果复刻工作流。它支持多模态输入，会先做效果原型路由，再确定实现表面、后处理链和性能约束，最后产出可运行 demo 和配套的 `REPORT.md`。

### `material-lab`

当问题比“完整复刻一个效果”更窄时，用 `material-lab`。它适合处理材质分类、灯光验证、扫描材质清理、透射、SSS 等偏表面与材质层面的实验。

### `perf-doctor`

`perf-doctor` 用于显式的性能诊断。它围绕当前 Three.js 运行时路径来组织分析，重点是基于证据输出结论，而不是泛化的“优化建议”。

### `shader-port`

当输入是独立着色器或后处理效果时，用 `shader-port`。它会给出可落地的 Three.js 迁移路线、明确的 fallback 合同，以及验证说明。

## 安装

所有宿主都应以共享的 `skills/` 目录作为唯一来源。

### Claude Code

```bash
claude plugin marketplace add https://github.com/taoquo/three-skills
claude plugin install three-skills
```

如果使用本地 checkout，这个仓库还提供了 `.claude/skills/<skill>` 镜像入口，统一回指到规范的技能目录。

完整说明见 [`.claude/INSTALL.md`](./.claude/INSTALL.md)，其中包含 marketplace 安装、本地镜像使用方式和维护者说明。

### Cursor

```bash
git clone https://github.com/taoquo/three-skills.git ~/.cursor/three-skills
```

将 Cursor 的 skills 路径指向：

```text
~/.cursor/three-skills/skills/
```

完整说明见 [`.cursor-plugin/INSTALL.md`](./.cursor-plugin/INSTALL.md)，其中包含 Windows 指引、校验方法和更新方式。

### Codex

```bash
git clone https://github.com/taoquo/three-skills.git ~/.codex/three-skills
mkdir -p ~/.agents/skills
ln -s ~/.codex/three-skills/skills ~/.agents/skills/three-skills
```

完整说明见 [`.codex/INSTALL.md`](./.codex/INSTALL.md)，其中包含 Windows 安装、校验步骤和卸载说明。

### OpenCode

```bash
git clone https://github.com/taoquo/three-skills.git ~/.three-skills
mkdir -p ~/.config/opencode/skills
ln -s ~/.three-skills/skills/* ~/.config/opencode/skills/
```

完整说明见 [`.opencode/INSTALL.md`](./.opencode/INSTALL.md)，其中包含校验、更新和 Windows 安装说明。

## 示例效果

当前仓库附带一个公开示例效果：

- [`effects/volumetric-lighting-webgpu/`](./effects/volumetric-lighting-webgpu/)：一个以 WebGPU 为优先路径的体积光场景，用作面向浏览器的参考实现

在仓库根目录下预览：

```bash
python3 -m http.server 4173 -d .
```

然后打开：

```text
http://localhost:4173/effects/volumetric-lighting-webgpu/
```

这些零构建示例应通过 `http://localhost/...` 预览，不要使用 `file://`。

## 校验

发布或提交变更前，先跑以下仓库级检查：

```bash
python3 scripts/validate_skills.py
python3 scripts/smoke_test_replicator.py
python3 scripts/validate_replicator_fixtures.py
```

覆盖范围：

- `validate_skills.py`：技能 frontmatter、仓库元数据、宿主支持文件，以及 Claude 本地镜像入口
- `smoke_test_replicator.py`：replicator 的规范脚手架预设
- `validate_replicator_fixtures.py`：`effects/` 下已提交的公开示例

如果某个效果在 `review-artifacts/` 下保存了文件化审阅产物，更新抓取后还要刷新 manifest 和审阅摘要：

```bash
python3 skills/replicator/scripts/capture_audit.py effects/volumetric-lighting-webgpu
```

## 仓库规范

- 许可证：[MIT](./LICENSE)
- 贡献说明：[CONTRIBUTING.md](./CONTRIBUTING.md)
- 安全策略：[SECURITY.md](./SECURITY.md)
- 发布历史：[CHANGELOG.md](./CHANGELOG.md)

公开发布使用 `vX.Y.Z` 标签，宿主清单和公开技能定义中的版本号需要保持一致。

## 贡献

改动应尽量保持小而明确，便于验证。优先更新 `skills/`、`effects/` 和 `scripts/` 下的规范来源，不要为了小改动再引入平行副本或额外抽象层。

提交 PR 前，请先阅读 [CONTRIBUTING.md](./CONTRIBUTING.md) 并执行上面的校验命令。
