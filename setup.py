# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

from version import get_version

setup(name='gs.image',
      version=get_version(),
      description="Image manipulation and display on GroupServer",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Web Environment",
          "Framework :: Zope2",
          "Intended Audience :: Developers",
          "License :: Other/Proprietary License",
          "Natural Language :: English",
          "Operating System :: POSIX :: Linux"
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='image groupserver',
      author='Richard Waid',
      author_email='richard@onlinegroups.net',
      url='http://www.groupserver.org/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gs'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          'Pillow',  # Provides PIL
          'zope.app.file',
          'zope.schema',
          'Products.XWFCore',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
