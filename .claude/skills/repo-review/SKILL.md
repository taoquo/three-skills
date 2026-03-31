---
name: repo-review
description: Review changes in the three-skills repository itself. Use when validating PRs, checking host support files, or reviewing modifications to the replicator skill and its packaging for Codex, Claude Code, Cursor, or OpenCode.
license: MIT
metadata:
  version: "1.0.0"
  category: tooling
---

# Repo Review

Use this local Claude skill when reviewing changes to this repository itself.

This is not a public exported skill. It exists only under `.claude/skills/` for maintainers working inside the repository checkout.

## Run The Required Checks

Run these before approving or finishing a change:

```bash
python3 scripts/validate_skills.py
python3 scripts/smoke_test_replicator.py
python3 scripts/validate_replicator_fixtures.py
```

## Review Focus

Check these areas in order:

1. Public skill integrity
   Ensure `skills/replicator/` remains the canonical source and that `.claude/skills/replicator` is only a mirror entry.
2. Host support integrity
   Verify `.codex/`, `.claude/`, `.claude-plugin/`, `.cursor-plugin/`, and `.opencode/` still describe the same repository and install shape.
3. Validation coverage
   Make sure new host files or conventions are enforced by `scripts/validate_skills.py`.
4. Example and scaffold health
   Confirm example artifacts and scaffold output still match the expected replicator shape.

## References

- [Host Checklist](references/host-checklist.md)
- [Validation Commands](references/validation-commands.md)
