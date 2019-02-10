#!/usr/local/bin/python3

# The above shebang must not use /usr/bin/env, otherwise running this tool
# within an active virtualenv will fail

import argparse
import glob
import os
import os.path
import re
import semver
import sys
from contextlib import suppress
from functools import partial

# The regular expression pattern used to match the version to be incremented
# within any given file of any type
VERSION_PATT = r'({key}\s*[=:]\s*(["\']?)){value}(\3\s*)'.format(
    key=r'(["\']?)version\2',
    value=r'(?P<version>(?P<semver>\d+\.\d+\.\d+)[a-z0-9\-\+\.]*)')


# Increment the major, minor, or patch part of the given version string and
# return the incremented version
def bump_version(version, increment_type):
    if increment_type == 'major':
        return semver.bump_major(version)
    elif increment_type == 'minor':
        return semver.bump_minor(version)
    elif increment_type == 'patch':
        return semver.bump_patch(version)


# The callback function for the substitution call that locates and increments
# the version in-place
def replace_version(increment_type, file_path, version_match):
    old_version = version_match['version']
    semantic_version = version_match['semver']
    new_version = bump_version(semantic_version, increment_type)
    print('{}: {} -> {}'.format(file_path, old_version, new_version))
    return ''.join((
        version_match[1],
        new_version,
        version_match[6]))


# Locate the version number in the specified file and increment it
def bump_version_for_file(increment_type, file_path):
    with open(file_path, 'r+') as file:
        file_contents = file.read()
        new_file_contents = re.sub(
            VERSION_PATT,
            partial(replace_version, increment_type, file_path),
            file_contents,
            flags=re.IGNORECASE,
            count=1)
        if new_file_contents != file_contents:
            file.truncate(0)
            file.seek(0)
            file.write(new_file_contents)
        else:
            print('{}: could not find version info'.format(file_path),
                  file=sys.stderr)


# Retrieve the path to the nearest SuiteCommerce Advanced extension/theme
# directory
def get_sca_extension_dir():
    workspace_subdirs = glob.glob('Workspace/*/')
    with suppress(ValueError):
        workspace_subdirs.remove('Workspace/Extras/')
    if workspace_subdirs:
        return workspace_subdirs[0]
    else:
        print('cannot locate SCA extension/theme directory', file=sys.stderr)


# Find files in the current project (according to the project type) that
# include version information
def populate_file_paths(file_paths):
    # Get the name of the project directory
    project_name = os.path.basename(os.getcwd())
    # If a SuiteCommerce Advanced extension/theme
    if os.path.exists('Workspace'):
        file_paths.append(os.path.join(get_sca_extension_dir(),
                          'manifest.json'))
        return
    # If a Node project
    if os.path.exists('package.json'):
        file_paths.append('package.json')
    # If Node project contains a lockfile
    if os.path.exists('package-lock.json'):
        file_paths.append('package-lock.json')
    # If a WordPress theme
    if os.path.exists('style.css'):
        file_paths.append('style.css')
    # If a WordPress plugin
    if os.path.exists('{}.php'.format(project_name)):
        file_paths.append('{}.php'.format(project_name))
    # If a Python project
    if os.path.exists('setup.py'):
        file_paths.append('setup.py')


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'increment_type',
        choices=('major', 'minor', 'patch'))
    parser.add_argument(
        'file_paths',
        metavar='file',
        nargs='*',
        type=os.path.expanduser)
    return parser.parse_args()


def main():
    args = parse_cli_args()
    if not args.file_paths:
        populate_file_paths(args.file_paths)
    if not args.file_paths:
        print('cannot locate file(s) to bump', file=sys.stderr)
        sys.exit(1)
    for file_path in args.file_paths:
        try:
            bump_version_for_file(
                file_path=file_path,
                increment_type=args.increment_type)
        except FileNotFoundError:
            print('{}: file not found'.format(file_path), file=sys.stderr)


if __name__ == '__main__':
    main()
