#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
This file is part of Radar.

Radar is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Radar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
Lesser GNU General Public License for more details.

You should have received a copy of the Lesser GNU General Public License
along with Radar. If not, see <http://www.gnu.org/licenses/>.

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

    def _get_status(self, uptime_seconds):
        try:
            threshold_seconds = int(self._cli_options.seconds)
        except ValueError:
            raise UptimeError('Error - Number of seconds must be a positive value.')

        if threshold_seconds <= 0:
            raise UptimeError('Error - Number of seconds must be a positive value.')

        return 'SEVERE' if (0 < uptime_seconds <= threshold_seconds) else 'OK'

    def _get_details(self, seconds):
        d = datetime(1, 1, 1) + timedelta(seconds=seconds)
        return '{:} days {:} hours {:} minutes'.format(d.day - 1, d.hour, d.minute, d.second)

    def _get_uptime(self):
        return int(time.time() - boot_time())

    def check(self):
        output = {'status': 'ERROR'}

        try:
            uptime = self._get_uptime()
            output.update({
                'status': self._get_status(uptime),
                'details': self._get_details(uptime),
                'data': {
                    'uptime': uptime,
                    'name': self.PROGRAM_NAME
                },
            })
        except Exception, e:
            output['details'] = str(e)

        return serialize_json(output)


if __name__ == '__main__':
    print Uptime().check()
