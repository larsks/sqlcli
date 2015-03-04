This is tool that uses [SQLAlchemy][] to execute SQL queries against a
database specified via a URL or an INI-style configuration file.   For
example, if you have a configuration file that looks like this:

    [database]
    connection = mysql://quantum:secret@192.168.122.179/ovs_quantum

Then you can run a query like this:

    $ sqlcli -f /path/to/config.ini database connection \
      'select name,cidr from subnets'

And get output like this:

    public,172.24.4.224/28
    net0-subnet0,10.0.0.0/24

Or you can add the `--pretty` flag and get output like this:

    +--------------+-----------------+
    |     name     |       cidr      |
    +--------------+-----------------+
    |    public    | 172.24.4.224/28 |
    | net0-subnet0 |   10.0.0.0/24   |
    +--------------+-----------------+

If you don't specify a SQL command on the command line, `sqlcli` will
read a command from `stdin`.

Options
=======

- `--url`, `-u` *url* -- specify the database url on the command line.

    Defaults to the value of the `SQLCLI_URL` environment variable.

- `--config`, `-f` *path* *section* *option* -- get the database url
  from option *option* in section *section* of *path*, an INI-style
  configuration file.

- `--verbose`,`-v` -- enable verbose logging
- `--fs`, `-F` -- specify an output field separator.

  Defaults to `,`.

- `--pretty`, `-p` -- generate formatted table output

[sqlalchemy]: http://www.sqlalchemy.org/

License
=======

sqlcli -- a command line sql query tool
Copyright (C) 2013-2015 Lars Kellogg-Stedman <lars@oddbit.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

