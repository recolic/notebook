# OpenVPN recolic's toolkit

## udp forwarder (fake obfs)

https://gist.github.com/recolic/5d0cf1bed2ca454e5e8edc7ac24431ba

- openwrt

~/ovpn_forward.daemon.sh

```
#!/bin/sh

udp_forwarder -l 0.0.0.0:9999 -r 34.80.141.142:9998 -b PASSWORD_PASSWORD > /dev/null 2>&1 &
exit $?
```

/etc/init.d/ovpn-forwarder

```
#!/bin/sh /etc/rc.common
# Copyright (C) 2006-2011 OpenWrt.org

START=50

START=10 
STOP=15

start() {        
	echo starting...
	/root/ovpn_forward.daemon.sh
}                 

stop() {          
	echo stoping...
	kill $(ps | grep udp_forwarder | grep -v grep | sed 's/^ *//g' | cut -d ' ' -f 1)
}
```

- server side

/etc/systemd/system/ovpn_forward.service

```
[Unit]
Description=ovpn_forwarder

[Service]
TimeoutStartSec=0
WorkingDirectory=/home/recolickeghart/port_forwording
ExecStart=/home/recolickeghart/port_forwording/daemon.sh

[Install]
WantedBy=multi-user.target
```

daemon.sh (./forward is the compiled ovpn_forwarder)
```
#!/bin/bash

./forward -l 0.0.0.0:9998 -r 127.0.0.1:9999 -a PASSWORD_PASSWORD
#socat tcp4-listen:9998,reuseaddr,fork UDP:127.0.0.1:9999
#nc -l -p 9998 < fifo | nc -u 127.0.0.1 9999 > fifo
```


dustbin
```
# openwrt daemon.sh
#!/bin/sh
ssh -i id_dropbear -l recolickeghart -f -N -L 9998:127.0.0.1:9998 base.tw1.recolic.net
socat udp-listen:9999,reuseaddr,fork TCP:127.0.0.1:9998

#netcat -l -u -p 9999 < fifo | netcat localhost 9998 > fifo
```

## NEW: real obfs

- client side proxy
```
[Unit]
Description=obfsP

[Service]
TimeoutStartSec=0
ExecStart=/usr/bin/obfsproxy-c --log-file=/var/log/obfsproxy.log --log-min-severity=info obfs2 --shared-secret=222222222222222 socks 0.0.0.0:10809

[Install]
WantedBy=multi-user.target


```

- server side proxy
```

[Unit]
Description=obfsProxy

[Service]
TimeoutStartSec=0
ExecStart=/usr/bin/obfsproxy-c --log-file=/var/log/obfsproxy.log --log-min-severity=info obfs2 --dest=127.0.0.1:9999 --shared-secret=1111111111111111 server 0.0.0.0:9989

[Install]
WantedBy=multi-user.target
```

- ovpn
```
client
proto tcp
## obfs
socks-proxy-retry
socks-proxy pi.recolic 10809
remote base.tw1.recolic.net 9989
#remote pi.recolic 9999
dev tun
resolv-retry infinite
...
```
