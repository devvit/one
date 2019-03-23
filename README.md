### test

```
### for f in `docker images -q`; do docker image rm -f $f; done
### docker system prune -a
### docker run -p 127.0.0.1:8080:8080/tcp

### heroku container:login
### docker tag <imageregistry.heroku.com/<app>/<process-type>
### docker push registry.heroku.com/<app>/<process-type>
### heroku container:release web
```
