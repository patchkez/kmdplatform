#!/bin/bash

VRSC_HOME="/home/veruscoin"

confd -confdir ${VRSC_HOME}/confd -onetime -backend env

exec "$@"
