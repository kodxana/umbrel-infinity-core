# Roon Server for umbrelOS

This directory is a community integration, not a Roon Labs product or an
official Umbrel app. It uses the vendor's official container:
`ghcr.io/roonlabs/roonserver:latest`.

## Quick setup

1. Install this app from the **Local Audio Apps** Community App Store.
2. In Umbrel's native **Music Library** selector, choose the same folder used by
   Infinity Core, e.g. the existing Umbrel Files **Music** folder.
3. Roon Server starts on your Umbrel machine with host networking.
4. Open the **Roon app** on Windows, macOS, iOS or Android, discover the Roon
   Server on the LAN, sign in using your Roon account, then configure storage.
5. Roon > Settings > Storage > add `/Music` if not already watched.
6. Roon > Settings > Audio > enable **TEAC UD-701N** or another Roon-compatible
   output. It must be idle in Infinity Core when Roon opens it for exclusive
   USB playback.

The Umbrel dashboard tile opens a tiny **information page**, not Roon Remote.
Roon Server does not offer a native browser playback/management UI.

## Layout

| Container path | Role | Permissions |
| --- | --- | --- |
| `/Roon` | Roon database, application files, logs | Read/write, persistent |
| `/RoonBackups` | Backups configured in Roon's own settings | Read/write, persistent |
| `/Music` | User-selected existing library | Read-only |
| `/dev/snd` | Direct ALSA audio outputs | Read/write devices |

The Roon folders live under Umbrel app data and should be placed on SSD-backed
storage. Note that **backups inside the same disk are not independent backups**;
copy them to your NAS/another drive periodically.

## Networking

The Roon service uses `network_mode: host` for SSDP/RAAT discovery and has no
host port publishing. Keep PC/phone and Roon Server in the same LAN/VLAN.
No reverse proxy should be placed between Roon Server and its discovery clients.
The lightweight information page is served separately through Umbrel's app
gateway (manifest port `8998`).

**Do not expose Roon Server's host service ports directly to the internet.**

## Local USB DAC

For the MINISFORUM's directly attached TEAC UD-701N, this package exposes the
ALSA character devices and grants Linux device major 116. As with the tested
Infinity Core configuration, `security_opt: systempaths=unconfined` removes
Docker's default `/proc/asound` masking so ALSA can enumerate its cards.
This option also broadens visibility of other protected system paths; it is a
security tradeoff and should be used only on a trusted host.

The TEAC USB DAC is a shared physical resource: Roon and Infinity Core cannot
reliably stream to it at the same time. Stop playback in one before using the
other. Other outputs (Roon Ready/RAAT, AirPlay, UPnP) may depend on device
protocol support and network discovery.

## Updating and logs

Roon Server updates its application binaries itself. The official Docker
image can also be updated through the Umbrel app mechanism when its image tag
changes, but the integration version `1.0.0` is **not the Roon build number**.

```sh
# Check containers
sudo docker ps --filter name=localmedia-roon-server

# Read the official Roon image startup logs
sudo docker logs --tail 100 localmedia-roon-server_roon_1

# Confirm the active USB DAC card is available to the container
sudo docker exec localmedia-roon-server_roon_1 cat /proc/asound/cards
```

Full Roon Server application logs are inside its persistent data directory,
generally under `/Roon/database/RoonServer/Logs/`.

## Important

- Official container is **amd64 only**.
- Roon requires a subscription or trial.
- Roon's primary music folder is read-only here. Drag-and-drop imports to it
  won't work; use Infinity Core's sync or another authorized file manager.
- Do not run heavy Roon library analysis while Infinity Core is transferring
  thousands of tracks from your DX340 if you want predictable I/O throughput.

Sources:
- https://github.com/RoonLabs/roon-docker
- https://help.roonlabs.com/portal/en/kb/articles/roonserver-on-linux-with-docker
- https://roonlabs.github.io/roon-docker/
- Official logo: https://github.com/RoonLabs/roon-docker/blob/main/configurator/public/roon-moon.svg
