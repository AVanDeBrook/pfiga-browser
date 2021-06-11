#!/usr/bin/env python
import os
from pathlib import Path
from imageinfo import ImageCollection, Image
from copy import deepcopy


class DirectoryWalker(object):
    scanned_paths = []
    root = ""

    def __init__(self, rootpath):
        if os.path.isdir(rootpath):
            self.root = os.path.abspath(rootpath)
        else:
            # raise builtin exception if path is invalid
            # TODO: create more specific error/exception object for this case?
            raise FileNotFoundError()

    def recurse_dirs(self) -> list[Path]:
        """
        Recursively find all subdirectories in the specified root path.


        :returns: List of all absolute file paths found within the specified root path.
        """
        self._recurse_dirs(self.root)
        return self.scanned_paths

    def first_level_paths(self, name: str) -> list[Path]:
        """
        Finds first level readme files from the list of scanned paths (found by recurse_dirs) and returns a list of absolute file paths.


        :param name: First level readme file name to search for.

        :returns: List of absolute paths to first level readme files.
        """

        return self.find_readmes("first", name)

    def second_level_paths(self, name: str) -> list[Path]:
        """
        Find second level readme files from the list of scanned paths (found by recurse_dirs) and returns a list of absolute file paths.


        :param name: First level readme file name to search for.

        :returns: List of absolute paths to second level readme files.
        """

        return self.find_readmes("second", name)

    def find_readmes(self, level: str, name: str) -> list[Path]:
        """
        Function to find a generic readme file in a list of directories.


        :param level: Readme level.

        :param name: Name of the file to search for.

        :returns: List of absolute file paths to readme files.
        """
        readme_paths: list[Path] = []

        for path in self.scanned_paths:
            print("[*] Searching for readme files in '%s'..." % (path))

            if name in os.listdir(path):
                readme_path = os.path.join(path, name)
                readme_paths.append(Path(readme_path))
                print("\033[32m[+] Found readme: level='%s' name='%s'\033[m" %
                      (level, readme_path))

        return readme_paths

    def find_all_images(self, paths: list[Path], exts: list[str] = [".jpg", ".png", ".svg"]) -> dict:
        """
        Finds all images in a list of scanned paths. Scans for only '.jpg', '.png', and '.svg' files by default.


        :param paths: list of paths to search for images (search for images in each path).

        :param exts: (optional) Image extensions to search for.

        :returns: A dictionary where each key (Path) is mapped to a collection of images (ImageCollection). Omits paths where no images were found.
        """
        collections = {}

        for path in paths:
            collection = self.find_images_in_path(path, exts=exts)
            if not collection.is_empty():
                collections[str(path.absolute())] = deepcopy(collection)

        return collections

    def find_images_in_path(self, path: Path, exts: list[str] = [".jpg", ".png", ".svg"]) -> ImageCollection:
        """
        Finds all images in an individual path. Scans for only '.jpg', '.png', and '.svg' files by default.


        :param path: Path to search for images.

        :param exts: (optional) Image extensions to search for.

        :returns: A collection of images (ImageCollection).
        """
        if not path.exists():
            raise FileNotFoundError()
        if not path.is_dir():
            raise PathNotADirectoryError()

        collection = ImageCollection()

        for item in path.iterdir():
            if item.is_file() and item.suffix in exts:
                collection.add(Image(name=item.name))

        return collection

    def _recurse_dirs(self, path):
        subdirs = []

        print("[*] Scanning '%s'..." % (os.path.abspath(path)))

        for directory in os.listdir(path):
            full_path = os.path.join(path, directory)

            if os.path.isdir(full_path):
                self.scanned_paths.append(Path(full_path))
                subdirs.append(full_path)

        if len(subdirs) != 0:
            for directory in subdirs:
                self._recurse_dirs(directory)


class PathNotADirectoryError(Exception):
    def __init__(self):
        super.__init__(self)
