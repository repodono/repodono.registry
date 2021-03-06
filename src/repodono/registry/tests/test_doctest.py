# -*- coding: utf-8 -*-
import doctest
import unittest
from os.path import join

from plone.testing import layered
from plone.testing import zca

import zope.component.testing

path = lambda x: join('..', x)


def setUp(suite):  # pragma: no cover
    zope.component.testing.setUp(suite)

    try:
        from Zope2.App.schema import configure_vocabulary_registry
    except ImportError:
        try:
            from zope.schema.vocabulary import setVocabularyRegistry
            from Products.Five.schema import Zope2VocabularyRegistry
        except ImportError:
            pass
        else:
            setVocabularyRegistry(Zope2VocabularyRegistry())
    else:
        configure_vocabulary_registry()


def test_suite():
    return unittest.TestSuite((
        layered(
            doctest.DocFileSuite(
                path('directives.rst'),
                setUp=setUp,
                tearDown=zope.component.testing.tearDown
            ),
            layer=zca.UNIT_TESTING,
        ),

        doctest.DocFileSuite(
            path('utilities.rst'),
            setUp=setUp,
            tearDown=zope.component.testing.tearDown
        ),
    ))
