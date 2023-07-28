#!/usr/bin/env python3

import argparse
import os
import os.path
import re
import sys
from functools import partial

import semver

# The regular expression pattern used to match the version to be incremented
# within any given file of any type
VERSION_PATT = r"({key}\s*[=:]\s*([\"\']?)){value}(\3\s*)".format(
    key=r'(["\']?)version\2',
    value=r"(?P<version>(?P<semver>\d+\.\d+\.\d+)[a-z0-9\-\+\.]*)",
)


def get_auto_detectable_file_names():
    # Get the name of the project directory
    project_name = os.path.basename(os.getcwd())
    return (
        # If a Node project
        "package.json",
        # If Node project contains a lockfile
        "package-lock.json",
        # If a WordPress theme
        "style.css",
        # If a WordPress plugin
        "{}.php".format(project_name),
        # If a Python project
        "setup.py",
        "pyproject.toml",
    )


# Increment the major, minor, or patch part of the given version string and
# return the incremented version
def bump_version(version, increment_type):
    if increment_type == "major":
        return semver.bump_major(version)
    elif increment_type == "minor":
        return semver.bump_minor(version)
    elif increment_type == "patch":
        return semver.bump_patch(version)


# The callback function for the substitution call that locates and increments
# the version in-place
def replace_version(increment_type, file_path, version_match):
    old_version = version_match.group("version")
    semantic_version = version_match.group("semver")
    new_version = bump_version(semantic_version, increment_type)
    print("{}: {} -> {}".format(file_path, old_version, new_version))
    return "".join((version_match[1], new_version, version_match[6]))


# Locate the version number in the specified file and increment it
def bump_version_for_file(increment_type, file_path):
    with open(file_path, "r+") as file:
        file_contents = file.read()
        new_file_contents = re.sub(
            VERSION_PATT,
            partial(replace_version, increment_type, file_path),
            file_contents,
            flags=re.IGNORECASE,
            count=1,
        )
        if new_file_contents != file_contents:
            file.truncate(0)
            file.seek(0)
            file.write(new_file_contents)
        else:
            print("{}: could not find version info".format(file_path), file=sys.stderr)


# Find files in the current project (according to the project type) that
# include version information
def get_default_file_paths():
    return (
        file_name
        for file_name in get_auto_detectable_file_names()
        if os.path.exists(file_name)
    )


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("increment_type", choices=("major", "minor", "patch"))
    parser.add_argument(
        "file_paths", metavar="file", nargs="*", type=os.path.expanduser
    )
    return parser.parse_args()


def main():
    args = parse_cli_args()
    if args.file_paths:
        file_paths = args.file_paths
    else:
        file_paths = get_default_file_paths()
    if not args.file_paths:
        print("cannot locate file(s) to bump", file=sys.stderr)
        sys.exit(1)
    for file_path in file_paths:
        try:
            bump_version_for_file(
                file_path=file_path, increment_type=args.increment_type
            )
        except FileNotFoundError:
            print("{}: file not found".format(file_path), file=sys.stderr)


if __name__ == "__main__":
    main()
