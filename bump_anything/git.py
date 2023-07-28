#!/usr/bin/env python3

import subprocess


def run_git_command(subcommand, *args):
    try:
        print(
            subprocess.check_output(["git", subcommand, *args]).decode("utf-8"),
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
