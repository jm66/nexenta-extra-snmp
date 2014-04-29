#!/usr/bin/python

import sys, commands, re
import simplejson as json

# iostat_e = {'device': None,'rs': None, 'ws': None, 'krs':None, 'kws': None, 'wait': None, 'actv': None, 'wsvc_t': None, 'asvc_t': None,'w': None, 'b': None}

def iostat():
    # r/s    w/s   kr/s   kw/s wait actv wsvc_t asvc_t  %w  %b device
    iostat = {}
    command = 'iostat -xntpz | egrep -v "tty|tout|extended|device"'
    output = commands.getoutput(command).split("\n")
    for line in output:
     line_attr=re.split('\s+', line)
     if len(line_attr) > 5: 
      iostat[line_attr[11]] = {'device': line_attr[11], 'rs': line_attr[1], 'ws': line_attr[2], 'krs': line_attr[3], 'kws': line_attr[4], 
      'wait': line_attr[5], 'actv': line_attr[6], 'wsvc_t': line_attr[7], 'asvc_t': line_attr[8], 'w': line_attr[9], 'b': line_attr[10]}
     else: pass
     
    return iostat


iostat = iostat()
iostat_fn = "/tmp/iostat.snmp.cache"

json.dump(iostat, open(iostat_fn,'w'))
