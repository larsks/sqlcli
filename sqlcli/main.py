#!/usr/bin/python
#
# usage: sqlclient -u <url> <sql command>
#        sqliclient -f inifile -i section/param <sql command>

import os
import sys
import argparse
import logging

import iniparse
import prettytable
from sqlalchemy import create_engine
from sqlalchemy.exc import *

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--url', '-u')
    p.add_argument('--config', '-f')
    p.add_argument('--item', '-i')
    p.add_argument('-v', '--verbose', 
            action='store_true', default=False)
    p.add_argument('--pretty', '-p',
            action='store_true', default=False)
    p.add_argument('--fs', default=',')
    p.add_argument('command', nargs='+')
    return p.parse_args()

def main():
    args = parse_args()
    logging.basicConfig(
            level=logging.INFO if args.verbose else logging.WARN,
            format='%(asctime)s %(levelname)s: %(message)s',
            timefmt='%Y-%m-%d %T',
            )

    if not args.url and not (args.config and args.item):
        logging.error('you must provide either a url or an ini file ' \
                'and section/param')
        sys.exit(1)

    if not args.url:
        with open(args.config) as fd:
            cfg = iniparse.INIConfig(fd)
            section, param = args.item.split('/')
            if section in cfg and param in cfg[section]:
                args.url = cfg[section][param]

    if not args.url:
        logging.error('unable to determine database url')
        sys.exit(1)

    logging.info('using url: %s' % args.url)

    engine = create_engine(args.url)
    cmd = ' '.join(args.command)
    logging.info('running command: %s' % cmd)

    try:
        res = engine.execute(cmd)
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

