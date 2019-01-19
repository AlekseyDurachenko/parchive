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
from typing import List, Union
from parchivetool_const import const_root_folder_flag
from parchivetool_const import const_raw_folder_flag
from parchivetool_const import const_raw_exts
from parchivetool_const import const_jpg_ext
from parchivetool_const import const_darktable_xmp_ext


def is_root_folder(path: str = '.') -> bool:
    return os.path.exists(os.path.join(path, const_root_folder_flag()))


def is_raw_folder(path: str = '.') -> bool:
    return os.path.exists(os.path.join(path, const_raw_folder_flag()))


def find_xmp_files(path: str = '.') -> List[str]:
    filenames: List[str] = []
    for file in os.listdir(path):
        if file.lower().endswith(const_darktable_xmp_ext()):
            filenames.append(os.path.join(path, file))
    return filenames


def find_raw_files(path: str = '.') -> List[str]:
    filenames: List[str] = []
    for file in os.listdir(path):
        if file.lower().endswith(tuple(const_raw_exts())):
            filenames.append(os.path.join(path, file))
    return filenames


def find_jpg_files(path: str = '.') -> List[str]:
    filenames: List[str] = []
    for file in os.listdir(path):
        if file.lower().endswith(const_jpg_ext()):
            filenames.append(os.path.join(path, file))
    return filenames


def find_raw_for_jpg(jpgname: str, path: str = '.') -> Union[str, None]:
    basename: str = os.path.basename(jpgname).rsplit('.', 1)[0]
    for file in os.listdir(path):
        for ext in const_raw_exts():
            if file.lower() == (basename + '.' + ext).lower():
                return os.path.join(path, file)
    return None


def find_xmp_for_jpg(jpgname: str, path: str = '.') -> Union[str, None]:
    basename: str = os.path.basename(jpgname).rsplit('.', 1)[0]
    for file in os.listdir(path):
        for ext in const_raw_exts():
            if file.lower() == (basename + '.' + ext + "." + const_darktable_xmp_ext()).lower():
                return os.path.join(path, file)
    return None


def find_raw_for_xmp(xmpname: str, path: str = '.') -> Union[str, None]:
    basename: str = os.path.basename(xmpname).rsplit('.', 1)[0]
    for file in os.listdir(path):
        if file.lower() == basename.lower():
            return os.path.join(path, file)
    return None


def find_jpg_for_xmp(xmpname: str, path: str = '.') -> Union[str, None]:
    basename: str = os.path.basename(xmpname).rsplit('.', 1)[0].rsplit('.', 1)[0]
    for file in os.listdir(path):
        if file.lower() == (basename + "." + const_jpg_ext()).lower():
            return os.path.join(path, file)
    return None


if __name__ == "__main__":
    pass
