# Changelog

## 14.0-beta12-umbrel.3

- Added raw USB bus and ALSA device access, including hot-plug support.
- Scoped device cgroup rules to Linux majors 116 (sound) and 189 (USB).
- Kept privileged mode off and avoided exposing host block devices.
- Documented USB DAC usage and access verification via SSH.
- Retained writable music sync, native folder picker and official icon.

## 14.0-beta12-umbrel.2

- Added native umbrelOS 2.x folder access entry for a selectable `/music` library.
- Enabled read/write storage at both the Compose and folder-access layer.
- Verified the icon URL corresponds to the original upstream project artwork.
- Added editable environment options, separate application-state storage,
  implementation notes, and sync-specific safeguards.
- Preserved the original app ID `localmedia-infinity-core` and store ID
  `localmedia` to support upgrades from the previous package.
