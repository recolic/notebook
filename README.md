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



## recolic.net

fresh deployment
```
mkdir -p /var/www.recolic.net-tmp
docker run -tid -p 80:80 -p 443:443 -v /var/www.recolic.net-tmp:/var/www/html/tmp --name rweb 600163736385.dkr.ecr.us-west-2.amazonaws.com/www.recolic.net /entry.sh
```

mig (just commit and push)
```
docker commit rweb 600163736385.dkr.ecr.us-west-2.amazonaws.com/www.recolic.net
docker push 600163736385.dkr.ecr.us-west-2.amazonaws.com/www.recolic.net
```

new netpush.sh
```
#!/bin/bash

[[ $1 == '' ]] && echo 'Put some file into https://recolic.net/tmp/. Usage: netpush <filename>' && exit 1

function do_push () {
    _path=$1
    _name=`basename $1`
    scp $_path root@recolic.net:/var/www.recolic.net-tmp/$_name &&
    echo 'Pushed to https://recolic.net/tmp/'"$_name"
}

for fl in "$@"
do
    do_push $fl
done
```

## mail.recolic.net

fresh deploy
```
mkdir -p /docker_data
docker run -tid --privileged -p 80:80 -p 443:443 -p 110:110 -p 995:995 -p 143:143 -p 993:993 -p 25:25 -p 465:465 -p 587:587 -v /docker_data/vmail:/var/vmail -v /docker_data/mysql:/var/lib/mysql -v /docker_data/clamav:/var/lib/clamav --name rweb --hostname func.mail.recolic.net 600163736385.dkr.ecr.us-west-2.amazonaws.com/mail.recolic.net /entry.sh
```

mig: copy /docker_data out, commit and push docker(nothing may changed).
```
docker commit rweb 600163736385.dkr.ecr.us-west-2.amazonaws.com/mail.recolic.net
docker push 600163736385.dkr.ecr.us-west-2.amazonaws.com/mail.recolic.net

rsync -avz /docker_data/mysql/ $newServerIp:/docker_data/mysql
rsync -avz /docker_data/vmail/ $newServerIp:/docker_data/vmail
#           -----------------^-------------
# Be caution to the slash|
```

passwd:
postmaster -> passwd(mail.recolic.net)
root, admin -> passwd(recolic.net)

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
docker run -tid -p 1194:1194/udp --cap-add=NET_ADMIN --name rvpn --privileged 600163736385.dkr.ecr.us-west-2.amazonaws.com/openvpn-server ovpn_run
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
docker run -tid -v /srv/tm/log:/app/log -v /srv/tm/keys:/app/keys -p 0.0.0.0:3080:80 --name rtm 600163736385.dkr.ecr.us-west-2.amazonaws.com/tm
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

## push-to-markdown agent

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
docker run -d -p 8080:80 --name rweb -v /srv/nextcloud/nextcloud:/var/www/html -v /srv/nextcloud/apps:/var/www/html/custom_apps -v /srv/nextcloud/config:/var/www/html/config -v /srv/nextcloud/data:/var/www/html/data -v /srv/nextcloud/theme:/var/www/html/themes/rdef nextcloud
```

