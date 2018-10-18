#!/bin/bash

# If BTC_PUBKEY variable is not empty string and no arguments were passed to container, start mining with pubkey
if [ -n "${BTC_PUBKEY}" -a $# -eq 0 ]; then
  exec hushd -pubkey="${BTC_PUBKEY}"

# We do not have pubkey yeti and no arguments passed to container
elif [ -z "${BTC_PUBKEY}" -a $# -eq 0 ]; then
  exec hushd

# Some arguments were passed
elif [ $# -ne 0 ]; then
  # Pass all commands which were passes as commands to container
  exec "$@"
fi
