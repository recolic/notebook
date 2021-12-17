# recolic's private notebook

Some note about deploying my website and other services. 

I'm just making it public for convenience. **Commands here won't succeed without authorization.**

If you want to deploy a similiar service, the following content may help. But be careful, this is not a guide, this is my private notebook. 

## common

currently using uswest server by DO, docker image is hosted by Amazon ECR (600163736385.dkr.ecr.us-west-2.amazonaws.com). 

Get login info (valid for 12h)
```
aws ecr get-login --no-include-email --region us-west-2
```

do not use docker attach. 
```
docker exec -ti rweb /bin/bash
```

Every server saves `acme.sh`, `nginx.conf`, `crontab.log`, `cert.sh`, `startup.sh` into `/srv/conf`. Every server has an nginx, which redirects 
all HTTPS traffic to `http://localhost:xxxx`. 

## docker-ipv6 support (NAT mode)

Requires docker > 20.10.2, edit `/etc/docker/daemon.json`: 

```json
{
  "experimental": true,
  "ip6tables": true,
  "ipv6": true,
  "fixed-cidr-v6": "fd00:dead:beef::/48",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  }
}
```

# DO NOT FORGET WRITING DOCKER-START INTO rc.local

## proxi-ed http port usage:

|port|service|
|-----|-----|
|2080|git|
|3000|rocket|
|3002|riot.backend|
|3003|riot.web|
|3004(https)|zulip|
|3007|wishbox|
|3008|onlyoffice|
|3080|tm|
|3081|baidupan_proxy|
|3083|drive|
|3091|www|
|3092(https)|mail|
|6080|WebVirtMgr(VNC-Proxy)|
|6081|WebVirtMgr|
|6088|Android ADB Web|
|8080|test_only|
|8448(https)|matrix.api|
|10000|v2ray|

## reserved port on all recolic servers:

|port|service|
|-----|-----|
|80|nginx-only rproxy http|
|443|nginx-only rproxy https|
|81|secondary-http|
|444|secondary-https|
|22|ssh|
|4022|secondary-ssh|
|25566|secondary-ssh|
|25567|secondary-ssh|
|5700-5710|VNC|
|3389|RDP|
|3128|http_proxy|
|1080|socks5|
|10808|socks5|
|25551|shadowsocks|
|25580|shadowsocks|
|25581|snakesocks|
|25554|openvpn|
|1194|openvpn|
|466|shadowsocksR|
|588|shadowsocksR|
|30999|FRPS server|
|30998|FRPS monitor|
|30997|FRPC console|
|30500-30899|FRP server dynamic ports|
|9399|Virtualbox web interface|
|9000-9389|Virtualbox dynamic ports (RDP)|
|31000-31499|Virtualbox dynamic ports (Other use)|
|30400-30499|Generic dynamic ports (Other use)|

--------

# Services

> doc for closed services are archived into archived/README.md

## www.recolic.net

fresh deploy:
201905 update: move all /var out.
201911 update: remove https, remove zhixiang, logs, reconstructed.
202106 update: re-written from stretch, simple state-less dockerfile. https://git.recolic.net/root/scripts/-/tree/one/groundup/php-nginx

Put the website into /srv/html, and make sure `/srv/html/.config/nginx.conf` exists. 

```
docker run --log-opt max-size=10M -tid -p 3091:80 -v /srv/html:/var/www/html --name rwww --restart=always recolic/php-nginx /entry.sh
```

The docker image is HTTP-only and contains no certificate since 20210630. 

## mail.recolic.net

too complicated. Refer to this article: https://recolic.net/blog/2020/10/self-build-iredmail-in-docker

mig: copy /srv/iredmail out, commit and push docker(nothing may changed).
```
docker commit rmail 600163736385.dkr.ecr.us-west-2.amazonaws.com/mail.recolic.net
docker push 600163736385.dkr.ecr.us-west-2.amazonaws.com/mail.recolic.net

rsync -avz /srv/iredmail/mysql/ $newServerIp:/srv/iredmail/mysql
rsync -avz /srv/iredmail/vmail/ $newServerIp:/srv/iredmail/vmail
#           ------------------^-------------
# Be caution to the slash     |
```

