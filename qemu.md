# qemu commands

## manual networking

Read this doc before doing manual networking. Use default (ignore -net/-nic/-netdev) network if not necessary. 

https://www.qemu.org/2018/05/31/nic-parameter/

```
ip l add veth1 type veth
ip tuntap add vnic2 mode tap
ip tuntap add vnic1 mode tap
ip tuntap add vnic0 mode tap
ip l add br0 type bridge

#################################

ip l set veth1 master br0
ip l set vnic2 master br0
ip l set vnic1 master br0
ip l set vnic0 master br0
ip l set enp4s0 master br0
dhclient br0
```

## go

https://wiki.archlinux.org/index.php/QEMU

```
sudo qemu-system-x86_64 t2.img -m 1G --enable-kvm -nic tap,ifname=veth1,script=no,downscript=no,mac=10:11:11:11:11:10
sudo qemu-system-x86_64 t1.img -m 1G --enable-kvm -net nic,macaddr=10:11:11:11:11:11 -net tap,ifname=vnic0,script=no,downscript=no
qemu-system-x86_64 -cdrom ~/Downloads/android-x86_64-7.1-r2.iso  -boot order=d -drive file=rand.img,format=raw -m 4G
```
