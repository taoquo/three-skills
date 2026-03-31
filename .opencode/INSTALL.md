# Installing Three Skills for OpenCode

Enable this repository in OpenCode by cloning it locally and symlinking each exported skill into OpenCode's skills directory.

## Installation

### macOS / Linux

```bash
git clone https://github.com/taoquo/three-skills.git ~/.three-skills

mkdir -p ~/.config/opencode/skills
ln -s ~/.three-skills/skills/* ~/.config/opencode/skills/
```

### Windows (PowerShell)

```powershell
git clone https://github.com/taoquo/three-skills.git "$env:USERPROFILE\.three-skills"

New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\opencode\skills"
Get-ChildItem "$env:USERPROFILE\.three-skills\skills" -Directory | ForEach-Object {
    New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.config\opencode\skills\$($_.Name)" -Target $_.FullName
}
```

Restart OpenCode after installation.

## Verify

Ask OpenCode to list available skills. This repository should expose `replicator`.

## Updating

```bash
cd ~/.three-skills && git pull
```

## Uninstalling

```bash
rm -rf ~/.config/opencode/skills/replicator
rm -rf ~/.three-skills
```
