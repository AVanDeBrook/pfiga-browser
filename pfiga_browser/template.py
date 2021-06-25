#!/usr/bin/env python
"""TODO Add file doc string."""
# python level imports
from typing import Union, List
from pathlib import Path
import os
# jinja level imports
import jinja2 as jinja
# pfiga-browser level imports
from pfiga_browser.imageinfo import Image, ImageCollection


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
            raise jinja.TemplateNotFound(
                "Could not find template: '%s'" % path)

        mtime = os.path.getmtime(str(path))

        with path.open("r") as f_path:
            source = f_path.read()

        return (source, str(path), lambda: mtime == os.path.getmtime(path))


def add_indent(text: str, level: int = 1) -> str:
    """
    Add `level` levels of indent to `text`. `text` must be lines in a file separated by a carriage return.

    :param text: text to add indent levels to.

    :param level: (optional) level of indent to add (number of levels, in other words; the number of tab characters to add to the lines). Defaults to 1.

    :returns: `text` indented by `level` levels.
    """
    lines = text.split("\n")
    indented_text = ""

    for line in lines:
        indented_text += ("\t" * level) + line.strip() + "\n"

    return indented_text


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
        Uses the `readme.rst` template in `pfiga-browser/templates` to render the image info in valid reST syntax and appends that info
        to the end of the file specified in `outpath`.

        :param images: Either a list of `Images` or single `ImageCollection`.

        :param outpath: `Path` to file to update.

        :raises: `FileNotFoundError` if `outpath` is not a file or does not exist.
        """
        # type checking and argument validation (in that order)
        if not isinstance(images, (List, ImageCollection)):
            raise TypeError(
                "Expected List or ImageCollection type for argument 'images' but got '%s'" % type(images))
        if not isinstance(outpath, Path):
            raise TypeError(
                "Expected Path type for argument outpath but got '%s'" % type(outpath))
        if not outpath.exists() and not outpath.is_file():
            raise FileNotFoundError(
                "Could not find file to append to: '%s'" % outpath)

        # render template and save text
        image_template = self.environment.get_template("readme.rst")
        rendered_text = image_template.render(
            images=images.collection if isinstance(images, ImageCollection) else images)

        # append rendered string to file
        with outpath.open("a") as f_outpath:
            f_outpath.write(rendered_text)

    def update_first_level_readme(self, paths: List[Path], outpath: Path) -> None:
        """
        Update first level readmes with untracked second level readmes.

        :param paths: List of `Path`s to untracked second level.

        :param outpath: `Path`/file to write to.

        :raises: `FileNotFoundError` if `outpath` is not a file or does not exist.
        """
        if not outpath.exists() and not outpath.is_file():
            raise FileNotFoundError(
                "Could not find file to append to: '%s'" % outpath)

        readme_template = self.environment.get_template("index.rst")
        rendered_text = readme_template.render(
            paths=[str(path) for path in paths])

        with outpath.open("a") as f_outpath:
            f_outpath.write(add_indent(rendered_text))

    def update_index(self, paths: List[Path], outpath: Path) -> None:
        """
        Update `outpath` with with the paths in `paths`.

        :param paths: List of paths to first level readme's to append to the index file.

        :param outpath: `Path` to the index file to update.

        :raises: `FileNotFoundError` if `outpath` is not a file or does not exist.
        """
        if not outpath.exists() and not outpath.is_file():
            raise FileNotFoundError(
                "Could not find file to append to: '%s'" % outpath)

        index_template = self.environment.get_template("index.rst")
        rendered_text = index_template.render(
            paths=[str(path.relative_to(outpath.parent)) for path in paths])

        with outpath.open("a") as f_outfile:
            f_outfile.write(add_indent(rendered_text))
