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
from random import randint


class Template(object):

    PROGRAM_NAME = 'template'

    def _get_status(self):
        statuses = ['OK', 'WARNING', 'SEVERE']
        return statuses[randint(0, len(statuses) - 1)]

    def check(self):
        output = {'status': 'ERROR'}

        try:
            output.update({
                'status': self._get_status(),
                'details': '',
                'data': {},
            })
        except Exception, e:
            output['details'] = str(e)

        return serialize_json(output)


if __name__ == '__main__':
    print Template().check()
