#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(name='django-oscar-avalara',
      version='0.2',
      url='https://github.com/django-oscar/django-oscar-avalara',
      author="David Winterbottom",
      author_email="david.winterbottom@gmail.com",
      description="Avalara integration for django-oscar",
      long_description=open('README.rst').read(),
      keywords="Taxes, Avalara",
      license='BSD',
      packages=find_packages(exclude=['sandbox*', 'tests*']),
      include_package_data=True,
      install_requires=[
          'django-oscar>=1.0',
          'requests',
          'purl>=0.8',
      ],
      # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: Unix',
          'Programming Language :: Python']
      )
