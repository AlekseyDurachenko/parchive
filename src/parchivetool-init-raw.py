#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2019, Durachenko Aleksey V. <durachenko.aleksey@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
import os
from parchivetool_const import const_raw_folder_flag
from parchivetool_exec import executable_git
from parchivetool_exec import check_executables
from parchivetool_cmd import run_cmd


def create_raw_folder_flag() -> bool:
    if os.path.exists(const_raw_folder_flag()):
        print("# (*) '%s' already exists" % (const_raw_folder_flag(),))
        return True
    open(const_raw_folder_flag(), 'a').close()
    return True


def create_gitignore_file() -> bool:
    if os.path.exists(".gitignore"):
        print("# (*) '.gitignore' already exists")
        return True
    with open(".gitignore", 'w') as f:
        f.write("*.ORF\n")
        f.write("*.orf\n")
        f.write("*.CR2\n")
        f.write("*.cr2\n")
        f.write("*.DNG\n")
        f.write("*.dng\n")
        f.write("*.JPG\n")
        f.write("*.jpg\n")
        f.write("*.PEF\n")
        f.write("*.pef\n")
        f.write("*.NEF\n")
        f.write("*.nef\n")
        f.write("*.PNG\n")
        f.write("*.png\n")
        f.write("*.JPG\n")
        f.write("*.jpg\n")
        f.write("*.RW2\n")
        f.write("*.ARW\n")
        f.write("*.tiff\n")
        f.write("*.TIFF\n")
        f.write(".sha1.sum\n")
        f.write(".par2\n")
        f.write("processed-*\n")
        f.write("open.sh\n")
    return True


def init_raw_folder() -> None:
    print("# PROC: INIT RAW FOLDER")
    code = run_cmd(executable_git(), ['init', '.'])
    if not code:
        print("# (!) 'git init .' failed")
        sys.exit(1)
    if not create_gitignore_file():
        print("# (!) '.gitignore' creation failed")
        sys.exit(1)
    if not create_raw_folder_flag():
        print("# (!) '%s' creation failed" % (const_raw_folder_flag()))
        sys.exit(1)
    print("# (=) done!")


if __name__ == "__main__":
    if not check_executables():
        sys.exit(1)
    else:
        init_raw_folder()
        sys.exit(0)
