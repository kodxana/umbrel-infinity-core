# Infinity Core for umbrelOS

**Unofficial Community App Store integration** for the official proprietary
Infinity Core beta by Anantar Ultimate / tekChansin. This repository contains
integration YAML only; it does not redistribute or modify Infinity Core.

## Features

- The **real Infinity Core project icon** is referenced directly from the
  developer's [official Home Assistant repository](https://github.com/tekchansin/Infinity-Homeassistant/blob/main/infinity_beta/icon.png).
  It is not AI-generated or replaced with an imitation.
- **Music library is read/write** (`/music:rw` and `folderAccess.readOnly: false`)
  for music sync and optional metadata/tag changes.
- **Native umbrelOS 2.x folder picker** for the music library.
- Persistent `/data` separate from music, with host networking for local device
  discovery (iBasso Infinity Link, AirPlay, Google Cast, UPnP).
- Editable `INFINITY_NAME` and `TZ` from Umbrel app settings.
- Direct ALSA audio and raw USB bus access, including hot-plugged compatible devices.

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

## USB access on your MINISFORUM

The Docker container can access ALSA sound devices and the raw USB bus:

```yaml
volumes:
  - /dev/snd:/dev/snd:rw
  - /dev/bus/usb:/dev/bus/usb:rw
device_cgroup_rules:
  - 'c 116:* rwm'  # ALSA
  - 'c 189:* rwm'  # USB bus
```

This supports direct audio output through compatible USB DACs and makes
raw USB device nodes available to applications inside the container.
**ALSA discovery:** Docker masks `/proc/asound` by default, so the TEAC's
device nodes may be mounted correctly while ALSA cannot enumerate any cards.
The Docker Compose `security_opt: [systempaths=unconfined]` option used by this
package unmasks `/proc/asound` **without** the forbidden bind mount.
This uses a documented Docker feature, but actual Infinity Core detection
on Umbrel hardware has not yet been verified.

**Security trade-off:** `systempaths=unconfined` disables Docker's path-level
masking and read-only restrictions for other system paths too, not only ALSA.
It is less isolated than the default container. The application still does
not run in `privileged` mode, and Docker's separate AppArmor/seccomp controls
are not disabled by this flag. Do not expose Infinity Core's ports to the
internet. To restore Docker's normal system-path isolation, remove
`security_opt: [systempaths=unconfined]` and recreate the container.

**Do not add a direct `/proc/asound:/proc/asound:ro` mount.** Umbrel's
Docker/runc refused that mount and the app could not start.

### Test before updating the app

This uses a one-off throwaway container that cannot affect the installed
Infinity Core database or music library:

```sh
sudo docker run --rm --pull=never --network=none --cap-drop=ALL \
  --security-opt systempaths=unconfined \
  --entrypoint sh ghcr.io/tekchansin/infinity-core:beta \
  -c 'cat /proc/asound/cards'
```

If this lists `2 [UD701N]`, then the Docker unmasking mechanism works
on the host. It does **not** prove Infinity Core will show the DAC or play
audio; verify those inside the app after the update.
Directory mounts expose newly connected USB devices without changing Compose.
Actual playback, MTP/sync and other USB functions still depend on upstream
Infinity Core support. Networking via Infinity Link does not require USB.

**Security and scope:** This is broad USB bus access, not unrestricted
host-device access. USB serial (`/dev/ttyUSB*`, `/dev/ttyACM*`), HID raw and
storage block devices are not passed through. There is no `privileged: true`
or whole-host `/dev` mount. For music on a USB SSD, select its folder through
Umbrel's Files/app storage selector rather than exposing the block device.

Verify through Umbrel SSH:

```sh
cid=$(sudo docker ps --filter 'ancestor=ghcr.io/tekchansin/infinity-core:beta' --format '{{.ID}}' | head -n 1)
test -n "$cid" || { echo 'Infinity Core container not found'; exit 1; }
sudo docker exec "$cid" sh -c 'ls -l /dev/snd/ /dev/bus/usb/ 2>&1'
sudo docker inspect "$cid" --format '{{json .HostConfig.DeviceCgroupRules}}'
```
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
- **Scoped USB access:** ALSA and USB bus device permissions are enabled.
  `privileged: true` and whole-host `/dev` access remain disabled.
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
