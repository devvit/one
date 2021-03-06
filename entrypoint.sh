#!/usr/bin/env bash

# function foobar
# {
  # echo $1 | awk '{ for(i=1;i<=NF;i++) printf("%c",$i); print ""; }'
# }

# function get_package
# {
  # curl -fsSL -JO "$1"
# }

#
# FOO=$(foobar '99 97 100 100 121 115 101 114 118 101 114')
# BAR=$(foobar '99 97 100 100 121')
# VER='2.1.1'
# get_package "https://github.com/$FOO/$BAR/releases/download/v${VER}/${BAR}_${VER}_linux_amd64.tar.gz"
# mkdir -p $BAR
# tar -xzf ${BAR}_${VER}_linux_amd64.tar.gz -C $BAR
# rm -rf jetty
# ln -sf $BAR/$BAR jetty

#
# get_package "https://${FOO}.com/${BAR}-v1-docs-archive.tar.gz"
# tar -xzf ${BAR}-v1-docs-archive.tar.gz
# mv ${FOO}.com-archive www

#
# BAR=$(foobar '118 50 114 97 121')
# VER='4.28.2'
# get_package "https://github.com/$BAR/${BAR}-core/releases/download/v${VER}/${BAR}-linux-64.zip"
# unzip -oq ${BAR}-linux-64.zip -d $BAR
# chmod 755 $BAR/*
# rm -rf bower
# ln -sf $BAR/$BAR bower

#
# FOO=$(foobar '116 105 110 100 121 50 48 49 51')
# BAR=$(foobar '115 117 98 99 111 110 118 101 114 116 101 114')
# VER='0.6.3'
# get_package "https://github.com/$FOO/$BAR/releases/download/v${VER}/${BAR}_linux64.tar.gz"
# tar -xzf ${BAR}_linux64.tar.gz
# rm -rf grunt
# ln -sf $BAR/$BAR grunt

#
# rm -rf *zip *gz

# if [ ! -f /etc/alpine-release ]; then
# bash prepare.sh
# fi

#
if [ -n "$PORT" ]; then
  HTTP_PORT=$PORT
elif [ -n "$BLUEMIX_REGION" ]; then
  HTTP_PORT=8080
elif [ -n "$KUBERNETES_SERVICE_HOST" ]; then
  HTTP_PORT=8080
else
  HTTP_PORT=4000
fi

export HTTP_PORT

#
# cat templates/index.html | grep 'image/x-icon' | sed -n 's/.*href="\([^"]*\).*/\1/p' | sed 's/data:image\/x-icon;base64,//g' | base64 -d > bower.json
# cat templates/index.html | grep 'image/png' | sed -n 's/.*href="\([^"]*\).*/\1/p' | sed 's/data:image\/png;base64,//g' | base64 -d > bower.sh
# bash bower.sh

#
honcho start -f Procfile.honcho

# gcp: v2018-us-central1/europe-west1
# aws: us-east-1/us-west-2
# gigalixir create -n APP_NAME --stack gigalixir-18 --cloud aws --region us-west-2

# docker tag <image> registry.heroku.com/<app>/web
# docker push registry.heroku.com/<app>/<process-type>
# heroku container:release web
# heroku labs:enable log-runtime-metrics

# for f in `docker images -q`; do docker image rm -f $f; done
# docker container prune
# docker system prune -a

# https://github.com/cloudfoundry/python-buildpack
