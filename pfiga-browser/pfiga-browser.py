#!/usr/bin/env python
"""
Notes:
* Templates for:
  * folder index
  * master index
  * build scripts
"""
from pathlib import Path
from argparse import ArgumentParser
from parsers import IndexParser
from directorywalker import DirectoryWalker


def main(args):
    # generate list of paths with first and second level readme files, if they exist, from index (passed by user through CLI)
    index = IndexParser(Path(args.index))
    print(index.parse())
    # scanner = DirectoryWalker(args.index)
    # scanned_paths = scanner.recurse_dirs()
    # images = scanner.find_all_images(
    #     scanned_paths, exts=[".png", ".svg", ".odg"])

    # print(images)

    # write build scripts to parent folder


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("index")
    args = argparser.parse_args()
    main(args)
