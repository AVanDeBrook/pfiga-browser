#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="pfiga_browser",
    version="0.1.3",
    packages=[
        "pfiga_browser",
        "pfiga_browser.templates"
    ],
    package_data={
        "pfiga_browser.templates": [
            "index.rst",
            "readme.rst"
        ]
    },
    install_requires=[
        "docutils",
        "jinja2",
        "setuptools"
    ]
)
