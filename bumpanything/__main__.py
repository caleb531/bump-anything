#!/usr/bin/env python3

import argparse
import os
import os.path
import re
import sys
from functools import partial

import semver

import bumpanything.git as git
from bumpanything.file_result import FileResult

# The regular expression pattern used to match the version to be incremented
# within any given file of any type
VERSION_PATT = r"({key}\s*[=:]\s*([\"\']?)){value}(\3\s*)".format(
    key=r'(["\']?)version\2',
    value=r"(?P<version>\d+\.\d+\.\d+[a-z0-9\-\+\.]*)",
)

# The valid types of increments you could make to a semantic version, and the
# functions they map to
INCREMENT_TYPES = {
    "major": semver.bump_major,
    "minor": semver.bump_minor,
    "patch": semver.bump_patch,
    "prerelease": semver.bump_prerelease,
}


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
        "setup.cfg",
        "pyproject.toml",
        "Cargo.toml",
    )


# Increment the major, minor, or patch part of the given version string and
# return the incremented version
def bump_version(version, version_specifier):
    if version_specifier in INCREMENT_TYPES.keys():
        return INCREMENT_TYPES[version_specifier](version)
    else:
        # If we are not incrementing the version using one of the above
        # commands, we can assume the version specified is the explicit new
        # version to use
        return version_specifier


# The callback function for the substitution call that locates and increments
# the version in-place
def replace_version(version_specifier, version_match):
    return "".join((version_match[1], version_specifier, version_match[5]))


# Replace the version in the given file contents with the version matching the
# given version specifier
def replace_version_in_file_contents(file_contents, version_specifier):
    version_matches = re.search(VERSION_PATT, file_contents)
    if not version_matches:
        return (None, None, None)
    current_version = version_matches.group("version")
    new_version = bump_version(current_version, version_specifier)
    new_file_contents = re.sub(
        VERSION_PATT,
        partial(replace_version, new_version),
        file_contents,
        flags=re.IGNORECASE,
        count=1,
    )
    return (current_version, new_version, new_file_contents)


# Locate the version number in the specified file and increment it
def bump_version_for_file(version_specifier, file_path):
    try:
        with open(file_path, "r+", newline="") as file:
            file_contents = file.read()
            (
                current_version,
                new_version,
                new_file_contents,
            ) = replace_version_in_file_contents(file_contents, version_specifier)
            if not current_version:
                return (False, None, None)
            if new_file_contents == file_contents:
                return (False, None, None)
            file.truncate(0)
            file.seek(0)
            file.write(new_file_contents)
            print("{}: {} -> {}".format(file_path, current_version, new_version))
            return (True, current_version, new_version)
    except FileNotFoundError:
        print("{}: file not found".format(file_path), file=sys.stderr)
        return (False, None, None)


# Find files in the current project (according to the project type) that
# include version information
def get_default_file_paths():
    return [
        file_name
        for file_name in get_auto_detectable_file_names()
        if os.path.exists(file_name)
    ]


def abort_if_version_mismatch(file_results):
    if len(set(result.new_version for result in file_results)) > 1:
        print(
            "Aborting commit because not all bumped versions are equal", file=sys.stderr
        )
        sys.exit()


def bump_version_for_files(file_paths, version_specifier):
    file_results = []
    for file_path in file_paths:
        did_version_change, current_version, new_version = bump_version_for_file(
            file_path=file_path, version_specifier=version_specifier
        )
        if did_version_change:
            file_results.append(
                FileResult(
                    file_path=file_path,
                    current_version=current_version,
                    new_version=new_version,
                )
            )
    return file_results


def handle_git_operations(
    file_results, commit_message, tag_name=None, should_tag=False
):
    if not git.is_in_git_repository():
        return
    abort_if_version_mismatch(file_results)
    changed_result_paths = [result.file_path for result in file_results]
    git.add(changed_result_paths)
    print(f"Staging {', '.join(changed_result_paths)}")
    did_commit = git.commit(commit_message)
    if not did_commit:
        print("Commit failed; aborting")
        return
    if not should_tag:
        return
    did_tag = git.tag(tag_name)
    if not did_tag:
        return
    print(f"Tagging commit as {tag_name}")


def version_specifier(arg_value):
    # Strip out 'v' prefix if included in the version specifier
    arg_value = re.sub(r"^v", "", arg_value)
    if arg_value in INCREMENT_TYPES.keys() or semver.Version.is_valid(arg_value):
        return arg_value
    else:
        raise argparse.ArgumentTypeError(
            "invalid version specifier (must be a valid semantic version)"
        )


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("version_specifier", type=version_specifier)
    parser.add_argument(
        "file_paths",
        metavar="file",
        nargs="*",
        type=os.path.expanduser,
        default=get_default_file_paths(),
    )
    parser.add_argument("--no-commit", "-n", action="store_true")
    parser.add_argument("--no-tag", action="store_true")
    parser.add_argument(
        "--commit-message", "-m", default="Prepare v{new_version} release"
    )
    parser.add_argument("--tag-name", "-t", default="v{new_version}")
    return parser.parse_args()


def main():
    args = parse_cli_args()
    file_results = bump_version_for_files(args.file_paths, args.version_specifier)
    if not file_results:
        print("No files updated")
        return
    if not args.no_commit:
        new_version = file_results[0].new_version
        handle_git_operations(
            file_results=file_results,
            commit_message=args.commit_message.format(new_version=new_version),
            tag_name=args.tag_name.format(new_version=new_version),
            should_tag=not args.no_tag,
        )


if __name__ == "__main__":
    main()
