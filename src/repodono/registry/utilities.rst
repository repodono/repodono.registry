===================================
repodono.registry: Utility Registry
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
        name="repodono.storage.backend"
        />

This would define the following things

- Register a utility that provides ``IUtilityRegistry`` with the name
  ``name``.  This utility will provide methods to enable/disable the
  name of the utility identified by ``interface`` from an end-user's
  perspective, assuming the corresponding Plone registry entry is
  also correctly provided.  See below.
- Two new vocabularies, one with the same name as ``name`` which can be
  used by end-user facing fields that require a vocabulary name, the
  other will be suffixed with ``.available`` by default, or be manually
  specified using ``available_vocab``.  This will provide the list of
  all utilities that are registered against the ``interface`` which
  serves as the vocabulary for the plone registry list entry.

The corresponding entry MUST be defined in ``registry.xml`` in the
generic setup profile, otherwise the methods provided will not work
(along with the vocabularies that are provided.  look like this, given
the above zcml configuration::

    <?xml version="1.0"?>
    <registry>
      <record name="repodono.storage.backend">
        <field type="plone.registry.field.List">
          <title>Backends available to end-users</title>
          <value_type type="plone.registry.field.Choice">
            <vocabulary>repodono.storage.backend.available</vocabulary>
          </value_type>
        </field>
      </record>
    </registry>

Example
-------

As an example on how the registry utility object might work, let's
define a basic utility that is described by the following interface::

    >>> from zope.interface import implementer
    >>> from zope.interface import Interface

    >>> class IBackend(Interface):
    ...     def acquire(context):
    ...         "Acquire from context."

Then define a couple utilities based on that::

    >>> @implementer(IBackend)
    ... class LocalBackend(object):
    ...     def acquire(self, context):
    ...         return "Local of: %s" % context
    ...
    >>> @implementer(IBackend)
    ... class RemoteBackend(object):
    ...     def acquire(self, context):
    ...         return "Remote to: %s" % context

Register the two backends as ``IBackend`` utilities::

    >>> from zope.component import provideUtility
    >>> from zope.component import getUtilitiesFor
    >>> from zope.component import queryUtility
    >>> provideUtility(LocalBackend(), name="local")
    >>> provideUtility(RemoteBackend(), name="remote")
    >>> [(k, v.__class__.__name__) for k, v in getUtilitiesFor(IBackend)]
    [(u'local', 'LocalBackend'), (u'remote', 'RemoteBackend')]

Now construct the utility registry registration::

    >>> from repodono.registry.registration import UtilityRegistry
    >>> registration = UtilityRegistry(
    ...     title=u"Backend Utilities",
    ...     description=u"The set of backend utilities.",
    ...     interface=IBackend,
    ...     name=u"repodono.test.backend",
    ... )
    >>> registration  # doctest: +ELLIPSIS
    <UtilityRegistry repodono.test.backend at ...
      interface: __builtin__.IBackend
      title: Backend Utilities
      The set of backend utilities.
    >

One can use the methods provided by the registration directly to
interact with the plone registry.  However, we don't have one yet, so
let's mock one up first::

    >>> from plone.registry.interfaces import IRegistry
    >>> registry = {'repodono.test.backend': []}
    >>> provideUtility(registry, IRegistry)

Enabling should work as expected, ignoring names that are not
registered::

    >>> registration.enable('remote')
    >>> registration.enable('local')
    >>> registration.enable('unregistered')
    >>> registry
    {'repodono.test.backend': ['remote', 'local']}

Likewise, disable should work as expected, ignoring unregistered names::

    >>> registration.disable('unregistered')
    >>> registration.disable('remote')
    >>> registry
    {'repodono.test.backend': ['local']}
