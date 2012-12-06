# -*- coding: utf-8 -*-
from zope.schema import Int
from zope.app.file.interfaces import IImage


class IGSImage(IImage):

    def get_resized(x, y, maintain_aspect=True):
        u"""Resize an image

        DESCRIPTION
            This does not change the GSImage instance, since we may
            want to resize a number of times.

        ARGUMENTS
            x: Width of the new image
            y: Height of the new image
            maintain_aspect: Force the aspect ratio to be maintained
            only_spaller: Only shrink the size. --=mpj17=--?

        RETURNS
            A GSImage instance of the resized image.

        """
        pass

    width = Int(title=u'Width',
        description=u'The width of the image, for Zope 2',
        required=False,
        default=0,
        min=0)

    height = Int(title=u'Height',
        description=u'The height of the image, for Zope 2',
        required=False,
        default=0,
        min=0)
