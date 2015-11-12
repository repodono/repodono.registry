# -*- coding: utf-8 -*-
import doctest
import unittest
from os.path import join

import zope.component.testing

path = lambda x: join('..', x)


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            path('utilities.rst'),
            setUp=zope.component.testing.setUp,
            tearDown=zope.component.testing.tearDown
        ),
    ))
