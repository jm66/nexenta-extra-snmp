#!/usr/bin/env python

import re
import subprocess
from tools import json
from tools.configuration import ZPOOLS_CACHE_FILE, ZPOOLS_IO_CACHE_FILE, \
    ZPOOLS_COMMAND, ZPOOLS_IO_COMMAND


def toMB(n):
    if "K" in n[1]:
        return int(round(n[0] / 2**10))
    elif "M" in n[1]:
        return int(round(n[0]))
    elif "G" in n[1]:
        return int(round(n[0] * 2**10))
    elif "T" in n[1]:
        return int(round(n[0] * 2**30))
    else:
        return 0


def toKB(n):
    if "B" in n[1]:
        return int(round(n[0] / 2**10))
    elif "K" in n[1]:
        return int(round(n[0]))
    elif "M" in n[1]:
        return int(round(n[0] * 2**10))
    elif "G" in n[1]:
        return int(round(n[0] * 2**20))
    elif "T" in n[1]:
        return int(round(n[0] * 2**30))
    else:
        return 0
 

def normalize(n):
    if "K" in n:
        return float(n.replace('K', '')), 'K'
    elif "M" in n:
        return float(n.replace('M', '')), 'M'
    elif "G" in n:
        return float(n.replace('G', '')), 'G'
    elif "T" in n:
        return float(n.replace('T', '')), 'T'
    else:
        return 0, 'E'


def normN(n):
    if "K" in n:
        return float(n.replace('K', '')), 'K'
    elif "M" in n:
        return float(n.replace('M', '')), 'M'
    elif "G" in n:
        return float(n.replace('G', '')), 'G'
    elif "T" in n:
        return float(n.replace('T', '')), 'T'
    else:
        return n, 'N'


def toN(n):
    if "K" in n[1]:
        return int(round(n[0] * 10**3))
    elif "M" in n[1]:
        return int(round(n[0] * 10**6))
    elif "G" in n[1]:
        return int(round(n[0] * 10**9))
    elif "T" in n[1]:
        return int(round(n[0] * 10**12))
    else:
        return n[0]


def zfs_pools():
    pools_stdout = subprocess.Popen(ZPOOLS_COMMAND, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
    return [line.replace('\n', '') for line in pools_stdout.stdout.readlines()]


def zpool_iostats(zpools):
    zpios = list()
    for p in zpools:
        zpios.append(zpoolio_simple(p))
    return zpios


def zpoolio_simple(pool):
    zpio = dict()
    output = subprocess.Popen(ZPOOLS_IO_COMMAND % pool, shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    e = re.split("\s+", output.stdout.read())
    zpio[pool] = {'calloc': toMB(normalize(e[1])),
                  'cfree':  toMB(normalize(e[2])),
                  'oread': toN(normN(e[3])),
                  'owrite': toN(normN(e[4])),
                  'bread': toN(normN(e[5])),
                  'bwrite': toN(normN(e[6])),
                  'lread':  e[7],
                  'lwrite': e[8]}
    return zpio


def save_to_json(dict_var, file_name):
    with open(file_name, 'w') as io_file_name:
        json.dump(dict_var, io_file_name)


def main():
    # gets zpool list
    zpools = zfs_pools()

    # saves zpool list in json file
    save_to_json(zpools, ZPOOLS_CACHE_FILE)

    # gets zpool iostats and saves in json file
    save_to_json(zpool_iostats(zpools), ZPOOLS_IO_CACHE_FILE)
    return 0


# Start program
if __name__ == "__main__":
    main()

