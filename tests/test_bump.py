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
    file_name = cli_args[-1]
    with use_cli_args(*cli_args):
        create_mock_file(
            file_name,
            f"""
            name = "foo"
            version = {old_version}
            """,
        )
        bump.main()
        case.assertIn(f"{file_name}: {old_version} -> {new_version}", out.getvalue())
        case.assertIn(f"version = {new_version}\n", read_mock_file(file_name))
