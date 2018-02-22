#!/bin/sh
set -e


umask 007
#chown komodo:shared -R ${HOME}/.komodo/
#chmod 0750 ${HOME}/.komodo


# first arg is `-f` or `--some-option`
# or first arg is `something.conf`
if [ "${1#-}" != "$1" ] || [ "${1%.conf}" != "$1" ]; then
	set -- komodo_oneshot "$@"
fi

exec "$@"

