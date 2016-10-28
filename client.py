import socket
import time
import threading
import uuid
import os
from datetime import datetime
from random import Random
from MySQL import *

default_encoding = 'utf-8'

db = MySQL()


def generate_data(tag, no):
    result = tag + "," + no + "#"
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    data_length = 1456 - len(result)
    for i in range(data_length):
        result += chars[random.randint(0, length)]
    return result


def receive_thread():
    while True:
        data, clintAddress = socketServer.recvfrom(2048)
        datas = data.split(",")
        update_thead(datas[0], datas[1], get_ts())


def update_thead(tag, key, value):
    print sql
    thread = threading.Thread(target=do_update_thead, args=(tag, key, value))
    thread.start()


def do_update_thead(tag, key, value):
    sql = "UPDATE kw_data SET `%s` = '%s' WHERE `TAG` = '%s'" % (key, value, tag)
    db.execute(sql)
    print sql


def get_ts():
    ts = datetime.utcnow()
    return str(ts.second).zfill(2) + str(ts.microsecond).zfill(6)


os.system('arp -s 10.0.0.1 00:00:00:00:00:01]]]]')

serverAddress = ('10.0.0.1', 9270)
listenAddress = ('10.0.0.2', 9271)
socketServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketServer.bind(listenAddress)
socketClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

t = threading.Thread(target=receive_thread, args=())
t.start()

while True:
    os.system('ovs-ofctl del-flows s1')
    os.system('ovs-ofctl del-flows s2')

    time.sleep(1)

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

socketClient.close()
