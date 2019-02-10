#!/usr/bin/env python
# coding=utf-8

from setuptools import setup


# Get long description (used on PyPI project page)
def get_long_description():
    try:
        # Use pandoc to create reStructuredText README if possible
        import pypandoc
        return pypandoc.convert_file('README.md', 'rst')
    except Exception:
        return None


setup(
    name='bump-anything',
    version='1.0.1',
    description='A CLI utility for bumping the version of any file type',
    long_description=get_long_description(),
    url='https://github.com/caleb531/bump-anything',
    author='Caleb Evans',
    author_email='caleb@calebevans.me',
    license='MIT',
    keywords='semver semantic version bump increment',
    py_modules=['bump'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'bump=bump:main'
        ]
    }
)
