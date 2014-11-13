#!/usr/bin/python

import re,commands

date_re = "(\d*\s[A-Za-z]*\s\d*\s\d*:\d*:\d*\s)"
record_re = "\d*\s[A-Za-z]*\s\d*\s\d*:\d*:\d*\s(.*)"
val_re = "(\d.*)"

fname = '/perflogs/nfsutil.out'
fjson = '/tmp/nfsutil.snmp.cache'

line = commands.getoutput('tail -1 %s' %fname)

date_string = re.compile(date_re).search(line).group(1)
data_string = re.compile(record_re).search(line).group(1)
data_array = data_string.split(';')

nfsutil = { 'datetime':   None,
            'max_nfs_req':  None,
            'max_active_threads': None,
            'thread_pool_util': None,
          }

nfsutil = { 'datetime': date_string,
            'max_nfs_req': re.compile(val_re).search(data_array[0]).group(1),
            'max_active_threads': re.compile(val_re).search(data_array[1]).group(1),
            'thread_pool_util': re.compile(val_re).search(data_array[2]).group(1),
          }

json.dump(nfsutil, open(fjson,'w'))
