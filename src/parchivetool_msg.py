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
import os


def msg_root_folder_flag_not_found() -> None:
    print("# ! root folder flag not found")


def msg_raw_folder_flag_not_found() -> None:
    print("# ! raw folder flag not found")


def msg_file_pick_label(filename: str, pick_label: int) -> None:
    if pick_label == 1:
        pick_label_name = 'Red'
    elif pick_label == 2:
        pick_label_name = 'Yellow'
    elif pick_label == 3:
        pick_label_name = 'Green'
    else:
        pick_label_name = 'None'
    basefilename = os.path.basename(filename)
    print("# (L) '%s' has PickLabel '%s'" % (basefilename, pick_label_name,))


def msg_file_rating(filename: str, rating: int) -> None:
    basefilename = os.path.basename(filename)
    print("# (R) '%s' has Rating '%s'" % (basefilename, rating,))


if __name__ == "__main__":
    pass
