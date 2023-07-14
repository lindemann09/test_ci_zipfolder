import tarfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

FOLDER = ["Distributions", "Assumptions"]
DEST_FOLDER = "build/packages"
EXCLUDE = ["-qti.zip", "-tv.zip", ".html"]

def zip_subdirs(folder, destination_folder, exclude_suffix):
    folder = Path(folder)
    dest_folder = Path(destination_folder)
    for source in folder.iterdir():
        if source.is_dir():
            zip_path = dest_folder.joinpath(source.name + ".zip")
            zipf = ZipFile(zip_path, 'w', ZIP_DEFLATED)
            print(zip_path.name)
            for fl in source.rglob("*"):
                excl = [fl.name.endswith(s) for s in exclude_suffix]
                if sum(excl) == 0:
                    dest = fl.relative_to(folder)
                    print("-", dest)
                    zipf.write(fl, dest)
            zipf.close()


def tarballs(folder, destination_folder, exclude_suffix):
    folder = Path(folder)
    dest_folder = Path(destination_folder)
    for source in folder.iterdir():
        if source.is_dir():
            tar_path = dest_folder.joinpath(source.name + ".tar")
            tarf = tarfile.open(tar_path, "w")
            print(tar_path.name)
            for fl in source.rglob("*"):
                excl = [fl.name.endswith(s) for s in exclude_suffix]
                if sum(excl) == 0:
                    dest = fl.relative_to(folder)
                    print("-", dest)
                    tarf.add(fl, dest)
            tarf.close()


if __name__ == "__main__":
    Path(DEST_FOLDER).mkdir(parents=True, exist_ok=True)
    for fld in FOLDER:
        tarballs(fld, DEST_FOLDER, EXCLUDE)
