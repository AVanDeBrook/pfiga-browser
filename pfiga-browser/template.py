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
