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


from math import floor
from platform import system as platform_name
from json import dumps as serialize_json
from argparse import ArgumentParser


class DiskUsageError(Exception):
    pass


class DiskUsage(object):

    PROGRAM_NAME = 'disk-usage'
    PROGRAM_VERSION = '0.0.1'

    def __init__(self):
        self.available_platforms = {
            'Linux': self._linux_disk_usage,
            'Windows': self._windows_disk_usage,
        }

        self.units = {
            'bytes': 1,
            'kib': 1024,
            'mib': 1024 ** 2,
            'gib': 1024 ** 3,
            'per': 1,
        }

        self._cli_options = self._build_argument_parser().parse_args()

    def _build_argument_parser(self):
        parser = ArgumentParser(prog=self.PROGRAM_NAME)
        parser.add_argument(
            '-u', '--units', dest='units', action='store', default='mib',
            help='Valid units are : kib, mib, gib or per. Default is mib.'
        )
        parser.add_argument(
            '-p', '--partition', dest='partition', action='store', required=True,
            help='The partition to check.'
        )
        parser.add_argument(
            '-O', '--ok', dest='ok_threshold', action='store', required=True,
            help='Ok status range. E.g : (0,1500]. Don\'t include brackets !'
        )
        parser.add_argument(
            '-W', '--warning', dest='warning_threshold', action='store', required=True,
            help='Warning status range. E.g : (1500,1700]. Don\'t include brackets !'
        )
        parser.add_argument('-v', '--version', action='version', version=self.PROGRAM_VERSION)

        return parser

    def _linux_disk_usage(self):
        try:
            from os import statvfs
        except ImportError:
            raise DiskUsageError('Error - Couldn\'t import statvfs.')

        stats = statvfs(self._cli_options.partition)
        total = stats.f_blocks * stats.f_bsize
        free = stats.f_bavail * stats.f_bsize

        return {
            'in use': total - free,
            'free': free,
            'total': total,
        }

    def _windows_disk_usage(self):
        try:
            from win32api import GetDiskFreeSpaceEx
        except ImportError:
            raise DiskUsageError('Error - Couldn\'t import win32api.')

        _, total, free = GetDiskFreeSpaceEx()

        return {
            'in use': total - free,
            'free': free,
            'total': total,
        }

    # TODO: Implement percentage units !
    def _get_thresholds(self):
        try:
            units = self.units[self._cli_options.units]
            min_ok, max_ok, min_warning, max_warning = [
                float(t) * units for t in self._cli_options.ok_threshold.split(',') + self._cli_options.warning_threshold.split(',')
            ]
        except ValueError:
            raise DiskUsageError('')
        except KeyError:
            raise DiskUsageError('Error - Wrong \'{:}\' units parameter.')

        return {
            'min ok': min_ok,
            'max ok': max_ok,
            'min warning': min_warning,
            'max warning': max_warning,
        }

    def _get_current_status(self, stats):
        status = 'SEVERE'
        thresholds = self._get_thresholds()

        if thresholds['min ok'] < stats['in use'] <= thresholds['max ok']:
            status = 'OK'
        elif thresholds['min warning'] < stats['in use'] <= thresholds['max warning']:
            status = 'WARNING'

        return status

    def _get_detailed_output(self, stats):
        return 'Total : {:.2f}, in use : {:.2f}, free : {:.2f}.'.format(
            *[stats[k] / float(self.units[self._cli_options.units]) for k in ['total', 'in use', 'free']]
        )

    def get(self):
        output = {'status': 'ERROR'}
        platform = platform_name()

        try:
            stats = self.available_platforms[platform]()
            output.update({
                'status': self._get_current_status(stats),
                'details': self._get_detailed_output(stats),
                'data': {
                    'name': self.PROGRAM_NAME,
                    'in use': stats['in use'],
                    'free': stats['free'],
                    'total': stats['total'],
                },
            })
        except DiskUsageError, e:
            output.update({'details': str(e)})
        except KeyError:
            output.update({'details': '{:} platform is not supported.'.format(platform)})

        return serialize_json(output)


if __name__ == '__main__':
    print DiskUsage().get()
