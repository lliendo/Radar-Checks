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
from psutil import process_iter


class ProcessStatusError(Exception):
    pass


class ProcessStatus(object):

    PROGRAM_NAME = 'process-status'

    def __init__(self):
        self._cli_options = self._build_argument_parser().parse_args()

    def _build_argument_parser(self):
        parser = ArgumentParser(prog=self.PROGRAM_NAME)
        parser.add_argument(
            '-n', '--name', dest='process_name', action='store', required=True,
            help='The name of the process to look for.'
        )
        parser.add_argument(
            '-O', '--ok', dest='ok_threshold', action='store', required=True,
            help='Ok threshold. E.g : (0,1]. Don\'t include brackets !'
        )
        parser.add_argument(
            '-W', '--warning', dest='warning_threshold', action='store', required=True,
            help='Warning threshold. E.g : (1,30]. Don\'t include brackets !'
        )

        return parser

    def _get_thresholds(self):
        try:
            min_ok, max_ok, min_warning, max_warning = self._cli_options.ok_threshold.split(',') + \
                self._cli_options.warning_threshold.split(',')
        except ValueError, e:
            raise ProcessStatusError('Error - One or more given thresholds are invalid. Details : {:}'.format(e))

        return {
            'min ok': min_ok,
            'max ok': max_ok,
            'min warning': min_warning,
            'max warning': max_warning,
        }

    def _get_current_status(self, processes):
        status = 'SEVERE'
        thresholds = self._get_thresholds()
        process_count = len(processes)

        if thresholds['min ok'] < process_count <= thresholds['max ok']:
            status = 'OK'
        elif thresholds['min warning'] < process_count <= thresholds['max warning']:
            status = 'WARNING'

        return status

    def _get_detailed_output(self, processes):
        return '{:} \'{:}\' processes found.'.format(len(processes), self._cli_options.process_name)

    def _get_processes(self):
        return [p for p in process_iter() if self._cli_options.process_name in p.name()]

    def check(self):
        output = {'status': 'ERROR'}

        try:
            processes = self._get_processes()
            output.update({
                'status': self._get_current_status(processes),
                'details': self._get_detailed_output(processes),
                'data': {
                    'process': self._cli_options.process_name,
                    'count': len(processes),
                },
            })

            output['data'].update({'name': self.PROGRAM_NAME})
        except Exception, e:
            output.update({'details': str(e)})

        return serialize_json(output)


if __name__ == '__main__':
    print ProcessStatus().check()
