# Infinity Core for umbrelOS

**Unofficial Community App Store integration** for the official proprietary
Infinity Core beta by Anantar Ultimate / tekChansin. This repository contains
integration YAML only; it does not redistribute or modify Infinity Core.

## What is different in revision 2?

- The **real Infinity Core project icon** is referenced directly from the
  developer's [official Home Assistant repository](https://github.com/tekchansin/Infinity-Homeassistant/blob/main/infinity_beta/icon.png).
  It is not AI-generated or replaced with an imitation.
- **Music library is read/write** (`/music:rw` and `folderAccess.readOnly: false`)
  for music sync and optional metadata/tag changes.
- **Native umbrelOS 2.x folder picker** for the music library.
- Persistent `/data` separate from music, with host networking for local device
  discovery (iBasso Infinity Link, AirPlay, Google Cast, UPnP).
- Editable `INFINITY_NAME` and `TZ` from Umbrel app settings.

## Requirements

- umbrelOS 2.x on an **x86-64 Intel/AMD** machine, not ARM.
- Ports **TCP 8930 and TCP 8931** available on the Umbrel host.
- Music stored in an Umbrel-accessible folder; for this configuration the
  default is the Umbrel **Downloads/music** folder. It can be changed to any
  location exposed by Umbrel Files, including the internal 4 TB SSD.
- The official Docker image `ghcr.io/tekchansin/infinity-core:beta`.

## Install as an Umbrel app (with dashboard tile)

1. Create a **public GitHub repository** (for example `umbrel-infinity-core`).
2. Put the **contents of this ZIP at the repository root**, including
   `umbrel-app-store.yml` and `localmedia-infinity-core/`.
3. Open Umbrel **App Store → ⋯ → Community App Stores → Add** and enter your
   GitHub repository URL.
4. Open the **Local Audio Apps** store and install **Infinity Core (Beta)**.
5. If Umbrel asks for access to a music folder, select the folder containing
   your files. Grant **read/write** access; leave the service mount `/music`.
   You can change it later at **App Settings → Storage → Access to your folders**.
6. Open the app tile or visit `http://umbrel.local:8930` on your LAN.
7. On the pairing screen, choose **Show a code**. Find the six-digit pairing
   code in **App Settings → Advanced → View logs** and enter it in the browser.
8. Under **Infinity Core → Settings → Storage**, add `/music` if it is not
   already present; the contents are the selected host music folder.

> The 4 TB SSD is not automatically mounted merely because it exists.
> Pick the actual music folder using Umbrel Files/App Settings. Do not
> select or write to the 2 TB boot partition based on device size alone.

## Music sync and file safety

The complete `/music` folder is **writable**. This is intentional:

```yaml
# Docker Compose
- ${UMBREL_ROOT}/data/storage/downloads/music:/music:rw

# umbrel-app.yml (inside folderAccess.mounts)
readOnly: false
```

That allows Infinity Core to create, update or delete music files **to the
extent supported by the upstream sync feature**. It also permits optional
metadata/tag editing. Keep an independent backup of your music library and
consider a smaller test folder before a first two-way sync. This integration
cannot enforce sync direction, resolve conflicts, or prevent accidental deletes.

If a different folder is selected in Umbrel App Settings, its folder-access
mount should replace the default `/music` mapping. **Do not add a second
manual bind to `/music`** or edit Umbrel-generated Compose files.

## Play on iBasso DX340

Enable **Infinity Link** on your DAP and select the DAP from the playback
outputs in Infinity Core. Keep the DAP and Umbrel on the same LAN/VLAN for
automatic discovery. Host networking is required for normal mDNS/SSDP
behavior. Do not forward Infinity Core ports to the internet.

For desktop Infinity Core pairing from Windows or macOS, the developer also
supports using a code obtained with:

```sh
# On Umbrel via SSH; finds the app container without assuming its name:
cid=$(sudo docker ps --filter 'ancestor=ghcr.io/tekchansin/infinity-core:beta' --format '{{.ID}}' | head -n 1)
test -n "$cid" || { echo 'Infinity Core is not running'; exit 1; }
sudo docker exec "$cid" infinity-core --pair-code
```

## Operations and caveats

- **Host mode:** there is intentionally no `app_proxy` and no `ports:` mapping.
  The web UI is on `8930` and PC client uses `8931` directly. Browser
  security comes from Infinity Core's pairing, not Umbrel's proxy login.
- **No speculative healthcheck:** upstream does not document a stable health
  endpoint; inspect the app's logs and verify `http://umbrel.local:8930`.
- **No elevated privileges by default:** no `/dev/snd` required for Infinity
  Link playback. USB DAC passthrough is available as a commented option.
- **Backups:** `/data` holds application state. A music library must be backed
  up independently, especially with write-enabled syncing. Do not assume
  user-selected external files are covered by Umbrel backups.
- **Image updates:** `:beta` is a moving tag. Take a backup before upgrading;
  update the store version if you publish a new integration release.
- **Compatibility:** this integration is based on upstream beta documentation,
  not an installation test on your MINISFORUM. Verify paths and syncing before
  making the library your source of truth.

## Quick verification via SSH

```sh
sudo docker ps --format 'table {{.Names}}	{{.Image}}	{{.Status}}' | grep -i infinity
sudo ss -lntup | grep -E ':(8930|8931)\b'
# For the default music path (not a custom selection):
ls -la /umbrel/data/storage/downloads/music 2>/dev/null || true
```

## Sources

- [Vendor Docker documentation](https://github.com/tekchansin/Infinity-Homeassistant)
- [Original project icon](https://github.com/tekchansin/Infinity-Homeassistant/blob/main/infinity_beta/icon.png)
- [Umbrel Community App Store template](https://github.com/getumbrel/umbrel-community-app-store)
- [Umbrel app storage settings](https://umbrel.com/support/apps/app-settings)
- [Infinity Core product](https://anantarultimate.com/infinity-core.html)
