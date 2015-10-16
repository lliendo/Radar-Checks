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


from sys import argv
from json import loads
from unittest import TestCase
from nose.tools import raises
from mock import MagicMock
from checks.uptime import Uptime, UptimeError


class TestUptime(TestCase):
    def _assert_uptime_returns_code(self, code, uptime_seconds):
        argv.extend(['-S', '300'])
        uptime = Uptime()
        uptime._get_uptime = MagicMock(side_effect=[uptime_seconds])
        self.assertEqual(loads(uptime.check())['status'], code)

    def test_uptime_returns_ok_code(self):
        self._assert_uptime_returns_code('OK', 301)

    def test_uptime_returns_severe_code(self):
        self._assert_uptime_returns_code('SEVERE', 60)

    @raises(Exception)
    def test_no_args_supplied_raises_error():
        Uptime()

    @raises(UptimeError)
    def test_cli_negative_seconds_raises_uptime_error(self):
        argv.extend(['-S', '-1'])
        Uptime()._get_status(1000)
