#!/usr/bin/env python
import os
import sys


class DirectoryInfo(object):
    paths = []
    root = ""

    def __init__(self, rootpath):
        if os.path.isdir(rootpath):
            self.root = os.path.abspath(rootpath)
        else:
            raise FileNotFoundError()

    def recurse_dirs(self):
        self._recurse_dirs(self.root)
        return self.paths

    def _recurse_dirs(self, path):
        subdirs = []

        print("\nScanning '%s'...\n" % (os.path.abspath(path)))
        for dir in os.listdir(path):
            if os.path.isdir(os.path.join(path, dir)):
                print("Adding path '%s'" % (os.path.abspath(dir)))
                subdirs.append(os.path.join(path, dir))

        if len(subdirs) != 0:
            for dir in subdirs:
                self.paths.append(dir)
            for dir in subdirs:
                self._recurse_dirs(dir)
