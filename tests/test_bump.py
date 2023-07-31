#!/usr/bin/env python3

import unittest

from nose2.tools import params
from nose2.tools.decorators import with_setup, with_teardown

import bump_anything.__main__ as bump
from tests import create_mock_file, read_mock_file, set_up, tear_down
from tests.utils import redirect_stdout, use_cli_args

case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
@params(
    # Bump the major part of the version
    (("major", "foo.py"), "1.2.3", "2.0.0"),
    # Bump the minor part of the version
    (("minor", "foo.py"), "1.2.3", "1.3.0"),
    # Bump the patch part of the version
    (("patch", "foo.py"), "1.2.3", "1.2.4"),
    # Bump the prerelease part of the version
    (("prerelease", "foo.py"), "1.2.3-beta.4", "1.2.3-beta.5"),
    # Set the version to an explicit new version
    (("4.5.6", "foo.py"), "1.2.3-beta.4", "4.5.6"),
    # Set the version to an explicit new version with prerelease part
    (("7.8.9-alpha.1", "foo.py"), "1.2.3-beta.4", "7.8.9-alpha.1"),
    # Set the version to an explicit new version with prerelease part
    (("7.8.9+post.1", "foo.py"), "1.2.3-beta.4", "7.8.9+post.1"),
)
@redirect_stdout
def test_bump_explicit_file(out, cli_args, old_version, new_version):
    """should bump version for various cases, given an explicit file path"""
    file_name = cli_args[-1]
    file_contents = f"""
    name = "foo"
    version = {old_version}
    """
    with use_cli_args(*cli_args):
        create_mock_file(
            file_name,
            file_contents,
        )
        bump.main()
        case.assertIn(f"{file_name}: {old_version} -> {new_version}", out.getvalue())
        case.assertIn(f"version = {new_version}\n", read_mock_file(file_name))


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_bump_multiple_files(out):
    """should bump version for various cases, given an explicit file path"""
    file_name_1 = "package.json"
    file_name_2 = "package-lock.json"
    old_version = "1.2.3"
    new_version = "4.5.6"
    file_contents_1 = f"""{{
        "name": "foo",
        "version": {old_version}
    }}"""
    file_contents_2 = f"""{{
        "lockfileVersion": 1,
        "name": "foo",
        "version": {old_version}
    }}"""
    with use_cli_args(new_version):
        create_mock_file(file_name_1, file_contents_1)
        create_mock_file(file_name_2, file_contents_2)
        bump.main()
        case.assertIn(f"{file_name_1}: {old_version} -> {new_version}", out.getvalue())
        case.assertIn(f"{file_name_2}: {old_version} -> {new_version}", out.getvalue())
        case.assertIn(f'"version": {new_version}\n', read_mock_file(file_name_1))
        case.assertIn(f'"version": {new_version}\n', read_mock_file(file_name_2))


@with_setup(set_up)
@with_teardown(tear_down)
@params(
    # Set the version to the same version
    (("1.2.3", "foo.py"), "1.2.3", "1.2.3"),
)
@redirect_stdout
def test_no_change(out, cli_args, old_version, new_version):
    """should not modify file if same version is given"""
    file_name = cli_args[-1]
    file_contents = f"""
    name = "foo"
    version = {old_version}
    """
    with use_cli_args(*cli_args):
        create_mock_file(
            file_name,
            file_contents,
        )
        bump.main()
        case.assertIn("No files updated", out.getvalue())
        case.assertEqual(file_contents, read_mock_file(file_name))
