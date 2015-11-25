#!/usr/bin/env python

import subprocess
import re
from tools import json
from tools.configuration import ZPOOLS_IOSTAT_CACHE_FILE, ZPOOLS_COMMAND, \
    ZPOOLS_IOSTAT_COMMAND_EXT
from tools import ZPool, ZPoolDevice


def create_zpool_device(zpool_serial):
    temp_dev_obj = ZPoolDevice()
    temp_dev_obj.from_values(label=zpool_serial[1],
                             calloc=0,
                             cfree=0,
                             oread=zpool_serial[4],
                             owrite=zpool_serial[5],
                             bread=zpool_serial[6],
                             bwrite=zpool_serial[7],
                             lread=zpool_serial[8],
                             lwrite=zpool_serial[9])
    return temp_dev_obj


def add_zpool_attributes(temp_zpool_obj, zpool_serial):
    temp_zpool_obj.from_values(label=zpool_serial[0],
                               calloc=zpool_serial[1],
                               cfree=zpool_serial[2],
                               oread=zpool_serial[3],
                               owrite=zpool_serial[4],
                               bread=zpool_serial[5],
                               bwrite=zpool_serial[6],
                               lread=zpool_serial[7],
                               lwrite=zpool_serial[8])
    return temp_zpool_obj


def zpool_iostat():
    """
       capacity     operations    bandwidth      latency
    alloc   free   read  write   read  write   read  write
    """
    zpool_iostats = list()
    zpools_output = subprocess.Popen(ZPOOLS_COMMAND,
                                     shell=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
    zpools = [pool.replace('\n', '') for pool in zpools_output.stdout.readlines()]

    for zpool in zpools:
        temp_zpool_obj = ZPool()
        output = subprocess.Popen(ZPOOLS_IOSTAT_COMMAND_EXT % zpool,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
        lines = output.stdout.readlines()[1:-1]
        i = 0
        # removing mirror, raid vDevices
        for line in lines:
            zpool_serial = re.split('\s+', line)[:-1]
            if zpool_serial[1] in ['mirror', 'raidz2', 'raidz1']:
                lines.pop(i)
            i += 1
        # parsing lines
        for line in lines:
            zpool_serial = re.split('\s+', line)[:-1]
            if zpool_serial[0] == zpool:
                add_zpool_attributes(temp_zpool_obj, zpool_serial)
                for zpool_dev in lines:
                    zpool_serial = re.split('\s+', zpool_dev)[:-1]
                    zpool_serial_next = re.split('\s+', lines[lines.index(zpool_dev)+1])[:-1]
                    if not zpool_serial[0]:
                        temp_dev_obj = create_zpool_device(zpool_serial)
                        temp_zpool_obj.devices.append(temp_dev_obj)
                    if zpool_serial_next[0] in ['cache', 'log']:
                        break
            elif zpool_serial[0] == 'cache':
                for zpool_dev in lines:
                    zpool_serial = re.split('\s+', zpool_dev)[:-1]
                    zpool_serial_next = re.split('\s+', lines[lines.index(zpool_dev)+1])[:-1]
                    if not zpool_serial[0]:
                        temp_dev_obj = create_zpool_device(zpool_serial)
                        temp_zpool_obj.cache.append(temp_dev_obj)
                    if zpool_serial_next[0] in ['cache', 'log']:
                        break
            elif zpool_serial[0] == 'log':
                for zpool_dev in lines:
                    zpool_serial = re.split('\s+', zpool_dev)[:-1]
                    zpool_serial_next = re.split('\s+', lines[lines.index(zpool_dev)+1])[:-1]
                    if not zpool_serial[0]:
                        temp_dev_obj = create_zpool_device(zpool_serial)
                        temp_zpool_obj.log.append(temp_dev_obj)
                    if zpool_serial_next[0] in ['cache', 'log']:
                        break
        # appending zpool object with devices
        zpool_iostats.append(temp_zpool_obj)
    return [pool.to_json() for pool in zpool_iostats]


def main():
    zpool_iostats = zpool_iostat()
    # saving file
    with open(ZPOOLS_IOSTAT_CACHE_FILE, 'w') as cache_file:
        json.dump(zpool_iostats, cache_file)


# Start program
if __name__ == "__main__":
    main()
