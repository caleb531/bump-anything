#!/usr/bin/env python3
# coding=utf-8

import os
import subprocess
import sys
from contextlib import contextmanager
from unittest.mock import patch

from tests.conftest import test_dir_path


def create_mock_file(mock_file_name, file_contents):
    with open(os.path.join(test_dir_path, mock_file_name), "w") as mock_file:
        mock_file.write(file_contents)


def read_mock_file(mock_file_name):
    with open(os.path.join(test_dir_path, mock_file_name), "r") as mock_file:
        return mock_file.read()


def run_git_command(*git_args):
    try:
        return subprocess.check_output(
            ["git", *git_args], stderr=subprocess.STDOUT, text=True
        )
    except subprocess.CalledProcessError as error:
        return error.output


def init_git_repo():
    run_git_command("init")
    run_git_command("config", "commit.gpgsign", "false")
    run_git_command("config", "user.name", "Test User")
    run_git_command("config", "user.email", "user@example.com")
    run_git_command("add", "-A")
    run_git_command("commit", "-m", "Initial commit")


@contextmanager
def use_cli_args(*args):
    """a context manager for using custom CLI arguments"""
    with patch.object(sys, "argv", ["bump-anything", *args]):
        yield
