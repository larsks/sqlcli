'''sqlcli -- a command line SQL query tool

## Usage

    sqlclient -u <url> <sql command>
    sqlclient -f inifile -i section/param <sql command>

## Options

- -u <url> -- a sqlalchemy database url, like
  mysql://user:password@host/database
- -f <inifile> -- path to an ini-format configuration file
- -i <section>/<param> -- specify a setting named <param> in section
  <section> of the ini file
- -p, --pretty -- display output in columns
- --fs, -F <fs> -- specify an output field separator
- -v, --verbose -- produce verbose output on stderr

## Examplles

Querying Neutron's "routers" table:

    # sqlcli -f /etc/neutron/plugin.ini -i DATABASE/sql_connection -p \
      'select name,id,status from routers'
    +-----------+--------------------------------------+--------+
    |    name   |                  id                  | status |
    +-----------+--------------------------------------+--------+
    | pubrouter | 934c3160-eefd-4cbc-995c-2d420d8f40a6 | ACTIVE |
    +-----------+--------------------------------------+--------+

Get a list of token ids and expirations from Keystone:

    # sqlcli -f /etc/keystone/keystone.conf -i sql/connection -p \
      'select id,expires from token'
    27271701dc8e430d9eee7b83ec1f3c8b,2013-11-25 21:32:07
    6a6ffeb6dcf54231b60604a736aef275,2013-11-25 21:32:10
    3db9c89063aa4c1694cbebf64d0b349a,2013-11-25 21:32:13
    c019c66c63534b7bb41d34a050642271,2013-11-25 21:32:16
    .
    .
    .

'''


