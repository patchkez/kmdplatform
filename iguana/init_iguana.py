#!/usr/bin/env python3
import requests
import json
import pprint
import sys
import os


# config area
iguana_ip = '172.18.0.2'
iguana_port = '7776'

bitcoind_ip = '172.18.0.3'
bitcoind_port = '8332'
bitcoind_rpcuser = 'bitcoin-notary-rpc'
bitcoind_rpcpassword = 'conejo-coelho-rabbit'

komodod_ip = '127.0.0.1'
komodod_port = '7771'
komodod_rpcuser = 'komodo-notary-rpc'
komodod_rpcpassword = 'conejo-coelho-rabbit'
# end of config area


# define url's
iguana_url = 'http://' + iguana_ip + ':' + iguana_port
bitcoind_url = (
    'http://' +
    bitcoind_rpcuser + ':' +
    bitcoind_rpcpassword + '@' +
    bitcoind_ip + ':' +
    bitcoind_port)
komodod_url = (
    'http://' +
    komodod_rpcuser + ':' +
    komodod_rpcpassword + '@' +
    komodod_ip + ':' +
    komodod_port)

# read passphrase from environment variable
try:
    passphrase = sys.argv[1]
except:
    print(
        "Error: no passphrase given.\n" +
        "Usage (include the spaces at the beginning, and " +
        "quotes enclosing the passphrase):\n" +
        "  " + sys.argv[0] + " 'this is my secret passphrase'\n")
    sys.exit(0)

# configure pretty printer
pp = pprint.PrettyPrinter(width=41, compact=True)


# define function that posts json data to iguana
def post_rpc(url, payload):
    try:
        r = requests.post(url, data=json.dumps(payload))
        return(json.loads(r.text))
    except Exception as e:
        print("Couldn't connect to " + url, e)
        sys.exit(0)


# addcoin method, iguana

addcoin_BTCD = {
    "poll": 100,
    "active": 1,
    "agent": "iguana",
    "method": "addcoin",
    "newcoin": "BTCD",
    "startpend": 1,
    "endpend": 1,
    "services": 128,
    "maxpeers": 16,
    "RELAY": 0,
    "VALIDATE": 0,
    "portp2p": 14631,
    "rpc": 14632
}
response_addcoin_BTCD = post_rpc(iguana_url, addcoin_BTCD)
print('== response_addcoin_BTCD ==')
pp.pprint(response_addcoin_BTCD)

addcoin_BTC = {
    "prefetchlag": 5,
    "poll": 100,
    "active": 1,
    "agent": "iguana",
    "method": "addcoin",
    "newcoin": "BTC",
    "startpend": 1,
    "endpend": 1,
    "services": 128,
    "maxpeers": 16,
    "RELAY": 0,
    "VALIDATE": 0,
    "portp2p": 8333
}
response_addcoin_BTC = post_rpc(iguana_url, addcoin_BTC)
print('== response_addcoin_BTC ==')
pp.pprint(response_addcoin_BTC)


# The encryptwallet RPC encrypts the wallet with a passphrase.
# This is only to enable encryption for the first time.
# After encryption is enabled, you will need to enter the passphrase to use
# private keys.

encryptwallet = {
    "agent": "bitcoinrpc",
    "method": "encryptwallet",
    "passphrase": passphrase
}
response_encryptwallet = post_rpc(iguana_url, encryptwallet)

try:
    # store BTCDwif
    BTCDwif = response_encryptwallet['BTCDwif']
    BTCD = response_encryptwallet['BTCD']
    print('== response_encryptwallet: BTCDwif successfully obtained. ==')
except:
    print("** Error: Could not obtain BTCDwif. **")
    print(response_encryptwallet['error'])
    e = sys.exc_info()[0]
    print(e)
    sys.exit(0)

try:
    # store BTCwif
    BTCwif = response_encryptwallet['BTCwif']
    BTC = response_encryptwallet['BTC']
    print('== response_encryptwallet: BTCwif successfully obtained. ==')
except:
    print("** Error: Could not obtain BTCwif. **")
    print(response_encryptwallet['error'])
    e = sys.exc_info()[0]
    print(e)
    sys.exit(0)


# The walletpassphrase RPC stores the wallet decryption key in memory for the
# indicated number of seconds. Issuing the walletpassphrase command while the
# wallet is already unlocked will set a new unlock time that overrides
# the old one.

walletpassphrase = {
    "method": "walletpassphrase",
    "params": [
        passphrase,
        9999999
    ]
}
response_walletpassphrase = post_rpc(iguana_url, walletpassphrase)

# store btcpubkey
btcpubkey = response_walletpassphrase['btcpubkey']

print('== response_walletpassphrase ==')
pp.pprint(response_walletpassphrase)


# Requires wallet support. Wallet must be unlocked.The importprivkey RPC adds
# a private key to your wallet. The key should be formatted in the wallet
# import format created by the dumpprivkey RPC.
# The private key to import into the wallet encoded in base58check using
# wallet import format (WIF).

btc_importprivkey = {
    "agent": "bitcoinrpc",
    "method": "importprivkey",
    "params": [BTCwif, "", False]
}
response_btc_importprivkey = post_rpc(bitcoind_url, btc_importprivkey)
print('== response_btc_importprivkey ==')
pp.pprint(response_btc_importprivkey)


# Requires wallet support. Wallet must be unlocked.The importprivkey RPC adds
# a private key to your wallet. The key should be formatted in the wallet
# import format created by the dumpprivkey RPC.
# The private key to import into the wallet encoded in base58check using
# wallet import format (WIF).

btcd_importprivkey = {
    "agent": "bitcoinrpc",
    "method": "importprivkey",
    "params": [BTCDwif, "", False]
}
response_btcd_importprivkey = post_rpc(komodod_url, btcd_importprivkey)
print('== response_btcd_importprivkey ==')
pp.pprint(response_btcd_importprivkey)


# The validateaddress RPC accepts a block, verifies it is a valid
# addition to the block chain, and broadcasts it to the network.

btc_validateaddress = {
    "method": "validateaddress",
    "params": [BTC]
}
response_btc_validateaddress = post_rpc(bitcoind_url, btc_validateaddress)
print('== response_btc_validateaddress ==')
pp.pprint(response_btc_validateaddress)

btcd_validateaddress = {
    "method": "validateaddress",
    "params": [BTCD]
}
response_btcd_validateaddress = post_rpc(komodod_url, btcd_validateaddress)
print('== response_btcd_validateaddress ==')
pp.pprint(response_btcd_validateaddress)
