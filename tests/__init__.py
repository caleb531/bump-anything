#!/usr/bin/env python3
# coding=utf-8

import os
import os.path
import shutil
import tempfile

temp_dir_path = tempfile.gettempdir()
temp_subdir_name = "bump-test"
test_dir_path = os.path.join(temp_dir_path, temp_subdir_name)


def set_up():
    try:
        os.makedirs(test_dir_path)
    except shutil.Error:
        pass
    os.chdir(test_dir_path)


def tear_down():
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