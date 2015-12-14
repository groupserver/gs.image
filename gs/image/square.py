# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################
from __future__ import absolute_import
from logging import getLogger
log = getLogger('gs.image')
from os.path import isfile
from .image import GSImage
from .utils import thumbnail_img_square


class GSSquareImage(GSImage):

    def __init__(self, data):
        super(GSSquareImage, self).__init__(data)

    def get_resized(self, size):
        """ Get the resized image"""
        retval = None
        cache_name = self.get_cache_name(size)
        if cache_name:
            retval = GSSquareImage(file(cache_name, 'rb'))
        else:
            retval = self

        return retval

    def get_cache_name(self, size):
        """SIDE EFFECTS
            Caches the image data if it scales the image
        """
        n = '{base}{size}x{size}xTrue'
        cache_name = n.format(base=self.base_path, size=size)
        if isfile(cache_name):
            retval = cache_name
        else:
            try:
                img = self._get_resized_img(size)
            except IOError as e:
                m = 'Failed to get the resized image for "{0}"'
                msg = m.format(self.base_path)
                log.error(msg)
                log.error(e)
                retval = None
            else:
                # TODO Ticket 663
                # <https://projects.iopen.net/groupserver/ticket/663>
                self.save_img_to_cache(img, cache_name)
                retval = cache_name
        return retval

    def _get_resized_img(self, size):
        i = self.pilImage()
        retval = thumbnail_img_square(i, size)
        return retval
