#!/bin/sh
set -e


umask 007
#chown komodo:shared -R ${HOME}/.komodo/
#chmod 0750 ${HOME}/.komodo

echo 'if [ -f /home/komodo/.shared/pubkey.txt ]; then export $(cat /home/komodo/.shared/pubkey.txt); fi' >> ~/.bashrc

export $(cat /home/komodo/.shared/pubkey.txt)

# first arg is `-f` or `--some-option`
# or first arg is `something.conf`
if [ "${1#-}" != "$1" ] || [ "${1%.conf}" != "$1" ]; then
	set -- komodo_oneshot "$@"
fi

exec "$@"

