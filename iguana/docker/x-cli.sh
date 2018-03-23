#!/bin/bash
# Maintainer: Emmanux

# Usage:
# You need to set environmental variable
# DOCKERMODE=1
# in order to resolve rpc address to same name as coin symbol.
# Example: for coin "SUPERNET", domain name "SUPERNET" will be used, instead
# of "127.0.0.1".

case $0 in
  *bitcoin-cli)
    CURRENCY=BTC
    source ~/.bitcoin/bitcoin.conf
    : ${rpcport=8332}
  ;;
  *komodo-cli)
    CURRENCY=KMD
    source ~/.komodo/komodo.conf
    case $1 in
      -ac_name=*)
      CURRENCY="${1#*=}"
      source ~/.komodo/$CURRENCY/$CURRENCY.conf
      shift
      ;;
    esac
    : ${rpcport=7771}
  ;;
esac

METHOD=$1
shift

if [[ $DOCKERMODE == "1" ]] ; then
  rpcaddress=$CURRENCY
else
  rpcaddress=127.0.0.1
fi

if [[ $1 ]] ; then
  params=$(printf ', "%s"' "${@}");
  params=${params:2};
fi

data=$(printf '{"method": "%s", "params": [%s]}' $METHOD "$params")

curl -s --url  $rpcuser:$rpcpassword@$rpcaddress:$rpcport --data "$data"

exit

