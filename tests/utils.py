#!/usr/bin/env python3
# coding=utf-8

import sys
from contextlib import contextmanager
from functools import wraps
from io import StringIO
from unittest.mock import patch

import bump_anything.__main__ as bump


def redirect_stdout(func):
    """a decorator to temporarily redirect stdout to new Unicode output
    stream"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        original_stdout = sys.stdout
        out = StringIO()
        try:
            sys.stdout = out
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
            return func(out, *args, **kwargs)
        finally:
            sys.stderr = original_stderr

    return wrapper


@contextmanager
def use_cli_args(*cli_args):
    """a context manager use the given arguments to the bump CLI utility"""

    with patch("sys.argv", [bump.__file__, *cli_args]):
        yield
