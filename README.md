# recolic's private notebook

Some note about deploying my website and other things. 

I'm just making it public for convenience. **Commands here won't succeed without authorization.**

## firstly setup new vm

```
curl https://recolic.net/setup/ | bash
```

## common

currently using uswest server by DO, docker image is hosted by Amazon ECR (600163736385.dkr.ecr.us-west-2.amazonaws.com). 

Get login info:
```
aws ecr get-login --no-include-email --region us-west-2
```

docker-push.sh
```
#!/bin/bash

[[ $1 == '' ]] && echo "Usage: $0 <image_name>[:latest]" && exit 1

docker tag $1 600163736385.dkr.ecr.us-west-2.amazonaws.com/$1 &&
docker push 600163736385.dkr.ecr.us-west-2.amazonaws.com/$1

exit $?
```

## recolic.net

fresh deployment
```
mkdir -p /var/www.recolic.net-tmp
docker run -tid -p 80:80 -p 443:443 -v /var/www.recolic.net-tmp:/var/www/html/tmp --name r 600163736385.dkr.ecr.us-west-2.amazonaws.com/www.recolic.net /entry.sh
```

mig (just commit and push)
```
docker commit r 600163736385.dkr.ecr.us-west-2.amazonaws.com/www.recolic.net
./docker-push.sh www.recolic.net
```

## mail.recolic.net

fresh deploy
```
mkdir -p /docker_data
docker run --privileged -v /docker_data/vmail:/var/vmail -v /docker_data/mysql:/var/lib/mysql -v /docker_data/clamav:/var/lib/clamav -tid --name r --hostname func.mail.recolic.net 600163736385.dkr.ecr.us-west-2.amazonaws.com/mail.recolic.net /entry.sh
```

mig: copy /docker_data out, commit and push docker(nothing may changed).
