#!/usr/bin/env python3
# coding=utf-8

import os
import os.path
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from functools import wraps
from io import StringIO
from unittest.mock import patch

import bumpanything.__main__ as bump

temp_dir_path = tempfile.gettempdir()
temp_subdir_name = "bump-test"
test_dir_path = os.path.join(temp_dir_path, temp_subdir_name)


class BumpAnythingTestCase(unittest.TestCase):
    def setUp(self):
        try:
            os.makedirs(test_dir_path)
        except shutil.Error:
            pass
        os.chdir(test_dir_path)

    def tearDown(self):
        os.chdir(temp_dir_path)
        try:
            shutil.rmtree(test_dir_path)
        except OSError:
            pass


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


def redirect_stdout(func):
    """a decorator to temporarily redirect stdout to new Unicode output
    stream"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        original_stdout = sys.stdout
        out = StringIO()
        try:
            sys.stdout = out
            # If the decorated function is a method, the `self` argument should
            # still be first
            if args and hasattr(args[0], "__class__"):
                self_arg, *rest_args = args
                return func(self_arg, out, *rest_args, **kwargs)
            else:
                return func(out, *args, **kwargs)
        finally:
            sys.stdout = original_stdout

    return wrapper


def redirect_stderr(func):
    """a decorator to temporarily redirect stderr to new Unicode output
    stream"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        original_stderr = sys.stderr
        out = StringIO()
        try:
            sys.stderr = out
            # If the decorated function is a method, the `self` argument should
            # still be first
            if args and hasattr(args[0], "__class__"):
                self_arg, *rest_args = args
                return func(self_arg, out, *rest_args, **kwargs)
            else:
                return func(out, *args, **kwargs)
        finally:
            sys.stderr = original_stderr

    return wrapper


@contextmanager
def use_cli_args(*cli_args):
    """a context manager use the given arguments to the bump CLI utility"""

    with patch("sys.argv", [bump.__file__, *cli_args]):
        yield
