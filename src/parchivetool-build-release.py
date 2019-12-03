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
import argparse
from typing import List
from parchivetool_exec import executable_darktable_cli
from parchivetool_exec import executable_exiftool
from parchivetool_exec import check_executables
from parchivetool_msg import msg_raw_folder_flag_not_found
from parchivetool_msg import msg_file_rating
from parchivetool_cmd import run_cmd
from parchivetool_cmd import cmd_get_rating
from parchivetool_utils import is_raw_folder
from parchivetool_utils import find_xmp_files
from parchivetool_utils import find_raw_for_xmp
from parchivetool_utils import find_jpg_for_xmp


JPG_QUALITY: int = 95


def build_release(input_xmp_files: List[str] = [], acceptable_rating: List[int] = [5]):
    print("# PROC: BUILD RELEASE")
    if not is_raw_folder():
        msg_raw_folder_flag_not_found()
    else:
        output_dir = "processed-release"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        if input_xmp_files:
            xmp_files = input_xmp_files
        else:
            xmp_files = find_xmp_files('.')

        for xmp_file in xmp_files:
            raw_file = find_raw_for_xmp(xmp_file, ".")
            jpg_file = find_jpg_for_xmp(xmp_file, "..")
            if raw_file is None or jpg_file is None:
                print("# (!) build '%s' failed, jpg or raw file not found" % (xmp_file))
                continue
            dst_jpg_file = "./" + output_dir + "/" + os.path.basename(jpg_file)
            rating = cmd_get_rating(xmp_file)
            msg_file_rating(xmp_file, rating)
            if rating not in acceptable_rating:
                continue
            # convert to jpeg
            code, _ = run_cmd(executable_darktable_cli(), [
                              raw_file,
                              xmp_file,
                              dst_jpg_file.lower(),
                              "--core",
                              "--conf",
                              "plugins/imageio/format/jpeg/quality=%d" % (JPG_QUALITY,)])
            if code != 0:
                continue
            # rename to original name
            os.rename(dst_jpg_file.lower(), dst_jpg_file)
            # remove rating from the jpeg file, because the darktable-cli create it, but i don't need it!
            # exiftool -overwrite_original -rating=0 -IFD0:Rating=0 -xmp:Rating=0 -IFD0:RatingPercent=0 -xmp:RatingPercent=0 ${DST_PATH}/${1%%.*}.${JPG_EXT}
            code, _ = run_cmd(executable_exiftool(), [
                              "-overwrite_original",
                              "-rating=0",
                              "-IFD0:Rating=0",
                              "-xmp:Rating=0",
                              "-IFD0:RatingPercent=0",
                              "-xmp:RatingPercent=0",
                              dst_jpg_file])
            if code != 0:
                continue
            # exiftool -overwrite_original -rating= -IFD0:Rating= -xmp:Rating= -IFD0:RatingPercent= -xmp:RatingPercent= ${DST_PATH}/${1%%.*}.${JPG_EXT}
            code, _ = run_cmd(executable_exiftool(), [
                              "-overwrite_original",
                              "-rating=",
                              "-IFD0:Rating=",
                              "-xmp:Rating=",
                              "-IFD0:RatingPercent=",
                              "-xmp:RatingPercent=",
                              dst_jpg_file])
            if code != 0:
                continue
            # copy metadata from the original jpeg file
            # exiftool -overwrite_original -TagsFromFile ../${1%%.*}.${JPG_EXT}  "-all:all>all:all" ${DST_PATH}/${1%%.*}.${JPG_EXT}
            code, _ = run_cmd(executable_exiftool(), [
                              "-overwrite_original",
                              "-TagsFromFile",
                              jpg_file,
                              "-all:all>all:all",
                              dst_jpg_file])
            if code != 0:
                continue
            # mark photo as PickLabel=3 (green flag)
            #exiftool -overwrite_original -orientation= -xmp:PickLabel=3 ${DST_PATH}/${1%%.*}.${JPG_EXT}
            code, _ = run_cmd(executable_exiftool(), [
                              "-overwrite_original",
                              "-orientation=",
                              "-xmp:PickLabel=3",
                              dst_jpg_file])
            if code != 0:
                continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--jpg-quality', type=int, help='set jpeg quality (default 95)')
    parser.add_argument('files', type=str, nargs='*', help='files', default=[])
    args = parser.parse_args()

    if args.jpg_quality:
        JPG_QUALITY = args.jpg_quality

    if not check_executables():
        sys.exit(1)
    else:
        if args.files:
            build_release(args.files)
        else:
            build_release()
        sys.exit(0)
