# stubby fucking china gfw

## server addr

base.cn2.recolic.net, dns.recolic.org, dns.recolic.net, 123.206.117.183

## config backup:

```yml
listen_addresses:
  - 0.0.0.0
  - 0::1





upstream_recursive_servers:
# IPv4 addresses
# The Surfnet/Sinodun servers
  - address_data: 8.8.4.4
    tls_auth_name: "dns.google"
    tls_pubkey_pinset:
      - digest: "sha256"
        value: V7bhl+p/oVCN1kofbZtBaCANIMbxlsoUi6lTzk7yArI=
  - address_data: 145.100.185.15
    tls_auth_name: "dnsovertls.sinodun.com"
    tls_pubkey_pinset:
      - digest: "sha256"
        value: 62lKu9HsDVbyiPenApnc4sfmSYTHOVfFgL3pyB+cBL4=
  - address_data: 145.100.185.16
    tls_auth_name: "dnsovertls1.sinodun.com"
    tls_pubkey_pinset:
      - digest: "sha256"
        value: cE2ecALeE5B+urJhDrJlVFmf38cJLAvqekONvjvpqUA=
# The getdnsapi.net server
  - address_data: 185.49.141.37
    tls_auth_name: "getdnsapi.net"
    tls_pubkey_pinset:
      - digest: "sha256"
        value: foxZRnIh9gZpWnl+zEiKa0EJ2rdCGroMWm02gaxSc9Q=
# IPv6 addresses
# The Surfnet/Sinodun servers
  - address_data: 2001:610:1:40ba:145:100:185:15
    tls_auth_name: "dnsovertls.sinodun.com"
    tls_pubkey_pinset:
      - digest: "sha256"
        value: 62lKu9HsDVbyiPenApnc4sfmSYTHOVfFgL3pyB+cBL4=
  - address_data: 2001:610:1:40ba:145:100:185:16
    tls_auth_name: "dnsovertls1.sinodun.com"
    tls_pubkey_pinset:
      - digest: "sha256"
        value: cE2ecALeE5B+urJhDrJlVFmf38cJLAvqekONvjvpqUA=
# The getdnsapi.net server
  - address_data: 2a04:b900:0:100::38
    tls_auth_name: "getdnsapi.net"
    tls_pubkey_pinset:
      - digest: "sha256"
        value: foxZRnIh9gZpWnl+zEiKa0EJ2rdCGroMWm02gaxSc9Q=

```
