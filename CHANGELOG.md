# Changelog

## 14.0-beta12-umbrel.5

- **Hotfix:** removed unsupported `/proc/asound` bind mount from revision 4.
- Restored compatibility with Docker/runc procfs mount-safety checks on Umbrel.
- Retained USB and ALSA device-node access, host networking and music RW mounts.
- DAC enumeration remains under investigation; no unverified runtime workaround applied.

## 14.0-beta12-umbrel.4

- Exposed host ALSA inventory as a read-only `/proc/asound:/proc/asound:ro` bind mount.
- Fixed missing `/proc/asound/cards` inside Docker, which can block USB DAC enumeration.
- Kept the existing USB and ALSA device cgroup rules, host networking and writable music folder.
- Separated USB DAC discovery troubleshooting from LAN multicast discovery.

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
