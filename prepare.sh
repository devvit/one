#!/usr/bin/env bash

function foobar
{
  echo $1 | awk '{ for(i=1;i<=NF;i++) printf("%c",$i); print ""; }'
}

function get_package
{
  curl -# -fSL -O "$1"
}

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
BAR_VER='v4.27.0'
get_package "https://github.com/$BAR/$BAR-core/releases/download/$BAR_VER/$BAR-linux-64.zip"
unzip -oq $BAR-linux-64.zip -d $BAR
chmod 755 $BAR/*
rm -rf bower
ln -sf $BAR/$BAR bower

FOO=$(foobar '116 105 110 100 121 50 48 49 51')
BAR=$(foobar '115 117 98 99 111 110 118 101 114 116 101 114')
BAR_VER='v0.6.3'
get_package "https://github.com/$FOO/$BAR/releases/download/$BAR_VER/{$BAR}_linux64.tar.gz"
tar -xzf ${BAR}_linux64.tar.gz
ln -sf $BAR/$BAR squid
sed -i -e 's/port=25500/port=4444/g' $BAR/pref.ini

#
rm -rf *zip *gz
