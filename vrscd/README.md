# Usage
```
useradd -u 3009 -m veruscoin
```

Build image:
```
docker build --build-arg VRSC_BRANCH=beta . -t kmdplatform/vrscd
```

```
# For asset chains (e.g. SUPERNET)
To overwrite <ASSETCHAIN>.conf, 2 variables must be set: AC_NAME and AC_RPC_PORT:
```
# start asset chain
docker run --rm --name SUPERNET -ti \
    -v /home/komodo/.komodo/SUPERNET:/home/komodo/.komodo/SUPERNET \
    -p 127.0.0.1:11340:11340 \
    -p 127.0.0.1:11341:11341 \
    kmdplatform/komodod komodod -ac_name=SUPERNET -ac_supply=816061 -addnode=78.47.196.146 -gen \
    -e ASSET_NAME=SUPERNET \
    -e ASSET_RPC_PORT=11341 \
    -e ASSET_BTCPUBKEY=<pubkey>
```
# access asset chain via rpc
password='<get password from SUPERNET.conf>'
user='<get user from SUPERNET.conf>'
curl \
    --data-binary '{
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getinfo"
    }' \
    -H 'content-type: text/plain;' \
    http://$user:$password@127.0.0.1:11341/
```
