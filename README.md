# Bump Anything

*Copyright 2019 Caleb Evans*  
*Released under the MIT license*

Bump Anything is a command-line utility for incrementing the version  It serves
as a more-flexible alternative to `npm version` and similar tools because
Bump Anything can handle any arbitrary text file and has built-in support for
different types of projects.

## Features

- Bump the version number in any arbitrary file
- Supports most project types (if no paths are supplied, automatically detects `package.json` in Node, `setup.py` in Python, WordPress themes, etc.)

## Installation

Bump Anything requires Python 3.4 or newer to run, so please ensure you have it
installed.

```sh
pip install bump-anything
```

## Usage

Bump Anything exposes a `bump` command to your shell. The only required argument
is a keyword indicating how you want to increment each version. It can be either
`major`, `minor`, or `patch`.


```
bump major
```

```
bump minor
```

```
bump patch
```

With this syntax, Bump Anything will do its best to find the relevant files to
bump. However, Bump Anything can also accept an optional list of one or more
file paths whose versions to bump. Only the first occurrence of the version
field in each file will be updated.

```
bump minor subdir/myfile1.txt subdir/myfile2.txt
```
