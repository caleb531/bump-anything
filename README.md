# Bump Anything

*Copyright 2019-2023 Caleb Evans*  
*Released under the MIT license*

Bump Anything is a command-line utility for incrementing the version  It serves
as a more-flexible alternative to `npm version` and similar tools because
Bump Anything can handle any arbitrary text file and has built-in support for
different types of projects.

## Features

- Bump the version number in any arbitrary file
- Supports most project types (if no paths are supplied, automatically detects
  `package.json` in Node, `setup.py` or `pyproject.toml` in Python, `style.css`
  for WordPress themes, etc.)

## Installation

Bump Anything requires Python 3.9 or newer to run, so please ensure you have it
installed.

```sh
pip3 install bump-anything
```

## Usage

Bump Anything exposes to your shell a `bump-anything` command (also aliased to
`bump`). The only required argument is a keyword indicating how you want to
increment each version. It can be either `major`, `minor`, or `patch`.


```sh
bump major # 1.2.3 -> 2.0.0
```

```sh
bump minor # 1.2.3 -> 1.3.0
```

```sh
bump patch # 1.2.3 -> 1.2.4
```

```sh
bump prerelease # 1.2.3-beta.1 -> 1.2.3-beta.2
```

With this syntax, Bump Anything will do its best to find the relevant files to
bump. However, Bump Anything can also accept an optional list of one or more
file paths whose versions to bump. Only the first occurrence of the version
field in each file will be updated.

```
bump minor subdir/myfile1.json subdir/myfile2.toml
```

## Auto-Detected Files

- `package.json` (Node)
- `package-lock.json` (Node)
- `setup.py` (Python)
- `pyproject.toml` (Python)
- `style.css` (WordPress Theme)
- `<cwd name>.php` (WordPress Plugin)
