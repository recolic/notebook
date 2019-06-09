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

