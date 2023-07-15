
from pathlib import Path
from .item import Item

SOURCE_FOLDER = ("Distributions", "Assumptions")
TARBALL_FOLDER = "build/tarballs"
EXCLUDE = ("-qti.zip", "-tv.zip", ".html")


def tarballs(zipped=True):
    Path(TARBALL_FOLDER).mkdir(parents=True, exist_ok=True)
    for item in Item.item_list(SOURCE_FOLDER, TARBALL_FOLDER):
        if zipped:
            item.zip(EXCLUDE)
        else:
            item.tar(EXCLUDE)
