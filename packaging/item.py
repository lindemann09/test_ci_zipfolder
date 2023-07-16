import tarfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


class Item(object):

    def __init__(self, item_folder, destination_folder):
        self.path = Path(item_folder)
        self.dest = Path(destination_folder)
        if not self.path.is_dir():
            raise RuntimeError("Please specify an existing item folder.")

    def dest_file(self, suffix):
        return self.dest.joinpath(self.path.name + suffix)

    def file_list(self, exculde_suffixes):
        """returns list of tuples (filepath, filepath relative to base directory)"""
        rtn = []
        for fl in self.path.rglob("*"):
            excl = [fl.name.endswith(s) for s in exculde_suffixes]
            if sum(excl) == 0:
                rtn.append((fl, fl.relative_to(self.path.parent)))
        return rtn

    def zip(self, exculde_suffixes):
        zip_path = self.dest_file(suffix=".zip")
        print(zip_path.name)
        zipf = ZipFile(zip_path, 'w', ZIP_DEFLATED)
        for fl, rel_path in self.file_list(exculde_suffixes):
            print("-", rel_path)
            zipf.write(fl, rel_path)
        zipf.close()

    def tar(self, exculde_suffixes):
        tar_path = self.dest_file(suffix=".tar")
        print(tar_path.name)
        tarf = tarfile.open(tar_path, "w")
        for fl, rel_path in self.file_list(exculde_suffixes):
            print("-", rel_path)
            tarf.add(fl, rel_path)
        tarf.close()

    @staticmethod
    def item_list(source_folders, destination_folder):
        """list of all items in multiple folders"""
        rtn = []
        for fld in source_folders:
            for src in Path(fld).iterdir():
                try:
                    rtn.append(Item(src, destination_folder))
                except RuntimeError:
                    pass
        return rtn

    def rmd_file(self):
        return self.path.joinpath(self.path.name+".Rmd")
