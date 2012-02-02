from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='thumbor-dumper',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Mike Lewis',
      author_email='mikelikespie@gmail.com',
      url='http://lolrus.org',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          "tornado>=2.1.1",
          "thumbor>=2.3.0"
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      thumbor-dumper = thumbordumper.server:main
      """,
      )
