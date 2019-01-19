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
import subprocess
from parchivetool_exec import executable_exiftool


def run_cmd(app, args):
    try:
        out = subprocess.check_output([app] + args, stderr=subprocess.PIPE)
        return 0, out.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("# (!) can't execute command '%s': %s" % (e.cmd, e.stderr,))
        return e.returncode, e


def cmd_get_picklabel(filename: str) -> int:
    code, data = run_cmd(executable_exiftool(), ["-xmp:PickLabel", "-s", "-s", "-s", filename])
    if code == 0:
        if data == '':
            return 0
        else:
            return int(data)
    else:
        return -1


def cmd_get_rating(filename: str) -> int:
    code, data = run_cmd(executable_exiftool(), ["-xmp:Rating", "-s", "-s", "-s", filename])
    if code == 0:
        if data == '':
            return 0
        else:
            return int(data)
    else:
        return -1


def cmd_get_createdate(filename: str) -> str:
    #code, data = run_cmd(executable_exiftool(), ["-createdate", "-s", "-s", "-s", filename])
    code, data = run_cmd(executable_exiftool(), ["-datetimeoriginal", "-s", "-s", "-s", filename])
    if code == 0:
        if data == '':
            return "00000000_000000"
        else:
            return data.strip().replace(':', '').replace(' ', '_')
    else:
        return None


if __name__ == "__main__":
    pass
