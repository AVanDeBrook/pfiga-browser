#!/usr/bin/env python

from pathlib import Path
from typing import List
from docutils import nodes, frontend
from docutils.parsers import rst
from docutils.utils import new_document
from docutils.parsers.rst import directives


class directory(nodes.General, nodes.Element):
    pass


class TocTree(rst.Directive):
    """ Trimmed version of Sphinx's TocTree reST directive """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "maxdepth": int,
        "caption": directives.unchanged_required
    }

    def run(self) -> List[nodes.Node]:
        self.assert_has_content()
        nodelist: List[nodes.Node] = []

        for entry in self.content:
            dir_node = directory(rawtext=entry)
            dir_node["fullpath"] = str(Path(entry))
            nodelist.append(dir_node)

        return nodelist


class RstParser(object):
    path: Path
    text: str
    parser: rst.Parser
    rst_document: nodes.document

    def __init__(self, path: Path, text: str):
        directives.register_directive("toctree", TocTree)

        self.path = path
        self.text = text
        self.parser = rst.Parser()

        self.rst_document = new_document(
            str(path.absolute()), settings=frontend.OptionParser(components=(rst.Parser,)).get_default_values())

    def parse(self) -> nodes.document:
        self.parser.parse(self.text, self.rst_document)
        return self.rst_document


class RstNodeVisitor(nodes.NodeVisitor):
    pathlist: List[Path]
    parent: Path

    def __init__(self, document: nodes.document, parent: Path, pathlist: List[Path]):
        self.pathlist = pathlist
        self.parent = parent
        super(RstNodeVisitor, self).__init__(document)

    def dispatch_visit(self, node: nodes.Node) -> None:
        if isinstance(node, directory):
            self.pathlist.append(self.parent.joinpath(node["fullpath"]))

    def dispatch_departure(self, node: nodes.Node) -> None:
        pass

    def unknown_visit(self, node: nodes.Node) -> None:
        pass


class ReadmeDirectoryParser(object):
    path: Path
    content: str

    def __init__(self, path: Path):
        if path.exists() and path.is_file():
            self.path = path
            with path.open("r") as f_readme:
                self.content = f_readme.read()

    def parse(self) -> List[Path]:
        parsed_paths: List[Path] = []

        parsed_rst = RstParser(self.path, self.content).parse()
        parsed_rst.walk(RstNodeVisitor(
            parsed_rst, self.path.parent, parsed_paths))

        return parsed_paths
