#!/usr/bin/env python
"""Common data structures for images and collections of images."""
# python level imports
from typing import Dict, Union, List
from pathlib import Path
from copy import deepcopy


class Image(object):
    """
    Class representation of an image.

    Maintains a name of the image (e.g. file name), description, and small/large width for displaying image previews in thumbnails.

    `name`: Name of the image. Usually the name of the file that the image is stored in.

    `description`: Description of the image. By default this is either "" or "Add description here.". Used primarily in second level readme files.

    `width`: Width of the image thumbnail (optional argument in reST `image` directives)
    """

    name: str

    description: str

    width: int

    def __init__(self, name: str, description: str = "Add description here.", width: int = 300):
        """
        Initialize with name, description (optional), and width (optional).

        :param name: Required. Name of the image.

        :param description: Optional. Image description.

        :param width: Optional. Small/large pixel values for displaying image thumbnails.
        """
        self.name = name
        self.description = description
        self.width = width

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """
        Return a dictionary representation of the object.

        :returns: a dictionary version of the object. Each attribute of the class is represented as a key, value pair.
        """
        return {
            "name": self.name,
            "description": self.description,
            "width": self.width
        }

    def __repr__(self) -> str:
        """Represent the object as a dictionary where all the class attributes are key-value pairs. See `to_dict`."""
        return str(self.to_dict())

    def __str__(self) -> str:
        """Return name of the image as a string representation of the class."""
        return self.name


class ImageCollection(object):
    """
    Class representing a collection of images i.e. all images in a specific directory.

    In most if not all cases the images in this collection are all present in the same directory. Their string representation reflect as much.
    If this is not suitable for a specific application, then this class should be extended and methods overriden as necessary.

    `collection`: Collection of images in the directory. Represented as a list of Image objects. There is no importance placed on order when this object is created.
    """

    collection: List[Image]

    def __init__(self, collection: List[Image] = []):
        """
        Initialize object to either an empty list or list provided (optional).

        :param collection: Optional, existing list to initalize the object with/to.
        """
        if collection:
            self.collection = collection
        else:
            self.collection = []

    def add(self, image: Image) -> None:
        """
        Add the image to the collection.

        :paraam image: image to add.
        """
        self.collection.append(image)

    def copy(self) -> "ImageCollection":
        """
        Return a "deepcopy" of the class. See copy.deepcopy.

        :returns: a 'deep' copy of the object i.e. the object and all objects embedded within it are copied.
        """
        return deepcopy(self)

    def is_empty(self) -> bool:
        """
        Return true is list is empty, false otherwise.

        :returns: true if there are no images in the collection. False otherwise.
        """
        return len(self.collection) == 0

    def find(self, name: str) -> Image:
        """
        Find an image with a specific name in the collection.

        Raises an ItemNotFoundError when an image with a matching name is not found in the collection.

        :param name: Name of the image to search for (see `name` field in Image class).

        :returns: Reference to the image object with a matching name.

        :raises: ItemNotFoundError when an Image with a matching name is not present in the collection.
        """
        for image in self.collection:
            if image.name == name:
                return image
        raise ItemNotFoundError

    def to_dict(self) -> List[Dict[str, Union[str, int]]]:
        """
        Return a list of dictionary representation of Image objects.

        :returns: a list of dictionary representations of the images in the collection. See Image.to_dict()
        """
        return [image.to_dict() for image in self.collection]

    def __repr__(self) -> str:
        """Return representation of the class as a list of dictionary objects. See `to_dict`."""
        return str(self.to_dict())

    def __str__(self) -> str:
        """Return a list of string representations of the images in the collection."""
        return str([str(image) for image in self.collection])


class ItemNotFoundError(Exception):
    """Exception raised when an item cannot be found by `ImageCollection.find`."""

    def __init__(self, *args: object):
        """
        Initialize the exception object. See `Exception` base class.

        :param args: Arguments passed to the Exception super class to initialize with.
        """
        super(ItemNotFoundError, self).__init__(args)
