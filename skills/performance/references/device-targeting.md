# Device Targeting

Use one explicit target device class.

## `desktop-high`

Use when:

- the work is a premium demo or controlled environment
- the effect depends on high density, deep post, or expensive simulation

## `desktop-mid`

Use when:

- the work still targets desktops first
- some degradation is acceptable
- the goal is broad modern desktop coverage without chasing low-end laptops

## `laptop-balanced`

Use when:

- the user gives no strict requirement
- the work should feel reasonable on common laptops
- the effect can tolerate a controlled quality ladder

This is the default class for this repository.

## `mobile-safe`

Use when:

- broad public compatibility matters
- the scene must survive narrow thermal and power budgets
- the quality ladder must be aggressive and predictable

## Rule

Do not describe support vaguely.

Pick one default device class, then describe any premium or degraded variants around it.
