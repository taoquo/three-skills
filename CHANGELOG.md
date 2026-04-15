# Changelog

All notable changes to this repository will be documented in this file.

The format is intentionally simple and repository-focused.

## [Unreleased]

## [4.6.4] - 2026-04-15

- Removed the remaining `workflow ... to/which/that` lint pattern in `validate_skills.py` so symptom-style trigger descriptions that mention broken CI workflows or startup failures are no longer rejected.
- Added regression tests covering valid trigger descriptions such as CI workflow publish failures and workflows that refuse to start on Windows.

## [4.6.3] - 2026-04-15

- Narrowed the skill-description lint in `validate_skills.py` so trigger-oriented descriptions that mention `output`, `deliver`, `workflow`, or `REPORT.md` as symptoms are no longer rejected.
- Added regression tests covering valid trigger descriptions that mention outputs, delivery wording, workflow migrations, and `REPORT.md` drift without summarizing workflow steps.

## [4.6.2] - 2026-04-15

- Slimmed `replicator` into a clearer remake orchestrator, keeping evidence gates and fidelity review while routing material, shader, and performance uncertainty into specialist skills.
- Synced the `replicator` wording across the skill file, agent prompt, and repository READMEs to reflect the new orchestrator boundary.
- Hardened `validate_skills.py` to enforce trigger-first skill descriptions and require `references/README.md` indexes for skill reference packs.
- Added a dedicated `replicator` references index that separates active reads from on-demand specialist reference packs.

## [4.6.1] - 2026-04-15

- Removed the redundant `test/` mirror and simplified replicator validation to use `effects/` as the only checked-in example source.
- Added three focused public skills: `material-lab` for isolated look development, `perf-doctor` for performance diagnosis, and `shader-port` for shader translation work.
- Tightened `shader-port` around current Three.js TSL and WebGPU constraints, added an explicit TSL mapping reference, and made unsupported-case fallback reporting mandatory.
- Rewrote all public skill frontmatter descriptions to use trigger-first `Use when...` wording for better host-side skill selection.

## [4.6.0] - 2026-04-01

- Formalized the public-repo baseline with `LICENSE`, contribution guidance, security policy, changelog, and GitHub collaboration templates.
- Aligned repository metadata on a single `4.6.0` version.
- Strengthened fixture validation to cover public example parity and artifact schema checks.
- Reconnected the public volumetric example to a real render pipeline and removed misleading dead controls.

## Historical Note

- Versions prior to `4.6.0` were shipped before changelog adoption and are only reflected in git history.
