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
tag = ""

time_data = {
    "P1_SEND": 0,
    "P1_RECV": 0,
    "P2_SEND": 0,
    "P2_RECV": 0,
    "P3_SEND": 0,
    "P3_RECV": 0,
    "P4_SEND": 0,
    "P4_RECV": 0
}


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
        if datas[0] == tag:
            time_data[datas[1]] = get_ts()


def update_thead(tag):
    sql = "UPDATE kw_data SET `P1_SEND` = '%s', `P1_RECV` = '%s', `P2_SEND` = '%s', `P2_RECV` = '%s'," \
          "`P3_SEND` = '%s', `P3_RECV` = '%s', `P4_SEND` = '%s', `P4_RECV` = '%s' WHERE `TAG` = '%s'" %\
          (time_data['P1_SEND'], time_data['P1_RECV'], time_data['P2_SEND'], time_data['P2_RECV'], time_data['P3_SEND'],
           time_data['P3_RECV'], time_data['P4_SEND'], time_data['P4_RECV'], tag)
    db.execute(sql)
    print sql


def get_ts():
    ts = datetime.utcnow()
    return str(ts.second).zfill(2) + str(ts.microsecond).zfill(6)


def clear_data():
    time_data['P1_SEND'] = 0;
    time_data['P1_RECV'] = 0;
    time_data['P2_SEND'] = 0;
    time_data['P2_RECV'] = 0;
    time_data['P3_SEND'] = 0;
    time_data['P3_RECV'] = 0;
    time_data['P4_SEND'] = 0;
    time_data['P4_RECV'] = 0;

os.system('arp -s 10.0.0.1 00:00:00:00:00:01')

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
    clear_data();

    tag = str(uuid.uuid1())
    sql = "INSERT INTO `kw_data` (`TAG`) VALUES ('%s')" % tag
    db.execute(sql)
    print sql

    time_data['P1_SEND'] = get_ts()
    socketClient.sendto(generate_data(tag, "P1_RECV"), serverAddress)

    time_data['P2_SEND'] = get_ts()
    socketClient.sendto(generate_data(tag, "P2_RECV"), serverAddress)

    time.sleep(1)

    time_data['P3_SEND'] = get_ts()
    socketClient.sendto(generate_data(tag, "P3_RECV"), serverAddress)

    time_data['P4_SEND'] = get_ts()
    socketClient.sendto(generate_data(tag, "P4_RECV"), serverAddress)

    time.sleep(3)
    update_thead(tag)

socketClient.close()
