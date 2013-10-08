This is a small script to add additional useful variables for SNMP monitoring
under Solaris. It's known to be compatible with Solaris 10/11 Express, Solaris 10/11,
and recently tested on NexentaStor 3.1.3.x.

When deployed, it provides the following additional information:

    NYMNETWORKS-MIB::zfsFilesystemName.1 = STRING: "syspool"
    NYMNETWORKS-MIB::zfsFilesystemName.2 = STRING: "server-vol1"
    NYMNETWORKS-MIB::zfsFilesystemAvailableKB.1 = Gauge32: 444020639
    NYMNETWORKS-MIB::zfsFilesystemAvailableKB.2 = Gauge32: 4294967295
    NYMNETWORKS-MIB::zfsFilesystemUsedKB.1 = Gauge32: 129878112
    NYMNETWORKS-MIB::zfsFilesystemUsedKB.2 = Gauge32: 4294967295
    NYMNETWORKS-MIB::zfsPoolHealth.1 = INTEGER: online(1)
    NYMNETWORKS-MIB::zfsPoolHealth.2 = INTEGER: online(1)
    NYMNETWORKS-MIB::zfsFilesystemSizeKB.1 = Gauge32: 573898751
    NYMNETWORKS-MIB::zfsFilesystemSizeKB.2 = Gauge32: 4294967295
    NYMNETWORKS-MIB::zfsFilesystemAvailableMB.1 = Gauge32: 433613
    NYMNETWORKS-MIB::zfsFilesystemAvailableMB.2 = Gauge32: 10867977
    NYMNETWORKS-MIB::zfsFilesystemUsedMB.1 = Gauge32: 126834
    NYMNETWORKS-MIB::zfsFilesystemUsedMB.2 = Gauge32: 7840502
    NYMNETWORKS-MIB::zfsFilesystemSizeMB.1 = Gauge32: 560447
    NYMNETWORKS-MIB::zfsFilesystemSizeMB.2 = Gauge32: 18708479
    NYMNETWORKS-MIB::zfsARCSizeKB.0 = Gauge32: 120084804
    NYMNETWORKS-MIB::zfsARCMetadataSizeKB.0 = Gauge32: 0
    NYMNETWORKS-MIB::zfsARCDataSizeKB.0 = Gauge32: 119074236
    NYMNETWORKS-MIB::zfsARCHits.0 = Counter32: 440763384
    NYMNETWORKS-MIB::zfsARCMisses.0 = Counter32: 6666959
    NYMNETWORKS-MIB::zfsARCTargetSize.0 = Gauge32: 120085188
    NYMNETWORKS-MIB::zfsARCMru.0 = Gauge32: 25684130
    NYMNETWORKS-MIB::zfsL2ARCHits.0 = Counter32: 0
    NYMNETWORKS-MIB::zfsL2ARCMisses.0 = Counter32: 0
    NYMNETWORKS-MIB::zfsL2ARCReads.0 = Counter32: 0
    NYMNETWORKS-MIB::zfsL2ARCWrites.0 = Counter32: 0
    NYMNETWORKS-MIB::zfsReadKB.0 = Counter32: 784738816
    NYMNETWORKS-MIB::zfsReaddirKB.0 = Counter32: 893528
    NYMNETWORKS-MIB::zfsWriteKB.0 = Counter32: 475031744
    NYMNETWORKS-MIB::zfsVolumeName.3 = STRING: "syspool/dump"
    NYMNETWORKS-MIB::zfsVolumeName.4 = STRING: "syspool/swap"
    NYMNETWORKS-MIB::zfsVolumeAvailableKB.3 = Gauge32: 444020637
    NYMNETWORKS-MIB::zfsVolumeAvailableKB.4 = Gauge32: 445102477
    NYMNETWORKS-MIB::zfsVolumeUsedKB.3 = Gauge32: 93955840
    NYMNETWORKS-MIB::zfsVolumeUsedKB.4 = Gauge32: 1081856
    NYMNETWORKS-MIB::zfsVolumeSizeKB.3 = Gauge32: 537976477
    NYMNETWORKS-MIB::zfsVolumeSizeKB.4 = Gauge32: 446184333
    NYMNETWORKS-MIB::zfsVolumeSizeKB.10 = Gauge32: 4294967295
    NYMNETWORKS-MIB::zfsVolumeAvailableMB.3 = Gauge32: 433613
    NYMNETWORKS-MIB::zfsVolumeAvailableMB.4 = Gauge32: 434670
    NYMNETWORKS-MIB::zfsVolumeUsedMB.3 = Gauge32: 91753
    NYMNETWORKS-MIB::zfsVolumeUsedMB.4 = Gauge32: 1056
    NYMNETWORKS-MIB::zfsVolumeSizeMB.3 = Gauge32: 525367
    NYMNETWORKS-MIB::zfsVolumeSizeMB.4 = Gauge32: 435726


With this information, you can graph ZFS ARC size and hit rate, ZFS IO rate and
ZFS L2ARC hit rate and IO rate. Have a look in the MIB or in the source for
more detailed descriptions of the individual variables. 

If you add the `ipmi-snmp` script, you'll get a basic temperature reading:

    NYMNETWORKS-MIB::tempSensorName.0 = STRING: "System Temp"
    NYMNETWORKS-MIB::tempSensorValue.0 = Gauge32: 20

If you have a NUT installation and add the `nut-snmp` script, youll get some
basic UPS stats:

    NYMNETWORKS-MIB::upsId.1 = STRING: "smartups"
    NYMNETWORKS-MIB::upsModel.1 = STRING: "Smart-UPS 750"
    NYMNETWORKS-MIB::upsManufacturer.1 = STRING: "American Power Conversion"
    NYMNETWORKS-MIB::upsSerial.1 = STRING: "AS1141221798"
    NYMNETWORKS-MIB::upsBatteryChargePercent.1 = Gauge32: 100
    NYMNETWORKS-MIB::upsBatteryRuntimeSec.1 = Gauge32: 2340
    NYMNETWORKS-MIB::upsBatteryVoltagedV.1 = Gauge32: 275
    NYMNETWORKS-MIB::upsBatteryNominalVoltagedV.1 = Gauge32: 240
    NYMNETWORKS-MIB::upsBatteryType.1 = STRING: "PbAc"
    NYMNETWORKS-MIB::upsStatus.1 = STRING: "OL"

To use, drop the scripts

    snmpresponse.py
    zfs-snmp
    ipmi-snmp
    nut-snmp

in for example `/opt/solaris-extra-snmp`, add the following to `/etc/sma/snmp/snmpd.conf`:

    # ZFS - Solaris extra OIDs
    pass .1.3.6.1.4.1.25359.1 /opt/solaris-extra-snmp/zfs-snmp
    pass .1.3.6.1.4.1.25359.2 /opt/solaris-extra-snmp/ipmi-snmp # Optional, for IPMI
    pass .1.3.6.1.4.1.25359.3 /opt/solaris-extra-snmp/nut-snmp # Optional, for NUT/UPS
    pass .1.3.6.1.4.1.25359.5 /opt/solaris-extra-snmp/net-snmp # Optional, for IPNet Stats

Restart snmp agent via sma
    
    svcadm disable svc:/application/management/sma:default
    svcadm disable svc:/application/management/snmpdx:default
    svcadm enable svc:/application/management/sma:default
    svcadm enable svc:/application/management/snmpdx:default

Try it via snmpwalk

    /usr/sfw/bin/snmpwalk -v 2c -m ALL -c public localhost 1.3.6.1.4.1.25359.1

License
-------

2-Clause BSD


