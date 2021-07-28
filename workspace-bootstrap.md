# Reproduce recolic's workspace

> If you're in fucking China, change all `recolic.net` to breakwall domain (such as recolic.cc). 

## Server mode (Ring0)

> Run everything as root

- Install ArchLinux

Extra: `pacman -S --noconfirm fish dhcpcd vim sudo openssh`

## GUI Workspace

```
useradd --create-home --shell /usr/bin/fish recolic
passwd recolic

echo 'recolic ALL=(ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo
pacman -S --noconfirm gnome networkmanager
systemctl enable gdm NetworkManager
reboot
```

> Now, reboot and enter gnome terminal, run everything below as recolic, in fish, in /home/recolic

```
sudo pacman -S --noconfirm base-devel thunderbird firefox telegram-desktop docker    pcsclite ccid

sudo systemctl enable pcscd.service --now
gpg --keyserver keyserver.ubuntu.com --recv-keys E3933636
set -gx SSH_AUTH_SOCK (gpgconf --list-dirs agent-ssh-socket) # already in fish.config
echo enable-ssh-support > ~/.gnupg/gpg-agent.conf
echo 93AC57E30E88111EC71D9215A1B436AFE705C71C > ~/.gnupg/sshcontrol
gpg-connect-agent reloadagent /bye
set -g GPG_TTY (tty)
gpg-connect-agent updatestartuptty /bye

git clone git@git.recolic.net:/root/scripts.git /home/recolic/sh
```

- gnome configure

TODO: move this section to scripts/README.md

```
# TODO: install extension

gsettings set org.gnome.desktop.interface enable-hot-corners false
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

- thunderbird

Config editor: set `mail.openpgp.allow_external_gnupg` to true.   
AccountSettings -> Composition -> WhenQuoting: start my reply above the quote, and `place my signature` below my reply. 



