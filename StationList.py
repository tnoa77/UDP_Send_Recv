# encoding: utf-8
from urllib2 import *
from MySQL import *
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def get_station_list():
    conn = urlopen("https://kyfw.12306.cn/otn/resources/js/framework/station_name.js")
    station_list = conn.read()
    conn.close()
    station_list = station_list.replace("var station_names ='@", "")
    station_list = station_list.replace("';", "")
    station_list = station_list.split("@")

    db = MySQL()
    db.execute("TRUNCATE TABLE ct_station")
    for station in station_list:
        station = station.split("|")
        sql = "INSERT INTO `ct_station` (`PINCODE`, `NAME`, `TELCODE`, `PIN`, `PYSCODE`, `ORDER`) VALUES ('%s'," \
              " '%s','%s','%s','%s','%s')" % (station[0], station[1], station[2], station[3], station[4], station[5])
        db.execute(sql)
        print "正在采集车站信息，%s %s 添加成功" % (station[5], station[1])
    return