# Validation Commands

Use these commands from the repository root:

```bash
python3 scripts/validate_skills.py
python3 scripts/smoke_test_replicator.py
python3 scripts/validate_replicator_fixtures.py
```

Expected outcomes:

- `validate_skills.py` reports the exported skills and host support files as valid
- `smoke_test_replicator.py` scaffolds all canonical profiles successfully
- `validate_replicator_fixtures.py` confirms checked-in fixture shape
