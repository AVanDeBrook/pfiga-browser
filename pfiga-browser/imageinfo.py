#!/usr/bin/env python
# python level imports
from typing import Dict, Union, List
from pathlib import Path
from copy import deepcopy


class Image(object):
    """
    Class representation of an image.

    Maintains a name of the image (e.g. file name), description, and small/large width for displaying image previews in thumbnails.
    """

    name: str
    """
    Name of the image. Usually the name of the file that the image is stored in.
    """

    description: str
    """
    Description of the image. By default this is either "" or "Add description here.". Used primarily in second level readme files.
    """

    width: Dict[str, int]
    """
    Small/large width of the image. Used for displaying thumbnails of the image in reST readme files.

    Defaults to 'small': 300 and 'large': 600.
    """

    def __init__(self, name: str, description: str = "Add description here.", width: Dict[str, int] = {"small": 300, "large": 600}):
        """
        :param name: Required. Name of the image.

        :param description: Optional. Image description.

        :param width: Optional. Small/large pixel values for displaying image thumbnails.
        """

        self.name = name
        self.description = description
        self.width = width

    def to_dict(self) -> Dict[str, Union[str, Dict[str, int]]]:
        """
        :returns: a dictionary version of the object. Each attribute of the class is represented as a key, value pair.
        """
        return {
            "name": self.name,
            "description": self.description,
            "width": self.width
        }

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


class ImageCollection(object):
    """
    Class representing a collection of images i.e. all images in a specific directory.

    In most if not all cases the images in this collection are all present in the same directory. Their string representation reflect as much.
    If this is not suitable for a specific application, then this class should be extended and methods overriden as necessary.
    """

    collection: List[Image]
    """
    Collection of images in the directory. Represented as a list of Image objects. There is no importance placed on order when this object is created.
    """

    def __init__(self, collection: List[Image] = []):
        """
        :param collection: Optional, existing list to initalize the object with/to.
        """
        if collection:
            self.collection = collection
        else:
            self.collection = []

    def add(self, image: Image) -> None:
        """
        Adds the image to the collection.


        :paraam image: image to add.
        """

        self.collection.append(image)

    def copy(self) -> "ImageCollection":
        """
        :returns: a 'deep' copy of the object i.e. the object and all objects embedded within it are copied.
        """

        return deepcopy(self)

    def is_empty(self) -> bool:
        """
        :returns: true if there are no images in the collection. False otherwise.
        """

        return len(self.collection) == 0

    def to_dict(self) -> List[Dict[str, Union[str, Dict[str, int]]]]:
        """
        :returns: a list of dictionary representations of the images in the collection. See Image.to_dict()
        """

        return [image.to_dict() for image in self.collection]

    def __repr__(self) -> str:
        return str([str(image) for image in self.collection])

    def __str__(self) -> str:
        return str([str(image) for image in self.collection])
