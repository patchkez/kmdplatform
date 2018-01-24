# Usage

```
docker run -d --rm \
  -p 50001:50001 \
  -p 50002:50002 \
  -v /home/electrumx/data:/home/electrumx/data \
  -e DAEMON_URL=http://<user>:<password>@172.17.0.1:8332 \
  -e COIN=BitcoinSegwit \
  --name electrumx kmdplatform/electrumx
  ```
