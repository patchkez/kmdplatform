#!/bin/bash

# if no arguments were passed, start bitcoind
if [ $# -eq 0 ]; then
  exec bitcoind

# Some arguments were passed
elif [ $# -ne 0 ]; then
  # Pass all commands which were passes as commands to container
  exec "$@"
fi
