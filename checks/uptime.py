#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
This file is part of Radar-Checks.

Radar-Checks is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Radar-Checks is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
Lesser GNU General Public License for more details.

You should have received a copy of the Lesser GNU General Public License
along with Radar-Checks. If not, see <http://www.gnu.org/licenses/>.

Copyright 2015 Lucas Liendo.
"""


from json import dumps as serialize_json
from argparse import ArgumentParser
from datetime import datetime, timedelta
from psutil import time
from psutil import boot_time


class UptimeError(Exception):
    pass


class Uptime(object):

    PROGRAM_NAME = 'uptime'

    def __init__(self):
        self._cli_options = self._build_argument_parser().parse_args()

    def _build_argument_parser(self):
        parser = ArgumentParser(prog=self.PROGRAM_NAME)
        parser.add_argument(
            '-S', '--severe', dest='seconds', action='store', required=True,
            help='Number of seconds for which uptime is severe. E.g. : 300. If uptime is below 300 seconds a severe status is returned.'
        )

        return parser

    def _get_status(self, seconds):
        return 'SEVERE' if (0 < seconds <= int(self._cli_options.seconds)) else 'OK'

    def _get_details(self, seconds):
        d = datetime(1, 1, 1) + timedelta(seconds=seconds)
        return '{:} days {:} hours {:} minutes.'.format(d.day - 1, d.hour, d.minute, d.second)

    def _get_uptime(self):
        return int(time.time() - boot_time())

    def check(self):
        uptime = self._get_uptime()
        output = {
            'status': self._get_status(uptime),
            'details': self._get_details(uptime),
            'data': {'uptime': uptime, 'name': self.PROGRAM_NAME},
        }

        return serialize_json(output)


if __name__ == '__main__':
    print Uptime().check()
