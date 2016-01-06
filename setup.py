#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
  from setuptools import setup
except Exception:
  from distutils.core import setup

setup(
  name = 'dddUtils',
  version = '0.0.3',
  license = 'MIT',
  author = '@inconvergent',
  packages = ['dddUtils'],
  install_requires = ['numpy>=1.8.2'],
  zip_safe = True,
  # package_dir = {'dddUtils': 'src/dddUtils'}
)

