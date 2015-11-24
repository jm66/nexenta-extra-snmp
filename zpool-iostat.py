#!/usr/bin/env python

import subprocess
import re
from tools import json
from tools.configuration import ZPOOLS_IOSTAT_CACHE_FILE, ZPOOLS_COMMAND,\
    ZPOOLS_IOSTAT_COMMAND_EXT
from tools import ZPool, ZPoolDevice

"""
                              capacity     operations    bandwidth      latency
pool                       alloc   free   read  write   read  write   read  write
-------------------------  -----  -----  -----  -----  -----  -----  -----  -----
"""


def zpool_iostat():
    zpool_iostats = list()
    zpools_output = subprocess.Popen(ZPOOLS_COMMAND,
                                     shell=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
    zpools = [pool for pool in zpools_output.stdout.readlines()]

    for zpool in zpools:
        temp_zpool_obj = ZPool()
        output = subprocess.Popen(ZPOOLS_IOSTAT_COMMAND_EXT % zpool,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
        lines = output.stdout.readlines()
        lines_iter = iter(lines)
        for line in lines_iter:
            zpool_serial = re.split('\s+', line)[1:-2]
            if zpool == zpool_serial[0]:
                # Adding attributes to Zpool Object if
                # line contains zpool name
                temp_zpool_obj.from_values(label=zpool_serial[0],
                                           calloc=zpool_serial[1],
                                           cfree=zpool_serial[2],
                                           oread=zpool_serial[3],
                                           owrite=zpool_serial[4],
                                           bread=zpool_serial[5],
                                           bwrite=zpool_serial[6],
                                           lread=zpool_serial[7],
                                           lwrite=zpool_serial[8])
            elif not zpool_serial[0] and zpool_serial[1] not in ['mirror', 'raidz2']:
                # Appending device if line is empty and does not contain
                # vdevs (mirror, raidz2)
                temp_dev_obj = ZPoolDevice()
                temp_dev_obj.from_values(label=zpool_serial[1],
                                         calloc=0, cfree=0,
                                         oread=zpool_serial[4],
                                         owrite=zpool_serial[5],
                                         bread=zpool_serial[6],
                                         bwrite=zpool_serial[7],
                                         lread=zpool_serial[8],
                                         lwrite=zpool_serial[9])
                # appending device
                temp_zpool_obj.devices.append(temp_dev_obj)
            elif 'log' in zpool_serial or 'cache' in zpool_serial:
                type_device = zpool_serial[0]

                lines_iter.next()
                zpool_serial = re.split('\s+', line)[1:-2]
                temp_dev_obj = ZPoolDevice()
                temp_dev_obj.from_values(label=zpool_serial[1],
                                         calloc=0, cfree=0,
                                         oread=zpool_serial[4],
                                         owrite=zpool_serial[5],
                                         bread=zpool_serial[6],
                                         bwrite=zpool_serial[7],
                                         lread=zpool_serial[8],
                                         lwrite=zpool_serial[9])
                if type_device == 'log':
                    temp_zpool_obj.log.append(temp_dev_obj)
                elif type_device == 'cache':
                    temp_zpool_obj.cache.append(temp_dev_obj)

    return [pool.to_json() for pool in zpool_iostats]


def main():
    zpool_iostats = zpool_iostat()
    # saving file
    with open(ZPOOLS_IOSTAT_CACHE_FILE, 'w') as cache_file:
        json.dump(zpool_iostats, cache_file)


# Start program
if __name__ == "__main__":
    main()
