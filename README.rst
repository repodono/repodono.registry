=================
repodono.registry
=================

Integrates and extends the Plone registry to support the management of
what global utilities are visible for end-users to use for a given site
with the of vocabularies, with such a declaration be done with just a
single zcml statement (and a corresponding registry.xml entry).

.. image:: https://travis-ci.org/repodono/repodono.registry.svg?branch=master
  :target: https://travis-ci.org/repodono/repodono.registry
.. image:: https://coveralls.io/repos/repodono/repodono.registry/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/repodono/repodono.registry?branch=master


Documentation
-------------

TODO.


Installation
------------

Install repodono.registry by adding it to your buildout::

   [buildout]
    ...
    eggs =
        repodono.registry

and then running "bin/buildout"

License
-------

The project is licensed under the GPLv2.
