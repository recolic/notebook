# Reproduce recolic's workspace

> If you're in fucking China, change all `recolic.net` to breakwall domain (such as recolic.cc). 

## GUI Workspace

> After installing Arch Linux, run as root

```
pacman -Sy --noconfirm fish dhcpcd vim sudo openssh
useradd --create-home --shell /usr/bin/fish recolic
echo 'recolic ALL=(ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo
echo 'kernel.sysrq=1' >> /etc/sysctl.d/99-sysctl.conf

pacman -Sy --noconfirm gnome networkmanager power-profiles-daemon
systemctl enable gdm NetworkManager
systemctl enable power-profiles-daemon

echo '[recolic-aur]
SigLevel = Optional TrustAll
Server = https://drive.recolic.cc/mirrors/recolic-aur' >> /etc/pacman.conf
sed -i 's/^[# ]*ParallelDownloads =[ 0-9A-Za-z]*$/ParallelDownloads = 5/g' /etc/pacman.conf
sed -i 's/^[# ]*SystemMaxUse=[ 0-9A-Za-z]*$/SystemMaxUse=150M/g' /etc/systemd/journald.conf
sed -i 's/^[# ]*SystemMaxFileSize=[ 0-9A-Za-z]*$/SystemMaxFileSize=30M/g' /etc/systemd/journald.conf

### Require Input
passwd recolic

```

> Now, reboot and enter gnome terminal, run everything below **as recolic**, in **fish**

```
sudo pacman -Sy --noconfirm base-devel thunderbird nextcloud-client firefox telegram-desktop docker shadowsocks-libev v2ray proxychains xclip adobe-source-han-sans-cn-fonts      pcsclite ccid    git inetutils wget ttf-fira-code htop tmux dos2unix nfs-utils python-pip gnome-tweaks fcitx5-im man-db man-pages  kolourpaint breeze
# sudo apt install pcscd scdaemon gnupg2 pcsc-tools -y
sudo pacman -Sy recolic-aur/gnome-terminal-transparency recolic-aur/oreo-cursors-git recolic-aur/pikaur

sudo systemctl enable bluetooth --now

echo "GTK_IM_MODULE=fcitx" >> /etc/environment
echo "QT_IM_MODULE=fcitx" >> /etc/environment
echo "XMODIFIERS=@im=fcitx" >> /etc/environment

sudo systemctl enable pcscd.service --now
gpg --keyserver keyserver.ubuntu.com --recv-keys E3933636
set -gx SSH_AUTH_SOCK (gpgconf --list-dirs agent-ssh-socket) # already in fish.config
echo pinentry-timeout 0 > ~/.gnupg/gpg-agent.conf
echo "pinentry-program /usr/bin/pinentry-gnome3" >> ~/.gnupg/gpg-agent.conf
echo enable-ssh-support >> ~/.gnupg/gpg-agent.conf
echo 93AC57E30E88111EC71D9215A1B436AFE705C71C > ~/.gnupg/sshcontrol
gpg-connect-agent reloadagent /bye
## For non-GUI setup: 
#set -g GPG_TTY (tty)
#gpg-connect-agent updatestartuptty /bye
```

<!--
echo "options cfg80211 ieee80211_regdom=AU" >> /etc/modprobe.d/cfg80211.conf
echo "options cfg80211 internal_regdb=y" >> /etc/modprobe.d/cfg80211.conf
echo "options cfg80211 crda_support=y" >> /etc/modprobe.d/cfg80211.conf
pacman -S --noconfirm wireless-regdb
-->

- nextcloud

Login Nextcloud, and make sure `~/.config/autostart/com.nextcloud.desktopclient.nextcloud.desktop` exists, and wait for initial sync.   
Then run: 

```
fish ~/Nextcloud/workspace/setup-management.fish
```

- gnome configure

```
# gnome extension will be managed by nextcloud sync
# TODO: add recolic-aur to pacman.conf and install gnome-terminal-transparency

gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type nothing
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type nothing
gsettings set org.gnome.settings-daemon.plugins.power idle-dim false
gsettings set org.gnome.desktop.screensaver idle-activation-enabled false
gsettings set org.gnome.desktop.privacy remember-recent-files false
gsettings set org.gnome.desktop.peripherals.touchpad tap-to-click true
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
gsettings set org.gnome.desktop.wm.keybindings switch-windows "['<Primary>Tab']"
gsettings set org.gnome.desktop.wm.keybindings switch-windows-backward "['<Primary><Shift>Tab']"
gsettings set org.gnome.desktop.wm.keybindings switch-applications "['<Super>Tab', '<Alt>Tab']"
gsettings set org.gnome.desktop.wm.keybindings switch-applications-backward "['<Shift><Super>Tab', '<Shift><Alt>Tab']"
gsettings set org.gnome.settings-daemon.plugins.media-keys window-screenshot-clip "['disabled']"
gsettings set org.gnome.settings-daemon.plugins.media-keys area-screenshot-clip "['<Primary>Print']"
gsettings set org.gnome.settings-daemon.plugins.media-keys window-screenshot "['disabled']"
gsettings set org.gnome.settings-daemon.plugins.media-keys screenshot-clip "['<Primary><Shift>Print']"
gsettings set org.gnome.settings-daemon.plugins.media-keys area-screenshot "['Print']"
gsettings set org.gnome.settings-daemon.plugins.media-keys screenshot "['<Shift>Print']"
```

**After Nextcloud sync complete**, enable your plugins and config your plugins.

- OPT: thunderbird

Config editor: set `mail.openpgp.allow_external_gnupg` to true.   
AccountSettings -> Composition -> WhenQuoting: set `start my reply above the quote`, and place my signature `below my reply`. 

- OPT: libreoffice

Select `Tools>Options>LibreOffice Writer>Formatting Aids` from the menu. For Image/Anchor you can select: `As Character` .

Select `Tools -> Autocorrect -> Autocorrect Options` from the menu, then `Localized options`, uncheck everything. 

Select `Tools -> Autocorrect -> Autocorrect Options` from the menu, then `Options`, uncheck everything. 

`Tools -> Options -> LibreOffice Calc -> General -> Measurement unit`, change to `Centimeter`

- OPT: firefox

Visit `about:config` and set/add the following entries: 

```
browser.tabs.tabmanager.enabled = false
services.sync.prefs.sync.browser.uiCustomization.state = true
browser.tabs.hoverPreview.enabled = false
```

> Ref: <https://support.mozilla.org/en-US/questions/1292568>

- OPT: CLion

~~Must use Clion 2022.1, do not upgrade because of severe performance downgrade.
Add `-fsized-deallocation` to clangd flags in `Settings | Languages & Frameworks | C/C++ | Clangd`.~~


[starting 2023] Disable `reopen projects on startup` <https://stackoverflow.com/questions/5362036/how-to-prevent-open-last-projects-when-intellij-idea-starts>

- OPT: microsoft devbox setup

Refer to <https://git.recolic.net/root/ms-scripts/-/blob/master/notes/workspace-bootstrap-ms.md>

- OPT: wayland fix

Set /etc/environment

```
QT_QPA_PLATFORM=wayland
```
