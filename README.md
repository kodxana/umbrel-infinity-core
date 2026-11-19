# Local Audio Apps for umbrelOS

An **unofficial community app store** that provides Umbrel integrations for music servers using upstream-provided container images. The repository contains packaging and documentation, not proprietary application binaries.

## Available applications

| App | App ID | Upstream image | Interface |
| --- | --- | --- | --- |
| Infinity Core (Beta) | `localmedia-infinity-core` | `ghcr.io/tekchansin/infinity-core:beta` | Web UI on port 8930 |
| Roon Server | `localmedia-roon-server` | `ghcr.io/roonlabs/roonserver:latest` | Roon Remote; dashboard tile opens an information page |

The apps install independently, each with its own persistent state. They can read the same music library when the appropriate storage folder is selected in Umbrel.

## Installation

1. Add this repository in **Umbrel → App Store → Community App Stores** using its GitHub repository URL.
2. Open **Local Audio Apps** and install the desired application.
3. Select a music folder from Umbrel's storage picker.
4. Use the app-specific setup instructions below to finish configuration.

## Infinity Core (Beta)

**Upstream version:** 14.0-beta14 (2026-11-19). The device selector now
supports **Edit list** to hide or restore unused local and network outputs.
The currently playing output stays visible, and visibility choices are
shared between clients connected to the same server.

- **Playback:** local ALSA sound devices, Infinity Link, and compatible network renderers.
- **Network:** host networking for local device discovery.
- **Music:** a selected music folder appears inside the container at `/music`, with **read/write** access for music transfers and optional metadata editing.
- **Persistent state:** `/data`.
- **Browser:** open `http://<server-ip>:8930` and use the pairing code supplied in the container logs.
- **Timezone:** defaults to UTC in the published template; change `TZ` in Umbrel app settings for the deployment.

### USB audio on Linux

The package mounts `/dev/snd` and `/dev/bus/usb` and permits device character majors 116 (ALSA) and 189 (USB bus). Docker normally masks `/proc/asound`, so the Compose definition enables `security_opt: systempaths=unconfined` for audio device enumeration.

**Security consideration:** this setting exposes additional system paths normally hidden from a container. It is broader than a default Docker container, although the app is not in privileged mode. Do not publish its service ports directly to the internet.

Do **not** bind-mount `/proc/asound` directly onto `/proc/asound` inside the container: recent runc configurations reject such mounts.

### Update safely

Complete any active music transfers first, back up persistent app data, then use Umbrel's app update workflow. The moving `:beta` image may change independently from this integration's version. Verify installed application version from its startup logs.

Official upstream documentation: [Infinity Core Docker instructions](https://github.com/tekchansin/Infinity-Homeassistant).

## Roon Server

- **Official container:** `ghcr.io/roonlabs/roonserver:latest` for AMD64/Linux.
- **Network:** host networking required for Roon Remote and device discovery.
- **Persistent state:** `/Roon`, including Roon database and downloaded application files.
- **Backup destination:** `/RoonBackups`, configured in Roon settings.
- **Music:** selectable folder mounted read-only at `/Music` to protect existing files.
- **Playback:** compatible local ALSA devices or network outputs; an exclusive USB audio device should only be used by one playback application at a time.
- **Management:** Roon Server is headless. Control it using the Roon app on a supported desktop or mobile device; the Umbrel dashboard tile displays setup instructions.
- **Subscription:** Roon trial or subscription required.

Roon's internal application version is distinct from the Umbrel integration version. Roon can update its installed binaries while retaining `/Roon`.

Official upstream documentation: [Roon Labs Docker image](https://github.com/RoonLabs/roon-docker).

## Storage and privacy

No installation-specific hardware models, music-library details, local IP addresses, disk sizes, user profiles, or usernames belong in this repository. All examples are intended to be generic. Store deployment-specific settings in Umbrel app settings or local configuration, not in the public store.

For music libraries with write-enabled syncing, maintain an independent backup. Backups kept on the same storage device as the application are not independent disaster recovery backups.

## Troubleshooting

```bash
# List community app containers
sudo docker ps --filter name=localmedia-

# Inspect Infinity Core startup messages
sudo docker logs --tail 100 localmedia-infinity-core_server_1

# Inspect Roon container startup messages
sudo docker logs --tail 100 localmedia-roon-server_roon_1
```

Roon's application logs are stored in the persistent `/Roon/database/RoonServer/Logs/` directory.

## Acknowledgements

This is an unofficial packaging project. Infinity Core is proprietary software developed by Anantar Ultimate, and Roon Server is proprietary software developed by Roon Labs. The application logos are referenced from the respective developers' public repositories; the container images are maintained by the upstream developers.
