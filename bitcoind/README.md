# Usage
Create user on host:
```
useradd -u 3001 -m bitcoin
```

Run container:
```
docker run -d --rm \
    -p 127.0.0.1:8333:8333 \
    -p 127.0.0.1:8332:8332 \
    --mount 'src=BTC_VOL,dst=/home/bitcoin' \
    --name BTC \
    kmdplatform/bitcoind
```
Optionally if you want to override settings in config file:
```
docker run -d --rm --name bitcoin -ti \
    --mount 'src=BTC_VOL,dst=/home/bitcoin' \
    -p 127.0.0.1:8332:8332 \
    -p 127.0.0.1:8333:8333 \
    -e BITCOIN_BIND=0.0.0.0 \
    -e BITCOIN_RPC_BIND=0.0.0.0 \
    -e BITCOIN_RPC_ALLOWIP=0.0.0.0/0 \
    -e BITCOIN_RPC_USER=bitcoinrpcuser123 \
    -e BITCOIN_RPC_PASSWORD=VerySecur3RPCBTCPassword \
    kmdplatform/bitcoind
```
