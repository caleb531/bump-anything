#!/usr/bin/env python3

import unittest

from nose2.tools.decorators import with_setup, with_teardown

import bump_anything.__main__ as bump
from tests import create_mock_file, read_mock_file, run_git_command, set_up, tear_down
from tests.utils import redirect_stderr, redirect_stdout, use_cli_args

case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
@redirect_stderr
def test_version_mismatch(err, out):
    """should abort Git operations due to mismatch between multiple files"""
    file_name_1 = "package.json"
    file_name_2 = "package-lock.json"
    old_version_1 = "1.2.3"
    old_version_2 = "4.5.6"
    increment = "minor"
    new_version_1 = "1.3.0"
    new_version_2 = "4.6.0"
    file_contents_1 = f"""{{
        "name": "foo",
        "version": {old_version_1}
    }}"""
    file_contents_2 = f"""{{
        "lockfileVersion": 1,
        "name": "foo",
        "version": {old_version_2}
    }}"""
    with use_cli_args(increment):
        create_mock_file(file_name_1, file_contents_1)
        create_mock_file(file_name_2, file_contents_2)
        run_git_command("init")
        bump.main()
        case.assertIn(f'"version": {new_version_1}\n', read_mock_file(file_name_1))
        case.assertIn(f'"version": {new_version_2}\n', read_mock_file(file_name_2))
        case.assertIn("abort", err.getvalue().lower())
