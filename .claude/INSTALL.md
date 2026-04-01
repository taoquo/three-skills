# Installing Three Skills for Claude Code

This repository supports two Claude Code workflows:

- marketplace install for general use
- local checkout usage through `.claude/skills/`

## Marketplace Install

```bash
claude plugin marketplace add https://github.com/taoquo/three-skills
claude plugin install three-skills
```

This is the recommended path when you want the repository as a reusable plugin.

## Local Checkout Workflow

When you open this repository in Claude Code, the local mirror entries below are already present:

```text
.claude/skills/replicator -> ../../skills/replicator
.claude/skills/material-lab -> ../../skills/material-lab
.claude/skills/perf-doctor -> ../../skills/perf-doctor
.claude/skills/shader-port -> ../../skills/shader-port
```

Those mirrors keep Claude's local skill discovery pointed at the canonical public skill sources under `skills/`.

If you want to use any of these skills from another workspace, symlink the canonical skill into that workspace:

```bash
mkdir -p /path/to/target/.claude/skills
ln -s /absolute/path/to/three-skills/skills/replicator /path/to/target/.claude/skills/replicator
```

## Maintainer Helper

This repository also ships a maintainer-only local helper skill:

- `repo-review` under `.claude/skills/repo-review`

Use it when reviewing changes to this repository itself. It points maintainers at the repo validation scripts and the host-support checks.

## Verify

```bash
ls -la .claude/skills
```

You should see:

- `material-lab` as a symlink to `../../skills/material-lab`
- `perf-doctor` as a symlink to `../../skills/perf-doctor`
- `replicator` as a symlink to `../../skills/replicator`
- `shader-port` as a symlink to `../../skills/shader-port`
- `repo-review` as a local helper skill directory

## Updating

```bash
git pull
```