passwd:
postmaster -> passwd(mail.recolic.net)
root, admin -> passwd(recolic.net)
    
crontab should restart docker container every 3 month, to renew email server certificate. 

## openvpn-server

build from stretch (modified from kylemanna)
```
git clone https://github.com/kylemanna/docker-openvpn.git
# remove the line: VOLUME ["/etc/openvpn"]
docker build --pull --tag recolic/openvpn -f Dockerfile .

docker run --log-opt max-size=10M -ti -p 1194:1194/udp --cap-add=NET_ADMIN --name rvpn recolic/openvpn
#### Now you're in container
#### ovpn_genconfig -u udp://ovpn.recolic.net
#### ovpn_initpki
#### vi /add_cli.sh
#### ctrl-P-Q

docker exec -ti rvpn /add_cli.sh recolic
# add more users
docker commit rvpn recolic/openvpn
docker tag recolic/openvpn:latest 600163736385.dkr.ecr.us-west-2.amazonaws.com/openvpn-server:latest
docker push 600163736385.dkr.ecr.us-west-2.amazonaws.com/openvpn-server:latest
```

/add_cli.sh
```
#!/bin/bash

[[ $1 == '' ]] && echo "Usage: $0 clientName" && exit 1

echo 'Use CA password genpasswd(ovpn.recolic.net)'
client="$1"

easyrsa build-client-full "$client" nopass &&
    ovpn_getclient "$client"
```

fresh deploy && mig (nodata!)
```
docker run --log-opt max-size=10M -tid -p 1194:1194/udp --cap-add=NET_ADMIN --name rvpn --privileged --restart=always 600163736385.dkr.ecr.us-west-2.amazonaws.com/openvpn-server ovpn_run
```

push your changes(after adding some users)
```
docker commit rvpn 600163736385.dkr.ecr.us-west-2.amazonaws.com/openvpn-server
docker push 600163736385.dkr.ecr.us-west-2.amazonaws.com/openvpn-server
```

## git.recolic.net

deploy (using /srv as datadir)
```
docker run --log-opt max-size=10M --detach \
  --hostname git.recolic.net \
  --publish 20443:443 --publish 2080:80 --publish 0.0.0.0:22:22 \
  --name rgit \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab \
  --volume /srv/gitlab/logs:/var/log/gitlab \
  --volume /srv/gitlab/data:/var/opt/gitlab \
  gitlab/gitlab-ce:latest
```

exec
```
docker exec -ti rgit /bin/bash
```

frontend cert issue:
```
./acme.sh --issue -d git.recolic.net -d tm.recolic.net -d hustdb.recolic.net -d git.recolic.org -d tm.recolic.org -d hustdb.recolic.org --dns dns_cf
```

## drive.recolic.net

data dir: `/srv/nextcloud`.

```
docker run --log-opt max-size=10M -d -p 3083:80 --name rdrive --restart=always -v /srv/nextcloud/nextcloud:/var/www/html -v /srv/nextcloud/apps:/var/www/html/custom_apps -v /srv/nextcloud/config:/var/www/html/config -v /srv/nextcloud/data:/var/www/html/data -v /srv/nextcloud/theme:/var/www/html/themes/rdef nextcloud
```

upgrade: at most one BIG-version each time. just stop and run with new image version. 

- customize

I strongly recommend you to disable the "Text" app, and enable "Plain Text Editor" and "Markdown Editor". The builtin Text app doesn't support table in markdown... 

This is my active app list: 

```
Accessibility
Activity
Automated PDF conversion
Calendar
Comments
Contacts Interaction
Deleted files
Federation
File sharing
First run wizard
GitHub integration
GitLab integration
Log Reader
Markdown Editor
Monitoring
Nextcloud announcements
Notifications
Password policy
PDF viewer
Plain text editor
Privacy
Right click
Share by mail
Social sharing via email
Support
Tasks
Theming
Usage survey
User status
Versions
Video player
Weather status
```

|If you|Want|Don't want|
|---|---|---|
|Task management|Use `2do` android app|disable Calendar and Tasks|
|Startup dashboard|Enable dashboard|Disable GitHub integration,GitLab integration,Weather Status|

