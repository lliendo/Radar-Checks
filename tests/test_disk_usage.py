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


from json import loads
from nose.tools import raises
from mock import patch, MagicMock
from checks.disk_usage import DiskUsage, DiskUsageError
from . import TestCheck


class TestDiskUsage(TestCheck):
    def _get_options(self, partition='', units='', ok_threshold='', warning_threshold=''):
        return [
            ('-p', {'action': 'store', 'dest': 'partition', 'default': partition}),
            ('-u', {'action': 'store', 'dest': 'units', 'default': units}),
            ('-O', {'action': 'store', 'dest': 'ok_threshold', 'default': ok_threshold}),
            ('-W', {'action': 'store', 'dest': 'warning_threshold', 'default': warning_threshold})
        ]

    def _get_usage(self, in_use, available):
        return {
            'in use': in_use * (1024 ** 3),
            'available': available * (1024 ** 3),
            'total': (in_use + available) * (1024 ** 3),
        }

    def _test_invalid_args_raises_error(self, options):
        with patch.object(DiskUsage, '_build_argument_parser', return_value=self._get_argument_parser(options)):
            disk_usage = DiskUsage()
            disk_usage._get_thresholds()

    @raises(DiskUsageError)
    def test_invalid_units_raises_error(self):
        self._test_invalid_args_raises_error(self._get_options(partition='/', units='wrong_units'))

    @raises(DiskUsageError)
    def test_invalid_ok_threshold_raises_error(self):
        self._test_invalid_args_raises_error(self._get_options(partition='/', units='mib'))

    @raises(DiskUsageError)
    def test_invalid_warning_threshold_raises_error(self):
        self._test_invalid_args_raises_error(self._get_options(partition='/', units='mib', ok_threshold='0,500'))

    def _assert_disk_usage_returns_code(self, code, in_use, available):
        options = self._get_options('/', 'gib', '0,500', '500,1000')
        usage = self._get_usage(in_use, available)

        with patch.object(DiskUsage, '_build_argument_parser', return_value=self._get_argument_parser(options)):
            disk_usage = DiskUsage()
            disk_usage._get_disk_usage = MagicMock(side_effect=[usage])
            self.assertEqual(loads(disk_usage.check())['status'], code)

    def test_disk_usage_returns_ok_code(self):
        self._assert_disk_usage_returns_code('OK', 250, 1250)

    def test_disk_usage_returns_warning_code(self):
        self._assert_disk_usage_returns_code('WARNING', 750, 750)

    def test_disk_usage_returns_severe_code(self):
        self._assert_disk_usage_returns_code('SEVERE', 1250, 250)

    def test_disk_usage_returns_error_code(self):
        options = self._get_options()
        usage = self._get_usage(750, 750)

        with patch.object(DiskUsage, '_build_argument_parser', return_value=self._get_argument_parser(options)):
            disk_usage = DiskUsage()
            disk_usage._get_disk_usage = MagicMock(side_effect=[usage])
            self.assertEqual(loads(disk_usage.check())['status'], 'ERROR')
