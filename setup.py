#!/usr/bin/env python
# coding=utf-8

from setuptools import setup


# Get long description (used on PyPI project page)
def get_long_description():
    with open('README.md', 'r') as readme_file:
        return readme_file.read()


setup(
    name='bump-anything',
    version='1.0.4',
    description='A CLI utility for bumping the version of any file type',
    long_description=get_long_description(),
    url='https://github.com/caleb531/bump-anything',
    author='Caleb Evans',
    author_email='caleb@calebevans.me',
    license='MIT',
    keywords='semver semantic version bump increment',
    py_modules=['bump'],
    install_requires=[
        'semver >= 2, < 3'
    ],
    entry_points={
        'console_scripts': [
            'bump=bump:main'
        ]
    }
)
