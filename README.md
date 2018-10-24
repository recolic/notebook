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

# DO NOT FORGET WRITING DOCKER-RUN INTO rc.local



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
