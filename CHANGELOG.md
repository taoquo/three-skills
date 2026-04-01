# Changelog

All notable changes to this repository will be documented in this file.

The format is intentionally simple and repository-focused.

## [Unreleased]

- Removed the redundant `test/` mirror and simplified replicator validation to use `effects/` as the only checked-in example source.
- Added three focused public skills: `material-lab` for isolated look development, `perf-doctor` for performance diagnosis, and `shader-port` for shader translation work.
- Tightened `shader-port` around current Three.js TSL and WebGPU constraints, added an explicit TSL mapping reference, and made unsupported-case fallback reporting mandatory.

## [4.6.0] - 2026-04-01

- Formalized the public-repo baseline with `LICENSE`, contribution guidance, security policy, changelog, and GitHub collaboration templates.
- Aligned repository metadata on a single `4.6.0` version.
- Strengthened fixture validation to cover public example parity and artifact schema checks.
- Reconnected the public volumetric example to a real render pipeline and removed misleading dead controls.

## Historical Note

- Versions prior to `4.6.0` were shipped before changelog adoption and are only reflected in git history.
