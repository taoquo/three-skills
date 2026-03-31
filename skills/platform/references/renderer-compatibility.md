# Renderer Compatibility

Use an explicit compatibility contract.

## `desktop-webgpu`

Use when:

- the task is a desktop-first demo, prototype, or controlled environment
- there is no hard requirement for broad browser reach
- the effect benefits materially from the WebGPU path

## `desktop-webgpu-plus-webgl2-fallback`

Use when:

- the premium path is worth keeping
- a fallback is still useful
- approximate parity is acceptable

Record where the fallback degrades:

- lower effect density
- fewer passes
- simpler simulation
- reduced post

## `webgl2-first`

Use when:

- public compatibility matters more than renderer novelty
- the effect still lands cleanly on `WebGL2`
- the team wants one stable implementation path

## Rule

Do not promise silent fallback.

If the fallback changes the look or behavior in a meaningful way, write that down as part of the contract.
