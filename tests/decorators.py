#!/usr/bin/env python3
# coding=utf-8

import sys
from functools import wraps
from io import StringIO


def redirect_stdout(func):
    """temporarily redirect stdout to new Unicode output stream"""

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
    """temporarily redirect stderr to new Unicode output stream"""

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
