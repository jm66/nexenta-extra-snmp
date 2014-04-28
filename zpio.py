#!/usr/bin/python

import sys, commands, re
import simplejson as json

def toMB(n):
  if "K" in n[1]: return int(round(n[0] / 2**10))
  elif "M" in n[1]: return int(round(n[0]))
  elif "G" in n[1]: return int(round(n[0] * 2**10))
  elif "T" in n[1]: return int(round(n[0] * 2**30))
  else: return 0

def toKB(n):
  if "B" in n[1]: return int(round(n[0] / 2**10))
  elif "K" in n[1]: return int(round(n[0]))
  elif "M" in n[1]: return int(round(n[0] * 2**10))
  elif "G" in n[1]: return int(round(n[0] * 2**20))
  elif "T" in n[1]: return int(round(n[0] * 2**30))
  else: return 0

def norm(n):
 if "K" in n: return (float(n.replace('K','')), 'K')
 elif "M" in n: return (float(n.replace('M','')), 'M')
 elif "G" in n: return (float(n.replace('G','')), 'G')
 elif "T" in n: return (float(n.replace('T','')), 'T')
 else: return (0, 'E')

def normN(n):
 if "K" in n: return (float(n.replace('K','')), 'K')
 elif "M" in n: return (float(n.replace('M','')), 'M')
 elif "G" in n: return (float(n.replace('G','')), 'G')
 elif "T" in n: return (float(n.replace('T','')), 'T')
 else: return (n, 'N')

def toN(n):
  if "K" in n[1]: return (int(round(n[0] * 10**3)))
  elif "M" in n[1]: return (int(round(n[0] * 10**6)))
  elif "G" in n[1]: return (int(round(n[0] * 10**9)))
  elif "T" in n[1]: return (int(round(n[0] * 10**12)))
  else: return n[0]

def zfs_pools():
    pools = [ re.split('\s+', line) for line in commands.getoutput("zpool list -H -o name,health").split("\n") ]
    pools = [ row[0] for row in pools ]
    return pools

def zpool_iostats(zpools):
  zpios = {}
  for p in zpools:
    zpios[p] = zpoolio_simple(p)
  return zpios

def zpoolio_simple(pool):
  zpio = {}
  output = commands.getoutput("zpool iostat %s 1 2 |tail -1" % pool)
  e = re.split("\s+", output)
  zpio[pool] = {'zpool': e[0], 'calloc': toMB(norm(e[1])), 'cfree':  toMB(norm(e[2])), 'oread': toN(normN(e[3])),
          'owrite': toN(normN(e[4])), 'bread': toN(normN(e[5])), 'bwrite': toN(normN(norm(e[6])), 'lread':  e[7], 'lwrite': e[8]}
  return zpio

zpools = zfs_pools()
zpools_fn = "/tmp/zpools.snmp.cache"

zpios = zpool_iostats(zpools)
zpios_fn =  "/tmp/zpios.snmp.cache"

json.dump(zpools, open(zpools_fn,'w'))
json.dump(zpios, open(zpios_fn, 'w'))

