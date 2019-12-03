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
from typing import List


def const_root_folder_flag() -> str:
    return '.root'


def const_done_folder_flag() -> str:
    return '.done'


def const_raw_folder_flag() -> str:
    return '.raw'


def const_darktable_xmp_ext() -> str:
    return 'xmp'


def const_jpg_ext() -> str:
    return 'jpg'


def const_raw_exts() -> List[str]:
    return ['cr2', 'orf', 'dng', 'pef', 'png', 'nef', 'arw', 'rw2', 'tiff', 'jpg']


if __name__ == "__main__":
    pass
