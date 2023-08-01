#!/usr/bin/env python3

import unittest

from nose2.tools.decorators import with_setup, with_teardown

import bump_anything.__main__ as bump
from tests import (
    create_mock_file,
    init_git_repo,
    read_mock_file,
    redirect_stderr,
    redirect_stdout,
    run_git_command,
    set_up,
    tear_down,
    use_cli_args,
)

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
        init_git_repo()
        with case.assertRaises(SystemExit):
            bump.main()
        case.assertIn(f'"version": {new_version_1}\n', read_mock_file(file_name_1))
        case.assertIn(f'"version": {new_version_2}\n', read_mock_file(file_name_2))
        case.assertIn("abort", err.getvalue().lower())


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_auto_commit_auto_tag(out):
    """should auto-commit and auto-tag release with Git after bumping version"""
    file_name = "package.json"
    old_version = "1.2.3"
    increment = "minor"
    new_version = "1.3.0"
    file_contents = f"""{{
        "name": "foo",
        "version": {old_version}
    }}"""
    with use_cli_args(increment):
        create_mock_file(file_name, file_contents)
        create_mock_file(file_name, file_contents)
        init_git_repo()
        bump.main()
        case.assertEqual(
            f"Prepare v{new_version} release",
            run_git_command("show", "-s", "--format=%B").strip(),
        )
        case.assertEqual(
            f"v{new_version}",
            run_git_command("describe", "--tags", "--exact-match").strip(),
        )


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_auto_commit_no_tag(out):
    """should auto-commit but not tag release"""
    file_name = "package.json"
    old_version = "1.2.3"
    new_version = "1.3.0"
    file_contents = f"""{{
        "name": "foo",
        "version": {old_version}
    }}"""
    with use_cli_args(new_version, "--no-tag"):
        create_mock_file(file_name, file_contents)
        create_mock_file(file_name, file_contents)
        init_git_repo()
        bump.main()
        case.assertEqual(
            f"Prepare v{new_version} release",
            run_git_command("show", "-s", "--format=%B").strip(),
        )
        case.assertIn(
            "fatal",
            run_git_command("describe", "--tags", "--exact-match").strip(),
        )


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_auto_commit_existing_tag(out):
    """should auto-commit but not tag release due to existing tag"""
    file_name = "package.json"
    old_version = "0.8.0"
    new_version = "1.0.0"
    file_contents = f"""{{
        "name": "foo",
        "version": {old_version}
    }}"""
    with use_cli_args(new_version):
        create_mock_file(file_name, file_contents)
        create_mock_file(file_name, file_contents)
        init_git_repo()
        # Tag the initial commit created in init_git_repo()
        run_git_command("tag", f"v{new_version}")
        bump.main()
        case.assertEqual(
            f"Prepare v{new_version} release",
            run_git_command("show", "-s", "--format=%B").strip(),
        )
        case.assertIn(
            "fatal",
            run_git_command("describe", "--tags", "--exact-match").strip(),
        )


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_no_commit(out):
    """should not commit when --no-commit is supplied"""
    file_name = "package.json"
    old_version = "0.8.0"
    new_version = "1.0.0"
    file_contents = f"""{{
        "name": "foo",
        "version": {old_version}
    }}"""
    with use_cli_args(new_version, "--no-commit"):
        create_mock_file(file_name, file_contents)
        create_mock_file(file_name, file_contents)
        init_git_repo()
        bump.main()
        case.assertEqual(
            "Initial commit",
            run_git_command("show", "-s", "--format=%B").strip(),
        )
        case.assertIn(
            "fatal",
            run_git_command("describe", "--tags", "--exact-match").strip(),
        )
