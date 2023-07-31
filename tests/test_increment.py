#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from nose2.tools.decorators import with_setup, with_teardown

import bump_anything.__main__ as bump
from tests import create_mock_file, read_mock_file, set_up, tear_down
from tests.decorators import redirect_stdout

case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
@patch("sys.argv", [bump.__file__, "major", "major_bump.py"])
@redirect_stdout
def test_major_bump(out):
    create_mock_file(
        "major_bump.py",
        """
        name = "major test"
        version = 1.2.3
    """,
    )
    bump.main()
    case.assertIn("major_bump.py: 1.2.3 -> 2.0.0", out.getvalue())
    case.assertIn("version = 2.0.0\n", read_mock_file("major_bump.py"))


@with_setup(set_up)
@with_teardown(tear_down)
@patch("sys.argv", [bump.__file__, "minor", "minor_bump.py"])
@redirect_stdout
def test_minor_bump(out):
    create_mock_file(
        "minor_bump.py",
        """
        name = "minor test"
        version = 1.2.3
    """,
    )
    bump.main()
    case.assertIn("minor_bump.py: 1.2.3 -> 1.3.0", out.getvalue())
    case.assertIn("version = 1.3.0\n", read_mock_file("minor_bump.py"))


@with_setup(set_up)
@with_teardown(tear_down)
@patch("sys.argv", [bump.__file__, "patch", "patch_bump.py"])
@redirect_stdout
def test_patch_bump(out):
    create_mock_file(
        "patch_bump.py",
        """
        name = "patch test"
        version = 1.2.3
    """,
    )
    bump.main()
    case.assertIn("patch_bump.py: 1.2.3 -> 1.2.4", out.getvalue())
    case.assertIn("version = 1.2.4\n", read_mock_file("patch_bump.py"))


@with_setup(set_up)
@with_teardown(tear_down)
@patch("sys.argv", [bump.__file__, "patch", "prerelease_bump.py"])
@redirect_stdout
def test_prerelease_bump(out):
    create_mock_file(
        "prerelease_bump.py",
        """
        name = "prerelease test"
        version = 1.2.3
    """,
    )
    bump.main()
    case.assertIn("prerelease_bump.py: 1.2.3 -> 1.2.4", out.getvalue())
    case.assertIn("version = 1.2.4\n", read_mock_file("prerelease_bump.py"))
