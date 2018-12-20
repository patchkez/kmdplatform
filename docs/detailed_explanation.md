# More in deep explanation how everything is interconnected
## Sensitive data
Sensitive data or data which are unique to every NN operator are put into `.env` file inside root of the repo.
This will lower chance to push sensitive data into public repository by mistake.

## Single host limitation
Iguana was developed for localhost communication with other services. E.g. it loads assetchains configuration from filesystem, it is hardcoded loopback IP addrress for communication with all assetchains. On production NN node, we run all containers in host mode (no virtual docker network is used).


## KMD and assetchains config files generation
komodod.conf file is created automatically on first startup. It contains rpc port, rpc username and rpc password. The problem here is that rpc password is randomly generated.
Because we want be in charge how komodod.conf and assetchains conf files are created, we create them manually. That way we can create known password which we use for communication between iguana and coin daemons.


## KMD container
We use same komodod image for assetchains and KMD coin.

Let's look at how this container is [started](https://github.com/patchkez/kmdplatform/blob/master/komodod/Dockerfile#L65).
First entrypoint.sh is executed and afterwards `start-komodod.sh`.
[entrypoint.sh](https://github.com/patchkez/kmdplatform/blob/master/komodod/entrypoint.sh) has if condition block which is executed only when asset variables are passed to container. This code of block is executed in assetchains containers. In this block we use [confd](https://github.com/kelseyhightower/confd) to create/templatize config files on container startup.
After initialization is done in entrypoint, start-komodod.sh is executed. Again we use if conditions to distinguish if we started komodod or assetchains.

## Assetchains
All KMD based assetchains are started from the same image as KMD container.
How each assetchain is started is defined in [Docker compose file for assets](https://github.com/patchkez/kmdplatform/blob/master/docker-compose-assets-production.yml).

### Ports
With every new coin added for notarization, this file must be updated manually. Here is some explanation of some entries in that file:
2 pairs of ports are exposed. The one bound to localhost is RPC port and the other bound to all addresses on host is p2p port.
For every new added coin, coin file must me [examined ](https://github.com/jl777/SuperNET/blob/dev/iguana/coins/zex_7776) and ports noted down.

### Volumes
There are 2 volumes mounted from host to containers:
- komodo-data
- shared-data

Shared data volume is not needed any more and will be removed. It was used in the past to share data between asset container and iguana container.

### Environment variables
These variables are passed into every container. These are picked by confd which does templatizing of assetchain config files.

### Asset commands
All komodod based assetchains are started by passing specific commands into container.

## Iguana container
We use similar approach here with confd for generating assetchain configuration files. We need to create exactly the same config files of assetchains, because these are read by iguana ([example](https://github.com/jl777/SuperNET/blob/dev/iguana/coins/zex_7776)).
[Emmanux](https://github.com/emmnx) tried to pass json config of coin directly to iguana without reading it from FS. I bundled [dokomodo](https://github.com/KomodoPlatform/komodotools/tree/master/dragonriders) tool into iguana image and it is started via [entrypoint](https://github.com/patchkez/kmdplatform/blob/master/iguana/docker/entrypoint.sh#L13) script. Dokomodo script fetches [this](https://github.com/KomodoPlatform/komodotools/blob/master/dragonriders/dokomodo/cli.py#L19) file which is preparesed content from [iguana coins](https://github.com/jl777/SuperNET/tree/dev/iguana/coins) directory. Then we have dokomodo config file where we tell what [coins to notarize](https://github.com/KomodoPlatform/komodotools/blob/master/dragonriders/dokomodo/yaml/config.ini#L53).
This file must be updated with every new added coin, also iguana container must be restarted do download new json with preparsed coins.

### m_notary_run and dpowassets execution
Initial idea was to keep iguana private key outside of NN server. Therefore ssh tunnel to NN is created with iguana port forwarded to my laptop. On laptop from cloned SuperNET repo I start m_notary_run and dpowassets scripts.

It is not ideal, but this is how this solution is deployed now.



