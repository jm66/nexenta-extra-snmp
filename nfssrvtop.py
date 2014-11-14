#!/usr/bin/python

import commands, sys
import simplejson as json
from datetime import datetime

PRG = 'nfssvrtop'
TMPD = '/tmp/'
PERFD = '/perflogs/'

def doLock(lockf,dtime):
      lock = {'running': True, 'lastrun': dtime}
      json.dump(lock, open(lockf,'w'))

def checkLock(lockf):
   lock = {'running': None, 'lastrun': None}
   try:
      f = open(lockf,'r')
      lockj = json.load(f)
      # Lock file found and status is running
      return True if lockj['running'] else False
   except IOError:
      return False

def getNow():
   now = datetime.now()
   return now.strftime("%Y-%m-%d %H:%M:%S.%f")

def main():
   fname = PERFD+PRG+'.out'
   fjson = TMPD+PRG+'.snmp.cache'
   lockf = TMPD+PRG+'.lck'

   # lock file check
   sys.exit() if checkLock(lockf) else doLock(lockf, getNow())
   # lock file check

   line = commands.getoutput('tail -1 %s' %fname)
   d = json.loads(line)
   json.dump(d,open(fjson,'w'))

if __name__ == "__main__":
    main()

