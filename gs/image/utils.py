
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
from __future__ import unicode_literals, division
from PIL import Image


def rgba(image):
    '''Try and convert the image to RGBA '''
    retval = image
    if (image.mode not in ('RGB', 'RGBA', 'RGBX', 'CMYK')):
        try:
            retval = image.convert('RGBA')
        except:
            retval = image
    return retval


def thumbnail_img(i, x, y, method=Image.ANTIALIAS):
    '''Create a new image thumbnail, preserving the aspect ratio.

:param PIL.Image i: The image to thumbnail
:param int x: The maximum width
:param int y: The maximum height
:param method:  The scaling method to use
:returns: A new scaled image
:rtype: :class:`PIL.Image`

With thanks to kevin@cazabon.com:
<http://mail.python.org/pipermail/image-sig/2006-January/003724.html>'''
    image = rgba(i)

    imAspect = image.size[0] / image.size[1]
    outAspect = x / y
    if imAspect >= outAspect:
        #set to maxWidth x maxWidth/imAspect
        height = int((x / imAspect) + 0.5)
        height = height if (height > 0) else 1
        img = image.resize((x, height), method)
    else:
        #set to maxHeight*imAspect x maxHeight
        img = image.resize((int((y * imAspect) + 0.5), y), method)

    if img.mode != i.mode:
        # Change the image back to the original mode before saving
        img = img.convert(i.mode)
    return img


def thumbnail_img_noaspect(i, x, y, method=Image.ANTIALIAS):
    '''Create a new image thumbnail, ignoring the aspect ratio.

:param PIL.Image i: The image to thumbnail
:param int x: The maximum width
:param int y: The maximum height
:param method:  The scaling method to use
:returns: A new scaled image
:rtype: :class:`PIL.Image`'''
    image = rgba(i)
    img = image.resize((x, y), method)
        # Change the image back to the original mode before saving
    if img.mode != i.mode:
        img = img.convert(i.mode)
    return img


def thumbnail_img_square(i, size, method=Image.ANTIALIAS):
    '''Create a square version of the thumbnail image

:param PIL.Image i: The image to thumbnail
:param int size: The maximum size
:param method:  The scaling method to use
:returns: A new scaled image
:rtype: :class:`PIL.Image`

A square-image is created by scaling the short axis to the new size, leaving the long axis
unconstrained, and then cropping the image.'''
    origWidth, origHeight = i.size

    if origHeight <= origWidth:
        scaledImage = thumbnail_img(i, origWidth, size)
    else:
        scaledImage = thumbnail_img(i, size, origHeight)
    # Truncate the long axis to the new size.
    box = (0, 0, size, size)

    retval = scaledImage.crop(box)
    return retval
