# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.interface import implementer


class IMessageUtility(Interface):

    def message(context):
        """Message a context"""


@implementer(IMessageUtility)
class BasicMessage(object):

    def message(self, context):
        "Messaging basic"


@implementer(IMessageUtility)
class AdvancedMessage(object):

    def message(self, context):
        "Messaging advanced"


@implementer(IMessageUtility)
class LuxuryMessage(object):

    def message(self, context):
        "Messaging luxury"
