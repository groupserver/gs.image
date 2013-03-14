# -*- coding: utf-8 -*-
from os.path import isfile
from image import GSImage
from utils import thumbnail_img_square


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
            img = self._get_resized_img(size)
            # TODO Ticket 663
            # <https://projects.iopen.net/groupserver/ticket/663>
            img.save(cache_name, self.pilImage().format)
            retval = cache_name
        return retval

    def _get_resized_img(self, size):
        i = self.pilImage()
        retval = thumbnail_img_square(i, size)
        return retval
