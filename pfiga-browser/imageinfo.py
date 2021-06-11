#!/usr/bin/env python

from typing import Dict, Union, List
from pathlib import Path
from copy import deepcopy


class Image(object):
    name: str
    description: str
    width: Dict[str, int]

    def __init__(self, name: str = None, description: str = "Add description here.", width: Dict[str, int] = {"small": 300, "large": 600}):
        if name:
            self.name = name

        self.description = description
        self.width = width

    def to_dict(self) -> Dict[str, Union[str, Dict[str, int]]]:
        return {
            "name": self.name,
            "description": self.description,
            "width": {
                "small": self.width["small"],
                "large": self.width["large"]
            }
        }

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class ImageCollection(object):
    collection: List[Image]

    def __init__(self, collection: List[Image] = []):
        if collection:
            self.collection = collection
        else:
            self.collection = []

    def add(self, image: Image) -> None:
        self.collection.append(image)

    def copy(self) -> "ImageCollection":
        return deepcopy(self)

    def is_empty(self) -> bool:
        return len(self.collection) == 0

    def to_dict(self) -> List[Dict[str, Union[str, Dict[str, int]]]]:
        return [image.to_dict() for image in self.collection]

    def __repr__(self):
        return str([str(image) for image in self.collection])

    def __str__(self):
        return str([str(image) for image in self.collection])
