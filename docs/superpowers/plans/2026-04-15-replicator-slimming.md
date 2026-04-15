# Replicator Slimming Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `skills/replicator/SKILL.md` so `replicator` acts as a reference-driven remake orchestrator instead of embedding full material, shader, and performance specialist workflows.

**Architecture:** Keep evidence gates, mode contract, archetype routing, and fidelity review in `replicator`, but replace embedded specialist policy with short escalation rules and on-demand references. The implementation is documentation-only and should preserve link integrity and current repository validation behavior.

**Tech Stack:** Markdown, repository skill conventions, Python validator (`scripts/validate_skills.py`)

---

### Task 1: Rewrite The Top-Level Contract

**Files:**
- Modify: `skills/replicator/SKILL.md`
- Test: `scripts/validate_skills.py`

- [ ] **Step 1: Capture a backup of the current opening structure**

Run:

```bash
sed -n '1,220p' skills/replicator/SKILL.md
```

Expected: the current file still contains `Overview`, `Accept Multimodal Inputs`, `Enforce Evidence Gates`, `Escalate Material Choices With AskUserOption`, `Route By Archetype First`, and `Do Not Use The Full Workflow For`.

- [ ] **Step 2: Replace the current overview block with orchestrator-first wording**

Update the opening prose under `# Three.js Replicator` so it reads in this shape:

```md
## Overview

Recreate reference-driven effects with an evidence-first orchestration workflow: lock the reference contract, choose the dominant archetype, identify the specialist branches that matter, implement the dominant route, then validate fidelity honestly.

`replicator` remains the canonical full-remake entry point. It owns reference access, mode selection, archetype routing, cross-source alignment, and final fidelity review. It does not replace specialist skills for material routing, shader-port policy, or performance diagnosis.

Default stance:

- prefer visual fidelity over premature optimization
- prefer the smallest honest route that preserves the look
- escalate to a specialist skill when uncertainty is domain-specific rather than remake-wide
```

- [ ] **Step 3: Insert explicit ownership boundaries after `Route By Archetype First`**

Add these new sections immediately after the archetype section:

```md
## What Replicator Owns

- multimodal remake intake
- reference access gate
- mode contract
- archetype routing
- visual evidence table
- cross-source conflict resolution
- overall remake plan ownership
- final fidelity review and honest status reporting

## What Replicator Does Not Own

- material-family classification and surface-route selection
- shader-source classification and port-route policy
- runtime-route discovery, instrumentation, bottleneck diagnosis, and degradation planning

## Escalation Rules

- Use `material-lab` when the remake is blocked by material model, lighting interpretation, scan cleanup, transmission, translucency, thickness, or SSS decisions.
- Use `shader-port` when the remake includes a standalone shader source or when the main uncertainty is TSL fit, interop scope, backend contract, or raw fallback policy.
- Use `perf-doctor` when the remake is visually understood but blocked by frame budget, bottleneck diagnosis, device targeting, or degradation ladder design.
```

- [ ] **Step 4: Keep the hard gates intact but remove “internal decision modules” language**

Delete the old overview wording that says `replicator` includes internal implementation surface, post, and performance decision modules. Do not weaken any evidence-gate language in `Enforce Evidence Gates`.

- [ ] **Step 5: Validate that the file still parses and links cleanly**

Run:

```bash
python3 scripts/validate_skills.py
```

Expected: `[OK] validated 4 skill(s)`

- [ ] **Step 6: Commit the boundary rewrite**

Run:

```bash
git add skills/replicator/SKILL.md
git commit -m "docs: slim replicator contract"
```

Expected: one commit containing only the top-level contract rewrite.

### Task 2: Compress Outputs, Workflow, And Resource Loading

**Files:**
- Modify: `skills/replicator/SKILL.md`
- Test: `scripts/validate_skills.py`

- [ ] **Step 1: Replace `Deliver Required Outputs` with orchestration-level deliverables**

Rewrite that section so it keeps only this scope:

```md
## Deliver Required Outputs

Produce all of the following for each remake:

- reference-access decision
- active mode contract and honest status label
- chosen archetype and rejected alternative
- visual evidence table
- measurable effect spec
- specialist decision log when escalation happened
- runnable demo under `effects/<effect-slug>/`
- browser-validation note
- review-artifact note
- reference-vs-current fidelity review
- current `REPORT.md`
```

