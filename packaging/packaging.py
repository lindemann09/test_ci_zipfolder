from pathlib import Path
from .item import Item

PACK_FOLDER = "packages/"
EXCLUDE_FOLDER = ("scripts", "packaging", "packages", "build")
EXCLUDE_FILES = ("-qti.zip", "-tv.zip", ".html")
COMPILATION_INSTRUCTION = "compl.instr"

def item_list(source_folders, package_folder):
    """list of all items in multiple folders"""
    rtn = []
    for fld in source_folders:
        for src in Path(fld).iterdir():
            try:
                rtn.append(Item(src, package_folder))
            except RuntimeError:
                pass
    return rtn


def subfolder(base_folder, exclude_folder):
    """list of all items in multiple folders"""
    rtn = []
    for subfolder in Path(base_folder).iterdir():
        if subfolder.is_dir() and not subfolder.name.startswith(".") \
                and subfolder.name not in exclude_folder:
            rtn.append(subfolder)
    return rtn


def tarballs(zipped=True):
    dest_folder = PACK_FOLDER + "tarballs"
    Path(dest_folder).mkdir(parents=True, exist_ok=True)
    source_folder = subfolder(".", EXCLUDE_FOLDER)
    for item in item_list(source_folder, dest_folder):
        if zipped:
            item.zip(EXCLUDE_FILES)
        else:
            item.tar(EXCLUDE_FILES)


def compilation_file(formats=("qti", "tv", "html")):
    Path(PACK_FOLDER).mkdir(parents=True, exist_ok=True)
    source_folder = subfolder(".", EXCLUDE_FOLDER)
    fl = open(PACK_FOLDER + COMPILATION_INSTRUCTION, "w", encoding="utf-8")
    fl.write('"format"\t"file"\t"name"\t"dir"\n')
    for frmt in formats:
        pkg_fld = PACK_FOLDER + frmt
        Path(pkg_fld).mkdir(exist_ok=True)
        for item in item_list(source_folder, pkg_fld):
            if frmt in ("qti", "tv"):
                pack_name = item.package_file("-" + frmt).name
                update = item.package_needs_update("-" + frmt + ".zip")
            else:
                pack_name = item.package_file("").name
                if frmt == "html":
                    update = item.package_needs_update("1.html")
                else:
                    update = item.package_needs_update("")
            if update:
                fl.write(
                f'"{frmt}"\t"{item.rmd_file()}"\t"{pack_name}"\t"{pkg_fld}"\n')
    fl.close()