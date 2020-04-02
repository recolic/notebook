# recolic's private notebook

Some note about deploying my website and other things. Github is indeed a good online markdown writer.

I'm just making it public for convenience. **Please leave if you are not me. Commands here won't succeed without authorization.**


## common

currently using uswest server by DO, docker image is hosted by Amazon ECR (600163736385.dkr.ecr.us-west-2.amazonaws.com). 

Get login info (valid for 12h)
```
aws ecr get-login --no-include-email --region us-west-2
```

docker-push.sh (deprecated)
```
#!/bin/bash

[[ $1 == '' ]] && echo "Usage: $0 <image_name>[:latest]" && exit 1

docker tag $1 600163736385.dkr.ecr.us-west-2.amazonaws.com/$1 &&
docker push 600163736385.dkr.ecr.us-west-2.amazonaws.com/$1

exit $?
```

do not use docker attach. 
```
docker exec -ti rweb /bin/bash
```

# DO NOT FORGET WRITING DOCKER-START INTO rc.local

## proxi-ed http port usage:

|port|service|
|-----|-----|
|3091|www|
|3092(https!)|mail|
|3080|tm|
|3081|baidupan_proxy|
|3000|rocket|
|3003|riot|
|3083|drive|
|10000|v2ray|
|2080|git|
|8080|test_only|

## reserved port on all recolic servers:

|port|service|
|-----|-----|
|80|nginx-only rproxy http|
|443|nginx-only rproxy https|
|25580|shadowsocks|
|3128|http_proxy|
|1080|socks5|
|10808|socks5|
|25581|snakesocks|
|466|shadowsocksR|
|588|shadowsocksR|
|30999|FRPS server|
|30998|FRPS monitor|
|30997|FRPC console|
|30500-30899|FRP server dynamic ports|


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

fresh deploy
```
mkdir -p /srv/iredmail
docker run -tid --privileged -p 3092:443 -p 110:110 -p 995:995 -p 143:143 -p 993:993 -p 25:25 -p 465:465 -p 587:587 -v /srv/iredmail/vmail:/var/vmail -v /srv/iredmail/mysql:/var/lib/mysql -v /srv/iredmail/clamav:/var/lib/clamav -v /root/.acme.sh/mail.recolic.net/mail.recolic.net.key:/etc/ssl/private/iRedMail.key -v /root/.acme.sh/mail.recolic.net/fullchain.cer:/etc/ssl/certs/iRedMail.crt --name rmail --restart=always --hostname func.mail.recolic.net 600163736385.dkr.ecr.us-west-2.amazonaws.com/mail.recolic.net /entry.sh
```

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
postmaster -> passwd(mail.recolic.net / org)
root, admin -> passwd(recolic.net / org)

cert issue: (used **only inside container**)
```
./acme.sh --issue -d mail.recolic.net -d imap.recolic.net -d pop3.recolic.net -d smtp.recolic.net -d mail.recolic.org -d imap.recolic.org -d pop3.recolic.org -d smtp.recolic.org --dns dns_cf
```

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

## rserver-monitor

```
touch /srv/html/status.html
docker run -d --name rmon --restart=always -v /srv/html/status.html:/app/status.html recolic/rserver-status
```

## rocket chat [closed, 2019 data on drive machine, 2020 version running]

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