## rserver-monitor

source=<https://git.recolic.net/root/server-monitor>

```
touch /srv/html/status.html
docker run --log-opt max-size=10M -d --name rmon --restart=always -v /srv/html/status.html:/app/status.html recolic/rserver-status
```

## Matrix + Riot.im (TODO: it's outdated)

> https://git.recolic.net/root/matrix-riot-docker

## new Shadowsocks server setup 2020

```
wget https://golang.org/dl/go1.15.linux-amd64.tar.gz -O - | tar -xz -C /usr/local
cp /usr/local/go/bin/go /usr/bin
go get -v github.com/shadowsocks/go-shadowsocks2
```

- /etc/rc.local:
```
nohup /root/go/bin/go-shadowsocks2 -s 'ss://chacha20-ietf-poly1305:>>>>>>>>>>>>>>>>>>>ADD_PASSWORD<<<<<<<<<<<<<<<<<<<<@:25551' -verbose >> /var/log/ss.log 2>&1 & disown 
```

gen url: https://zhiyuan-l.github.io/SS-Config-Generator/

## blog (htmly), included in www.recolic.net docker image

- fresh deploy

Patched: https://github.com/recolic/htmly

htmly is flat-file-d, so just add nginx config: 

```
    location /htmly/ {
        try_files $uri $uri/ /htmly/index.php?$args;
    }
  location ~ /htmly/config/ {
     deny all;
  }
  location ~ \.php$ {
        fastcgi_pass			unix:/run/php-fpm/php-fpm.sock;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
        include        fastcgi_params;
  }
```

then `mkdir htmly && chmod 777 htmly && cd htmly && wget https://github.com/danpros/htmly/releases/download/v2.7.5/installer.php`. 

Then everything is done. Admin password is `recolic, genpasswd(recolic.net, v4)`

> Warning: installer.php not working on my prod environment. Seems like URL prefix error. Please download source code zip, and modify `config/*` manually. 

- patch

modify functions.php to make disqus working:

```
// Disqus on post.
function disqus($title = null, $url = null)
{
    $comment = config('comment.system');
    $disqus = config('disqus.shortname');
    $script = <<<EOF
    <script type="text/javascript">
        var getAbsolutePath = function(href) { 
            var link = document.createElement('a');
            link.href = href;
            return link.href;
        };
    var disqus_config = function () {
    this.page.url = getAbsolutePath('{$url}');  // Replace PAGE_URL with your page's canonical URL variable
    };
    (function() { // DON'T EDIT BELOW THIS LINE
    var d = document, s = d.createElement('script');
    s.src = 'https://{$disqus}.disqus.com/embed.js';
    s.setAttribute('data-timestamp', +new Date());
    (d.head || d.body).appendChild(s);
    })();
    </script>
EOF;
    if (!empty($disqus) && $comment == 'disqus') {
        return $script;
    }
}
```

for 'gridzone' theme, search for `.entry code` in style.css, and remove its background. Just to make it looks better... 

- migrate

all files inside /srv/html. Migrate together with www.recolic.net. 

## LAN printer (CUPS)

- build from stretch (from archwiki)

```
pacman -S cups avahi nss-mdns
```

edit /etc/nsswitch.conf: find the `hosts` line, add `mdns_minimal [NOTFOUND=return]` BEFORE `resolve ... dns`. 

To allow LAN to access the web interface, do

```sh
vim /etc/cups/cupsd.conf # EDIT: listen 0.0.0.0:631
cupsctl --remote-admin --remote-any --share-printers
```

Enable and start `avahi-daemon.service` and `org.cups.cupsd.service`. 

- PPD file for HP 1020

https://github.com/koenkooi/foo2zjs/blob/master/PPD/HP-LaserJet_1020.ppd

HP1020 should use CUPS 2.3.3-3 (ArchLinux) and **should not upgrade**. 

- FAQ: 

