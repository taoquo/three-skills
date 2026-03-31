# Codex Install

Expose this repository to Codex by linking the shared `skills/` directory:

```bash
git clone <this-repo> ~/.codex/three-skills
mkdir -p ~/.agents/skills
ln -s ~/.codex/three-skills/skills ~/.agents/skills/three-skills
```

After restarting Codex, the only discoverable skill in this repository should be `$replicator`.

The platform, post-processing, and performance decision frameworks are bundled inside `replicator` and are no longer separate public skills.
