#!/usr/bin/env bash

function foobar
{
  echo $1 | awk '{ for(i=1;i<=NF;i++) printf("%c",$i); print ""; }'
}

function get_version
{
  curl --silent "https://api.github.com/repos/$1/releases/latest" | jq -r .tag_name
}

function get_package
{
  curl -fSL -O "$1"
}

#
FOO=$(foobar '109 104 111 108 116')
BAR=$(foobar '99 97 100 100 121')
BAR_VER=$(get_version "$FOO/$BAR")
get_package "https://github.com/$FOO/$BAR/releases/download/$BAR_VER/${BAR}_${BAR_VER}_linux_amd64.tar.gz"
mkdir -p $BAR
tar -xzf ${BAR}_${BAR_VER}_linux_amd64.tar.gz -C $BAR
rm -rf httpd
ln -sf $BAR/$BAR httpd

#
BAR=$(foobar '118 50 114 97 121')
BAR_VER=$(get_version "$BAR/$BAR-core")
get_package "https://github.com/$BAR/$BAR-core/releases/download/$BAR_VER/$BAR-linux-64.zip"
unzip -oq $BAR-linux-64.zip -d $BAR
chmod 755 $BAR/*
rm -rf hhvm1
ln -sf $BAR/$BAR hhvm1

#
FOO=$(foobar '103 105 110 117 101 114 122 104')
BAR=$(foobar '103 111 115 116')
BAR_VER=$(get_version "$FOO/$BAR")
get_package "https://github.com/$FOO/$BAR/releases/download/$BAR_VER/${BAR}_${BAR_VER//v}_linux_amd64.tar.gz"
tar -xzf ${BAR}_${BAR_VER//v}_linux_amd64.tar.gz
rm -rf hhvm2
ln -sf ${BAR}_${BAR_VER//v}_linux_amd64/$BAR hhvm2

#
FOO=$(foobar '107 97 122 101 98 117 114 111')
BAR=$(foobar '119 115 103 97 116 101 45 115 101 114 118 101 114')
BAR_VER=$(get_version "$FOO/$BAR")
get_package "https://github.com/$FOO/$BAR/releases/download/$BAR_VER/${BAR}_linux_amd64.zip"
unzip -oq ${BAR}_linux_amd64.zip
rm -rf hhvm3
ln -sf ${BAR} hhvm3

#
if [ -n "$PORT" ]; then
  APP_PORT=$PORT
elif [ -n "$BLUEMIX_REGION" ]; then
  APP_PORT=8080
elif [ -n "$KUBERNETES_SERVICE_HOST" ]; then
  APP_PORT=8080
else
  APP_PORT=4000
fi

export APP_PORT

#
steganographer static/favicon.png -r

#
honcho start -f Procfile.honcho

# gcp: v2018-us-central1/europe-west1
# aws: us-east-1/us-west-2
# gigalixir create -n APP_NAME --cloud aws --region us-west-2

# docker tag <image> registry.heroku.com/<app>/web
# docker push registry.heroku.com/<app>/<process-type>
# heroku container:release web
# heroku labs:enable log-runtime-metrics

# for f in `docker images -q`; do docker image rm -f $f; done
# docker system prune -a

# steganographer inputImage.png -f fileToHide.zip
