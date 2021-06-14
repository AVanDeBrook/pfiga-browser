#!/usr/bin/env python

# core level imports
from typing import List, Dict
from pathlib import Path
from argparse import ArgumentParser
# pfiga-browser level imports
from parsers import ReadmeDirectoryParser, ReadmeImageParser
from directorywalker import DirectoryWalker
from imageinfo import ImageCollection


def main(args) -> int:
    index: Path = Path(args.index).absolute()
    index_parser: ReadmeDirectoryParser
    first_level_readme_list: List[Path] = []
    second_level_readme_list: List[Path] = []
    image_collection_map: Dict[Path, ImageCollection] = {}

    # print("index: ", index)

    # validate index file
    if index.exists() and index.is_file():
        index_parser = ReadmeDirectoryParser(index)
    else:
        raise FileNotFoundError()

    # parse first level readme paths from index file
    first_level_readme_list = index_parser.parse()

    # print("first level readmes: ", first_level_readme_list)

    # parse second level readme paths from each of the first level readmes
    for path in first_level_readme_list:
        # need a new parser object each time so it operates on and crafts directories correctly
        first_level_parser: ReadmeDirectoryParser = ReadmeDirectoryParser(path)
        # add all second level readme paths to collection
        second_level_readme_list.extend(first_level_parser.parse())

    # print("second level readmes: ", second_level_readme_list)

    # process each second level readme and store image data found in the readme
    for path in second_level_readme_list:
        # parse file using the image parser class
        collection: ImageCollection = ReadmeImageParser(path).parse()
        # its possible for some second level readmes to have no image data in them; need to check if the collection has items in it
        if not collection.is_empty():
            image_collection_map[path.parent] = collection

    # print("image collection map: ", image_collection_map)

    # TODO directorywalker.py, parsers.py, template.py: search for first and second level readme files that aren't being tracked and update relevant files
    # TODO directorywalker.py, parsers.py, template.py: search directories for images that aren't being tracked by existing second level readmes and update or create one if it doesn't exist
    return


if __name__ == "__main__":
    # TODO document/add CLI arguments
    # TODO move argument parser to its own file (arguments.py?)
    argparser = ArgumentParser()
    argparser.add_argument("index")
    args = argparser.parse_args()
    main(args)
