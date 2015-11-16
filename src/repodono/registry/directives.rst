==================================
repodono.registry: ZCML directives
==================================

The registry defines a ZCML directive in meta.zcml as per convention.

The following shows that the ``repodono.utilities`` directive will
register the vocabulary that leverages on top of ``plone.registry``.

Demonstration
-------------

A complete zcml for this might be defined like so::

Then define something like this::

    >>> configuration = """\
    ... <configure
    ...     package="repodono.registry"
    ...     xmlns="http://namespace.zope.org/zope"
    ...     xmlns:repodono="http://namespaces.physiomeproject.org/repodono"
    ...     i18n_domain="repodono.registry.tests">
    ...
    ...   <include package="repodono.registry" file="meta.zcml" />
    ...
    ...   <repodono:utilities
    ...       title="Backends available"
    ...       description="Backends to be made available to end-users"
    ...       interface="repodono.registry.testing.IMessageUtility"
    ...       name="repodono.message.utility"
    ...       />
    ...
    ... </configure>
    ... """

First verify that nothing related to the above declaration have been
registered beforehand::

    >>> from zope.component import getGlobalSiteManager
    >>> from zope.component import queryUtility
    >>> sm = getGlobalSiteManager()
    >>> from zope.schema.interfaces import IVocabularyFactory
    >>> from repodono.registry.interfaces import IUtilityRegistry
    >>> [u for u in sm.registeredUtilities()
    ...  if u.name == u"repodono.message.utility"]
    []
    >>> queryUtility(IVocabularyFactory, name="repoodno.storage.backend")

Now load the sample configuration which includes the ``meta.zcml`` that
defines the directive::

    >>> from StringIO import StringIO
    >>> from zope.configuration import xmlconfig
    >>> xmlconfig.xmlconfig(StringIO(configuration))

First and foremost, query for the utility that was registered via this
directive::

    >>> len([u for u in sm.registeredUtilities()
    ...      if u.name == u"repodono.message.utility"])
    2
    >>> u = queryUtility(IUtilityRegistry, name=u'repodono.message.utility')
    >>> u  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    <UtilityRegistry repodono.message.utility at ...
      interface: repodono.registry.testing.IMessageUtility
      title: Backends available
      Backends to be made available to end-users
    >

It would also do nothing, with the plone registry not being available::

    >>> u.enable('basic')
    >>> u.disable('basic')

Secondly, the vocabularies must be available::

    >>> v_enabled = queryUtility(IVocabularyFactory,
    ...                          name=u'repodono.message.utility')
    >>> v_available = queryUtility(IVocabularyFactory,
    ...                            name=u'repodono.message.utility.available')

Without the registry in place and also none of the utilities registered
for the ``IMessageUtility`` interface, an empty list should simply be
returned::

    >>> v_enabled(None)  # doctest: +ELLIPSIS
    <zope.schema.vocabulary.SimpleVocabulary object at ...>
    >>> v_available(None)  # doctest: +ELLIPSIS
    <zope.schema.vocabulary.SimpleVocabulary object at ...>
    >>> list(v_enabled(None)) == list(v_available(None)) == []
    True

Before the enabled vocabulary will work, the actual registry utility
will need to be available.  As the ideal editing interface is provided
if the correct schemas are registered, the definitions that one might
define within a ``registry.xml`` will be recreated here::

    >>> from plone.registry.interfaces import IRegistry
    >>> from plone.registry.registry import Registry, Record
    >>> from plone.registry.field import List, Choice
    >>> registry = Registry()
    >>> registry.records['repodono.message.utility'] = Record(
    ...     List(
    ...         title=u'Enabled Message Type',
    ...         default=[],
    ...         required=True,
    ...         value_type=Choice(
    ...             vocabulary='repodono.message.utility.available'),
    ...     )
    ... )
    >>> sm.registerUtility(registry, IRegistry)

The available vocabulary should start working once any of the components
declared in the ``testing`` module be registered as a named global
utility::

    >>> from repodono.registry import testing
    >>> sm.registerUtility(testing.BasicMessage(), name="basic")

The available vocabulary should reflect this::

    >>> list(t.value for t in v_available(None))
    [u'basic']

If we use the utility registry to enable this term, it will also be
shown in the enabled vocabulary::

    >>> u.enable(u'basic')
    >>> list(t.value for t in v_enabled(None))
    [u'basic']

At least until the utilities are registered::

    >>> sm.registerUtility(testing.AdvancedMessage(), name="advanced")
    >>> sm.registerUtility(testing.LuxuryMessage(), name="luxury")
    >>> u.enable(u'advanced')
    >>> list(t.value for t in v_enabled(None))
    [u'basic', u'advanced']

Available version should contain everything::

    >>> list(t.value for t in v_available(None))
    [u'luxury', u'advanced', u'basic']

TODO verify that the sorting is stable, and whether a sorted output is
more desirable.

Shouldn't duplicate entries::

    >>> u.enable(u'basic')
    >>> list(t.value for t in v_enabled(None))
    [u'basic', u'advanced']

Naturally, the enabled vocabulary should never provide names that have
been unregistered from the interface at the global level::

    >>> advanced = queryUtility(testing.IMessageUtility, 'advanced')
    >>> sm.unregisterUtility(advanced, name='advanced')
    True
    >>> list(t.value for t in v_enabled(None))
    [u'basic']
    >>> registry['repodono.message.utility']
    [u'basic', u'advanced']

Enabling should really disable the value and not cause any schema
conflicts::

    >>> u.enable(u'luxury')
    >>> registry['repodono.message.utility']
    [u'basic', u'luxury']

TODO: document how might the ordering of the enabled vocabulary on
various manipulation methods be determined.

Integrators that make use of this directive should construct integration
tests that makes use of their test layers and test via the testbrowser
to ensure that the interactions with the registry configuration editor
achieves the exact desired results.
