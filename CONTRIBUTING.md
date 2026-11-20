# Contributing to Madiator Audio Apps

This is an **unofficial** umbrelOS Community App Store maintained by **Madiator**.

- Prefer upstream-maintained images and official artwork.
- Keep `id: localmedia` and established `localmedia-...` app IDs unchanged.
- Use persistent app-owned data directories and Umbrel `folderAccess` for user music.
- Mount music **read-only by default**; justify writable media access for sync or tagging.
- Document mDNS/multicast requirements and peer-versus-server TCP ports. Do not use Docker port publishing for host-networked apps.
- Avoid `privileged: true`, broad host-device access, and Docker socket mounts unless demonstrably required.
- Keep README, changelog and app package versions consistent.
- Do not include personal IP addresses, local disk sizes, private devices, credentials, or real library file names.

## Verification

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_store.py
```

Validate YAML and Compose files, then test each changed app against a backed-up installation. Do not claim a release is hardware-tested without evidence.

Only original packaging and documentation are distributed under the repository's MIT license. Upstream software retains its own license.
