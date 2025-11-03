#!/usr/bin/env python3
# coding=utf-8

import os
import shutil
import tempfile

import pytest

temp_dir_path = tempfile.gettempdir()
temp_subdir_name = "bump-test"
test_dir_path = os.path.join(temp_dir_path, temp_subdir_name)


@pytest.fixture(autouse=True)
def test_workspace():
    """
    Create a temporary workspace for running tests and clean it up when done.
    """
    try:
        os.makedirs(test_dir_path)
    except shutil.Error:
        pass
    os.chdir(test_dir_path)
    yield
    os.chdir(temp_dir_path)
    try:
        shutil.rmtree(test_dir_path)
    except OSError:
        pass
