# TODO - info not accurate
Create user on host:
```
useradd -u 3012 -m gin
```
Run container:
```
docker run --rm --name gin -ti \
    -v /home/gin/.gincoin:/home/gin/.gincoin \
    -p 127.0.0.1:40001:40001 \
    -p 40002:40002 \
    kmdplatform/gind
```

Optionally if you want to override settings in config file:
```
docker run --rm --name gin -ti \
    -v /home/gin/.gincoin:/home/gin/.gincoin \
    -p 127.0.0.1:40001:40001 \
    -p 40002:40002 \
    -e GIN_BIND=0.0.0.0 \
    -e GIN_RPC_BIND=0.0.0.0 \
    -e GIN_RPC_ALLOWIP=0.0.0.0/0 \
    -e GIN_RPC_USER=ginrpcuser \
    -e GIN_RPC_PASSWORD=VerySecur3G4mEPassword \
    kmdplatform/gind
```
