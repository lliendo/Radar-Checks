
Radar checks
============

This repository holds some basic and useful scripts to monitor :

    * Uptime.
    * Ram usage.
    * Disk usage.

All scripts are written in Python programming language.


Documentation
-------------

All Radar checks provide help from the command line by providing the -h (or --help)
argument.


Supported platforms
-------------------

All Radar checks should run in the following platforms :

    * GNU/Linux.
    * FreeBSD.
    * NetBSD.
    * OpenBSD.
    * Darwin / Mac OS X.
    * Microsoft Windows.

Additional dependences are required for these checks to properly run in some
OSes :

    * FreeBSD : 
    * Microsoft Windows : Requires the pywin32 module.


Installation
------------

Manually copy the checks you want to add to your Radar client's checks
directory.


Tests
-----

Radar checks uses Travis CI to run its tests. You can however run tests manually by
cloning the latest version of this project (you will need to install `Tox <https://...>`) :

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


Authors
-------

    * Lucas Liendo.
