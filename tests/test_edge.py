#!/usr/bin/env python3

import unittest

from nose2.tools.decorators import with_setup, with_teardown

import bumpanything.__main__ as bump
from tests import (
    create_mock_file,
    redirect_stderr,
    redirect_stdout,
    set_up,
    tear_down,
    use_cli_args,
)

case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
@redirect_stderr
def test_nonexistent_file_explicit(err, out):
    """should indicate if the specified file does not exist"""
    with use_cli_args("major", "foo.py"):
        bump.main()
        case.assertIn("foo.py: file not found", err.getvalue())
        case.assertNotIn("foo.py: file not found", out.getvalue())


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_nonexistent_file_implicit(out):
    """should indicate if no files were specified and none of the default files
    were found"""
    with use_cli_args("major"):
        bump.main()
        case.assertIn("No files updated", out.getvalue())


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_no_version_found(out):
    """should indicate when no version field was found in the specified file"""
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
    """should throw an error if supplied version specifier is not a valid
    semantic version or increment type"""
    with use_cli_args("1.2.3_1"):
        with case.assertRaises(SystemExit):
            bump.main()
        case.assertIn("invalid version specifier", err.getvalue())
