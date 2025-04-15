# Reproduce recolic's workspace

## PC / MPC / HMS / MSPC

> After installing Arch Linux

```
set hostname manually otherwise startup doesn't work
set root password
run linuxconf mgr
(follow linuxconf instruction)
```

<!--
# doesn't work for intel NIC
echo "options cfg80211 ieee80211_regdom=AU" >> /etc/modprobe.d/cfg80211.conf
echo "options cfg80211 internal_regdb=y" >> /etc/modprobe.d/cfg80211.conf
echo "options cfg80211 crda_support=y" >> /etc/modprobe.d/cfg80211.conf
pacman -S --noconfirm wireless-regdb
-->

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
