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
from __future__ import unicode_literals
from zope.schema import Int
from zope.app.file.interfaces import IImage


class IGSImage(IImage):

    def get_resized(x, y, maintain_aspect=True):
        """Resize an image

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

    width = Int(title='Width',
        description='The width of the image, for Zope 2',
        required=False,
        default=0,
        min=0)

    height = Int(title='Height',
        description='The height of the image, for Zope 2',
        required=False,
        default=0,
        min=0)
