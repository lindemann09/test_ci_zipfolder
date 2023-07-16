
from pathlib import Path
from .item import Item

SOURCE_FOLDER = ("Distributions", "Assumptions")
BUILD = "build/"
COMPILATION_CSV = "compl.tmp"
EXCLUDE = ("-qti.zip", "-tv.zip", ".html")


def tarballs(zipped=True):
    dest_folder = BUILD + "tarballs"
    Path(dest_folder).mkdir(parents=True, exist_ok=True)
    for item in Item.item_list(SOURCE_FOLDER, dest_folder):
        if zipped:
            item.zip(EXCLUDE)
        else:
            item.tar(EXCLUDE)

def compilation_csv(formats=("qti", "tv", "html")):
    Path(BUILD).mkdir(parents=True, exist_ok=True)
    fl = open(BUILD + COMPILATION_CSV, "w", encoding="utf-8")
    fl.write('"format"\t"file"\t"name"\t"dir"\n')
    for frmt in formats:
        dest_folder = BUILD + frmt
        Path(dest_folder).mkdir(exist_ok=True)
        for item in Item.item_list(SOURCE_FOLDER, dest_folder):
            name = item.path.name
            if frmt in ("qti", "tv"):
                name = name + "-" + frmt
            fl.write(f'"{frmt}"\t"{item.rmd_file()}"\t"{name}"\t"{dest_folder}"\n')
    fl.close()
