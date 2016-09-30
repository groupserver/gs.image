# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015, 2016 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from unittest import TestSuite, main as unittest_main
from gs.image.tests.image import (GSImageTest, GSImageJPEGTest, GSImagePNGTest, GSImageGIFTest,
                                  GSImageWideTest)
from gs.image.tests.utils import (
    RGBATest, ThumbnailTest, ThumbnailNoAspectTest, ThumbnailImageSquare)
testCases = (GSImageTest, GSImageJPEGTest, GSImagePNGTest, GSImageGIFTest, GSImageWideTest,
             RGBATest, ThumbnailTest, ThumbnailNoAspectTest, ThumbnailImageSquare)


def load_tests(loader, tests, pattern):
    suite = TestSuite()
    for testClass in testCases:
        tests = loader.loadTestsFromTestCase(testClass)
        suite.addTests(tests)
    return suite

if __name__ == '__main__':
    unittest_main()
