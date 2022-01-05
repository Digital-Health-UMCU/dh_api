========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis| |requires|
        | |codecov|
    * - package
      - | |commits-since|

.. |travis| image:: https://api.travis-ci.com/Digital-Health-UMCU/dh_api.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/Digital-Health-UMCU/dh_api

.. |requires| image:: https://requires.io/github/Digital-Health-UMCU/dh_api/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/Digital-Health-UMCU/dh_api/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/Digital-Health-UMCU/dh_api/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Digital-Health-UMCU/dh_api

.. |commits-since| image:: https://img.shields.io/github/commits-since/Digital-Health-UMCU/dh_api/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/Digital-Health-UMCU/dh_api/compare/v0.0.0...master



.. end-badges

Python package to install standardized UMCU Digital Health API

* Free software: MIT license

Installation
============

::

    pip install dh-api

You can also install the in-development version with::

    pip install https://github.com/Digital-Health-UMCU/dh_api/archive/master.zip


Documentation
=============


To use the project:

.. code-block:: python

    import dh_api
    dh_api.longest()


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
