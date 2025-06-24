#!/usr/bin/env python3

from nose2.tools import params

import bumpanything.__main__ as bump
from tests import (
    BumpAnythingTestCase,
    create_mock_file,
    read_mock_file,
    redirect_stdout,
    use_cli_args,
)


class TestBump(BumpAnythingTestCase):
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
    def test_bump_explicit_file(self, out, cli_args, old_version, new_version):
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
            self.assertIn(
                f"{file_name}: {old_version} -> {new_version}", out.getvalue()
            )
            self.assertIn(f"version = {new_version}\n", read_mock_file(file_name))

    @redirect_stdout
    def test_bump_multiple_files(self, out):
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
            self.assertIn(
                f"{file_name_1}: {old_version} -> {new_version}", out.getvalue()
            )
            self.assertIn(
                f"{file_name_2}: {old_version} -> {new_version}", out.getvalue()
            )
            self.assertIn(f'"version": {new_version}\n', read_mock_file(file_name_1))
            self.assertIn(f'"version": {new_version}\n', read_mock_file(file_name_2))

    @params(
        # Set the version to the same version
        (("1.2.3", "foo.py"), "1.2.3", "1.2.3"),
    )
    @redirect_stdout
    def test_no_change(self, out, cli_args, old_version, new_version):
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
            self.assertIn("No files updated", out.getvalue())
            self.assertEqual(file_contents, read_mock_file(file_name))
