#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from nose2.tools.decorators import with_setup, with_teardown

import bump_anything.__main__ as bump
from tests import create_mock_file, set_up, tear_down
from tests.decorators import redirect_stderr, redirect_stdout

case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
@patch("sys.argv", [bump.__file__, "major", "foo.py"])
@redirect_stdout
@redirect_stderr
def test_nonexistent_file_explicit(out, err):
    bump.main()
    case.assertIn("foo.py: file not found", out.getvalue())
    case.assertNotIn("foo.py: file not found", err.getvalue())


@with_setup(set_up)
@with_teardown(tear_down)
@patch("sys.argv", [bump.__file__, "major"])
@redirect_stdout
def test_nonexistent_file_implicit(out):
    bump.main()
    case.assertIn("No files updated", out.getvalue())


@with_setup(set_up)
@with_teardown(tear_down)
@patch("sys.argv", [bump.__file__, "major", "foo.py"])
@redirect_stdout
def test_no_version_found(out):
    create_mock_file(
        "foo.py",
        """
        There's no version here.. unless you brought it with you!
    """,
    )
    bump.main()
    case.assertIn("No files updated", out.getvalue())
