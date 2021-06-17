#!/usr/bin/env python
"""Module for error handling routines and exit code enumerations."""
# python level imports
import enum

class ExitCode(enum.Enum):
    """Enumeration of all possible exit statuses for the program."""

    NORMAL = 0
    UNKOWN = 1
    FILENOTFOUND = 2
