#!/usr/bin/python

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
from psutil import process_iter


class ProcessStatusError(Exception):
    pass


class ProcessStatus(object):

    PROGRAM_NAME = 'process_status'

    def __init__(self):
        self._cli_options = self._build_argument_parser().parse_args()
        self._filters = {
            'process_name': lambda process: self._cli_options.process_name in process.name(),
            'process_status': lambda process: self._cli_options.process_status.lower() == process.status(),
        }
        self._verify_enabled_filters()

    def _verify_enabled_filters(self):
        if all([getattr(self._cli_options, key) is None for key in self._filters.keys()]):
            raise ProcessStatusError('Error - At least one of the available options (-n | -s) must be supplied.')

    def _build_argument_parser(self):
        parser = ArgumentParser(prog=self.PROGRAM_NAME)
        parser.add_argument(
            '-n', '--name', dest='process_name', action='store', required=False,
            default=None, help='The name of the process to look for.'
        )
        parser.add_argument(
            '-s', '--status', dest='process_status', action='store', required=False,
            default=None, help='The status of the process.'
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
            thresholds = self._cli_options.ok_threshold.split(',') + self._cli_options.warning_threshold.split(',')
            min_ok, max_ok, min_warning, max_warning = [int(threshold) for threshold in thresholds]
        except ValueError as error:
            raise ProcessStatusError('Error - One or more given thresholds are invalid. Details : {:}.'.format(error))

        return {
            'min ok': min_ok,
            'max ok': max_ok,
            'min warning': min_warning,
            'max warning': max_warning,
        }

    def _get_status(self, processes):
        status = 'SEVERE'
        thresholds = self._get_thresholds()
        process_count = len(processes)

        if thresholds['min ok'] < process_count <= thresholds['max ok']:
            status = 'OK'
        elif thresholds['min warning'] < process_count <= thresholds['max warning']:
            status = 'WARNING'

        return status

    def _get_details(self, processes):
        return '{:} \'{:}\' processes found'.format(len(processes), self._cli_options.process_name)

    def _filters_apply(self, process):
        enabled_filters = [filter for key, filter in self._filters.iteritems() if getattr(self._cli_options, key) is not None]
        return all([filter(process) for filter in enabled_filters])

    def _get_filtered_processes(self):
        return [process for process in process_iter() if self._filters_apply(process)]

    def check(self):
        output = {'status': 'ERROR'}

        try:
            processes = self._get_filtered_processes()
            output.update({
                'status': self._get_status(processes),
                'details': self._get_details(processes),
                'data': {
                    'process': self._cli_options.process_name,
                    'count': len(processes),
                    'name': self.PROGRAM_NAME,
                },
            })
        except Exception as error:
            output['details'] = str(error)

        return serialize_json(output)


if __name__ == '__main__':
    try:
        print ProcessStatus().check()
    except Exception as error:
        print error
