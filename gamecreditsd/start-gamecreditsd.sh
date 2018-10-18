#!/bin/bash

# If BTC_PUBKEY variable is not empty string and no arguments were passed to container, start with pubkey
if [ -n "${BTC_PUBKEY}" -a $# -eq 0 ]; then
  exec gamecreditsd -pubkey="${BTC_PUBKEY}" \
    -addnode=18.196.233.17 \
    -addnode=18.197.49.217 \
    -addnode=18.197.63.122 \
    -addnode=13.81.80.199 \
    -addnode=13.81.97.125 \
    -addnode=13.81.99.236 \
    -addnode=74.208.211.94 \
    -addnode=54.36.51.177

# We do not have pubkey yet and no arguments passed to container
elif [ -z "${BTC_PUBKEY}" -a $# -eq 0 ]; then
  exec gamecreditsd

# Some arguments were passed
elif [ $# -ne 0 ]; then
  # Pass all commands which were passes as commands to container
  exec "$@"
fi
