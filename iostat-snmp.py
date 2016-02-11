#!/usr/bin/python -u

from tools import json, sys, syslog, errno, time, socket, snmp
from tools.configuration import IOSTAT_BASE_OID as BASE_OID
from tools.configuration import IOSTAT_CACHE_FILE, POLLING_INTERVAL, MAX_RETRY


def update_data():
    # Server info
    pp.add_str('1.1.0', socket.gethostname())
    with open(IOSTAT_CACHE_FILE) as cache_file:
        iostat_json = json.load(cache_file)
        #  devices
        pp.add_gau('1.2.0', len(iostat_json))
        # Disk IOs from JSON cache file
        for io_device in iostat_json:
            oid = pp.encode(io_device['device'])
            pp.add_str('1.3.1.' + oid, io_device['device'])
            pp.add_gau('1.3.2.' + oid, int(io_device['reads_ps']))
            pp.add_gau('1.3.3.' + oid, int(io_device['writes_ps']))
            pp.add_gau('1.3.4.' + oid, int(io_device['KB_read_ps']))
            pp.add_gau('1.3.5.' + oid, int(io_device['KB_written_ps']))
            pp.add_gau('1.3.6.' + oid, int(io_device['wait']))
            pp.add_gau('1.3.7.' + oid, int(io_device['actv']))
            pp.add_gau('1.3.8.' + oid, int(io_device['wsvc_t']))
            pp.add_gau('1.3.9.' + oid, int(io_device['asvc_t']))
            pp.add_gau('1.3.10.' + oid,  int(io_device['wait_pct']))
            pp.add_gau('1.3.11.' + oid,  int(io_device['busy_pct']))


def main():
    global pp
    # opening syslog
    syslog.openlog('IOstat-snmp', 0, syslog.LOG_LOCAL0)
    # retries
    retry_timestamp = int(time.time())
    retry_counter = MAX_RETRY
    while retry_counter > 0:
        try:
            syslog.syslog(syslog.LOG_INFO, "Starting IOstat monitoring... with base OID %s" % BASE_OID)
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
