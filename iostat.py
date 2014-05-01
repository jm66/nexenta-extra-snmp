#!/usr/bin/python

import sys, commands, re
import simplejson as json

# iostat_e = {'device': None,'rs': None, 'ws': None, 'krs':None, 'kws': None, 'wait': None, 'actv': None, 'wsvc_t': None, 'asvc_t': None,'w': None, 'b': None}
# command = "iostat -xntpz 1 2 | awk 'n > 1 { print ; next } $NF == \"device\" { n++ }'"
command = "iostat -xn 1 2 | awk \'n > 1 { print ; next } $NF == \"device\" { n++ }\'"

def toInt(n):
    return int(round(float(n)))

def iostat(command):
    # r/s    w/s   kr/s   kw/s wait actv wsvc_t asvc_t  %w  %b device
    iostat = {}
    output = commands.getoutput(command).split("\n")
    for line in output:
     line_attr=re.split('\s+', line)
     if len(line_attr) > 5: 
      iostat[line_attr[11]] = {'device': line_attr[11],
      'rs': toInt(line_attr[1]), 'ws': toInt(line_attr[2]),
      'krs': toInt(line_attr[3]), 'kws': toInt(line_attr[4]),
      'wait': toInt(line_attr[5]), 'actv': toInt(line_attr[6]), 
      'wsvc_t': toInt(line_attr[7]), 'asvc_t': toInt(line_attr[8]),
       'w': toInt(line_attr[9]), 'b': toInt(line_attr[10])}
     else: pass
     
    return iostat


iostats = iostat(command)
iostat_fn = "/tmp/iostat.cache"

json.dump(iostats, open(iostat_fn,'w'))
