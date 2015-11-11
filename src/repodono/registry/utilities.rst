===================================
repodono.registry: Registry Utility
===================================

The goal is to provide user (manager) a way to enable or disable a set
of utilities for a particular interface.  Essentially the registry entry
serves as a filter for the results of ``getUtilitiesFor`` against the
target interface, at the same time register the relevant vocabularies.

Usage
-----

First, define an interface common to the set of utilities.
Second, register the utilities via zcml or other methods to a given
site.

Then define something like this::

    <repodono:utilities
        title="Backends available"
        description="Backends to be made available to end-users"
        interface=".interfaces.IStorageBackend"
        prefix="repodono.storage.backend"
        />

This would define the following things

- Two new vocabularies, one ``available``, other for ``enabled``,
  prefixed by ``prefix``.
- A new interface of the same name as the one specified in ``interface``
  at ``repodono.registry.interface`` specifically to enable registration
  in ``registry.xml``.  It will have a single field ``enabled`` of List
  with Choice based on the ones provided by the ``available`` version of
  the vocabulary above.
- The newly created interface will also provide a utility that provides
  the methods ``enabled`` and ``disabled`` that can be used by setup
  methods of an add-on that provides the specific utility to toggle.
- Naturally, the ``enabled`` vocabulary can be used in any other
  ``Choice`` field defined elsewhere.
