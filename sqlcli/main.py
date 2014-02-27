import os
import sys
import argparse
import logging

import iniparse
import prettytable
from sqlalchemy import create_engine
from sqlalchemy.exc import *

default_db_url   = os.environ.get('SQLCLI_URL')
default_ini_file = os.environ.get('SQLCLI_INI_FILE')
default_ini_item = os.environ.get('SQLCLI_INI_ITEM')


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--url', '-u',
                   default=default_db_url,
                   help='a database connection url')
    p.add_argument('--config', '-f',
                   default=default_ini_file,
                   help='path to an ini-style configuration file')
    p.add_argument('--item', '-i',
                   default=default_ini_item,
                   help='an item from the config file, specified as section/name')
    p.add_argument('-v', '--verbose',
                   action='store_true',
                   default=False,
                   help='enable verbose logging')
    p.add_argument('--pretty', '-p',
                   action='store_true',
                   default=False,
                   help='output pretty tables')
    p.add_argument('--fs', '-F',
                   default=',',
                   help='output field separator')
    p.add_argument('command', nargs='?')
    return p.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARN,
        format='%(asctime)s %(levelname)s: %(message)s',
        timefmt='%Y-%m-%d %T',
    )

    if not args.url and not (args.config and args.item):
        logging.error('you must provide either a url or an ini file '
                      'and section/param')
        sys.exit(1)

    if not args.url:
        with open(args.config) as fd:
            cfg = iniparse.INIConfig(fd)
            section, param = args.item.split('/')
            section = getattr(cfg, section, {})
            if param in section:
                args.url = section[param]

    if not args.url:
        logging.error('unable to determine database url')
        sys.exit(1)

    if not args.command:
        args.command = sys.stdin.read()

    logging.info('using url: %s' % args.url)

    engine = create_engine(args.url)
    logging.info('running command: %s' % args.command)

    try:
        res = engine.execute(args.command)
    except ProgrammingError as detail:
        logging.error('query failed: %s' % detail)
        sys.exit(1)

    if args.pretty:
        pt = prettytable.PrettyTable(
            res.keys if isinstance(res.keys, list)
            else res.keys())
        for row in res:
            pt.add_row(row)
        print pt
    else:
        for row in res:
            print args.fs.join(str(x) for x in row)

if __name__ == '__main__':
    main()

