#!/bin/bash

# Tempatize bitcoin and komodo configuration files
confd -confdir ~/confd -onetime -backend env


function templatize_acs {

  export LC_ALL=C.UTF-8
  export LANG=C.UTF-8
  source ~/komodotools-venv/bin/activate
  cd ~/komodotools/dragonriders
  dokomodo generate_assetchains_conf -b ${1}
  cd -
}


# If DEBUG var is not empty, debugging is enabled
if [ -n "${DEBUG}" ]; then
  DEBUG_PREFIX="gdb -args"
else
  DEBUG_PREFIX=""
fi

cd ~/SuperNET/iguana

# Check if IGUANA_MODE was passed as env variable
if [ -z ${IGUANA_MODE} ];then
  echo "IGUANA_MODE variable not set!!! Set it to 'production' or 'development'"
  exit 1
fi

# Are we running in TEST/DEV mode?
if [ "${IGUANA_MODE}" = "production" ];then
  MODE="notary"
elif [ "${IGUANA_MODE}" = "development" ];then
  MODE="testnet"
  curl -o testnet https://raw.githubusercontent.com/KomodoPlatform/vote2018/master/testnet/testnet.json
else 
  echo "Unknown branch variable passed..."
fi


templatize_acs ${IGUANA_MODE}
exec ${DEBUG_PREFIX} ~/SuperNET/agents/iguana ${MODE}
