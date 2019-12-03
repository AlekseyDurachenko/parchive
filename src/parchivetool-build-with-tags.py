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


MAX_WIDTH: int = 1280
MAX_HEIGHT: int = 1024
JPG_QUALITY: int = 95


def build_notags(input_xmp_files: List[str] = [], acceptable_rating: List[int] = [5]):
    print("# PROC: BUILD WITH TAGS")
    if not is_raw_folder():
        msg_raw_folder_flag_not_found()
    else:
        output_dir = "processed-with-tags-%dx%d" % (MAX_WIDTH, MAX_HEIGHT,)
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
            code, _ = run_cmd(executable_darktable_cli(), [
                              raw_file,
                              xmp_file,
                              dst_jpg_file.lower(),
                              "--width",
                              str(MAX_WIDTH),
                              "--height",
                              str(MAX_HEIGHT),
                              "--core",
                              "--conf",
                              "plugins/imageio/format/jpeg/quality=%d" % (JPG_QUALITY,)])
            if code != 0:
                continue
            os.rename(dst_jpg_file.lower(), dst_jpg_file)
            code, _ = run_cmd(executable_exiftool(), [
                              "-overwrite_original",
                              "-all=",
                              dst_jpg_file])
            if code != 0:
                continue
            # copy metadata from the original jpeg file
            # exiftool -overwrite_original -TagsFromFile ../${1%%.*}.${JPG_EXT}  "-all:all>all:all" ${DST_PATH}/${1%%.*}.${JPG_EXT}
            # exiftool -overwrite_original -TagsFromFile ../${1%%.*}.${JPG_EXT}
            #          -gps:all -model -make -lensmodel -iso -fnumber -exposuretime 
            #          -apterture -focallength -datetimeoriginal -modifydate 
            #          -creatdate ${DST_PATH}/${1%%.*}.${JPG_EXT}
            code, _ = run_cmd(executable_exiftool(), [
                              "-overwrite_original",
                              "-TagsFromFile",
                              jpg_file,
                              "-gps:all",
                              "-model",
                              "-make",
                              "-lensmodel",
                              "-iso",
                              "-fnumber",
                              "-exposuretime",
                              "-apterture",
                              "-focallength",
                              "-datetimeoriginal",
                              "-modifydate",
                              "-creatdate",
                              "-by-line",
                              "-Artist",
                              "-CopyrightNotice",
                              "-Copyright",
                              "-XMP-cc:License",
                              dst_jpg_file])
            if code != 0:
                continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-width', type=int, help='set maximum width of images (default 1280)')
    parser.add_argument('--max-height', type=int, help='set maximum height of images (default 1024)')
    parser.add_argument('--jpg-quality', type=int, help='set jpeg quality (default 95)')
    parser.add_argument('files', type=str, nargs='*', help='files', default=[])
    args = parser.parse_args()

    if args.max_width:
        MAX_WIDTH = args.max_width

    if args.max_height:
        MAX_HEIGHT = args.max_height

    if args.jpg_quality:
        JPG_QUALITY = args.jpg_quality

    if not check_executables():
        sys.exit(1)
    else:
        if args.files:
            build_notags(args.files)
        else:
            build_notags()
        sys.exit(0)
