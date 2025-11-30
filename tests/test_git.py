#!/usr/bin/env python3

from unittest.mock import patch

import pytest

import bumpanything.__main__ as bump
from tests import (
    create_mock_file,
    init_git_repo,
    read_mock_file,
    run_git_command,
    use_cli_args,
)


def test_version_mismatch(capsys):
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
        with pytest.raises(SystemExit):
            bump.main()
        captured = capsys.readouterr()
        assert f'"version": {new_version_1}\n' in read_mock_file(file_name_1)
        assert f'"version": {new_version_2}\n' in read_mock_file(file_name_2)
        assert "abort" in captured.err.lower()


def test_auto_commit_auto_tag(capsys):
    """should auto-commit and auto-tag release with Git after bumping version"""
    file_name = "package.json"
    old_version = "1.2.3"
    new_version = "1.3.0"
    file_contents = f"""{{
        "name": "foo",
        "version": {old_version}
    }}"""
    with use_cli_args(new_version):
        create_mock_file(file_name, file_contents)
        create_mock_file(file_name, file_contents)
        init_git_repo()
        bump.main()
        assert (
            f"Prepare v{new_version} release"
            == run_git_command("show", "-s", "--format=%B").strip()
        )
        assert (
            f"v{new_version}"
            == run_git_command("describe", "--tags", "--exact-match").strip()
        )


@pytest.mark.parametrize(
    ("commit_msg_flag", "tag_name_flag"),
    [
        ("--commit-message", "--tag-name"),
        ("-m", "-t"),
    ],
)
def test_custom_commit_message_custom_tag_name(capsys, commit_msg_flag, tag_name_flag):
    """should use custom commit message and custom tag name"""
    file_name = "package.json"
    old_version = "1.2.3"
    new_version = "1.3.0"
    commit_msg = "Release version {new_version}"
    tag_name = "release-{new_version}"
    file_contents = f"""{{
        "name": "foo",
        "version": {old_version}
    }}"""
    with use_cli_args(
        new_version, commit_msg_flag, commit_msg, tag_name_flag, tag_name
    ):
        create_mock_file(file_name, file_contents)
        create_mock_file(file_name, file_contents)
        init_git_repo()
        bump.main()
        assert (
            commit_msg.format(new_version=new_version)
            == run_git_command("show", "-s", "--format=%B").strip()
        )
        assert (
            tag_name.format(new_version=new_version)
            == run_git_command("describe", "--tags", "--exact-match").strip()
        )


def test_auto_commit_no_tag(capsys):
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
        assert (
            f"Prepare v{new_version} release"
            == run_git_command("show", "-s", "--format=%B").strip()
        )
        assert "fatal" in run_git_command("describe", "--tags", "--exact-match").strip()


def test_auto_commit_existing_tag(capsys):
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
        assert (
            f"Prepare v{new_version} release"
            == run_git_command("show", "-s", "--format=%B").strip()
        )
        assert "fatal" in run_git_command("describe", "--tags", "--exact-match").strip()


def test_commit_failure_aborts_git_operations(capsys):
    """should abort further Git operations when commit fails"""
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
        with (
            patch("bumpanything.git.commit", return_value=False) as commit_mock,
            patch("bumpanything.git.tag") as tag_mock,
        ):
            bump.main()
    captured = capsys.readouterr()
    assert "Commit failed; aborting" in captured.out
    assert commit_mock.called
    assert not tag_mock.called
    assert "Initial commit" == run_git_command("show", "-s", "--format=%B").strip()
    assert "fatal" in run_git_command("describe", "--tags", "--exact-match").strip()


@pytest.mark.parametrize(
    "no_commit_flag",
    [
        "--no-commit",
        "-n",
    ],
)
def test_no_commit(capsys, no_commit_flag):
    """should not commit when --no-commit is supplied"""
    file_name = "package.json"
    old_version = "0.8.0"
    new_version = "1.0.0"
    file_contents = f"""{{
        "name": "foo",
        "version": {old_version}
    }}"""
    with use_cli_args(new_version, no_commit_flag):
        create_mock_file(file_name, file_contents)
        create_mock_file(file_name, file_contents)
        init_git_repo()
        bump.main()
        assert "Initial commit" == run_git_command("show", "-s", "--format=%B").strip()
        assert "fatal" in run_git_command("describe", "--tags", "--exact-match").strip()
