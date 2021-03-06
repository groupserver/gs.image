============
``gs.image``
============
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Image support for GroupServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Authors: `Michael JasonSmith`_,
         Richard Waid
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-11-14
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

GroupServer_ displays images in many places, including on
profiles [#profiles]_, in posts [#posts]_, and on the Image page
[#image]_. This egg wraps some functions provided by PIL_ to
provide support to the other products for resizing and caching
images. The functionality of this product is primarily provided
by two classes:

* GSImage_ is used to resize and implicitly cache images. 
* The GSSquareImage_ class resizes and crops the images to ensure
  they are square, before implicitly caching the result.

The resizing is done by one of three utilities_.

``GSImage``
===========

The ``gs.image.GSImage`` class provides an application cache for
images. This means the computationally-expensive task of creating
a thumbnail only has to be done once. It also provides convenient
methods_ for integrating and resizing the image.

Constructor
-----------

::

 GSImage(data)

``data``:
  Either a ``file`` or a byte-array (string) containing the
  image.

Properties
----------

``data``:
  The image data.

``width``:
  The width of the image.

``height``:
  The height of the image.

``contentType``:
  The content type of the image (useful for setting the HTTP
  response).

Methods
-------

``getSize()``:
  Returns the size of the image in bytes.

``getImageSize()``:
  Returns a 2-tuple of ``(GSImage.width, GSImage.height)``.

``get_resized(x, y, maintain_aspect=True, only_smaller=True, return_cache_path=False)``:
  Returns a new ``GSImage``, with a maximum width of ``x`` and a
  maximum height of ``y``.

  * If ``maintain_aspect`` is ``True`` then the aspect ratio of
    the new image (``x/y``) will be the same as the aspect ratio
    of the old image.
  * If ``only_smaller`` is ``True`` then the image will be scaled
    only if it is smaller.
  * Finally [#command]_, if ``return_cache`` is ``True`` then the
    path to the file in the cache is returned, not the image (see
    `Side Effects`_ below).

Side Effects
------------

The main job of the ``GSImage`` class is to *implicitly* cache
the scaled image when ``get_resized`` is called. The cache is
located at
``{clientHome}/groupserver.data/groupserver.GSImage.cache``,
where ``clientHome`` is the directory of the GroupServer instance
(normally ``var/instance`` in the installation directory).

The file-name is made up of ``{md5}{width}x{height}x{maintainAspect}``:

* ``md5``: An MD5 Sum of the image data.
* ``width``: The width of the image.
* ``height``: The height of the image.
* ``maintainAspect``: If the aspect ratio was kept.

The cached image will be of the same type as the original image. However,
the quality_ may be set to a different value.

Quality
~~~~~~~

If the base image is a JPEG, then the quality of the image is set
depending on the size of the *smallest* dimension. The idea is
that the low quality is less noticeable at small sizes. For large
sizes progressive-rendering is turned on, so the time-to-glass is
reduced. The different quality settings at different sizes is as
follows:

================ =======
Size             Quality
================ =======
s <= 50px             40
50 < s <= 200px       60
s > 200px             75  
================ =======

If the base image is something other than a JPEG (such as a PNG)
then it is simply resized.

Examples
--------

Resize the image in ``fileName``, ensuring neither dimension is
more than 128px::

  f = file(fileName)
  i = GSImage(f)
  scaledImage = i.get_resized(128, 128)

Return a scaled image from a Zope page view by over-writing the
``__call__`` method::

    class MyImage(Products.Five.BrowserView):
        def __init__(self, context, request):
            super(MyImage, self).__init__(context, request)

        ...
    
        def __call__(self):
            f = file(self.fileName)
            i = GSImage(f)
            scaledImage = i.get_resized(128, 128)

            self.request.RESPONSE.setHeader('Content-Type',
                                            scaledImage.contentType)
            self.request.RESPONSE.setHeader('Content-Length',
                                            scaledImage.getSize())
            retval = scaledImage.data
            return retval


``GSSquareImage``
=================

The ``gs.image.GSSquareImage`` class resizes images, just like
the parent GSImage_ class, but all images are made square. It
inherits the same constructor_, and properties_ as its
parent. However, the `get_resized`_ method is different.

``get_resized``
---------------

Get a resized square image.

:Synopsis: ``get_resized(size)``

:Description: The ``get_resized`` method resizes the image, so
              neither the width nor the height will exceed the
              ``size``, and both will be the same. See
              `thumbnail_img_square`_ for more details on the
              algorithm used to do this.

:Arguments: ``size`` the maximum width and height of the image in
            pixels.

:Returns: A new ``GSSquareImage``.

Example
-------

Create a square image, 32 pixels on a side::

  f = file(fileName)
  i = GSSquareImage(f)
  scaledImage = i.get_resized(32)


Utilities
=========

Three utilities are provided 

#. `thumbnail_img`_ 
#. `thumbnail_img_noaspect`_
#. `thumbnail_img_square`_

``thumbnail_img``
-----------------

Create a thumbnail of an image.

:Synopsis: ``thumbnail_img(i, x, y, method=Image.ANTIALIAS)``

:Description: The ``thumbnail_img`` utility creates a new image, scaled
          down so the width will not exceed ``x``, and height will not
          exceed ``y``, and the aspect-ratio (``x/y``) will be
          maintained. It is similar to ``Image.thumbnail``, but it returns
          a new image, rather than working on the image in-place.

:Arguments: 
 
  ``i``:
    The PIL_ image to resize.

  ``x``: 
    The maximum width.

  ``y``:
    The maximum height.

  ``method``
    The scaling method.

:Returns: A new image. The width will not exceed ``x``, and height will not
          exceed ``y``, and the aspect-ratio (``x/y``) will be maintained.

Example
~~~~~~~

Scale a PIL image so neither dimension is more that 127px::

   i = PIL.Image.open(data)
   scaledImage = thumbnail_img(i, 127, 127)

``thumbnail_img_noaspect``
--------------------------

Create a thumbnail of an image, without maintaining the aspect ratio.

:Synopsis: ``thumbnail_img(i, x, y, method=Image.ANTIALIAS)``

:Description: The ``thumbnail_img_noaspect`` utility creates a new image,
          scaled down so the width will be ``x``, and height will be ``y``.

:Arguments: 
 
  ``i``:
    The image to resize.

  ``x``: 
    The width.

  ``y``:
    The height.

  ``method``
    The scaling method.

:Returns: A new image. The width be ``x``, and height will be ``y``.

``thumbnail_img_square``
------------------------

Create a square thumbnail image.

:Synopsis: ``thumbnail_img_square(i, size, method=Image.ANTIALIAS)``

:Description: The ``thumbnail_img_square`` method creates a square version
              of the original image.

              * First, it scales the image so the shortest axis is ``size``
                pixels, leaving the long axis unconstrained.

              * Second, it crops the image, so the long axis is ``size``
                pixels. The cropping is done from the top-left
                corner. (There may need to be a top-right version used when
                non-Roman scripts are introduced to GroupServer.)

:Arguments:

  ``i``:
    The image to resize.

  ``size``:
    The width and height of the new image, in pixels.

  ``method``
    The scaling method.

:Returns: A new image. The width will be ``size``, and height will be
          ``size``.

Authors
=======

Thanks to Kevin for the original code:
<http://mail.python.org/pipermail/image-sig/2006-January/003724.html>.

Resources
=========

- Code repository: https://github.com/groupserver/gs.image
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net/
.. _Michael JasonSmith: http://groupserver.org/p/mpj17/

.. [#profiles] See ``gs.profile.image.base`` for the profile-image code:
               <https://github.com/groupserver/gs.profile.image.base/>
.. [#posts] See ``gs.group.messages.post`` for the post-rendering code:
            <https://github.com/groupserver/gs.group.messages.post/>
.. [#image] See ``gs.group.messages.image`` for the Image page:
            <https://github.com/groupserver/gs.group.messages.image/>

.. _PIL: http://www.pythonware.com/library/pil/handbook/

.. [#command] The ``get_resized`` method is a good example of why
              command-coupling is a Bad Thing.

..  LocalWords:  resizes GSSquareImage getSize px resized ANTIALIAS mpj
..  LocalWords:  retval noaspect LocalWords resize
