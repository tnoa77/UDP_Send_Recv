import socket
import time
import threading
import uuid
import os
from datetime import datetime
from random import Random
from MySQL import *

default_encoding = 'utf-8'


def generate_data(tag, no):
    result = tag + "," + no + "#"
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    data_length = 1458 - len(result)
    for i in range(data_length):
        result += chars[random.randint(0, length)]
    return result


def receive_thread():
    while True:
        data, clintAddress = socketServer.recvfrom(2048)
        datas = data.split(",")
        update_thead(datas[0], datas[1], get_ts())


def update_thead(tag, key, value):
    sql = "UPDATE kw_data SET `%s` = '%s' WHERE `TAG` = '%s'" % (key, value, tag)
    db.execute(sql)
    print sql


def get_ts():
    ts = datetime.utcnow()
    return str(ts.minute).zfill(2) + str(ts.second).zfill(2) + str(ts.microsecond).zfill(6)


serverAddress = ('127.0.0.1', 9250)
listenAddress = ('127.0.0.1', 9251)
socketServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketServer.bind(listenAddress)
socketClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

db = MySQL()
t = threading.Thread(target=receive_thread, args=())
t.start()

# while start

# CLEAR
os.system('ovs-ofctl del-flows s1')
os.system('ovs-ofctl del-flows s2')

tag = str(uuid.uuid1())
sql = "INSERT INTO `kw_data` (`TAG`) VALUES ('%s')" % tag
db.execute(sql)
print sql

update_thead(tag, 'P1_SEND', get_ts())
socketClient.sendto(generate_data(tag, "P1_RECV"), serverAddress)

update_thead(tag, 'P2_SEND', get_ts())
socketClient.sendto(generate_data(tag, "P2_RECV"), serverAddress)

time.sleep(1)

update_thead(tag, 'P3_SEND', get_ts())
socketClient.sendto(generate_data(tag, "P3_RECV"), serverAddress)

update_thead(tag, 'P4_SEND', get_ts())
socketClient.sendto(generate_data(tag, "P4_RECV"), serverAddress)

time.sleep(2)

# while end

socketClient.close()
