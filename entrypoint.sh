#!/usr/bin/env bash

function foobar
{
  echo $1 | awk '{ for(i=1;i<=NF;i++) printf("%c",$i); print ""; }'
}

function get_package
{
  curl -# -fSL -O "$1"
}

# export http_proxy=http://192.168.56.1:8123
# export https_proxy=http://192.168.56.1:8123

#
FOO=$(foobar '99 97 100 100 121 115 101 114 118 101 114')
BAR=$(foobar '99 97 100 100 121')
BAR_VER='v1.0.4'
get_package "https://github.com/$FOO/$BAR/releases/download/$BAR_VER/${BAR}_${BAR_VER}_linux_amd64.tar.gz"
mkdir -p $BAR
tar -xf ${BAR}_${BAR_VER}_linux_amd64.tar.gz -C $BAR
rm -rf httpd
ln -sf $BAR/$BAR httpd

#
BAR=$(foobar '118 50 114 97 121')
BAR_VER='v4.22.1'
get_package "https://github.com/$BAR/$BAR-core/releases/download/$BAR_VER/$BAR-linux-64.zip"
unzip -oq $BAR-linux-64.zip -d $BAR
chmod 755 $BAR/*
rm -rf bower
ln -sf $BAR/$BAR bower

#
FOO=$(foobar '103 105 110 117 101 114 122 104')
BAR=$(foobar '103 111 115 116')
BAR_VER='v2.11.0'
get_package "https://github.com/$FOO/$BAR/releases/download/$BAR_VER/${BAR}-linux-amd64-${BAR_VER//v}.gz"
gunzip ${BAR}-linux-amd64-${BAR_VER//v}.gz
chmod 755 ${BAR}-linux-amd64-${BAR_VER//v}
rm -rf hhvm
ln -sf ${BAR}-linux-amd64-${BAR_VER//v} hhvm

#
rm -rf *zip *gz

#
if [ -n "$PORT" ]; then
  WWW_PORT=$PORT
elif [ -n "$BLUEMIX_REGION" ]; then
  WWW_PORT=8080
elif [ -n "$KUBERNETES_SERVICE_HOST" ]; then
  WWW_PORT=8080
else
  WWW_PORT=4000
fi

export WWW_PORT

#
cat static/index.html | grep icon | sed -n 's/.*href="\([^"]*\).*/\1/p' | sed 's/data:image\/x-icon;base64,//g' | base64 -d > bower.json

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
# docker system prune -a

# https://github.com/cloudfoundry/python-buildpack
