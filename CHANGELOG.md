# Changelog

## Roon Server — Umbrel integration 1.0.1

- Published a separate Roon Server app using the official upstream container image.
- Added independent persistent app data and backup mounts.
- Added a read-only music-folder selection, host networking, ALSA access and a setup information page.
- Generalized the sample configuration and documentation for public distribution.

## Infinity Core — Umbrel integration 14.0-beta13-umbrel.8

- Aligned the community package with upstream Infinity Core 14.0-beta13.
- Kept USB, ALSA, host networking and writable music-folder support.
- Generalized the timezone default and removed environment-specific descriptions.
- Preserved the original upstream icon.

## Previous compatibility changes

- Added native Umbrel music-folder selection and writable sync support.
- Added Linux ALSA and USB device-node access with device-specific cgroup rules.
- Reverted a direct `/proc/asound` bind mount because modern runc blocks mounting into procfs.
- Enabled the documented Docker `systempaths=unconfined` option for ALSA card enumeration; this broadens the container's system-path visibility.
- Kept application state separate from the selected music folder.
