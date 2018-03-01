# Usage
```
useradd -u 3003 -m komodod

docker run --rm --name komodod -ti \
    -v /home/komodod/.komodo:/home/komodod/.komodo \
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
# For asset chains (e.g. SUPERNET)
```
# start asset chain
docker run --rm --name SUPERNET -ti \
    -v /home/komodod/.komodo/SUPERNET:/home/komodod/.komodo/SUPERNET \
    -p 127.0.0.1:11340:11340 \
    -p 127.0.0.1:11341:11341 \
    kmdplatform/komodod \
    -bind=0.0.0.0 -rpcbind=0.0.0.0 -rpcallowip=0.0.0.0/0 \
    -ac_name=SUPERNET  -ac_supply=816061 -addnode=78.47.196.146 -gen

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
