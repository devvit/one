FROM alpine

# ENV http_proxy 'http://192.168.56.1:8123'
# ENV https_proxy 'http://192.168.56.1:8123'

RUN apk add --no-cache \
  bash \
  curl \
  unzip \
  git \
  jq \
  grep \
  htop \
  python3 \
  && apk add --no-cache --virtual .build-deps build-base linux-headers musl-dev python3-dev

COPY . /app
RUN chmod 777 /app
WORKDIR /app

RUN pip3 install -U -r /app/requirements.txt

RUN apk del .build-deps

RUN adduser -D somebody
USER somebody
EXPOSE 8080
ENTRYPOINT /app/entrypoint.sh
