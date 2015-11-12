# -*- coding: utf-8 -*-
from zope.component.zcml import utility
from zope.component import queryUtility
from zope.component import getUtilitiesFor
from zope.configuration import fields as configuration_fields
from zope.interface import provider
from zope.interface import Interface
from zope.schema import TextLine
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import getVocabularyRegistry

from plone.registry.interfaces import IRegistry

from repodono.registry import logger
from repodono.registry.interfaces import IUtilityRegistry
from repodono.registry.registration import UtilityRegistry


class IUtilityRegistryDirective(Interface):
    """
    Directive which registers the availablility of global utilities
    within a given Plone site to the Plone registry, from an end-user
    perspective.
    """

    interface = configuration_fields.GlobalInterface(
        title=u"Utility Interface",
        description=u"The interface of the utilities to be queried.",
        required=True,
    )

    name = TextLine(
        title=u"name",
        description=u"Name for the registration.  This registry will be "
                    "registered as utility with this name, along with the "
                    "vocabulary for getting the names of utilities that have "
                    "been enabled in the registry.  There should be a choice "
                    "entry that is defined with this name also as per "
                    "documentation.",
        required=True,
    )

    title = configuration_fields.MessageID(
        title=u"Title",
        description=u"A user friendly title describing this registry.",
        required=True,
    )

    description = configuration_fields.MessageID(
        title=u"Description",
        description=u"A longer description for what this utility registry is.",
        required=False,
    )

    available_vocab = TextLine(
        title=u"Available vocabulary name",
        description=u"The name for the vocabulary of the available utilities. "
                    "Default value is the `name + .available`.",
        required=False,
    )


def UtilityRegistryDirective(_context, interface, name, title,
                             description=None, available_vocab=None):
    utility_registry = UtilityRegistry(
        title=title,
        description=description,
        interface=interface,
        name=name,
    )

    enabled_vocab = name
    if available_vocab is None:
        available_vocab = name + '.available'

    # Register the registration for the utility registry as a utility.
    utility(
        _context,
        provides=IUtilityRegistry,
        name=name,
        component=utility_registry,
    )

    @provider(IVocabularyFactory)
    def AvailableVocabFactory(context):
        terms = []

        for name, _ in getUtilitiesFor(interface):
            # TODO define standard i18n the title for implementations
            title = name
            terms.append(SimpleVocabulary.createTerm(name, name, title))

        return SimpleVocabulary(terms)

    @provider(IVocabularyFactory)
    def EnabledVocabFactory(context):
        terms = []

        registry = queryUtility(IRegistry)
        if not registry:
            logger.warning(
                'No registry found, unable to provide registry backed '
                'vocabulary.'
            )
            return SimpleVocabulary([])
        enabled = registry[enabled_vocab]
        for name in enabled:
            if queryUtility(interface, name=name) is None:
                continue
            # TODO define standard i18n the title for implementations
            title = name
            terms.append(SimpleVocabulary.createTerm(name, name, title))

        return SimpleVocabulary(terms)

    vr = getVocabularyRegistry()

    utility(
        _context,
        provides=IVocabularyFactory,
        name=available_vocab,
        component=AvailableVocabFactory,
    )

    vr.register(available_vocab, AvailableVocabFactory)

    utility(
        _context,
        provides=IVocabularyFactory,
        name=enabled_vocab,
        component=EnabledVocabFactory,
    )

    vr.register(enabled_vocab, EnabledVocabFactory)

    # The actual fields will need to be registered through registry.xml
