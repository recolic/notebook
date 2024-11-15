# Reproduce recolic's workspace

> If you're in fucking China, change all `recolic.net` to breakwall domain (such as recolic.cc). 

## GUI Workspace

> After installing Arch Linux, run as root

```
pacman -Sy --noconfirm fish dhcpcd vim sudo openssh
useradd --create-home --shell /usr/bin/fish recolic
echo 'recolic ALL=(ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo

pacman -Sy --noconfirm gnome networkmanager power-profiles-daemon nextcloud-client firefox
systemctl enable gdm NetworkManager power-profiles-daemon

### Require Input
passwd recolic

```

> Reboot. Log into gnome as recolic, login Nextcloud.

**After Nextcloud sync complete**, run **as recolic**:

```
bash ~/Nextcloud/workspace/init.bash
```

<!--
# doesn't work for intel NIC
echo "options cfg80211 ieee80211_regdom=AU" >> /etc/modprobe.d/cfg80211.conf
echo "options cfg80211 internal_regdb=y" >> /etc/modprobe.d/cfg80211.conf
echo "options cfg80211 crda_support=y" >> /etc/modprobe.d/cfg80211.conf
pacman -S --noconfirm wireless-regdb
-->

- gnome configure

**After Nextcloud sync complete**, enable and config your plugins.

- OPT: thunderbird

Config editor: set `mail.openpgp.allow_external_gnupg` to true.   
AccountSettings -> Composition -> WhenQuoting: set `start my reply above the quote`, and place my signature `below my reply`. 

- OPT: libreoffice

Select `Tools>Options>LibreOffice Writer>Formatting Aids` from the menu. For Image/Anchor you can select: `As Character` .

Select `Tools -> Autocorrect -> Autocorrect Options` from the menu, then `Localized options`, uncheck everything. 

Select `Tools -> Autocorrect -> Autocorrect Options` from the menu, then `Options`, uncheck everything. 

`Tools -> Options -> LibreOffice Calc -> General -> Measurement unit`, change to `Centimeter`

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
