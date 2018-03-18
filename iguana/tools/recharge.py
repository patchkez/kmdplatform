#!/usr/bin/env python3
import requests
import json
import sys
import os
import configparser


# define function that posts json data to daemon
def post_rpc(url, payload):
    try:
        r = requests.post(url, data=json.dumps(payload))
        return(json.loads(r.text))
    except Exception as e:
        print("Couldn't connect to " + url, e)
        sys.exit(0)


# define function that counts utxo's
def count_unspent(url, amount):
    # request list of utxo's
    listunspent_payload = {"method": "listunspent"}
    response_listunspent = post_rpc(url, listunspent_payload)

    # count how many
    counter = 0
    for i, val in enumerate(response_listunspent['result']):
        if val['amount'] == float(amount):
            counter += 1
    print("Filtered by utxo size: " + amount)
    print("Number of relevant utxo's: " + str(counter))
    return(counter)


# define function that splits funds
def splitfunds(coin, utxo_size, number_needed, url):
    satoshis = int(float(utxo_size) * 100000000)
    splitfunds_payload = {
        "coin": coin,
        "agent": "iguana",
        "method": "splitfunds",
        "satoshis": satoshis,
        "sendflag": 1,
        "duplicates": int(number_needed)
    }
    response_splitfunds = post_rpc(url, splitfunds_payload)
    try:
        txid = response_splitfunds['txid']
        print("Success! Transaction id: " + txid)
    except:
        print("Could not split funds: ")
        print(response_splitfunds)


# this script
def main():

    # read configuration file
    config = configparser.ConfigParser()
    path = os.path.dirname(sys.argv[0])
    path += '/recharge.ini'
    config.read(path)

    # iterate through list of coins
    for i, coin in enumerate(config):
        if coin == 'DEFAULT':
            continue
        print(coin)
        # define url of the daemon
        rpcuser = config[coin]['rpcuser']
        rpcpassword = config[coin]['rpcpassword']
        rpcip = config[coin]['rpcip']
        rpcport = config[coin]['rpcport']
        rpcurl = 'http://'
        rpcurl += rpcuser + ':' + rpcpassword + '@' + rpcip + ':' + rpcport
        # define utxo size to filter by
        utxo_size = config[coin]['utxo_size']
        # ask how many utxo's
        n_relevant_utxos = count_unspent(rpcurl, utxo_size)
        # define number of relevant utxo's threshold and target
        try:
            threshold = config[coin]['threshold']
            target = config[coin]['target']
        except:
            print("Threshold and/or target not found.\n")
            continue
        if int(threshold) > int(target):
            print(
                "Can't process this! " +
                "Target must be greater than threshold!\n")
            continue
        else:
            pass
        print("Threshold: " + threshold)
        # if necessary, generate more utxo's
        if int(n_relevant_utxos) <= int(threshold):
            print("Threshold reached! ")
            print("Target: " + target)
            # define iguana url
            try:
                iguana_ip = config[coin]['iguana_ip']
            except:
                iguana_ip = '127.0.0.1'
            try:
                iguana_port = config[coin]['iguana_port']
            except:
                iguana_port = '7776'
            iguana_url = 'http://' + iguana_ip + ':' + iguana_port
            # calulate how many utxo's needed to reach target
            n_utxos_needed = int(target) - int(n_relevant_utxos)
            # generate needed utxos
            splitfunds(coin, utxo_size, n_utxos_needed, iguana_url)
        print("")


if __name__ == '__main__':
    main()

