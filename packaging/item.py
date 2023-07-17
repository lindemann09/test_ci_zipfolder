import hashlib
import tarfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

HASH_ALGORITHMS = "sha256"

class Item(object):

    def __init__(self, item_folder):
        self.path = Path(item_folder)
        if not self.path.is_dir():
            raise RuntimeError("Please specify an existing item folder.")

    def name(self):
        """item name"""
        return str(self.path)

    def package_file(self, folder, suffix=""):
        """filename of the resulting package"""
        return Path(folder).joinpath(self.path.name + suffix)

    def file_list(self, exculde_suffixes=()):
        """returns list of of all files"""
        rtn = []
        for fl in self.path.rglob("*"):
            if fl.is_file():
                excl = [fl.name.endswith(s) for s in exculde_suffixes]
                if sum(excl) == 0:
                    rtn.append(fl)
        return rtn

    def zip(self, package_folder, exculde_suffixes):
        """creates zip file"""
        zip_path = self.package_file(package_folder, suffix=".zip")
        print(zip_path.name)
        zipf = ZipFile(zip_path, 'w', ZIP_DEFLATED)
        for fl in self.file_list(exculde_suffixes):
            rel_path = fl.relative_to(self.path.parent)
            #print("-", rel_path)
            zipf.write(fl, rel_path)
        zipf.close()

    def tar(self, package_folder, exculde_suffixes):
        """creates tar file, if update is required"""
        tar_path = self.package_file(package_folder, suffix=".tar")
        print(tar_path.name)
        tarf = tarfile.open(tar_path, "w")
        for fl in self.file_list(exculde_suffixes):
            rel_path = fl.relative_to(self.path.parent)
            #print("-", rel_path)
            tarf.add(fl, rel_path)
        tarf.close()

    def rmd_file(self):
        """name of the Rmd file"""
        return self.path.joinpath(self.path.name + ".Rmd")

    def fingerprint(self):
        """Data finger print
        Hashes all file, sorts hashes and generates hash of sorted hashes
        see https://expyriment.org/dataintegrityfingerprint/
        """

        fl_hashes = [_hash_file(fl) for fl in self.file_list()]

        hasher = hashlib.new(HASH_ALGORITHMS)
        for h in sorted(fl_hashes):
            hasher.update(h.encode("utf-8"))

        return hasher.hexdigest()


def _hash_file(filepath):
    # helper function for file hashing
    hasher = hashlib.new(HASH_ALGORITHMS)
    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(64 * 1024), b''):
            hasher.update(block)
    return hasher.hexdigest()
