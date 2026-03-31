# Degradation Playbook

Reduce quality in the order that least harms the signature look.

## Common ladder

1. Lower DPR or internal render scale
2. Reduce secondary post quality
3. Reduce simulation or field resolution
4. Reduce effect density such as particles, samples, or octaves
5. Simplify lighting or atmosphere details
6. Remove whole visual layers only as a last step

## Raymarch and volume effects

Preferred order:

1. lower DPR
2. reduce max steps
3. reduce shadow or AO step counts
4. reduce secondary fog or glow polish

Do not flatten the core silhouette first.

## Particle or simulation effects

Preferred order:

1. reduce count or simulation resolution
2. reduce trail length or persistence
3. simplify secondary post
4. reduce per-particle shading detail

Do not immediately remove motion character if density alone can solve the issue.

## Post-heavy scenes

Preferred order:

1. reduce post resolution
2. shorten the chain
3. reduce sample radius or iteration count
4. disable low-value polish effects

## Rule

Expose only the first few safe steps in the GUI.

Keep more destructive steps internal unless the user is explicitly debugging or benchmarking.
