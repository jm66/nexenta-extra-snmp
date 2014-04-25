#!/usr/bin/python

import sys, commands, re
import simplejson as json

def kstat(name):
    output = commands.getoutput("kstat -p " + name)
    try:
        return int(re.split("\s+", output)[1])
    except:
        return 0

# ZFS stats
def zfs_arc_size():
    return kstat("zfs:0:arcstats:size") / 1024 # KB

def zfs_arc_data():
    return kstat("zfs:0:arcstats:data_size") / 1024 # KB

def zfs_arc_meta():
    return kstat("zfs:0:arcstats:meta_used") / 1024 # KB

def zfs_arc_hits():
    return kstat("zfs:0:arcstats:hits") % 2**32 # 32 bit counter

def zfs_arc_misses():
    return kstat("zfs:0:arcstats:misses") % 2**32 # 32 bit counter

def zfs_arc_c():
    return kstat("zfs:0:arcstats:c") / 1024 # KB

def zfs_arc_p():
    return kstat("zfs:0:arcstats:p") / 1024 # KB  

def zfs_read():
    return kstat("unix:0:vopstats_zfs:read_bytes") / 1024 % 2**32 # 32 bit KB counter

def zfs_readdir():
    return kstat("unix:0:vopstats_zfs:readdir_bytes") / 1024 % 2**32 # 32 bit KB counter

def zfs_write():
    return kstat("unix:0:vopstats_zfs:write_bytes") / 1024 % 2**32 # 32 bit KB counter

def zfs_l2arc_hits():
    return kstat("zfs:0:arcstats:l2_hits") % 2**32 # 32 bit counter

def zfs_l2arc_misses():
    return kstat("zfs:0:arcstats:l2_misses") % 2**32 # 32 bit counter

def zfs_l2arc_write():
    return kstat("zfs:0:arcstats:l2_write_bytes") / 1024 % 2**32 # 32 bit KB counter

def zfs_l2arc_read():
    return kstat("zfs:0:arcstats:l2_read_bytes") / 1024 % 2**32 # 32 bit KB counter

# Per pool data
def zfs_used_avail(fs):
    return [ int(x) / 1024 for x in commands.getoutput("zfs get -Hpo value used,available " + fs).split("\n")]

def zfs_used(fs, divisor=1):
    return zfs_used_avail(fs)[0] / divisor

def zfs_avail(fs, divisor=1):
    return zfs_used_avail(fs)[1] / divisor

def zfs_size(fs, divisor=1):
    return (zfs_used_avail(fs)[0] + zfs_used_avail(fs)[1]) / divisor

def zfs_vols():
    vols = [ re.split('\s+', line) for line in commands.getoutput("zfs list -H -t volume").split("\n")]
    vols = [ ( row[0] ) for row in vols ]
    return vols

def zfs_pools():
    statuses = { "ONLINE": 1, "DEGRADED": 2, "FAULTED": 3 }
    pools = [ re.split('\s+', line) for line in commands.getoutput("zpool list -H -o name,health").split("\n") ]
    pools = [ ( row[0], statuses.get(row[1], 4) ) for row in pools ]
    return pools

def zfs_fss():
   fss = [ re.split('\s+', line) for line in commands.getoutput("zfs list -H -t filesystem").split("\n")]
   fss = [ ( row[0] ) for row in fss ]
   return fss 

zpools = zfs_pools()
zvols = zfs_vols()
zfss = zfs_fss()

zfs_stats = { 'arc_size': None, 'arc_data': None, 'arc_meta': None, 'arc_hits': None, 'arc_misses': None,
              'arc_c': None, 'arc_p': None,  'read': None, 'readdir': None, 'write': None, 'l2arc_hits': None,
              'l2arc_misses': None, 'l2arc_write': None, 'l2arc_read': None, 'pools': None, 'vols': None, 'fss': None }

zfs_stats['arc_size'] = zfs_arc_size()
zfs_stats['arc_data'] = zfs_arc_data()
zfs_stats['arc_meta'] = zfs_arc_meta()
zfs_stats['arc_hits'] = zfs_arc_hits()
zfs_stats['arc_misses'] = zfs_arc_misses()
zfs_stats['arc_c'] = zfs_arc_c()
zfs_stats['arc_p'] = zfs_arc_p()
zfs_stats['read'] = zfs_read()
zfs_stats['readdir'] = zfs_readdir()
zfs_stats['write']= zfs_write()
zfs_stats['l2arc_hits'] = zfs_l2arc_hits()
zfs_stats['l2arc_misses'] = zfs_l2arc_misses()
zfs_stats['l2arc_write'] = zfs_l2arc_write()
zfs_stats['l2arc_read'] = zfs_l2arc_read()

pools = {}
for p, h in zpools:
  pools[p] = { 'name': p ,'health': h, 'used_avail': zfs_used_avail(p) ,'used': zfs_used(p, 1024) ,'avail': zfs_avail(p, 1024), 'size': zfs_size(p, 1024)}

vols = {}
for p in zvols:
  vols[p] = { 'name': p , 'used_avail': zfs_used_avail(p) ,'used': zfs_used(p, 1024) ,'avail': zfs_avail(p, 1024), 'size': zfs_size(p, 1024)}

fss = {}
for p in zfss:
  fss[p] = { 'name': p , 'used_avail': zfs_used_avail(p) ,'used': zfs_used(p, 1024) ,'avail': zfs_avail(p, 1024), 'size': zfs_size(p, 1024)}

zfs_stats['pools'] = pools
zfs_stats['vols'] = vols
zfs_stats['fss'] = fss


zfsfs_fn = "/tmp/zfss_full.snmp.cache"
zvols_fn = "/tmp/zvols_full.snmp.cache"
zpools_fn = "/tmp/zpools_health.snmp.cache"
zfs_stats_fn = "/tmp/zfs_stats.snmp.cache"

json.dump(fss, open(zfsfs_fn, 'w'))
json.dump(zpools, open(zpools_fn,'w'))
json.dump(zvols, open(zvols_fn, 'w'))
json.dump(zfs_stats, open(zfs_stats_fn, 'w'))


