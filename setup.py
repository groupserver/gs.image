from setuptools import setup, find_packages
import os

version = '1.0a2'

setup(name='gs.image',
      version=version,
      description="Image manipulation and display on GroupServer",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
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
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )