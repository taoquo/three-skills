# Codex Install

Expose this repository to Codex by linking the shared `skills/` directory:

```bash
git clone <this-repo> ~/.codex/three-skills
mkdir -p ~/.agents/skills
ln -s ~/.codex/three-skills/skills ~/.agents/skills/three-skills
```

After restarting Codex, the skills in `skills/` should be discoverable by explicit name, for example `$replicator`.
