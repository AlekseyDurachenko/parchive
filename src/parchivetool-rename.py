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
import re
import os
import argparse
from typing import List
from parchivetool_exec import check_executables
from parchivetool_msg import msg_raw_folder_flag_not_found
from parchivetool_cmd import cmd_get_createdate
from parchivetool_utils import is_raw_folder
from parchivetool_utils import find_jpg_files
from parchivetool_utils import find_raw_for_jpg
from parchivetool_utils import find_xmp_for_jpg


def rename(dry_run: bool, any_name: bool = False) -> None:
    print("# PROC: RENAME")
    if not is_raw_folder():
        msg_raw_folder_flag_not_found()
    else:
        # rename CANON files, template: IMG_NNNN.JPG
        # rename OLYMPUS PEN files, template: PNNNNNNN.JPG
        # rename PENTAX, template IMGPNNNN.JPG
        # rename OTHER, template DSCNNNNN.JPG
        # rename OTHER, template DSCFNNNN.JPG
        # rename OTHER, template DSC_NNNN.JPG
        jpg_files: List[str] = find_jpg_files('..')
        for jpg_file in jpg_files:
            if any_name \
                    or re.match(r'IMG_\d\d\d\d\.JPG$', os.path.basename(jpg_file)) \
                    or re.match(r'P\d\d\d\d\d\d\d\.JPG$', os.path.basename(jpg_file)) \
                    or re.match(r'DSC\d\d\d\d\d\.JPG$', os.path.basename(jpg_file)) \
                    or re.match(r'DSCF\d\d\d\d\.JPG$', os.path.basename(jpg_file)) \
                    or re.match(r'DSC_\d\d\d\d\.JPG$', os.path.basename(jpg_file)) \
                    or re.match(r'IMGP\d\d\d\d\.JPG$', os.path.basename(jpg_file)):
                raw_file = find_raw_for_jpg(jpg_file)
                xmp_file = find_xmp_for_jpg(jpg_file)
                prefix = cmd_get_createdate(jpg_file)
                if not prefix:
                    print("# (!) '%s' problems..." % (jpg_file,))
                    continue
                if jpg_file:
                    new_jpg_file = os.path.dirname(jpg_file) + "/" + prefix + "_" + os.path.basename(jpg_file)
                    if not dry_run:
                        os.rename(jpg_file, new_jpg_file)
                    print("# (>) '%s' -> '%s'" % (jpg_file, new_jpg_file,))
                if raw_file:
                    new_raw_file = os.path.dirname(raw_file) + "/" + prefix + "_" + os.path.basename(raw_file)
                    if not dry_run:
                        os.rename(raw_file, new_raw_file)
                    print("# (>) '%s' -> '%s'" % (raw_file, new_raw_file,))
                if xmp_file:
                    new_xmp_file = os.path.dirname(xmp_file) + "/" + prefix + "_" + os.path.basename(xmp_file)
                    if not dry_run:
                        os.rename(xmp_file, new_xmp_file)
                    print("# (>) '%s' -> '%s'" % (xmp_file, new_xmp_file,))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action="count", help='dry run (only show rename command)')
    parser.add_argument('--any-name', action="count", help='rename with any name')
    args = parser.parse_args()

    if not check_executables():
        sys.exit(1)
    else:
        rename(not not args.dry_run, not not args.any_name)
        sys.exit(0)
