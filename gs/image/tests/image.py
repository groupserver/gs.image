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
import base64
import logging
from mock import patch
import os
from pkg_resources import resource_filename
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase
from gs.image.image import GSImage


class GSITest(TestCase):
    '''An abstract base-class for the image tests. Needs ``self.dataDir`` defined.'''

    @staticmethod
    def filename_in_tests(filename):
        testname = os.path.join('tests', 'images', filename)
        retval = resource_filename('gs.image', testname)
        return retval

    def load_image(self, filename):
        fullname = self.filename_in_tests(filename)
        with patch('gs.image.image.locateDataDirectory') as mock_ldd:
            mock_ldd.return_value = self.dataDir
            retval = GSImage(open(fullname, 'rb'))
        return retval

    def get_resized(self, width, height, maintain_aspect=True, only_smaller=True):
        with patch('gs.image.image.locateDataDirectory') as mock_ldd:
            mock_ldd.return_value = self.dataDir
            retval = self.image.get_resized(width, height, maintain_aspect, only_smaller)
        return retval


class GSImageTest(GSITest):
    '''Basic test for the :class:`GSImage` class'''

    #: A tiny 1px transparent PNG from <http://garethrees.org/2007/11/14/pngcrush/>
    TINY_PNG = base64.decodestring(b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAA'
                                   b'QAABQABDQottAAA\nAABJRU5ErkJggg==\n')

    def setUp(self):
        self.dataDir = mkdtemp()

    @patch('gs.image.image.locateDataDirectory')
    def test_init(self, m_ldd):
        m_ldd.return_value = '/tmp/'
        r = GSImage(self.TINY_PNG)

        self.assertEqual(1, m_ldd.call_count)
        self.assertEqual('93ca32a536da1698ea979f183679af29', r.md5sum)

    @patch('gs.image.image.locateDataDirectory')
    def test_setData(self, m_ldd):
        '''Ensure we get the data back'''
        m_ldd.return_value = '/tmp/'
        i = GSImage(b'')  # --=mpj17=-- To ensure that the __init__ does not cause issues
        i.data = self.TINY_PNG
        r = i.data

        self.assertEqual(self.TINY_PNG, r)
        self.assertEqual(67, i._size)
        self.assertEqual('image/png', i._contentType)
        self.assertEqual(1, i._width)
        self.assertEqual(1, i._height)

    @patch('gs.image.image.locateDataDirectory')
    def test_data_set_none(self, m_ldd):
        'Ensure it is impossible to set the data to None'
        m_ldd.return_value = '/tmp/'
        with self.assertRaises(TypeError):
            GSImage(None)

    @patch('gs.image.image.locateDataDirectory')
    def test_data_set_file(self, m_ldd):
        'Ensure we can set the image-data to a file'
        m_ldd.return_value = '/tmp/'
        i = GSImage(b'')
        filename = self.filename_in_tests('tiny.png')
        with open(filename, 'rb') as f:
            i.data = f
        r = i.data

        self.assertEqual(self.TINY_PNG, r)

    def test_width(self):
        i = self.load_image('warty-final-ubuntu.png')
        r = i.width

        self.assertEqual(1600, r)

    def test_height(self):
        i = self.load_image('warty-final-ubuntu.png')
        r = i.height

        self.assertEqual(1200, r)


