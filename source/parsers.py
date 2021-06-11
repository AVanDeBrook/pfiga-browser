#!/usr/bin/env python

from pathlib import Path
from typing import List
from docutils.parsers.rst import Parser, Directive, directives
from docutils.frontend import OptionParser
from docutils.utils import new_document
from docutils.nodes import document, NodeVisitor, Node, reference, definition, General, Element
from sphinx import addnodes


class directory(General, Element):
    pass


class TocTree(Directive):
    """ Trimmed version of Sphinx's TocTree reST directive """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "maxdepth": int,
        "caption": directives.unchanged_required
    }

    def run(self) -> List[Node]:
        self.assert_has_content()
        nodelist: List[Node] = []

        for entry in self.content:
            dir_node = directory(rawtext=entry)
            dir_node["fullpath"] = str(Path(entry + ".rst").absolute())
            nodelist.append(dir_node)

        return nodelist


class RstParser(object):
    path: Path = None
    text: str = None
    parser: Parser = None
    rst_document = None

    def __init__(self, path: Path, text: str):
        directives.register_directive("toctree", TocTree)

        self.path = path
        self.text = text

        self.parser = Parser()

        self.rst_document = new_document(
            str(path.absolute()), settings=OptionParser(components=(Parser,)).get_default_values())

    def parse(self) -> document:
        self.parser.parse(self.text, self.rst_document)
        return self.rst_document


class RstNodeVisitor(NodeVisitor):
    def __init__(self, document, pathlist):
        self.pathlist = pathlist
        super(RstNodeVisitor, self).__init__(document)

    def dispatch_visit(self, node):
        if isinstance(node, directory):
            self.pathlist.append(Path(node["fullpath"]))

    def unknown_visit(self, node: Node) -> None:
        pass


class IndexParser(object):
    file = None
    text = None

    def __init__(self, file: Path):
        if file.exists():
            self.file = file

            with file.open("r") as f_index:
                self.text = f_index.read()
                f_index.close()

    def parse(self) -> List[Path]:
        index_paths: List[Path] = []

        parsed_rst = RstParser(self.file, self.text).parse()
        parsed_rst.walk(RstNodeVisitor(parsed_rst, index_paths))

        return index_paths
