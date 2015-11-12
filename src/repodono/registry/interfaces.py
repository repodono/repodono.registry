# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.interface import Interface
from zope.interface.interfaces import IInterface


class IUtilityRegistry(Interface):
    """
    The registry interface.  User may adapt their utility interface to
    this interface.
    """

    title = schema.TextLine(
        title=u'Short title of this utility registry.',
        required=True,
    )

    description = schema.Text(
        title=u'Long description of what this registry is about.',
        required=False,
    )

    interface = schema.Object(
        title=u'The interface that this registry is for.',
        required=True,
        schema=IInterface,
    )

    name = schema.TextLine(
        title=u'The name of this utility.',
        required=True,
    )

    vocab_available = schema.TextLine(
        title=u'The name of the vocabulary that contain the entire set',
        required=True,
    )

    def enable(name):
        """
        Enable this utility in the registry identified by name.
        """

    def disable(name):
        """
        Enable this utility in the registry identified by name.
        """
