# Reproduce recolic's workspace

## Server side (Ring0)

> Run everything as root

- Install ArchLinux

Extra: `pacman -S fish dhcpcd vim sudo`

- thunderbird

Config editor: set `mail.openpgp.allow_external_gnupg` to true.   
AccountSettings -> Composition -> WhenQuoting: start my reply above the quote, and `place my signature` below my reply. 

## GUI Workspace

```
useradd -m recolic
passwd recolic
```

```
echo 'recolic ALL=(ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo
```

> Now, run everything below as recolic

```
sudo pacman -S --noconfirm gnome base-devel thunderbird firefox telegram-desktop docker
# TODO: setup gpg ssh
git clone https://git.recolic.net/root/scripts /home/recolic/sh
```

- gnome

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


