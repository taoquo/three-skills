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

#### `replicator` 常见使用方式

- 典型请求：
  - “把这个 URL、CodePen、视频或截图里的 hero effect、demo 或交互场景，尽可能忠实地复刻成 Three.js 版本。”
  - “我只有几张截图或一段社交媒体短视频。先帮我反推大概率用到的渲染技术，再做一个最诚实的近似复刻。”
  - “以这个 repo 或在线 demo 作为主参考，再从第二个参考里借用 post 质感，从第三个参考里保留交互线索。”
  - “从关键词或视觉方向出发，比如 volumetric god rays、liquid chrome blobs、stylized particle trails，先搜集参考，再把效果做出来。”
- 推荐输入：
  - 一个可访问的主参考，用来定义构图、运动语言和标志性模块，例如 URL、截图组、视频、本地图片，或代码仓库
  - 任何 secondary 或 accent reference，并注明它们各自只负责贡献什么
  - 如果已知，也建议说明交付意图：faithful remake、limited evidence 下的 approximation，或 inspired variant
  - 任何会实质影响路线的目标约束，例如 `WebGPU`、`WebGL2`、仅桌面端、需要 mobile-safe、允许重 post，或必须包含哪些交互
- 预期产出：
  - 一个可运行的 Three.js 效果 demo，通常落在 `effects/<effect-slug>/` 下，并暴露关键调参控制项
  - 一份 `REPORT.md`，记录 reference-access 决策、所选 archetype、实现路线、post 与性能决策、验证说明，以及当前 fidelity 状态
  - 一组 review artifacts 或对比说明，明确哪些部分已高保真匹配、哪些只是近似、哪些是有意不纳入本次范围

### `material-lab`

当问题比“完整复刻一个效果”更窄时，用 `material-lab`。它适合处理材质分类、灯光验证、扫描材质清理、透射、SSS 等偏表面与材质层面的实验。

#### `material-lab` 常见使用方式

- 典型请求：
  - “这个像蜡、玉、皮肤的表面应该走 `transmission` 还是严格的 `SSS`？帮我做一个最小可验证的 Three.js 原型。”
  - “这组扫描 PBR 材质发灰发脏，帮我清理 scan-driven 输入，并对比清理前后。”
  - “在同一套灯光下，对比 `MeshStandardMaterial`、`MeshPhysicalMaterial` 和 SSS 路线，看看哪个更适合这个表面。”
  - “在固定 HDRI 下把这个清漆金属、玻璃或半透明塑料材质调准，并说明关键调参抓手。”
- 推荐输入：
  - 一张或多张参考图、简短 turntable、扫描说明，或已有材质资产
  - 目标表面的描述，以及最重要的外观线索，例如边缘响应、粗糙度分布、背光、厚度感、扫描保真度
  - 如果已知，也可以提供渲染器或管线约束，例如 `WebGL2`、`WebGPU`、`R3F`、`glTF` 或 `MaterialX`
- 预期产出：
  - 一个最小可运行的 Three.js 材质研究原型，而不是完整场景复刻
  - 一份短报告，说明材质分类、选用路线、灯光假设、关键控制项，以及哪些部分是物理合理、哪些是有意的艺术化处理

### `perf-doctor`

`perf-doctor` 用于显式的性能诊断。它围绕当前 Three.js 运行时路径来组织分析，重点是基于证据输出结论，而不是泛化的“优化建议”。

#### `perf-doctor` 输入契约

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

当输入是独立着色器或后处理效果时，用 `shader-port`。它会给出可落地的 Three.js 迁移路线、明确的 fallback 合同，以及验证说明。

#### `shader-port` 常见使用方式

- 典型请求：
  - “把这个 Shadertoy fragment 迁移到当前 Three.js，优先走 TSL，并说明它是否还能跑在 `WebGL2` backend 上。”
  - “我有一个带 uniforms 和 textures 的旧 GLSL 全屏后处理 shader，帮我改写成 Three.js 版本，并写清楚资源映射。”
  - “把这段 WGSL 迁移到最诚实的 Three.js 路线里，并明确指出哪些部分不能干净移植。”
  - “这个旧 WebGL shader demo 或多 pass 效果到底能继续留在 TSL、只需要少量 interop，还是必须退回 raw WebGL？帮我判断并落地。”
- 推荐输入：
  - 权威的 shader 源输入，例如 Shadertoy URL、GLSL 文件、WGSL 片段，或旧 demo 代码
  - 定义目标效果的参考截图、录屏，或仍可运行的演示
  - 必需的 uniforms、textures、buffers、pass 顺序，以及已知交互输入，例如 time、mouse、audio、history、depth
  - 如果已有明确限制，也建议直接说明，例如目标必须是 `WebGPU`、`WebGL2`、`R3F`、要接入现有 post chain，或“不能接受 raw GLSL fallback”
- 预期产出：
  - 一个按最小诚实路线实现的 Three.js 可运行移植版本，通常先尝试纯 TSL，只有必要时才退到更窄的 fallback
  - 一份短报告，说明 source contract、所选路线、renderer 或 backend 合同、fallback 方案和验证结论
  - 一份资源与 pass 映射摘要，明确哪些部分被完整保留、哪些是近似处理、哪些暂不支持

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
python3 scripts/validate_perf_doctor_fixtures.py
```

覆盖范围：

- `validate_skills.py`：技能 frontmatter、仓库元数据、宿主支持文件，以及 Claude 本地镜像入口
- `smoke_test_replicator.py`：replicator 的规范脚手架预设
- `validate_replicator_fixtures.py`：`effects/` 下已提交的公开示例
- `validate_perf_doctor_fixtures.py`：`skills/perf-doctor/fixtures/` 下的规范诊断案例和报告形状示例

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
