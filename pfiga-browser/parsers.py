#!/usr/bin/env python
"""
Collection of parser, directive, and AST walker implementation for use processing first and second level readme as described by this project's requirements.

`directory`: Dummy class for specifying directories described within `toctree` directives in reST documents.

`TocTree`: Re-implementation of Sphinx's `toctree` directive. See class description for details/rationale.

`RstParser`: Abstract class for setting up objects required to parse and lex a reST document and directives.

TODO Finish module description.
"""

# python level imports
from pathlib import Path
from typing import List, Dict, Tuple, Any
# docutils level imports
from docutils import nodes, frontend
from docutils.parsers import rst
from docutils.utils import new_document
from docutils.parsers.rst import directives
# pfiga-browser level imports
from imageinfo import ImageCollection, Image, ItemNotFoundError


class directory(nodes.General, nodes.Element):
    """Dummy class for representing directory path nodes in the docutils reST AST."""

    pass


class TocTree(rst.Directive):
    """
    Heavily trimmed and modified version of Sphinx's TocTree reST directive.

    See sphinx.other and docutils.parsers.rst for more info.

    `has_content`: Specifies whether the directive can have additional content after the directive and directive options.

    `required_arguments`: Number of required arguments for the directive (these come after the initial directive declaration).

    `optional_arguments`: Number of optional arguments allowed for the directive.

    `final_argument_whitespace`: Indicates whether the final argument can contain whitespace.

    `option_spec`: Dictionary mapping directive options to their specific type in the document e.g. int, boolean, optional string, required string, etc.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "maxdepth": int,
        "caption": directives.unchanged_required
    }

    def run(self) -> List[nodes.Node]:
        """
        Parse the table of contents directories from the reST document and creates "directory" nodes in the AST for them.

        :returns: List of nodes to add to the AST.
        """
        nodelist: List[nodes.Node] = []

        # in this case we're assuming all of the content of the toctree is file paths
        for entry in self.content:
            # create directory node as a representation of the path in the AST
            # include both rawtext and path version for completeness' sake
            dir_node = directory(rawtext=entry)
            dir_node["fullpath"] = str(Path(entry))
            nodelist.append(dir_node)

        return nodelist


class RstParser(object):
    """
    Initialized everything needed to parsing a reST file and analyzing the resulting AST.

    See docutils.parsers.rst.Parser for more info.
    """

    path: Path
    """
    Path to the file to parse.
    """

    text: str
    """
    Content of the file to parse.
    """

    parser: rst.Parser
    """
    Parser object responsible for generating the AST from the reST file/text.
    """

    rst_document: nodes.document
    """
    AST representation of the reST document.
    """

    def __init__(self, path: Path, text: str):
        """
        Set path to and text of the document to parse and set up a parser and AST document for traversal later.

        :param path: Path to the file being parsed.

        :param text: Text of the document being parsed.
        """
        # register the TocTree class to the "toctree" directive in reST
        directives.register_directive("toctree", TocTree)

        self.path = path
        self.text = text
        self.parser = rst.Parser()

        # create a document object for storing the AST information from the reST document
        self.rst_document = new_document(str(path.absolute()), settings=frontend.OptionParser(components=(rst.Parser,)).get_default_values())

    def parse(self) -> nodes.document:
        """
        Parse the reST document and returns the AST.

        :returns: AST representation of the document.
        """
        self.parser.parse(self.text, self.rst_document)
        return self.rst_document


class TocTreeProcessor(nodes.NodeVisitor):
    """
    Extension of the docutils.nodes.NodeVisitor class that overrides the dispatch_visit function to add process the director(y/ies) that have been parsed from the "toctree" directive.

    `pathlist`: List of paths (directories; see directory class) that have been found in the reST document.

    `parent`: Parent path of the reST document being parsed. Needed for concatenating the full path to the file correctly.
    """

    pathlist: List[Path]

    parent: Path

    def __init__(self, document: nodes.document, parent: Path, pathlist: List[Path]):
        """
        Initialize with AST to walk through and list of paths to save to.

        :param document: AST to walk through.

        :param parent: Parent path of the reST file.

        :param pathlist: List to save parsed directories to.
        """
        self.pathlist = pathlist
        self.parent = parent
        super(TocTreeProcessor, self).__init__(document)

    def dispatch_visit(self, node: nodes.Node) -> None:
        """
        Add the node to the path list if it is a directory node.

        :param node: Current node.
        """
        # if the node is a directory object add the absolute version of the path to the path list
        if isinstance(node, directory):
            self.pathlist.append(self.parent.joinpath(node["fullpath"]))

    def dispatch_departure(self, node: nodes.Node) -> None:
        """Force this function to do nothing to avoid duplicate results or output."""
        pass

    def unknown_visit(self, node: nodes.Node) -> None:
        """Force this function to do nothing to avoid duplicate results or output."""
        pass

    def unknown_departure(self, node: nodes.Node) -> None:
        """Force this function to do nothing to avoid duplicate results or output."""
        pass


class SecondLevelProcessor(nodes.NodeVisitor):
    """
    NodeVisitor implementation used to find image directives and descriptions and process them into Image and ImageCollection object(s) where applicable.

    `image_collection`: Collection of images (found/described in the readme).

    `description_map`: Map of image names/uris to descriptions.

    Needs to be parsed like this because image descriptions can be written before the actual image directive.
    The easiest and most sensical way to approach the problem is to store everything separately and combine
    everything together at the end once everything has been processed.
    """

    image_collection: ImageCollection

    description_map: Dict[str, str]

    def __init__(self, document: nodes.document, collection: ImageCollection, description_map: Dict[str, str]):
        """
        Initialize with an AST to traverse, collection to save found images to and dictionary to map images and their descriptions.

        :param document: AST to walk through.

        :param collection: image collection to store processed images to.

        :param description_map: dictionary to store maps between image names and descriptions.
        """
        self.image_collection = collection
        self.description_map = description_map
        super(SecondLevelProcessor, self).__init__(document)

    def parse_image(self, node: nodes.Node) -> Image:
        """
        Process image uri and width from the AST into an Image object.

        :param node: Current node.

        :returns: Image
        """
        return Image(name=node["uri"], width=node["width"])

    def parse_description(self, node: nodes.Node) -> Tuple[str, str]:
        """
        Get image name and description from AST and store into a dictionary to finish filling out the image metadata later.

        :param node: Current node.
        """
        name_node = node.next_node()
        return (name_node.astext(), node.astext())

    def dispatch_visit(self, node: nodes.Node) -> None:
        """
        Analyzes and processes images and description into their data structures.

        :param node: Current node.
        """
        # if node is an image, parse and store into collection
        if isinstance(node, nodes.image):
            self.image_collection.add(self.parse_image(node))
        # if node is a paragraph and next node is bold (strong aka image name) and store into dictionary
        elif isinstance(node, nodes.paragraph) and isinstance(node.next_node(), nodes.strong):
            self.description_map.update([self.parse_description(node)])

    def dispatch_departure(self, node: nodes.Node) -> None:
        """Force this function to do nothing to avoid duplicate results or output."""
        pass

    def unknown_visit(self, node: nodes.Node) -> None:
        """Force this function to do nothing to avoid duplicate results or output."""
        pass

    def unknown_departure(self, node: nodes.Node) -> None:
        """Force this function to do nothing to avoid duplicate results or output."""
        pass


class ReadmeParser(object):
    """
    Abstract class for parsing and process readme files in a project.

    `path`: Path to the file to parse.

    `content`: Content of the file.
    """

    path: Path

    content: str

    def __init__(self, path: Path):
        """
        Initialize with path to file to parse.

        :param path: Path to the file to parse.
        """
        # validate the file path
        if path.exists() and path.is_file():
            self.path = path
            # read and store contents
            with path.open("r") as f_readme:
                self.content = f_readme.read()
        else:
            raise FileNotFoundError()

    def parse(self) -> Any:
        """Abstract function definition (needs to be implemented by extending class)."""
        raise NotImplementedError("%s: must implement the run() function in the class." % (self.__class__.__name__))


class ReadmeDirectoryParser(ReadmeParser):
    """
    Class for parsing readme locations from "toctree" directives in reST documents.

    Generally this class is used for parsing index and first level readme files.
    These files describe the same things, just at different levels of the project.
    """

    def __init__(self, path: Path):
        """
        Initialize with path to file to parse.

        :param path: Path to project index or first level readme file.
        """
        super(ReadmeDirectoryParser, self).__init__(path)

    def parse(self) -> List[Path]:
        """
        Parse the reST document and return the directories listed within the toctree directive it.

        :returns: List of file paths found in the "toctree" directive of the document.
        """
        parsed_paths: List[Path] = []

        # instantiate a parser and parse the readme to get an AST
        parsed_rst = RstParser(self.path, self.content).parse()
        # walk through the AST and process directory nodes (absolute paths sotred in parsed_paths)
        parsed_rst.walk(TocTreeProcessor(
            parsed_rst, self.path.parent, parsed_paths))

        return parsed_paths


class ReadmeImageParser(ReadmeParser):
    """
    Class for parsing directory and image info from reST files.

    Generally this class is used for processing second level readme files into a format that the
    program can analyze and perform operations on as needed.
    """

    def __init__(self, path: Path):
        """
        Initialize with path to the file to parse.

        :param path: Path to second level readme file (describes directory/images in directory).
        """
        super(ReadmeImageParser, self).__init__(path)

    def parse(self) -> ImageCollection:
        """
        Parse all image directives and descriptions in the readme file and return an ImageCollection object.

        :returns: A collection of images present and described in the second level readme file specified.
        """
        image_collection: ImageCollection = ImageCollection()
        description_map: Dict[str, str] = {}

        # instantiate a parser and parse the readme to get an AST
        parsed_rst = RstParser(self.path, self.content).parse()
        # walk through the AST and process the directives and descriptions
        parsed_rst.walk(SecondLevelProcessor(parsed_rst, image_collection, description_map))

        # set descriptions in the Image objects to what was found in the readme
        for name, description in description_map.items():
            try:
                image = image_collection.find(name)
                image.description = description
            except ItemNotFoundError:
                continue

        return image_collection
