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

When you open this repository in Claude Code, the local mirror entry below is already present:

```text
.claude/skills/replicator -> ../../skills/replicator
```

That mirror keeps Claude's local skill discovery pointed at the canonical public skill source under `skills/`.

If you want to use `replicator` from another workspace, symlink the canonical skill into that workspace:

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

- `replicator` as a symlink to `../../skills/replicator`
- `repo-review` as a local helper skill directory

## Updating

```bash
git pull
```
