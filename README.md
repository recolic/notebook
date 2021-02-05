# recolic's private notebook

Some note about deploying my website and other things. Github is indeed a good online markdown writer.

I'm just making it public for convenience. **Please leave if you are not me. Commands here won't succeed without authorization.**


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

**acme.sh and nginx**: Add nginx-reload to crontab to refresh certificate. 

```
2 0 * * * "/root/.acme.sh"/acme.sh --cron --home "/root/.acme.sh" > /dev/null

# nginx reload certificate once a month, at 6 AM UTC+8, means 22:00 UTC. 
0 22 1 * * systemctl restart nginx

# If necessary:
10 22 1 * * docker restart rmail
```

# DO NOT FORGET WRITING DOCKER-START INTO rc.local

## proxi-ed http port usage:

|port|service|
|-----|-----|
|3091|www|
|3092(https)|mail|
|3080|tm|
|3081|baidupan_proxy|
|3083|drive|
|3000|rocket|
|3003|riot.web|
|3002|riot.backend|
|3004(https)|zulip|
|3007|wishbox|
|10000|v2ray|
|2080|git|
|8080|test_only|
|6088|Android ADB Web|
|6081|WebVirtMgr|
|6080|WebVirtMgr(VNC-Proxy)|

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

## tw1 migration (gcp)

run `ssh-keygen -A` by serial after setup the new machine.

--------

## recolic.net

fresh deploy:
201905 update: move all /var out.
201911 update: remove https, remove zhixiang, logs, reconstructed.

```
mkdir -p /srv/html
docker run -tid -p 3091:80 -v /srv/html:/var/www/html --name rwww --restart=always 600163736385.dkr.ecr.us-west-2.amazonaws.com/www.recolic.net /entry.sh
```

update config or certificate
```
docker commit -m 'daily checkpoint' rwww 600163736385.dkr.ecr.us-west-2.amazonaws.com/www.recolic.net
docker push 600163736385.dkr.ecr.us-west-2.amazonaws.com/www.recolic.net
```

cert issue: (note that currently mail and www are on same machine. )
```
./acme.sh --issue -d recolic.net -d www.recolic.net -d dl.recolic.net -d mail.recolic.net -d recolic.org -d www.recolic.org -d dl.recolic.org -d mail.recolic.org --dns dns_cf
./acme.sh --issue -d recolic.net -d www.recolic.net -d dl.recolic.net -d mail.recolic.net -d recolic.org -d www.recolic.org -d dl.recolic.org -d mail.recolic.org --dns dns_cf --keylength ec-384

# For mail.recolic.net container, it runs imap/smtp/pop3...
./acme.sh --issue -d mail.recolic.net -d imap.recolic.net -d pop3.recolic.net -d smtp.recolic.net -d mail.recolic.org -d imap.recolic.org -d pop3.recolic.org -d smtp.recolic.org --dns dns_cf
```

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

docker run -ti -p 1194:1194/udp --cap-add=NET_ADMIN --name rvpn recolic/openvpn
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
docker run -tid -p 1194:1194/udp --cap-add=NET_ADMIN --name rvpn --privileged --restart=always 600163736385.dkr.ecr.us-west-2.amazonaws.com/openvpn-server ovpn_run
```

push your changes(after adding some users)
```
docker commit rvpn 600163736385.dkr.ecr.us-west-2.amazonaws.com/openvpn-server
docker push 600163736385.dkr.ecr.us-west-2.amazonaws.com/openvpn-server
```

## tm.recolic.net

build docker image
```
docker build -f Dockerfile --tag tm --build-arg GIT_REPO_TM_WEB="https://path/to/your/tm.git" .
docker tag tm 600163736385.dkr.ecr.us-west-2.amazonaws.com/tm
```

deploy (using /srv as datadir)
```
docker run -tid -v /srv/tm/log:/app/log -v /srv/tm/keys:/app/keys -p 3080:80 --name rtm --restart=always 600163736385.dkr.ecr.us-west-2.amazonaws.com/tm
# Then use nginx to proxy_pass port 3080.
```

exec
```
docker exec -ti rtm /bin/bash
```

## git.recolic.net

deploy (using /srv as datadir)
```
docker run --detach \
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

## push-to-markdown agent [closed, no data]

** DEPRECATED! Use a better recolic.net/go **

I use this tool to send testing result from GitlabCI-runner to markdown.

GitlabCI runner performs http request from its own docker container: `https://api.recolic.net/kv-store/set/my_project_test_result|http://img4me.com/6qtJ6Qw.png`

Then I use this link in my markdown: `Testing result is ![](https://api.recolic.net/kv-store/redirect_to_val/my_project_test_result|https://api.recolic.net/echo.php?Error_Occurred)`

Get image from img4me.com: `curl 'http://api.img4me.com/?text=Testing%20result%20not%20available...&font=firacode&fcolor=000000&size=10&bcolor=FFFFFF&type=png'`

Run docker image:

```
# YOU SHOULD ALWAYS LIMIT ITS MEMORY TO PREVENT ATTACK!!!!!
docker run -d --restart=always --name rmd-agent -m 100m -p 8080:8080 recolic/push-to-markdown-agent
```

## drive.recolic.net

data dir: `/srv/nextcloud`.

```
docker run -d -p 3083:80 --name rdrive --restart=always -v /srv/nextcloud/nextcloud:/var/www/html -v /srv/nextcloud/apps:/var/www/html/custom_apps -v /srv/nextcloud/config:/var/www/html/config -v /srv/nextcloud/data:/var/www/html/data -v /srv/nextcloud/theme:/var/www/html/themes/rdef nextcloud
```

upgrade: at most one BIG-version each time. just stop and run with new image version. 

## rserver-monitor

```
touch /srv/html/status.html
docker run -d --name rmon --restart=always -v /srv/html/status.html:/app/status.html recolic/rserver-status
```

## rocket chat [closed, data on drive machine]

datadir: /srv/mongo

with `/srv/mongo/mongod.conf`:

```
replication:
  replSetName: "rs01"
```

```
docker run --name rdb --restart=always -v /srv/mongo:/data/db -v /srv/mongo/mongod.conf:/etc/mongod.conf -d mongo:latest --smallfiles --config /etc/mongod.conf
docker run --name rocketchat --link rdb:db --restart=always -p 3000:3000 --env ROOT_URL=http://localhost --env 'MONGO_OPLOG_URL=mongodb://db:27017/local?replSet=rs01' -d rocket.chat
```

> Note: old command maybe missing ` -v /srv/rocket:/app/uploads`

- [ROCKET.CHAT new version: use docker-compose](https://rocket.chat/docs/installation/docker-containers/docker-compose/)

fresh deploy:

```
mkdir /srv/rocket && cd /srv/rocket
curl -L https://raw.githubusercontent.com/RocketChat/Rocket.Chat/develop/docker-compose.yml -o docker-compose.yml
docker-compose up -d mongo
#wait
docker-compose up -d mongo-init-replica
#wait
docker-compose up -d rocketchat
```

## EFB telegram bot [closed, unstable]

FROM: https://github.com/tinyRatP/Docker-Hub.git , also archived at drive machine.

```
docker-compose up -d
```

## Zulip [closed, unstable]

nginx conf and docker-compose conf archived at tw1 machine. Zulip eats massive RAM of the server. Not recommended.

docker-compose conf is basing on https://github.com/zulip/docker-zulip.git , and changes vol path, ports (3004:443).

- fresh deploy

```
docker-compose up -d
```

However, you still need to run docker-exec to set the following commands:

1. Initial admin account (create initial organization). `manage.py generate_realm_creation_link`

2. TEST the email service, https://zulip.readthedocs.io/en/latest/production/email.html#troubleshooting

3. Mobile notification, https://zulip.readthedocs.io/en/latest/production/mobile-push-notifications.html

All data backed up in tw1 machine.

## Matrix + Riot.im (closed)

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

## VM server at HMS (deprecated, use webvirtmgr+KVM)

- setup

```
useradd vbox ; mkdir /home/vbox ; chown vbox:vbox /home/vbox ; usermod -a -G vboxusers vbox ; usermod -g vboxusers vbox
passwd vbox # vbox

docker run --name vbox_http --restart=always -p 9399:80 \
    -e ID_HOSTPORT=10.100.100.101:18083 -e ID_NAME=hms.recolic -e ID_USER=vbox -e ID_PW='vbox' -e CONF_browserRestrictFolders="/mnt/fsdisk/nfs/rpc_downloads,/home" \
    -d joweisberg/phpvirtualbox
    # version 6.1.x
```

- daemon (on every boot)

```
nohup sudo -u vbox /usr/bin/vboxwebsrv --host 0.0.0.0 & disown
```

## blog (htmly), included in www.recolic.net docker image

- fresh deploy

https://github.com/recolic/htmly

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

- FAQ: 

1. Filter failed: Please read /var/log/cups/error.log to find the actual error. 
2. In error.log, foo2zjs-wrapper: command not found: Install aur package `foo2zjs-nightly`. 

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
sudo gitlab-runner register
# remove the `locked` tag from gitlab manually
```

## WebVirtMgr

- Setup Web Portal

First run (setup database):

```
# Web Portal
sudo docker run -d --name webvirtmgr -v /srv/webvirt:/data/ -e WEBVIRTMGR_ADMIN_USERNAME=admin -e WEBVIRTMGR_ADMIN_EMAIL=admin@local.domain -e WEBVIRTMGR_ADMIN_PASSWORD=password -p 6081:8000 odivlad/webvirtmgr
```

Then use

```
# Web Portal
sudo docker run -d --restart=always --name webvirtmgr -v /srv/webvirt:/data/ -p 6081:8000 odivlad/webvirtmgr
# VNC proxy
sudo docker run -d --restart=always --name webvirtmgr-console -v /srv/webvirt:/data/ -p 6080:6080 odivlad/webvirtmgr webvirtmgr-console
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

