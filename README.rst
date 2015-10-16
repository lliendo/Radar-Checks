.. image:: https://codeclimate.com/github/lliendo/Radar-Checks/badges/gpa.svg
   :target: https://codeclimate.com/github/lliendo/Radar-Checks
   :alt: Code Climate


.. image:: https://api.travis-ci.org/lliendo/Radar-Checks.svg?branch=master
    :target: https://travis-ci.org/lliendo/Radar-Checks
    :alt: Travis CI


Radar checks
============

This repository contains some basic but useful checks to monitor :

* Uptime.
* Ram usage.
* Disk usage.
* Process status.

All scripts are written in the `Python <https://www.python.org/>`_ programming language.
They use the excellent `psutil <https://github.com/giampaolo/psutil>`_ module for maximum portability.
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

Clone this repository to a temporary directory using `GIT <https://git-scm.com/>`_ (or alternatively download
as `.zip <https://github.com/lliendo/Radar-Checks/archive/master.zip>`_), and run  :

.. code-block:: bash

    git clone https://github.com/lliendo/Radar-Checks.git
    cd Radar-Checks
    python setup.py install

Now manually copy the checks you want to use to your Radar's client checks
directory.


Tests
-----

Radar-Checks uses `Nose <https://nose.readthedocs.org/en/latest/>`_ to run its tests.
To install Nose, from the command line run :

.. code-block:: bash
    
    pip install nose

To run the tests, clone the this repository and run Nose.

.. code-block:: bash

    git clone https://github.com/lliendo/Radar-Checks.git
    cd Radar-Checks
    nosetests


License
-------

Radar checks are distributed under the `GNU LGPLv3 <https://www.gnu.org/licenses/lgpl.txt>`_ license. 


Acknowledgements
----------------

To `Giampaolo Rodola <https://github.com/giampaolo>`_  for its psutil module.


Authors
-------

* Lucas Liendo.
