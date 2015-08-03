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
from psutil import virtual_memory


class RamUsageError(Exception):
    pass


class RamUsage(object):

    PROGRAM_NAME = 'ram-usage'

    def __init__(self):
        self.units = {
            'bytes': 1,
            'kib': 1024,
            'mib': 1024 ** 2,
            'gib': 1024 ** 3,
            # 'per': 1,
        }

        self._cli_options = self._build_argument_parser().parse_args()

    def _build_argument_parser(self):
        parser = ArgumentParser(prog=self.PROGRAM_NAME)
        parser.add_argument(
            '-u', '--units', dest='units', action='store', default='mib',
            help='Valid units are : kib, mib or gib. Default is mib.'
        )
        parser.add_argument(
            '-O', '--ok', dest='ok_threshold', action='store', required=True,
            help='Ok threshold. E.g : (0,1500]. Don\'t include brackets !'
        )
        parser.add_argument(
            '-W', '--warning', dest='warning_threshold', action='store', required=True,
            help='Warning threshold. E.g : (1500,1700]. Don\'t include brackets !'
        )

        return parser

    # TODO: Implement percentage units !
    def _get_thresholds(self):
        try:
            units = self.units[self._cli_options.units]
            thresholds = self._cli_options.ok_threshold.split(',') + self._cli_options.warning_threshold.split(',')
            min_ok, max_ok, min_warning, max_warning = [float(t) * units for t in thresholds]
        except ValueError, e:
            raise RamUsageError('Error - One or more given thresholds are invalid. Details : {:}'.format(e))
        except KeyError:
            raise RamUsageError('Error - Wrong \'{:}\' units parameter.'.format(self._cli_options.units))

        return {
            'min ok': min_ok,
            'max ok': max_ok,
            'min warning': min_warning,
            'max warning': max_warning,
        }

    def _get_status(self, stats):
        status = 'SEVERE'
        thresholds = self._get_thresholds()

        if thresholds['min ok'] < stats['in use'] <= thresholds['max ok']:
            status = 'OK'
        elif thresholds['min warning'] < stats['in use'] <= thresholds['max warning']:
            status = 'WARNING'

        return status

    def _get_details(self, stats):
        return 'Total : {:.2f}, in use : {:.2f}, available : {:.2f}.'.format(
            *[stats[k] / float(self.units[self._cli_options.units]) for k in ['total', 'in use', 'available']]
        )

    def _get_ram_usage(self):
        stats = virtual_memory()

        return {
            'in use': stats.used,
            'available': stats.available,
            'total': stats.total,
        }

    def check(self):
        output = {'status': 'ERROR'}

        try:
            stats = self._get_ram_usage()
            output.update({
                'status': self._get_status(stats),
                'details': self._get_details(stats),
                'data': stats,
            })

            output['data'].update({'name': self.PROGRAM_NAME})
        except Exception, e:
            output.update({'details': str(e)})

        return serialize_json(output)


if __name__ == '__main__':
    print RamUsage().check()
