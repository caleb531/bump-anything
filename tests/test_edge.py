#!/usr/bin/env python3

import bumpanything.__main__ as bump
from tests import (
    BumpAnythingTestCase,
    create_mock_file,
    redirect_stderr,
    redirect_stdout,
    use_cli_args,
)


class TestEdge(BumpAnythingTestCase):
    @redirect_stdout
    @redirect_stderr
    def test_nonexistent_file_explicit(self, err, out):
        """should indicate if the specified file does not exist"""
        with use_cli_args("major", "foo.py"):
            bump.main()
            self.assertIn("foo.py: file not found", err.getvalue())
            self.assertNotIn("foo.py: file not found", out.getvalue())

    @redirect_stdout
    def test_nonexistent_file_implicit(self, out):
        """should indicate if no files were specified and none of the default files
        were found"""
        with use_cli_args("major"):
            bump.main()
            self.assertIn("No files updated", out.getvalue())

    @redirect_stdout
    def test_no_version_found(self, out):
        """should indicate when no version field was found in the specified file"""
        with use_cli_args("major", "foo.py"):
            create_mock_file(
                "foo.py",
                """
                There's no version here.. unless you brought it with you!
            """,
            )
            bump.main()
            self.assertIn("No files updated", out.getvalue())

    @redirect_stdout
    @redirect_stderr
    def test_invalid_version_specifier(self, err, out):
        """should throw an error if supplied version specifier is not a valid
        semantic version or increment type"""
        with use_cli_args("1.2.3_1"):
            with self.assertRaises(SystemExit):
                bump.main()
            self.assertIn("invalid version specifier", err.getvalue())
