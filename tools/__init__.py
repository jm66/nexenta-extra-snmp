try:
    import simplejson as json
except ImportError:
    import json
import sys
import syslog
import errno
import time
import socket
import snmp_passpersist as snmp


class IODevice(object):
    # r/s    w/s   kr/s   kw/s wait actv wsvc_t asvc_t  %w  %b device
    def __init__(self):
        self.device = None
        self.reads_ps = None
        self.writes_ps = None
        self.KB_read_ps = None
        self.KB_written_ps = None
        self.wait = None
        self.actv = None
        self.wsvc_t = None
        self.asvc_t = None
        self.wait_pct = None
        self.busy_pct = None

    def __repr__(self):
        return "<%s>" % self.device

    def to_json(self):
        return {'device': self.device,
                'reads_ps': self.reads_ps,
                'writes_ps': self.writes_ps,
                'KB_read_ps': self.KB_read_ps,
                'KB_written_ps': self.KB_written_ps,
                'wait': self.wait,
                'actv': self.actv,
                'wsvc_t': self.wsvc_t,
                'asvc_t': self.asvc_t,
                'wait_pct': self.wait_pct,
                'busy_pct': self.busy_pct}

    def from_json(self, iodevice):
        self.device = iodevice['device']
        self.reads_ps = iodevice['reads_ps']
        self.writes_ps = iodevice['writes_ps']
        self.KB_written_ps = iodevice['KB_written_ps']
        self.KB_read_ps = iodevice['KB_read_ps']
        self.wait = iodevice['wait']
        self.actv = iodevice['actv']
        self.wsvc_t = iodevice['wsvc_t']
        self.asvc_t = iodevice['asvc_t']
        self.wait_pct = iodevice['wait_pct']
        self.busy_pct = iodevice['busy_pct']


class ZPoolDevice(object):
    def __init__(self):
        self.label = None
        # IOstat
        self.calloc = None
        self.cfree = None
        self.oread = None
        self.owrite = None
        self.bread = None
        self.bwrite = None
        self.lread = None
        self.lwrite = None

    def from_values(self, label, calloc, cfree, oread, owrite,
                   bread, bwrite, lread, lwrite):
        self.label = label
        self.calloc = calloc
        self.cfree = cfree
        self.oread = oread
        self.owrite = owrite
        self.bread = bread
        self.bwrite = bwrite
        self.lread = lread
        self.lwrite = lwrite


    def to_json(self):
        return {'label': self.label,
                'capacity_alloc': self.calloc,
                'capacity_free': self.cfree,
                'operations_read': self.oread,
                'operations_write': self.owrite,
                'bandwidth_read': self.bread,
                'bandwidth_write': self.bwrite,
                'latency_read': self.lread,
                'latency_write': self.lwrite}

    def from_json(self, device):
        self.label = device['label']
        self.calloc = device['capacity_alloc']
        self.cfree = device['capacity_free']
        self.oread = device['operations_read']
        self.owrite = device['operations_write']
        self.bread = device['bandwidth_read']
        self.bwrite = device['bandwidth_write']
        self.lread = device['latency_read']
        self.lwrite = device['latency_write']


class ZPool(ZPoolDevice):
    def __init__(self):
        super(ZPool, self).__init__()
        self.devices = list()  # list of ZpoolDevice
        self.cache = list()    # list of ZpoolDevice
        self.log = list()      # list of ZpoolDevice

    def to_json(self):
        return {'label': self.label,
                'capacity_alloc': self.calloc,
                'capacity_free': self.cfree,
                'operations_read': self.oread,
                'operations_write': self.owrite,
                'bandwidth_read': self.bread,
                'bandwidth_write': self.bwrite,
                'latency_read': self.lread,
                'latency_write': self.lwrite,
                'devices': [dev.to_json() for dev in self.devices],
                'cache': [dev.to_json() for dev in self.cache],
                'log': [dev.to_json() for dev in self.log]
                }
