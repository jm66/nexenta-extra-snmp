ZPOOLS_CACHE_FILE = "/tmp/zpool.cache"
ZPOOLS_IO_CACHE_FILE = "/tmp/zpoolio.cache"
ZPOOLS_IO_BASE_OID = ".1.3.6.1.4.1.25359.9"
ZPOOLS_COMMAND = "zpool list -H -o name,health | awk '{print $1}'"
ZPOOLS_DETAILED_COMMAND = "zpool status %s"
ZPOOLS_IO_COMMAND = 'zpool iostat %s 1 2 |tail -1'
ZPOOLS_IO_COMMAND_EXT = "zpool iostat -v %s 1 2| sed '1,3d;$d'"

# IOStat
IOSTAT_CACHE_FILE = "/tmp/iostat.cache"
IOSTAT_BASE_OID = '.1.3.6.1.4.1.25359.12'
IOSTAT_COMMAND = "iostat -xn 1 2 | awk \'n > 1 { print ; next } $NF == \"device\" { n++ }\'"
