from scapy.all import *
from datetime import datetime
import os
from MySQL import *
import time

db = MySQL()


def random_mac():
    mac = [0x52, 0x54, 0x00,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def get_ts():
    ts = datetime.utcnow()
    return str(ts.second).zfill(2) + str(ts.microsecond).zfill(6)

while True:
    mac = random_mac()

    os.system("ifconfig h2-eth0 down")
    os.system("ifconfig h2-eth0 hw ether " + mac)
    os.system("ifconfig h2-eth0 up")

    time.sleep(1)

    icmp = IP(dst="10.0.0.1") / ICMP()

    t1 = get_ts()
    sr(icmp)
    t2 = get_ts()

    time.sleep(1)

    t3 = get_ts()
    sr(icmp)
    t4 = get_ts()

    sql = "INSERT INTO kw_icmp(`MAC`, `T1`, `T2`, `T3`, `T4`) VALUES('%s', %s, %s, %s, %s)" % (mac, t1, t2, t3, t4)

    db.execute(sql)
    print "%s: %s, %s, %s, %s" % (mac, t1, t2, t3, t4)

    time.sleep(2)
