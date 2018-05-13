Create user on host:
```
useradd -u 3008 -m gamecredits
```
Run container:
```
docker run --rm --name gamecredits -ti \
    -v /home/gamecredits/.gamecredits:/home/gamecredits/.gamecredits \
    -p 127.0.0.1:40001:40001 \
    -p 40002:40002 \
    kmdplatform/gamecreditsd
```

Optionally if you want to override settings in config file:
```
docker run --rm --name gamecredits -ti \
    -v /home/gamecredits/.gamecredits:/home/gamecredits/.gamecredits \
    -p 127.0.0.1:40001:40001 \
    -p 40002:40002 \
    -e GAME_BIND=0.0.0.0 \
    -e GAME_RPC_BIND=0.0.0.0 \
    -e GAME_RPC_ALLOWIP=0.0.0.0/0 \
    -e GAME_RPC_USER=gamerpcuser \
    -e GAME_RPC_PASSWORD=VerySecur3G4mEPassword \
    kmdplatform/gamecreditsd
```
