#!/usr/bin/env python
# python level imports
from pathlib import PurePath
# jinja level imports
from jinja2 import Template, Environment, PackageLoader, select_autoescape


class TemplateEngine(object):
    env = None

    def __init__(self):
        self.env = Environment(
            loader=PackageLoader("pfiga-browser"),
            autoescape=select_autoescape()
        )
