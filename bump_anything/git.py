#!/usr/bin/env python3

import subprocess


def run_git_command(subcommand, *args):
    print(subprocess.check_output(["git", subcommand, *args]).decode("utf-8"))


def add(file_paths):
    run_git_command("add", *file_paths)


def commit(message):
    run_git_command("commit", "-m", message)


def tag(tag_name):
    run_git_command("tag", tag_name)
