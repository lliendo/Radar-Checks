Radar checks
============

    This repository contains some basic but useful checks to monitor :

        * Uptime.
        * Ram usage.
        * Disk usage.
        * Process status.

    All scripts are written in the `Python <https://www.python.org/>` programming language.
    They use the excellent `psutil <https://github.com/giampaolo/psutil>` module for maximum portability.
    There's also included a template that you can use as a starting point to code
    a check.


Documentation
-------------

    All Radar checks provide help from the command line by passing the -h (or --help)
    command line argument.


Supported platforms
-------------------

    These set of checks rely on the psutil to properly work. As long as psutil is
    supported on your platform you'll be able to run them without issues.


Installation
------------

    Clone this repository to a temporary directory using GIT, and run  :

        .. code-block:: bash

            git clone https://github.com/lliendo/Radar-Checks.git
            cd Radar-Checks
            python setup.py install

    Now manually copy the checks you want to use to your Radar's client checks
    directory.


Tests
-----

    Radar-Checks uses `Tox <http://codespeak.net/tox/>` to run its tests.
    To install Tox, from the command line run :

        .. code-block:: bash
            
            pip install tox

    To run the tests, clone the this repository and run Tox.

        .. code-block:: bash

            git clone https://github.com/lliendo/Radar-Checks.git
            cd Radar-Checks
            tox


License
-------

    Radar checks are distributed under the LGPL v3 license.


Acknowledgements
----------------

    To Giampaolo Rodola for its `psutil <https://github.com/giampaolo/psutil>` module.


Authors
-------

    * Lucas Liendo.
