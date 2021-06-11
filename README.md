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
pfiga-browser <path>
```
* `path` is either a relative or absolute path to an index file (usually `index.rst` see `test/test_file_browser_v2/pfiga/index.rst` and `test/4gr/00readme.rst` as an example)

Example execution:
```bash
$ pfiga-browser test/test_file_browser_v2/pfiga/index.rst
```
**Note**: Depending on how it was built and installed, `pfiga-browser` may need to be run as `pfiga-browser/pfiga-browser.py` from the root of the git repo.

# Disclaimers, Acknowledgements, etc.
This project is still in its infancy, so there are many functionalities that are intended but not yet present as well as debugging messages and object dumps.

This project makes heavy use of reStructuredText and thereby uses the `docutils` library to read and process those files (why re-invent the wheel right?)

The reStructuredText files that the application reads also assume that Sphinx's `toctree` directive will be present in some or all files. As such, this program uses a stripped down, heavily modified version of Sphinx's `toctree` implementation. The inclusion and usage of this will be reflected in the license and documentation as necessary as it becomes more fully complete (I was forced to re-invent the wheel here because the "official" implementation of `toctree` is so closley coupled with Sphinx that it no longer works with `docutils`).

Lastly, the automated dependency installation workflow I've used here is somewhat new and not fully supported as of yet and requires a `pip` version >= ~19 and `python` version >= ~3.5. If you encounter any problem due to this, I recommend you install the dependencies manually using the snippet below, however, I will not be diligently keeping this up to date, so ensure you have the latest version of all packages (listed above and in `pyproject.toml` and `setup.cfg`):
```
python -m pip install -U build docutils jinja2 setuptools
```
