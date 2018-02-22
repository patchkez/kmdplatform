# Dockerized Komodo Notary Node
## Host preparation
### Prerequisities
- docker
- docker-compose (can be started from container)

### Create users and groups on host:
```
groupadd -g 3001 bitcoin
groupadd -g 3003 komodo
groupadd -g 3004 iguana
groupadd -g 3005 shared
useradd -u 3001 -g bitcoin -G shared -m -d /home/bitcoin
useradd -u 3003 -g komodo -G shared -m -d /home/komodo
useradd -u 3004 -g iguana -G shared -m -d /home/iguana
```

### Modify .env file and point variables to place where data for each volume can be stored
- see .env.example how .env should look like
```
...
BITCOIN_DATA=/mnt/docker/bitcoin_data
KOMODO_DATA=/mnt/docker/komodo__data
IGUANA_DATA=/mnt/docker_/iguana_data
SHARED_DATA=/mnt/docker/shared_data
...
```

### Source .env file
``` 
source .env
```

### Create directories with proper permissions and ownership
```
mkdir ${BITCOIN_DATA} -m 0750 && chown bitcoin:shared ${BITCOIN_DATA}
mkdir ${KOMODO_DATA} -m 0750 && chown komodo:shared ${KOMODO_DATA}
mkdir ${IGUANA_DATA} -m 0750 && chown iguana:shared ${IGUANA_DATA}
mkdir ${SHARED_DATA} -m 0750 && chown iguana:shared ${SHARED_DATA}
```

### Prepare storage for docker layers/images - direct-lvm mode
https://docs.docker.com/storage/storagedriver/device-mapper-driver/

## First init - Start everything up
Docker images are built automatically by running `docker-compose run <service>`. You can build images manually by executing:
```
docker-compose build bitcoin
docker-compose build komodo
docker-compose build iguana
```

First startup of containers will create needed config files. Some files are stored on shared volumes, so other containers can access generated keys.
```
docker-compose run --rm bitcoin
docker-compose run --rm komodo
docker-compose run --rm iguana
```
or
```
docker-compose up #(not tested yet)
```

## Import of privkeys
Run these commands one by one.

We need to create iguana wallet. IGUANA_WALLET_PASSPHRASE variable inside .env file is used to pass passphrase into container.
### Create Iguana wallet
```
docker-compose run --rm iguana first_time_init
```

### Import the privkey of your BTCD address into Komodo
```
docker-compose run --rm komodo import_key
```

### Import BTC privkey into Bitcoin
```
docker-compose run --rm bitcoin import_key
```

Stop all containers now.

## Start everything with pubkey
All config files were generated and stored to corresponding volumes. Each container has entrypoint script which detects e.g. if pubkey file exists and starts daemon with different arguments.


```
docker-compose run --rm bitcoin
docker-compose run --rm komodo
docker-compose run --rm iguana
```
`docker-compose up` should also start all containers, but did not have time to test it.


TODO:
- monitoring of logs
- files on komodo volume are created with wrong permissions 

