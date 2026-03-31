---
name: performance
license: MIT
description: Diagnose Three.js performance constraints before or after implementation. Use when the user needs a clear decision for target device class, frame-budget tradeoffs, bottleneck diagnosis, degradation strategy, quality ladders, or which controls should be exposed to keep the intended look under load.
metadata:
  version: "1.0.0"
  category: threejs
  render_backends:
    - webgpu
    - webgl2
  shader_language: tsl
  skill_type: decision
  owns_templates: "false"
  owns_scaffolder: "false"
---

# Three.js Performance

## Overview

Use this skill to make performance decisions explicit.

The job is not only to say "optimize it". The job is to produce a concrete performance contract:

- target device class
- performance contract
- dominant bottleneck
- degradation ladder
- exposed versus hidden controls

Prefer simple, visually robust levers over fragile micro-optimizations.

## Deliver Required Outputs

Produce a short decision summary with these fields:

| Field | Allowed values |
| --- | --- |
| Target device class | `desktop-high`, `desktop-mid`, `laptop-balanced`, `mobile-safe` |
| Performance contract | `fidelity-first`, `balanced`, `fps-first` |
| Dominant bottleneck | `fill-rate`, `ray-steps`, `particle-count`, `bandwidth`, `post-chain`, `cpu-driver`, `unknown` |
| Degradation ladder | ordered list of quality levers |
| Exposed controls | controls safe to give the user |
| Hidden controls | controls that should stay internal unless debugging |

Also record stop conditions, such as minimum acceptable frame rate or maximum quality loss.

## Follow This Workflow

### 1. Set the target device class

Choose one explicit device target:

- `desktop-high`
- `desktop-mid`
- `laptop-balanced`
- `mobile-safe`

If the user gives no hard requirement, default to `laptop-balanced`.

Read [references/device-targeting.md](references/device-targeting.md).

### 2. Set the performance contract

Choose one explicit contract:

- `fidelity-first`: preserve the signature look and accept a narrower target
- `balanced`: preserve the look while exposing controlled degradations
- `fps-first`: simplify aggressively to maintain responsiveness

Do not leave this implicit.

### 3. Diagnose the dominant bottleneck

Classify the first bottleneck that meaningfully explains the problem:

- `fill-rate`
- `ray-steps`
- `particle-count`
- `bandwidth`
- `post-chain`
- `cpu-driver`
- `unknown`

Read [references/bottleneck-diagnosis.md](references/bottleneck-diagnosis.md).

### 4. Build the degradation ladder

Choose the cheapest quality drops that preserve the look best.

Typical levers:

- DPR or render scale
- ray step count
- particle count
- simulation resolution
- bloom or post quality
- noise octaves
- shadow softness or fog density

Read [references/degradation-playbook.md](references/degradation-playbook.md).

### 5. Decide what should be exposed

Expose controls that are safe, legible, and predictable.

Hide controls that:

- break the intended look too easily
- are only useful for debugging
- create unstable combinations

### 6. Validate with a short profiling checklist

Before finalizing, confirm:

- the likely bottleneck matches the implementation shape
- the first degradation step is low-risk
- the fallback contract is honest
- the GUI does not expose self-destructive controls by default

Read [references/profiling-checklist.md](references/profiling-checklist.md).

## Keep These Rules

- Prefer a small quality ladder over many tiny knobs.
- Degrade in the order that least harms the visual signature.
- Do not optimize before identifying the bottleneck class.
- Do not call a fallback equivalent if it materially changes motion, density, or atmosphere.
- If no bottleneck can be identified yet, say `unknown` and state what measurement is missing.

## Typical Routes

| Situation | Recommended first move |
| --- | --- |
| Heavy full-screen shader | lower DPR before rewriting shading logic |
| Raymarch or volume scene | reduce step count and max distance before changing the whole effect |
| Dense particle field | cut count or simulation resolution before touching color/lookdev |
| Bloom-heavy post chain | reduce post resolution or pass count before flattening the scene |
| CPU-heavy scene setup or per-frame object churn | reduce object churn, batching overhead, or GUI/event cost before shader rewrites |

## Use Bundled Resources

- [references/device-targeting.md](references/device-targeting.md): use for default device assumptions and device classes.
- [references/bottleneck-diagnosis.md](references/bottleneck-diagnosis.md): use for classifying the first meaningful bottleneck.
- [references/degradation-playbook.md](references/degradation-playbook.md): use for choosing quality ladders that preserve the look.
- [references/profiling-checklist.md](references/profiling-checklist.md): use for final validation before locking the contract.

## Keep Decisions Explicit

State these clearly in the final answer or report:

- which device class is being targeted
- what the performance contract is
- what the dominant bottleneck is
- which degradation lever comes first, second, and third
- which controls are safe to expose
- what minimum acceptable quality or frame rate defines failure
