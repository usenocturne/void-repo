#!/usr/bin/env python3

from pathlib import Path
import shutil
import stat
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: ./vendor-xbps-src.py [path to void-packages repo]")

    void_packages_path = sys.argv[1]

    try:
        shutil.rmtree("./common/xbps-src")
    except FileNotFoundError:
        pass
    Path("./xbps-src").unlink(missing_ok=True)

    with open(void_packages_path + "/COPYING", "r") as f:
        vendor_line = "This file is vendored from https://github.com/void-linux/void-packages.\n"
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

    shutil.copytree(void_packages_path + "/common/xbps-src", "./common/xbps-src")
    shutil.copyfile(void_packages_path + "/COPYING", "./common/COPYING")
