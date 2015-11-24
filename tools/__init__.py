try:
    import simplejson as json
except ImportError:
    import json
import sys
import syslog
import errno
import time
import socket

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
