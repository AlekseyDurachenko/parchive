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
from typing import List
from parchivetool_exec import executable_darktable
from parchivetool_exec import check_executables
from parchivetool_msg import msg_raw_folder_flag_not_found
from parchivetool_msg import msg_file_pick_label
from parchivetool_cmd import cmd_get_picklabel
from parchivetool_utils import is_raw_folder
from parchivetool_utils import find_jpg_files
from parchivetool_utils import find_raw_for_jpg


def open_in_darktable(acceptable_pick_labels: List[int] = [2, 3]):
    print("# PROC: OPEN IN DARKTABLE")
    if not is_raw_folder():
        msg_raw_folder_flag_not_found()
    else:
        raw_files: List[str] = []
        for jpg_file in find_jpg_files('..'):
            pick_label = cmd_get_picklabel(jpg_file)
            msg_file_pick_label(jpg_file, pick_label)
            if pick_label in acceptable_pick_labels:
                raw_file = find_raw_for_jpg(jpg_file, '.')
                if raw_file is None:
                    print("# (!) '%s' does not have a RAW file" % (jpg_file,))
                else:
                    raw_files.append(raw_file)
        if not raw_files:
            print("# (=) nothing to open")
        else:
            print("%s %s" % (executable_darktable(), ' '.join(raw_files)))


if __name__ == "__main__":
    if not check_executables():
        sys.exit(1)
    else:
        open_in_darktable()
        sys.exit(0)
