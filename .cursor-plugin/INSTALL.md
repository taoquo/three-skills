# Installing Three Skills for Cursor

Enable this repository in Cursor by cloning it locally and pointing Cursor's skills path at the shared `skills/` directory.

## Installation

### macOS / Linux

```bash
git clone https://github.com/taoquo/three-skills.git ~/.cursor/three-skills
```

Set Cursor's skills path to:

```text
~/.cursor/three-skills/skills/
```

### Windows (PowerShell)

```powershell
git clone https://github.com/taoquo/three-skills.git "$env:USERPROFILE\.cursor\three-skills"
```

Set Cursor's skills path to:

```text
C:\Users\YOUR_USERNAME\.cursor\three-skills\skills\
```

Restart Cursor or reload the window after saving the path.

## Verify

```bash
find ~/.cursor/three-skills/skills -maxdepth 2 -name SKILL.md
```

You should see `skills/replicator/SKILL.md`.
You should also see `skills/material-lab/SKILL.md`, `skills/perf-doctor/SKILL.md`, and `skills/shader-port/SKILL.md`.

## Updating

```bash
cd ~/.cursor/three-skills && git pull
```

## Uninstalling

```bash
rm -rf ~/.cursor/three-skills
```
