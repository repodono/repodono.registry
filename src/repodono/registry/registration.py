# -*- coding: utf-8 -*-
from zope.interface import implementer
from zope.component import queryUtility
from zope.schema.interfaces import IList
from zope.schema.interfaces import IChoice
from plone.registry.interfaces import IRegistry

from repodono.registry.interfaces import IUtilityRegistry
from repodono.registry import logger

import textwrap

REGISTRATION_REPR = """\
<{class} {name} at 0x{id:x}
  interface: {interface}
  title: {title}
  {description}
>"""


@implementer(IUtilityRegistry)
class UtilityRegistry(object):
    """
    A registration for the utility registry for a given set of utilities
    identified by the given interface, where the availability of the
    tracked utilities to the end-users of the given site is managed by
    the list stored in the plone registry.

    This does require the accompanied entries (of the same identifiers)
    be registered using registry.xml for the given Plone add-on that
    makes use of this.
    """

    def __init__(self, title, description, interface, name, available_vocab):
        self.title = title
        self.description = description
        self.interface = interface
        self.name = name
        self.available_vocab = available_vocab

    def __repr__(self):
        info = {
            'class': self.__class__.__name__,
            'name': self.name,
            'id': id(self),
            'interface': self.interface.__identifier__,
            'title': self.title or '(no title)',
            'description': textwrap.fill(
                self.description or '(no description)',
                subsequent_indent='  '
            )
        }
        return REGISTRATION_REPR.format(**info)

    def verify_registry_key(self):
        registry = queryUtility(IRegistry)

        if registry is None:
            logger.warning('Plone registry is not available, doing nothing.')
            return False

        record = registry.records.get(self.name)

        if record is None:
            logger.warning(
                'The registry key for the utility registry `%s` is not '
                'registered.', self.name)
            return False

        if not (IList.providedBy(record.field) and
                IChoice.providedBy(record.field.value_type) and
                record.field.value_type.vocabularyName == self.available_vocab
                ):
            logger.warning(
                'The registry key for the utility registry `%s` is registered '
                'incorrectly.', self.name)
            return False

        return True

    def enable(self, name):
        """
        Add the ``name`` into this registry's registration in the plone
        registry.
        """

        if not self.verify_registry_key():
            return

        registry = queryUtility(IRegistry)
        enabled = set()
        result = []

        value = registry[self.name] or []

        for n in value + [name]:
            if n in enabled or not queryUtility(self.interface, name=n):
                continue
            enabled.add(unicode(n))
            result.append(n)

        registry[self.name] = result

    def disable(self, name):
        """
        Remove the ``name`` from this registry's registration in the
        plone registry.
        """

        if not self.verify_registry_key():
            return

        registry = queryUtility(IRegistry)

        original = registry[self.name]
        registry[self.name] = [
            n for n in original
            if n != name and queryUtility(self.interface, name=n)
        ]
