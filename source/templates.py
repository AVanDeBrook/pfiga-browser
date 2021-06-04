#!/usr/bin/env python

import os
from pathlib import PurePath
from jinja2 import Template, Environment, PackageLoader, select_autoescape


class TemplateEngine(object):
    env = None

    def __init__(self):
        self.env = Environment(
            loader=PackageLoader("pfiga-browser"),
            autoescape=select_autoescape()
        )

    def render_readme(self, outpath, images):
        template: Template = self.env.get_template('readme.rst')
        with open(os.path.join(outpath, "readme.rst"), "w") as f_readme:
            f_readme.write(template.render(
                images=images, folder_name=outpath
            ))
            f_readme.close()


class Image(object):
    name = ""
    description = ""
    width = {
        "small": 300,
        "large": 600
    }

    def __init__(self, name: str = None, description: str = None, width: dict = None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if width is not None:
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


class ImageCollection(object):
    collection = []
    valid_exts = []

    def __init__(self, collection: list[Image] = None, exts: list[str] = None):
        if collection is not None:
            self.collection = collection
        if exts is not None:
            self.valid_exts = exts

    def add(self, image: Image):
        if type(image) == Image:
            if PurePath(image.name).suffix in self.valid_exts:
                self.collection.append(image)
        else:
            raise TypeError()

    def to_dict(self) -> list[dict]:
        return [image.to_dict() for image in self.collection]
