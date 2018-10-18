#!/bin/bash

# If BTC_PUBKEY variable is not empty string and no arguments were passed to container, start with pubkey
if [ -n "${BTC_PUBKEY}" -a $# -eq 0 ]; then
  exec chipsd -pubkey="${BTC_PUBKEY}" \
  -connect=192.99.20.33 \
  -connect=145.239.204.33 \
  -connect=167.99.69.47 \
  -connect=139.99.148.62 \
  -connect=149.56.28.84 \
  -connect=213.32.7.136 \
  -connect=149.56.29.163 \
  -connect=164.132.202.176 \
  -connect=37.9.62.186 \
  -connect=78.47.196.146 \

# We do not have pubkey yet and no arguments passed to container
elif [ -z "${BTC_PUBKEY}" -a $# -eq 0 ]; then
  exec chipsd

# Some arguments were passed
elif [ $# -ne 0 ]; then
  # Pass all commands which were passes as commands to container
  exec "$@"
fi
