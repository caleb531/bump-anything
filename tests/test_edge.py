#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from nose2.tools.decorators import with_setup, with_teardown

import bump_anything.__main__ as bump
from tests import create_mock_file, set_up, tear_down
from tests.utils import redirect_stderr, redirect_stdout, use_cli_args

case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
@redirect_stderr
def test_nonexistent_file_explicit(err, out):
    with use_cli_args("major", "foo.py"):
        bump.main()
        case.assertIn("foo.py: file not found", err.getvalue())
        case.assertNotIn("foo.py: file not found", out.getvalue())


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_nonexistent_file_implicit(out):
    with use_cli_args("major"):
        bump.main()
        case.assertIn("No files updated", out.getvalue())


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_no_version_found(out):
    with use_cli_args("major", "foo.py"):
        create_mock_file(
            "foo.py",
            """
            There's no version here.. unless you brought it with you!
        """,
        )
        bump.main()
        case.assertIn("No files updated", out.getvalue())


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
@redirect_stderr
def test_invalid_version_specifier(err, out):
    with use_cli_args("1.2.3_1"):
        with case.assertRaises(SystemExit):
            bump.main()
        case.assertIn("invalid version specifier", err.getvalue())
