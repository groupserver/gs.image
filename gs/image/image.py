# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
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
import md5
import os
from StringIO import StringIO
from zope.app.file.image import getImageInfo
from PIL import Image as PILImage, ImageFile
from Products.XWFCore.XWFUtils import locateDataDirectory
from .utils import thumbnail_img, thumbnail_img_noaspect


class GSImage(object):

    def __init__(self, data):
        if type(data) == file:
            self.data = data.read()
        else:
            self.data = data
        self.fromCache = False

        self.data_dir = locateDataDirectory("groupserver.GSImage.cache")
        self.md5sum = md5.new(StringIO(self.data).read()).hexdigest()
        self.base_path = os.path.join(self.data_dir, self.md5sum)

    @property
    def contentType(self):
        assert isinstance(self._contentType, str)
        return self._contentType

    def _getData(self):
        assert isinstance(self._data, str)
        return self._data

    def _setData(self, data):
        '''Set  the image data.

        Nicked from the Zope 3 Image and File classes.

        ARGUMENTS
          data:   A string containing the data to set.

        RETURNS
          None.

        SIDE EFFECTS
          Sets "self._data" to contain the data.
          Sets "self._size" to the length of the data.
          Sets "self._contentType" to the content type of the image.
          Sets "self._width" to the width of the image.
          Sets "self._height" to the height of the image.'''

        assert isinstance(data, str),\
            'Data is a {0} not a string'.format(type(data))
        self._data = data
        self._size = len(data)
        self._contentType, self._width, self._height = getImageInfo(data)
        self._pilImage = None

        # assert self._data == data  # --=mpj17=-- performance issue
        assert isinstance(self._data, str)
        assert isinstance(self._size, int)
        assert isinstance(self._contentType, str)
        assert isinstance(self._width, int)
        assert isinstance(self._height, int)

    data = property(_getData, _setData)

    def getSize(self):
        assert isinstance(self._size, int)
        return self._size

    def getImageSize(self):
        assert isinstance(self._width, int)
        assert isinstance(self._height, int)
        return (self._width, self._height)

    @property
    def width(self):
        assert isinstance(self._width, int)
        return self._width

    @property
    def height(self):
        assert isinstance(self._height, int)
        return self._height

    def pilImage(self):
        if self._pilImage is None:
            data_reader = StringIO(self._data)
            self._pilImage = PILImage.open(data_reader)
        return self._pilImage

    def get_resized(self, x, y, maintain_aspect=True, only_smaller=True,
                    return_cache_path=False):
        """ Get the resized image, or the path to the resized image.

        """
        retval = None
        cache_name = self.get_cache_name(x, y, maintain_aspect,
                                         only_smaller)
        if return_cache_path:
            # possibly None if no resizing was done
            retval = cache_name
        elif cache_name:
            retval = GSImage(file(cache_name, 'rb'))
        else:
            retval = self

        return retval

    def get_cache_name(self, x, y, maintain_aspect=True, only_smaller=True):
        """SIDE EFFECTS
            Caches the image data if it scales the image
        """
        cache_name = self.base_path + '%sx%sx%s' % (x, y, maintain_aspect)
        if (only_smaller and (self._height <= y) and (self._width <= x)):
            retval = None
        elif os.path.isfile(cache_name):
            retval = cache_name
        else:
            img = self._get_resized_img(x, y, maintain_aspect)
            self.save_img_to_cache(img, cache_name)
            retval = cache_name
        return retval

    def _get_resized_img(self, x, y, maintain_aspect):
        i = self.pilImage()
        if maintain_aspect:
            retval = thumbnail_img(i, x, y)
        else:
            retval = thumbnail_img_noaspect(i, x, y)
        return retval

    def save_img_to_cache(self, img, cache_name):
        imgFormat = self.pilImage().format
        if imgFormat == 'JPEG':
            # See Ticket 663 <https://redmine.iopen.net/issues/663>
            m = min(img.size)
            if m <= 50:
                quality = 40  # You got 40px? No quality for you.
                progressive = False
            elif m <= 200:
                quality = 60  # Medium quality.
                progressive = False
            else:  # > 200
                # This is *high* according to the JPEG standard.
                quality = 75
                progressive = True
            try:
                img.save(cache_name, imgFormat, quality=quality,
                         progressive=progressive, optimize=True)
            except IOError:
                # --=mj17=-- Increase the size of the "block" used by
                # libjpeg so we can scale stupidly large images, and retain
                # progressive rendering.
                # http://stackoverflow.com/questions/6788398/
                s = img.size[0] * img.size[1]
                ImageFile.MAXBLOCK = s
                img.save(cache_name, imgFormat, quality=quality,
                         progressive=progressive, optimize=True)
        else:
            img.save(cache_name, imgFormat)

    def _clean_cache(self):
        """ Tidy up files that have been saved in association with this
        image."""
        for fname in os.listdir(self.data_dir):
            if fname.find(self.md5sum) == 0:
                os.remove(os.path.join(self.data_dir, fname))
