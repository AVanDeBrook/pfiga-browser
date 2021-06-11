#!/usr/bin/env python
"""
Notes:
* Templates for:
  * folder index
  * master index
  * build scripts
"""
import os
from argparse import ArgumentParser
from directorywalker import DirectoryWalker
from template import TemplateEngine


def main(args):
    # generate list of paths with first and second level readme files from root (passed by user through CLI)
    scanner = DirectoryWalker(args.path)
    scanned_paths = scanner.recurse_dirs()
    images = scanner.find_all_images(
        scanned_paths, exts=[".png", ".svg", ".odg"])

    print(images)

    # write build scripts to parent folder


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("path")
    args = argparser.parse_args()
    main(args)
