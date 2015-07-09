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


from platform import system as platform_name
from json import dumps as serialize_json
from argparse import ArgumentParser
from datetime import datetime, timedelta


class UptimeError(Exception):
    pass


class Uptime(object):

    PROGRAM_NAME = 'uptime'
    PROGRAM_VERSION = '0.0.1'

    def __init__(self):
        self.available_platforms = {
            'Linux': self._linux_uptime,
            'Windows': self._windows_uptime,
        }

        self._cli_options = self._build_argument_parser().parse_args()

    def _build_argument_parser(self):
        parser = ArgumentParser(prog=self.PROGRAM_NAME)
        parser.add_argument(
            '-s', '--seconds', dest='seconds', action='store', required=True,
            help='Number of seconds for which uptime is severe. E.g. : 300. If uptime is below 300 seconds then severe status is returned.'
        )
        parser.add_argument('-v', '--version', action='version', version=self.PROGRAM_VERSION)

        return parser

    def _linux_uptime(self):
        try:
            with open('/proc/uptime') as fd:
                uptime, _ = fd.readline().split()
        except IOError, e:
            raise UptimeError('Error - Couldn\'t open \'/proc/uptime\'. Details : {:}'.format(e))

        return float(uptime)

    def _windows_uptime(self):
        try:
            from win32api import GetTickCount
        except ImportError:
            raise UptimeError('Error - Couldn\'t import win32api.')

        return GetTickCount() / 1000.0

    def _get_current_status(self, seconds):
        return 'SEVERE' if (0 < seconds <= int(self._cli_options.seconds)) else 'OK'

    def _get_detailed_output(self, seconds):
        d = datetime(1, 1, 1) + timedelta(seconds=seconds)
        return '{:} days {:} hours {:} minutes.'.format(d.day - 1, d.hour, d.minute, d.second)

    def get(self):
        output = {'status': 'ERROR'}
        platform = platform_name()

        try:
            seconds = int(self.available_platforms[platform]())
            output.update({
                'status': self._get_current_status(seconds),
                'details': self._get_detailed_output(seconds),
                'data': {
                    'name': self.PROGRAM_NAME,
                    'uptime': seconds,
                },
            })
        except UptimeError, e:
            output.update({'details': str(e)})
        except ValueError:
            output.update({'details': 'Error - uptime\'s \'-s\' argument must be a valid interger value.'})
        except KeyError:
            output.update({'details': '{:} platform is not supported.'.format(platform)})

        return serialize_json(output)


if __name__ == '__main__':
    print Uptime().get()
