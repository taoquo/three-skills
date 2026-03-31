# PostFX Quality Tiering

Degrade the post stack in the order that least harms the look.

## Preferred order

1. Lower post resolution
2. Reduce blur radius or iteration count
3. Shorten secondary polish passes
4. Disable low-value finishing effects
5. Remove core signature effects only as a last step

## Safe exposed controls

Usually safe:

- bloom strength
- bloom threshold
- bloom radius within a limited range
- grain amount
- vignette amount
- chromatic aberration amount within a narrow range
- feedback decay when the effect is designed for it

## Usually hidden controls

Usually keep internal:

- history buffer topology changes
- aggressive pass count changes
- destructive resolution drops
- debug-only compositing views

## Rule

Expose only the controls that preserve the intended visual language across their normal range.
