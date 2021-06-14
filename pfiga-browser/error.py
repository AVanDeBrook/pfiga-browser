#!/usr/bin/env python
# python level imports
from enum import Enum


class ExitCode(Enum):
    NORMAL = 0
    UNKOWN = 1
    FILENOTFOUND = 2
