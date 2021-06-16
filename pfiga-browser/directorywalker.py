#!/usr/bin/env python
"""Directory walker class and associated functions for efficiently searching through directories and finding files matching specified patterns."""
# python level import
from typing import List, Union, Dict
from pathlib import Path
# pfiga-browser level imports
from imageinfo import ImageCollection, Image


class DirectoryWalker(object):
    """
    Responsible for all directory related manipulation, searching, etc.

    Maintains a list of scanned paths i.e. all subpaths of the root path that the DirectoryWalker was initialized on.

    `scanned_paths`: List of absolute file paths to directories found within the project(s) (specified in the project index)

    `root`: The root directory that the walker is in charge of analyzing.
    """

    scanned_paths: List[Path]

    root: Path

    def __init__(self, root: Union[Path, str]):
        """
        Initialize directory walker with root path to start searching from.

        :param root: Top-most level of the director(y/ies) to walk through.
        """
        # if the root path is a string, make a path from it
        if not isinstance(root, Path):
            root = Path(root)

        # validate the directory/path
        if root.exists() and root.is_dir():
            self.root = root
        else:
            # TODO create more specific error/exception object for this case?
            raise FileNotFoundError()

        self.scanned_paths = []

    def recurse_dirs(self) -> List[Path]:
        """
        Recursively find all subdirectories in the specified root path.

        :returns: List of all absolute file paths found within the specified root path.
        """
        self.scanned_paths.append(self.root)
        self._recurse_dirs(self.root)
        return self.scanned_paths.sort()

    def first_level_paths(self, name: str) -> List[Path]:
        """
        Find first level readme files from the list of scanned paths (found by recurse_dirs) and returns a list of absolute file paths.

        :param name: First level readme file name to search for.

        :returns: List of absolute paths to first level readme files.
        """
        return self.find_readmes("first", name)

    def second_level_paths(self, name: str) -> List[Path]:
        """
        Find second level readme files from the list of scanned paths (found by recurse_dirs) and returns a list of absolute file paths.

        :param name: First level readme file name to search for.

        :returns: List of absolute paths to second level readme files.
        """
        return self.find_readmes("second", name)

    def find_readmes(self, level: str, name: str) -> List[Path]:
        """
        Find a generic readme file in a list of directories. Finds all file matching `name`, not just the first one.

        :param level: Readme level.

        :param name: Name of the file to search for.

        :returns: Sorted list of absolute paths to readme files.
        """
        # the paths must be scanned first in order to find anything
        if not self.scanned_paths:
            self.recurse_dirs() # TODO raise exception instead of calling `recurse_dirs`

        readme_paths: List[Path] = []

        for path in self.scanned_paths:
            for item in path.iterdir():
                if item.name == name and item.is_file():
                    readme_paths.append(item)

        # sort for consistency in output later
        readme_paths.sort()

        return readme_paths

    def find_all_images(self, exts: List[str] = [".jpg", ".png", ".svg"]) -> Dict[str, ImageCollection]:
        """
        Find all images in the list of scanned paths. Populates the list of scanned paths if it hasn't been already.

        Scans for only '.jpg', '.png', and '.svg' files by default.

        :param paths: list of paths to search for images (search for images in each path).

        :param exts: (optional) Image extensions to search for.

        :returns: A dictionary where each key (Path) is mapped to a collection of images (ImageCollection). Omits paths where no images were found.
        """
        # make sure there is a list of directories to search
        if not self.scanned_paths:
            self.recurse_dirs() # TODO raise exception instead of calling `recurse_dirs`

        collections: Dict[str, ImageCollection] = {}

        # find all images in all the scanned paths and map each path to its associated collection of images
        for path in self.scanned_paths:
            collection = self.find_images_in_path(path, exts=exts)

            # omit if no images were found
            if not collection.is_empty():
                collections[str(path.absolute())] = collection.copy()

        return collections

    def find_images_in_path(self, path: Path, exts: List[str] = [".jpg", ".png", ".svg"]) -> ImageCollection:
        """
        Find all images in `path` matching `exts`.

        :param path: Path to search for images.

        :param exts: (optional) Image extensions to search for. By default: '.jpg', '.png', '.svg'

        :returns: A collection of images (ImageCollection).

        :raises: FileNotFoundError if `path` does not exist on the system. PathNotADirectoryError if `path` is not a directory.
        """
        # validate path
        if not path.exists():
            raise FileNotFoundError()
        if not path.is_dir():
            raise PathNotADirectoryError()

        collection = ImageCollection()

        # check the extension of each file in the directory and add to the collection if it's one of the file types specified
        for item in path.iterdir():
            if item.is_file() and item.suffix in exts:
                collection.add(Image(name=item.name))

        return collection

    def _recurse_dirs(self, path: Path) -> None:
        """
        Recursively finds and adds all directories from the top level path until the end of all paths.

        TODO Should probably add an optional `maxdepth` argument

        :param path: 'root' path to start searching from
        """
        subdirs = []

        # find directories in `path`
        for item in path.iterdir():
            if item.is_dir():
                self.scanned_paths.append(item)
                subdirs.append(item)

        if subdirs:
            # recurse through found directories
            for directory in subdirs:
                self._recurse_dirs(directory)


class PathNotADirectoryError(Exception):
    """Exception object that is raised when a given path is not a directory."""

    def __init__(self, *args: object):
        """
        Initialize with `args`. See `Exception` base class.

        :param args: Arguments to pass to the super class
        """
        super(PathNotADirectoryError, self).__init__()
