#!/usr/bin/env python

import subprocess
import re
from tools import json
from tools.configuration import ZPOOLS_IOSTAT_CACHE_FILE, ZPOOLS_COMMAND, \
    ZPOOLS_IOSTAT_COMMAND_EXT
from tools import ZPool, ZPoolDevice
from tools.normalize import normalize_bytes, normalize_number, \
    to_MiB, to_base_10


def create_zpool_device(zpool_serial):
    temp_dev_obj = ZPoolDevice()
    try:
        temp_dev_obj.from_values(label=zpool_serial[1],
                                 calloc=0,
                                 cfree=0,
                                 oread=to_base_10(normalize_number(zpool_serial[4])),
                                 owrite=to_base_10(normalize_number(zpool_serial[5])),
                                 bread=to_base_10(normalize_number(zpool_serial[6])),
                                 bwrite=to_base_10(normalize_number(zpool_serial[7])),
                                 lread=to_base_10(normalize_number(zpool_serial[8])),
                                 lwrite=to_base_10(normalize_number(zpool_serial[9])))
    except Exception:
        print zpool_serial
    return temp_dev_obj


def add_zpool_attributes(temp_zpool_obj, zpool_serial):
    temp_zpool_obj.from_values(label=zpool_serial[0],
                               calloc=to_MiB(normalize_bytes(zpool_serial[1])),
                               cfree=to_MiB(normalize_bytes(zpool_serial[2])),
                               oread=to_base_10(normalize_number(zpool_serial[3])),
                               owrite=to_base_10(normalize_number(zpool_serial[4])),
                               bread=to_base_10(normalize_number(zpool_serial[5])),
                               bwrite=to_base_10(normalize_number(zpool_serial[6])),
                               lread=to_base_10(normalize_number(zpool_serial[7])),
                               lwrite=to_base_10(normalize_number(zpool_serial[8])))
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
    # Parsing ZPools
    zpools = [pool.replace('\n', '') for pool in zpools_output.stdout.readlines()]
    # Processing pools
    for zpool in zpools:
        output = subprocess.Popen(ZPOOLS_IOSTAT_COMMAND_EXT % zpool,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
        lines = output.stdout.readlines()[1:-2]
        # list of list
        lines_list = [re.split('\s+', line)[:-1] for line in lines]
        # removing mirror, raid vDevices
        for line in lines_list:
            if line[1] in ['mirror', 'raid']:
                lines_list.pop(lines_list.index(line))
        # processing lines
        temp_zpool_obj = ZPool()
        n = 0
        device, logs, cache = False, False, False
        lines_iter = iter(lines_list)
        for line in lines_iter:
            if zpool == line[0]:
                temp_zpool_obj = add_zpool_attributes(temp_zpool_obj, line)
            elif cache:
                if 'cache' in line:
                    line = lines_iter.next()
                    n += 1
                temp_zpool_obj.cache.append(create_zpool_device(line))
            elif logs:
                if 'logs' in line:
                    line = lines_iter.next()
                    n += 1
                temp_zpool_obj.log.append(create_zpool_device(line))
            elif device:
                temp_zpool_obj.devices.append(create_zpool_device(line))
            # checking if next element is log or cache
            tmp = n + 1
            if tmp < len(lines_list):
                is_next_line_cache = lines_list[tmp][0] == 'cache'
                is_next_line_logs = lines_list[tmp][0] == 'logs'
                if is_next_line_logs or logs:
                    logs = True
                    cache = is_next_line_cache
                    device = False
                elif is_next_line_cache or cache:
                    cache = True
                    logs = is_next_line_logs
                    device = False
                else:
                    device = True
                    logs, cache = False, False
            # increasing counter
            n += 1
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
