# Profiling Checklist

Use this before locking a performance decision.

## Check 1: Device contract

- Is the default device class explicit?
- Does the implementation match that target honestly?

## Check 2: Bottleneck label

- Is the dominant bottleneck named explicitly?
- Does the chosen label match the effect shape?

## Check 3: First degradation step

- Is the first lever low-risk?
- Does it preserve the main silhouette, density, and motion character?

## Check 4: GUI safety

- Are exposed controls stable and understandable?
- Are destructive controls hidden by default?

## Check 5: Failure condition

- What frame rate or responsiveness threshold counts as failure?
- What visual loss is unacceptable even if performance improves?

## Rule

If any of these remain vague, the performance contract is not finished.
