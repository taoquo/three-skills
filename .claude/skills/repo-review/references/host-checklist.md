# Host Support Checklist

Review these repository-level host surfaces together:

- `.codex/INSTALL.md`
- `.claude/INSTALL.md`
- `.claude/skills/replicator`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.cursor-plugin/INSTALL.md`
- `.cursor-plugin/plugin.json`
- `.opencode/INSTALL.md`
- `README.md`

Checks to apply:

- repository name is `three-skills`
- repository URL is `https://github.com/taoquo/three-skills`
- public skill count matches the `skills/` directory
- Claude local mirrors still point at canonical public skills
- Cursor plugin still points `skills` to `./skills/`
- install instructions do not contradict each other
