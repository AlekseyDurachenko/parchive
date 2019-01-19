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
from parchivetool_const import const_done_folder_flag
from parchivetool_exec import check_executables
from parchivetool_utils import is_raw_folder
from parchivetool_msg import msg_raw_folder_flag_not_found


def create_done_folder_flag() -> bool:
    if os.path.exists(const_done_folder_flag()):
        print("# (*) '%s' already exists" % (const_done_folder_flag(),))
        return True
    open(const_done_folder_flag(), 'a').close()
    return True


def mark_raw_as_done() -> None:
    print("# PROC: MARK RAW FOLDER AS DONE")
    if not is_raw_folder():
        msg_raw_folder_flag_not_found()
    else:
        if not create_done_folder_flag():
            print("# (!) '%s' creation failed" % (const_done_folder_flag()))
            sys.exit(1)
        print("# (=) done!")


if __name__ == "__main__":
    if not check_executables():
        sys.exit(1)
    else:
        mark_raw_as_done()
        sys.exit(0)
