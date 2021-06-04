#!/usr/bin/env python
"""
Notes:
* Templates for:
  * folder index
  * master index
  * build scripts
"""
import os
from argparse import ArgumentParser
from dirinfo import DirectoryInfo
from templates import Image, ImageCollection, TemplateEngine


def main(args):
    # generate list of folder (path) to generate indexes from
    dirinfo = DirectoryInfo(args.path)
    temp_engine = TemplateEngine()

    # for each folder:
    for path in dirinfo.recurse_dirs():
        collection = ImageCollection(exts=[".png", ".odg", ".svg"])
        for file in os.listdir(path):
            # - generate index with small/large version and path for each image
            if not os.path.isdir(os.path.join(path, file)):
                collection.add(Image(
                    name=str(file),
                    description="Add description here.",
                    width={
                        "small": 300,
                        "large": 600
                    }
                ))

        # - write index to a file in folder
        temp_engine.render_readme(path, images=collection.to_dict())

        # write master index to file in root folder
        # write build scripts to parent folder


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("path")
    args = argparser.parse_args()
    main(args)
