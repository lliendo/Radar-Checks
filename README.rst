
Radar checks
============

This repository holds some basic and useful scripts to monitor :

    * Uptime.
    * Ram usage.
    * Disk usage.
    * Service alive.

All scripts are written in `Python <https://www.python.org/>` programming language.
They use the excellent `psutil <https://github.com/giampaolo/psutil>` module for maximum portability.


Documentation
-------------

All Radar checks provide help from the command line by providing the -h (or --help)
option.


Supported platforms
-------------------

All Radar checks should run fine at least on the following platforms :

    * GNU/Linux.
    * FreeBSD.
    * NetBSD.
    * OpenBSD.
    * Darwin / Mac OS X.
    * Microsoft Windows.


Installation
------------

Manually copy the checks you want to add to your Radar client's checks directory.


Tests
-----

Radar checks uses `Tox <http://codespeak.net/tox/>` to run its tests. To install Tox, from the
command line run :

.. code-block:: bash
    
    pip install tox


To run tests, clone the this repository and run Tox.

.. code-block:: bash

    git clone https://github.com/lliendo/Radar-Checks.git
    cd Radar-Checks
    tox


License
-------

Radar checks are distributed under the LGPL v3 license.


Contact
-------

If you find this software useful you can drop me a line. Bug reporting,
suggestions, missing documentation and critics of any kind are always welcome !


Special thanks
--------------

To Giampaolo Rodola for its psutil module.


Authors
-------

    * Lucas Liendo.
