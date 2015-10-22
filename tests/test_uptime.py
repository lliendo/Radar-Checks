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
from checks.uptime import Uptime, UptimeError
from . import TestCheck


class TestUptime(TestCheck):
    def _get_options(self, severe_uptime=''):
        return [
            ('-S', {'action': 'store', 'dest': 'seconds', 'default': severe_uptime})
        ]

    def _assert_uptime_returns_code(self, code, uptime_seconds):
        options = self._get_options('300')

        with patch.object(Uptime, '_build_argument_parser', return_value=self._get_argument_parser(options)):
            uptime = Uptime()
            uptime._get_uptime = MagicMock(side_effect=[uptime_seconds])
            self.assertEqual(loads(uptime.check())['status'], code)

    @raises(Exception)
    def test_no_args_supplied_raises_error():
        Uptime()

    @raises(UptimeError)
    def test_cli_negative_seconds_raises_uptime_error(self):
        options = self._get_options('-1')

        with patch.object(Uptime, '_build_argument_parser', return_value=self._get_argument_parser(options)):
            Uptime()._get_status(1000)

    def test_uptime_returns_ok_code(self):
        self._assert_uptime_returns_code('OK', 301)

    def test_uptime_returns_severe_code(self):
        self._assert_uptime_returns_code('SEVERE', 60)

    def test_uptime_returns_error_code(self):
        options = self._get_options()

        with patch.object(Uptime, '_build_argument_parser', return_value=self._get_argument_parser(options)):
            self.assertEqual(loads(Uptime().check())['status'], 'ERROR')
