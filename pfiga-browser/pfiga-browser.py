#!/usr/bin/env python
"""
Notes:
* Templates for:
  * folder index
  * master index
  * build scripts
"""
from typing import List
from pathlib import Path
from argparse import ArgumentParser
from parsers import ReadmeDirectoryParser
from directorywalker import DirectoryWalker


def main(args):
    index: Path = Path(args.index).absolute()
    index_parser: ReadmeDirectoryParser
    first_level_readme_list: List[Path] = []
    second_level_readme_list: List[Path] = []

    print("index: ", index)

    if index.exists() and index.is_file():
        index_parser = ReadmeDirectoryParser(index)
    else:
        raise FileNotFoundError()

    first_level_readme_list = index_parser.parse()

    print("first level readmes: ", first_level_readme_list)

    for path in first_level_readme_list:
        first_level_parser: ReadmeDirectoryParser = ReadmeDirectoryParser(path)
        for second_level_path in first_level_parser.parse():
            second_level_readme_list.append(second_level_path)

    print("second level readmes: ", second_level_readme_list)

    # write build scripts to parent folder


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("index")
    args = argparser.parse_args()
    main(args)
