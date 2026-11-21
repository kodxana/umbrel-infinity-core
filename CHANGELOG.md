# Changelog

## Infinity Core 14.0-beta16-umbrel.11 — 2026-11-21

- Update the package version to match upstream **14.0-beta16**.
- Document offline album, playlist and track downloads on Android; automatic Favorite and Smart Downloads (requires Infinity Core for Mobile beta13, with iPhone support planned).
- Note Devices & Sharing improvements, tablet Now Playing changes, UPnP playback and radio fixes, and corrected Infinity Link skip behavior.
- Preserve existing host networking, Infinity Link/mDNS port documentation, USB/ALSA configuration, data persistence and read/write music-folder permissions.
- No changes to Roon Server or existing application and store IDs.

## Infinity Core 14.0-beta15-umbrel.10 — 2026-11-20

- Follow the upstream Infinity Core **14.0-beta15** release for tablet/foldable layouts, Now Playing and navigation refinements.
- Brand the community store **Madiator Audio Apps** while retaining its existing `localmedia` ID.
- Add documented network protocols: TCP 8930/8931, UDP 5353 multicast 224.0.0.251 for `_infinitylink._tcp`, and peer TCP 4720 streaming / TCP 8910 Wi-Fi Transfer.
- Maintain existing USB/ALSA, host networking, persistent configuration and RW music mounts.
- Add validation workflow, contribution guidance, and operational/network documentation.

## Previous releases

- **Infinity Core beta14:** edit/hide unused output devices.
- **Infinity Core beta13:** share audio devices and improve mobile playback.
- **Infinity Core compatibility:** native music-folder picker, ALSA/USB device permissions and `systempaths=unconfined` for audio enumeration.
- **Roon Server 1.0.1:** official image, persistent data, separate backups, read-only music mount and Umbrel setup landing page.
