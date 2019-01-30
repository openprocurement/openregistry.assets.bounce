.. image:: https://travis-ci.org/openprocurement/openregistry.assets.bounce.svg?branch=master
    :target: https://travis-ci.org/openprocurement/openregistry.assets.bounce

.. image:: https://coveralls.io/repos/openprocurement/openregistry.assets.bounce/badge.svg
  :target: https://coveralls.io/r/openprocurement/openregistry.assets.bounce

.. image:: https://img.shields.io/hexpm/l/plug.svg
    :target: https://github.com/openprocurement/openregistry.assets.bounce/blob/master/LICENSE.txt


Documentation
=============

openregistry.assets.bounce contains the description of the Registry Data Base.

How to build the docs
+++++++++++++++++++++

To build the docs with existing sources, just run::

./docs/makedocs.sh

Build process could require you to install `sphinx_rtd_theme` package with `pip`. If it does - do that.

To update request files, that will be used as source for the tutorial docs generation, run this::

./docs/gen-requests.sh
