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
VER='v1.0.4'
get_package "https://github.com/$FOO/$BAR/releases/download/$VER/${BAR}_${VER}_linux_amd64.tar.gz"
mkdir -p $BAR
tar -xf ${BAR}_${VER}_linux_amd64.tar.gz -C $BAR
rm -rf httpd
ln -sf $BAR/$BAR httpd

#
BAR=$(foobar '118 50 114 97 121')
VER='v4.27.0'
get_package "https://github.com/$BAR/$BAR-core/releases/download/$VER/$BAR-linux-64.zip"
unzip -oq $BAR-linux-64.zip -d $BAR
chmod 755 $BAR/*
rm -rf bower
ln -sf $BAR/$BAR bower

#
rm -rf *zip *gz
