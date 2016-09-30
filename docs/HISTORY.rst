Changelog
=========

3.1.1 (2016-09-30)
------------------

* Ensuring scaled images are always at least 1 pixel wide and 1
  pixel high, with thanks to Donald Winship for reporting `the
  issue with scaling`_

.. _the issue with scaling:
   http://groupserver.org/r/topic/1aK6lIYi2YaN6WLmAHM3nL

3.1.0 (2016-04-11)
------------------

* Making :class:`gs.image.GSImage.data` accept either strings or files
* Adding more unit tests

3.0.4 (2015-12-14)
------------------

* Ensuring an ``IOError`` when reading the cache is handled
* Updating all the unit tests, switching from a ``doctest``
* Updating the doc-strings
* Pointing at GitHub_ as the main repository

.. _GitHub: https://github.com/groupserver/gs.image

3.0.3 (2014-09-17)
------------------

* Naming all the ReStructuredText files as such

3.0.2 (2014-01-23)
------------------

* Switching to ``absolute_import``

3.0.1 (2013-09-19)
------------------

* Allowing large progressive images to scale

3.0.0 (2013-03-26)
------------------

* Added support for square images

2.0.2 (2012-12-06)
------------------

* Cleaning up the code (PEP-8)

2.0.1 (2012-10-17)
------------------

* Switching from ``PIL`` to `Pillow`_ as the main dependency

.. _Pillow: https://pillow.readthedocs.io/

2.0.0 (2011-02-15)
------------------

* Moving the Image page to `gs.group.messages.image`_

.. _gs.group.messages.image:
   https://github.com/groupserver/gs.group.messages.image

1.3.3 (2010-12-14)
------------------

* Updating the Image page so it uses arrows in the navigation
  links, and better formatting of the file-name

1.3.2 (2010-08-05)
------------------

* Fixing the ``GSImage.get_resized`` method
* Fixing the unit tests

1.3.1 (2010-07-09)
------------------

* Fixing the traversal code

1.3.0 (2009-10-20)
------------------

* Adding support for only getting the name of a cached file
* Fixing the metadata

1.2.1 (2009-09-28)
------------------

* Updating some wording
* Updating the tests

1.2.0 (2009-05-29)
------------------

* Adding a method for getting the name of the cached-file off
  disc

1.1.4 (2009-05-15)
------------------

* Dropping the Zope Image super-class, as it is persistent
* Fixing the MD5 calculation

1.1.3 (2009-05-01)
------------------

* Ensuring that ``text/html`` is used for the page-templates

1.1.2 (2008-10-02)
------------------

* Switching to anti-aliasing

1.1.1 (2008-09-26)
------------------

* Scaling the images *after* converting them to RGBA mode first

1.1.0 (2008-09-04)
------------------

* Moving code from ``GSImage`` to this product
* Using the Zope 3 image code for scaling

1.0.0 (2008-08-29)
------------------

Initial version.

..  LocalWords:  Changelog
