# pfiga-browser File System

# Installing Dependences, Building, and Running
## Installing Dependencies
The following dependencies are needed to build and run the program:
* `build` (cannot be installed automatically)
* `docutils`
* `jinja2`
* `setuptools`

`build` can be installed using the following. It is used to automatically build the project and install its dependencies (see below).
```bash
$ python -m pip install -U build
```

## Building
Building the project will also automatically install the dependent packages from PyPi.

Use the following in the root of the git repository to build the project and install its dependencies:
```bash
$ python -m build
```

## Running
The command line interface for this application is, as of yet, undocumented. However, it is very simple at the moment. It requires one input, the index file of the project, to run. See regex below:
```
pfiga-browser/pfiga-browser.py <path>
```
* `path` is either a relative or absolute path to an index file (usually `index.rst` see `test/test_file_browser_v2/pfiga/index.rst` and `test/4gr/00readme.rst` as an example)

Example execution:
```bash
$ chmod +x pfiga-browser/pfiga-browser.py
$ pfiga-browser/pfiga-browser.py test/test_file_browser_v2/pfiga/index.rst
```
Alternatively:
```bash
$ python pfiga-browser/pfiga-browser.py test/test_file_browser_v2/pfiga/index.rst
```
**Note**: At the moment the program needs to be run from within the git repo so that it can find the template and configuration files it needs to execute correctly. One of the items on the To-Do list is to make the program runnable from anywhere on the system.

# To-Do List
* See TODO statements in code base for more specifics
* Package Installation:
  * Create environment variables for template and config file locations
  * Create a configuration file for the program with template and config locations (not to be confused with project specific configuration files)
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
* Templates:
  * Finish templates
  * Finish module to render and write templates:
    * Images
    * Indexes
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

Lastly, the automated dependency installation workflow I've used here is somewhat new and not fully supported as of yet and requires a `pip` version >= ~19 and `python` version >= ~3.5. If you encounter any problem due to this, I recommend you install the dependencies manually using the snippet below, however, I will not be diligently keeping this up to date, so ensure you have the latest version of all packages (listed above and in `pyproject.toml` and `setup.cfg`):
```
python -m pip install -U build docutils jinja2 setuptools
```
