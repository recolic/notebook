# home router

## port forward

OpenWRT /etc/config/firewall, user-defined section only

```

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

config redirect
	option dest_port '10808'
	option src 'wan'
	option name 'hms.recolic-10808'
	option src_dport '10808'
	option target 'DNAT'
	option dest_ip '10.100.100.101'
	option dest 'lan'

config redirect
	option dest_port '1080'
	option src 'wan'
	option name 'hms.recolic-1080-to-10809'
	option src_dport '10809'
	option target 'DNAT'
	option dest_ip '10.100.100.101'
	option dest 'lan'
```

## DHCP static leases

DHCP pool: 10.100.100.120 - 10.100.100.220, router 10.100.100.1

```
RECOLICHMS
2C:56:DC:08:42:73
10.100.100.101
none
none
none
RECOLICPC
24:4B:FE:8D:BF:84
10.100.100.34
none
none
none
RECOLICHMS.wifi
DC:85:DE:F8:8E:71
10.100.100.104
none
none
none
LadlodRouter
7C:B5:40:74:FD:CE
10.100.100.122
none
none
none
```

## DNS

router /etc/hosts

```
10.100.100.101 hms.recolic
10.100.100.101 nfs.recolic
10.100.100.34 pc.recolic
10.100.100.1 openwrt.recolic

# Used by DNSSD printer broadcast
10.100.100.101 RECOLICHMS
```


