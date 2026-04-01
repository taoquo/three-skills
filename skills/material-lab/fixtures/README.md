# Material Lab Fixtures

This directory contains minimal runnable fixtures for the main `material-lab` branches.

All fixtures are zero-build and intended to be previewed over localhost from the repository root.

## Preview

```bash
python3 -m http.server 4173 -d .
```

## Fixtures

- [standard-vs-physical-vs-sss/README.md](standard-vs-physical-vs-sss/README.md): compare `MeshStandardMaterial`, `MeshPhysicalMaterial` transmission, and an SSS route on the same target
- [scanned-pbr-vs-scan-assisted-cleanup/README.md](scanned-pbr-vs-scan-assisted-cleanup/README.md): compare raw scan-like PBR inputs against scan-assisted cleanup on the same stock route
- [gltf-khr-materials-vs-materialx-route/README.md](gltf-khr-materials-vs-materialx-route/README.md): compare the `glTF + KHR_materials_*` asset route against the `MaterialX` route

## Operating Principle

Each fixture should prove one routing decision with the smallest honest sample. If a fixture needs a large scene or heavy custom pipeline to make its point, the fixture is probably not minimal enough.
