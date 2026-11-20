# Madiator Audio Apps

[![Validate store](https://github.com/kodxana/umbrel-infinity-core/actions/workflows/validate.yml/badge.svg)](https://github.com/kodxana/umbrel-infinity-core/actions/workflows/validate.yml)
![Platform](https://img.shields.io/badge/platform-umbrelOS%202.x-555)
![License](https://img.shields.io/badge/integrations-MIT-blue)

**Unofficial community app store for self-hosted audio. Maintained by Madiator.**

A curated collection of audio services, packaged for umbrelOS with predictable storage, original developer artwork and documented network access. This repository ships app definitions, not proprietary application binaries. Neither Umbrel nor the upstream vendors endorse these packages.

## Available apps

| App | Version in this store | Official upstream image | Music folder |
| --- | --- | --- | --- |
| **Infinity Core (Beta)** | **14.0-beta15-umbrel.10** | `ghcr.io/tekchansin/infinity-core:beta` | `/music` — read/write |
| **Roon Server** | 1.0.1 (integration version) | `ghcr.io/roonlabs/roonserver:latest` | `/Music` — read-only |

Both apps have separate persistent databases. Roon's integration version is independent of the Roon application build.

## Installation

1. In Umbrel, open **App Store → Community App Stores → Add**.
2. Paste `https://github.com/kodxana/umbrel-infinity-core`.
3. Open **Madiator Audio Apps**, then install the desired app.
4. Pick an existing Music folder in Umbrel's native storage selector.

**Compatibility:** the store ID remains `localmedia` and existing app IDs are unchanged. Do not rename IDs in an established store.

### Infinity Core

Open `http://<server-address>:8930` on the local network and pair the browser with the code from the app logs. App configuration persists at `/data`; music is writable at `/music` to support synchronization and optional tag editing. Host networking supports Infinity Link, compatible network renderers and local ALSA/USB audio.

**Infinity Link:** mDNS/DNS-SD advertises `_infinitylink._tcp` using UDP 5353 multicast (224.0.0.251). Streaming peers use TCP 4720; Wi-Fi Transfer peers use TCP 8910. The Infinity Core LAN and browser interfaces use TCP 8931 and 8930 respectively. **Do not add Docker port mappings to the host-networked service.** See [Network reference](docs/NETWORKING.md) for service roles and firewall guidance.

Upstream [Infinity Core 14.0-beta15 release notes](https://github.com/tekchansin/Infinity-Homeassistant/blob/main/infinity_beta/CHANGELOG.md) cover improved large-screen layouts, Now Playing, and mobile navigation.

### Roon Server

Roon Server is headless. Open the official Roon app on a desktop or mobile client to sign in and configure playback. The Umbrel tile opens a setup page, not a Roon music interface. Server data is retained under `/Roon`, backups at `/RoonBackups`. A Roon trial or subscription is required.

## Documentation

- [Networking and firewall reference](docs/NETWORKING.md)
- [Operations, backup and security notes](docs/OPERATIONS.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

**Safe defaults:** keep services on trusted local networks, keep independent library backups and avoid uploading personal configuration details to public issues.

## Ownership and licensing

Maintained by **Madiator**. The [MIT license](LICENSE) covers original integration files and documentation only—not the proprietary Infinity Core or Roon applications. App icons reference original developer-supplied artwork.

Upstream: [Infinity Core](https://github.com/tekchansin/Infinity-Homeassistant) · [Roon Server](https://github.com/RoonLabs/roon-docker)
