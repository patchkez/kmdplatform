#!/bin/bash


# Tempatize bitcoin and komodo configuration files
confd -confdir ~/confd -onetime -backend env


function templatize_acs {
  if [ "${1}" = "dev" -o "${1}" = "jl777" ];then
    BRANCH="development"
  else
    BRANCH="production"
  fi
 
  export LC_ALL=C.UTF-8
  export LANG=C.UTF-8
  source ~/komodotools-venv/bin/activate 
  cd ~/komodotools/dragonriders
  dokomodo generate_assetchains_conf -b ${BRANCH}
  cd -
}


# If DEBUG var is not empty, debugging is enabled
if [ -n "${DEBUG}" ]; then 
  DEBUG_PREFIX="gdb -args"
else
  DEBUG_PREFIX=""
fi

cd ~/SuperNET/iguana
# Are we running in TEST/DEV mode?
if [ "${IGUANA_BRANCH}" = "dev" -o "${IGUANA_BRANCH}" = "jl777" ];then
  templatize_acs ${IGUANA_BRANCH}
  # Download latest testnet file wiht btcpubkeys
  curl -o testnet https://raw.githubusercontent.com/KomodoPlatform/vote2018/master/testnet/testnet.json
  exec ${DEBUG_PREFIX} ~/SuperNET/agents/iguana testnet

else 
  templatize_acs ${IGUANA_BRANCH}
  exec ${DEBUG_PREFIX} ~/SuperNET/agents/iguana "${args[@]}"
fi

# exec "$@"
