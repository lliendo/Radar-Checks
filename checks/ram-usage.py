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


from math import floor
from platform import system as platform_name
from json import dumps as serialize_json
from argparse import ArgumentParser


class RamUsageError(Exception):
    pass


class RamUsage(object):

    PROGRAM_NAME = 'ram-usage'
    PROGRAM_VERSION = '0.0.1'

    def __init__(self):
        self.available_platforms = {
            'Linux': self._linux_ram_usage,
            'Windows': self._windows_ram_usage,
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
            '-O', '--ok', dest='ok_threshold', action='store', required=True,
            help='Ok status range. E.g : (0,1500]. Don\'t include brackets.'
        )
        parser.add_argument(
            '-W', '--warning', dest='warning_threshold', action='store', required=True,
            help='Warning status range. E.g : (1500,1700]. Don\'t include brackets.'
        )
        parser.add_argument('-v', '--version', action='version', version=self.PROGRAM_VERSION)

        return parser

    def _linux_ram_usage(self):
        def _process_meminfo_line(line):
            units = {'kB': 1024, 'none': 1}

            try:
                k, v, u = line.split()
            except ValueError:
                k, v, u = line.split() + ['none']

            return k.rstrip(':'), int(v) * units[u]

        try:
            with open('/proc/meminfo') as fd:
                mem_stats = {k: v for k, v in [_process_meminfo_line(l) for l in fd.readlines()]}
        except IOError, e:
            raise RamUsageError('Error - Couldn\'t open /proc/meminfo. Details : {:}'.format(e))

        mem_stats.update({
            'in use': mem_stats['MemTotal'] - mem_stats['MemFree'],
            'free': mem_stats['MemFree'],
            'total': mem_stats['MemTotal'],
        })

        return mem_stats

    def _windows_ram_usage(self):
        try:
            from win32api import GlobalMemoryStatusEx
        except ImportError:
            raise RamUsageError('Error - Couldn\'t import win32api.')

        mem_stats = GlobalMemoryStatusEx()
        in_use = floor((mem_stats['MemoryLoad'] / 100.0) * mem_stats['TotalPhys'])

        mem_stats.update({
            'in use': in_use,
            'free': mem_stats['TotalPhys'] - in_use,
            'total': mem_stats['TotalPhys'],
        })

        return mem_stats

    def _get_thresholds(self):
        try:
            units = self.units[self._cli_options.units]
            min_ok, max_ok, min_warning, max_warning = [
                float(t) * units for t in self._cli_options.ok_threshold.split(',') + self._cli_options.warning_threshold.split(',')
            ]

            return {
                'min ok': min_ok,
                'max ok': max_ok,
                'min warning': min_warning,
                'max warning': max_warning,
            }
        except ValueError:
            raise RamUsageError('')
        except KeyError:
            raise RamUsageError('Error - Wrong \'{:}\' units parameter.')

    def _get_current_status(self, mem_stats):
        status = 'SEVERE'
        thresholds = self._get_thresholds()

        if thresholds['min ok'] < mem_stats['in use'] <= thresholds['max ok']:
            status = 'OK'
        elif thresholds['min warning'] < mem_stats['in use'] <= thresholds['max warning']:
            status = 'WARNING'

        return status

    def _get_detailed_output(self, mem_stats):
        return 'total : {:.2f}, in use : {:.2f}, free : {:.2f}.'.format(
            *[mem_stats[k] / float(self.units[self._cli_options.units]) for k in ['total', 'in use', 'free']]
        )

    def get(self):
        output = {'status': 'ERROR'}
        platform = platform_name()

        try:
            mem_stats = self.available_platforms[platform]()
            output.update({
                'status': self._get_current_status(mem_stats),
                'details': self._get_detailed_output(mem_stats),
                'data': {
                    'name': self.PROGRAM_NAME,
                    'in use': mem_stats['in use'],
                    'free': mem_stats['free'],
                    'total': mem_stats['total'],
                },
            })
        except RamUsageError, e:
            output.update({'details': str(e)})
        except KeyError:
            output.update({'details': '{:} platform is not supported.'.format(platform)})

        return serialize_json(output)


if __name__ == '__main__':
    print RamUsage().get()
