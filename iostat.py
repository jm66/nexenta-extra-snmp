#!/usr/bin/env python

import commands
import re
from tools import json
from tools.configuration import IOSTAT_CACHE_FILE, IOSTAT_COMMAND


def toInt(n):
    return int(round(float(n)))


def iostat(command):
    # r/s    w/s   kr/s   kw/s wait actv wsvc_t asvc_t  %w  %b device
    iostat = dict()
    output = commands.getoutput(command).split("\n")
    for line in output:
        line_attr = re.split('\s+', line)
        if len(line_attr) > 5:
            iostat[line_attr[11]] = {'device': line_attr[11],
                                     'rs': toInt(line_attr[1]), 'ws': toInt(line_attr[2]),
                                     'krs': toInt(line_attr[3]), 'kws': toInt(line_attr[4]),
                                     'wait': toInt(line_attr[5]), 'actv': toInt(line_attr[6]),
                                     'wsvc_t': toInt(line_attr[7]), 'asvc_t': toInt(line_attr[8]),
                                     'w': toInt(line_attr[9]), 'b': toInt(line_attr[10])}
    return iostat


def main():
    iostats = iostat(IOSTAT_COMMAND)

    with open(IOSTAT_CACHE_FILE, 'w') as cache_file:
        json.dump(iostats, cache_file)


# Start program
if __name__ == "__main__":
    main()
