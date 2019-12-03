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
from typing import List, Tuple
from parchivetool_exec import check_executables
from parchivetool_msg import msg_raw_folder_flag_not_found
from parchivetool_msg import msg_file_pick_label
from parchivetool_cmd import cmd_get_picklabel
from parchivetool_utils import is_raw_folder
from parchivetool_utils import find_jpg_files
from parchivetool_utils import find_raw_for_jpg
from parchivetool_utils import find_xmp_for_jpg
from parchivetool_const import const_root_folder_flag


def find_root_dir() -> Tuple[str, str]:
    cwd = os.getcwd()
    path = '/'
    for e in cwd.split('/'):
        if os.path.exists(os.path.join(path, const_root_folder_flag())):
            return (path, cwd[len(path)+1:])
        else:
            path = os.path.join(path, e)
    return (None, None)


def move_to_trash(dry_run: bool, move_pick_labels: List[int] = [1]) -> None:
    print("# PROC: MOVE TO TRASH")
    if not is_raw_folder():
        msg_raw_folder_flag_not_found()
    else:
        root_path, sub_path = find_root_dir()
        trash_path = os.path.join(root_path, 'Trash', sub_path)
        if not root_path or not sub_path:
            print('# ERROR: NO ROOT PATH FOUND (".root")')
        if not os.path.exists(trash_path):
            if not dry_run:
                os.makedirs(trash_path, exist_ok=True)
        for jpg_file in find_jpg_files('..'):
            pick_label = cmd_get_picklabel(jpg_file)
            msg_file_pick_label(jpg_file, pick_label)
            if pick_label in move_pick_labels:
                new_jpg_file = os.path.join(trash_path, jpg_file)
                if not dry_run:
                    os.rename(jpg_file, new_jpg_file)
                print("# (>) '%s' -> '%s'" % (jpg_file, new_jpg_file,))

                raw_file = find_raw_for_jpg(jpg_file, '.')
                if raw_file:
                    new_raw_file = os.path.join(trash_path, raw_file)
                    if not dry_run:
                        os.rename(raw_file, new_raw_file)
                    print("# (>) '%s' -> '%s'" % (raw_file, new_raw_file,))

                xmp_file = find_xmp_for_jpg(jpg_file, '.')
                if xmp_file:
                    new_xmp_file = os.path.join(trash_path, xmp_file)
                    if not dry_run:
                        os.rename(xmp_file, new_xmp_file)
                    print("# (>) '%s' -> '%s'" % (xmp_file, new_xmp_file,))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action="count", help='dry run (only show move command)')
    args = parser.parse_args()

    if not check_executables():
        sys.exit(1)
    else:
        move_to_trash(not not args.dry_run)
        sys.exit(0)
