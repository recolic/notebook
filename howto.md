# How to

## port forward

iptables:

```
echo 1 > /proc/sys/net/ipv4/ip_forward

iptables -t nat -A PREROUTING -p tcp --dport 11192 -j DNAT --to-destination 1.1.1.1:25551
iptables -t nat -A PREROUTING -p udp --dport 11192 -j DNAT --to-destination 1.1.1.1:25551
iptables -A FORWARD -p tcp -d 1.1.1.1 --dport 25551 -j ACCEPT
iptables -A FORWARD -p udp -d 1.1.1.1 --dport 25551 -j ACCEPT

iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

socat:

```
socat tcp-listen:444,fork,reuseaddr tcp:microsoft.com:443
socat udp-listen:444,fork,reuseaddr udp:microsoft.com:443
```

