# Contributing

Thanks for contributing to `three-skills`.

## Scope

- Keep changes small, explicit, and production-friendly.
- Prefer improving the canonical sources under `skills/`, `effects/`, and `scripts/` instead of adding parallel variants.
- Do not add heavy dependencies or new abstraction layers for small workflow improvements.

## Local Validation

Run all four checks before opening a pull request:

```bash
python3 scripts/validate_skills.py
python3 scripts/smoke_test_replicator.py
python3 scripts/validate_replicator_fixtures.py
python3 scripts/validate_perf_doctor_fixtures.py
```

If you touch capture artifacts, also refresh them:

```bash
python3 skills/replicator/scripts/capture_audit.py effects/volumetric-lighting-webgpu
python3 skills/replicator/scripts/capture_audit.py test/volumetric-lighting-webgpu
```

## Pull Request Expectations

- Describe the user-visible outcome, not just the files changed.
- Keep public examples under `effects/` aligned with checked-in fixtures under `test/`.
- Update README, install docs, or metadata when behavior or versioned packaging changes.
- Do not merge changes that leave the public example or fixture set in a drifting state.

## Commit Message Convention

Use short, imperative commit messages with a clear type prefix:

- `feat: add WebGL2 fallback template guidance`
- `fix: align public effect metadata with fixture schema`
- `docs: add installation and contribution guidance`
- `chore: cut v4.6.0 release`

Guidelines:

- Keep the subject line under about 72 characters.
- Use one commit for one coherent change.
- Reserve `chore: cut vX.Y.Z release` for release-only commits.
- Do not use version-only release commits for feature work.

## Versioning

This repository now uses `vX.Y.Z` tags for public releases and keeps the same semantic version across:

- `skills/replicator/SKILL.md`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.cursor-plugin/plugin.json`
- README release highlights and changelog entries