Do not keep full performance tables, shader route enums, or post-pipeline contract tables in this section.

- [ ] **Step 2: Replace the long `Follow This Workflow` ladder with a compact orchestrator workflow**

Rewrite the entire workflow section into this shape:

```md
## Workflow

1. Lock the reference access decision and active mode contract.
2. Route the dominant archetype and reject the nearest wrong route.
3. Build the visual evidence table and measurable effect spec.
4. Identify whether the main uncertainty is material, shader, performance, or general remake orchestration.
5. Resolve specialist uncertainty through the dedicated skill when needed.
6. Implement the dominant route.
7. Run browser validation and task-appropriate fidelity review.
8. Update `REPORT.md` with decisions, current status, and remaining gaps.
```

Delete the old subsections for:

- detailed technique-module routing
- detailed TSL fit and research execution
- detailed implementation-surface routing
- detailed post-pipeline routing
- detailed import-map boilerplate
- detailed GUI naming catalogs
- detailed performance diagnosis and degradation workflow

- [ ] **Step 3: Downgrade `Use Bundled Resources` to on-demand loading guidance**

Keep only the references that still belong to orchestration:

```md
## References To Load On Demand

- `references/archetypes.md`
- `references/research.md`
- `references/visual-quality.md`
- `references/fidelity-rubric.md`
- `scripts/capture_audit.py`
```

Then add a short note like:

```md
Load platform, post, or performance references only when the chosen route or specialist branch requires them. Do not restate those references as top-level mandatory workflow.
```

- [ ] **Step 4: Shorten `Keep Decisions Explicit` so it only covers orchestrator decisions**

Reduce that section to:

```md
## Keep Decisions Explicit

State these decisions clearly in the report and user-facing summary:

- which reference artifact unlocked the task
- which mode contract and status label are active
- which archetype was chosen and why
- which modules were evidenced, inferred, or unknown
- which specialist branches were escalated and why
- whether browser validation passed
- what medium was used for fidelity review
- what remains blocked before completion
```

- [ ] **Step 5: Run the validator after the compression pass**

Run:

```bash
python3 scripts/validate_skills.py
```

Expected: `[OK] validated 4 skill(s)`

- [ ] **Step 6: Commit the workflow compression**

Run:

```bash
git add skills/replicator/SKILL.md
git commit -m "docs: trim replicator workflow"
```

Expected: one commit containing only the deliverables/workflow/resource-loading rewrite.

### Task 3: Final Consistency Pass And Acceptance Check

**Files:**
- Modify: `skills/replicator/SKILL.md`
- Test: `scripts/validate_skills.py`

- [ ] **Step 1: Check the rewritten skill against the design acceptance criteria**

Run:

```bash
rg -n 'pure-tsl|tsl-plus-interop|legacy-webgl-raw|degradation ladder|MeshStandardMaterial|MeshPhysicalMaterial|MeshSSSNodeMaterial|post pipeline type|render-target layout' skills/replicator/SKILL.md
```

Expected: no matches for full specialist route enums or embedded specialist workflow phrases.

- [ ] **Step 2: Verify the top-level structure reads like an orchestrator**

Inspect the final file:

```bash
sed -n '1,260p' skills/replicator/SKILL.md
sed -n '261,420p' skills/replicator/SKILL.md
```

Expected:

- ownership and non-ownership are explicit
- escalation rules are present
- `replicator` still answers when to use it and what it must deliver
- specialist skill bodies are not redefined here

- [ ] **Step 3: Run the repository validator one final time**

Run:

```bash
python3 scripts/validate_skills.py
```

Expected: `[OK] validated 4 skill(s)`

- [ ] **Step 4: Review the final diff size**

Run:

```bash
git diff --stat
wc -l skills/replicator/SKILL.md
```

Expected:

- the file is materially shorter than before
- the remaining diff is limited to `skills/replicator/SKILL.md` unless a tiny wording sync was explicitly needed

- [ ] **Step 5: Commit the final consistency pass**

Run:

```bash
git add skills/replicator/SKILL.md
git commit -m "docs: finalize replicator slimming"
```

Expected: one final documentation commit for the acceptance cleanup.
