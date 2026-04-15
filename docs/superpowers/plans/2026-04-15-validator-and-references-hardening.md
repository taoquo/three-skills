# Validator And References Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen `scripts/validate_skills.py` with better skill description and structure checks, and add a clear `replicator` references index that separates active reads from on-demand references.

**Architecture:** Add minimal, repo-specific validation rules rather than a generic lint framework. Cover the new rules with Python unit tests first, then add `skills/replicator/references/README.md` in the same vocabulary already used by the other public skills.

**Tech Stack:** Python, `unittest`, Markdown

---

### Task 1: Add Failing Validator Tests

**Files:**
- Create: `tests/test_validate_skills.py`
- Test: `tests/test_validate_skills.py`

- [ ] **Step 1: Write tests for the new description rules**
- [ ] **Step 2: Write a test for `references/README.md` as a required structure file**
- [ ] **Step 3: Run the tests and confirm they fail against the current validator**

### Task 2: Implement Validator Hardening

**Files:**
- Modify: `scripts/validate_skills.py`
- Test: `tests/test_validate_skills.py`

- [ ] **Step 1: Add focused helper functions for description and structure validation**
- [ ] **Step 2: Enforce the new rules inside `validate_skill()`**
- [ ] **Step 3: Run the unit tests and make them pass**
- [ ] **Step 4: Run `python3 scripts/validate_skills.py` against the repo**

### Task 3: Add Replicator References Index

**Files:**
- Create: `skills/replicator/references/README.md`
- Test: `scripts/validate_skills.py`

- [ ] **Step 1: Write the README using the same style as the other public skills**
- [ ] **Step 2: Separate “active reads” from “on-demand reference packs”**
- [ ] **Step 3: Re-run the validator to confirm link integrity**
