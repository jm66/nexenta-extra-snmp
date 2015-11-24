EIS_OID = '.1.3.6.1.4.1.6973'
STORAGE_OID = EIS_OID + '.1'  # .1.3.6.1.4.1.6973.1
STORAGE_MIB = 'iso.org.dod.internet.private.enterprises.eis.storage'
POLLING_INTERVAL = 3
MAX_RETRY = 10				# Number of successives retry in case of error
LOG_FILE = '/var/log/snmp-passpersist.log'

# IOStat
IOSTAT_BASE_OID = STORAGE_OID + '.1'  # .1.3.6.1.4.1.6973.1.1
IOSTAT_CACHE_FILE = "/tmp/iostat.cache"
IOSTAT_COMMAND = "iostat -xn 1 2 | awk \'n > 1 { print ; next } $NF == \"device\" { n++ }\'"

ZPOOLS_IOSTAT_BASE_OID = STORAGE_OID + '.3'
ZPOOLS_IOSTAT_CACHE_FILE = "/tmp/zpool.iostat.cache"
ZPOOLS_COMMAND = "zpool list -H -o name,health | awk '{print $1}'"
ZPOOLS_IOSTAT_COMMAND_EXT = "zpool iostat -v %s 1 2 |  awk 'n > 1 { print ; next } $NF == \"write\" { n++ }'"


