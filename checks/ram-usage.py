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


from math import ceil
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

        self._cli_options = self._build_argument_parser().parse_args()

    def _build_argument_parser(self):
        parser = ArgumentParser(prog=self.PROGRAM_NAME)
        parser.add_argument('-p', '--partition', dest='partition', action='store', required=True)
        parser.add_argument('-u', '--units', dest='units', action='store')
        parser.add_argument('-O', '--ok', dest='ok_threshold', action='store', required=True)
        parser.add_argument('-W', '--warning', dest='warning_threshold', action='store', required=True)
        parser.add_argument('-S', '--severe', dest='severe_threshold', action='store', required=True)
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
                mem_info = {k: v for k, v in [_process_meminfo_line(l) for l in fd.readlines()]}
        except IOError, e:
            raise RamUsageError('Error - Couldn\'t open /proc/meminfo. Details : {:}'.format(e))

        return mem_info

    def _windows_ram_usage(self):
        try:
            from win32api import GlobalMemoryStatusEx
        except ImportError:
            raise RamUsageError('Error - Couldn\'t import win32api.')

        mem_info = GlobalMemoryStatusEx()
        mem_info.update({
            'MemFree': mem_info['TotalPhys'] - ceil((mem_info['MemoryLoad'] / 100.0) * mem_info['TotalPhys'])
        })

        return mem_info

    def _get_current_status(self, seconds):
        pass

    def _get_detailed_output(self, seconds):
        pass

    def get(self):
        output = {'status': 'ERROR'}
        platform = platform_name()

        try:
            mem_info = int(self.available_platforms[platform]())
            output.update({
                'status': self._get_current_status(mem_info),
                'details': self._get_detailed_output(mem_info),
                'data': {'name': self.PROGRAM_NAME, 'uptime': mem_info},
            })
        except RamUsageError, e:
            output.update({'details': str(e)})
        except ValueError:
            output.update({'details': 'Error - uptime\'s \'-s\' argument must be a valid interger value.'})
        except KeyError:
            output.update({'details': '{:} platform is not supported.'.format(platform)})

        return serialize_json(output)


if __name__ == '__main__':
    print RamUsage().get()
