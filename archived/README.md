
## tw1 migration (gcp)

run `ssh-keygen -A` by serial after setup the new machine.

## www.recolic.net

cert issue: (note that currently mail and www are on same machine. )
```
./acme.sh --issue -d recolic.net -d www.recolic.net -d dl.recolic.net -d mail.recolic.net -d recolic.org -d www.recolic.org -d dl.recolic.org -d mail.recolic.org --dns dns_cf
./acme.sh --issue -d recolic.net -d www.recolic.net -d dl.recolic.net -d mail.recolic.net -d recolic.org -d www.recolic.org -d dl.recolic.org -d mail.recolic.org --dns dns_cf --keylength ec-384

# For mail.recolic.net container, it runs imap/smtp/pop3...
./acme.sh --issue -d mail.recolic.net -d imap.recolic.net -d pop3.recolic.net -d smtp.recolic.net -d mail.recolic.org -d imap.recolic.org -d pop3.recolic.org -d smtp.recolic.org --dns dns_cf
```


## tm.recolic.net

build docker image
```
docker build -f Dockerfile --tag tm --build-arg GIT_REPO_TM_WEB="https://path/to/your/tm.git" .
docker tag tm 600163736385.dkr.ecr.us-west-2.amazonaws.com/tm
```

deploy (using /srv as datadir)
```
docker run --log-opt max-size=10M -tid -v /srv/tm/log:/app/log -v /srv/tm/keys:/app/keys -p 3080:80 --name rtm --restart=always 600163736385.dkr.ecr.us-west-2.amazonaws.com/tm
# Then use nginx to proxy_pass port 3080.
```

exec
```
docker exec -ti rtm /bin/bash
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
docker run --log-opt max-size=10M -d --restart=always --name rmd-agent -m 100m -p 8080:8080 recolic/push-to-markdown-agent
```

## rocket chat [closed, data on drive machine]

datadir: /srv/mongo

with `/srv/mongo/mongod.conf`:

```
replication:
  replSetName: "rs01"
```

```
docker run --log-opt max-size=10M --name rdb --restart=always -v /srv/mongo:/data/db -v /srv/mongo/mongod.conf:/etc/mongod.conf -d mongo:latest --smallfiles --config /etc/mongod.conf
docker run --log-opt max-size=10M --name rocketchat --link rdb:db --restart=always -p 3000:3000 --env ROOT_URL=http://localhost --env 'MONGO_OPLOG_URL=mongodb://db:27017/local?replSet=rs01' -d rocket.chat
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

## Virtualbox server at HMS (deprecated, use webvirtmgr+KVM)

- setup

```
useradd vbox ; mkdir /home/vbox ; chown vbox:vbox /home/vbox ; usermod -a -G vboxusers vbox ; usermod -g vboxusers vbox
passwd vbox # vbox

docker run --log-opt max-size=10M --name vbox_http --restart=always -p 9399:80 \
    -e ID_HOSTPORT=10.100.100.101:18083 -e ID_NAME=hms.recolic -e ID_USER=vbox -e ID_PW='vbox' -e CONF_browserRestrictFolders="/mnt/fsdisk/nfs/rpc_downloads,/home" \
    -d joweisberg/phpvirtualbox
    # version 6.1.x
```

- daemon (on every boot)

```
nohup sudo -u vbox /usr/bin/vboxwebsrv --host 0.0.0.0 & disown
```

## onlyoffice server for nextcloud online office

```
# The server is stateful, but no need to save it at all.
docker run --log-opt max-size=10M -tid --restart=always --name roffice -p 3008:80 onlyoffice/documentserver
```




