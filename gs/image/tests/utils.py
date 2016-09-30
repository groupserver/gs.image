# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals, print_function, division
from mock import patch
import os
from pkg_resources import resource_filename
from unittest import TestCase
from PIL import Image
from gs.image.utils import rgba, thumbnail_img, thumbnail_img_noaspect, thumbnail_img_square


class UtilTest(object):

    @staticmethod
    def load_image(filename):
        testname = os.path.join('tests', 'images', filename)
        fullname = resource_filename('gs.image', testname)
        retval = Image.open(file(fullname, 'rb'))
        return retval


class RGBATest(TestCase, UtilTest):
    def test_rgb_stat(self):
        'Test that an image that is already an RGB is left as-is'
        i = self.load_image('whirlpool.jpg')
        r = rgba(i)

        self.assertIs(i, r)

    def test_index_converted(self):
        'Test that an image with an indexed colour-map (a GIF) is converted to RGBA'
        i = self.load_image('grypaws.gif')
        r = rgba(i)

        self.assertIsNot(i, r)
        self.assertEqual('RGBA', r.mode)

    def test_exception(self):
        'Test that if an exception is raised we get the original image back'
        i = self.load_image('whirlpool.jpg')
        with patch.object(i, 'convert') as m_convert:
            m_convert.side_effect = Exception
            r = rgba(i)
        self.assertIs(i, r)


class ThumbnailTest(TestCase, UtilTest):
    def test_scale(self):
        'Test we scale and keep the same aspect ratio'
        i = self.load_image('whirlpool.jpg')
        r = thumbnail_img(i, 640, 480)

        self.assertEqual(r.size[0], 640)
        self.assertEqual(r.size[1], 400)

        aOrig = i.size[0] / i.size[1]
        aR = r.size[0] / r.size[1]
        self.assertEqual(aOrig, aR)

    def test_scale_indexed(self):
        'Test we keep the same image-mode'
        i = self.load_image('grypaws.gif')
        r = thumbnail_img(i, 10, 10)

        self.assertEqual(i.mode, r.mode)


class ThumbnailNoAspectTest(TestCase, UtilTest):
    def test_scale(self):
        'Test we can modify the aspect ratio when scaling'
        i = self.load_image('whirlpool.jpg')
        r = thumbnail_img_noaspect(i, 640, 480)

        self.assertEqual(r.size[0], 640)
        self.assertEqual(r.size[1], 480)

        aOrig = i.size[0] / i.size[1]
        aR = r.size[0] / r.size[1]
        self.assertNotEqual(aOrig, aR)


class ThumbnailImageSquare(TestCase, UtilTest):
    def test_scale(self):
        i = self.load_image('whirlpool.jpg')
        r = thumbnail_img_square(i, 640)

        self.assertEqual(r.size[0], 640)
        self.assertEqual(r.size[1], 640)

    def test_scale_indexed(self):
        i = self.load_image('grypaws.gif')
        r = thumbnail_img_square(i, 10)

        self.assertEqual(r.size[0], 10)
        self.assertEqual(r.size[1], 10)
