#!/usr/bin/env python

import os
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


class ImageCollection(object):
    collection = []

    def __init__(self):
        pass

    def add(self, image):
        if type(image) == Image:
            self.collection.append(image)
        else:
            raise TypeError()

    def to_dict(self):
        return [image.to_dict() for image in self.collection]


class Image(object):
    name = ""
    description = ""
    width = {
        "small": 300,
        "large": 600
    }

    def __init__(self, name: str, description: str, width: dict):
        self.name = name
        self.description = description
        self.width = width

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "width": {
                "small": self.width["small"],
                "large": self.width["large"]
            }
        }
