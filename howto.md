# How to

## port forward

iptables:

```
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A PREROUTING -p tcp --dport 11191 -j DNAT --to-destination 1.1.1.1:1111
iptables -A FORWARD -p tcp -d 1.1.1.1 --dport 1111 -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

socat:

```
socat tcp-listen:444,fork,reuseaddr tcp:microsoft.com:443
```

