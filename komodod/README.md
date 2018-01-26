# Usage
```
docker run --rm --name komodod -ti \
  -p 127.0.0.1:7770:7770 \
  -p 127.0.0.1:7771:7771 \
  kmdplatform/komodod \
  -server=1 \
  -rpcuser=<user> \
  -rpcpasswd=<password> \
  -txindex=1 \
  -bind=0.0.0.0 \
  -rpcbind=0.0.0.0 \
  -rpcallowip=0.0.0.0/0
```
