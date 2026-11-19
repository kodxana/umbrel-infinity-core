# Roon Server for umbrelOS

An **unofficial community integration** using Roon Labs' official Linux/AMD64 Docker image:
`ghcr.io/roonlabs/roonserver:latest`.

## Install and connect

1. Install **Roon Server** from the Local Audio Apps store in Umbrel.
2. In the Music Library folder picker, select the folder containing audio files.
3. Open the official Roon app on a compatible computer, tablet or phone on the same LAN.
4. Connect to the Roon Server, authenticate your Roon account and configure the server.
5. Open **Settings → Storage** and ensure the selected folder `/Music` is being watched.
6. Open **Settings → Audio** and enable a compatible local or network output.

The Umbrel app tile provides an **information page**, not a browser-based music interface. Roon Server itself is headless.

## Storage

| Container path | Purpose | Access |
| --- | --- | --- |
| `/Roon` | Application data, identity, library database, application binaries | Persistent, read/write |
| `/RoonBackups` | Backups configured in Roon Settings | Persistent, read/write |
| `/Music` | Selected existing music library | Read-only |
| `/dev/snd` | Linux ALSA playback devices | Device access |

This package mounts music read-only to avoid unintentional modifications when sharing a library with another application. Roon's drag-and-drop imports into `/Music` therefore will not work unless the mount is explicitly made writable.

Store Roon state on persistent storage. Set up scheduled backups and copy them to a different device or backup destination.

## Networking and audio

Roon needs `network_mode: host` for device discovery on the LAN. Remote control devices should be able to discover the server via local networking.

Local ALSA playback uses `/dev/snd` and Linux device major 116. Docker typically masks `/proc/asound`; the integration uses `systempaths=unconfined` to expose the ALSA card inventory. This setting reduces the container's default isolation and should only be used on trusted systems.

Do not expose Roon Server's listening ports directly to the internet. When multiple applications use the same exclusive hardware output, only one should play through it at a time.

## Updates

Roon Server can update its application files independently of the Umbrel app integration version. The official container also supports the production and early-access branches via `ROON_INSTALL_BRANCH`; take a backup before changing branches.

```bash
sudo docker ps --filter name=localmedia-roon-server
sudo docker logs --tail 100 localmedia-roon-server_roon_1
sudo docker exec localmedia-roon-server_roon_1 cat /proc/asound/cards
```

Application-specific log files are under `/Roon/database/RoonServer/Logs/` inside the persistent mount.

## Requirements and sources

- Linux AMD64 host with Docker and Umbrel.
- Roon subscription or trial.
- [Official Roon Labs Docker image](https://github.com/RoonLabs/roon-docker)
- [Official Docker setup guide](https://roonlabs.github.io/roon-docker/)
- [Roon support](https://help.roonlabs.com/)
