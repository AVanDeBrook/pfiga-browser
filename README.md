# pfiga-browser File System

# Installing Dependences, Building, and Running
## Installing Dependencies
The following dependencies are needed to build and run the program:
* `docutils`
* `jinja2`
* `setuptools`

`build` can be used to automatically install dependencies and create a wheel to install the project as a package.
```bash
$ python -m pip install -U build
$ python -m build
$ python -m pip install dist/pfiga-browser-0.1.3-py3-none-any.whl
```

## Running
The program can be run directly using `python` or `python -m` or a package can be built and run using `build` and `pip`.

The command line interface for this application is, as of yet, undocumented. However, it is very simple at the moment. It requires one input, the index file of the project, to run. See regex below:
```
pfiga-browser/pfiga-browser.py <path>
```
* `path` is either a relative or absolute path to an index file (usually `index.rst` see `test/test_file_browser_v2/pfiga/index.rst` and `test/4gr/00readme.rst` as an example)

To run the program directly, use the following:
```bash
$ python pfiga_browser/pfiga_browser.py test/test_file_browser_v2/pfiga/index.rst
```

To run the program as a package, use the following steps (I would recommend using a virtual environment for development):
```bash
# Virtual environment (for active development)
$ python venv .
$ source bin/activate
# Build wheel for package installation
$ python -m build
# Install using pip
$ python -m pip install dist/pfga_browser-0.1.3-py3-none-any.whl
# Run as a module (and print help/usage text)
$ python -m pfiga_browser
```
**Note**: At the moment the program needs to be run from within the git repo so that it can find the template and configuration files it needs to execute correctly. One of the items on the To-Do list is to make the program runnable from anywhere on the system.

# To-Do List
* See TODO statements in code base for more specifics
* ~~Package Installation:~~
  * ~~Create environment variables for template and config file locations~~
  * ~~Create a configuration file for the program with template and config locations (not to be confused with project specific configuration files~~
* Command Line Interface Arguments:
  * Add CLI documentation
  * Add error handling for too many, too few, or incorrect arguments
  * Add optional arguments:
    * Add optional arguments here
* Configuration:
  * Create formal configuration format/syntax (probably using YAML)
  * Add configuration module for processing files, options, etc.
  * Add template for config files (jinja, yaml)
  * Add default config file
* ~~Templates:~~
  * ~~Finish templates~~
  * ~~Finish module to render and write templates:~~
    * ~~Images~~
    * ~~Indexes~~
* Logging/Error Handling:
  * Add prettier console logging
  * Add better error handling w/ more verbose output:
    * File not found
    * Name errors
    * Type errors
    * File instead of directory
    * Directory instead of file
    * Invalid path
    * Inaccessible file
  * Stronger typing and stronger type enforcement
* Documentation:
  * Parser explanations and methodologies
    * Sphinx:
      * Mediocre core code documentation
      * Directive implementations are unusable outside of sphinx
      * Incompatible with docutils (despite being derived from them)
      * Explain modifications to toctree implementation
      * Explain how directive is processed (from documents to AST to directory strings)
      * Explain how tree-walker and parser are implemented, how they work together, etc.
    * Docutils:
      * Horrendous dev documentation (couldn't figure out how to use the Parser, NodeVisitor without StackOverflow; source code is a better reference than the official docs)
      * Explain NodeVisitor (and methods within)
      * Explain Parser (implementation, extension, wrappers, return values, AST, etc.)
      * Explain directives (concepts, implementation, processing, analysis, required args, optional args, content, etc.)
  * License(s):
    * Review dependency requirements for licenses (if any)

# Disclaimers, Acknowledgements, etc.
This project is still in its infancy, so there are many functionalities that are intended but not yet present as well as debugging messages and object dumps.

This project makes heavy use of reStructuredText and thereby uses the `docutils` library to read and process those files (why re-invent the wheel right?)

The reStructuredText files that the application reads also assume that Sphinx's `toctree` directive will be present in some or all files. As such, this program uses a stripped down, heavily modified version of Sphinx's `toctree` implementation. The inclusion and usage of this will be reflected in the license and documentation as necessary as it becomes more fully complete (I was forced to re-invent the wheel here because the "official" implementation of `toctree` is so closley coupled with Sphinx that it no longer works with `docutils`).
