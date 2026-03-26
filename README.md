# Three Skills

Skills repository for reusable Codex-oriented workflows. The repo follows a simple structure inspired by the MiniMax `skills` repository: the root holds repository metadata and install notes, and the actual skills live under `skills/`.

## Layout

- `skills/`: reusable skills, one folder per skill
- `assets/`: shared repository-level assets
- `plugins/`: optional heavier plugin packages
- `.codex/`: Codex-specific installation notes

## Available Skills

| Skill | Description |
| --- | --- |
| `replicator` | Analyze graphics references and recreate the effect in Three.js, with research notes, a runnable demo, GUI controls, and a required `REPORT.md`. |

## Codex Installation

Clone the repo and symlink the `skills/` directory into a location Codex discovers:

```bash
git clone <this-repo> ~/.codex/three-skills
mkdir -p ~/.agents/skills
ln -s ~/.codex/three-skills/skills ~/.agents/skills/three-skills
```

See [`.codex/INSTALL.md`](./.codex/INSTALL.md) for a shorter explanation.

## Validation

Run the lightweight validator before publishing changes:

```bash
python3 scripts/validate_skills.py
```
