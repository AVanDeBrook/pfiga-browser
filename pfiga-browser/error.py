#!/usr/bin/env python
"""Module for error handling routines and exit code enumerations."""
# python level imports
from enum import Enum

class ExitCode(Enum):
    """Enumeration of all possible exit statuses for the program."""

    NORMAL = 0
    UNKOWN = 1
    FILENOTFOUND = 2
