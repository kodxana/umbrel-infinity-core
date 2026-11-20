# Infinity Core: network ports and discovery

Infinity Core uses `network_mode: host` in this Umbrel package. Docker `ports:` forwarding is unnecessary and should not be configured on a host-networked service.

| Service | Transport | Port / destination | Connection role |
| --- | --- | --- | --- |
| Infinity Core browser | TCP | **8930** | Browser to server |
| Infinity Core LAN clients | TCP | **8931** | Local client/control connection to server |
| mDNS / DNS-SD | UDP multicast | **5353**, **224.0.0.251** | Discover `_infinitylink._tcp` services |
| Infinity Link streaming | TCP | **4720** | Participating streaming device/peer |
| Wi-Fi Transfer | TCP | **8910** | Participating transfer device/peer |
| UPnP/SSDP (optional) | UDP multicast | **1900**, **239.255.255.250** | Compatible renderer discovery |

**Port roles matter.** TCP 4720 and TCP 8910 represent device/peer services; they do not imply that every Infinity Core server listens on those ports. Actual connection direction and remote endpoint depend on the device and application role. Use the advertised DNS-SD endpoint to identify a peer rather than assuming the core server hosts every service.

## Firewall checklist

- Permit local clients to reach the Infinity Core server on TCP **8930/8931** as required.
- Permit UDP **5353** multicast to **224.0.0.251** between local participating devices. This is link-local multicast; cross-subnet discovery requires deliberate networking configuration.
- Permit TCP **4720** for streaming and TCP **8910** for transfer to the participating peers when those features are used.
- Permit UDP **1900** for SSDP if UPnP/DLNA is used.
- Keep all audio services **LAN-only**. Do not forward discovery or streaming ports to the internet.

## Diagnostics (run on the hosting device)

```bash
# Locally listening TCP sockets (peer services may be on a different device)
sudo ss -lntp | grep -E ':(8930|8931|4720|8910)\\b' || true

# Locally listening UDP sockets
sudo ss -ulnp | grep -E ':(5353|1900)\\b' || true

# Optional: when avahi-utils is installed
avahi-browse -rt _infinitylink._tcp
```

No `ss` listener for TCP 4720/8910 on the Infinity Core host is necessarily expected: those services may run on a peer. Network interfaces, VLAN filtering, firewall rules and client isolation can affect multicast discovery.

The upstream [Docker README](https://github.com/tekchansin/Infinity-Homeassistant) documents host networking, TCP 8930/8931 and UDP 5353. TCP 4720 and 8910 are additional integration port information; their exact listener roles have not been independently confirmed in that upstream README.
