#!/usr/bin/python3

try:
  from setuptools import setup
except Exception:
  from distutils.core import setup

setup(
  name = 'dddUtils',
  version = '0.0.1',
  license = 'MIT',
  author = '@inconvergent',
  packages = ['dddUtils'],
  zip_safe = True,
  package_dir={'dddUtils': 'src/dddUtils'}
  #install_requires = []
)

