#!/usr/bin/env python3
from jinja2 import Environment, FileSystemLoader
from ruamel.yaml import YAML
import requests
import socket
import shlex
import subprocess
import time
import argparse
# import random
# import sys

yaml = YAML(typ='safe', pure=True)
yaml.default_flow_style = True
# yaml.preserve_quotes = True

# Load data from YAML into Python dictionary
# config_data = yaml.load(open('./yaml/data.yaml'))

asset_data_url = ("https://raw.githubusercontent.com/patchkez/kmdplatform/"
    "first_improvement/yaml/data.yaml")

r = requests.get(asset_data_url)
config_data = yaml.load(r.text)

# Load Jinja2 template
env = Environment(loader=FileSystemLoader('./templates/'), trim_blocks=True, lstrip_blocks=True)


def seed_ip():
    return socket.gethostbyname(config_data['seed_host'])


# def random_gen():
#     random_int = random.randint(0, 32767)
#     # print('random is:', random_int)
#     if random_int % 10 == 1:
#         gen_param = "-gen"
#     else:
#         gen_param = ""
#     return gen_param
#
#
# def komodod_command(assetname, asset_amount):
#     return "komodod -pubkey=$PUBKEY -ac_name=" + assetname + " " + "-ac_supply=" + \
#         asset_amount + " " + "-addnode=" + seed_ip() + " " + random_gen()
#     return


def generate_docker_compose():
    template = env.get_template('docker-compose-template.conf.j2')
    templatized_config = template.render(items=config_data['assetchains'], seed_ip=seed_ip())

    fo = open('docker-compose_assets.yml', 'w')
    fo.write(templatized_config)
    fo.close()


def run_assetchains():
    bash_template = env.get_template('assetchains.j2')
    bash_templatized_config = bash_template.render(items=config_data['assetchains'],
        seed_ip=seed_ip())

    fa = open('assetchains', 'w')
    fa.write(bash_templatized_config)
    fa.close()

    for assetchain_command in bash_templatized_config.split("\n"):
        args = shlex.split(assetchain_command)
        print("Line", args)
        p = subprocess.Popen(args)
        time.sleep(20)

# print('Writing config...')
# with open("docker-compose_assets.yml", 'w') as newconf:
#    yaml.dump(templatized_config, newconf)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--assetchains",
                        help="Run assetchains", action="store_true")
    parser.add_argument("-g", "--generate",
                        help="Generate docker-compose.yml for assetchains", action="store_true")
    args = parser.parse_args()
    if args.assetchains:
        print("Executing assetchains:")
        run_assetchains()
    elif args.generate:
        print("Creating new docker compose file for assetchains:")
        generate_docker_compose()
    else:
        wrong_arg_msg = "Unknown option!"
        print(wrong_arg_msg)


if __name__ == "__main__":
    main()