1. Filter failed: Please read /var/log/cups/error.log to find the actual error. 
2. In error.log, foo2zjs-wrapper: command not found: Install AUR package `foo2zjs-nightly`. 
3. `lpinfo -v` shows `usb://unknown/printer`, or `Waiting for printer to become available` after archlinux upgrade:   
  Please [downgrade cups/libcups to 2.3.3-3](https://wiki.archlinux.org/index.php/CUPS/Troubleshooting#Issues_Relating_to_Upgrade_2.3.3-3_-%3E_2.3.3+106+ga72b0140e-1), and downgrade cups-filters to 1.28.5-1, and set these packages as IgnorePkg in `/etc/pacman.conf`. Switching Arch's CUPS upstream from Apple's senescent original to the actively-developed OpenPrinting fork broke your CUPS. 
4. TODO

## Gitlab runner

```
# Linux x86-64
sudo curl -L --output /usr/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64

sudo chmod +x /usr/bin/gitlab-runner
sudo useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash
sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner
sudo gitlab-runner start

#############################

apt install -y docker.io
sudo gitlab-runner register -n \
  --url https://git.recolic.net/ \
  --registration-token K9bsS-UPjjyxxLX1FVUW \
  --executor docker \
  --description "Give a name here" \
  --docker-image "ubuntu" \
  --docker-privileged

# remove the `locked` tag from gitlab manually
# Use `sudo gitlab-runner register --docker-privileged` to register manually. 
```

Docker-in-docker: Set firewall rule to prevent Internet from accessing port 2375. 

> disable tls if there's any problem. https://docs.gitlab.com/ee/ci/docker/using_docker_build.html

## WebVirtMgr

- Setup Web Portal

First run (setup database):

```
# Web Portal
sudo docker run --log-opt max-size=10M -d --name webvirtmgr -v /srv/webvirt:/data/ -e WEBVIRTMGR_ADMIN_USERNAME=admin -e WEBVIRTMGR_ADMIN_EMAIL=admin@local.domain -e WEBVIRTMGR_ADMIN_PASSWORD=password -p 6081:8000 odivlad/webvirtmgr
```

Then use

```
# Web Portal
sudo docker run --log-opt max-size=10M -d --restart=always --name webvirtmgr -v /srv/webvirt:/data/ -p 6081:8000 odivlad/webvirtmgr
# VNC proxy
sudo docker run --log-opt max-size=10M -d --restart=always --name webvirtmgr-console -v /srv/webvirt:/data/ -p 6080:6080 odivlad/webvirtmgr webvirtmgr-console
```

- Setup Host machine

Arch packages: `ebtables bridge-utils dnsmasq openbsd-netcat libvirt edk2-ovmf dmidecode qemu-headless`

Read [archwiki](https://wiki.archlinux.org/index.php/Libvirt) and set libvirtd.conf:

```
listen_tls = 0
listen_tcp = 1
tcp_port = "16509"
listen_addr = "0.0.0.0"
auth_tcp = "none"
```

If requiring auth, set `auth_tcp = "sasl"` and read <https://github.com/retspen/webvirtmgr/wiki/Setup-TCP-authorization>

DO NOT use systemd service (it always crash with `--listen parameter not permitted with systemd activation sockets`). Directly run `sudo libvirtd --listen`

```
sudo systemctl enable --now virtlogd
sudo libvirtd --listen
```

## Android ADB web

<https://github.com/say-no-to-wechat/android-web-control-docker>

## Gitlab2github gitsync

source=<https://git.recolic.net/root/gitlab2github>

```
docker run --log-opt max-size=10M -d --restart=always --name rgitsync --env github_user_dst="recolic:ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" recolic/gitlab2github
```

## recolic mirror site

source=<https://git.recolic.net/root/aur-autobuild-mirror>

Clone the repo and setup crontab. 

## storage.recolic.net

follow the guide at source=<https://git.recolic.net/root/scripts/-/tree/one/storage-server-backup-sh>

## dedicated v2ray

usually, I run v2ray with a real web server, usually drive.recolic.net or git.recolic.net. However, sometimes, we want to setup v2ray on a dedicated toy cock. 

```
curl -O https://raw.githubusercontent.com/jinwyp/one_click_script/master/trojan_v2ray_install.sh && chmod +x ./trojan_v2ray_install.sh && ./trojan_v2ray_install.sh
```

