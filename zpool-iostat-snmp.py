#!/usr/bin/python -u

from tools import json, sys, syslog, errno, time, socket, snmp
from tools.configuration import ZPOOLS_IOSTAT_BASE_OID as BASE_OID
from tools.configuration import ZPOOLS_IOSTAT_CACHE_FILE, POLLING_INTERVAL, MAX_RETRY
from tools import ZPool


def update_data():
    # Server info
    pp.add_str('2.1.0', socket.gethostname())
    with open(ZPOOLS_IOSTAT_CACHE_FILE) as cache_file:
        zpool_iostat_json = json.load(cache_file)
        #  pools
        pp.add_gau('2.2.0', len(zpool_iostat_json))
        zpools_iostat = list()
        # from json to list of obj
        for pool in zpool_iostat_json:
            temp_zpool_obj = ZPool()
            temp_zpool_obj.from_json(pool)
            zpools_iostat.append(temp_zpool_obj)
        # Disk IOs from JSON cache file
        for zpool in zpools_iostat:
            oid = pp.encode(zpool.label)
            pp.add_str('.'.join(['2.3.1', oid]), zpool.label)
            pp.add_gau('.'.join(['2.3.2', oid]), zpool.calloc)
            pp.add_gau('.'.join(['2.3.3', oid]), zpool.cfree)
            pp.add_gau('.'.join(['2.3.4', oid]), zpool.oread)
            pp.add_gau('.'.join(['2.3.5', oid]), zpool.owrite)
            pp.add_gau('.'.join(['2.3.6', oid]), zpool.bread)
            pp.add_gau('.'.join(['2.3.7', oid]), zpool.bwrite)
            pp.add_gau('.'.join(['2.3.8', oid]), zpool.lread)
            pp.add_gau('.'.join(['2.3.9', oid]), zpool.lwrite)
            pp.add_int('.'.join(['2.3.10', oid]), len(zpool.devices))
            pp.add_int('.'.join(['2.3.11', oid]), len(zpool.log))
            pp.add_int('.'.join(['2.3.12', oid]), len(zpool.cache))
            # ZPool Devices
            for device in zpool.devices:
                d_oid = pp.encode(device.label)
                pp.add_str('.'.join(['2.3.13.1', d_oid]), device.label)
                pp.add_str('.'.join(['2.3.13.2', d_oid]), zpool.label)
                pp.add_gau('.'.join(['2.3.13.3', d_oid]), device.oread)
                pp.add_gau('.'.join(['2.3.13.4', d_oid]), device.owrite)
                pp.add_gau('.'.join(['2.3.13.5', d_oid]), device.bread)
                pp.add_gau('.'.join(['2.3.13.6', d_oid]), device.bwrite)
                pp.add_gau('.'.join(['2.3.13.7', d_oid]), device.lread)
                pp.add_gau('.'.join(['2.3.13.8', d_oid]), device.lwrite)
            # ZPool Log Devices
            for l_device in zpool.log:
                l_oid = pp.encode(l_device.label)
                pp.add_str('.'.join(['2.3.14.1', l_oid]), l_device.label)
                pp.add_str('.'.join(['2.3.14.2', l_oid]), zpool.label)
                pp.add_gau('.'.join(['2.3.14.3', l_oid]), l_device.oread)
                pp.add_gau('.'.join(['2.3.14.4', l_oid]), l_device.owrite)
                pp.add_gau('.'.join(['2.3.14.5', l_oid]), l_device.bread)
                pp.add_gau('.'.join(['2.3.14.6', l_oid]), l_device.bwrite)
                pp.add_gau('.'.join(['2.3.14.7', l_oid]), l_device.lread)
                pp.add_gau('.'.join(['2.3.14.8', l_oid]), l_device.lwrite)
            # ZPool Cache Devices
            for c_device in zpool.cache:
                c_oid = pp.encode(c_device.label)
                pp.add_str('.'.join(['2.3.15.1', c_oid]), c_device.label)
                pp.add_str('.'.join(['2.3.15.2', c_oid]), zpool.label)
                pp.add_gau('.'.join(['2.3.15.3', c_oid]), c_device.oread)
                pp.add_gau('.'.join(['2.3.15.4', c_oid]), c_device.owrite)
                pp.add_gau('.'.join(['2.3.15.5', c_oid]), c_device.bread)
                pp.add_gau('.'.join(['2.3.15.6', c_oid]), c_device.bwrite)
                pp.add_gau('.'.join(['2.3.15.7', c_oid]), c_device.lread)
                pp.add_gau('.'.join(['2.3.15.8', c_oid]), c_device.lwrite)


def main():
    global pp
    # opening syslog
    syslog.openlog('Zpool-IOstat-snmp', 0, syslog.LOG_LOCAL0)
    # retries
    retry_timestamp = int(time.time())
    retry_counter = MAX_RETRY
    while retry_counter > 0:
        try:
            syslog.syslog(syslog.LOG_INFO, "Starting Zpool-IOstat monitoring... with base OID %s" % BASE_OID)
            pp = snmp.PassPersist(BASE_OID)
            pp.start(update_data, POLLING_INTERVAL)
        except KeyboardInterrupt:
            print "Exiting on user request."
            syslog.syslog(syslog.LOG_INFO, "Exiting")
            sys.exit(0)
        except IOError, e:
            if e.errno == errno.EPIPE:
                syslog.syslog(syslog.LOG_INFO, "SNMPD has closed the pipe, exiting...")
                sys.exit(0)
            else:
                syslog.syslog(syslog.LOG_WARNING, "Updater thread died: IOError: %s" % e)
        except Exception, e:
            syslog.syslog(syslog.LOG_WARNING, "Main thread died: %s: %s" % (e.__class__.__name__, e))

        syslog.syslog(syslog.LOG_WARNING, "Restarting monitoring in 15 sec...")
        # Errors frequency detection
        now = int(time.time())
        if (now - 3600) > retry_timestamp: 	# If the previous error is older than 1H
            retry_counter = MAX_RETRY       # Reset the counter
        else:
            retry_counter -= 1 				# Else countdown

        retry_timestamp = now
    syslog.syslog(syslog.LOG_ERR, "Too many retries, aborting...")
    sys.exit(1)


# Start program
if __name__ == "__main__":
    main()
