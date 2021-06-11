#!/usr/bin/env python

from pathlib import Path


class Image(object):
    name = ""
    description = ""
    width = {}

    def __init__(self, name: str = None, description: str = "Add description here.", width: dict = {"small": 300, "large": 600}):
        if name is not None:
            self.name = name

        self.description = description
        self.width = width

    def to_dict(self) -> dict:
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
    collection = []

    def __init__(self, collection: list[Image] = None):
        if collection is not None:
            self.collection = collection
        else:
            self.collection = []

    def add(self, image: Image):
        self.collection.append(image)

    def is_empty(self) -> bool:
        return len(self.collection) == 0

    def to_dict(self) -> list[dict]:
        return [image.to_dict() for image in self.collection]

    def __repr__(self):
        return str([str(image) for image in self.collection])

    def __str__(self):
        return str([str(image) for image in self.collection])
