#!/usr/bin/env python

import subprocess
import re
from tools import json
from tools.configuration import IOSTAT_CACHE_FILE, IOSTAT_COMMAND
from tools import IODevice


def iostat():
    # r/s    w/s   kr/s   kw/s wait actv wsvc_t asvc_t  %w  %b device
    devices = list()
    output = subprocess.Popen(IOSTAT_COMMAND,
                              shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    for line in output.stdout.readlines():
        # ignoring first and last element
        device_serial = re.split('\s+', line)[1:-1]
        temp_device = IODevice()
        temp_device.device = device_serial[10]
        temp_device.reads_ps = float(device_serial[0])
        temp_device.writes_ps = float(device_serial[1])
        temp_device.KB_read_ps = float(device_serial[2])
        temp_device.KB_written_ps = float(device_serial[3])
        temp_device.wait = float(device_serial[4])
        temp_device.actv = float(device_serial[5])
        temp_device.wsvc_t = float(device_serial[6])
        temp_device.asvc_t = float(device_serial[7])
        temp_device.wait_pct = float(device_serial[8])
        temp_device.busy_pct = float(device_serial[9])

        # appending recently created obj
        devices.append(temp_device)

    return [dev.to_json() for dev in devices]


def main():
    iostats = iostat()
    # saving file
    with open(IOSTAT_CACHE_FILE, 'w') as cache_file:
        json.dump(iostats, cache_file)


# Start program
if __name__ == "__main__":
    main()
