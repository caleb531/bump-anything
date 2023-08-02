#!/usr/bin/env python3

import os
import os.path
import subprocess


def is_in_git_repository():
    root_dir = os.path.abspath(os.path.sep)
    current_dir_path = os.getcwd()
    while current_dir_path != root_dir:
        if os.path.exists(os.path.join(current_dir_path, ".git")):
            return True
        current_dir_path = os.path.dirname(current_dir_path)
    return False


def run_git_command(subcommand, *args):
    try:
        print(
            subprocess.check_output(
                ["git", subcommand, *args], stderr=subprocess.STDOUT, text=True
            ),
            end="",
        )
        return True
    except subprocess.CalledProcessError:
        return False


def add(file_paths):
    return run_git_command("add", *file_paths)


def commit(message):
    return run_git_command("commit", "-m", message)


def tag(tag_name):
    return run_git_command("tag", tag_name)
