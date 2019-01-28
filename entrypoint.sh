#!/usr/bin/env bash

function foobar
{
  echo $1 | awk '{ for(i=1;i<=NF;i++) printf("%c",$i); print ""; }'
}

function get_version
{
  curl --silent "https://api.github.com/repos/$1/releases/latest" | jq -r .tag_name
}

#
FOOBAR=$(foobar '99 97 100 100 121')
FOOBAR_VER=$(get_version "mholt/$FOOBAR")
curl -fSL -O "https://github.com/mholt/$FOOBAR/releases/download/$FOOBAR_VER/${FOOBAR}_${FOOBAR_VER}_linux_amd64.tar.gz"
mkdir -p $FOOBAR
tar -xzf ${FOOBAR}_${FOOBAR_VER}_linux_amd64.tar.gz -C $FOOBAR
ln -sf $FOOBAR/$FOOBAR httpd

#
FOOBAR=$(foobar '118 50 114 97 121')
FOOBAR_VER=$(get_version "$FOOBAR/$FOOBAR-core")
curl -fSL -O "https://github.com/$FOOBAR/$FOOBAR-core/releases/download/$FOOBAR_VER/$FOOBAR-linux-64.zip"
unzip -q $FOOBAR-linux-64.zip -d $FOOBAR
chmod 755 $FOOBAR/*
ln -sf $FOOBAR/$FOOBAR hhvm

# appport
if [ -z "$PORT" ]; then
  MY_APP_PORT=$PORT
elif [ -z "$BLUEMIX_REGION" ]; then
  MY_APP_PORT=8080
elif [ -z "$KUBERNETES_SERVICE_HOST" ]; then
  MY_APP_PORT=8080
else
  MY_APP_PORT=4000
fi

export MY_APP_PORT

#
honcho start -f Procfile.honcho
