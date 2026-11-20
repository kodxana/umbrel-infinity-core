# Operations and security

## Updating

1. Finish or stop active file transfers and back up app state and music separately.
2. Update using Umbrel's App Store; this can stop and recreate containers.
3. Verify the runtime build from the logs, not just the integration manifest version.

```bash
sudo docker ps --filter name=localmedia-
sudo docker logs --tail 60 localmedia-infinity-core_server_1
sudo docker logs --tail 60 localmedia-roon-server_roon_1
```

Infinity Core uses a mutable `:beta` tag, while Roon also manages its own application updates. Upstream and integration version numbers are separate.

## Storage

| App | Persistent state | Music path | Access |
| --- | --- | --- | --- |
| Infinity Core | `/data` | `/music` | Read/write |
| Roon | `/Roon`, `/RoonBackups` | `/Music` | Read-only |

Host-side music paths are selected in the Umbrel folder picker, not hard-coded to a particular physical disk. Verify mounts from the Docker engine:

```bash
sudo docker inspect localmedia-infinity-core_server_1 --format '{{range .Mounts}}{{println .Source "->" .Destination "RW=" .RW}}{{end}}'
```

Write-enabled synchronization can modify or remove files. Maintain an independent, regularly tested backup.

## Linux USB audio

The Infinity Core app exposes `/dev/snd` and `/dev/bus/usb` with class-specific cgroup rules. Roon uses `/dev/snd`. Both packages enable Docker's `systempaths=unconfined` option to expose `/proc/asound` for ALSA enumeration.

This option **reduces container isolation** because other normally protected system paths are also exposed. Neither app uses full `privileged: true`. Avoid direct bind mounts into `/proc/asound`; modern runc versions can reject them.

If the DAC is enumerated but not available in an application's UI, inspect the application logs and API before changing the Docker permissions.

Do not attempt simultaneous exclusive playback through the same local USB audio endpoint from multiple programs.

## Public repository hygiene

Never publish installation-specific IP addresses, hardware serials, device inventories, private usernames, library contents, passwords or API tokens. Only the public maintainer name **Madiator** is used in project branding. Historical Git commits may retain previous content until history is explicitly rewritten.
