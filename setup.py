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


from setuptools import setup


setup(
    name='Radar-Checks',
    description='Basic Radar checks',
    version='0.0.1a',
    author='Lucas Liendo',
    author_email='mindmaster@gmail.com',
    keywords='monitor monitoring system administration',
    license='LGPLv3',
    zip_safe=False,
    test_suite='nose.collector',
    url='https://github.com/lliendo/Radar-Checks',
    install_requires=[
        'nose==1.3.7',
        'psutil==3.1.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python 2',
        'Programming Language :: Python 2.7',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
    ],
)
