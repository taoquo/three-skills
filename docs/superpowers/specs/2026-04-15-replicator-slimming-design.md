# Replicator Slimming Design

**Date:** 2026-04-15

## Goal

Reduce `replicator` from a monolithic full-stack remake skill into a clearer reference-driven orchestrator, without changing its role as the main entry point for full effect reconstruction.

## Problem

`replicator` currently mixes four layers of responsibility in one `SKILL.md`:

- trigger conditions
- hard gates and completion rules
- specialist domain decisions
- execution detail and implementation guidance

This creates three concrete costs:

1. host-side skill selection is diluted by implementation detail
2. `replicator` duplicates specialist judgment that should live in other public skills
3. maintenance work on shader, material, and performance policy tends to spill back into `replicator`

## Design Principles

- Keep `replicator` as the entry skill for reference-driven remakes.
- Keep evidence gates, mode contracts, and fidelity review in `replicator`.
- Remove deep specialist policy from `replicator` when that policy already belongs to a dedicated skill.
- Prefer orchestration rules over embedded specialist workflows.
- Move detail into `references/` only when it is still genuinely part of `replicator`'s orchestration job.

## Responsibility Boundary

### `replicator` owns

- multimodal intake for remake tasks
- reference access gate
- mode contract: faithful remake, approximation, inspired variant
- archetype routing
- visual evidence table
- cross-source conflict resolution
- overall effect plan ownership
- final fidelity review and honest status reporting

### `replicator` does not own

- material-family classification and surface-route selection
- shader-source classification and port-route policy
- runtime-route discovery, instrumentation, bottleneck diagnosis, and degradation planning

### Specialist skill mapping

- escalate to `material-lab` when the main uncertainty is material model, lighting rig, scan cleanup, transmission, thickness, translucency, or SSS
- escalate to `shader-port` when the task includes a standalone shader source or when the main uncertainty is TSL fit, interop scope, backend contract, or raw fallback policy
- escalate to `perf-doctor` when the main uncertainty is frame budget, bottleneck diagnosis, device targeting, or quality ladder design

## Proposed `replicator` Structure

The rewritten `SKILL.md` should be reduced to these sections:

1. `Overview`
2. `When To Use`
3. `Hard Gates`
4. `What Replicator Owns`
5. `What Replicator Does Not Own`
6. `Escalation Rules`
7. `Workflow`
8. `Required Outputs`
9. `References To Load On Demand`

## Section-Level Rewrite Plan

### Keep mostly intact

- `Overview`
- `Accept Multimodal Inputs`
- `Enforce Evidence Gates`
- `Escalate Material Choices With AskUserOption`
- `Route By Archetype First`
- `Do Not Use The Full Workflow For`

These sections already define the reference-driven orchestration contract.

### Compress heavily

#### `Deliver Required Outputs`

Keep only repository-level deliverables:

- reference-access decision
- mode contract
- archetype choice
- visual evidence table
- effect spec
- specialist decision log when escalation happened
- runnable demo
- browser validation note
- fidelity review note
- current `REPORT.md`

Remove subdomain-specific output contracts such as full performance tables or shader route taxonomies.

#### `Follow This Workflow`

Reduce the current long execution ladder to a compact orchestration flow:

1. lock evidence and active mode
2. route dominant archetype
3. write visual evidence table
4. identify specialist branches
5. resolve material, shader, or performance uncertainty through the dedicated skill when needed
6. implement the dominant route
7. run browser validation and fidelity review
8. update `REPORT.md`

### Remove from top-level `SKILL.md`

These sections should no longer appear as full internal policy blocks:

- detailed TSL fit rules
- detailed implementation-surface decision trees
- detailed post-pipeline decision trees
- detailed performance diagnosis and degradation instructions
- detailed import-map boilerplate
- detailed GUI naming catalogs

If any of these remain important, they should be referenced as optional support material rather than embedded as required top-level workflow.

## Reference Reorganization

### Keep as active `replicator` references

- archetype routing
- research intake and link-tree expansion
- visual quality framing
- fidelity rubric
- review artifact guidance

### Downgrade to on-demand support references

- platform routing details
- backend capability details
- post-processing implementation details
- performance diagnosis details

These references may stay in `skills/replicator/references/`, but the top-level skill should no longer read like a full restatement of them.

## Rewritten Escalation Rules

The new `replicator` should include direct trigger rules such as:

- If the remake is blocked by surface realism or lighting interpretation, use `material-lab`.
- If the remake is blocked by standalone shader logic or authoring-route ambiguity, use `shader-port`.
- If the remake is visually close but blocked by budget, bottleneck, or degradation uncertainty, use `perf-doctor`.

These rules should be short, explicit, and written as routing conditions, not as mini versions of the downstream skill workflow.

## Non-Goals

- Do not merge the public skills into one meta-skill.
- Do not remove `replicator` as the main remake entry point.
- Do not rewrite fixture schemas or helper scripts in this design phase.
- Do not force multi-skill usage on trivial remakes that do not have material, shader, or performance ambiguity.

## Risks

### Too little slimming

`replicator` remains long and still competes with the specialist skills.

### Too much slimming

`replicator` loses the ability to independently handle straightforward remakes.

### Weak escalation wording

The agent keeps staying inside `replicator` because the triggers to route into specialist skills are vague.

## Mitigations

- keep evidence, archetype, and fidelity review in `replicator`
- remove only specialist policy, not orchestration policy
- write escalation rules as concrete blocking conditions
- keep support references available, but demote them from mandatory top-level reading

## Acceptance Criteria

- `skills/replicator/SKILL.md` is reduced substantially in length
- top-level `replicator` text no longer defines full shader-port route enums
- top-level `replicator` text no longer defines full performance-diagnosis workflow
- top-level `replicator` text no longer defines full material authoring-route workflow
- the rewritten skill still clearly answers:
  - when to use `replicator`
  - when not to use it
  - when to route into `material-lab`, `shader-port`, or `perf-doctor`
  - what the remake must still deliver

## Implementation Notes For The Later Plan

- rewrite `skills/replicator/SKILL.md` first
- avoid changing specialist skill bodies in the same step unless boundary wording needs a small sync
- validate repository links after any section move
- keep changes documentation-first before touching validation rules
