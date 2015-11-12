# -*- coding: utf-8 -*-
from zope.interface import implementer
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from repodono.registry.interfaces import IUtilityRegistry

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

    def __init__(self, title, description, interface, name):
        self.title = title
        self.description = description
        self.interface = interface
        self.name = name

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

    def enable(self, name):
        """
        Add the ``name`` into this registry's registration in the plone
        registry.
        """

        registry = queryUtility(IRegistry)
        if queryUtility(self.interface, name=name):
            registry[self.name] = registry[self.name] + [name]

    def disable(self, name):
        """
        Remove the ``name`` from this registry's registration in the
        plone registry.
        """

        registry = queryUtility(IRegistry)
        original = registry[self.name]
        registry[self.name] = [
            n for n in original
            if n != name and queryUtility(self.interface, name=n)
        ]
