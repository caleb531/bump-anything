#!/usr/bin/env python3

import pytest

import bumpanything.__main__ as bump
from tests import (
    create_mock_file,
    use_cli_args,
)


def test_nonexistent_file_explicit(capsys):
    """should indicate if the specified file does not exist"""
    with use_cli_args("major", "foo.py"):
        bump.main()
        captured = capsys.readouterr()
        assert "foo.py: file not found" in captured.err
        assert "foo.py: file not found" not in captured.out


def test_nonexistent_file_implicit(capsys):
    """should indicate if no files were specified and none of the default files
    were found"""
    with use_cli_args("major"):
        bump.main()
        captured = capsys.readouterr()
        assert "No files updated" in captured.out


def test_no_version_found(capsys):
    """should indicate when no version field was found in the specified file"""
    with use_cli_args("major", "foo.py"):
        create_mock_file(
            "foo.py",
            """
            There's no version here.. unless you brought it with you!
        """,
        )
        bump.main()
        captured = capsys.readouterr()
        assert "No files updated" in captured.out


def test_invalid_version_specifier(capsys):
    """should throw an error if supplied version specifier is not a valid
    semantic version or increment type"""
    with use_cli_args("1.2.3_1"):
        with pytest.raises(SystemExit):
            bump.main()
        captured = capsys.readouterr()
        assert "invalid version specifier" in captured.err
