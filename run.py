#! /usr/bin/env python
import logging
import os

from pgomap import config
from pgomap.app import Pgomap
from pgomap.models import create_tables
from pgomap.utils import parse_args

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(module)11s] [%(levelname)7s] %(message)s')


def main():
    args = parse_args()
    create_tables()

    if args.username and args.password:
        config['USERNAME'] = args.username
        config['PASSWORD'] = args.password

    if args.open:
        os.system('open "http://localhost:5000"')

    if args.debug:
        logging.getLogger("requests").setLevel(logging.DEBUG)
        logging.getLogger("pgoapi").setLevel(logging.DEBUG)
        logging.getLogger("rpc_api").setLevel(logging.DEBUG)

    app = Pgomap(__name__)
    app.run(threaded=True, debug=args.debug, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
