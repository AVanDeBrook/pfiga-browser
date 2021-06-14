#!/usr/bin/env python

# core level imports
from typing import List, Dict
from pathlib import Path
from argparse import ArgumentParser
# pfiga-browser level imports
from parsers import ReadmeDirectoryParser, ReadmeImageParser
from directorywalker import DirectoryWalker
from imageinfo import ImageCollection
from error import ExitCode


def main(args) -> int:
    index: Path = Path(args.index).absolute()
    index_parser: ReadmeDirectoryParser

    print("index: ", index, end="\n\n")

    # validate index file
    try:
        index_parser = ReadmeDirectoryParser(index)
    except FileNotFoundError:
        print("Error processing index: File '%s' not found" % (index))
        return ExitCode.FILENOTFOUND
    except Exception as ex:
        print("Unkown error occured: ", ex)
        return ExitCode.UNKOWN

    # parse first level readme paths from index file
    first_level_readme_list: List[Path] = index_parser.parse()

    print("first level readmes:")
    for path in first_level_readme_list:
        print(path)
    print()

    second_level_readme_list: List[Path] = []
    # parse second level readme paths from each of the first level readmes
    for path in first_level_readme_list:
        try:
            # need a new parser object each time so it operates on and crafts directories correctly
            first_level_parser: ReadmeDirectoryParser = ReadmeDirectoryParser(
                path)
            # add all second level readme paths to collection
            second_level_readme_list.extend(first_level_parser.parse())
        except FileNotFoundError:
            print("Error processing first level readme: File '%s' not found" % (path))
            return ExitCode.FILENOTFOUND

    print("second level readmes:")
    for path in second_level_readme_list:
        print(path)
    print()

    image_collection_map: Dict[Path, ImageCollection] = {}
    # process each second level readme and store image data found in the readme
    for path in second_level_readme_list:
        try:
            # parse file using the image parser class
            collection: ImageCollection = ReadmeImageParser(path).parse()
            # its possible for some second level readmes to have no image data in them; need to check if the collection has items in it
            if not collection.is_empty():
                image_collection_map[path.parent] = collection
        except FileNotFoundError:
            print("Error processing second level readme: File '%s' not found" % (path))
            return ExitCode.FILENOTFOUND

    # print("image collection map: ", image_collection_map)

    # TODO directorywalker.py, parsers.py, template.py: search for first and second level readme files that aren't being tracked and update relevant files
    all_first_level_readmes: List[Path] = []
    all_second_level_readmes: List[Path] = []

    # scan paths from top level (retrieved from index) for any untracked first and second level readmes
    for path in first_level_readme_list:
        directory_walkler = DirectoryWalker(path.parent)

        # TODO config.py: update first level readme name to be user configurable
        all_first_level_readmes.extend(
            directory_walkler.first_level_paths("01readme.rst"))

        # TODO config.py: update second level readme name to be user configurable
        all_second_level_readmes.extend(
            directory_walkler.second_level_paths("02readme.rst"))

    # TODO add user options to automatically update untracked files (does this by default at the moment)

    for path in all_first_level_readmes:
        if path not in first_level_readme_list:
            print("found untracked first level readme: '%s'" % (path))
    print()

    for path in all_second_level_readmes:
        if path not in second_level_readme_list:
            print("found untracked second level readme: '%s'" % (path))
    print()

    # TODO directorywalker.py, parsers.py, template.py: search directories for images that aren't being tracked by existing second level readmes and update or create one if it doesn't exist
    return ExitCode.NORMAL


if __name__ == "__main__":
    # TODO document/add CLI arguments
    # TODO move argument parser to its own file (arguments.py?)
    argparser = ArgumentParser()
    argparser.add_argument("index")
    args = argparser.parse_args()
    exit(main(args))
