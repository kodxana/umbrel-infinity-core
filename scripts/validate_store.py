#!/usr/bin/env python3
"""Lightweight checks for the Madiator umbrelOS Community App Store."""
from pathlib import Path
import sys
import yaml

root = Path(__file__).resolve().parents[1]
problems = []

def read(path):
    try:
        item = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(item, dict):
            return item
        raise ValueError("expected a mapping")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        problems.append(f"{path}: {exc}")
        return {}

store = read(root / "umbrel-app-store.yml")
if store.get("id") != "localmedia" or store.get("name") != "Madiator Audio Apps":
    problems.append("Store id/name unexpected")

manifests = sorted(root.glob("*/umbrel-app.yml"))
if len(manifests) < 2:
    problems.append("Expected at least two applications")

for path in manifests:
    app = read(path)
    pkg = path.parent.name
    compose = read(path.parent / "docker-compose.yml")
    services = compose.get("services", {})
    if app.get("id") != pkg or not pkg.startswith("localmedia-"):
        problems.append(f"{pkg}: invalid app ID/directory")
    if str(app.get("manifestVersion")) != "1.1":
        problems.append(f"{pkg}: invalid manifest version")
    if not isinstance(app.get("port"), int):
        problems.append(f"{pkg}: port must be numeric")
    if app.get("submitter") != "Madiator":
        problems.append(f"{pkg}: missing submitter attribution")
    if not isinstance(services, dict) or not services:
        problems.append(f"{pkg}: missing Compose services")
        continue
    for name, svc in services.items():
        if svc.get("privileged") is True:
            problems.append(f"{pkg}/{name}: privileged containers need review")
        if svc.get("network_mode") == "host" and svc.get("ports"):
            problems.append(f"{pkg}/{name}: redundant port publishing in host mode")
    for folder in app.get("folderAccess", []):
        for mount in folder.get("mounts", []):
            if mount.get("service") not in services:
                problems.append(f"{pkg}: folder mount references missing service")
            if not str(mount.get("targetPath", "")).startswith("/"):
                problems.append(f"{pkg}: invalid folder mount target")

    if pkg == "localmedia-infinity-core":
        svc = services.get("server", {})
        if not str(app.get("version", "")).startswith("14.0-beta16-umbrel."):
            problems.append(f"{pkg}: outdated app version")
        if svc.get("image") != "ghcr.io/tekchansin/infinity-core:beta":
            problems.append(f"{pkg}: unexpected Docker image")
        if svc.get("network_mode") != "host":
            problems.append(f"{pkg}: host networking required")
        if not any("/music:rw" in str(x) for x in svc.get("volumes", [])):
            problems.append(f"{pkg}: missing RW music mount")
        if not any(m.get("targetPath") == "/music" and m.get("readOnly") is False for f in app.get("folderAccess", []) for m in f.get("mounts", [])):
            problems.append(f"{pkg}: missing writable music folder selection")
    if pkg == "localmedia-roon-server":
        svc = services.get("roon", {})
        if svc.get("image") != "ghcr.io/roonlabs/roonserver:latest":
            problems.append(f"{pkg}: unexpected Roon image")
        if not any(m.get("targetPath") == "/Music" and m.get("readOnly") is True for f in app.get("folderAccess", []) for m in f.get("mounts", [])):
            problems.append(f"{pkg}: missing read-only music folder selection")

if problems:
    print("App store validation failed:")
    for line in problems:
        print(" -", line)
    sys.exit(1)
print(f"Validated {len(manifests)} apps in '{store['name']}'")
