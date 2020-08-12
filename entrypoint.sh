#!/usr/bin/env bash

if [ ! -f /etc/alpine-release ]; then
  bash prepare.sh
fi

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
cat templates/index.html | grep icon | sed -n 's/.*href="\([^"]*\).*/\1/p' | sed 's/data:image\/x-icon;base64,//g' | base64 -d > bower.json

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
