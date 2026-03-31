# Installing Three Skills for Codex

Enable this repository in Codex through native skill discovery.

## Installation

### macOS / Linux

```bash
git clone https://github.com/taoquo/three-skills.git ~/.codex/three-skills

mkdir -p ~/.agents/skills
ln -s ~/.codex/three-skills/skills ~/.agents/skills/three-skills
```

### Windows (PowerShell)

```powershell
git clone https://github.com/taoquo/three-skills.git "$env:USERPROFILE\.codex\three-skills"

New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
cmd /c mklink /J "$env:USERPROFILE\.agents\skills\three-skills" "$env:USERPROFILE\.codex\three-skills\skills"
```

Restart Codex after installation.

## Verify

```bash
ls -la ~/.agents/skills/three-skills
```

You should see a symlink or junction that points at the repository `skills/` directory.

## Available Skill

- `replicator` — reference-driven Three.js effect recreation with archetype routing, implementation-surface decisions, post-pipeline design, and performance planning

## Updating

```bash
cd ~/.codex/three-skills && git pull
```

## Uninstalling

```bash
rm ~/.agents/skills/three-skills
```

Optionally delete the clone:

```bash
rm -rf ~/.codex/three-skills
```
