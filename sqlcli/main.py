import os
import sys
import argparse
import logging

import iniparse
from ConfigParser import NoOptionError
import prettytable
from sqlalchemy import create_engine
from sqlalchemy.exc import *

LOG = logging.getLogger('sqlcli')

default_db_url   = os.environ.get('SQLCLI_URL')
default_ini_file = os.environ.get('SQLCLI_INI_FILE')
default_ini_item = os.environ.get('SQLCLI_INI_ITEM')


class sqlcliError(Exception):
    pass


class DeprecatedOption(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        raise sqlcliError('Option %s is no longer available' % (
                          option_string))


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('--url', '-u',
                   default=default_db_url,
                   help='a database connection url')
    p.add_argument('--config', '-f',
                   nargs=3,
                   metavar=('PATH', 'SECTION', 'OPTION'),
                   default=default_ini_file,
                   help='path, section, and option for an ini-style configuration file')
    p.add_argument('-v', '--verbose',
                   action='store_const',
                   const='INFO',
                   dest='loglevel',
                   default=False,
                   help='enable verbose logging')
    p.add_argument('--pretty', '-p',
                   action='store_true',
                   default=False,
                   help='output pretty tables')
    p.add_argument('--fs', '-F',
                   default=',',
                   help='output field separator')
    p.add_argument('--item', '-i',
                   action=DeprecatedOption,
                   help=argparse.SUPPRESS)
    p.add_argument('command', nargs='?')

    p.set_defaults(loglevel='WARN')

    return p.parse_args()


def get_database_url():
    if not args.url and not args.config:
        raise sqlcliError('you must provide either a url with --url '
                          'or an ini-format configuration file with '
                          '--config.')

    if args.url:
        url = args.url
    else:
        inipath, section, option = args.config
        try:
            with open(inipath) as fd:
                cfg = iniparse.ConfigParser()
                cfg.readfp(fd)
                url = cfg.get(section, option)
        except NoOptionError as err:
            raise sqlcliError('failed to retrieve database connection '
                              'from %s: %s' % (inipath, err))
        except IOError as err:
            raise sqlcliError('failed to open %s: %s' % (inipath, err))

    return url


def get_sql_command():
    if not args.command:
        LOG.warn('reading sql script from stdin')
        command = sys.stdin.read()
    else:
        command = args.command

    return command


def run_sql_command(engine, command):
    try:
        res = engine.execute(command)
    except ProgrammingError as err:
        raise sqlcliError('sql command failed: %s' % err)

    return res


def print_pretty_results(results):
        pt = prettytable.PrettyTable(
            results.keys if isinstance(results.keys, list)
            else results.keys())
        for row in results:
            pt.add_row(row)
        print pt


def print_csv_results(results):
    print '\n'.join(
        args.fs.join(str(col) for col in row) for row in results)


def print_results(results):
    if results.closed:
        LOG.warn('Command completed but returned no results.')
        return

    if args.pretty:
        print_pretty_results(results)
    else:
        print_csv_results(results)


def main():
    global args

    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %T',
    )

    args = parse_args()
    logging.getLogger().setLevel(args.loglevel)

    url = get_database_url()
    if not url:
        raise sqlcliError('unable to determine database url')
    LOG.info('using url: %s' % url)

    command = get_sql_command()
    LOG.info('running command: %s' % command)

    engine = create_engine(url)
    results = run_sql_command(engine, command)
    print_results(results)

    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except sqlcliError as err:
        LOG.error('%s', err)
        sys.exit(1)
