# coding=utf-8
##############################################################################
#
# Copyright (c) 2004, 2005 Zope Corporation and Contributors.
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
"""Size adapters for testing

$Id: test_size.py 61072 2005-10-31 17:43:51Z philikon $
"""
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

def test_gsimage():
    """
    Test GSImage and adapters

    Set up:
      >>> from zope.app.testing.placelesssetup import setUp, tearDown
      >>> setUp()
      >>> import md5
      >>> import os
      >>> import Products.Five
      >>> import gs.image
      >>> from zope.app.file.image import Image
      >>> from gs.image import image
      >>> from gs.image.interfaces import IGSImage
      
      >>> from Products.Five import zcml

      >>> zcml.load_config('meta.zcml', Products.Five)
      >>> zcml.load_config('permissions.zcml', Products.Five)
      >>> zcml.load_config('configure.zcml', gs.image)

      >>> _prefix = os.path.dirname(gs.image.tests.__file__)

      >>> image = Image(file(os.path.join(_prefix, 'whirlpool.jpg')))
      >>> original_width, original_height = image.getImageSize()
      >>> original_aspect = float(original_width)/float(original_height)
      
    Setup the adapter
      >>> adapted_image = IGSImage(image)
      
    Clean up the cache first
      >>> adapted_image._clean_cache()
      
    Resize an image -- do it twice, the second time should have been cached
      >>> width, height = (640, 480)
      >>> resized_image = adapted_image.get_resized(width, height)
      >>> resized_image.fromCache
      False
      >>> resized_image.contentType
      'image/jpeg'
      
      >>> resized_image = adapted_image.get_resized(width, height)
      >>> resized_image.fromCache
      True
      >>> resized_image.contentType
      'image/jpeg'
    
    Check aspect ratio
      >>> resized_image.height, resized_image.width
      (400, 640)
      >>> original_height >= resized_image.height
      True
      >>> original_width >= resized_image.width
      True
      >>> new_aspect = float(resized_image.width)/float(resized_image.height)
      >>> original_aspect == new_aspect
      True
            
    Switch around the height and width to double check that the aspect ratios
    are being maintained
    
      >>> height, width = width, height
      >>> resized_image = adapted_image.get_resized(width, height)
      >>> original_height >= resized_image.height
      True
      >>> original_width >= resized_image.width
      True
      
      >>> new_aspect = float(resized_image.width)/float(resized_image.height)
      >>> original_aspect == new_aspect
      True
      
      >>> height, width = width, height
    
      >>> adapted_image._clean_cache()
      
    Test PNG support
      >>> image = Image(file(os.path.join(_prefix, 'warty-final-ubuntu.png')))
      >>> adapted_image = IGSImage(image)
      >>> adapted_image._clean_cache()
      
      >>> resized_image = adapted_image.get_resized(width, height)
      >>> resized_image.height, resized_image.width
      (480, 640)
    
    Quick thumbnail test
      >>> resized_image = adapted_image.get_resized(80, 60)
      >>> resized_image.height, resized_image.width
      (60, 80)
    
      >>> adapted_image._clean_cache()
      
    Test GIF support
      >>> image = Image(file(os.path.join(_prefix, 'grypaws.gif')))
      >>> adapted_image = IGSImage(image)
      >>> adapted_image._clean_cache()

    This should not actually change the image size, since it is already smaller
      >>> resized_image = adapted_image.get_resized(width, height)
      >>> resized_image.height, resized_image.width
      (94, 94)
    
    Unless we're daft and do this, in which case the aspect ratio should still be
    maintained at least
      >>> resized_image = adapted_image.get_resized(width, height, only_smaller=False)
      >>> resized_image.height, resized_image.width
      (480, 480)
    
    Or we do something really daft, and switch off maintaining the aspect ratio
    too
      >>> resized_image = adapted_image.get_resized(width, height,
      ...                            maintain_aspect=False, only_smaller=False)
      >>> resized_image.height, resized_image.width
      (480, 640)
    
    Clean up:
      >>> tearDown()
      
    """

def test_suite():
    from Testing.ZopeTestCase import ZopeDocTestSuite
    return ZopeDocTestSuite()

if __name__ == '__main__':
    framework()
