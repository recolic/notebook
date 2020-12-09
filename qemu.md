# qemu commands

## manual networking

Read this doc before doing manual networking. Use default (ignore -net/-nic/-netdev) network if not necessary. 

https://www.qemu.org/2018/05/31/nic-parameter/

```
echo 0 > /proc/sys/net/bridge/bridge-nf-call-iptables
echo 0 > /sys/devices/virtual/net/br0/bridge/multicast_querier
echo 0 > /sys/devices/virtual/net/br0/bridge/multicast_snooping

ip tuntap add vnic3 mode tap
ip tuntap add vnic2 mode tap
ip tuntap add vnic1 mode tap
ip tuntap add vnic0 mode tap
ip l add br0 type bridge

ip l set vnic3 master br0
ip l set vnic2 master br0
ip l set vnic1 master br0
ip l set vnic0 master br0
ip l set eno1 master br0

ip l set vnic3 up
ip l set vnic2 up
ip l set vnic1 up
ip l set vnic0 up
ip l set br0 up
ip l set eno1 up
dhcpcd br0
```

## go

https://wiki.archlinux.org/index.php/QEMU

```
sudo qemu-system-x86_64 t2.img -m 1G --enable-kvm -nic tap,ifname=veth1,script=no,downscript=no,mac=10:11:11:11:11:10
sudo qemu-system-x86_64 t1.img -m 1G --enable-kvm -net nic,macaddr=10:11:11:11:11:11 -net tap,ifname=vnic0,script=no,downscript=no
qemu-system-x86_64 -cdrom ~/Downloads/android-x86_64-7.1-r2.iso  -boot order=d -drive file=rand.img,format=raw -m 4G

# nohup qemu-system-x86_64 workbox-win.qcow2 -m 10G -cpu host -smp 8 -vnc :9 --enable-kvm -nic tap,ifname=vnic0,script=no,downscript=no,mac=10:11:11:11:11:10 -usb -device usb-host,hostbus=1,hostaddr=17  & disown
# nohup qemu-system-x86_64 workbox-win.qcow2 -m 10G -cpu host -smp 8 -vnc :9 --enable-kvm -nic tap,ifname=vnic0,script=no,downscript=no,mac=10:11:11:11:11:10 -usb -device usb-host,vendorid=0x08e6,productid=0x3437 & disown
nohup qemu-system-x86_64 -drive file=workbox-win.qcow2,if=virtio -m 10G -cpu host -smp 8 -vnc :9 --enable-kvm -nic tap,ifname=vnic0,script=no,downscript=no,mac=10:11:11:11:11:10 & disown

nohup qemu-system-x86_64 git-server-box.qcow2 -m 1G -cpu host -smp 1 -vnc :8 --enable-kvm -nic tap,ifname=vnic1,script=no,downscript=no,mac=10:11:11:11:11:18 & disown
```


## FAQ: Guest machine unable to DHCP on IPv4?

With wireshark, I realized that my Host::br0 is not forwarding broadcast packets (DHCP). My DHCP packets appears on Host::br0, but disappears on Host::enp3s0. 

Solution: https://unix.stackexchange.com/questions/272146/packets-not-moving-through-linux-ethernet-bridge

```
# do not query iptables for package routing
echo 0 > /proc/sys/net/bridge/bridge-nf-call-iptables

# no additional processing for multicast packages
echo 0 > /sys/devices/virtual/net/br0/bridge/multicast_querier
echo 0 > /sys/devices/virtual/net/br0/bridge/multicast_snooping
```
