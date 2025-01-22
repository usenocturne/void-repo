#!/usr/bin/env python3

from pathlib import Path
import shutil
import stat
import sys

def rmtree_if_exists(path: str) -> None:
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: ./vendor-xbps-src.py [path to void-packages repo]")

    void_packages_path = sys.argv[1]

    rmtree_if_exists("./common")
    rmtree_if_exists("./etc")
    Path("./xbps-src").unlink(missing_ok=True)

    vendor_line = "This file is vendored from https://github.com/void-linux/void-packages.\n"
    with open(void_packages_path + "/COPYING", "r") as f:
        vendor_text = [vendor_line + "# \n"] + f.readlines()
        license_text = ["# " + s for s in vendor_text]
    with open(void_packages_path + "/xbps-src", "r") as f:
        xbps_src_text = f.readlines()
        # add newline to separate from the vim modeline present in the original file
        xbps_src_text[2:2] = ["\n"] + license_text

    with open("./xbps-src", "w+") as f:
        f.writelines(xbps_src_text)
    xbps_src_f = Path("./xbps-src")
    xbps_src_f.chmod(xbps_src_f.stat().st_mode | stat.S_IEXEC)

    shutil.copytree(void_packages_path + "/common", "./common")
    shutil.copytree(void_packages_path + "/etc", "./etc")

    with open(void_packages_path + "/COPYING", "r") as f:
        copying_file_content = [vendor_line, "\n"] + f.readlines()
    with open("./common/COPYING", "w+") as f:
        f.writelines(copying_file_content)

    shutil.copyfile("./common/COPYING", "./etc/COPYING")

    def vendor_srcpkg(name: str) -> None:
        source_path = void_packages_path + "/srcpkgs/" + name
        dest_path = "./srcpkgs/" + name
        shutil.copytree(source_path, dest_path)
        shutil.copyfile("./common/COPYING", dest_path + "/COPYING")

    rmtree_if_exists("./srcpkgs/base-files")
    vendor_srcpkg("base-files")