class GSImageJPEGTest(GSITest):

    def setUp(self):
        self.dataDir = mkdtemp()

        self.image = self.load_image('whirlpool.jpg')
        self.original_width = 1280
        self.original_height = 800
        self.original_aspect = self.original_width / self.original_height

    def tearDown(self):
        rmtree(self.dataDir)

    def test_resize_content_type(self):
        'Test the content-type stays the same for a JPEG'
        width, height = (640, 480)
        r = self.get_resized(width, height)

        self.assertEqual('image/jpeg', r.contentType)
        self.assertEqual(self.image.contentType, r.contentType)

    def test_resize_aspect(self):
        width, height = (640, 480)
        r = self.get_resized(width, height)

        self.assertEqual(width, r.width)
        self.assertGreaterEqual(self.original_width, r.width)
        self.assertGreaterEqual(height, r.height)
        self.assertGreaterEqual(self.original_height, r.height)

        new_aspect = r.width / r.height
        self.assertEqual(self.original_aspect, new_aspect)

    def test_resize_h_w_switch(self):
        'Switch around the height and width to double check that the aspect ratios are maintained'
        height = 640
        width = 480
        r = self.get_resized(width, height)

        self.assertGreaterEqual(self.original_height, r.height)
        self.assertGreaterEqual(self.original_width, r.width)

        new_aspect = r.width / r.height
        self.assertEqual(self.original_aspect, new_aspect)

    def test_resize_cached(self):
        'Resize an image and it should be cached'
        width = 640
        height = 480
        r = self.get_resized(width, height)  # lint:ok

        self.assertEqual(1, len(os.listdir(self.dataDir)))

    @patch('gs.image.image.locateDataDirectory')
    def test_resize_cached_retrieve(self, mock_ldd):
        'Resize an image -- do it twice, the second time should be retrieved from the cache'
        mock_ldd.return_value = self.dataDir
        width = 640
        height = 480
        # Prime the cache
        r = self.get_resized(width, height)  # lint:ok

        with patch.object(self.image, '_get_resized_img') as mock_gri:
            fileName = self.image.get_cache_name(width, height)

        self.assertEqual(0, mock_gri.call_count)
        self.assertTrue(os.path.isfile(fileName))

    @patch('gs.image.image.locateDataDirectory')
    def test_resize_exception(self, mock_ldd):
        'Test throwing an exception when GSImage._get_resized_image is called'
        mock_ldd.return_value = self.dataDir
        width = 640
        height = 480

        logging.getLogger('gs.image').addHandler(logging.NullHandler())
        with patch.object(self.image, '_get_resized_img') as mock_gri:
            mock_gri.side_effect = IOError('Ethyl the frog')
            r = self.image.get_cache_name(width, height)
            i = self.image.get_resized(width, height)

        self.assertIs(None, r)
        self.assertIs(self.image, i)


class GSImagePNGTest(GSITest):

    def setUp(self):
        self.dataDir = mkdtemp()
        self.image = self.load_image('warty-final-ubuntu.png')

    def tearDown(self):
        rmtree(self.dataDir)

    def test_resize(self):
        width = 640
        height = 480
        r = self.get_resized(width, height)

        self.assertEqual(width, r.width)
        self.assertEqual(height, r.height)

    def test_content_type(self):
        width = 640
        height = 480
        r = self.get_resized(width, height)

        self.assertEqual('image/png', r.contentType)
        self.assertEqual(self.image.contentType, r.contentType)


class GSImageGIFTest(GSITest):
    def setUp(self):
        self.dataDir = mkdtemp()
        self.image = self.load_image('grypaws.gif')

    def tearDown(self):
        rmtree(self.dataDir)

    def test_no_resize(self):
        'This should not actually change the image size, since it is already smaller'
        width = height = 94
        r = self.get_resized(width, height)

        self.assertEqual(width, r.width)
        self.assertEqual(height, r.height)

    def test_force_resize(self):
        'The aspect ratio should still be maintained with a forced-resize'
        width = 640
        height = 480
        r = self.get_resized(width, height, only_smaller=False)

        self.assertEqual(height, r.width)  # Yes, the width
        self.assertEqual(height, r.height)

    def test_aspect_odd(self):
        'Test switching off maintaining the aspect ratio, too'
        width = 640
        height = 480
        r = self.get_resized(width, height, maintain_aspect=False, only_smaller=False)

        self.assertEqual(width, r.width)
        self.assertEqual(height, r.height)


class GSImageWideTest(GSITest):
    def setUp(self):
        self.dataDir = mkdtemp()
        self.image = self.load_image('wide.png')

    def tearDown(self):
        rmtree(self.dataDir)

    def test_resize(self):
        'Test that making a wide-and-short image smaller works'
        width = height = 190
        r = self.get_resized(width, height)

        self.assertEqual(width, r.width)
        self.assertEqual(1, r.height)
