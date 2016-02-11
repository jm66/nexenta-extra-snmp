# NexentaStor extra SNMP 
 
Python scripts to extend SNMP agent with custom data.

## Installation

1. Install ```nexenta-extra-snmp```

```
    cd /opt
    git clone git@gitlab.eis.utoronto.ca:vss/nexenta-extra-snmp.git
```

2. Install requirements:

```
    cd /opt/nexenta-extra-snmp
    pip install -r requirements.txt
```

## Usage

### IOstat

1. Add scripts which generate cache files in crontab:

```
    # running IOstat script every minute
    # will generate cache file in /tmp
    * * * * * /opt/nexenta-extra-snmp/iostat.py
```

2. Add counterpart multi-threaded script using pass_persist protocol to SNMPD via NMC ```setup network service snmp-agent edit-settings```

```    
    # IOstat SNMP script 
    pass_persist .1.3.6.1.4.1.6973.1.1 /opt/nexenta-extra-snmp/iostat-snmp.py
```

### Zpool IOstat

1. Add scripts which generate cache files in crontab:

```
    # running Zpool IOstat script every minute
    # will generate cache file in /tmp
    * * * * * /opt/nexenta-extra-snmp/zpool-iostat.py
```

2. Add counterpart multi-threaded script using pass_persist protocol to SNMPD via NMC ```setup network service snmp-agent edit-settings```

```    
    # Zpool IOstat SNMP script 
    pass_persist .1.3.6.1.4.1.6973.1.2 /opt/nexenta-extra-snmp/zpool-iostat-snmp.py
```

## Resources

* [Extend SNMP MIB with ZFS performance Counters](https://wiki.eis.utoronto.ca/display/VSS/Extend+SNMP+OID+with+ZFS+counters+on+Nexenta)
* [Monitor Nexenta with SNMP nad Cacti](https://wiki.eis.utoronto.ca/pages/viewpage.action?pageId=5406770)
