#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(name='django-oscar-avalara',
      version='0.1.1',
      url='https://github.com/tangentlabs/django-oscar-avalara',
      author="Tangent Labs (part of Tangent Snowball)",
      author_email="oscar@tangentlabs.co.uk",
      description="Avalara integration for django-oscar",
      long_description=open('README.rst').read(),
      keywords="Taxes, Avalara",
      license='BSD',
      packages=find_packages(exclude=['sandbox*', 'tests*']),
      include_package_data=True,
      install_requires=[
          'django-oscar>=0.6,<1.0',
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
