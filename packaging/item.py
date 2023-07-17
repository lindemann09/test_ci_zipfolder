import tarfile
from os.path import getmtime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


class Item(object):

    def __init__(self, item_folder, destination_folder):
        self.path = Path(item_folder)
        self.dest = Path(destination_folder)
        if not self.path.is_dir():
            raise RuntimeError("Please specify an existing item folder.")

    def package_file(self, suffix=""):
        return self.dest.joinpath(self.path.name + suffix)

    def file_list(self, exculde_suffixes):
        """returns list of tuples (filepath, filepath relative to base directory)"""
        rtn = []
        for fl in self.path.rglob("*"):
            excl = [fl.name.endswith(s) for s in exculde_suffixes]
            if sum(excl) == 0:
                rtn.append((fl, fl.relative_to(self.path.parent)))
        return rtn

    def zip(self, exculde_suffixes, force_update=False):
        # creates zip if file required
        if force_update or self.package_needs_update(".zip"):
            zip_path = self.package_file(suffix=".zip")
            print(zip_path.name)
            zipf = ZipFile(zip_path, 'w', ZIP_DEFLATED)
            for fl, rel_path in self.file_list(exculde_suffixes):
                #print("-", rel_path)
                zipf.write(fl, rel_path)
            zipf.close()

    def tar(self, exculde_suffixes, force_update=False):
        if force_update or self.package_needs_update(".tar"):
            tar_path = self.package_file(suffix=".tar")
            print(tar_path.name)
            tarf = tarfile.open(tar_path, "w")
            for fl, rel_path in self.file_list(exculde_suffixes):
                #print("-", rel_path)
                tarf.add(fl, rel_path)
            tarf.close()

    def rmd_file(self):
        return self.path.joinpath(self.path.name+".Rmd")

    def package_needs_update(self, suffix=""):
        """return true is package file is older or does not exists"""
        return True # FIXME use hashing timestamps are not reliable on server
        try:
            time_pack = getmtime(self.package_file(suffix)) # modification time of package
        except FileNotFoundError:
            #print(self.package_file(suffix))
            return True

        file_times = [getmtime(fl) for fl in self.path.rglob("*")] # mod time of all files
        return time_pack < max(file_times)
