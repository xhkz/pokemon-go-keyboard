#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import getpass
import json
import os
import sys

from . import config


def parse_unicode(byte_str):
    return byte_str.decode(sys.getfilesystemencoding())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--auth-service', help='Auth Service', type=str.lower, default='ptc')
    parser.add_argument('-u', '--username', help='Username', required=True)
    parser.add_argument('-p', '--password', help='Password', required=False)
    parser.add_argument('-H', '--host', help='Web server host', default='127.0.0.1')
    parser.add_argument('-P', '--port', help='Web server port', type=int, default=5000)
    parser.add_argument('-d', '--debug', help='Debug Mode', action='store_true')
    parser.add_argument('-o', '--open', help='open browser', action='store_true', default=False)
    parser.set_defaults(DEBUG=False)
    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass()

    return args


def get_pokemon_name(pokemon_id):
    if not hasattr(get_pokemon_name, 'names'):
        file_path = os.path.join(config['ROOT_PATH'], config['LOCALES_DIR'], 'pokemon.{}.json'.format(config['LOCALE']))

        with open(file_path, 'r') as f:
            get_pokemon_name.names = json.loads(f.read())

    return get_pokemon_name.names.get(str(pokemon_id), 'unknown')
