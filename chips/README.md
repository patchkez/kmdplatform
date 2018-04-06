Create user on host:
```
useradd -u 3007 -m chips
```
Run container:
```
docker run --rm --name chips -ti \
    -v /home/chips/.chips:/home/chips/.chips \
    -p 127.0.0.1:57776:57776 \
    -p 127.0.0.1:57777:57777 \
    kmdplatform/chips
```

Optionally if you want to override settings in config file:
```
docker run --rm --name chips -ti \
    -v /home/chips/.chips:/home/chips/.chips \
    -p 127.0.0.1:57776:57776 \
    -p 127.0.0.1:57777:57777 \
    -e CHIPS_BIND=0.0.0.0 \
    -e CHIPS_RPC_BIND=0.0.0.0 \
    -e CHIPS_RPC_ALLOWIP=rpcallowip=0.0.0.0/0 \
    -e CHIPS_RPC_USER=chipsrpcuser \
    -e CHIPS_RPC_PASSWORD=VerySecur3RPCCH1psPassword \
    kmdplatform/chips
```
