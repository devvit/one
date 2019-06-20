FROM python:3.6-alpine

# ENV http_proxy 'http://192.168.56.1:8123'
# ENV https_proxy 'http://192.168.56.1:8123'

RUN apk add --no-cache \
  bash \
  unzip \
  curl \
  htop \
  && apk add --no-cache --virtual .build-deps build-base linux-headers musl-dev

COPY . /app
RUN chmod 777 /app
WORKDIR /app

RUN pip3 install --no-cache-dir -U -r /app/requirements.txt

RUN apk del .build-deps

RUN adduser -D tomcat
USER tomcat
EXPOSE 8080
ENTRYPOINT /app/entrypoint.sh
