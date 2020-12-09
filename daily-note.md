
##  bridge hust wireless

```
sudo iw wlp1s0 disconnect; and sudo iw dev wlp1s0 connect HUST_WIRELESS 2437
```

## ovpn udp forwarder

the naive script is good. script hosted [here](https://gist.github.com/recolic/5d0cf1bed2ca454e5e8edc7ac24431ba). do not read the horrible code (not written by me), just compile and use it. works on mips gcc.

- server

```
./forward -l 0.0.0.0:9998 -r 127.0.0.1:9999 -a r**********************n
```

- any client

```
udp_forwarder -l 0.0.0.0:9999 -r 35.201.233.28:9998 -b r***************n
```

- then

```
set openvpn server to client:9999
```

## gnome

```
gsettings set org.gnome.desktop.media-handling automount false
gsettings set org.gnome.desktop.media-handling automount-open false
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-left "['<Shift><Alt>Left']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-right "['<Shift><Alt>Right']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-up "['<Shift><Alt>Up']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-down "['<Shift><Alt>Down']"
gsettings set org.gnome.desktop.wm.keybindings move-to-monitor-left "['<Super><Shift>Left']"
gsettings set org.gnome.desktop.wm.keybindings move-to-monitor-right "['<Super><Shift>Right']"
gsettings set org.gnome.desktop.wm.keybindings move-to-monitor-up "['<Super><Shift>Up']"
gsettings set org.gnome.desktop.wm.keybindings move-to-monitor-down "['<Super><Shift>Down']"
```
