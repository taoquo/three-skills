# WebGPU TSL Path

## Use This Path When

- the effect is a good fit for TSL
- modern browser support is acceptable
- you want the strongest default path for current Three.js work

## Implementation Notes

- Start from a `WebGPU`-ready template.
- Keep the first pass simple and visually verifiable.
- Favor node composition over embedding large opaque shader blocks too early.
- Add post and polish only after the core look is stable.

## Risks

- runtime support may still be narrower than `WebGL2`
- debugging may be slower if too much custom logic is packed into one pass
- some imported legacy shader ideas may still need scoped fallback code

## Report Expectations

Record:

- why `WebGPU` was selected
- what stayed pure TSL
- what, if anything, needed interop or raw shader support
- what the `WebGL2` fallback would be
