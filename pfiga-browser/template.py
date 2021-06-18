#!/usr/bin/env python
"""TODO Add file doc string."""
# python level imports
from typing import Union, List
from pathlib import Path
import os
# jinja level imports
import jinja2 as jinja
# pfiga-browser level imports
from imageinfo import Image, ImageCollection


class TemplateLoader(jinja.BaseLoader):
    """Implementation of a template loader class to work with the jinja2 template engine."""

    def __init__(self, path: Path):
        """
        Create an instance of a TemplateLoader class from the jinja2.BaseLoader class.

        :param path: Path to jinja2 templates.
        """
        self.path = path

    def get_source(self, environment, template):
        """
        Get a specific template from `path`.

        :param environment: Environment to work from (see jinja2 docs).

        :param template: Template file to load.
        """
        path: Path = self.path.joinpath(template)
        source: str = ""

        if not path.exists():
            raise jinja.TemplateNotFound("Could not find template: '%s'" % path)

        mtime = os.path.getmtime(str(path))

        with path.open("r") as f_path:
            source = f_path.read()

        return (source, str(path), lambda: mtime == os.path.getmtime(path))


class TemplateEngine(object):
    """Sets up the jinja2 template engine and environment and provides methods for rendering and updating readme files."""

    environment = None

    def __init__(self):
        """Create a jinja2 environment for the package."""
        self.environment = jinja.Environment(
            loader=TemplateLoader(Path("templates").absolute()),
            autoescape=jinja.select_autoescape()
        )

    def update_images(self, images: Union[List[Image], ImageCollection], outpath: Path) -> None:
        """
        Update an existing file with image data in `images`.

        Accepts either a list of Image objects or a single ImageCollection object as well as a path to the image file (second level readme) to update.
        Uses the `second-level-readme.rst` template in `pfiga-browser/templates` to render the image info in valid reST syntax and appends that info
        to the end of the file specified in `outpath`.

        :param images: Either a list of `Images` or single `ImageCollection`.

        :param outpath: `Path` to file to update.

        :raises: FileNotFoundError if `outpath` is not a file or does not exist.
        """
        # type checking and argument validation (in that order)
        if not isinstance(images, (List, ImageCollection)):
            raise TypeError("Expected List or ImageCollection type for argument 'images' but got '%s'" % type(images))
        if not isinstance(outpath, Path):
            raise TypeError("Expected Path type for argument outpath but got '%s'" % type(outpath))
        if not outpath.exists() and not outpath.is_file():
            raise FileNotFoundError("Could not find file to append to: '%s'" % outpath)

        # render template and save text
        image_template = self.environment.get_template("second-level-readme.rst")
        rendered_text = image_template.render(images=images.collection if isinstance(images, ImageCollection) else images)

        # append rendered string to file
        with outpath.open("a") as f_outpath:
            f_outpath.write(rendered_text)
