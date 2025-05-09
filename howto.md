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

## http upload server

<details>
  <summary>Deprecated</summary>
```
python3 -m pip install --user uploadserver
python3 -m uploadserver -b ::0
# Then access localhost:8000/upload with browser
```
</details>

```
# Installed on all recolic nodes.
simple-http-server -u -l 8000100100
```

## use hp4100 printer

Bad solution: Install and enable avahi service, and add printer.

Good solution: `sudo lpadmin -p MyPrinter -v 'ipp://10.100.100.178:631/ipp/print' -E -m everywhere`

## yt-dlp usage

```
yt-dlp --write-sub --write-auto-sub --sub-lang "en.*" "https://youtube.com/xxxxxxxxxxxxxxxxxxxx"
```

https://www.reddit.com/r/youtubedl/comments/wpq4y0/ytdlp_how_to_ensure_download_of_english_subtitles/

## GPG software for Windows noob

`gpg4win` at <https://gpg4win.org/download.html>

## 3HK prepaid SIM: Must install app for KYC verification, but the app doesn't work

`Need My3 app for real-name registration`: It's a lie.

Best solution: Just use the real KYC link. <https://www.three.com.hk/prepaid/account/tc/rnr-reg>

Alternative solution: If you love the app so much, you can download the correct app manually. The appid must be `hk.com.three.my3plus`. If Play Store says not available, download apk from 3rd-party.

## journal cleanup

```
journalctl --disk-usage
journalctl --vacuum-size=20M
```

## install intel icc

```
## Please run following as root:

echo "deb https://apt.repos.intel.com/oneapi all main" >/etc/apt/sources.list.d/intel-oneapi.list
apt update
apt install ca-certificates gnupg
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BAC6F0C353D04109
apt update
apt install intel-oneapi-compiler-dpcpp-cpp-and-cpp-classic

source /opt/intel/oneapi/setvars.sh
icpc -V
```

## aria2c seed only?

```
aria2c --bt-seed-unverified -V --seed-ratio=0.0 -d/path/to/download xxx.torrent
aria2c --bt-seed-unverified -V --seed-ratio=0.0 -d. xxx.torrent
```

## Microsoft Office

Use office pro plus 2021. It doesn't require login.

DO NOT install Microsoft 365.
