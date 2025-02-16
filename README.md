# Bump Anything

*Copyright 2019-2025 Caleb Evans*  
*Released under the MIT license*

[![tests](https://github.com/caleb531/bump-anything/actions/workflows/tests.yml/badge.svg)](https://github.com/caleb531/bump-anything/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/caleb531/bump-anything/badge.svg?branch=main)](https://coveralls.io/r/caleb531/bump-anything?branch=main)

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

```sh
bump 2.3.4
```

```sh
bump v2.3.4 # same as `bump 2.3.4`
```

With this syntax, Bump Anything will do its best to find the relevant files to
bump. However, Bump Anything can also accept an optional list of one or more
file paths whose versions to bump. Only the first occurrence of the version
field in each file will be updated.

```sh
bump minor subdir/myfile1.json subdir/myfile2.toml
```

### Git Integration

The `bump` command will automatically create a tagged commit if the current
directory is a Git repository. Only the files that have been modified by `bump`
will be staged.

### Custom commit message

You can explicitly specify the commit message with `--commit-message` or `-m`.
The default is `Prepare v<new_version> release`. You can use the `{new_version}`
placeholder to represent the new version (without any prefix).

```sh
bump --commit-message 'Release v{new_version}' major
```

```sh
bump -m 'Release v{new_version}' major
```

### Custom tag name

You can explicitly specify the tag name with `--tag-name` or `-t` (default:
`v<new_version>`). You can use the `{new_version}` placeholder to represent the
new version (without any prefix).

```sh
bump --tag-name 'release/{new_version}' patch
```

```sh
bump -t 'release/{new_version}' patch
```

### Disabling committing and/or tagging

If you do not wish for `bump` to automatically create a commit and tag, you can
pass the `--no-commit` flag (alias: `-n`):

```sh
bump --no-commit minor
```

```sh
bump -n minor
```

### Disabling tagging only

If you wish to disable the automatic tag creation but still create a commit, you
can pass the `--no-tag` flag:

```sh
bump --no-tag patch
```

## Auto-Detected Files

- `package.json` (Node)
- `package-lock.json` (Node)
- `setup.py` (Python)
- `setup.cfg` (Python)
- `pyproject.toml` (Python)
- `style.css` (WordPress Theme)
- `Cargo.toml` (Rust package manifest)
- `<cwd name>.php` (WordPress Plugin)
