#!/bin/bash

confd -onetime -backend env

exec "$@"
