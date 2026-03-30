# Legacy Shader Fallback

## Purpose

Use this path only when TSL is not the best fit for a specific module or effect.

This is a scoped fallback, not the default workflow.

## Good Reasons To Fall Back

- a reference already ships a clean raw shader that would be expensive to translate
- TSL would hide backend-specific details that matter for fidelity
- a single module needs lower-level control while the rest of the effect can stay in TSL

## Rules

- keep the fallback local to the module that needs it
- do not rewrite the whole effect in legacy shaders without explaining why
- document the exact boundary between TSL and fallback code
- record the migration path back to TSL when one exists

## Report Expectations

Record:

- why the fallback was necessary
- which modules use it
- whether the fallback is temporary or likely permanent
- what the cleanest future migration path would be
