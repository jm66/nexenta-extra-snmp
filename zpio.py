#!/usr/bin/env python

import commands
import re

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
    pools = [re.split('\s+', line) for line in commands.getoutput(ZPOOLS_COMMAND).split("\n")]
    return [row[0] for row in pools]


def zpool_iostats(zpools):
    zpios = dict()
    for p in zpools:
        zpios[p] = zpoolio_simple(p)
    return zpios


def zpoolio_simple(pool):
    zpio = dict()
    output = commands.getoutput(ZPOOLS_IO_COMMAND.format(pool))
    e = re.split("\s+", output)
    zpio[pool] = {'zpool': e[0],
                  'calloc': toMB(normalize(e[1])),
                  'cfree':  toMB(normalize(e[2])),
                  'oread': toN(normN(e[3])),
                  'owrite': toN(normN(e[4])),
                  'bread': toN(normN(e[5])),
                  'bwrite': toN(normN(e[6])),
                  'lread':  e[7],
                  'lwrite': e[8]}
    return zpio


def save_to_json(dict_var, file_name):
    with open(file_name, 'w'):
        json.dump(dict_var, file_name)


def main():
    # gets zpool list
    zpools = zfs_pools()

    # saves zpool list in json file
    save_to_json(ZPOOLS_CACHE_FILE, zpools)

    # gets zpool iostats and saves in json file
    save_to_json(ZPOOLS_IO_CACHE_FILE, zpool_iostats(zpools))
    return 0


# Start program
if __name__ == "__main__":
    main()

