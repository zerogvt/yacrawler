# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='yacrawler',
    version='0.1.0',
    description='yet another crawler',
    long_description=readme,
    author='Vasileios G',
    author_email='',
    url='https://github.com/zerogvt/yacrawler',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

