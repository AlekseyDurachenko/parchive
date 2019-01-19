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
import shutil
from typing import List


def executable_git() -> str:
    return "git"


def executable_exiftool() -> str:
    return "exiftool"


def executable_darktable() -> str:
    return "darktable"


def executable_darktable_cli() -> str:
    return "darktable-cli"


def print_install_cmd_ubuntu(cmd: str) -> str:
    install_cmds = {
        executable_git(): "apt install git",
        executable_exiftool(): "apt install exiftool",
        executable_darktable(): "apt install darktable",
        executable_darktable_cli(): "apt install darktable"
    }
    return install_cmds.get(cmd)


def print_install_cmd(cmd: str) -> str:
    return print_install_cmd_ubuntu(cmd)


def check_executables() -> bool:
    print("# PROC: DEPENDENCIES CHECKING")
    all: List[str] = [
        executable_git(),
        executable_exiftool(),
        executable_darktable(),
        executable_darktable_cli()
    ]
    for cmd in all:
        if not shutil.which(cmd):
            print("# (!) '%s' not found... please install dependencies: '%s'"
                  % (cmd, print_install_cmd(cmd),))
            return False
        else:
            print("# (+) '%s'... found" % (cmd))
    return True


if __name__ == "__main__":
    pass
