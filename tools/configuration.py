ZPOOLS_CACHE_FILE = "/tmp/zpools.snmp.cache"
ZPOOLS_IO_CACHE_FILE = "/tmp/zpios.snmp.cache"
ZPOOLS_IO_BASE_OID = ".1.3.6.1.4.1.25359.9"
ZPOOLS_COMMAND = 'zpool list -H -o name,health'
ZPOOLS_IO_COMMAND = 'zpool iostat {} 1 2 |tail -1'

IOSTAT_CACHE_FILE = "/tmp/iostat.cache"
IOSTAT_BASE_OID = '.1.3.6.1.4.1.25359.12'
IOSTAT_COMMAND = "iostat -xn 1 2 | awk \'n > 1 { print ; next } $NF == \"device\" { n++ }\'"
