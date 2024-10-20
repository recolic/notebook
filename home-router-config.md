# home router

## port forward

OpenWRT /etc/config/firewall, user-defined section only

```
[other config ...]

config include
	option path '/etc/firewall.user'

config redirect
	option dest_port '25565'
	option src 'wan'
	option name 'mc'
	option src_dport '25565'
	option target 'DNAT'
	option dest 'lan'
	option dest_ip '10.100.100.101'

config redirect
	option src 'wan'
	option target 'DNAT'
	option dest_ip '10.100.100.34'
	option dest 'lan'
	option dest_port '25566'
	option name 'pc.ssh'
	option src_dport '25566'

config redirect
	option dest_port '22'
	option src 'wan'
	option name 'hms.ssh'
	option src_dport '25567'
	option target 'DNAT'
	option dest_ip '10.100.100.101'
	option dest 'lan'

config redirect
	option dest_port '4662-4672'
	option src 'wan'
	option name 'ed2k highid'
	option src_dport '4662-4672'
	option target 'DNAT'
	option dest_ip '10.100.100.34'
	option dest 'lan'

config redirect
	option dest_port '80'
	option src 'wan'
	option target 'DNAT'
	option dest 'lan'
	option dest_ip '10.100.100.101'
	option name 'nfs-http'
	option src_dport '81'

config redirect
	option dest_port '1194'
	option src 'wan'
	option name 'openvpn'
	option target 'DNAT'
	option dest_ip '10.100.100.101'
	option dest 'lan'
	option src_dport '25554'

config redirect
	option src 'wan'
	option target 'DNAT'
	option dest_ip '10.100.100.101'
	option dest 'lan'
	option dest_port '6088'
	option name 'hms.recolic-6088'
	option src_dport '6088'
	list proto 'tcp'
	list proto 'udp'

config redirect
	option src 'wan'
	option target 'DNAT'
	option dest_ip '10.100.100.101'
	option dest 'lan'
	option dest_port '30400-30499'
	option name 'hms-generic-30400-30499'
	option src_dport '30400-30499'

config redirect
	option src 'wan'
	option target 'DNAT'
	option dest_ip '10.100.100.101'
	option dest 'lan'
	option dest_port '30500-30999'
	option name 'hms-frps-30500-30999'
	option src_dport '30500-30999'

```

## DHCP static leases and DNS

DHCP pool: 10.100.100.120 - 10.100.100.220, router 10.100.100.1

/etc/config/dhcp

```
[other config ...]

config host
	option name 'pc.re'
	option dns '1'
	option mac '24:4B:FE:8D:BF:84'
	option ip '10.100.100.34'

config host
	option name 'hms.re'
	option dns '1'
	option ip '10.100.100.101'
	option mac 'C8:4D:44:29:93:55'

config host
	option name 'rpi.re'
	option dns '1'
	option mac 'E4:5F:01:CD:FE:B8'
	option ip '10.100.100.187'

config domain
	option name 'hms.recolic'
	option ip '10.100.100.101'

config host
	option name 'HP2EB76F'
	option ip '10.100.100.178'
	option mac 'A8:B1:3B:2E:B7:6F'
```

## Traffic meter setup

```
opkg update
opkg install luci-app-statistics collectd-mod-ethstat collectd-mod-ipstatistics
/etc/init.d/collectd enable
reboot
```
